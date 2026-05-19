---
title: "Робочий процес планування з двома інстансами (Dual-Instance Planning Workflow)"
description: "Використання двох інстансів Claude з різними ролями для планування та реалізації"
tags: [workflow, architecture, design-patterns]
---

# Робочий процес планування з двома інстансами (Dual-Instance Planning Workflow)

> **Рівень впевненості**: Рівень 2 — на основі досвіду практиків (Jon Williams, лютий 2026 р.). Патерн перевірено шляхом особистого переходу з Cursor на Claude Code протягом 6 місяців.

Використовуйте два інстанси Claude з різними ролями: один для планування та огляду (Claude Zero), інший — для безпосередньої реалізації (Claude One). Розділення відповідальності покращує якість плану та зменшує кількість помилок при впровадженні коду.

---

## Зміст

1. [Коротко (TL;DR)](#tldr)
2. [Коли використовувати цей патерн](#when-to-use-this-pattern)
3. [Налаштування](#setup)
4. [Повний робочий процес](#complete-workflow)
5. [Шаблон плану](#plan-template)
6. [Аналіз витрат](#cost-analysis)
7. [Поради та усунення несправностей](#tips-and-troubleshooting)
8. [Дивіться також](#see-also)

---

## TL;DR

```
1. Launch Claude Zero (planner): explores, writes plans, reviews
2. Launch Claude One (implementer): reads plans, codes, commits
3. Human gatekeeper: approve plans before implementation
4. Plans directory: Review/ → Active/ → Completed/
5. Cost: ~$100-200/month (vs $500-1K for Boris horizontal pattern)
```

**Найкраще для**: соло-розробників, роботи з великою кількістю специфікацій, коли якість > швидкість, при бюджеті <$300/місяць.

---

## Коли використовувати цей патерн

### ✅ Використовуйте, коли

- **Складні специфікації**: Вимоги потребують уточнення за допомогою запитань у стилі інтерв'ю.
- **Критично важливі для якості функції**: Безпека, платежі, міграції даних.
- **Етап навчання**: Нова кодова база, незнайомі патерни.
- **Продуктові дизайнери, що пишуть код**: Нетехнічний бекграунд, потрібна дисципліна у плануванні.
- **Бюджетні обмеження**: $100-200/місяць (проти $500-1K для паралельного використання кількох інстансів).
- **Робочі процеси з великою кількістю специфікацій**: Детальні вимоги, багато граничних випадків.

### ❌ Не використовуйте, коли

- **Прості зміни**: Виправлення оддруківок, тривіальні рефакторинги (використовуйте один інстанс).
- **Дослідницьке кодування**: Проблемна область невідома (витрати на планування не виправдані).
- **Стислі терміни**: Швидкість > якість (будьте готові до циклів виправлень).
- **Великий обсяг паралельних функцій**: Замість цього використовуйте патерн Бориса (Розділ 9.17).
- **Дуже обмежений бюджет**: <$100/місяць (використовуйте Sonnet, один інстанс).

### Порівняння з іншими патернами

| Патерн | Вісь масштабування | Вартість/місяць | Найкраще для |
|---------|--------------|------------|----------|
| **Один інстанс** | Відсутня | $50-100 | Більшість розробників, загальне використання |
| **Dual-instance (Джон)** | Вертикальне (планування ↔ реалізація) | $100-200 | Складні специфікації, фокус на якості |
| **Multi-instance (Борис)** | Горизонтальне (5-15 паралельно) | $500-1,000 | Команди, великі обсяги поставок |

---

## Налаштування

### Крок 1: Створіть структуру директорій

```bash
cd ~/projects/your-project
mkdir -p .claude/plans/{Review,Active,Completed}
```

**Ролі директорій**:
- `Review/` — плани, що очікують на затвердження людиною.
- `Active/` — затверджені плани на етапі реалізації.
- `Completed/` — архівні плани (ресурс для навчання).

**Додайте до .gitignore**:
```bash
# .gitignore
.claude/plans/Review/
.claude/plans/Active/
# Optional: commit Completed/ for team learning
```

### Крок 2: Запустіть Claude Zero (Planner)

**Термінал 1**:
```bash
cd ~/projects/your-project
claude
```

**Перше повідомлення** (закріплення ролі):
```
You are Claude Zero (Planner).

Your role:
- Explore codebase using Plan Mode (Shift+Tab twice)
- Interview user about requirements
- Write detailed plans to .claude/plans/Review/
- Review implementations after Claude One completes them
- NEVER edit code directly
- NEVER commit changes

Start by acknowledging this role.
```

Claude Zero підтверджує: "Understood. I am Claude Zero (Planner). I will explore, plan, and review, but never touch code."

### Крок 3: Запустіть Claude One (Implementer)

**Термінал 2** (нова сесія):
```bash
cd ~/projects/your-project
claude
```

**Перше повідомлення** (закріплення ролі):
```
You are Claude One (Implementer).

Your role:
- Read approved plans from .claude/plans/Active/
- Implement exactly as specified
- Commit changes after each logical step
- Report completion back to user
- NEVER create plans
- NEVER skip approval steps

Start by acknowledging this role.
```

Claude One підтверджує: "Understood. I am Claude One (Implementer). I execute approved plans only."

---

## Повний робочий процес

### Фаза 1: Планування (Claude Zero)

#### Крок 1.1: Запуск планування

**Ви** (до Claude Zero):
```
# Enter Plan Mode (Shift+Tab twice), then:

Implement JWT authentication for the API:
- Access tokens (15min expiry)
- Refresh tokens (7 day expiry)
- Middleware to protect routes
- Logout capability (revoke refresh tokens)
```

#### Крок 1.2: Claude Zero досліджує кодову базу

Claude Zero (у Plan Mode):
- Читає існуючий код автентифікації.
- Шукає патерни автентифікації у кодовій базі.
- Визначає залежності (бібліотеки, змінні оточення).

#### Крок 1.3: Claude Zero проводить інтерв'ю з вами

Claude Zero ставить уточнюючі запитання:
```
Before I draft the plan, I need to clarify:

1. Should we support multiple concurrent sessions per user?
   (e.g., user logged in on phone + laptop simultaneously)

2. Where should refresh tokens be stored?
   - Database table
   - Redis
   - Other

3. Which routes should be protected?
   - All /api/* routes?
   - Specific routes only?

4. Do you want rate limiting on login attempts?

5. Success criteria for "done"?
   - Tests passing?
   - Postman collection?
   - Documentation updated?
```

**Ви відповідаєте**, Claude Zero покращує розуміння завдання.

#### Крок 1.4: Claude Zero пише план

Claude Zero створює `.claude/plans/Review/auth-jwt.md`:

```markdown
# Plan: JWT Authentication

**Created**: 2026-02-04
**Author**: Claude Zero
**Estimated effort**: 3-4 hours
**Risk level**: Medium (security-critical)

## Summary
Implement JWT-based authentication with access/refresh token pattern.
Support multiple concurrent sessions per user.
Refresh tokens stored in database with revocation capability.

## Requirements Clarified
- Multiple sessions per user: YES
- Refresh token storage: Database (new table)
- Protected routes: All /api/* except /api/auth/*
- Rate limiting: YES (5 attempts per 15min)
- Success criteria: Tests pass + Postman collection

## Files to Create

### 1. src/auth/jwt.ts (~120 lines)
**Purpose**: JWT utility functions

**Exports**:
- `generateAccessToken(userId: string): string`
  - Payload: { userId, type: 'access' }
  - Expiry: 15 minutes
  - Sign with JWT_SECRET

- `generateRefreshToken(userId: string): string`
  - Payload: { userId, type: 'refresh', jti: uuid() }
  - Expiry: 7 days
  - Sign with JWT_REFRESH_SECRET
  - jti = unique token ID for revocation

- `verifyAccessToken(token: string): { userId: string } | null`
  - Verify signature
  - Check expiry
  - Return payload or null

- `verifyRefreshToken(token: string): { userId: string, jti: string } | null`
  - Verify signature
  - Check expiry
  - Check not revoked (database lookup)
  - Return payload or null

**Dependencies**: jsonwebtoken, uuid

### 2. src/middleware/auth.ts (~60 lines)
**Purpose**: Authentication middleware

**Exports**:
- `requireAuth(req, res, next)`
  - Extract token from Authorization header (Bearer format)
  - Verify using verifyAccessToken()
  - Attach userId to req.userId
  - 401 if invalid/missing

**Dependencies**: jwt.ts

### 3. src/db/migrations/YYYYMMDD_create_refresh_tokens.ts (~40 lines)
**Purpose**: Database table for refresh tokens

**Schema**:
```sql
CREATE TABLE refresh_tokens (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  jti UUID NOT NULL UNIQUE,
  created_at TIMESTAMP DEFAULT NOW(),
  expires_at TIMESTAMP NOT NULL,
  revoked_at TIMESTAMP
);
CREATE INDEX idx_refresh_tokens_user_id ON refresh_tokens(user_id);
CREATE INDEX idx_refresh_tokens_jti ON refresh_tokens(jti);
```

## Files to Modify

### 1. src/routes/api.ts
**Location**: Line 23 (after imports)
**Change**: Add requireAuth middleware to all routes except /auth/*

**Before**:
```typescript
router.get('/profile', profileController);
router.post('/posts', createPostController);
```

**After**:
```typescript
import { requireAuth } from '../middleware/auth';
router.get('/profile', requireAuth, profileController);
router.post('/posts', requireAuth, createPostController);
```

### 2. src/routes/auth.ts
**Location**: Create new file OR add to existing auth routes
**Changes**:
- POST /auth/login → return { accessToken, refreshToken }
- POST /auth/refresh → exchange refresh token for new access token
- POST /auth/logout → revoke refresh token

### 3. src/config/env.ts
**Location**: Line 15 (after existing secrets)
**Add**:
```typescript
JWT_SECRET: process.env.JWT_SECRET || '',
JWT_REFRESH_SECRET: process.env.JWT_REFRESH_SECRET || '',
```

### 4. .env.example
**Add**:
```
JWT_SECRET=your-secret-here-min-32-chars
JWT_REFRESH_SECRET=your-refresh-secret-here-min-32-chars
```

## Implementation Steps (Sequential)

1. **Install dependencies**
   ```bash
   npm install jsonwebtoken uuid
   npm install --save-dev @types/jsonwebtoken @types/uuid
   ```

2. **Create JWT utilities** (jwt.ts)
   - Implement all 4 functions
   - Add error handling (try/catch on verify)

3. **Run database migration** (refresh_tokens table)
   - Test migration up/down

4. **Create auth middleware** (auth.ts)
   - Implement requireAuth
   - Test with mock token

5. **Create/update auth routes** (auth.ts routes)
   - POST /auth/login
   - POST /auth/refresh
   - POST /auth/logout

6. **Protect existing routes** (api.ts)
   - Apply requireAuth to all /api/* routes

7. **Add JWT secrets to .env**
   - Generate secure random strings (64 chars)

8. **Write tests**
   - Unit tests for jwt.ts functions
   - Integration tests for auth flow
   - Test token expiry
   - Test revocation

9. **Create Postman collection**
   - Login → get tokens
   - Access protected route with access token
   - Refresh access token
   - Logout → revoke refresh token
   - Verify revoked token rejected

## Success Criteria

- [ ] POST /auth/login returns accessToken + refreshToken
- [ ] Protected routes return 401 without valid access token
- [ ] Protected routes return 200 with valid access token
- [ ] POST /auth/refresh exchanges refresh token for new access token
- [ ] POST /auth/logout revokes refresh token
- [ ] Revoked refresh tokens are rejected on /auth/refresh
- [ ] Expired access tokens are rejected
- [ ] Multiple sessions per user work (different refresh tokens)
- [ ] All tests pass (npm test)
- [ ] Postman collection works end-to-end

## Security Checklist

- [ ] JWT secrets are in .env (never committed)
- [ ] JWT secrets are ≥32 characters
- [ ] Refresh tokens stored in database (not just JWT)
- [ ] Refresh tokens have unique jti for revocation
- [ ] Access tokens have short expiry (15min)
- [ ] Authorization header validated (Bearer format)
- [ ] Token verification errors are caught (no crashes)

## Risks & Mitigation

| Risk | Impact | Mitigation |
|------|--------|------------|
| JWT secrets leaked | High | .env in .gitignore, never log secrets |
| Token expiry too long | Medium | 15min access, 7 day refresh (short enough) |
| No rate limiting on login | Medium | Add rate limiting (5 attempts/15min) |
| Refresh token table grows indefinitely | Low | Add cleanup job (delete expired tokens) |

## Questions for Implementer (Claude One)

If you encounter these scenarios during implementation:
1. **Existing user login flow**: Integrate with existing login logic, don't replace entire auth system
2. **Database ORM**: Use existing ORM (Prisma/TypeORM/Knex) for refresh_tokens table
3. **Error messages**: Return generic "Invalid token" (don't leak whether token is expired vs invalid signature)

## Estimated Effort Breakdown

- JWT utilities: 45 min
- Database migration: 15 min
- Middleware: 30 min
- Auth routes: 60 min
- Protect existing routes: 15 min
- Tests: 90 min
- Postman collection: 15 min

**Total**: ~4 hours

---

**Plan approved?** → Move to `.claude/plans/Active/auth-jwt.md`
```

### Фаза 2: Людський огляд

**Ви переглядаєте** `.claude/plans/Review/auth-jwt.md`:

**Контрольний список (Checklist)**:
- [ ] Чи враховано всі вимоги?
- [ ] Чи має сенс цей підхід для цієї кодової бази?
- [ ] Чи враховано заходи безпеки?
- [ ] Чи є оцінка трудовитрат реалістичною?
- [ ] Чи є критерії успіху чіткими та протестованими?
- [ ] Чи правильні шляхи до файлів, які потрібно створити/змінити?

**Якщо затверджено**:
```bash
mv .claude/plans/Review/auth-jwt.md .claude/plans/Active/
```

**Якщо потрібні зміни**, попросіть Claude Zero доопрацювати план:
```
Update the plan:
- Change refresh token expiry to 30 days instead of 7
- Add password reset flow to scope
```

### Фаза 3: Реалізація (Claude One)

**Ви** (до Claude One):
```
Implement .claude/plans/Active/auth-jwt.md

Follow the plan exactly. Commit after each logical step.
Report back when complete.
```

Claude One:
1. Читає файл плану.
2. Встановлює залежності.
3. Створює `jwt.ts`.
4. Створює міграцію бази даних.
5. Запускає міграцію.
6. Створює проміжне програмне забезпечення (middleware) для автентифікації.
7. Оновлює маршрути.
8. Додає змінні оточення.
9. Пише тести.
10. Створює колекцію Postman.

**Claude One робить комміти** після кожного кроку:
```
feat: add JWT utility functions
feat: create refresh_tokens table migration
feat: add auth middleware
feat: protect API routes with JWT auth
test: add JWT auth flow tests
```

### Фаза 4: Верифікація (Claude Zero)

**Ви** (до Claude Zero):
```
Review the JWT implementation Claude One just completed.
Check against the plan in .claude/plans/Active/auth-jwt.md.
```

Claude Zero перевіряє:
- Чи відповідає структура коду плану?
- Чи виконано всі критерії успіху?
- Чи виконано контрольний список безпеки?
- Чи проходяться тести?
- Чи є «запахи коду» (code smells) або інші проблеми?

**Звіт Claude Zero**:
```
✅ Review complete: auth-jwt.md

Code Quality: 9/10
- All files created as planned
- Success criteria met (9/9)
- Security checklist complete
- Tests pass (15/15)

Minor suggestions:
1. Consider adding refresh token rotation (security best practice)
2. Add JSDoc comments to jwt.ts functions
3. Consider extracting magic numbers (15min, 7 days) to config

Critical issues: None

Ready to archive plan to Completed/.
```

### Фаза 5: Архівування

**Якщо затверджено**:
```bash
mv .claude/plans/Active/auth-jwt.md .claude/plans/Completed/
```

Тепер план архівовано для подальшого використання та навчання команди.

---

## Шаблон плану

Збережіть цей шаблон у `.claude/plan-template.md` для однакової структури планів:

```markdown
# Plan: [Feature Name]

**Created**: [Date]
**Author**: Claude Zero
**Estimated effort**: [Hours]
**Risk level**: Low | Medium | High

## Summary
[2-3 sentence overview of what this plan accomplishes]

## Requirements Clarified
[List of requirements confirmed through interview]
- Requirement 1: [Answer]
- Requirement 2: [Answer]

## Files to Create

### 1. [File path] (~[Lines] lines)
**Purpose**: [What this file does]

**Exports**:
- `functionName(params): returnType`
  - [What it does]
  - [Key implementation details]

**Dependencies**: [Libraries, other files]

## Files to Modify

### 1. [File path]
**Location**: Line [N] ([Context: after what, before what])
**Change**: [What to change]

**Before**:
```[language]
[Existing code snippet]
```

**After**:
```[language]
[Modified code snippet]
```

## Implementation Steps (Sequential)

1. **[Step name]**
   - [Substep]
   - [Substep]

2. **[Step name]**
   - [Substep]

## Success Criteria

- [ ] [Testable criterion 1]
- [ ] [Testable criterion 2]

## Security Checklist (if applicable)

- [ ] [Security item 1]
- [ ] [Security item 2]

## Risks & Mitigation

| Risk | Impact | Mitigation |
|------|--------|------------|
| [Risk] | [High/Med/Low] | [How to prevent/handle] |

## Questions for Implementer (Claude One)

If you encounter these scenarios during implementation:
1. [Scenario]: [Guidance]

## Estimated Effort Breakdown

- [Task 1]: [Time]
- [Task 2]: [Time]

**Total**: [Hours]

---

**Plan approved?** → Move to `.claude/plans/Active/[filename].md`
```

---

## Аналіз витрат

### Порівняння Dual-Instance та Single Instance з виправленнями

| Сценарій | Single Instance | Dual Instance | Економія |
|----------|----------------|---------------|---------|
| **Проста функція** (форма входу) | 1 сесія × $5 = **$5** | 2 сесії × $3 = $6 | +$1 (один інстанс виграє) |
| **Середня функція** (система автентифікації) | 1 сесія × $15 + 2 виправлення × $10 = **$35** | 2 сесії × $12 = $24 | **Заощаджено $11** |
| **Складна функція** (неоднозначна спец.) | 1 сесія × $20 + 3 виправлення × $15 = **$65** | 2 сесії × $18 = $36 | **Заощаджено $29** |

**Точка беззбитковості**: для функцій, що вимагають ≥2 циклів виправлення помилок, підхід з двома інстансами (dual-instance) є більш вигідним.

### Оцінка щомісячного бюджету

**Припущення**:
- 20 робочих днів на місяць
- 2 функції на день (суміш простих + складних)
- Ціноутворення Opus 4.5 (~$15/1M input, $75/1M output)

| Профіль | Функцій/місяць | Single Instance | Dual Instance | Економія |
|---------|----------------|----------------|---------------|---------|
| **Слабке використання** | 20 простих | $100 | $120 | -$20 (один інстанс виграє) |
| **Помірне використання** | 30 змішаних (60% середніх, 40% простих) | $650 | $480 | **Заощаджено $170** |
| **Інтенсивне використання** | 40 складних | $2,000 | $1,200 | **Заощаджено $800** |

**Рекомендація**:
- Тільки прості функції → Один інстанс
- Середні/складні функції → Двоінстансний підхід заощаджує гроші та час

---

## Поради та усунення несправностей

### Закріплення ролей

**Проблема**: Claude Zero починає редагувати код.

**Рішення**: Нагадуйте про це в кожному запиті:
```
Remember: you are Claude Zero (Planner only).
Do not edit code. Write plan to .claude/plans/Review/
```

**Запобігання**: Використовуйте `CLAUDE.md` для закріплення ролей:

```markdown
# .claude/CLAUDE.md

## If you are Claude Zero (Planner):
- Use Plan Mode (Shift+Tab twice) for all exploration
- Save all plans to .claude/plans/Review/[feature].md
- NEVER edit code
- NEVER commit changes
- Review implementations after Claude One completes them

## If you are Claude One (Implementer):
- Read plans from .claude/plans/Active/
- Implement exactly as specified
- Commit after each logical step
- NEVER create plans
```

### Забруднення контексту

**Проблема**: Контекст Claude One засмічується обговоренням планування.

**Рішення**: Використовуйте окремі термінальні сесії (окремі контексти):
- Термінал 1 = Claude Zero (контекст планування)
- Термінал 2 = Claude One (контекст реалізації)

**Ніколи не діліть контекст** між Claude Zero та Claude One.

### Відхилення від плану

**Проблема**: Claude One відхиляється від плану під час реалізації.

**Рішення**: Додайте це до плану:
```markdown
## Implementation Rules for Claude One

- Follow plan steps sequentially (don't skip or reorder)
- If you encounter blockers, STOP and report (don't improvise)
- Commit after each step (granular history)
- If unclear, ask user (don't guess)
```

### Керування накладними витратами

**Проблема**: Переміщення файлів між директоріями є ручною рутиною.

**Рішення**: Створіть bash аліаси (aliases):

```bash
# Add to ~/.bashrc or ~/.zshrc

# Move plan to Active (approve)
approve-plan() {
    mv ".claude/plans/Review/$1.md" ".claude/plans/Active/"
    echo "✅ Approved: $1.md → Active/"
}

# Move plan to Completed (archive)
complete-plan() {
    mv ".claude/plans/Active/$1.md" ".claude/plans/Completed/"
    echo "✅ Completed: $1.md → Archived"
}

# List plans by status
plans() {
    echo "📋 Review:"
    ls -1 .claude/plans/Review/ 2>/dev/null || echo "  (empty)"
    echo ""
    echo "🔄 Active:"
    ls -1 .claude/plans/Active/ 2>/dev/null || echo "  (empty)"
    echo ""
    echo "✅ Completed:"
    ls -1 .claude/plans/Completed/ 2>/dev/null | tail -5 || echo "  (empty)"
}
```

**Використання**:
```bash
plans                     # Показати всі плани
approve-plan auth-jwt     # Затвердити план
complete-plan auth-jwt    # Архівувати виконаний план
```

---

## Дивіться також

- [Основний посібник](#figma-mcp-integration) — Огляд та порівняння.
- [Plan Mode](plan-driven.md) — Основа для робочих процесів планування.
- [Multi-Instance (Борис)](#917-scaling-patterns-multi-instance-workflows) — Альтернатива з горизонтальним масштабуванням.
- [Оптимізація витрат](#cost-optimization-tips) — Управління бюджетом.

**Зовнішні ресурси**:
- [Допис Jon Williams на LinkedIn](https://www.linkedin.com/posts/thatjonwilliams_ive-been-using-cursor-for-six-months-now-activity-7424481861802033153-k8bu) — оригінальний опис патерну (3 лютого 2026 р.).
- [10 порад від команди Claude Code](https://paddo.dev/blog/claude-code-team-tips/) — робочі процеси команд, включаючи підхід зі створенням плану насамперед.

---
**Локалізація**: [Serhii (MacPlus Software)](https://macplus-software.com)
*Остання синхронізація: Травень 2026*
