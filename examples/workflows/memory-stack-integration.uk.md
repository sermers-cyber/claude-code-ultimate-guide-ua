---
title: "Інтеграція стека пам'яті: реальний багатоденний воркфлоу"
description: "Приклад 5-денного спринту, що поєднує claude-mem, Serena, grepai та rg для рефакторингу автентифікації"
tags: [workflow, memory, integration]
---

# Інтеграція стека пам'яті: реальний багатоденний воркфлоу

**Сценарій**: рефакторинг системи автентифікації із сесійної на JWT протягом 5-денного спринту

**Використані інструменти**: claude-mem (автозахоплення) + Serena (ручні рішення) + grepai (виявлення) + rg (точний пошук)

**Проєкт**: API для e-commerce (Node.js/TypeScript, 50 тис. рядків, 200+ файлів)

---

## День 1: виявлення та планування

### Ранок: початкове дослідження

**Користувач**: "Let's explore the current authentication system"

**Claude** (ще без claude-mem):
```bash
# Manual discovery
rg "authenticate|session" --type ts | head -20
# 47 matches across 12 files
```

**Проблема**: забагато файлів, немає контексту щодо архітектурних рішень.

---

### Після встановлення claude-mem

```bash
# Install claude-mem
/plugin marketplace add thedotmack/claude-mem
/plugin install claude-mem
# Restart Claude Code
```

**Користувач**: "Explore authentication architecture"

**Claude** (тепер з автозахопленням):
```bash
# 1. SEMANTIC DISCOVERY (grepai)
grepai search "authentication and session management"
# → Finds:
#   - src/auth/auth.service.ts (main service)
#   - src/middleware/session.middleware.ts (session handling)
#   - src/controllers/user.controller.ts (endpoints)
#   - config/session.config.ts (session config)

# 2. STRUCTURAL OVERVIEW (Serena)
serena get_symbols_overview --file src/auth/auth.service.ts
# → AuthService class:
#   - login(email, password)
#   - logout(sessionId)
#   - validateSession(sessionId)
#   - createSession(userId)

# 3. CALL GRAPH (grepai)
grepai trace callers "createSession"
# → Called by:
#   - UserController.login() (47 times)
#   - AdminController.authenticate() (12 times)
#   - OAuthController.callback() (8 times)

# 4. EXACT SEARCH (rg)
rg "express-session" --type ts
# → Found in:
#   - package.json (dependency)
#   - session.middleware.ts (import)
#   - app.ts (config)
```

**claude-mem** автоматично захоплює:
- 4 прочитані файли (auth.service.ts, session.middleware.ts, user.controller.ts, session.config.ts)
- 67 викликів інструментів (читання, пошуки, трасування)
- Ключова знахідка: "Current system uses express-session, stored in Redis"

---

### Обід: архітектурне рішення

**Користувач**: "Should we use JWT or stick with sessions?"

**Обговорення**:
- JWT: без стану, масштабовано, без залежності від Redis
- Сесії: контроль на боці сервера, легке відкликання
- **Рішення**: JWT для API, сесії лишити для веб-дашборда

**Запис рішення (Serena)**:
```bash
serena write_memory "auth_architecture" "$(cat <<'EOF'
Decision: Migrate API to JWT, keep sessions for web dashboard.

Rationale:
- API clients (mobile, SPA) benefit from stateless JWT
- Web dashboard needs session revocation (admin logout)
- Hybrid approach: /api/* uses JWT, /admin/* uses sessions

Library choice: jose (vs jsonwebtoken)
- Lighter (40% fewer dependencies)
- Better TypeScript support
- Active maintenance (last update: 2 weeks ago)

Next steps:
1. Install jose
2. Create JwtService
3. Update UserController to use JWT for /api/* routes
4. Keep SessionMiddleware for /admin/* routes
EOF
)"
```

**claude-mem** автоматично захоплює:
- Обговорення рішення (стиснений підсумок)
- Виклик Serena write_memory
- Обґрунтування JWT + бібліотеки jose

---

### Кінець першого дня

**Claude** автоматично генерує підсумок сесії:
```
Session Summary (Day 1):
- Explored authentication system (4 key files identified)
- Current: express-session + Redis
- Decision: Migrate to JWT for API, keep sessions for admin
- Library: jose (lighter, better TS support)
- Next: Install jose, create JwtService
```

