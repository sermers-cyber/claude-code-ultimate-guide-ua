---
name: security-checklist
description: Повний чекліст безпеки для вебзастосунків
effort: medium
---

# Skill «Чекліст безпеки»

## Швидкий аудит безпеки

### Автентифікація
- [ ] Паролі хешуються через bcrypt/argon2 (cost factor >= 10)
- [ ] Токени сесій криптографічно випадкові
- [ ] JWT-токени мають короткий термін дії (15 хв для access, 7 днів для refresh)
- [ ] На endpoint-ах входу діє rate limiting
- [ ] Обліковий запис блокується після невдалих спроб

### Авторизація
- [ ] Кожен endpoint API перевіряє права доступу
- [ ] Немає IDOR (Insecure Direct Object References)
- [ ] Реалізовано рольовий контроль доступу
- [ ] Чутливі операції вимагають повторної автентифікації

### Валідація вхідних даних
- [ ] Усі дані від користувача валідуються на боці сервера
- [ ] Завантаження файлів обмежене за типом і розміром
- [ ] SQL-запити використовують параметризовані вирази
- [ ] HTML-вивід екранується для запобігання XSS

### Захист даних
- [ ] Чутливі дані зашифровані у спокої (at rest)
- [ ] HTTPS примусово застосовується скрізь
- [ ] Захищені cookies (HttpOnly, Secure, SameSite)
- [ ] Немає чутливих даних в URL чи логах

### Заголовки та CORS
- [ ] Встановлено заголовок Content-Security-Policy
- [ ] X-Content-Type-Options: nosniff
- [ ] X-Frame-Options: DENY (або SAMEORIGIN)
- [ ] Увімкнено Strict-Transport-Security
- [ ] CORS коректно обмежено

## Шаблони коду

### Запобігання SQL-ін'єкціям
```javascript
// VULNERABLE
db.query(`SELECT * FROM users WHERE id = ${userId}`);

// SECURE
db.query('SELECT * FROM users WHERE id = $1', [userId]);
```

### Запобігання XSS
```javascript
// VULNERABLE
element.innerHTML = userInput;

// SECURE
element.textContent = userInput;

// SECURE (with sanitization)
element.innerHTML = DOMPurify.sanitize(userInput);
```

### Захист від CSRF
```javascript
// Generate token
const csrfToken = crypto.randomBytes(32).toString('hex');
session.csrfToken = csrfToken;

// Validate on POST
if (req.body.csrf !== session.csrfToken) {
  throw new ForbiddenError('Invalid CSRF token');
}
```

### Керування секретами
```javascript
// NEVER in code
const API_KEY = 'sk-abc123...';

// Environment variables
const API_KEY = process.env.API_KEY;

// Secrets manager (production)
const secret = await secretsManager.getSecret('api-key');
```

## Приклад заголовків безпеки

```javascript
// Express middleware
app.use((req, res, next) => {
  res.setHeader('X-Content-Type-Options', 'nosniff');
  res.setHeader('X-Frame-Options', 'DENY');
  res.setHeader('X-XSS-Protection', '1; mode=block');
  res.setHeader('Strict-Transport-Security', 'max-age=31536000; includeSubDomains');
  res.setHeader('Content-Security-Policy', "default-src 'self'");
  next();
});
```

## Безпека залежностей

```bash
# Check for vulnerabilities
npm audit

# Auto-fix what's possible
npm audit fix

# Check outdated packages
npm outdated

# Update dependencies
npm update
```

## Логування подій безпеки

```javascript
// Events to log
logger.security({
  event: 'login_failed',
  ip: req.ip,
  email: req.body.email,
  reason: 'invalid_password',
  timestamp: new Date().toISOString()
});

// Never log
// - Passwords
// - Full credit card numbers
// - Session tokens
// - Personal data (in production)
```

## Чекліст перед розгортанням

1. [ ] Запустіть `npm audit` - без критичних вразливостей
2. [ ] Усі секрети лежать у змінних середовища
3. [ ] Режим налагодження вимкнено
4. [ ] Повідомлення про помилки не розкривають внутрішніх деталей
5. [ ] Лише HTTPS (HTTP перенаправляє на HTTPS)
6. [ ] Облікові дані бази даних ротовано
7. [ ] Логування налаштовано (без чутливих даних)
8. [ ] Стратегію резервного копіювання перевірено
