---
name: release-notes
description: Згенерувати нотатки до релізу в кількох форматах із git-комітів
argument-hint: "[--from <tag>] [--format md|slack]"
effort: medium
when_to_use: "Використовуйте при підготовці релізу, коли потрібні нотатки в кількох форматах."
disable-model-invocation: true
---

# Генератор нотаток до релізу

Згенеруйте нотатки до релізу в 3 форматах із git-комітів для продакшен-релізів.

## Процес

1. **Аналіз історії Git**: Скануйте коміти від останнього тега релізу
2. **Отримання деталей PR**: Отримайте заголовки, описи через `gh api`
3. **Категоризація змін**: Групуйте за типом (feat, fix, perf тощо)
4. **Перевірка міграцій**: Виявіть файли міграцій бази даних
5. **Генерація 3 виводів**: CHANGELOG, тіло PR, повідомлення для комунікації
6. **Трансформація мови**: Перетворіть технічний жаргон на продуктову мову

## Формати виводу

### 1. Розділ CHANGELOG.md

```markdown
## [X.Y.Z] - YYYY-MM-DD

### Summary
[1-2 sentence overview of this release]

### New Features
#### [Feature Name] (#PR)
- **Description**: User-facing functionality added
- **Impact**: How it benefits users

### Bug Fixes
- **[Module]**: Description (#issue, tracking-ID)

### Technical Improvements
- [Internal improvements, refactoring, performance]

### Database Migrations
[If applicable - list migration files]

### Statistics
- PRs: X | Features: Y | Fixes: Z | Files changed: N
```

### 2. Тіло PR релізу

Використовує шаблон релізу вашого проєкту:
- `.github/PULL_REQUEST_TEMPLATE/release.md`
- `.github/pull_request_template_release.md`
- Або власне розташування, указане в конфігурації проєкту

### 3. Оголошення для комунікації

Згенеруйте оголошення для користувачів (Slack, email тощо):
- Нетехнічна мова
- Фокус на впливі на користувача
- Читабельне форматування (емодзі за бажанням)

Приклади розташування шаблонів:
- `.github/COMMUNICATION_TEMPLATE/slack-release.md`
- `docs/templates/release-announcement.md`

## Попередження про міграції

**Якщо виявлено міграції:**

```
╔══════════════════════════════════════════════════════════════════╗
║  ⚠️  [ATTENTION] DATABASE MIGRATIONS REQUIRED                    ║
╠══════════════════════════════════════════════════════════════════╣
║  This release contains X migration(s):                           ║
║  • 20250110_add_user_preferences                                 ║
║  • 20250112_create_audit_log_table                               ║
║  Action required: Run migration command after deployment         ║
╚══════════════════════════════════════════════════════════════════╝
```

**Якщо міграцій немає:**
```
✅ [OK] No database migrations required
```

## Перетворення технічного на продуктове

Перетворюйте технічні коміти на зрозумілі користувачу описи:

| Технічне | Продуктова/користувацька мова |
|----------|-------------------------------|
| "Optimize N+1 queries with DataLoader" | "Faster loading times for lists" |
| "Implement AI embeddings with pgvector" | "New intelligent search feature" |
| "Fix permissions scope bug" | "Resolved access issue for certain users" |
| "Migration webpack -> Turbopack" | *Лише внутрішнє - не повідомляти* |
| "Refactor React hooks architecture" | *Лише внутрішнє - не повідомляти* |
| "Add rate limiting to API endpoints" | "Improved system stability and security" |

## Категорії комітів

| Префікс | Категорія | Включати в оголошення? |
|---------|-----------|------------------------|
| `feat:` | Нові функції | Так |
| `fix:` | Виправлення багів | Так (якщо помітні користувачу) |
| `perf:` | Продуктивність | Так (спрощено) |
| `security:` | Безпека | Так |
| `refactor:` | Архітектура | Ні |
| `chore:` | Підтримка | Ні |
| `docs:` | Документація | Ні |
| `test:` | Тести | Ні |
| `build:` | Система збірки | Ні |
| `ci:` | CI/CD | Ні |

## Команди для виконання

