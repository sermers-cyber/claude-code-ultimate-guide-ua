---
name: skill-creator
description: "Створює каркас нового skill для Claude Code з SKILL.md, frontmatter і додатковими ресурсами. Використовуйте під час створення власного skill, уніфікації структури skills у команді або пакування skill для поширення."
allowed-tools: Write Bash
effort: low
---

# Skill creator

Генерує нові skills для Claude Code з коректною структурою каталогів, YAML frontmatter і необов'язковими додатковими ресурсами.

## Коли використовувати

- Створення нового власного skill для проєкту
- Уніфікація структури skills у команді
- Генерація шаблонів skills зі скриптами, довідниками та ресурсами
- Пакування skills для поширення

## Структура каталогу skill

```
skill-name/
├── SKILL.md          # Required: Main skill file with YAML frontmatter
├── scripts/          # Optional: Executable code for deterministic tasks
├── references/       # Optional: Documentation loaded contextually
└── assets/           # Optional: Templates, images, boilerplate (not loaded into context)
```

## Робочий процес

### 1. Створіть skill

```
Create a new skill called "my-skill-name" in ~/.claude/skills/
```

Або з конкретною метою:

```
Create a skill for generating release notes from git commits,
with templates for CHANGELOG.md and Slack announcements
```

Або через скрипт ініціалізації:

```bash
python3 ~/.claude/skills/skill-creator/scripts/init_skill.py <skill-name> --path <output-directory>
```

### 2. Згенерований шаблон SKILL.md

Створений SKILL.md має таку структуру:

```markdown
---
name: skill-name
description: "What the skill does. Use when [trigger conditions]."
---

# Skill Name

## When to Use
- Trigger condition 1
- Trigger condition 2

## What This Skill Does
1. **Step 1**: Description
2. **Step 2**: Description

## How to Use
[Usage examples]

## Example
**User**: "Example prompt"
**Output**: [Example output]
```

### 3. Перевірте skill

Після створення перевірте:

1. **Frontmatter**: `name` у kebab-case, 1-64 символи; `description` є рядком у лапках із застереженням «Use when»
2. **Вміст**: є розділ «When to Use» з умовами спрацювання та принаймні один приклад використання
3. **Структура**: SKILL.md не більше 5000 слів; довідники й ресурси лежать у правильних підкаталогах
4. **Тест**: викличте skill на реальному випадку і переконайтеся, що вивід відповідає очікуваному

### 4. Пакування для поширення (необов'язково)

```bash
python3 ~/.claude/skills/skill-creator/scripts/package_skill.py <path/to/skill-folder> [output-directory]
```

## Організаційні патерни

| Патерн | Найкраще для | Структура |
|--------|--------------|-----------|
| **Workflow-Based** | Послідовні процедури | Покрокові інструкції |
| **Task-Based** | Кілька операцій | Набір завдань |
| **Reference/Guidelines** | Стандарти, специфікації | Правила та приклади |
| **Capabilities-Based** | Взаємопов'язані можливості | Описи можливостей |

## Приклад: створення skill для release notes

**Користувач**: "Create a skill for generating release notes with 3 output formats"

**Кроки**:
1. Ініціалізація: `init_skill.py release-notes-generator --path ~/.claude/skills/`
2. Додайте шаблони в `assets/`: `changelog-template.md`, `pr-release-template.md`, `slack-template.md`
3. Додайте правила в `references/`: `tech-to-product-mappings.md`
4. Завершіть `SKILL.md` інструкціями з використання
5. Перевірка: звірте frontmatter, протестуйте на реальному діапазоні комітів
6. Пакування: `package_skill.py ~/.claude/skills/release-notes-generator`

## Поради

- Тримайте SKILL.md у межах 5000 слів для ефективного використання контексту
- Використовуйте `references/` для доменних знань, що рідко змінюються
- Кладіть шаблони в `assets/`, щоб вони не завантажувалися в контекст автоматично
- Завжди додавайте застереження «Use when» у frontmatter description
- Тестуйте на реальних випадках перед пакуванням
