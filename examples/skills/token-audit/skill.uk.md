---
name: token-audit
description: "Аудит конфігурації Claude Code для вимірювання фіксованих накладних витрат токенів контексту та складання пріоритезованого плану дій. Використовуйте, коли впираєтеся в ліміти запитів, зазнаєте раннього стиснення контексту або після додавання великих конфігураційних файлів."
effort: medium
allowed-tools: Read Grep Glob Bash
---

# /token-audit: аудит токенів контексту

**Призначення**: виміряти, скільки токенів споживає ваша конфігурація Claude Code до початку будь-якого завдання користувача. Визначити найбільші джерела накладних витрат. Скласти конкретний план дій з оцінками економії.

**Коли використовувати**:
- Ви впираєтеся в ліміти запитів ще до кінця дня
- Сесії здаються повільними або контекст стискається рано
- Ви додали багато файлів правил і хочете знати реальну вартість
- Після великої зміни конфігурації

---

## Що ви виміряєте

| Компонент | Коли завантажується | Типовий діапазон |
|-----------|---------------------|------------------|
| `~/.claude/CLAUDE.md` + @imports | Завжди | 5-15K токенів |
| `CLAUDE.md` проєкту | Завжди | 2-8K токенів |
| `.claude/rules/*.md` | Завжди (усі файли) | 5-40K токенів |
| `MEMORY.md` | Завжди | 1-3K токенів |
| Системний промпт Claude Code | Завжди | ~7 500 токенів |
| Stdout hook-ів | На кожен виклик інструмента | змінний |
| Команди, агенти, skills | Лише під час виклику | 0 за замовчуванням |

Ключове спостереження: `.claude/rules/` завантажує кожен файл `.md` на початку сесії незалежно від релевантності. Команди й агенти завантажуються ліниво: вони коштують нуль, доки їх не викликано. Файли правил є найпоширенішим джерелом несподіваних накладних витрат.

---

## Крок 1 — виконайте вимірювання

Виконайте ці команди з кореня проєкту:

```bash
# Component sizes
echo "=== PROJECT CLAUDE.md ===" && wc -c CLAUDE.md 2>/dev/null || echo "none"

echo ""
echo "=== RULES FILES (sorted by size) ===" && find .claude/rules -name "*.md" 2>/dev/null \
  | xargs wc -c 2>/dev/null | sort -rn | head -20

echo ""
echo "=== GLOBAL ~/.claude ===" && ls -la ~/.claude/*.md 2>/dev/null \
  | awk '{print $5, $9}' | sort -rn
```

Потім обчисліть повний бюджет:

```bash
GLOBAL=$(cat ~/.claude/CLAUDE.md ~/.claude/*.md 2>/dev/null | wc -c)
PROJECT=$(wc -c < CLAUDE.md 2>/dev/null || echo 0)
RULES=$(find .claude/rules -name "*.md" 2>/dev/null | xargs cat 2>/dev/null | wc -c || echo 0)
MEMORY=$(find ~/.claude/projects -name "MEMORY.md" 2>/dev/null \
  | xargs grep -l "$(basename $(pwd))" 2>/dev/null | head -1 \
  | xargs wc -c 2>/dev/null | awk '{print $1}' || echo 0)
TOTAL=$(( GLOBAL + PROJECT + RULES + MEMORY + 30000 ))

echo "Global ~/.claude   : ~$(( GLOBAL / 4 )) tokens ($(( GLOBAL / 1000 ))K chars)"
echo "Project CLAUDE.md  : ~$(( PROJECT / 4 )) tokens"
echo "Rules (auto-loaded): ~$(( RULES / 4 )) tokens"
echo "MEMORY.md          : ~$(( MEMORY / 4 )) tokens"
echo "System prompt      : ~7,500 tokens"
echo "---"
echo "TOTAL fixed context: ~$(( TOTAL / 4 )) tokens"
echo "% of 200K window   : $(( TOTAL / 4 * 100 / 200000 ))%"
```

---

## Крок 2 — класифікуйте файли правил

Для кожного файлу в `.claude/rules/` визначте клас:

| Клас | Визначення | Дія |
|------|------------|-----|
| **ALWAYS** | Стосується більшості завдань (конвенції, формат виводу, безпека) | Лишити в автозавантаженні |
| **SOMETIMES** | Релевантний у 20-40% сесій | Лишити, якщо малий (<3K символів); завантажувати ліниво, якщо великий |
| **RARELY** | Релевантний у <10% сесій (Figma, Windows, дизайн-система) | Прибрати з автозавантаження |
| **NEVER** | Застарілий або покритий деінде | Видалити або заархівувати |

Запустіть цей промпт для класифікації:

```
Read every file in .claude/rules/. For each file, output a table row:

| File | Size (chars) | Class (ALWAYS/SOMETIMES/RARELY/NEVER) | Reasoning (one sentence) |

Sort by size descending within each class.
At the end, calculate: total chars that would leave the fixed context if all
RARELY and NEVER files were excluded. Convert to tokens (÷ 4).
```

