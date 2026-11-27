# Аудит вашого налаштування context engineering

> Самодостатній prompt, що вимірює та покращує архітектуру контексту Claude Code.

**Автор**: [Florian BRUNIAUX](https://github.com/FlorianBruniaux) | Fractional Chief AI Officer

**Еталон**: [The Ultimate Claude Code Guide](https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md)

---

## 1. Що це робить

Цей prompt доручає Claude провести аудит вашого налаштування context engineering:

1. **Вимірювання** загального розміру постійного (always-on) контексту, довжини CLAUDE.md і частки правил з обмеженням за шляхами
2. **Виявлення** балансу skills і правил, надлишковості, а також негативних проти позитивних інструкцій
3. **Позначення** ознак застарілості (дата останнього оновлення, зламані імпорти, застарілі посилання)
4. **Оцінювання** за 8 вимірами із загальною сумою /100 та пріоритезованими рекомендаціями

**Продуктивність**: використовує bash/grep для ефективного сканування. Claude читає файли лише тоді, коли потрібен аналіз конкретного вмісту.

**Важливо**: Claude НЕ вноситиме жодних змін без вашого явного схвалення.

---

## 2. Для кого це

| Рівень | Що ви отримаєте |
|-------|-------------|
| **Розробник-одинак** | Швидкі перемоги: скоротити роздуття, додати відсутні розділи, виправити застарілі імпорти |
| **Мала команда (2-10)** | Виявити прогалини в узгодженості та можливості для збірки на основі профілів |
| **Велика команда (10+)** | Систематична оцінка архітектури контексту з оцінкою зрілості |

**Передумови**:
- Встановлений і робочий Claude Code
- Проєкт принаймні з CLAUDE.md або каталогом `.claude/`
- Оболонка Bash (нативна на macOS/Linux, WSL на Windows)

**Час**: ~3-5 хвилин

---

## 3. Як користуватися

### Крок 1: Скопіюйте prompt

Скопіюйте весь вміст блоку коду в [розділі 4](#4-prompt) нижче.

### Крок 2: Запустіть Claude Code

```bash
cd your-project-directory
claude
```

### Крок 3: Вставте та виконайте

Вставте prompt і натисніть Enter. Claude розпочне аудит.

### Крок 4: Перегляньте результати

Claude представить висновки, а потім попросить підтвердження перед внесенням будь-яких змін.

### Примітка щодо платформи

| Платформа | Шлях до глобальної конфігурації |
|----------|-------------------|
| **macOS/Linux** | `~/.claude/` |
| **Windows** | `%USERPROFILE%\.claude\` |

---

## 4. Prompt

```markdown
# Audit My Context Engineering Setup

## Контекст

Виконай комплексний аудит context engineering моєї конфігурації Claude Code.
Зосередься на розмірі контексту, якості структури, актуальності та масштабованості для команди.

Еталон: https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md

## Інструкції

### Фаза 1: Виявлення (сканування через Bash)

**ВАЖЛИВО**: у цій фазі використовуй виключно команди bash. Файли поки НЕ читай.

#### 1.1 Сканування розміру та структури

```bash
bash -c '
echo "=== GLOBAL CLAUDE.MD ==="
if [ -f ~/.claude/CLAUDE.md ]; then
  lines=$(wc -l < ~/.claude/CLAUDE.md | tr -d " ")
  chars=$(wc -c < ~/.claude/CLAUDE.md | tr -d " ")
  tokens=$(echo "scale=0; $chars / 4" | bc 2>/dev/null || echo "~$((chars/4))")
  echo "Lines: $lines"
  echo "Chars: $chars (~$tokens tokens)"
  echo "Imports: $(grep -c "^@" ~/.claude/CLAUDE.md 2>/dev/null || echo 0)"
  echo "Rules count: $(grep -cE "^[-*] |^\d+\. " ~/.claude/CLAUDE.md 2>/dev/null || echo 0)"
  echo "Last commit: $(cd ~/.claude && git log --format="%ar" -- CLAUDE.md 2>/dev/null | head -1 || echo "not tracked")"
else
  echo "NOT FOUND"
fi

echo ""
echo "=== PROJECT CLAUDE.MD ==="
for f in ./CLAUDE.md ./.claude/CLAUDE.md; do
  if [ -f "$f" ]; then
    lines=$(wc -l < "$f" | tr -d " ")
    chars=$(wc -c < "$f" | tr -d " ")
    tokens=$(echo "scale=0; $chars / 4" | bc 2>/dev/null || echo "~$((chars/4))")
    echo "File: $f"
    echo "Lines: $lines"
    echo "Chars: $chars (~$tokens tokens)"
    echo "Imports: $(grep -c "^@" "$f" 2>/dev/null || echo 0)"
    echo "Rules count: $(grep -cE "^[-*] |^\d+\. " "$f" 2>/dev/null || echo 0)"
    echo "Last commit: $(git log --format="%ar" -- "$f" 2>/dev/null | head -1 || echo "not tracked")"
  fi
done

echo ""
echo "=== IMPORTED FILES ==="
for f in ~/.claude/CLAUDE.md ./CLAUDE.md ./.claude/CLAUDE.md; do
  [ -f "$f" ] || continue
  while IFS= read -r line; do
    [[ "$line" =~ ^@ ]] || continue
    import_path="${line#@}"
    import_path="${import_path/ */}"
    resolved="${import_path/#\~/$HOME}"
    resolved="${resolved/#./$PWD}"
    if [ -f "$resolved" ]; then
      sz=$(wc -c < "$resolved" | tr -d " ")
      tk=$(echo "scale=0; $sz / 4" | bc 2>/dev/null || echo "$((sz/4))")
      echo "  FOUND $line (~$tk tokens)"
    else
      echo "  BROKEN $line (file not found)"
    fi
  done < "$f"
done

echo ""
echo "=== RULES & MODULES ==="
for d in ~/.claude ./.claude; do
  [ -d "$d" ] || continue
  for sub in rules skills commands agents hooks; do
    if [ -d "$d/$sub" ]; then
      count=$(find "$d/$sub" -maxdepth 1 -type f | wc -l | tr -d " ")
      total_chars=$(find "$d/$sub" -maxdepth 1 -type f -exec cat {} \; 2>/dev/null | wc -c | tr -d " ")
      tokens=$((total_chars / 4))
      echo "  $d/$sub: $count files (~$tokens tokens)"
    fi
  done
done
'
```

**Збережи вивід** для оцінювання.

#### 1.2 Сканування шаблонів якості

```bash
bash -c '
echo "=== NEGATIVE VS POSITIVE INSTRUCTIONS ==="
for f in ~/.claude/CLAUDE.md ./CLAUDE.md ./.claude/CLAUDE.md; do
  [ -f "$f" ] || continue
  neg=$(grep -ciE "never|do not|dont|avoid|prohibited|forbidden|not allowed|do NOT" "$f" 2>/dev/null || echo 0)
  pos=$(grep -ciE "always|prefer|use|should|must|recommended|do this" "$f" 2>/dev/null || echo 0)
  echo "$f: negative=$neg positive=$pos"
done

echo ""
echo "=== VAGUE INSTRUCTIONS (red flags) ==="
for f in ~/.claude/CLAUDE.md ./CLAUDE.md ./.claude/CLAUDE.md; do
  [ -f "$f" ] || continue
  echo "$f:"
  grep -inE "be careful|good practice|appropriately|as needed|when necessary|use your judgment|you should know|be smart" "$f" 2>/dev/null | head -5 || echo "  none found"
done

echo ""
echo "=== DUPLICATE SECTION HEADERS ==="
for f in ~/.claude/CLAUDE.md ./CLAUDE.md ./.claude/CLAUDE.md; do
  [ -f "$f" ] || continue
  dupes=$(grep -E "^#{1,3} " "$f" | sort | uniq -d)
  [ -n "$dupes" ] && echo "$f DUPLICATES: $dupes" || echo "$f: no duplicate headers"
done

echo ""
echo "=== DEPRECATED REFERENCES ==="
for f in ~/.claude/CLAUDE.md ./CLAUDE.md ./.claude/CLAUDE.md; do
  [ -f "$f" ] || continue
  echo "$f:"
  grep -niE "claude-1|claude-2\.0|claude-3-haiku-|gpt-3\.5|text-davinci|codex|copilot X|cursor pro 1\." "$f" 2>/dev/null | head -5 || echo "  none found"
done

echo ""
echo "=== PATH SCOPING (modular setup) ==="
for f in ~/.claude/CLAUDE.md ./CLAUDE.md ./.claude/CLAUDE.md; do
  [ -f "$f" ] || continue
  scoped=$(grep -cE "^@.+\.(ts|tsx|js|jsx|py|rs|go|md)$|globs:|path:" "$f" 2>/dev/null || echo 0)
  echo "$f path-scoped entries: $scoped"
done

echo ""
echo "=== SESSION & UPDATE PROTOCOL ==="
for f in ~/.claude/CLAUDE.md ./CLAUDE.md ./.claude/CLAUDE.md; do
  [ -f "$f" ] || continue
  has_update=$(grep -ciE "update|review|quarterly|maintenance|how to update|keep.*fresh" "$f" 2>/dev/null || echo 0)
  has_session=$(grep -ciE "session|retro|checkpoint|lesson learned|knowledge loop" "$f" 2>/dev/null || echo 0)
  echo "$f: update-protocol=$has_update session-retro=$has_session"
done

echo ""
echo "=== TEAM/PROFILE READINESS ==="
for f in ~/.claude/CLAUDE.md ./CLAUDE.md ./.claude/CLAUDE.md; do
  [ -f "$f" ] || continue
  has_profile=$(grep -ciE "profile|role:|junior|senior|lead|persona|persona-" "$f" 2>/dev/null || echo 0)
  has_module=$(grep -cE "^@" "$f" 2>/dev/null || echo 0)
  echo "$f: profile-mentions=$has_profile module-imports=$has_module"
done
'
```

**Збережи вивід** для оцінювання.

#### 1.3 Сканування актуальності та конфліктів

```bash
bash -c '
echo "=== GIT FRESHNESS ==="
for path in ~/.claude ./; do
  if git -C "$path" rev-parse --git-dir &>/dev/null 2>&1; then
    echo "Repo at $path:"
    git -C "$path" log --format="%ar %s" -- CLAUDE.md .claude/CLAUDE.md 2>/dev/null | head -3 || echo "  no commits for CLAUDE.md"
  fi
done

echo ""
echo "=== CONFLICTING RULES PATTERNS ==="
for f in ~/.claude/CLAUDE.md ./CLAUDE.md ./.claude/CLAUDE.md; do
  [ -f "$f" ] || continue
  echo "$f:"
  # Look for contradictory patterns like "always X" near "never X"
  always_terms=$(grep -ioE "always [a-z ]+" "$f" 2>/dev/null | sed "s/always //i" | sort)
  never_terms=$(grep -ioE "never [a-z ]+" "$f" 2>/dev/null | sed "s/never //i" | sort)
  conflicts=$(comm -12 <(echo "$always_terms") <(echo "$never_terms") 2>/dev/null)
  [ -n "$conflicts" ] && echo "  POTENTIAL CONFLICTS: $conflicts" || echo "  no obvious contradictions"
done

echo ""
echo "=== OVERVIEW / ARCHITECTURE SECTION ==="
for f in ~/.claude/CLAUDE.md ./CLAUDE.md ./.claude/CLAUDE.md; do
  [ -f "$f" ] || continue
  has_overview=$(grep -ciE "^## (overview|purpose|about|architecture|what this|context)" "$f" 2>/dev/null || echo 0)
  has_antip=$(grep -ciE "anti.pattern|bad example|do not do|wrong way|pitfall" "$f" 2>/dev/null || echo 0)
  has_hierarchy=$(grep -cE "^#{1,3} " "$f" 2>/dev/null || echo 0)
  echo "$f: has-overview=$has_overview anti-patterns=$has_antip section-count=$has_hierarchy"
done
'
```

**Збережи вивід** для оцінювання.

### Фаза 2: Оцінювання за 8 вимірами

Використовуй виводи сканування з Фази 1. Читай конкретні фрагменти файлів лише тоді, коли для звіту потрібні приклади вмісту.

#### Вимір 1: Розмір і бюджет (15 балів)

Оціни на основі оцінок токенів із Фази 1:

| Перевірка | Бали | Поріг |
|-----------|--------|-----------|
| Загальний always-on контекст менше 8K токенів | 5 | Сума всіх CLAUDE.md + імпорти |
| Кількість правил менше 150 інструкцій | 5 | глобальні + проєктні разом |
| Жоден окремий файл не перевищує 400 рядків | 5 | познач, якщо перевищено |

Знімай бали пропорційно, якщо пороги перевищено. Файл на 600 рядків = 3/5, а не 0.

#### Вимір 2: Структура (15 балів)

| Перевірка | Бали | Сигнал |
|-----------|--------|--------|
| Має розділ-огляд/призначення | 4 | h2 із "overview", "purpose", "about", "context" |
| Має розділ архітектури або структури проєкту | 3 | h2 із "architecture", "structure", "layout" |
| Містить антипатерни або погані приклади | 4 | "anti-pattern", "do not", "pitfall" |
| Кількість розділів свідчить про чітку ієрархію | 4 | 3+ окремих розділи h2 |

#### Вимір 3: Обмеження за шляхами (12 балів)

| Перевірка | Бали | Сигнал |
|-----------|--------|--------|
| Використовує @imports для модульного розбиття | 5 | щонайменше 2 рядки @import |
| Принаймні одне правило, специфічне для шляху або обмежене glob | 4 | globs: або розділ для конкретного файлу |
| Не монолітний файл (усі інструкції в одному блоці) | 3 | кілька файлів або розділів |

#### Вимір 4: Якість правил (15 балів)

| Перевірка | Бали | Сигнал |
|-----------|--------|--------|
| Співвідношення позитивних:негативних >= 2:1 | 5 | за лічильниками negative/positive |
| Не виявлено розпливчастих інструкцій | 5 | нуль "be careful", "as needed" тощо |
| Правила конкретні та дієві | 5 | оцінюється за вибіркою під час складання звіту |

#### Вимір 5: Актуальність (12 балів)

| Перевірка | Бали | Сигнал |
|-----------|--------|--------|
| CLAUDE.md закомічено протягом останніх 6 місяців | 5 | вивід git log |
| Немає посилань на застарілі інструменти/моделі | 4 | вивід сканування застарілого |
| Немає зламаних @imports | 3 | рядки BROKEN у скануванні імпортів |

#### Вимір 6: Готовність до командної роботи (10 балів)

| Перевірка | Бали | Сигнал |
|-----------|--------|--------|
| Має структуру на основі профілів або ролей | 4 | згадки профілів >= 1 |
| Імпорти модулів уможливлюють вибіркову збірку | 3 | module-imports >= 3 |
| Задокументований протокол оновлення для команди | 3 | update-protocol >= 1 |

#### Вимір 7: Виявлення конфліктів (11 балів)

| Перевірка | Бали | Сигнал |
|-----------|--------|--------|
| Суперечливих правил не виявлено | 5 | конфліктів немає за скануванням |
| Немає дубльованих заголовків розділів | 3 | дублікатів не знайдено |
| Патерн ретроспективи сесії або циклу знань | 3 | session-retro >= 1 |

#### Вимір 8: Цикл знань (10 балів)

| Перевірка | Бали | Сигнал |
|-----------|--------|--------|
| Задокументовано протокол оновлення/перегляду | 4 | update-protocol >= 1 |
| Є ретроспектива сесії або патерн lesson-learned | 3 | session-retro >= 1 |
| Контекст відстежується в git (змінами можна аудитувати) | 3 | сканування git-актуальності показує коміти |

#### Обчисли загальну оцінку

`Score = сума зароблених балів за всіма 8 вимірами`

### Фаза 3: Згенеруй звіт

Структуруй вивід точно так:

---

## Context Engineering Audit

### Score: [XX]/100

| Вимір | Бал | Примітки |
|-----------|-------|-------|
| Size & Budget | X/15 | загалом ~X токенів, X правил |
| Structure | X/15 | X розділів, є/немає огляду |
| Path-Scoping | X/12 | X імпортів, монолітно/модульно |
| Rule Quality | X/15 | X% позитивних, знайдено X розпливчастих |
| Freshness | X/12 | востаннє оновлено X, X зламаних імпортів |
| Team Readiness | X/10 | X профілів, протокол оновлення: так/ні |
| Conflict Detection | X/11 | X суперечностей, X дубльованих заголовків |
| Knowledge Loop | X/10 | відстежується в git: так/ні, ретро: так/ні |

### Context Budget
- Глобальний CLAUDE.md: ~X токенів
- Проєктний CLAUDE.md: ~X токенів
- @imports разом: ~X токенів
- Усього always-on: ~X токенів
- Кількість правил: X/150 інструкцій

### Priority Issues (виправ спершу)
1. [Проблема] — [конкретне виправлення з прикладом]
2. [Проблема] — [конкретне виправлення з прикладом]
3. [Проблема] — [конкретне виправлення з прикладом]

### Quick Wins (< 30 хв кожна)
- [Виправлення]: [що зробити і де]
- [Виправлення]: [що зробити і де]
- [Виправлення]: [що зробити і де]

### Maturity Level
[Обери один і поясни чому]

**Level 1 — Empty** (0-19): Немає структурованого контексту. Claude працює без жодних знань про проєкт.
**Level 2 — Basic** (20-39): CLAUDE.md існує, але він монолітний, застарілий або здебільшого з розпливчастих правил.
**Level 3 — Structured** (40-59): Чіткі розділи та імпорти, але бракує актуальності чи командних патернів.
**Level 4 — Optimized** (60-79): Модульний, з обмеженнями за шляхами, правила спершу позитивні, з відомою періодичністю оновлень.
**Level 5 — Engineering-Grade** (80-100): З урахуванням профілів, відстежується в git, без конфліктів, цикл знань активний.

### Ready-to-use Improvements

Надай 2-3 конкретні текстові блоки, які користувачі можуть вставити безпосередньо у свій CLAUDE.md.
Кожен блок має розв'язувати одну з Priority Issues, визначених вище. Формат:

**Improvement 1: [назва]**
File: `[шлях]` — додати [на початок/у розділ X/в кінець]
```
[точний текст для вставки]
```

**Improvement 2: [назва]**
File: `[шлях]` — додати [на початок/у розділ X/в кінець]
```
[точний текст для вставки]
```

---

### Фаза 4: Очікування підтвердження

**КРИТИЧНО**: НЕ створюй і НЕ змінюй жодних файлів без явного схвалення.

Після подання звіту запитай:

"Які покращення ви хотіли б, щоб я впровадив?

Варіанти:
- `all` — Застосувати всі готові покращення
- `1, 2` — Конкретні покращення за номером
- `priority` — Лише виправлення Priority Issues
- `none` — Залишити звіт лише для довідки

Вкажіть свій вибір:"

Дочекайся явної відповіді користувача, перш ніж щось робити.

## Формат виводу

Структуруй відповідь точно так:

1. **Таблиця оцінок** із розбивкою за вимірами
2. Підсумок **Context Budget**
3. **Priority Issues** (нумеровані, виправляти першими)
4. **Quick Wins** (маркований список, < 30 хв кожна)
5. **Maturity Level** з поясненням
6. **Ready-to-use Improvements** (текстові блоки, готові до вставки)
7. **Запит на підтвердження** (запитай перед впровадженням)
```

---

## 5. Чого очікувати

Ось приклад того, як виглядає звіт аудиту:

### Приклад таблиці оцінок

```
## Context Engineering Audit

### Score: 52/100

| Dimension | Score | Notes |
|-----------|-------|-------|
| Size & Budget | 10/15 | ~6,200 tokens total, 182 rules (over limit) |
| Structure | 9/15 | 4 sections, no anti-patterns section |
| Path-Scoping | 4/12 | 1 import, monolithic project CLAUDE.md |
| Rule Quality | 8/15 | 60% positive, 3 vague instructions found |
| Freshness | 9/12 | last commit 4 months ago, 1 broken import |
| Team Readiness | 3/10 | no profiles, no update protocol |
| Conflict Detection | 6/11 | 1 "always/never" contradiction, no duplicate headers |
| Knowledge Loop | 3/10 | not git tracked, no retro pattern |
```

### Приклад швидких перемог

```
Quick Wins (< 30 min each):
- Fix broken import: @~/.claude/TONE.md not found — update path or remove
- Add overview section: 2-line project description at top of CLAUDE.md
- Trim rule count: merge 3 formatting rules into one compressed block
```

---

## 6. Посібник з оцінювання

| Оцінка | Зрілість | Рекомендована дія |
|-------|----------|--------------------|
| **80-100** | Level 5: Engineering-Grade | Підтримувати щоквартальним переглядом |
| **60-79** | Level 4: Optimized | Усунути пріоритетні проблеми, дійти до 80 |
| **40-59** | Level 3: Structured | Присвятити сесію покращенню |
| **20-39** | Level 2: Basic | Рекомендовано перебудову, використати шаблон |
| **0-19** | Level 1: Empty | Почати з нуля зі скелетного шаблону |

---

## 7. Глосарій

| Термін | Визначення |
|------|-----------|
| **Always-on context** | Усе, що Claude завантажує до вашого першого повідомлення: файли CLAUDE.md плюс усі @imports |
| **@import** | Рядок, що починається з `@` у CLAUDE.md і завантажує інший файл у контекст |
| **Path-scoping** | Застосування правил лише до певних типів файлів або каталогів, а не глобально |
| **Rule quality** | Конкретність і дієвість інструкцій: розпливчасті правила марнують токени й збивають Claude з пантелику |
| **Knowledge loop** | Практика оновлення файлів контексту після сесій на основі того, що спрацювало, а що ні |
| **Profile assembly** | Поєднання різних модулів контексту для створення налаштувань під роль (junior, senior, reviewer) |
| **Staleness signal** | Ознаки того, що контекст застарів: зламані імпорти, застарілі назви моделей, немає історії git |
| **Conflict** | Два правила, що суперечать одне одному: Claude обере одне довільно, зазвичай хибне |
| **Monolithic CLAUDE.md** | Один великий файл з усіма інструкціями, без імпортів, без модульного розбиття |
| **Maturity level** | Шкала від 1 до 5, що вимірює витонченість context engineering від порожнього до інженерного рівня |

---

## 8. Типові проблеми

### "Token estimate seems off"

**Причина**: оцінка використовує chars/4 як грубе наближення для токенів у стилі GPT. Токенізатор Claude може дещо відрізнятися.

**Виправлення**: зосередьтеся на відносних числах і порогах, а не на абсолютній кількості токенів. Бюджет always-on у 8K є евристикою, а не жорстким обмеженням.

### "Score is low but Claude seems to work fine"

**Причина**: Claude працює і без context engineering: оцінка відображає оптимізацію, а не базову працездатність.

**Виправлення**: низька оцінка означає, що ви лишаєте продуктивність на столі. Кожна прогалина у вимірі додає когнітивне навантаження на сесію.

### "Broken import flagged but file exists"

**Причина**: розв'язання відносних шляхів відрізняється від фактичного робочого каталогу Claude під час запуску.

**Виправлення**: використовуйте абсолютні шляхи (`~/.claude/file.md`) для глобальних імпортів. Використовуйте шляхи відносно проєкту (`./docs/conventions.md`) для проєктних імпортів.

### "Profile-readiness flagged but I'm solo"

**Причина**: аудит перевіряє патерни масштабованості для команди незалежно від розміру команди.

**Виправлення**: збірка на основі профілів корисна й для розробників-одинаків під час перемикання контекстів (рецензування PR проти написання функцій проти налагодження). Для одинаків вона необов'язкова.

---

## 9. Пов'язані ресурси

- [The Ultimate Claude Code Guide](../guide/ultimate-guide.uk.md) - повний довідник
- [Audit Your Claude Code Setup](./audit-prompt.uk.md) - повний аудит конфігурації (agents, hooks, MCP, CI)
- [Cheatsheet](../guide/cheatsheet.uk.md) - швидка щоденна довідка
- [Claude Code Official Docs](https://docs.anthropic.com/en/docs/claude-code) - документація Anthropic
- [context-evaluator.ai](https://context-evaluator.ai) - аудит CLAUDE.md і AGENTS.md на основі LLM без встановлення: 17 ШІ-оцінювачів, автоматизоване виправлення через `.patch`. Доповнює цей prompt глибшим аналізом правило за правилом і іншим кутом оцінювання (LLM-as-judge проти bash-евристик).

---

*Востаннє оновлено: квітень 2026 | Версія 1.1*
