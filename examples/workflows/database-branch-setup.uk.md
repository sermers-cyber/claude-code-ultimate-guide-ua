---
title: "Налаштування гілок бази даних із worktrees"
description: "Посібник з ізольованої розробки функцій із використанням гілок бази даних у Neon або PlanetScale"
tags: [workflow, git, devops]
---

# Налаштування гілок бази даних із worktrees

Повний посібник з ізольованої розробки функцій із гілками бази даних.

**Джерело**: натхненно [гілкуванням баз даних Neon](https://neon.com/docs/introduction/branching) і [воркфлоу гілкування PlanetScale](https://planetscale.com/docs/concepts/branching).

---

## Коротко (90% випадків використання)

**З Neon:**
```bash
/git-worktree feature/auth
cd .worktrees/feature-auth
neonctl branches create --name feature-auth --parent main
# Copy DATABASE_URL from output to .env
pnpm prisma migrate dev
```

Готово. Переходьте до [прикладів воркфлоу](#приклади-воркфлоу).

---

## Налаштування провайдера

### Neon (рекомендовано)

**Встановіть CLI:**
```bash
npm install -g neonctl
neonctl auth
```

**Створіть гілку:**
```bash
neonctl branches create --name <branch-name> --parent main
```

**Отримайте рядок підключення:**
```bash
neonctl connection-string --branch <branch-name>
```

**Оновіть .env у worktree:**
```bash
echo "DATABASE_URL=<connection-string>" > .worktrees/<branch>/.env
```

**Видаліть, коли закінчите:**
```bash
neonctl branches delete <branch-name>
```

**Переваги:**
- Миттєве створення гілки (~1 с)
- Справжній copy-on-write (ефективне сховище)
- Скидання гілки без втрати даних
- Чудовий CLI

**Обмеження:**
- Потрібне налаштування пулу з'єднань

---

### PlanetScale

**Встановіть CLI:**
```bash
brew install pscale
pscale auth login
```

**Створіть гілку:**
```bash
pscale branch create <database-name> <branch-name>
```

**Підключіться (запускає локальний проксі):**
```bash
pscale connect <database-name> <branch-name> --port 3309
```

**Оновіть .env, щоб використовувати localhost:3309:**
```bash
echo "DATABASE_URL=mysql://root@127.0.0.1:3309/<database-name>" > .worktrees/<branch>/.env
```

**Видаліть, коли закінчите:**
```bash
pscale branch delete <database-name> <branch-name>
```

**Переваги:**
- Git-подібний воркфлоу для схеми
- Вбудований diff схеми
- Безпечні запити на розгортання

**Обмеження:**
- Різний рядок підключення на кожну гілку
- Для локальної розробки потрібен `pscale connect`

---

### Локальний Postgres (на основі схем)

Для проєктів без хмарної БД:

**Створіть схему:**
```bash
psql $DATABASE_URL -c "CREATE SCHEMA <schema-name>;"
```

**Оновіть .env, щоб використовувати схему:**
```bash
DATABASE_URL="postgresql://user:pass@localhost:5432/db?schema=<schema-name>"
```

**Запустіть міграції в схемі:**
```bash
npx prisma migrate deploy
```

**Прибирання:**
```bash
psql $DATABASE_URL -c "DROP SCHEMA <schema-name> CASCADE;"
```

**Переваги:**
- Безкоштовно
- Повний контроль

**Обмеження:**
- Ручне налаштування
- Немає автоматичного copy-on-write

---

## Коли використовувати гілки бази даних

### Дерево рішень

```
Does feature touch database schema?
├─ No → Use shared database, skip branch creation
└─ Yes → Create database branch
    ├─ Using Neon/PlanetScale? → Use native branching
    ├─ Using local Postgres? → Create dedicated schema
    └─ Other provider? → Consider Docker or shared DB with caution
```

### Таблиця сценаріїв

| Сценарій | Використовувати гілку БД? | Обґрунтування |
|----------|---------------------------|---------------|
| Додавання міграцій бази даних | ✅ Так | Ізолювати зміни схеми |
| Рефакторинг моделі даних | ✅ Так | Безпечно експериментувати |
| Тестування продуктивності | ✅ Так | Виділені ресурси |
| Виправлення бага (без зміни схеми) | ❌ Ні | Спільна БД підійде |
| Функція зі змінами схеми | ✅ Так | Уникнути конфліктів |
| Хотфікс (терміново) | ❌ Ні | Швидкість важливіша за ізоляцію |

---

## Приклади воркфлоу

### Приклад 1: функція зі зміною схеми

```bash
# 1. Create worktree + DB branch
/git-worktree feature/add-user-roles
cd .worktrees/feature-add-user-roles

# 2. Create Neon branch
neonctl branches create --name feature-add-user-roles --parent main

# 3. Update .env with new DATABASE_URL
# (Copy from neonctl output)

# 4. Create migration in steps
npx prisma migrate dev --name step1_add_role_column
npx prisma migrate dev --name step2_migrate_existing_users
npx prisma migrate dev --name step3_add_constraints

# 5. Test entire migration sequence
pnpm prisma migrate reset --skip-seed
pnpm prisma migrate deploy
pnpm test

# 6. If successful, merge PR
# 7. Apply to main DB after deploy
```

---

### Приклад 2: експерименти з моделлю даних

```bash
# Try different schemas without commitment
/git-worktree experiment/normalize-addresses
cd .worktrees/experiment-normalize-addresses

# Create DB branch
neonctl branches create --name experiment-normalize-addresses --parent main

# Completely remodel data
# Test with real-ish data
# Compare performance

# If better → merge
# If worse → delete branch (no cleanup needed)
```

---

### Приклад 3: паралельна розробка функцій

```bash
# Terminal 1
/git-worktree feature/payments
cd .worktrees/feature-payments
neonctl branches create --name feature-payments --parent main
# DATABASE_URL → feature-payments branch

# Terminal 2
/git-worktree feature/subscriptions
cd .worktrees/feature-subscriptions
neonctl branches create --name feature-subscriptions --parent main
# DATABASE_URL → feature-subscriptions branch

# Both can modify schema independently
# No conflicts until merge
```

---

## Контрольний список

### Перед початком роботи у worktree зі змінами БД:
- [ ] `.worktreeinclude` містить `.env`
- [ ] Гілку бази даних створено (якщо провайдер це підтримує)
- [ ] `.env` у worktree оновлено новим `DATABASE_URL`
- [ ] З'єднання перевірено (`npx prisma db execute --stdin <<< "SELECT 1;"`)
- [ ] Міграції застосовано (`npx prisma migrate dev`)

### Після злиття PR:
- [ ] Git worktree видалено
- [ ] Гілку бази даних видалено
- [ ] Немає «осиротілих» з'єднань

---

## Усунення несправностей

### Проблема: "Database not found" у worktree
**Виправлення:** перевірте, що `.env` було скопійовано, і налаштування `.worktreeinclude`

### Проблема: міграції зачіпають головну базу даних
**Виправлення:** переконайтеся, що `DATABASE_URL` вказує на гілку, а не на main

### Проблема: не вдається створити гілку Neon - "not authenticated"
**Виправлення:** виконайте `neonctl auth`, щоб увійти

### Проблема: гілка PlanetScale існує, але не вдається підключитися
**Виправлення:** використовуйте проксі `pscale connect`, не підключайтеся напряму

### Проблема: "Branch already exists"
```bash
# List existing branches
neonctl branches list

# Delete if stale
neonctl branches delete <branch-name> --force
```

### Проблема: міграція не вдалася
```bash
# Reset DB branch to clean state
neonctl branches reset <branch-name> --parent main

# Re-apply migrations
npx prisma migrate deploy
```

---

## Примітки щодо безпеки

⚠️ **Пам'ятайте:**
- Гілки бази даних за замовчуванням НЕ потрапляють у `.gitignore`
- Додайте `.env` до `.worktreeinclude`, щоб облікові дані копіювалися
- Ніколи не комітьте `DATABASE_URL` зі справжніми обліковими даними
- Використовуйте різні облікові дані для різних середовищ

✅ **Найкраща практика:**
```bash
# .worktreeinclude
.env
.env.local
.env.development

# Each worktree gets copy of credentials
# But each points to different DB branch
```

---

## Розширені патерни

### Патерн: поступова міграція схеми

```bash
# 1. Create worktree + DB branch
/git-worktree migration/split-user-table
cd .worktrees/migration-split-user-table

# 2. Create migration in steps
npx prisma migrate dev --name step1_add_new_columns
npx prisma migrate dev --name step2_migrate_data
npx prisma migrate dev --name step3_drop_old_columns

# 3. Test entire migration sequence
pnpm prisma migrate reset --skip-seed
pnpm prisma migrate deploy

# 4. If successful, merge PR
# 5. Apply to main DB after deploy
```

### Патерн: бенчмаркінг продуктивності

```bash
# Create worktree with isolated DB
/git-worktree perf/optimize-queries
cd .worktrees/perf-optimize-queries

# DB branch lets you:
# - Add indexes without affecting dev
# - Run load tests safely
# - Compare before/after metrics

# Merge proven optimizations only
```

---

**Пов'язані посібники:**
- [Довідник команди Git Worktree](../commands/git-worktree.uk.md)
- [Документація Neon Branching](https://neon.com/docs/introduction/branching)
- [PlanetScale Branching](https://planetscale.com/docs/concepts/branching)