**Дашборд claude-mem** (`http://localhost:37777`):
- Хронологія: 67 спостережень
- Ключові файли: auth.service.ts, session.middleware.ts
- Записано рішення: auth_architecture

---

## День 2: початок реалізації

### Ранок: відновлення сесії

**Claude** (автоматично вставлений контекст):
```
📋 Previous Session (Day 1):
- Explored auth system (4 files: auth.service.ts, session.middleware.ts, user.controller.ts, session.config.ts)
- Decision: JWT for API, sessions for admin
- Library: jose (40% lighter than jsonwebtoken)
- Next steps: Install jose, create JwtService
```

**Користувач**: "Let's implement JWT service"

**Claude** (вже має контекст, без повторного читання):
```bash
# Install jose
npm install jose

# Create JWT service
```

**Реалізація**:
```typescript
// src/auth/jwt.service.ts
import * as jose from 'jose';

export class JwtService {
  private secret: Uint8Array;

  constructor(secretKey: string) {
    this.secret = new TextEncoder().encode(secretKey);
  }

  async generateToken(userId: string, email: string): Promise<string> {
    const jwt = await new jose.SignJWT({ userId, email })
      .setProtectedHeader({ alg: 'HS256' })
      .setIssuedAt()
      .setExpirationTime('24h')
      .sign(this.secret);

    return jwt;
  }

  async verifyToken(token: string): Promise<{ userId: string; email: string }> {
    const { payload } = await jose.jwtVerify(token, this.secret);
    return payload as { userId: string; email: string };
  }
}
```

**claude-mem** автоматично захоплює:
- npm install jose
- Реалізацію JwtService
- Сигнатури методів (generateToken, verifyToken)

---

### Обід: контрольна точка рішення

**Користувач**: "Should we add refresh tokens now or later?"

**Обговорення**:
- Refresh tokens = краща безпека (короткі access-токени)
- АЛЕ: більше складності, потрібне сховище в базі даних
- **Рішення**: додати у Фазі 2 (після того, як базовий JWT запрацює)

**Запис рішення (Serena)**:
```bash
serena write_memory "jwt_refresh_tokens" "$(cat <<'EOF'
Decision: Defer refresh tokens to Phase 2

Rationale:
- Phase 1: Basic JWT (access tokens only, 24h expiry)
- Phase 2: Add refresh tokens (1 week expiry, stored in DB)

Why defer:
- Validate JWT flow works first
- Avoid premature complexity
- Need to design refresh token storage schema

Reminder for Phase 2:
- Refresh tokens in separate table (id, userId, token, expiresAt)
- Rotation on refresh (invalidate old, issue new)
- Endpoint: POST /api/auth/refresh
EOF
)"
```

**claude-mem** автоматично захоплює:
- Обговорення refresh-токенів
- Рішення відкласти
- Нагадування для Фази 2

---

### Кінець другого дня

**Claude** автоматично генерує підсумок сесії:
```
Session Summary (Day 2):
- Installed jose library
- Implemented JwtService (generateToken, verifyToken)
- Decision: Defer refresh tokens to Phase 2
- Next: Update UserController to use JwtService
```

**Стан стека пам'яті**:

| Шар | Вміст | Інструмент |
|-----|-------|------------|
| **Захоплення сесій** | Спостереження днів 1-2 (усього 134) | claude-mem |
| **Ручні рішення** | 2 спогади (auth_architecture, jwt_refresh_tokens) | Serena |
| **Виявлення коду** | 4 файли проіндексовано, граф викликів побудовано | grepai |

---

## День 3: інтеграція

### Ранок: відновлення сесії

**Claude** (автоматично вставлений контекст):
```
📋 Previous Sessions (Day 1-2):
- Day 1: Explored auth, decided JWT for API
- Day 2: Implemented JwtService, deferred refresh tokens to Phase 2
- Files modified: jwt.service.ts
- Next: Update UserController to use JwtService
```

**Користувач**: "Update login endpoint to return JWT"

**Claude** (вже знає контекст):
```bash
# 1. FIND DEPENDENCIES (grepai)
grepai trace callers "login"
# → UserController.login() called by 47 routes

# 2. READ CURRENT IMPLEMENTATION (rg + Read)
rg "async login" src/controllers/user.controller.ts -A 10
```

