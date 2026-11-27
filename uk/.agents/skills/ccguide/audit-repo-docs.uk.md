---
name: audit-repo-docs
description: Аудит документації репозиторію за 85+ найкращими практиками з claude-code-ultimate-guide
---

# Skill аудиту документації

Проаналізуй якість документації репозиторію та сформуй рекомендації щодо покращення на основі 85+ шаблонів із Claude Code Ultimate Guide.

## Використання

```
/audit-repo-docs              # Audit only, generate markdown report
/audit-repo-docs --generate   # Audit + propose creating missing files
```

## Воркфлоу

### Фаза 1: Виявлення (лише читання)

Скануй структуру репозиторію, щоб знайти наявні файли документації.

**Файли для перевірки:**

```bash
# Root files
ls -la README.md VERSION CHANGELOG.md CLAUDE.md CONTRIBUTING.md LICENSE .gitignore 2>/dev/null

# Documentation structure
ls -la docs/ guide/ documentation/ 2>/dev/null

# Machine-readable
ls -la machine-readable/ llms.txt robots.txt 2>/dev/null

# Automation
ls -la scripts/*.sh 2>/dev/null

# Examples
find examples/ -type f 2>/dev/null | head -20
```

**Виявлення шаблонів:**

```bash
# Check README Quick Start
grep -n "Quick Start\|Getting Started\|Installation" README.md 2>/dev/null | head -3

# Check for badges
grep -c "\!\[.*\](.*badge.*)" README.md 2>/dev/null || echo "0"

# Check CHANGELOG format
head -20 CHANGELOG.md 2>/dev/null

# Check VERSION format
cat VERSION 2>/dev/null

# Check for TOC
grep -n "Table of Contents\|## Contents" README.md 2>/dev/null

# Check for metadata in docs
grep -rn "^---$\|author:\|date:\|version:" docs/ guide/ 2>/dev/null | head -10
```

### Фаза 2: Оцінювання (30 критеріїв)

Оціни кожен критерій як: ✅ (є), ⚠️ (частково), ❌ (немає)

#### Категорія 1: Кореневі файли (8 критеріїв, вага ×3)

| # | Критерій | Виявлення | Бали |
|---|----------|-----------|------|
| 1.1 | README.md із Quick Start < 40 рядків | `head -50 README.md | grep -n "Quick Start"` | 3 |
| 1.2 | VERSION (один рядок semver) | `cat VERSION` збігається з `^\d+\.\d+\.\d+$` | 3 |
| 1.3 | CHANGELOG.md (формат Keep a Changelog) | Має розділи `## [Unreleased]` або `## [x.y.z]` | 3 |
| 1.4 | CLAUDE.md (інструкції проєкту) | Файл існує й має > 10 рядків | 3 |
| 1.5 | CONTRIBUTING.md | Файл існує | 3 |
| 1.6 | LICENSE | Файл існує | 3 |
| 1.7 | .gitignore (категоризовані розділи) | Має розділи-коментарі `# Category` | 3 |
| 1.8 | Функціональні бейджі в README | Щонайменше 2 зображення-бейджі | 3 |

#### Категорія 2: Структура документації (7 критеріїв, вага ×2)

| # | Критерій | Виявлення | Бали |
|---|----------|-----------|------|
| 2.1 | Окрема тека docs | Існує `docs/` або `guide/` | 2 |
| 2.2 | Метадані в документації (автор, дата, версія) | YAML frontmatter у файлах .md | 2 |
| 2.3 | Зміст із якорями | `## Table of Contents` або `## Contents` з посиланнями | 2 |
| 2.4 | Розділ TL;DR або Quick Start | Розділ існує в основному документі | 2 |
| 2.5 | Оцінки часу | Згадано `Time:`, `minutes` або `hours` | 2 |
| 2.6 | Наявна шпаргалка | Файл із назвою `cheatsheet.md` або подібною | 2 |
| 2.7 | Приклади в окремій теці | `examples/` із > 3 файлами | 2 |

