---
name: scaffold
description: "Інтерактивний коуч, який ставить 4-5 запитань, щоб визначити, чи потрібен вам agent, команда, skill, hook або правило, а потім генерує готовий до використання шаблон. Використання: /scaffold (аргументи не потрібні, запускає коучингову сесію)"
effort: medium
disable-model-invocation: true
---

# Коуч зі scaffold для Claude Code

Інтерактивний майстер, що визначає правильний компонент Claude Code для вашого сценарію та генерує готовий до використання шаблон.

**Використання**: `/scaffold` (аргументи не потрібні). Почніть розмову.

---

## Фаза 1: Виявлення

Почніть із цього prompt, а потім дочекайтеся відповіді користувача, перш ніж питати щось інше:

> Що ви хочете автоматизувати або створити? Для початку достатньо одного речення.

Коли матимете приблизне уявлення, ставте наступні запитання по порядку. Пропускайте запитання, якщо попередня відповідь уже на нього відповіла.

### Q1: Тригер

> Як це запускається?
>
> a) Я сам запускаю командою (наприклад, `/something`)
> b) Має спрацьовувати автоматично, коли Claude виконує дію (пише файл, запускає bash, завершує сесію...)
> c) Має діяти постійно, у кожній сесії, без моїх дій

- Якщо **b** → ймовірно **Hook** (перейти до Q_hook)
- Якщо **c** → ймовірно **Rule** (перейти до Q_rule)
- Якщо **a** → продовжити з Q2

### Q2: Предметна експертиза

> Чи потрібна для цього глибока експертиза, специфічна для проєкту?
> Наприклад: знання вашої схеми GraphQL, ваших конвенцій міграцій, внутрішніх патернів API, вашої моделі вартості...

- Якщо **так, глибока експертиза** → ймовірно **Agent** (перейти до Q_agent)
- Якщо **ні, це скоріше чекліст або процедура** → продовжити з Q3

### Q3: Складність

> Скільки контексту та логіки це охоплює?
>
> a) Багато: кілька правил, предметні приклади, тонкі судження
> b) Просто: кілька кроків, шаблон, трохи bash

- Якщо **a** → ймовірно **Skill**
- Якщо **b** → ймовірно **Command**

### Q4: Обсяг повторного використання

> Кому це потрібно?
>
> a) Лише мені
> b) Усій моїй команді
> c) Має автоматично викликатися іншими agents

- **c** → підсилює **Agent** (потрібне поле `description:`, яке можуть читати інші agents)
- **b** → підсилює **Command** або **Skill** (спільна конфігурація)
- **a** → може залишитися простою особистою **Command**

### Q5: Тип результату

> Що має статися в кінці?
>
> a) Звіт або аналіз: Claude читає й пояснює, жодних файлів не чіпає
> b) Згенерований код або файли
> c) Виконана дія (коміт, push, виклик API...)
> d) Поведінка Claude змінюється назавжди (завжди робить X, ніколи не робить Y)

- **a** → Agent лише для читання (без `Write` чи `Bash` в tools)
- **b/c** → Agent або Command/Skill з доступом на запис
- **d** → Rule, або Hook, якщо залежить від конкретної події

---

## Внутрішнє дерево рішень (не показувати, використовувати для міркувань)

```
Triggered automatically?
  ├─ On Claude action (Write, Bash, SessionEnd...) -> Hook
  └─ Always active, no trigger -> Rule

Triggered manually?
  ├─ Deep domain expertise required?
  │   ├─ Yes + invokable by other agents -> Agent
  │   └─ Yes + manual use only -> Agent or Skill
  └─ Procedure / checklist, no special expertise?
      ├─ Complex, lots of project-specific context -> Skill
      └─ Simple, a few steps -> Command

Common hybrid cases:
  - Agent + Command: specialist agent + a shortcut command to invoke it
  - Rule + Hook: permanent behavior + blocking on a specific action
  - Skill + Agent: skill that delegates analysis to an agent
```

---

## Фаза 2: Рекомендація

Після запитань покажіть таку структуру:

```
## Diagnosis

You want to: [one-line summary of the use case]

## Recommendation: [TYPE]

**Why?**
[2-3 sentences: trigger type, complexity level, reuse scope]

**What it would NOT be, and why:**
- Not an agent because [short reason]
- Not a rule because [short reason]
[adjust based on actual candidates]

**Hybrid case?** [Yes / No]
[If yes: explain the combination and which file to create first]
```

---

## Фаза 3: Scaffold

Запитайте: "Згенерувати файл scaffold?"

Якщо так, створіть шаблон нижче залежно від визначеного типу.

---

### Scaffold агента