---

## Крок 3 — проаудитуйте накладні витрати hook-ів

Hooks на `PreToolUse` і `PostToolUse` спрацьовують на кожен виклик інструмента. Кожен виклик додає свій stdout у контекст. Hook, що виводить 500 символів на 150 викликах інструментів за сесію = 75K символів ≈ 19K додаткових токенів.

Перевірте, що у вас є:

```bash
# List hooks by event type
python3 - << 'EOF'
import json, os
for path in [os.path.expanduser("~/.claude/settings.json"), ".claude/settings.json"]:
    if not os.path.exists(path): continue
    print(f"\n--- {path} ---")
    data = json.load(open(path))
    for event, hooks in data.get("hooks", {}).items():
        for h in hooks:
            cmd = h.get("command", "?")
            matcher = h.get("matcher", "*")
            print(f"  [{event}] matcher={matcher} → {cmd[:80]}")
EOF
```

Для кожного hook-а `PreToolUse` чи `PostToolUse` оцініть розмір його stdout, запустивши його вручну. Помножте на середню кількість викликів інструментів за сесію (видно в `/cost` після сесії).

**Червоні прапорці**:
- Hooks, що безумовно роблять `cat` файлів
- `git status` або `git log` на кожному виклику
- Багаторядковий вивід echo для налагодження, який так і не прибрали
- JSON-блоби, що вставляються як контекст

---

## Крок 4 — складіть план дій

Складіть пріоритезовану таблицю. Практичне правило: включайте лише дії, виконувані без зовнішньої інфраструктури (без RAG, векторних баз даних чи власних MCP-серверів).

| Дія | Оцінка економії токенів | Зусилля | Ризик |
|-----|------------------------|---------|-------|
| Прибрати файли RARELY з автозавантаження | залежить | 30 хв | Низький |
| Розділити великі правила на ядро + деталі | залежить | 1-2 год | Низький |
| Урізати stdout hook-ів до суттєвих полів | залежить | 1 год | Низький |
| Стиснути багатослівні правила (див. §8 context-engineering.md) | 20-30% правил | 1-2 год | Низький |
| Заархівувати застарілі записи MEMORY.md | 500-1K токенів | 30 хв | Низький |

---

## Крок 5 — питання про RAG

Ліниве завантаження через векторну базу даних (RAG) іноді пропонують як рішення. Чесно оцініть його, перш ніж братися:

1. Скільки токенів фіксованого контексту лишається після кроків 1-4? (Спершу виміряйте це.)
2. Чи виправданий RAG? Налаштування pgvector + власного MCP — це проєкт на 1-2 тижні.
3. Точка беззбитковості: якщо у вас 10 файлів правил у середньому по 3K символів, класифікація (30 хв) заощаджує стільки ж, скільки RAG. RAG окупається за 50+ файлів правил, де маршрутизація за наміром є єдиним масштабованим рішенням.

---

## Формат виводу

Після запуску аудиту складіть такий звіт:

```markdown
## Token Audit — [PROJECT] — [DATE]

### Budget Summary

| Component | Tokens | % of total |
|-----------|--------|------------|
| Global ~/.claude | X | Y% |
| Project CLAUDE.md | X | Y% |
| Rules (auto-loaded) | X | Y% |
| MEMORY.md | X | Y% |
| System prompt | 7,500 | Y% |
| **TOTAL** | **X** | **100%** |

Context window used before any task: X% of 200K

### Rules Classification

| File | Chars | Class | Action |
|------|-------|-------|--------|
| ... | ... | ALWAYS/SOMETIMES/RARELY | keep/lazy-load/remove |

### Hook Overhead

| Hook | Event | Est. stdout | Calls/session | Total tokens/session |
|------|-------|-------------|---------------|----------------------|
| ... | PreToolUse | X chars | ~Y | ~Z tokens |

### Action Plan

| Action | Savings | Effort | Risk |
|--------|---------|--------|------|
| ... | -X tokens | 30 min | Low |

**Total achievable without infrastructure**: -X tokens → from Y to Z (N% reduction)

### RAG Verdict

[One paragraph: remaining overhead after action plan, whether RAG is justified,
estimated setup cost vs savings.]
```

---

## Інтерпретація результатів

| Фіксований контекст | Оцінка |
|---------------------|--------|
| < 20K токенів | Здорово — термінових дій не потрібно |
| 20-40K токенів | Помірно — проведіть класифікацію, візьміть легкі перемоги |
| 40-60K токенів | Високо — аудит правил вартий одного пообіддя |
| > 60K токенів | Критично — ви спалюєте 30%+ вікна ще до будь-якого завдання |

Скорочення на 48% типове після першого проходу аудиту на сильно сконфігурованому проєкті без змін інфраструктури: достатньо прибрати рідковживані файли з автозавантаження.
