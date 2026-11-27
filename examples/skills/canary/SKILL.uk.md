---
name: canary
description: "Моніторинг після деплою: стежити за продакшеном після деплою і сповіщати про регресії"
argument-hint: "[--baseline]"
effort: medium
disable-model-invocation: true
---

# Canary: моніторинг після деплою

Стежте за робочим застосунком після розгортання. Сповіщайте про помилки й регресії. Порівнюйте з базовим станом до деплою.

**Два режими:**
- `--baseline`: зафіксувати поточний стан ДО деплою
- *(за замовчуванням)*: моніторити ПІСЛЯ деплою і порівнювати з базовим станом

## Інструкції

### Фаза 1: Підготовка

Розберіть аргументи користувача й визначте контекст розгортання.

```bash
# Detect current branch and recent deploy commit
git branch --show-current
git log --oneline -5

# Auto-detect platform from config files
[ -f fly.toml ]         && echo "PLATFORM: fly"
[ -f render.yaml ]      && echo "PLATFORM: render"
[ -f vercel.json ]      && echo "PLATFORM: vercel"
[ -f netlify.toml ]     && echo "PLATFORM: netlify"
[ -f Procfile ]         && echo "PLATFORM: heroku"
[ -f railway.toml ]     && echo "PLATFORM: railway"

# Check for health endpoint
curl -sf "${URL}/health" -w "\n%{http_code}" 2>/dev/null | tail -1
curl -sf "${URL}/api/health" -w "\n%{http_code}" 2>/dev/null | tail -1
```

Створіть робочу директорію:

```bash
mkdir -p .canary/baselines .canary/reports .canary/screenshots
```

---

### Фаза 2: Фіксація базового стану (режим `--baseline`)

Запустіть це ДО деплою, щоб зафіксувати поточний справний стан.

Для кожної сторінки, яку треба моніторити, запишіть:

1. **HTTP-статус**: чи повертає сторінка 200?
2. **Час відповіді**: скільки триває завантаження?
3. **Знімок вмісту**: ключовий текст, щоб потім виявляти порожні сторінки

```bash
# For each page URL
for PAGE_PATH in "/" "/dashboard" "/settings" "/api/health"; do
  SLUG=$(echo "$PAGE_PATH" | tr '/' '_' | tr -d '?&=')
  RESULT=$(curl -sf -o /dev/null -w "%{http_code}|%{time_total}" "${BASE_URL}${PAGE_PATH}" 2>/dev/null)
  STATUS=$(echo "$RESULT" | cut -d'|' -f1)
  TIME_MS=$(echo "$RESULT" | awk -F'|' '{printf "%.0f", $2 * 1000}')
  echo "  ${PAGE_PATH}: HTTP ${STATUS}, ${TIME_MS}ms"
done
```

Збережіть базовий стан у `.canary/baselines/baseline.json`:

```json
{
  "url": "<base-url>",
  "timestamp": "<ISO-8601>",
  "branch": "<branch-name>",
  "commit": "<git-SHA>",
  "pages": {
    "/": { "status": 200, "time_ms": 450 },
    "/dashboard": { "status": 200, "time_ms": 680 },
    "/api/health": { "status": 200, "time_ms": 45 }
  }
}
```

Потім **ЗУПИНІТЬСЯ** і скажіть користувачу: «Базовий стан зафіксовано. Розгорніть зміни, потім запустіть `/canary <url>` для моніторингу.»

---

### Фаза 3: Виявлення сторінок

Якщо сторінки не вказано, знайдіть сторінки для моніторингу автоматично.

**Із застосунку:**

```bash
# Check sitemap if available
curl -sf "${URL}/sitemap.xml" 2>/dev/null | grep -oP '(?<=<loc>)[^<]+' | head -10

# Check robots.txt for known paths
curl -sf "${URL}/robots.txt" 2>/dev/null | grep -i "allow\|disallow" | head -10

# Common paths to always check
echo "Always check: / /login /dashboard /settings /api/health"
```

Типові сторінки для моніторингу, якщо нічого не знайдено: `/`, тобто лише головна.

---

### Фаза 4: Цикл моніторингу

Моніторте протягом заданого часу (за замовчуванням: 10 хвилин). Виконуйте перевірку кожні 60 секунд.

**Кожен цикл перевірки:**

```bash
TIMESTAMP=$(date -u +%Y-%m-%dT%H:%M:%SZ)
CHECK_NUM=$((CHECK_NUM + 1))

for PAGE_PATH in "${PAGES[@]}"; do
  # Check HTTP status and response time
  RESULT=$(curl -sf -o /dev/null -w "%{http_code}|%{time_total}" \
    --max-time 10 "${BASE_URL}${PAGE_PATH}" 2>/dev/null || echo "0|0")
  STATUS=$(echo "$RESULT" | cut -d'|' -f1)
  TIME_MS=$(echo "$RESULT" | awk -F'|' '{printf "%.0f", $2 * 1000}')

  # Compare against baseline
  BASELINE_STATUS=$(jq -r ".pages[\"${PAGE_PATH}\"].status // 200" .canary/baselines/baseline.json 2>/dev/null)
  BASELINE_TIME=$(jq -r ".pages[\"${PAGE_PATH}\"].time_ms // 1000" .canary/baselines/baseline.json 2>/dev/null)

  echo "  [Check #${CHECK_NUM}] ${PAGE_PATH}: HTTP ${STATUS} (${TIME_MS}ms)"
done
```

