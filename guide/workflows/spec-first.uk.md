---
title: "Розробка спочатку зі специфікацією (Spec-First) з Claude"
description: "Визначайте специфікації в CLAUDE.md перед початком реалізації для структурованої розробки"
tags: [workflow, architecture, config]
---

# Розробка спочатку зі специфікацією (Spec-First) з Claude

> **Confidence**: Рівень 2 — Валідовано багатьма виробничими командами та узгоджується з офіційними рекомендаціями SDD.

Визначайте, що саме ви хочете отримати, в CLAUDE.md ПЕРЕД тим, як просити Claude писати код. Одна добре структурована ітерація дорівнює 8 неструктурованим.

---

## Зміст

1. [Стисло (TL;DR)](#tldr)
2. [Патерн](#патерн)
3. [Гранулярність завдань: вибір обсягу роботи для агентів](#гранулярність-завдань-вибір-обсягу-роботи-для-агентів)
4. [Шаблони специфікацій для CLAUDE.md](#шаблони-специфікацій-для-claudemd)
5. [Покроковий робочий процес](#покроковий-робочий-процес)
6. [Інтеграція з інструментами](#інтеграція-з-інструментами)
7. [Коли використовувати](#коли-використовувати)
8. [Антипатерни](#антипатерни)
9. [Дивіться також](#дивіться-також)

---

## TL;DR

```
1. Write spec in CLAUDE.md
2. Claude reads spec automatically
3. Implementation follows spec exactly
4. Verify against spec
```

CLAUDE.md — ЦЕ і є ваш файл специфікації. Ставтеся до нього як до контракту.

---

## Патерн

Розробка спочатку зі специфікацією (Spec-First Development) змінює типовий процес кодування з ШІ:

```
Traditional:        Spec-First:
───────────         ──────────
Prompt → Code       Spec → Prompt → Code → Verify
  │                   │               │       │
  └─ Hope it's       └── Contract    └── Follows spec
     what you want        defined          └── Check against spec
```

Специфікація стає єдиним джерелом правди (source of truth), яке:
- Обмежує те, що створює Claude
- Документує рішення для команди
- Дозволяє перевірити повноту реалізації

---

## Гранулярність завдань: вибір обсягу роботи для агентів

Перед написанням специфікації переконайтеся, що завдання має правильний розмір. Агенти працюють найкраще з **вертикальними зрізами (vertical slices)** — тонкими наскрізними блоками роботи, які проходять через усі рівні архітектури, але реалізують рівно один завершений сценарій поведінки користувача (наприклад, «скидання пароля через email», а не «система автентифікації»).

**Практичне правило**: одна сесія агента = один вертикальний зріз. Якщо в описі завдання між двома сценаріями використання стоїть сполучник «та», розділіть його.

### Контрольний список якості PRD

Запускайте цю перевірку перед передачею будь-кого завдання агенту. Шість вимірів для перевірки:

| Вимір | Запитання | Попереджувальний знак (Red flag) |
|-----------|----------------|----------|
| **Чіткість проблеми** | Чи є формулювання проблеми однозначним? | «Покращити продуктивність» |
| **Тестовані критерії** | Чи можна перевірити виконання автоматично? | «Працює добре» |
| **Межі обсягу роботи** | Що саме знаходиться ПОЗА межами (out of scope) проєкту? | Нічого не вказано як виключене |
| **Візуальна готовність** | Як саме виглядає «готове» завдання для користувача? | Лише внутрішній технічний опис |
| **Чіткість вимог** | У специфікації немає деталей реалізації? | «Використовувати Redis для кешування» |
| **Термінологія** | Чи використовуються однакові терміни скрізь? | Змішування слів «користувач» та «акаунт» |

Завдання, яке не відповідає двом або більше вимірам, потребує доопрацювання перед тим, як агент почане працювати над ним. Аналіз специфікації дозволяє виявити неоднозначність, яка інакше спливе як неправильна реалізація в середині сесії.

```
❌ Too big, ambiguous:
"Add user authentication to the app"

  ✅ One vertical slice:
"Users can log in with email + password.
- POST /auth/login returns JWT on success, 401 on failure
- Invalid credentials show 'Email or password incorrect' (not which is wrong)
- Session expires after 24h
- Out of scope: OAuth, password reset, remember me"
```

### Список функцій (Feature List): машиночитаний контроль обсягу роботи

Список функцій — це файл JSON, який відстежує обсяг роботи та стан виконання кожної функції між сесіями агентів. На відміну від PRD, який описує загальний намір, список функцій є робочим контрактом для агента: він зчитується на початку сесії, оновлюється в кінці сесії та зберігається під час передачі завдань.

Кожен запис про функцію має три обов'язкові поля. Поле `description` повідомляє агенту, що саме потрібно створити. Поле `verify` — це команда оболонки (shell command), яка повертає 0 у разі успішного виконання. Це важливо, оскільки змушує визначати «готовність» як щось виконуване, а не просто описове. Поле `status` відстежує прогрес через односпрямований кінцевий автомат: `not_started` → `active` → `blocked` → `passing`. Запис може рухатися лише вперед, ніколи назад. Коли функція досягає статусу `passing`, у полі `evidence` фіксується те, що це доводить (назва тесту, вихідні дані команди або конкретний рядок логу).

Тут діє правило WIP=1: лише одна функція може перебувати в статусі `active` у будь-який момент часу. Кілька одночасно активних функцій призводять до частково виконаної роботи та неповної валідації.

Зберігайте `feature_list.json` у корені проєкту поруч із `AGENTS.md`. На початку сесії агент читає його, щоб знати, що було зроблено і що обрати далі. Наприкінці сесії агент записує оновлений стан і докази перед створенням коміту.

Список функцій працює разом із `claudedocs/handoffs/`. Разом ці два артефакти дають наступній сесії як робочий стан (які функції готові та перевірені), так і наративний контекст (що сталося, що було випробувано, що залишилося відкритим). Жоден з них не замінює інший.

Мінімальний приклад, що показує дві функції на різних етапах:

```json
{
  "features": [
    {
      "id": "feat-001",
      "name": "Document Import",
      "description": "Allow users to import PDF and TXT files from local filesystem",
      "verify": "npm test -- --grep 'document import'",
      "status": "passing",
      "evidence": "npm test: 12 passed, 0 failed (2026-05-01 14:22)"
    },
    {
      "id": "feat-002",
      "name": "Document Chunking",
      "description": "Split imported documents into ~500-character chunks with metadata",
      "verify": "npm test -- --grep 'chunking'",
      "status": "not_started",
      "evidence": "",
      "dependencies": ["feat-001"]
    }
  ]
}
```

Поле `evidence` для `feat-001` точно показує, що саме було запущено і коли. Запис `feat-002` перебуває в статусі `not_started` з порожнім полем `evidence`, очікуючи, поки `feat-001` буде підтверджено як `passing` перед тим, як стати `active`. Цей патерн описано в інженерному блозі Anthropic у статті [harness design for long-running applications](https://www.anthropic.com/engineering/harness-design-long-running-apps). Готовий до використання шаблон доступний у `examples/workflows/feature-list.json`.

---

## Шаблони специфікацій для CLAUDE.md

### Специфікація функції (Найбільш поширена)

```markdown
## Feature: [Name]

### Description
[2-3 sentences explaining the feature purpose]

### Capabilities
- MUST: [Required functionality]
- MUST: [Another requirement]
- SHOULD: [Nice to have]
- MUST NOT: [Explicit exclusions]

### Tech Stack
- Required: [lib1, lib2, lib3]
- Forbidden: [lib4, lib5]

### Acceptance Criteria
- [ ] Criterion 1: [Specific, testable condition]
- [ ] Criterion 2: [Another condition]
- [ ] Criterion 3: [Edge case handling]

### API Contract (if applicable)
- Endpoint: POST /api/[resource]
- Request: { field1: string, field2: number }
- Response: { id: string, created: timestamp }
- Errors: 400 (validation), 404 (not found), 500 (server)
```

### Специфікація архітектури

```markdown
## Architecture: [Component Name]

### Purpose
[Why this component exists]

### Boundaries
- Owns: [What this component is responsible for]
- Delegates to: [What other components handle]
- Does NOT: [Explicit non-responsibilities]

### Dependencies
- Upstream: [Components that call this]
- Downstream: [Components this calls]

### Data Flow
```
Input → Validation → Processing → Output
         │              │
         └─ Errors ─────┘
```

### Constraints
- Performance: [Response time, throughput]
- Security: [Auth requirements, data handling]
- Scalability: [Expected load, limits]
```

### Специфікація API

```markdown
## API: [Endpoint Name]

### Endpoint
`POST /api/v1/[resource]`

### Authentication
Bearer token required. Scopes: `read:resource`, `write:resource`

### Request
```json
{
  "field1": "string (required, max 255 chars)",
  "field2": "number (optional, default: 0)",
  "nested": {
    "subfield": "boolean"
  }
}
```

### Response
```json
{
  "id": "uuid",
  "created_at": "ISO 8601 timestamp",
  "data": { ... }
}
```

### Error Codes
| Code | Meaning | Response Body |
|------|---------|---------------|
| 400 | Validation failed | `{ "errors": [...] }` |
| 401 | Not authenticated | `{ "message": "..." }` |
| 403 | Not authorized | `{ "message": "..." }` |
| 404 | Resource not found | `{ "message": "..." }` |
```

---

## Покроковий робочий процес

### Крок 1: Напишіть специфікацію

Перед будь-яким запитом на реалізацію додайте специфікацію до CLAUDE.md:

```markdown
## Feature: User Authentication

### Capabilities
- MUST: Email/password login
- MUST: JWT token generation
- MUST: Password hashing with bcrypt
- SHOULD: Remember me functionality
- MUST NOT: Store plain text passwords

### Tech Stack
- Required: bcrypt, jsonwebtoken
- Forbidden: passport.js (too heavy for this use case)

### Acceptance Criteria
- [ ] User can login with valid credentials
- [ ] Invalid credentials return 401
- [ ] Token expires after 24h (or 7d with remember me)
- [ ] Passwords hashed with cost factor 12
```

### Крок 2: Вкажіть посилання на специфікацію в запиті

```
Implement the User Authentication feature as specified in CLAUDE.md.
Follow the acceptance criteria exactly.
```

Claude автоматично прочитає CLAUDE.md і дотримуватиметься специфікації.

### Крок 3: Перевірте відповідність специфікації

Після реалізації виконайте перевірку:

```
Review the implementation against the User Authentication spec.
Check off each acceptance criterion that's satisfied.
List any gaps.
```

### Крок 4: Оновіть специфікацію за потреби

Якщо вимоги змінюються під час реалізації:

```
Update the User Authentication spec to include:
- MUST: Rate limiting (5 attempts per minute)
Then implement the rate limiting.
```

---

## Інтеграція з інструментами

### Зі Spec Kit (для нових проєктів / Greenfield)

```bash
# Install Spec Kit
npx @anthropic/spec-kit init

# Use slash commands
/speckit.constitution  # Define project guardrails
/speckit.specify       # Write feature specs
/speckit.plan          # Create implementation plan
/speckit.implement     # Build from spec
```

### З OpenSpec (для наявних проєктів / Brownfield)

```bash
# Install OpenSpec
npm install -g @fission-ai/openspec@latest
openspec init

# Use slash commands
/openspec:proposal "Add dark mode"  # Create change proposal
/openspec:apply add-dark-mode       # Implement changes
/openspec:archive add-dark-mode     # Merge to specs
```

### З Plan Mode

```
[Press Shift+Tab to enter Plan Mode]

I need to implement the Payment Processing feature.
Review the spec in CLAUDE.md and create an implementation plan.
```

---

## Коли використовувати

### Використовуйте Spec-First

| Сценарій | Чому |
|----------|-----|
| Нові функції | Визначення перед створенням |
| Проєкт API | Контракт має бути чітким |
| Архітектурні рішення | Документування обмежень |
| Співпраця в команді | Спільне розуміння |
| Складні вимоги | Зменшення неоднозначності |

### Пропускайте Spec-First

| Сценарій | Чому |
|----------|-----|
| Швидкі виправлення | Накладні витрати того не варті |
| Дослідження коду | Ви ще самі не знаєте, чого хочете |
| Прототипування | Вимоги часто змінюватимуться |
| Зміни в один рядок | Очевидний намір |

---

## Антипатерни

### Розмиті специфікації

```markdown
# Wrong
## Feature: User Management
- Handle users

# Right
## Feature: User Management
### Capabilities
- MUST: Create user with email, password, name
- MUST: Update user profile (name, avatar)
- MUST: Soft delete (mark as inactive, don't remove data)
- MUST NOT: Allow duplicate emails
```

### Специфікація після коду

```
# Wrong workflow
1. Ask Claude to implement feature
2. Write spec documenting what was built

# Right workflow
1. Write spec defining what should be built
2. Ask Claude to implement from spec
```

### Ігнорування заборонених речей (Forbidden)

```markdown
# Don't forget exclusions
### Tech Stack
- Required: React, TypeScript
- Forbidden: jQuery, vanilla JS, class components
             ↑ These constraints prevent drift
```

---

## Модульний дизайн специфікацій

**Патерн**: розділяйте великі специфікації на кілька окремих файлів замість того, щоб втискати все в один єдиний CLAUDE.md.

### Проблема: Монолітний CLAUDE.md

Коли розмір специфікації перевищує ~200 рядків, виникає кілька проблем:

- **Засмічення контексту (context pollution)**: Claude важко витягувати релевантну інформацію з роздутого контексту.
- **Когнітивне перевантаження**: розробники не можуть швидко знайти потрібні дані.
- **Труднощі з підтримкою**: оновлення однієї області вимагає навігації по непов'язаних розділах.
- **Зниження продуктивності**: великі файли CLAUDE.md уповільнюють завантаження та обробку контексту.

### Коли розділяти

| Поріг | Дія |
|-----------|--------|
| **<100 рядків** | Один файл CLAUDE.md є цілком прийнятним |
| **100-200 рядків** | Розгляньте можливість розділення, якщо існують окремі домени |
| **>200 рядків** | **Розділяйте негайно** — ви перевищили поріг когнітивного навантаження |
| **Багатокомандні проєкти** | Розділяйте за доменами/власністю незалежно від розміру |

### Стратегії розділення

**1. Розділення на основі функцій (Feature-Based Split)**

```
CLAUDE.md              # Core project context
CLAUDE-auth.md         # Authentication spec
CLAUDE-api.md          # API endpoints spec
CLAUDE-billing.md      # Payment processing spec
```

**2. Розділення на основі ролей (Role-Based Split)**

```
CLAUDE.md              # Shared conventions
CLAUDE-frontend.md     # UI/UX specifications
CLAUDE-backend.md      # API/database specs
CLAUDE-infra.md        # DevOps/deployment specs
```

**3. Розділення на основі процесів (Workflow-Based Split)**

```
CLAUDE.md              # Daily development rules
CLAUDE-testing.md      # Test specifications
CLAUDE-release.md      # Release process spec
CLAUDE-security.md     # Security requirements
```

### Патерн реалізації

**Основний CLAUDE.md** (залишається лаконічним):
```markdown
# Project: [NAME]

## Tech Stack
[Core technologies]

## Commands
[Daily commands]

## Rules
[Universal rules]

## Detailed Specs
- Authentication: See @CLAUDE-auth.md
- API Design: See @CLAUDE-api.md
- Testing: See @CLAUDE-testing.md
```

**CLAUDE-auth.md** (сфокусована специфікація):
```markdown
# Authentication Specification

## Capabilities
- MUST: JWT-based authentication
- MUST: Refresh token rotation
- MUST NOT: Store tokens in localStorage

## API Contract
[Detailed auth endpoints...]

## Security Requirements
[Specific auth security rules...]
```

**Переваги**:
- Claude може посилатися на конкретні файли за допомогою `@CLAUDE-auth.md`.
- Швидше завантаження контексту (тільки релевантні специфікації).
- Простіша підтримка (редагування одного домену без впливу на інші).
- Краща співпраця в команді (закріплення відповідальності за окремі файли специфікацій).

**Джерело**: Addy Osmani, ["How to write a good spec for AI agents"](https://addyosmani.com/blog/good-spec/) (Січень 2026)

---

## Операційні межі (Operational Boundaries)

**Патерн**: визначте чіткі межі для того, що ШІ-агенти повинні виконувати автоматично, про що повинні запитувати, а до чого ніколи не мають торкатися.

### Трирівнева система

Традиційні специфікації використовують бінарні обмеження (MUST/MUST NOT), але операційна робота вимагає трьох рівнів:

| Рівень | Значення | Відображення в Claude Code |
|------|---------|---------------------|
| **Always (Завжди)** | Виконувати автоматично без запитань | Режим автопідтвердження (Auto-accept mode) |
| **Ask First (Запитати)** | Отримати підтвердження користувача перед виконанням | Режим за замовчуванням (Default mode) |
| **Never (Ніколи)** | Заблокувати або вимагати Plan Mode | Режим планування (Plan mode) / Блокування хуками |

### Шаблон операційних меж (Operational Boundaries Template)

```markdown
## Boundaries

### Always (Auto-accept)
- Run tests after code changes
- Format code with Prettier
- Update imports when moving files
- Fix linting errors
- Add type annotations for untyped code

### Ask First (Confirm)
- Modify database schemas
- Add new dependencies
- Change API contracts
- Refactor >50 lines of code
- Update configuration files

### Never (Block)
- Push to production branch
- Commit secrets or API keys
- Delete data without backup
- Modify CI/CD workflows without review
- Bypass security checks
```

### Відображення на дозволи Claude Code

**Always → Permission Allowlist**:
```json
// In .claude/settings.json
{
  "permissions": {
    "allow": [
      "Bash(npm test*)",
      "Bash(npx prettier*)",
      "Bash(npx tsc*)"
    ]
  }
}
```

**Ask First → Default Mode**:
- Стандартна поведінка, запит підтвердження для кожної дії.
- Використовуйте для дій із помірним ризиком або впливом.

**Never → Plan Mode + Hooks**:
```bash
# Hook configured via settings.json (PreToolUse event)
#!/bin/bash
if [[ "$TOOL_NAME" == "Bash" ]] && [[ "$INPUT" =~ "git push origin main" ]]; then
  echo "BLOCKED: Direct push to main blocked. Use feature branches."
  exit 2  # Send feedback to Claude (non-zero exit blocks the action)
fi
```

### Структура прийняття рішень

Для кожної дії запитайте себе:
1. **Чи може це призвести до втрати даних?** → Ask First або Never.
2. **Чи можна це скасувати за допомогою git?** → Можливо Always.
3. **Чи впливає це на інших розробників?** → Ask First.
4. **Чи є це ризиком для безпеки?** → Never.
5. **Чи є це частиною стандартного робочого процесу?** → Always.

### Приклад: Розробка API

```markdown
### Always
- Run unit tests (npm test)
- Validate request schemas
- Generate API documentation
- Check response formats

### Ask First
- Add new API endpoints
- Change existing endpoint signatures
- Modify authentication requirements
- Update rate limiting rules

### Never
- Expose internal endpoints publicly
- Log sensitive user data
- Disable authentication checks
- Remove rate limiting
```

### Підтримка та оновлення

Переглядайте межі щоквартально:
- **Підвищення**: дії, які ніколи не викликали проблем (Ask First → Always).
- **Пониження**: дії, які призвели до проблем (Always → Ask First).
- **Блокування**: повторювані помилки (Ask First → Never).

**Джерело**: Addy Osmani, ["How to write a good spec for AI agents"](https://addyosmani.com/blog/good-spec/) (Січень 2026)

---

## Шаблон специфікації команд (Command Spec Template)

**Патерн**: документуйте виконувані команди з очікуваними вихідними результатами та обробкою помилок.

### Чому специфікації команд важливі

Більшість специфікацій зосереджені на **функціях** («створити автентифікацію»), але **команди** («як протестувати автентифікацію») є не менш критичними для ШІ-агентів.

### Структура шаблону

```markdown
## Commands

### [Command Category]

**Purpose**: [What this command accomplishes]

#### Command: `[actual command]`
**When**: [Trigger condition]
**Expected Output**: [What success looks like]
**Error Handling**: [What to do on failure]
**Flags**: [Important options]

---
```

### Приклад: Команди тестування

```markdown
## Commands

### Testing

#### Command: `pnpm test`
**When**: Before every commit, after code changes
**Expected Output**:
- All tests pass (exit code 0)
- Coverage ≥80% (lines, branches, functions)
- No console warnings
**Error Handling**:
- If tests fail → Fix tests, don't skip
- If coverage drops → Add tests for uncovered code
- If warnings appear → Investigate before committing
**Flags**:
- `--coverage`: Generate coverage report
- `--watch`: Run in watch mode for development
- `--silent`: Suppress console output

#### Command: `pnpm test:e2e`
**When**: Before merging to main, in CI pipeline
**Expected Output**:
- All E2E scenarios pass
- Screenshots captured for failures
- Test duration <5 minutes
**Error Handling**:
- If flaky → Investigate race conditions, don't retry blindly
- If timeout → Check network mocks, async handling
- If screenshots differ → Review UI changes deliberately
**Flags**:
- `--headed`: Run with visible browser (debugging)
- `--project chromium`: Test specific browser
```

### Приклад: Збірка та розгортання (Build & Deployment)

```markdown
## Commands

### Build

#### Command: `pnpm build`
**When**: Before deployment, in CI pipeline
**Expected Output**:
- Build succeeds (exit code 0)
- Output in `dist/` directory
- No TypeScript errors
- Bundle size <500KB (main chunk)
**Error Handling**:
- If TypeScript errors → Fix types, don't use `@ts-ignore`
- If bundle too large → Analyze with `pnpm analyze`, code-split
- If missing assets → Check public/ directory, update paths
**Flags**:
- `--mode production`: Production optimizations
- `--analyze`: Generate bundle size report

### Deployment

#### Command: `pnpm deploy:staging`
**When**: After PR approval, before production
**Expected Output**:
- Deployment succeeds
- Health check returns 200 OK
- Staging URL: https://staging.example.com
**Error Handling**:
- If health check fails → Rollback automatically
- If database migration fails → Don't proceed, investigate
- If environment vars missing → Check .env.staging, update secrets
**Never**: Run `pnpm deploy:production` manually — use CI/CD only
```

### Приклад: Команди бази даних

```markdown
## Commands

### Database

#### Command: `pnpm db:migrate`
**When**: After pulling schema changes, before development
**Expected Output**:
- Migrations applied successfully
- Database schema matches models
- Seed data loaded (development only)
**Error Handling**:
- If migration fails → Check database connection, review SQL
- If conflicts detected → Resolve migrations, don't force
**Never**: Run migrations in production manually — CI/CD only

#### Command: `pnpm db:reset`
**When**: Development only, never in staging/production
**Expected Output**:
- Database dropped and recreated
- All migrations applied
- Seed data loaded
**Error Handling**:
- If production check fails → Abort immediately, verify environment
**Safety**: Requires `NODE_ENV=development` check
```

### Інтеграція з CLAUDE.md

Посилання на специфікації команд у вашому основному файлі CLAUDE.md:

```markdown
## Commands
- Build: `pnpm build` (see spec for error handling)
- Test: `pnpm test` (must pass before commit)
- Deploy: See CLAUDE-deployment.md for full procedures
```

**Джерело**: Addy Osmani, ["How to write a good spec for AI agents"](https://addyosmani.com/blog/good-spec/) (Січень 2026)

---

## Антипатерн: Монолітний CLAUDE.md

### Проблема

**Симптом**: ваш файл CLAUDE.md розрісся до 300+ рядків, змішуючи специфікації функцій, контракти API, вимоги до тестування, процедури розгортання та командні конвенції.

**Наслідки**:
- **Неефективність контексту**: Claude завантажує всі 300 рядків для кожного запиту, навіть для найпростіших завдань.
- **Уповільнення відповіді**: великий контекст = повільніша обробка.
- **Зниження точності**: важливі деталі губляться в шумі.
- **Накладні витрати на підтримку**: оновлення одного розділу вимагає навігації по непов'язаному вмісту.
- **Конфлікти в команді**: кілька розробників редагують один і той самий файл = конфлікти злиття (merge conflicts).

### Реальний приклад

**До** (монолітний):
```markdown
# CLAUDE.md (387 lines)

## Tech Stack
[20 lines]

## Authentication
[45 lines of auth spec]

## API Endpoints
[67 lines of API contracts]

## Database Schema
[52 lines of schema rules]

## Testing
[38 lines of test requirements]

## Deployment
[41 lines of deployment procedures]

## Security Rules
[55 lines of security requirements]

## Team Conventions
[33 lines of coding standards]

## Git Workflow
[28 lines of branching rules]

## Troubleshooting
[8 lines of common issues]
```

**Проблема**: Claude завантажує всі 387 рядків, навіть коли користувач просто просить: «Add a new API endpoint for user profile».

**Після** (модульний):
```
CLAUDE.md (82 lines)          # Core context: tech stack, commands, rules
CLAUDE-auth.md (45 lines)     # Authentication spec only
CLAUDE-api.md (67 lines)      # API contracts only
CLAUDE-database.md (52 lines) # Database schema only
CLAUDE-testing.md (38 lines)  # Test requirements only
CLAUDE-deploy.md (41 lines)   # Deployment procedures only
CLAUDE-security.md (55 lines) # Security requirements only
```

**Перевага**: Claude завантажує CLAUDE.md (82 рядки) + CLAUDE-api.md (67 рядків) = 149 рядків (скорочення на 61%).

### Стратегія розділення

**Крок 1: Визначення доменів**

Шукайте логічні межі у вашій специфікації:
- Чи служать ці розділи різним цілям?
- Чи володітимуть різні члени команди різними розділами?
- Чи посилаються на деякі розділи частіше, ніж на інші?

**Крок 2: Витяг у сфокусовані файли**

Перемістіть специфічний для домену вміст в окремі файли:

```bash
# Keep in CLAUDE.md (always loaded)
- Tech stack (unchanging baseline)
- Daily commands (frequent reference)
- Universal rules (apply to all work)

# Extract to domain files (load on demand)
- Feature specs → CLAUDE-[feature].md
- API contracts → CLAUDE-api.md
- Testing → CLAUDE-testing.md
- Deployment → CLAUDE-deploy.md
```

**Крок 3: Створіть покажчик в основному CLAUDE.md**

```markdown
# Project: [NAME]

## Tech Stack
[Core technologies]

## Commands
[Daily commands]

## Rules
[Universal rules]

## Detailed Specifications
Reference these files for domain-specific requirements:
- @CLAUDE-auth.md — Authentication & authorization
- @CLAUDE-api.md — API endpoint contracts
- @CLAUDE-database.md — Schema and migrations
- @CLAUDE-testing.md — Test requirements
- @CLAUDE-deploy.md — Deployment procedures
- @CLAUDE-security.md — Security requirements
```

**Крок 4: Посилайтеся за потреби**

Claude може посилатися на конкретні файли:
```
User: "Add a new API endpoint for user settings"
Claude: Reads CLAUDE.md + @CLAUDE-api.md (relevant context only)
```

### Правила підтримки

1. **Тримайте CLAUDE.md <100 рядків** (тільки основний контекст).
2. **Файли доменів <150 рядків кожен** (якщо вони більші, розділяйте далі).
3. **Щоквартальний перегляд**: об'єднуйте рідко використовувані файли, розділяйте розділи, які часто оновлюються.
4. **Use @file references**: явно завантажуйте лише те, що вам потрібно.

### Контрольний список міграції

- [ ] Визначити домени в поточному CLAUDE.md (>200 рядків?).
- [ ] Створити окремі файли доменів (CLAUDE-[domain].md).
- [ ] Перемістити вміст у сфокусовані файли.
- [ ] Оновити основний CLAUDE.md індексом/посиланнями.
- [ ] Протестувати: попросити Claude виконати завдання з конкретного домену.
- [ ] Перевірити: оцінити використання контексту за допомогою `/status`.
- [ ] Задокументувати: ознайомити команду з новою структурою.

**Джерело**: Addy Osmani, ["How to write a good spec for AI agents"](https://addyosmani.com/blog/good-spec/) (Січень 2026)

---

## Дивіться також

- [../core/methodologies.md](../core/methodologies.md) — SDD та інші методології
- [Spec Kit Documentation](https://github.blog/ai-and-ml/generative-ai/spec-driven-development-with-ai-get-started-with-a-new-open-source-toolkit/)
- [OpenSpec Documentation](https://github.com/Fission-AI/OpenSpec)
- [tdd-with-claude.uk.md](./tdd-with-claude.uk.md) — Поєднання з TDD
- [Spec-to-Code Factory](https://github.com/SylvainChabaud/spec-to-code-factory) — Implémentation référence complète avec enforcement outillé (6 gates via Node.js, invariants "No Spec No Code" + "No Task No Commit", ~900K tokens/projet)
- [Superpowers](https://github.com/obra/superpowers) — Набір плагінів (понад 95 тис. зірок) з навичкою `brainstorming`, яка впроваджує розробку спочатку зі специфікацією (spec-first) як обов'язковий етап: агент відмовляється писати код, поки специфікація не буде перевірена та затверджена. Встановлення: `/plugin install superpowers@claude-plugins-official`.

---
**Локалізація**: [Serhii (MacPlus Software)](https://macplus-software.com)
*Остання синхронізація: Травень 2026*
