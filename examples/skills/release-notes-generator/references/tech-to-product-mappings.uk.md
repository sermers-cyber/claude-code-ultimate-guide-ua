# Правила перетворення технічного на продуктове

Цей документ визначає, як перетворювати технічні повідомлення комітів на зрозумілу користувачам продуктову мову.

## Категорії перетворення

### 1. ПОВІДОМЛЯТИ (перетворити на продуктову мову)

| Технічний патерн | Продуктове повідомлення |
|------------------|-------------------------|
| `N+1 queries`, `DataLoader`, `batching` | "Faster list loading" |
| `embeddings`, `vector search`, `pgvector` | "Improved intelligent search" |
| `permissions`, `scope`, `access control` | "Fixed an access bug" |
| `retry logic`, `resilience`, `connection errors` | "Better connection stability" |
| `SSE`, `real-time`, `WebSocket` | "Real-time updates" |
| `cache`, `memoization` | "Improved performance" |
| `responsive`, `mobile` | "Better mobile experience" |
| `accessibility`, `a11y`, `WCAG` | "Improved accessibility" |
| `monitoring`, `alerting`, `error tracking` | "Better error tracking" |
| `validation`, `sanitization` | "Enhanced security" |

### 2. НЕ ПОВІДОМЛЯТИ (лише внутрішнє/технічне)

Ці патерни НЕ повинні з'являтися в оголошеннях у Slack:

| Технічний патерн | Причина |
|------------------|---------|
| `refactor`, `refactoring` | Внутрішня якість коду |
| `webpack`, `turbopack`, `bundler` | Інструменти збірки |
| `eslint`, `prettier`, `linting` | Стиль коду |
| `kebab-case`, `naming convention` | Внутрішні стандарти |
| `TypeScript`, `type safety` | Досвід розробника |
| `test`, `spec`, `coverage` | Інфраструктура тестування |
| `chore`, `maintenance` | Рутинна підтримка |
| `docs`, `documentation` | Внутрішні документи |
| `deps`, `dependencies`, `bump` | Оновлення залежностей |
| `CI`, `CD`, `workflow` | Інфраструктура DevOps |

### 3. БЕЗПЕКА (завжди повідомляти, спрощено)

| Технічне | Продуктове |
|----------|------------|
| `CVE-XXXX-XXXXX` | "Fixed a security vulnerability" |
| `XSS`, `injection` | "Enhanced data protection" |
| `authentication`, `auth bypass` | "Improved login security" |
| `CORS`, `CSRF` | "Protection against web attacks" |

## Перетворення з урахуванням контексту

### Пов'язане з API
- "Fix endpoint rate limiting" -> "Improved API stability"
- "Add request validation" -> "Better input handling"
- "Optimize query performance" -> "Faster data loading"

### Пов'язане з дашбордом
- "Fix dashboard widget rendering" -> "Fixed display issues on dashboard"
- "Add export functionality" -> "New data export feature"
- "Improve chart performance" -> "Faster dashboard loading"

### Пов'язане зі сповіщеннями
- "Fix email delivery queue" -> "Improved notification reliability"
- "Add webhook retry logic" -> "More reliable integrations"
- "Optimize notification batching" -> "Faster notification delivery"

### Пов'язане з пошуком
- "Fix search indexing race condition" -> "Improved search reliability"
- "Add fuzzy matching" -> "Better search results"
- "Optimize search query execution" -> "Faster search"

## Вплив за ролями

Завжди вказуйте, кого це стосується:

| Вплив | Ролі |
|-------|------|
| Зміни дашборда | Кінцеві користувачі, адміністратори |
| Зміни API | Кінцеві користувачі, досвідчені користувачі |
| Адмін-панель | Лише адміністратори |
| Білінг/платежі | Адміністратори, стейкхолдери |
| Звіти/аналітика | Адміністратори, досвідчені користувачі |
| Сповіщення | Усі користувачі |
| Пошук | Усі користувачі |

## Індикатори серйозності

Використовуйте ці префікси, коли доречно:

- **Critical** : проблеми, що блокують продакшен
- **Important** : баги, помітні користувачам
- **Minor** : покращення зручності
- *Не згадувати* : внутрішні виправлення