```markdown
---
name: [kebab-case-name]
description: "[What this agent does in one sentence. When to invoke it. Example triggers for other agents.]"
model: sonnet
tools: Read, Grep, Glob[, Write, Bash (add only if this agent must modify files or run commands)]
---

# [Agent Name]

[One paragraph: what this agent is for, what it is NOT for, and when to prefer another agent.]

## Context

[Stack, conventions, or domain knowledge this agent needs to be effective.]

## When to invoke

- [Concrete trigger 1]
- [Concrete trigger 2]
- [Concrete trigger 3]

## Protocol

### Step 1: Read context

```bash
# What to read before reasoning
cat CLAUDE.md 2>/dev/null
```

### Step 2: Analyze

[What to look for. Patterns to detect. Red flags to surface.]

### Step 3: Output

[Exact output format: use a markdown code block to show the structure.]

## Red flags

| Pattern | Risk |
|---------|------|
| [pattern] | [impact] |

## What this agent does NOT do

- [Scope boundary 1]
- [Scope boundary 2: point to another agent if relevant]
```

**Файл**: `.claude/agents/[name].md`

---

### Scaffold команди

```markdown
---
name: [name]
description: "[What this command does in one sentence]"
argument-hint: "[arg] [--flag]"
---

# [Command Name]

[Brief description. What problem it solves. When to use it vs alternatives.]

## Arguments

- `[arg]`: [description] (default: [value])
- `--flag`: [description]

## Usage

```bash
/[name]              # Basic usage
/[name] --flag       # With flag
```

---

## Phase 1: [First phase name]

[What Claude does in this phase.]

```bash
# Example commands if applicable
```

## Phase 2: [Second phase name]

[What Claude does.]

## Phase 3: Output

[Output format. Use a markdown block to show the structure.]

$ARGUMENTS
```

**Файл**: `.claude/commands/[name].md`

---

### Scaffold skill

```markdown
---
name: [skill-name]
description: "[What this skill does. Trigger phrases that activate it. Usage: /[name] [arg]]"
---

# [Skill Name]

[What this skill does and when it applies. Distinguish from similar skills.]

## Trigger phrases

- "[phrase that activates this skill]"
- "[alternative phrasing]"

## When to use

- [Scenario 1]
- [Scenario 2]

## Workflow

### 1. [First action]: [brief description]

[Details]

### 2. [Second action]: [brief description]

[Details]

### 3. Deliver output

[Output format]

## Conventions to follow

[Project-specific rules, naming conventions, or patterns this skill must respect.]

## Common pitfalls

- [Mistake 1 and how to avoid it]
- [Mistake 2 and how to avoid it]

$ARGUMENTS
```

**Файл**: `.claude/skills/[name].md`

---

### Scaffold hook

```bash
#!/usr/bin/env bash
# =============================================================================
# [name].sh: [PreToolUse | PostToolUse | UserPromptSubmit | Stop] Hook
# =============================================================================
# [What this hook does in one line]
# Fires on: [event] matching [tool or pattern]
#
# Exit 0 = allow / continue
# Exit 2 = block with message (PreToolUse only)
#
# stdin: JSON payload from Claude Code
# =============================================================================

set -euo pipefail

INPUT=$(cat)
TOOL_NAME=$(echo "$INPUT" | jq -r '.tool_name // empty')

# --- Main logic ---

# [Your validation logic here]
# Example: block writes to protected paths
# FILE=$(echo "$INPUT" | jq -r '.tool_input.file_path // empty')
# if [[ "$FILE" == *"/secrets/"* ]]; then
#   echo "Blocked: writes to /secrets/ are not allowed" >&2
#   exit 2
# fi

exit 0
```

**Файл**: `.claude/hooks/[name].sh`

Також додайте до `.claude/settings.json`:
```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Write",
        "hooks": [{ "type": "command", "command": ".claude/hooks/[name].sh" }]
      }
    ]
  }
}
```

---

### Scaffold правила

```markdown
# [Rule Title] (Auto-loaded)

## Directive

[The rule in one imperative sentence.]

## When it applies

[Triggers, file types, or situations where this rule activates.]

## Required behavior

[What Claude must do concretely, be specific.]

## Anti-patterns

Do NOT:
- [Forbidden example]

Do:
- [Correct behavior]

---

**Auto-loaded**: This file is loaded automatically at session start.
```

**Файл**: `.claude/rules/[name].md`

Додайте посилання в `CLAUDE.md`, якщо файл не в автозавантажуваному каталозі.

---

## Коротка довідка

Якщо користувач не впевнений, покажіть цю таблицю:

| Тип | Тригер | Потрібна експертиза | Складність | Типовий приклад |
|-----|--------|---------------------|------------|-----------------|
| **Agent** | Вручну або автоматично | Висока, предметна | Багатокроковий аналіз | `migration-reviewer`, `dbt-specialist` |
| **Command** | Вручну `/name` | Низька або середня | Проста, кілька кроків | `/commit`, `/pr`, `/release` |
| **Skill** | Вручну `/name` | Середня або висока | Багатий воркфлоу, багато контексту | `tdd-workflow`, `api-review` |
| **Hook** | Автоматично за подією | Жодної (логіка bash) | Скрипт | `security-gate.sh`, `format-on-save.sh` |
| **Rule** | Постійно, у кожній сесії | Жодної (проза) | Інструкції | `no-direct-push.md`, `english-only.md` |

---

## Джерела

- Огляд типів компонентів: [Розділ 3](../../../guide/ultimate-guide.uk.md)
- Приклади agents: [agents/](../../agents/)
- Приклади hooks: [hooks/](../../hooks/)
- Приклади skills: [skills/](../../skills/)