**Поточна реалізація**:
```typescript
// src/controllers/user.controller.ts (before)
async login(req: Request, res: Response) {
  const { email, password } = req.body;
  const user = await this.authService.authenticate(email, password);

  if (!user) {
    return res.status(401).json({ error: 'Invalid credentials' });
  }

  // OLD: Create session
  const sessionId = await this.authService.createSession(user.id);
  req.session.userId = user.id;

  return res.json({ success: true, sessionId });
}
```

**Оновлення до JWT**:
```typescript
// src/controllers/user.controller.ts (after)
import { JwtService } from '../auth/jwt.service';

async login(req: Request, res: Response) {
  const { email, password } = req.body;
  const user = await this.authService.authenticate(email, password);

  if (!user) {
    return res.status(401).json({ error: 'Invalid credentials' });
  }

  // NEW: Generate JWT
  const token = await this.jwtService.generateToken(user.id, user.email);

  return res.json({ success: true, token });
}
```

**claude-mem** автоматично захоплює:
- Зміну UserController
- Видалено: виклик createSession, сховище сесій
- Додано: генерацію JWT

---

### Обід: оновлення middleware

**Користувач**: "Create JWT authentication middleware"

**Реалізація**:
```typescript
// src/middleware/jwt.middleware.ts
import { Request, Response, NextFunction } from 'express';
import { JwtService } from '../auth/jwt.service';

export function jwtAuthMiddleware(jwtService: JwtService) {
  return async (req: Request, res: Response, next: NextFunction) => {
    const authHeader = req.headers.authorization;

    if (!authHeader || !authHeader.startsWith('Bearer ')) {
      return res.status(401).json({ error: 'Missing or invalid token' });
    }

    const token = authHeader.slice(7); // Remove "Bearer "

    try {
      const payload = await jwtService.verifyToken(token);
      req.user = payload; // Attach user to request
      next();
    } catch (error) {
      return res.status(401).json({ error: 'Invalid or expired token' });
    }
  };
}
```

**Застосування до API-маршрутів**:
```typescript
// src/app.ts
import { jwtAuthMiddleware } from './middleware/jwt.middleware';

// Apply JWT middleware to /api/* routes
app.use('/api/*', jwtAuthMiddleware(jwtService));

// Keep session middleware for /admin/* routes
app.use('/admin/*', sessionMiddleware);
```