```bash
# 1. Get last release tag
LAST_TAG=$(git tag --sort=-v:refname | grep -E '^v[0-9]+\.[0-9]+\.[0-9]+$' | head -n 1)

# 2. List commits since tag (excluding merges)
git log $LAST_TAG..HEAD --oneline --no-merges

# 3. Get commit details with PR numbers
git log $LAST_TAG..HEAD --format="%h %s" --no-merges

# 4. Check for migrations (adjust path to your ORM)
# Prisma:
git diff $LAST_TAG..HEAD --name-only -- prisma/migrations/
# Sequelize:
git diff $LAST_TAG..HEAD --name-only -- migrations/
# Django:
git diff $LAST_TAG..HEAD --name-only -- '**/migrations/*.py'
# Alembic:
git diff $LAST_TAG..HEAD --name-only -- alembic/versions/

# 5. Get PR details via GitHub CLI
gh api repos/{owner}/{repo}/pulls/{number}

# 6. Count statistics
TOTAL_PRS=$(git log $LAST_TAG..HEAD --oneline --merges | wc -l)
FEATURES=$(git log $LAST_TAG..HEAD --oneline --no-merges | grep -c 'feat:')
FIXES=$(git log $LAST_TAG..HEAD --oneline --no-merges | grep -c 'fix:')
```

## Семантичне версіонування

Визначте номер версії за змінами:

| Тип зміни | Підвищення версії | Приклад |
|-----------|-------------------|---------|
| Зміна, що ламає сумісність | MAJOR (X.0.0) | API видалено, несумісна зміна |
| Нова функція | MINOR (0.X.0) | Нова функціональність, зворотно сумісна |
| Виправлення бага / патч | PATCH (0.0.X) | Лише виправлення багів |

**Індикатори**:
- `BREAKING CHANGE:` у тілі коміту → MAJOR
- Є коміти `feat:` → MINOR
- Лише `fix:` / `perf:` → PATCH

## Інтеграція у воркфлоу

Типовий воркфлоу релізу:

```
1. Verify all PRs merged to develop branch
2. Run: /release-notes (or specify version/range)
3. Review generated outputs for accuracy
4. Create PR: develop -> main with "release" label
5. Add generated CHANGELOG section to CHANGELOG.md
6. Use generated PR body as PR description
7. After merge: Create and push git tag
8. Post communication announcement (Slack/email/etc.)
9. Monitor deployment and migrations
```

## Створення git-тега

Після мерджу PR створіть анотований тег:

```bash
# Create annotated tag
git tag -a v1.2.3 -m "Release v1.2.3: Brief description"

# Push tag to remote
git push origin v1.2.3

# Or push all tags
git push --tags
```

## Налаштування під конкретний проєкт

Адаптуйте ці шляхи до свого проєкту:

```
# Migration detection (adjust ORM path)
prisma/migrations/        → Your ORM migration directory
db/migrate/               → Rails migrations
alembic/versions/         → Alembic migrations

# Template files (create if needed)
.github/PULL_REQUEST_TEMPLATE/release.md
.github/COMMUNICATION_TEMPLATE/announcement.md
docs/templates/release-notes.md
```

## Поради

- **Запускайте з кореня репозиторію**: Гарантує коректну роботу git-команд
- **Автентифікуйте GitHub CLI**: Виконайте `gh auth login`, якщо потрібно
- **Перевіряйте перед публікацією**: Завжди звіряйте згенерований вміст
- **Зміни, що ламають сумісність**: Шукайте в повідомленнях комітів `BREAKING CHANGE:`
- **Пов'язані issues**: Додавайте номери issue/тікетів для відстежуваності
- **Міграції бази даних**: Тестуйте на staging перед продакшеном

## Граничні випадки

| Сценарій | Поведінка |
|----------|-----------|
| Тегів не знайдено | Почати з першого коміту |
| Немає комітів після останнього тега | Помилка: "No changes to release" |
| Кілька тегів на одному коміті | Використати найновіший за датою |
| Pre-release теги (v1.0.0-beta.1) | Виключити з пошуку «останнього релізу» |
| Коміти без conventional-формату | Категоризувати як "Other Changes" |

## Приклади використання

```bash
# Generate release notes from last tag to HEAD
/release-notes

# Specify version manually
/release-notes v1.5.0

# Specify range
/release-notes from v1.4.0 to HEAD

# Preview without creating files
/release-notes --preview

# Include pre-release commits
/release-notes --include-pre-release
```

Version/Range: $ARGUMENTS
