---
name: release-notes-generator
description: "Генерує нотатки до релізу в 3 форматах (CHANGELOG.md, тіло PR, оголошення в Slack) із git-комітів. Автоматично категоризує зміни та перетворює технічну мову на зрозумілі користувачам повідомлення. Використовуйте для релізів, changelog, нотаток до версій, підсумків «що нового» або оголошень про випуск."
allowed-tools: Bash
effort: low
---

# Генератор нотаток до релізу

Згенеруйте повні нотатки до релізу в 3 форматах із git-комітів.

## Воркфлоу

1. **Проаналізуйте історію git** від останнього тега релізу або вказаної версії
2. **Отримайте деталі PR** (заголовки, описи, мітки) через `gh api`
3. **Категоризуйте зміни** на функції, виправлення багів, покращення, безпеку, зміни, що ламають сумісність
4. **Згенеруйте 3 виводи**: розділ CHANGELOG.md (технічний), тіло PR релізу (напівтехнічне), повідомлення для Slack (зрозуміле користувачам)
5. **Перетворіть мову** з технічного жаргону на доступні повідомлення
6. **Попередьте про міграції**, якщо виявлено міграції бази даних

## Як використовувати

### Базове використання

```
Generate release notes since last release
```

```
Create release notes for version 0.18.0
```

### З указаним діапазоном

```
Generate release notes from v0.17.0 to HEAD
```

### Лише попередній перегляд

```
Preview release notes without writing files
```

## Формати виводу

### 1. Розділ CHANGELOG.md

Технічний формат для розробників:

```markdown
## [0.18.0] - 2025-12-08

### Objective
[1-2 sentence summary]

### New Features
#### [Feature Name] (#PR)
- **Description**: ...
- **Impact**: ...

### Bug Fixes
- **[Module]**: Description (#issue, [error-tracker] ISSUE-XX)

### Technical Improvements
#### Performance / UI/UX / Architecture
- [Description]

### Database Migrations
[If applicable]

### Statistics
- PRs: X
- Features: Y
- Bugs: Z
```

### 2. Тіло PR релізу

Використовує шаблон із `.github/PULL_REQUEST_TEMPLATE/release.md`:
- Підсумок мети
- Функції з посиланнями на специфікації
- Виправлення багів із посиланнями на error tracker
- Покращення за категоріями
- Інструкції з міграцій
- Чекліст розгортання

### 3. Оголошення в Slack

Продуктово-орієнтований формат із `.github/COMMUNICATION_TEMPLATE/slack-release.md`:
- **Посилання на PR** для відстежуваності
- Нетехнічна мова
- Фокус на впливі на користувача (кінцеві користувачі, адміністратори, стейкхолдери)
- Емодзі для читабельності
- Підсумок статистики

## Інтеграція у воркфлоу

Цей skill інтегрується з воркфлоу релізу:

```
1. Analyze commits: git log <last-tag>..HEAD
2. Determine version number (MAJOR.MINOR.PATCH)
3. Generate 3 outputs
4. Create PR develop -> main with "Release" label
5. Update CHANGELOG.md
6. After merge: create git tag
7. Generate Slack announcement
```

## Перетворення технічного на продуктове

Skill автоматично перетворює технічну мову:

| Технічне | Продуктове |
|----------|------------|
| "N+1 query optimization with DataLoader" | "Faster list loading" |
| "AI embeddings implementation with pgvector" | "New intelligent search" |
| "Fix scope permissions in getPermissionScope()" | "Fixed access permissions bug" |
| "Migration webpack -> Turbopack" | *Не повідомляти* |
| "React hooks refactoring" | *Не повідомляти* |
| "Fix N+1 in user loaders" | "Performance improvement" |
| "Add retry logic for DB connection errors" | "Better connection stability" |

## Категорії комітів

Коміти категоризуються за префіксом conventional commit:

| Префікс | Категорія | Включати в Slack? |
|---------|-----------|-------------------|
| `feat:` | Нові функції | Так |
| `fix:` | Виправлення багів | Так (якщо помітні користувачу) |
| `perf:` | Продуктивність | Так (спрощено) |
| `security:` | Безпека | Так |
| `refactor:` | Архітектура | Ні |
| `chore:` | Підтримка | Ні |
| `docs:` | Документація | Ні |
| `test:` | Тести | Ні |
| `style:` | Стиль | Ні |

## Формат виводу в консоль

Під час генерації нотаток до релізу ЗАВЖДИ показуйте чіткий підсумок у консолі з:

### Попередження про міграції (КРИТИЧНО)

Якщо виявлено міграції, покажіть їх помітно:

```
╔══════════════════════════════════════════════════════════════════╗
║  ⚠️  [WARNING] DATABASE MIGRATIONS REQUIRED                      ║
╠══════════════════════════════════════════════════════════════════╣
║                                                                  ║
║  This release contains X migration(s):                           ║
║                                                                  ║
║  • 20251210123456_add_feature_description                        ║
║  • 20251211094532_update_status_enum                             ║
║                                                                  ║
║  Action required BEFORE deployment:                              ║
║  → Run: [migration-command]                                      ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝
```

Якщо міграцій НЕМАЄ:

```
✅ [OK] No database migrations required
```

### Метод виявлення

Перевірте нові файли міграцій від останнього релізу:

```bash
# Find new migrations since last tag
git diff <last-tag>..HEAD --name-only -- migrations/
```

## Приклад

**Користувач**: "Generate release notes since v0.17.0"

**Вивід**:

```
Analyzing commits from v0.17.0 to HEAD...

Found:
- 15 commits
- 8 PRs merged
- 2 new features
- 5 bug fixes
- 3 improvements

╔══════════════════════════════════════════════════════════════════╗
║  ⚠️  [WARNING] DATABASE MIGRATIONS REQUIRED                      ║
╠══════════════════════════════════════════════════════════════════╣
║  This release contains 1 migration(s):                           ║
║  • 20251208143021_add_user_preferences                           ║
║  Action required: [migration-command]                             ║
╚══════════════════════════════════════════════════════════════════╝

--- CHANGELOG.md Section ---
[Technical format output]

--- PR Release Body ---
[Semi-technical format output]

--- Slack Announcement ---
[Product-focused format output]

Write to files? (CHANGELOG.md, clipboard for PR/Slack)
```

## Використані команди

```bash
# Get last release tag
git tag --sort=-v:refname | head -n 1

# List commits since tag
git log <tag>..HEAD --oneline --no-merges

# Get PR details
gh api repos/{owner}/{repo}/pulls/{number}

# Get commit details
git show --stat <sha>
```

## Поради

- Запускайте з кореня репозиторію
- Переконайтеся, що `gh` CLI автентифіковано
- Перевіряйте згенерований вміст перед публікацією
- Підлаштуйте продуктову мову під свою аудиторію
- Використовуйте `--preview`, щоб побачити вивід без запису

## Довідкові файли

- `assets/changelog-template.md` - шаблон розділу CHANGELOG
- `assets/slack-template.md` - шаблон оголошення в Slack
- `references/tech-to-product-mappings.md` - правила перетворення
- `references/commit-categories.md` - правила категоризації

## Пов'язані skills

- `github-actions-templates` - для воркфлоу CI/CD
- `changelog-generator` - оригінальне джерело натхнення (ComposioHQ)