#### Категорія 3: Машинозчитуваний вміст (5 критеріїв, вага ×1)

| # | Критерій | Виявлення | Бали |
|---|----------|-----------|------|
| 3.1 | llms.txt або еквівалент | Файл існує для індексації AI | 1 |
| 3.2 | Індекс YAML/JSON < 3K токенів | `machine-readable/` з індексним файлом | 1 |
| 3.3 | Номери рядків для навігації | Посилання на кшталт `file.md:123` у документації | 1 |
| 3.4 | Синхронізована версія | VERSION збігається з посиланнями в README, документації | 1 |
| 3.5 | Ключові слова/теги | Теги або ключові слова у frontmatter | 1 |

#### Категорія 4: Автоматизація (5 критеріїв, вага ×1)

| # | Критерій | Виявлення | Бали |
|---|----------|-----------|------|
| 4.1 | Скрипт синхронізації версії | `scripts/*version*` або `scripts/*sync*` | 1 |
| 4.2 | Скрипт перевірки | `scripts/*check*` або `scripts/*verify*` | 1 |
| 4.3 | Режим --check (dry-run) | Скрипт підтримує прапорець `--check` | 1 |
| 4.4 | Інтеграція CI/CD | `.github/workflows/` із воркфлоу, пов'язаним із документацією | 1 |
| 4.5 | Задокументовані slash-команди | `.claude/commands/` із README або в CLAUDE.md | 1 |

#### Категорія 5: Якість (5 критеріїв, вага ×2)

| # | Критерій | Виявлення | Бали |
|---|----------|-----------|------|
| 5.1 | Таблиці для структурованих даних | Щонайменше 3 markdown-таблиці в документації | 2 |
| 5.2 | Блоки коду з підказками мови | Використано синтаксис ` ```language ` | 2 |
| 5.3 | Згортані блоки для необов'язкового вмісту | Використано теги `<details>` | 2 |
| 5.4 | Робочі перехресні посилання | Наявні внутрішні посилання `[text](./path)` | 2 |
| 5.5 | Футер із версією/датою | В останньому рядку згадано версію або дату | 2 |

### Фаза 3: Підрахунок балів

**Формула:**

```
Score = Σ(criteria_ok × weight) / Σ(max_weights) × 100

Max points:
- Root Files:     8 × 3 = 24
- Structure:      7 × 2 = 14
- Machine-Read:   5 × 1 = 5
- Automation:     5 × 1 = 5
- Quality:        5 × 2 = 10
─────────────────────────────
Total:            58 points
```

**Шкала оцінок:**

| Бали | Оцінка | Статус |
|------|--------|--------|
| 90-100 | A | 🟢 Відмінно |
| 75-89 | B | 🟢 Добре |
| 60-74 | C | 🟡 Потрібне доопрацювання |
| 40-59 | D | 🟡 Суттєві прогалини |
| 0-39 | F | 🔴 Критичні проблеми |

### Фаза 4: Формування звіту

Виведи звіт у точно такому форматі:

```markdown
# 📋 Documentation Audit Report

**Repository**: {repo_name}
**Date**: {current_date}
**Score**: {score}/100 ({grade})

## Summary

| Category | Score | Status |
|----------|-------|--------|
| Root Files | {x}/8 | {emoji} {percent}% |
| Structure | {x}/7 | {emoji} {percent}% |
| Machine-Readable | {x}/5 | {emoji} {percent}% |
| Automation | {x}/5 | {emoji} {percent}% |
| Quality | {x}/5 | {emoji} {percent}% |

## 🔴 Critical Issues (Priority 1)

{List missing items from Root Files category - weight ×3}

## 🟡 Recommended Improvements (Priority 2)

{List missing items from Structure and Quality categories - weight ×2}

## 🟢 Quick Wins (Priority 3)