**Рівні сповіщень:**

| Рівень | Умова | Тригер |
|-------|-----------|---------|
| **CRITICAL** | Збій завантаження сторінки | HTTP-статус не 2xx, тайм-аут curl, збій DNS |
| **HIGH** | Нові помилки | Частка помилок зросла порівняно з базовим станом (помилки в консолі, відповіді 5xx) |
| **MEDIUM** | Регресія продуктивності | Час відповіді перевищує базовий удвічі |
| **LOW** | Нові биті посилання | Маршрути, що раніше працювали, тепер повертають 404 |

**Ключові принципи:**
- **Сповіщайте про зміни, а не про абсолютні значення.** Сторінка з 3 помилками в базовому стані в нормі, якщо їх і далі 3. Одна НОВА помилка вже є приводом для сповіщення.
- **Толерантність до тимчасових збоїв.** Сповіщайте лише про патерни, що зберігаються у 2+ послідовних перевірках. Один мережевий збій не є приводом для сповіщення.

**Коли спрацьовує сповіщення CRITICAL або HIGH (2 послідовні перевірки):**

```
CANARY ALERT
=====================================
Time:     [check #N at Xs elapsed]
Page:     [URL]
Level:    [CRITICAL / HIGH / MEDIUM / LOW]
Finding:  [what changed, be specific]
Baseline: [baseline value]
Current:  [current value]
=====================================
Options:
  A) Investigate now: stop monitoring, focus on this issue
  B) Continue monitoring: wait for next check to confirm
  C) Rollback: revert the deploy
  D) Dismiss: known issue, continue monitoring
```

---

### Фаза 5: Звіт про стан

Після завершення моніторингу (або зупинки користувачем) підготуйте підсумок.

```
CANARY REPORT: [url]
=========================================
Duration:    [X minutes]
Checks:      [N total per page]
Pages:       [N pages monitored]
Commit:      [deployed SHA]
Status:      [HEALTHY / DEGRADED / BROKEN]

Per-Page Results:
-----------------------------------------
  Page           Status      Avg Time   Alerts
  /              HEALTHY     450ms      0
  /dashboard     DEGRADED    1100ms     1 medium (was 450ms)
  /settings      HEALTHY     380ms      0
  /api/health    HEALTHY     45ms       0

Alerts Fired: [N] (X critical, Y high, Z medium, W low)

VERDICT: [DEPLOY HEALTHY / DEPLOY HAS ISSUES (see alerts above)]
=========================================
```

Збережіть звіт у `.canary/reports/<date>-canary.md`.

---

### Фаза 6: Оновлення базового стану

Якщо деплой справний і користувач хоче оновити базовий стан:

```bash
cp .canary/reports/latest-snapshot.json .canary/baselines/baseline.json
echo "Baseline updated to commit $(git rev-parse --short HEAD)"
```

---

## Формат виводу

Повний шаблон CANARY REPORT див. вище у Фазі 5.

Формат сповіщень у рядку (під час моніторингу):
```
[08:42:15] Check #3: /dashboard: ALERT HIGH, response time 1250ms (baseline: 420ms)
[08:43:15] Check #4: /dashboard: ALERT HIGH, response time 1180ms (baseline: 420ms)
-> Consistent across 2 checks. Firing alert.
```

## Використання

```
/canary https://app.example.com                # Monitor homepage for 10 min
/canary https://app.example.com --baseline     # Capture baseline before deploying
/canary https://app.example.com --duration 5m  # Monitor for 5 minutes
/canary https://app.example.com --quick        # Single-pass health check (no loop)
/canary https://app.example.com --pages /,/dashboard,/api/health
```

## Поради

1. **Завжди фіксуйте базовий стан** перед деплоєм у продакшен: запустіть `/canary <url> --baseline`
2. **Починайте моніторинг одразу** після деплою; перші 5 хвилин виявляють 90% регресій
3. **Сповіщення CRITICAL** потребують негайного розслідування; не чекайте завершення моніторингу
4. **Сповіщення MEDIUM (продуктивність)** можуть бути наслідком прогрівання кешу; дайте ще 2-3 перевірки, перш ніж діяти
5. **Тримайте `.canary/baselines/` у git**, щоб будь-хто з команди міг запускати canary з тим самим базовим станом

## Пов'язані команди

- `/ship`: чекліст перед деплоєм (запускайте перед розгортанням)
- `/land-and-deploy`: повний конвеєр від злиття до перевірки (автоматично запускає canary)
- `/qa`: інтерактивне QA-тестування перед випуском

$ARGUMENTS
