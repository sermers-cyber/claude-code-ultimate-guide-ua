---
title: "Поведінкові режими"
description: "Готові файли поведінкових режимів для налаштування поведінки Claude Code"
tags: [config, template, workflows]
---

# Поведінкові режими

Готові до використання файли поведінкових режимів для Claude Code. Скопіюйте їх у `~/.claude/` і пошліться на них у своєму `CLAUDE.md`.

## Доступні режими

| Режим | Файл | Призначення |
|------|------|---------|
| **Learning** | [MODE_Learning.md](./MODE_Learning.md) | Пояснення «саме вчасно», коли техніка застосовується вперше |

## Встановлення

### 1. Скопіюйте файл режиму

```bash
cp MODE_Learning.md ~/.claude/
```

### 2. Пошліться на нього у своєму CLAUDE.md

Додайте до `~/.claude/CLAUDE.md`:

```markdown
# Behavioral Modes
@MODE_Learning.md
```

### 3. Додайте прапорці (необов'язково)

Додайте до `~/.claude/FLAGS.md` для активації через прапорці:

```markdown
**--learn**
- Trigger: User requests learning mode, "why/how" questions
- Behavior: Enable just-in-time explanations with first-occurrence tracking

**--no-learn**
- Trigger: User wants pure execution without educational offers
- Behavior: Suppress all learning mode offers
```

## Використання

```bash
# Activate for entire session
claude --learn

# Focus on specific domain
claude --learn focus:git
claude --learn focus:architecture

# Batch explanations at task end
claude --learn batch
```

## Більше режимів: фреймворк SuperClaude

Цей посібник містить лише **Learning Mode**. Щоб отримати повний поведінковий фреймворк із додатковими режимами, перегляньте [SuperClaude](https://github.com/SuperClaude-Org/SuperClaude_Framework):

| Режим | Призначення |
|------|---------|
| **Orchestration** | Розумний вибір інструментів, оптимізація паралельного виконання |
| **Task Management** | Ієрархічне відстеження завдань із постійною пам'яттю |
| **Token Efficiency** | Стиснення із символьними скороченнями (скорочення токенів на 30-50%) |
| **Learning** | Розвиток навичок «саме вчасно» (включено сюди) |

SuperClaude також містить:
- `FLAGS.md` (власні поведінкові маркери, як-от `--delegate`, `--learn`). Це домовленості в промптах, а не прапорці CLI Claude Code. Для налаштувань міркувань використовуйте `/effort` або `--effort`; `ultrathink` додає інструкцію, не змінюючи effort в API.
- `PRINCIPLES.md` — інженерні принципи (SOLID, DRY, підхід на основі доказів)
- `RULES.md` — практичні правила із системою пріоритетів
- Документація MCP-серверів (Context7, Sequential, Serena)

## Див. також

- [SuperClaude Behavioral Modes](../../guide/ultimate-guide.md#superclaude-behavioral-modes): повна документація
- [Репозиторій SuperClaude](https://github.com/SuperClaude-Org/SuperClaude_Framework): повний фреймворк
