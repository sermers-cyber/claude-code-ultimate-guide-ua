---
name: git-worktree
description: Створення ізольованих git worktrees для розробки фіч без перемикання гілок
argument-hint: "<branch_name> [--from <base>]"
effort: medium
when_to_use: "Використовуйте, коли починаєте роботу над фічею, яку потрібно ізолювати від основного робочого простору."
disable-model-invocation: true
---

# Налаштування git worktree

Створення ізольованих git worktrees для розробки фіч без перемикання гілок.

**Основний принцип:** розумний вибір каталогу + оптимізація через симлінки + фонова перевірка = швидка й надійна ізоляція.

**Потрібно:** Git 2.5.0+ (липень 2015)

**Супутні команди:** [`/git-worktree-status`](../../commands/git-worktree-status.uk.md) | [`/git-worktree-remove`](../../commands/git-worktree-remove.uk.md) | [`/git-worktree-clean`](../../commands/git-worktree-clean.uk.md)

## Процес

1. **Перевірте назву гілки**: перевірка конвенції іменування й конфліктів
2. **Перевірте наявні каталоги**: `.worktrees/` або `worktrees/`
3. **Перевірте .gitignore**: переконайтеся, що каталог worktree ігнорується
4. **Створіть worktree**: `git worktree add`
5. **Залежності через симлінки**: повторне використання `node_modules/` з основного worktree
6. **Визначте провайдера бази даних**: перевірка можливості розгалуження БД
7. **Встановіть залежності**: автовизначення пакетного менеджера (якщо не через симлінк)
8. **Запустіть фонову перевірку**: перевірка типів + тести у фоні
9. **Повідомте розташування**: підтвердьте готовність зі статусом

## Прапорці

| Прапорець | Дія |
|------|--------|
| `--fast` | Пропустити встановлення залежностей і базові тести |
| `--isolated` | Нове встановлення `node_modules` (без симлінка) |
| `--skip-install` | Пропустити встановлення залежностей, залишити базові тести |

## Перевірка назви гілки

```bash
# Auto-prefix based on naming convention
# "auth" → "feat/auth" (default prefix)
# "fix/login-bug" → kept as-is
# "refactor/db-layer" → kept as-is

# Accepted prefixes: feat/, fix/, refactor/, chore/, docs/, test/, perf/
# If no prefix → default to feat/

# Reject invalid characters
echo "$BRANCH_NAME" | grep -qE '^[a-zA-Z0-9/_-]+$' || exit 1

# Check branch doesn't already exist
git show-ref --verify --quiet "refs/heads/$BRANCH_NAME" && echo "Branch already exists" && exit 1
```

## Вибір каталогу

### Порядок пріоритету

```bash
# 1. Check existing directories
ls -d .worktrees 2>/dev/null     # Preferred (hidden)
ls -d worktrees 2>/dev/null      # Alternative

# 2. Check CLAUDE.md for preference
grep -i "worktree.*director" CLAUDE.md 2>/dev/null

# 3. Ask user if neither exists
```

**Якщо існують обидва:** перевагу має `.worktrees/`.

## Перевірка безпеки

**Для локальних каталогів проєкту:**

```bash
# Check if directory in .gitignore
grep -q "^\.worktrees/$" .gitignore || grep -q "^worktrees/$" .gitignore
```

**Якщо його НЕМАЄ в .gitignore:**
1. Додайте рядок у .gitignore
2. Закомітьте зміну
3. Продовжуйте створення worktree

**Чому це критично:** запобігає випадковому коміту вмісту worktree.

## Кроки створення

```bash
# 1. Detect project name
project=$(basename "$(git rev-parse --show-toplevel)")

# 2. Create worktree with new branch
git worktree add .worktrees/$BRANCH_NAME -b $BRANCH_NAME

# 3. Navigate
cd .worktrees/$BRANCH_NAME
```

## Оптимізація залежностей (node.js)

**Поведінка за замовчуванням:** симлінк на `node_modules` з основного worktree, щоб уникнути повторних встановлень (економія ~30 с).

```bash
# Symlink node_modules (default, unless --isolated)
if [ -d "../../node_modules" ] && [ ! "$ISOLATED" = true ]; then
  ln -s "$(cd ../.. && pwd)/node_modules" node_modules
  echo "Symlinked node_modules from main worktree"
fi

# With --isolated: fresh install
if [ "$ISOLATED" = true ]; then
  pnpm install   # or npm/yarn based on lockfile detection
fi
```

**Коли використовувати `--isolated`:**
- Зміни схеми, що потребують інших версій пакетів
- Тестування оновлень залежностей
- Налагодження проблем із `node_modules`

## Автовизначення налаштувань (мультистек)

