---
title: "Робочий процес каркасних проєктів (Skeleton Projects)"
description: "Використовуйте наявні, перевірені на практиці репозиторії як основу для нових проєктів"
tags: [workflow, architecture, template]
---

# Робочий процес каркасних проєктів (Skeleton Projects)

Використовуйте наявні, перевірені в реальних умовах репозиторії як каркас (scaffolding) для нових проєктів замість того, щоб починати розробку з нуля.

---

## Коли використовувати

- **Запуск нового проєкту** з відомим стеком технологій.
- **Стандартизація командних патернів** у кількох різних сервісах.
- **Швидке створення прототипів**, коли основні архітектурні рішення вже прийнято.
- **Онбординг (Onboarding)** нових членів команди за допомогою робочого референсу коду.

**Не використовуйте, коли**: ви досліджуєте невідомі технології (натомість використовуйте [Vibe Coding](#98-vibe-coding-skeleton-projects)) або коли вимоги є занадто унікальними для наявних шаблонів.

---

## Передумови

- Встановлений та налаштований інструмент Claude Code
- Доступ через Git до референсних репозиторіїв
- Чітке розуміння вимог до цільового проєкту

---

## Покрокова інструкція

### Фаза 1: Пошук та оцінка каркаса (Skeleton)

Не будуйте систему з нуля. Знайдіть наявний репозиторій, який відповідає вашій цільовій архітектурі.

**Крок 1: Пошук кандидатів**

```bash
# Ask Claude to help find reference repos
claude -p "I need a skeleton for a Next.js 15 app with:
- App Router
- Prisma ORM with PostgreSQL
- tRPC for type-safe API
- Tailwind CSS
- Jest + Playwright testing

Search GitHub for well-maintained starter templates.
Evaluate the top 3 by: last commit date, stars, dependency freshness, test coverage."
```

**Крок 2: Клонування та аудит**

```bash
git clone <candidate-repo> skeleton-eval
cd skeleton-eval
claude
```

```markdown
User: Audit this repository as a potential skeleton for our project:
1. List all dependencies and their versions (flag outdated ones)
2. Assess code quality: patterns, consistency, test coverage
3. Identify what we'd keep vs. what we'd remove
4. Flag any security concerns (vulnerable deps, exposed secrets)
5. Rate overall suitability (1-5) with specific justification
```

**Крок 3: Оцінка за допомогою суб-агентів (sub-agents)** (для детального аналізу)

```markdown
User: Run a multi-perspective evaluation of this skeleton:

Agent 1 (Security): Check for vulnerabilities, hardcoded secrets, unsafe patterns
Agent 2 (Architecture): Assess modularity, separation of concerns, scalability
Agent 3 (DX): Evaluate developer experience - setup time, documentation, tooling

Synthesize findings into a go/no-go recommendation.
```

### Фаза 2: Створення відгалуження (Fork) та кастомізація

**Крок 4: Створення вашого проєкту на основі каркаса**

```bash
# Create new repo from skeleton
mkdir my-project
cp -r skeleton-eval/. my-project/
cd my-project
rm -rf .git
git init
```

**Крок 5: Очищення та адаптація з Claude**

```markdown
User: Customize this skeleton for our project "Acme Dashboard":

1. Remove: example routes, demo data, sample tests
2. Keep: config structure, auth setup, database schema pattern, CI pipeline
3. Update: package.json (name, description, version 0.1.0)
4. Add: our CLAUDE.md with project conventions
5. Verify: `pnpm install && pnpm build && pnpm test` all pass after changes

Important: Don't break the working skeleton. Each removal should be followed
by a build check.
```

### Фаза 3: Розширення від каркаса до MVP

**Крок 6: Створення першої реальної функції**

```markdown
User: Using the patterns established in this skeleton, implement our first feature:
User Authentication (login + registration + password reset)

Follow the skeleton's existing patterns for:
- Route structure (match the example routes pattern)
- Service layer (match the existing service pattern)
- Test structure (match the example test pattern)
- Error handling (match the existing error pattern)

Create a task plan before starting implementation.
```

**Крок 7: Валідація цілісності каркаса**

```markdown
User: Now that we have one real feature, verify the skeleton still works:
1. Run full test suite
2. Check that the CI pipeline passes
3. Verify no skeleton patterns were broken
4. Confirm new code follows skeleton conventions consistently
```

### Фаза 4: Документування та ітерація

**Крок 8: Документування рішень у CLAUDE.md**

```markdown
User: Update CLAUDE.md with:
1. Which skeleton we started from (repo URL, commit hash)
2. What we kept and why
3. What we removed and why
4. Any pattern deviations from the original skeleton
5. Conventions we've added on top
```

---

## Хронологія розширення каркаса (Skeleton Expansion Timeline)

```
Skeleton (Day 1)     →    MVP (Week 1)      →    Production (Month 1)
──────────────────────────────────────────────────────────────────────
1 example route      →    5 real routes      →    20+ routes
1 example test       →    30 tests           →    200+ tests
Basic config         →    Env-based config   →    Multi-env + secrets
SQLite/local DB      →    Docker PostgreSQL  →    Managed DB + migrations
No CI                →    Basic CI           →    Full CI/CD pipeline
README only          →    CLAUDE.md + ADRs   →    Full documentation
```

---

## Реальний приклад: мікросервіс на основі каркаса

```bash
# 1. Clone proven skeleton
git clone https://github.com/example/express-prisma-starter skeleton
cd skeleton && claude

# 2. Audit (2 minutes)
User: "Audit this skeleton. Is it suitable for a billing microservice?"
# Claude: Reports deps, patterns, suitability score

# 3. Customize (5 minutes)
User: "Strip examples, rename to billing-service, add our CLAUDE.md"
# Claude: Removes demo code, updates config, adds project context

# 4. First feature (30 minutes)
User: "Implement invoice creation endpoint following skeleton patterns"
# Claude: Creates route, service, repo, tests matching skeleton conventions

# 5. Verify (2 minutes)
User: "Run all tests, verify build, check skeleton patterns preserved"
# Claude: All green, patterns consistent
```

---

## Поширені помилки

| Помилка | Симптом | Вирішення |
|---------|---------|-----|
| Каркас занадто складний | Витрачається більше часу на видалення зайвого, ніж на розробку | Оберіть простіший каркас або створіть власний мінімальний |
| Застарілі залежності | Попередження про безпеку під час встановлення | Перевіряйте дату останнього коміту перед клонуванням (ідеально < 6 місяців) |
| Порушення патернів каркаса | Новий код відхиляється від конвенцій каркаса | Додайте патерни каркаса до вашого CLAUDE.md як обмеження |
| Збереження мертвого коду | Невикористовуваний приклад коду засмічує проєкт | Безжально видаляйте зайве під час Фази 2, перевіряйте збірку після кожного видалення |
| Відсутність документації | Забули, чому саме цей каркас було обрано | Негайно задокументуйте це в CLAUDE.md (Фаза 4) |

---

## Пов'язані робочі процеси

- **[Vibe Coding](#98-vibe-coding-skeleton-projects)**: дослідження перед вибором каркаса.
- **[Plan-Driven Development](./plan-driven.uk.md)**: планування кастомізації каркаса перед виконанням.
- **[TDD з Claude](./tdd-with-claude.uk.md)**: розширення функцій каркаса за принципом «тести попереду».
- **[Permutation Frameworks](#919-permutation-frameworks)**: тестування кількох варіантів каркасів перед остаточним вибором.

---

**Останнє оновлення**: Січень 2026

---
**Локалізація**: [Serhii (MacPlus Software)](https://macplus-software.com)
*Остання синхронізація: Травень 2026*
