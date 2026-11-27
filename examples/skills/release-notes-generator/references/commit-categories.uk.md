# Правила категоризації комітів

Цей документ визначає, як категоризувати коміти за форматом Conventional Commits.

## Основні категорії

### Функції (`feat:`)
**CHANGELOG**: New Features
**Slack**: Так - завжди включати
**Приклади**:
- `feat(dashboard): add export report system`
- `feat(search): add fuzzy matching`
- `feat(api): add batch operations endpoint`

### Виправлення багів (`fix:`)
**CHANGELOG**: Bug Fixes
**Slack**: Так - якщо помітні користувачу; Ні - якщо внутрішні
**Приклади**:
- `fix(auth): correct token refresh flow` -> Включити в Slack
- `fix(test): correct mock setup` -> НЕ включати в Slack

### Продуктивність (`perf:`)
**CHANGELOG**: Technical Improvements > Performance
**Slack**: Так - спрощено ("Performance improvement")
**Приклади**:
- `perf(api): optimize N+1 queries with batching`
- `perf(build): reduce bundle size by 30%`

### Безпека (`security:` або `fix(security):`)
**CHANGELOG**: Security
**Slack**: Так - завжди, із відповідним рівнем деталізації
**Приклади**:
- `security: fix CVE-2025-55182 dependency RCE`
- `fix(security): prevent XSS in user input`

## Другорядні категорії (лише CHANGELOG)

### Рефакторинг (`refactor:`)
**CHANGELOG**: Technical Improvements > Architecture
**Slack**: Ні
**Приклади**:
- `refactor(hooks): migrate to new pattern`
- `refactor(permissions): extract to service layer`

### Документація (`docs:`)
**CHANGELOG**: Documentation (якщо суттєва)
**Slack**: Ні
**Приклади**:
- `docs: update CLAUDE.md with new patterns`
- `docs(api): add endpoint documentation`

### Тести (`test:`)
**CHANGELOG**: Tests (лише кількість)
**Slack**: Ні
**Приклади**:
- `test(api): add endpoint integration tests`
- `test(e2e): add workflow tests`

### Chores (`chore:`)
**CHANGELOG**: Ні (якщо не суттєві)
**Slack**: Ні
**Приклади**:
- `chore: update dependencies`
- `chore(ci): fix workflow permissions`

### Стиль (`style:`)
**CHANGELOG**: Ні
**Slack**: Ні
**Приклади**:
- `style: apply prettier formatting`
- `style(eslint): fix linting errors`

## Патерни scope

Поширені scope:

| Scope | Область |
|-------|---------|
| `auth` | Автентифікація |
| `billing` | Білінг і платежі |
| `api` | Ендпоінти API |
| `ui` | UI-компоненти |
| `dashboard` | Функції дашборда |
| `notifications` | Система сповіщень |
| `search` | Функціональність пошуку |
| `user` | Керування користувачами |
| `db` | База даних і міграції |
| `permissions` | Система дозволів |
| `admin` | Адмін-панель |

## Зміни, що ламають сумісність

Позначаються `!` після типу/scope або `BREAKING CHANGE:` у футері:
- `feat(api)!: change status enum`
- `fix(auth)!: require new token format`

**CHANGELOG**: розділ Breaking Changes
**Slack**: Так - з інструкціями з міграції

## Витягування номерів PR

Витягуйте номери PR з:
1. Повідомлення коміту: `(#123)`
2. Merge-коміту: `Merge pull request #123`
3. GitHub API: перехресне зіставлення за SHA коміту

## Зв'язування з issues в error tracker

Зіставляйте патерни:
- `[error-tracker]: PROJECT-XX`
- `fixes PROJECT-XX`
- `closes #XX` (GitHub issue)

## Обчислення статистики

Підрахунок для статистики релізу:
- **PRs**: унікальні номери PR
- **Features**: коміти `feat:`
- **Bugs**: коміти `fix:` (крім test/internal)
- **Improvements**: `perf:` + `refactor:` + покращення UI
- **Security**: коміти `security:`
- **Breaking**: коміти з `!` або `BREAKING CHANGE`