{List easy-to-add items from any category that take < 5 min}

## 📝 Suggested Templates

{For each critical/recommended missing item, provide a collapsible template}

<details>
<summary>{filename} template</summary>

\`\`\`{format}
{template content}
\`\`\`

</details>
```

### Фаза 5: Необов'язкова генерація (прапорець --generate)

Якщо `$ARGUMENTS` містить `--generate`:

1. Перелічи всі відсутні файли, які буде створено
2. Запитай схвалення користувача: "Create these {n} files? (y/n/select)"
3. Після схвалення створи файли за наданими шаблонами
4. Повідом, що було створено

**Джерела шаблонів:**

| Файл | Розташування шаблону |
|------|----------------------|
| VERSION | Один рядок: `1.0.0` |
| CHANGELOG.md | `examples/templates/` або формат Keep a Changelog |
| CONTRIBUTING.md | Стандартний посібник для контриб'юторів |
| llms.txt | `machine-readable/llms.txt` як зразок |
| Cheatsheet | `guide/cheatsheet.md` як зразок |

## Приклад виводу

```markdown
# 📋 Documentation Audit Report

**Repository**: my-awesome-project
**Date**: 2026-01-23
**Score**: 52/100 (D)

## Summary

| Category | Score | Status |
|----------|-------|--------|
| Root Files | 4/8 | 🟡 50% |
| Structure | 3/7 | 🟡 43% |
| Machine-Readable | 0/5 | 🔴 0% |
| Automation | 1/5 | 🔴 20% |
| Quality | 3/5 | 🟡 60% |

## 🔴 Critical Issues (Priority 1)

- Missing `VERSION` file (single source of truth for versioning)
- Missing `CHANGELOG.md` (track changes for users)
- Missing `CLAUDE.md` (AI context for Claude Code)
- No functional badges in README

## 🟡 Recommended Improvements (Priority 2)

- Add Table of Contents to README
- Create `examples/` folder with usage examples
- Add time estimates to documentation sections
- Create a cheatsheet for quick reference

## 🟢 Quick Wins (Priority 3)

- Add 2-3 badges to README (build status, version, license)
- Add `<details>` collapsibles for long code examples
- Add language hints to all code blocks

## 📝 Suggested Templates

<details>
<summary>VERSION template</summary>

```
1.0.0
```

</details>

<details>
<summary>CHANGELOG.md template</summary>

```markdown
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Initial project setup

## [1.0.0] - YYYY-MM-DD

### Added
- First release
```

</details>

<details>
<summary>CLAUDE.md template</summary>

```markdown
# {Project Name} - Claude Code Context

## Project Overview

{Brief description of what the project does}

## Tech Stack

- {Language/Framework}
- {Key dependencies}

## Directory Structure

\`\`\`
src/           # Source code
tests/         # Test files
docs/          # Documentation
\`\`\`

## Commands

\`\`\`bash
# Install dependencies
{install_command}

# Run tests
{test_command}

# Build
{build_command}
\`\`\`

## Conventions

- {Coding convention 1}
- {Coding convention 2}

## Current Focus

{What you're currently working on - update this regularly}
```

</details>

<details>
<summary>llms.txt template</summary>

```
# {Project Name}

> {One-line description}

## Overview

{2-3 sentences explaining what this project does}

## Key Files

- README.md - Project overview
- src/ - Source code
- docs/ - Documentation

## Quick Start

1. {Step 1}
2. {Step 2}
3. {Step 3}

## Keywords

{keyword1}, {keyword2}, {keyword3}
```

</details>
```

## Валідація

Після реалізації перевір:

1. **На цьому репозиторії (claude-code-ultimate-guide)**: очікувана оцінка ~95%
2. **На мінімальному репозиторії**: створи тимчасовий репозиторій лише з README, перевір виявлення прогалин
3. **Валідність шаблонів**: переконайся, що згенеровані шаблони синтаксично коректні