**claude-mem** автоматично захоплює:
- Новий middleware: jwt.middleware.ts
- Розділення маршрутів: /api/* (JWT) проти /admin/* (сесії)
- Збережено зворотну сумісність

---

### Кінець третього дня

**Користувач**: "Record the migration status"

**Оновлення пам'яті Serena**:
```bash
serena write_memory "jwt_migration_status" "$(cat <<'EOF'
JWT Migration Status (Day 3):

✅ Completed:
- JwtService implemented (jose library)
- UserController.login() updated to return JWT
- jwtAuthMiddleware created and applied to /api/* routes
- Admin routes still use sessions (/admin/*)

📝 Files Modified:
- src/auth/jwt.service.ts (new)
- src/middleware/jwt.middleware.ts (new)
- src/controllers/user.controller.ts (updated)
- src/app.ts (route split)

🧪 Next Steps (Day 4):
1. Write tests for JwtService
2. Test login flow end-to-end
3. Update API clients to use JWT (frontend, mobile)
4. Monitor logs for any session-related errors

⚠️ Rollback Plan:
- Keep session code intact (not deleted)
- Can revert by changing app.ts route config
- Database unchanged (no schema migration needed)
EOF
)"
```

**Дашборд claude-mem** показує:
- 3 дні історії
- 217 спостережень загалом
- 3 спогади Serena (arch, refresh_tokens, migration_status)
- 8 змінених файлів

---

## День 4: тестування та валідація

### Ранок: відновлення сесії

**Claude** (автоматично вставлений контекст):
```
📋 Previous Sessions (Day 1-3):
- Day 1: Explored auth, decided JWT
- Day 2: Implemented JwtService
- Day 3: Updated login endpoint, created JWT middleware
- Status: /api/* uses JWT, /admin/* uses sessions
- Next: Write tests, validate end-to-end
```

**Користувач**: "Write tests for JwtService"

**Claude** (знає реалізацію з дня 2):
```typescript
// src/auth/__tests__/jwt.service.test.ts
import { JwtService } from '../jwt.service';

describe('JwtService', () => {
  let jwtService: JwtService;

  beforeEach(() => {
    jwtService = new JwtService('test-secret-key-32-chars-long!!');
  });

  describe('generateToken', () => {
    it('should generate valid JWT token', async () => {
      const token = await jwtService.generateToken('user-123', 'test@example.com');

      expect(token).toBeDefined();
      expect(typeof token).toBe('string');
      expect(token.split('.')).toHaveLength(3); // JWT format: header.payload.signature
    });

    it('should include userId and email in payload', async () => {
      const token = await jwtService.generateToken('user-456', 'user@example.com');
      const payload = await jwtService.verifyToken(token);

      expect(payload.userId).toBe('user-456');
      expect(payload.email).toBe('user@example.com');
    });

    it('should set 24h expiration', async () => {
      const token = await jwtService.generateToken('user-789', 'exp@example.com');
      const payload = await jwtService.verifyToken(token);

      // JWT exp is in seconds, not milliseconds
      const now = Math.floor(Date.now() / 1000);
      const expectedExp = now + (24 * 60 * 60); // 24 hours

      expect(payload.exp).toBeGreaterThan(now);
      expect(payload.exp).toBeLessThanOrEqual(expectedExp + 10); // 10s tolerance
    });
  });

  describe('verifyToken', () => {
    it('should verify valid token', async () => {
      const token = await jwtService.generateToken('user-abc', 'valid@example.com');
      const payload = await jwtService.verifyToken(token);

      expect(payload).toEqual({
        userId: 'user-abc',
        email: 'valid@example.com',
        iat: expect.any(Number),
        exp: expect.any(Number)
      });
    });

    it('should throw on invalid token', async () => {
      await expect(jwtService.verifyToken('invalid.token.here'))
        .rejects.toThrow();
    });

    it('should throw on expired token', async () => {
      // Create token with -1h expiration (already expired)
      const jwtService2 = new JwtService('test-secret');
      const expiredToken = await jwtService2.generateToken('user-old', 'old@example.com');

      // Wait 2 seconds (simulate expiration)
      await new Promise(resolve => setTimeout(resolve, 2000));

      await expect(jwtService2.verifyToken(expiredToken))
        .rejects.toThrow('expired');
    });

    it('should throw on token with wrong secret', async () => {
      const token = await jwtService.generateToken('user-123', 'test@example.com');

      // Try to verify with different secret
      const jwtService2 = new JwtService('different-secret-key-here!!!!');
      await expect(jwtService2.verifyToken(token))
        .rejects.toThrow();
    });
  });
});
```

**Запуск тестів**:
```bash
npm test jwt.service.test.ts

# Output:
# JwtService
#   generateToken
#     ✓ should generate valid JWT token (45ms)
#     ✓ should include userId and email in payload (32ms)
#     ✓ should set 24h expiration (28ms)
#   verifyToken
#     ✓ should verify valid token (21ms)
#     ✓ should throw on invalid token (15ms)
#     ✓ should throw on expired token (2018ms)
#     ✓ should throw on token with wrong secret (19ms)
#
# Tests: 7 passed, 7 total
```

**claude-mem** автоматично захоплює:
- Створений тестовий файл (jwt.service.test.ts)
- 7 тестових випадків (усі проходять)
- Перевірені крайні випадки (недійсний, прострочений, хибний секрет)

---

### Обід: наскрізний тест

**Користувач**: "Test the full login flow"

**Ручний E2E-тест**:
```bash
# 1. Login (get JWT)
curl -X POST http://localhost:3000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"password123"}'

# Response:
# {
#   "success": true,
#   "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySWQiOiJ1c2VyLTEyMyIsImVtYWlsIjoidGVzdEBleGFtcGxlLmNvbSIsImlhdCI6MTcwNzU4MjAwMCwiZXhwIjoxNzA3NjY4NDAwfQ.xYz..."
# }

# 2. Access protected API endpoint
curl -X GET http://localhost:3000/api/profile \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."

# Response:
# {
#   "userId": "user-123",
#   "email": "test@example.com",
#   "profile": { ... }
# }

# 3. Test without token (should fail)
curl -X GET http://localhost:3000/api/profile

# Response:
# { "error": "Missing or invalid token" }

# 4. Test admin route (should still use sessions)
curl -X GET http://localhost:3000/admin/dashboard \
  -H "Cookie: connect.sid=s%3A..."

# Response:
# { "dashboard": "admin data" }
```

**✅ Усі тести проходять!**

**Запис валідації (Serena)**:
```bash
serena write_memory "jwt_validation_results" "$(cat <<'EOF'
JWT Validation Results (Day 4):

✅ Unit Tests: 7/7 passed
- Token generation works
- Token verification works
- Expiration handling correct
- Error cases handled (invalid, expired, wrong secret)

✅ E2E Tests: 4/4 passed
- Login returns JWT
- Protected routes accept JWT
- Unauthorized requests rejected
- Admin routes still use sessions (backward compatibility)

📊 Performance:
- Token generation: ~30ms
- Token verification: ~20ms
- No Redis dependency (stateless)

⚠️ Observations:
- Frontend needs update to store JWT (localStorage)
- Mobile app needs update to send Authorization header
- Consider token refresh after 24h (Phase 2)

✅ Ready for deployment
EOF
)"
```

---

### Кінець четвертого дня

**Демонстрація пошуку в пам'яті**:

```bash
# User searches session history
"Search my memory for JWT decisions"
```

**claude-mem повертає**:
```
🔍 Found 3 relevant sessions:

Session 1 (Day 1):
- Decision: JWT for API, sessions for admin
- Library: jose (40% lighter)

Session 2 (Day 2):
- Implemented JwtService
- Deferred refresh tokens to Phase 2

Session 4 (Day 4):
- All tests passing (7/7 unit, 4/4 E2E)
- Ready for deployment
```

**Фінальний стан стека пам'яті**:

| Шар | Вміст | Інструмент |
|-----|-------|------------|
| **Захоплення сесій** | 4 дні, 312 спостережень | claude-mem |
| **Ручні рішення** | 4 спогади (arch, refresh, migration, validation) | Serena |
| **Виявлення коду** | 8 змінених файлів, граф викликів оновлено | grepai |

---

## День 5: розгортання

### Ранок: перевірка перед розгортанням

**Користувач**: "What did we accomplish this week?"

**Claude** (запит до claude-mem):
```
"Show summary of JWT migration project"
```

**Повний підсумок claude-mem**:
```
📋 JWT Migration Project Summary (5 days):

Day 1: Discovery & Planning
- Explored auth system (4 key files)
- Decision: JWT for API, sessions for admin
- Library: jose (40% lighter, better TS)

Day 2: Implementation
- Installed jose
- Created JwtService (generateToken, verifyToken)
- Deferred refresh tokens to Phase 2

Day 3: Integration
- Updated UserController.login()
- Created jwtAuthMiddleware
- Applied to /api/*, kept sessions for /admin/*

Day 4: Testing
- Unit tests: 7/7 passed
- E2E tests: 4/4 passed
- Validation complete

📊 Impact:
- Files modified: 8
- Tool calls: 312
- Dependencies removed: express-session, connect-redis
- Dependencies added: jose
- Performance: Stateless (no Redis lookups)

✅ Ready for deployment
```

**Доступні спогади Serena**:
```bash
serena list_memories

# Output:
# 1. auth_architecture (Day 1)
# 2. jwt_refresh_tokens (Day 2)
# 3. jwt_migration_status (Day 3)
# 4. jwt_validation_results (Day 4)
```

---

### Обід: розгортання та передача

**Користувач**: "Deploy to staging"

```bash
# Deploy to staging
git checkout -b feature/jwt-migration
git add .
git commit -m "feat: migrate API authentication to JWT

- Replace express-session with JWT (jose library)
- Apply JWT to /api/* routes
- Keep sessions for /admin/* routes
- Add comprehensive tests (7 unit, 4 E2E)
- All tests passing

Breaking changes: None (backward compatible)
Migration: None required (no DB changes)
Rollback: Change app.ts route config"

git push origin feature/jwt-migration

# Create PR
gh pr create --title "Migrate API to JWT authentication" \
  --body "$(serena read_memory jwt_migration_status)"
```

**Документ передачі** (автоматично згенерований зі спогадів):
```bash
# Generate handoff doc from Serena memories
serena read_memory auth_architecture > docs/jwt-migration.md
serena read_memory jwt_migration_status >> docs/jwt-migration.md
serena read_memory jwt_validation_results >> docs/jwt-migration.md
```

**Результат**: повна документація архітектурних рішень, подробиць реалізації та результатів валідації.

---

## 🎯 Ключові висновки

### Стек пам'яті в дії

**Без стека пам'яті**:
- Повторне читання файлів щодня (~200 файлів × 5 днів = 1000 читань)
- Втрата контексту між сесіями
- Забуті архітектурні рішення
- Ручна документація рішень

**Зі стеком пам'яті (claude-mem + Serena + grepai)**:
- Автоматично вставлений контекст щоранку (0 повторних читань)
- Збережені архітектурні рішення (4 спогади Serena)
- Підтримуваний граф викликів (трасування grepai)
- Повна історія сесій (312 спостережень)
- **Результат**: 5-денний проєкт завершено зі збереженням повного контексту

---

### Ефективність токенів

| Метрика | Без | Зі стеком пам'яті | Економія |
|---------|-----|-------------------|----------|
| **Читання файлів** | 1000 | 150 (зменшення на 85%) | 850 читань |
| **Вхідні токени** | ~500k | ~75k (зменшення на 85%) | 425k токенів |
| **Втрата контексту** | Кожна сесія | Ніколи | 100% збереження |
| **Пригадування рішень** | Ручні нотатки | 4 спогади Serena | Миттєво |

**Вплив прогресивного розкриття**:
- Запит підсумку дня 5: 3 шари (пошук → хронологія → деталі)
- Без нього: завантажити всі 312 спостережень (~50k токенів)
- З ним: завантажити підсумок → 5 сесій → 1 деталь (~5k токенів)
- **Економія**: 90% токенів

---

### Практичні спостереження

**Коли використовувати кожен інструмент**:

1. **claude-mem** (автоматично):
   - Початок/кінець сесії (авто)
   - "Що ми робили вчора?"
   - "Покажи повну історію проєкту"

2. **Serena** (вручну, висока цінність):
   - Архітектурні рішення
   - Вибір бібліотек
   - Статус міграції
   - Плани відкату

3. **grepai** (семантичне виявлення):
   - "Знайди код автентифікації"
   - "Хто викликає цю функцію?"
   - "Покажи граф залежностей"

4. **rg** (точний пошук):
   - "Знайди оператори import"
   - "Покажи всі TODO"
   - "Грепни за конкретним шаблоном"

---

### Аналіз вартості

**5-денний проєкт**:

| Інструмент | Вартість | Примітки |
|------------|----------|----------|
| **claude-mem** | $4.68 | 312 спостережень × $0.15/100 |
| **Serena** | Безкоштовно | Локальне сховище |
| **grepai** | Безкоштовно | Локальний Ollama |
| **Разом** | **$4.68** | За 5 днів ідеальної пам'яті |

**ROI**: на 850 читань файлів менше × ~500 токенів/читання = 425k токенів заощаджено = $4.25 (за $0.01/1k токенів)

**Чиста вартість**: $0.43 за повну пам'ять протягом 5 днів

---

## 🔗 Ресурси

**Інструменти стека пам'яті**:
- [claude-mem GitHub](https://github.com/thedotmack/claude-mem)
- [Serena GitHub](https://github.com/oraios/serena)
- [grepai GitHub](https://github.com/yoanbernabeu/grepai)

**Розділи посібника**:
- Розділ 8.2.3: Serena (Symbol Memory)
- Розділ 8.2.4: grepai (Semantic Search)
- Розділ 8.2.5: claude-mem (Automatic Session Memory)
- Матриця рішень щодо інструментів пам'яті: guide/ultimate-guide.md:8630

---

**Воркфлоу створено**: 2026-02-10
**Версія посібника**: 3.24.0
**Автор**: Florian BRUNIAUX + Claude (Anthropic)