```bash
# Node.js (if not symlinked)
if [ -f package.json ] && [ ! -L node_modules ]; then
  pnpm install   # Detect from lockfile: pnpm-lock.yaml / yarn.lock / package-lock.json
fi

# Rust
if [ -f Cargo.toml ]; then cargo build; fi

# Python
if [ -f requirements.txt ]; then pip install -r requirements.txt; fi
if [ -f pyproject.toml ]; then poetry install; fi

# Go
if [ -f go.mod ]; then go mod download; fi
```

## Фонова перевірка

**Замість блокування на повному наборі тестів запускайте перевірку у фоні:**

```bash
# Create log directory
mkdir -p .worktree-logs

# Background type check (Node.js)
if [ -f tsconfig.json ]; then
  npx tsc --noEmit > .worktree-logs/typecheck.log 2>&1 &
  echo "Type check running in background (check with /git-worktree-status)"
fi

# Background test run
if [ -f package.json ]; then
  npx vitest run --reporter=json > .worktree-logs/tests.log 2>&1 &
  echo "Tests running in background (check with /git-worktree-status)"
fi
```

**З `--fast`:** пропустіть усі перевірки.

## Фінальний звіт

```
Worktree ready at <full-path>
Branch: feat/auth (created from main)
Dependencies: symlinked from main worktree
Background checks: type check + tests running
Check status: /git-worktree-status

Ready to implement <feature-name>
```

## Пропозиція гілки бази даних

**Після створення worktree визначте провайдера бази даних і запропонуйте ізоляцію.**

### Короткий довідник команд

| Провайдер | Рекомендована команда |
|----------|-------------------|
| **Neon** | `neonctl branches create --name <branch> --parent main` |
| **PlanetScale** | `pscale branch create <db> <branch>` |
| **Локальний Postgres** | `psql -c "CREATE SCHEMA <schema>;"` |
| **Інше** | Ручне налаштування або спільна БД |

**Приклад виводу:**

```
Worktree created at .worktrees/feat/auth

DB Isolation: neonctl branches create --name feat-auth --parent main
   Then update .env with new DATABASE_URL
   Full guide: ../workflows/database-branch-setup.md
```

### Налаштування .worktreeinclude

**Критично для змінних середовища:**

```bash
# .worktreeinclude (at project root)
.env
.env.local
.env.development
**/.claude/settings.local.json
```

**Чому:** без цього файли `.env` не будуть скопійовані у worktrees.

### Коли створювати гілку бази даних

| Сценарій | Створювати гілку? |
|----------|---------------|
| Міграції схеми | Так |
| Рефакторинг моделі даних | Так |
| Виправлення бага (без зміни схеми) | Ні |
| Експерименти з продуктивністю | Так |

**Див.:** [Посібник із налаштування гілок бази даних](../../workflows/database-branch-setup.uk.md) з повними воркфлоу.

## Короткий довідник

| Ситуація | Дія |
|-----------|--------|
| `.worktrees/` існує | Використовуйте його (перевірте .gitignore) |
| `worktrees/` існує | Використовуйте його (перевірте .gitignore) |
| Існують обидва | Використовуйте `.worktrees/` |
| Не існує жодного | Перевірте CLAUDE.md, потім запитайте користувача |
| Немає в .gitignore | Негайно додайте + закомітьте |
| Немає префікса гілки | Автоматично додайте префікс `feat/` |
| Проєкт Node.js | За замовчуванням симлінк на `node_modules` |
| Прапорець `--fast` | Пропустіть встановлення + тести |
| Прапорець `--isolated` | Нове встановлення `node_modules` |
| Виявлено Neon | Запропонуйте `neonctl branches create` |
| Виявлено PlanetScale | Запропонуйте `pscale branch create` |
| Немає .worktreeinclude | Створіть із патерном `.env` |

## Поширені помилки

**Пропуск перевірки .gitignore**
- Вміст worktree починає відстежуватися і засмічує git status

**Припущення щодо розташування каталогу**
- Дотримуйтеся пріоритету: наявний > CLAUDE.md > запитати

**Повне встановлення node_modules у кожному worktree**
- Марнує диск і час. За замовчуванням використовуйте симлінк, `--isolated` лише за потреби

**Не скопійовано .env у worktree**
- Симптом: Claude падає з "DATABASE_URL not found"
- Виправлення: додайте `.env` до `.worktreeinclude`

**Використання спільної бази даних для змін схеми**
- Симптом: конфлікти міграцій, зламане середовище розробки
- Виправлення: створіть гілку бази даних перед зміною схеми

## Використання

```
/git-worktree auth
/git-worktree fix/session-bug
/git-worktree feature/new-api --fast
/git-worktree refactor/db-layer --isolated
```

Назва гілки: $ARGUMENTS
