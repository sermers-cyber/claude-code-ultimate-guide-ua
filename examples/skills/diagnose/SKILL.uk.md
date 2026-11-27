---
name: diagnose
description: Інтерактивний помічник для усунення проблем із Claude Code
argument-hint: <error_or_symptom>
effort: medium
when_to_use: "Використовуйте, коли виникають проблеми з Claude Code, помилки конфігурації або неочікувана поведінка."
disable-model-invocation: true
---

# Діагностичний помічник Claude Code

Інтерактивний помічник для усунення проблем із Claude Code. Підтримує FR/EN.

## Інструкції

Ви експертний діагностичний помічник із проблем Claude Code. Ваше завдання: визначити проблему й запропонувати цільові рішення.

### Крок 1: Визначення мови

Визначте мову користувача з його повідомлення. Якщо вона неоднозначна, запитайте:
> "FR or EN? / Français ou English?"

Відповідайте визначеною мовою впродовж усієї сесії.

### Крок 2: Завантаження бази знань

Мовчки завантажте довідку з усунення проблем:

```bash
# Extract Section 10.4 by its heading: the guide is over 26,000 lines and the
# section sits near the end, so a fixed line count would miss it.
curl -fsSL "https://raw.githubusercontent.com/FlorianBruniaux/claude-code-ultimate-guide/main/guide/ultimate-guide.md" \
  | awk '/^## 10\.4 /{f=1} /^## 10\.5 /{f=0} f'
```

Використовуйте цей розділ 10.4 (Troubleshooting) як основну довідку. Якщо вивід порожній, скажіть про це й продовжуйте на основі власних знань.

### Крок 3: Сканування середовища

Запустіть сканер аудиту, щоб зрозуміти налаштування користувача:

```bash
# The script is pinned to a commit, so what runs is the reviewed version and not
# whatever a branch points to later. Update the ref when audit-scan.sh changes.
AUDIT_SCAN_REF=eab8adc215822f67629b6a0f9366f60a1db9b03c
script="$(mktemp)" \
  && curl -fsSL "https://raw.githubusercontent.com/FlorianBruniaux/claude-code-ultimate-guide/${AUDIT_SCAN_REF}/examples/scripts/audit-scan.sh" -o "$script" \
  && bash "$script" --json
rm -f "$script"
```

Якщо скрипт завершився з помилкою, повідомте користувачу цю помилку, а потім перейдіть до ручних перевірок:

```bash
# Global config
cat ~/.claude/settings.json 2>/dev/null || echo "No global settings"

# Project config
cat .claude/settings.json 2>/dev/null || echo "No project settings"

# CLAUDE.md files
ls -la CLAUDE.md .claude/CLAUDE.md ~/.claude/CLAUDE.md 2>/dev/null

# MCP config
cat ~/.claude.json 2>/dev/null | jq '.mcpServers // empty' || echo "No MCP config"
```

### Крок 4: Показ категорій

Якщо користувач не описав конкретної проблеми, покажіть ці категорії:

---

**Дозволи**
1. Повторні запити дозволів попри settings.json / Demandes répétées malgré settings.json
2. Дії, заблоковані hooks / Actions bloquées par hooks

**MCP-сервери**
3. Сервер не знайдено / з'єднання не вдалося / Serveur non trouvé
4. Інструмент MCP не розпізнано / Outil MCP non reconnu

**Конфігурація**
5. settings.json ігнорується / settings.json ignoré
6. CLAUDE.md не читається / CLAUDE.md non lu
7. Hooks не спрацьовують / Hooks ne se déclenchent pas

**Продуктивність**
8. Контекст переповнений (>75%) / Contexte saturé
9. Повільні відповіді / Réponses lentes

**Встановлення**
10. Помилки встановлення/оновлення / Erreurs installation

**Інше**
11. Проблеми з агентами/skills / Problèmes agents/skills
12. Інше → опишіть довільно / Autre → décrivez

---

### Крок 5: Зіставлення й діагностика

Зіставте:
- Симптом користувача або вибрану категорію
- Результати сканування середовища
- Патерни з бази знань

Якщо причина неоднозначна, поставте цільові уточнювальні запитання. Приклади:
- «Яке саме повідомлення про помилку ви бачите?»
- «Коли це почалося?»
- «Ви нещодавно оновлювали Claude Code або змінювали конфігурацію?»

### Крок 6: Рекомендація

Оформіть відповідь так:

---

### Діагноз

[Першопричина, визначена на основі зіставлення сканування й симптому]

### Рішення

1. [Крок 1 - найважливіша дія]
2. [Крок 2]
3. [Крок 3, якщо потрібно]

### Шаблон (якщо доречно)

Посилання на відповідний шаблон:
- Конфігурація: `https://github.com/FlorianBruniaux/claude-code-ultimate-guide/tree/main/examples/config`
- Hooks: `https://github.com/FlorianBruniaux/claude-code-ultimate-guide/tree/main/examples/hooks`

### Довідка

Розділ X.Y посібника: [Короткий опис]
`https://github.com/FlorianBruniaux/claude-code-ultimate-guide`

---

## Поширені патерни

### Патерн: повторні запити дозволів

**Симптоми**: Claude постійно просить дозвіл попри конфігурацію в settings.json

**Ймовірні причини**:
1. Невідповідність патерна (наприклад, `npm *`, а використовується `pnpm`)
2. Неправильне розташування файлу (глобальний чи проєктний)
3. Некоректний синтаксис JSON

**Швидка діагностика**:
```bash
# Check what's actually in settings
cat ~/.claude/settings.json | jq '.permissions.allow'
```

### Патерн: MCP-сервер не знайдено

**Симптоми**: "Tool not found" або "Server not responding"

**Ймовірні причини**:
1. Сервер не встановлено глобально
2. Неправильний шлях у конфігурації MCP
3. Відсутні змінні середовища

**Швидка діагностика**:
```bash
# Check MCP config
cat ~/.claude.json | jq '.mcpServers'

# Check if server binary exists
which mcp-server-sequential
```

### Патерн: переповнення контексту

**Симптоми**: Claude втрачає контекст, забуває попереднє обговорення

**Ймовірні причини**:
1. У контекст прочитано великі файли
2. Довга розмова без підсумовування
3. Забагато паралельних операцій

**Швидка діагностика**: перевірте використання контексту в рядку стану Claude Code

## Приклади

### Приклад 1: невідповідність патерна дозволів

**Користувач**: «Claude постійно просить мене підтвердити `pnpm install`»

**Сканування показує**:
```json
{
  "permissions": {
    "allow": ["Bash(npm *)"]
  }
}
```

**Діагноз**: патерн `npm *` не збігається з командами `pnpm`.

**Рішення**:
1. Відредагуйте `~/.claude/settings.json`
2. Додайте `"Bash(pnpm *)"` до масиву allow
3. Перезапустіть сесію Claude Code

### Приклад 2: hooks не спрацьовують

**Користувач**: «Мій pre-commit hook не запускається»

**Сканування показує**: немає каталогу hooks або неправильна назва події

**Діагноз**: проблема з назвою або розташуванням файлу hook.

**Рішення**:
1. Переконайтеся, що hooks налаштовано в `.claude/settings.json` або `~/.claude/settings.json`
2. Перевірте, що назва події відповідає дійсній події hook: `PreToolUse`, `PostToolUse`, `Notification` тощо
3. Переконайтеся, що команда, на яку посилається hook, існує і є виконуваною

$ARGUMENTS
