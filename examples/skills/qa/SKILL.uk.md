---
name: qa
description: "Систематичне QA-тестування вебзастосунку: з урахуванням diff, багаторівневе, з циклом виправлення та перевірки"
argument-hint: "[path] [--thorough]"
effort: high
disable-model-invocation: true
---

# QA: Тестування вебзастосунку

Систематично протестуйте вебзастосунок на баги, а потім виправте й перевірте кожну знайдену проблему.

Три рівні ґрунтовності. Обсяг з урахуванням diff тестує те, що справді змінилося.

## Інструкції

### Крок 1: Визначення обсягу

Визначте, які сторінки та функції тестувати.

**Режим з урахуванням diff (за замовчуванням):** Визначте зачеплені маршрути за змінами поточної гілки.

```bash
# Files changed in this branch
git diff --name-only origin/main...HEAD 2>/dev/null || git diff --name-only HEAD~5

# Identify affected routes from changed files
# e.g., changes in src/pages/dashboard/ → test /dashboard
# changes in api/payments/ → test payment flows
```

**Повний режим** (`/qa --full`): Протестуйте весь застосунок, починаючи з критичних шляхів.

**Явний обсяг** (`/qa /dashboard /settings`): Тестуйте лише вказані сторінки.

---

### Крок 2: Вибір рівня

| Рівень | Прапорець | Обсяг | Коли використовувати |
|--------|-----------|-------|----------------------|
| Quick | `--quick` | Лише Critical + High | Швидка перевірка перед комітом |
| Standard | *(за замовчуванням)* | + Medium | Рев'ю перед PR |
| Exhaustive | `--exhaustive` | + Low + косметичні | Реліз-кандидат |

---

### Крок 3: Чисте робоче дерево

Перед тестуванням переконайтеся, що можете комітити виправлення атомарно.

```bash
git status --short
```

Якщо є незакомічені зміни: спершу сховайте їх (`git stash`) або закомітьте. Тестування на брудному дереві унеможливлює ізоляцію комітів з виправленнями.

---

### Крок 4: Тестування

Для кожної сторінки в обсязі систематично перевірте всі категорії, релевантні обраному рівню.

#### Як тестувати

Використовуйте будь-які доступні браузерні інструменти:
- **MCP-інструменти браузера** (якщо налаштовано): автоматична навігація та скриншоти
- **Playwright/Puppeteer** (якщо є в проєкті): скриптові запуски тестів
- **Ручне тестування**: перейдіть за URL, систематично документуйте знахідки

Для кожної сторінки перевірте:

```
1. Load the page: does it render without errors?
2. Check console: any uncaught errors, failed requests, warnings?
3. Test primary user action: the core thing this page is for
4. Test empty state: what shows when there's no data?
5. Test error state: what happens when an action fails?
6. Test on narrow viewport: does it break below 375px?
```

#### Таксономія проблем

**Visual** (розмітка, відступи, типографіка, кольори, адаптивність)
**Functional** (зламана взаємодія, відсутні функції, неправильна поведінка)
**UX** (заплутані потоки, відсутній зворотний зв'язок, погані повідомлення про помилки)
**Content** (одруківки, неправильний текст, текст-заглушка в продакшені)
**Performance** (повільне завантаження сторінок, зсуви розмітки, неоптимізовані зображення)
**Console** (помилки JavaScript, невдалі мережеві запити, попередження про застарілість)
**Accessibility** (відсутній alt-текст, пастки клавіатури, відсутні підписи, контраст)

#### Рівні серйозності

| Серйозність | Критерії | Приклади |
|-------------|----------|----------|
| **Critical** | Функція повністю зламана або ризик втрати даних | Помилка 500, порожня сторінка, форма, що втрачає дані |
| **High** | Основна функція погіршена, значна шкода для UX | Показано неправильні дані, зламаний основний CTA, зламана мобільна розмітка |
| **Medium** | Незначна проблема функції, помітна, але є обхідний шлях | Візуальний глюк, заплутаний порожній стан, повільне завантаження |
| **Low** | Косметична, ледь помітна | Незначні відступи, дрібна проблема з текстом, попередження консолі низької серйозності |

**Рівень Quick**: лише Critical + High
**Рівень Standard**: Critical + High + Medium
**Рівень Exhaustive**: усі рівні серйозності

---

### Крок 5: Документування знахідок

Відстежуйте кожну проблему з унікальним ID.

```
ISSUE-001
  Severity:  [Critical / High / Medium / Low]
  Category:  [Visual / Functional / UX / Content / Performance / Console / Accessibility]
  Page:      [URL or route]
  Finding:   [What is wrong, specific not vague]
  Steps:     [How to reproduce]
  Expected:  [What should happen]
  Evidence:  [Screenshot path or console output]
```

---

### Крок 6: Цикл виправлення та перевірки

Для кожної проблеми Critical і High (а також Medium/Low на рівнях Standard/Exhaustive):

1. **Виправте проблему** у вихідному коді
2. **Комітьте атомарно**: один коміт на одне виправлення

```bash
git add <changed-files>
git commit -m "fix: <brief description of what was fixed>"
```

3. **Повторно перевірте**: відкрийте ту саму сторінку й переконайтеся, що проблему розв'язано
4. **Оновіть статус проблеми** на FIXED із хешем коміту

Не об'єднуйте кілька виправлень в один коміт. Кожне виправлення має відкочуватися окремо.

---

## Формат виводу

```
QA REPORT
════════════════════════════════════════
Branch:    [current branch]
Scope:     [pages tested]
Tier:      [Quick / Standard / Exhaustive]
Duration:  [time taken]

HEALTH SCORES
─────────────────────────────────────────
  Visual        [PASS / WARN / FAIL]  [N issues]
  Functional    [PASS / WARN / FAIL]  [N issues]
  UX            [PASS / WARN / FAIL]  [N issues]
  Content       [PASS / WARN / FAIL]  [N issues]
  Performance   [PASS / WARN / FAIL]  [N issues]
  Console       [PASS / WARN / FAIL]  [N issues]
  Accessibility [PASS / WARN / FAIL]  [N issues]

ISSUES FOUND: N (X critical, Y high, Z medium, W low)
ISSUES FIXED: N
ISSUES REMAINING: N

─────────────────────────────────────────
ISSUE-001 [FIXED | OPEN]
  Severity:  High
  Category:  Functional
  Page:      /dashboard
  Finding:   Save button does nothing when form has validation errors, no feedback shown
  Fix:       Added error toast notification (commit abc1234)

ISSUE-002 [OPEN]
  Severity:  Medium
  Category:  Visual
  Page:      /settings
  Finding:   Input fields overflow container below 375px viewport
  ...

─────────────────────────────────────────
SHIP READINESS
  Critical issues:  [0 remaining / N remaining (BLOCKER)]
  High issues:      [0 remaining / N remaining (CONCERN)]

VERDICT: [READY TO SHIP / NOT READY: address critical and high issues first]
════════════════════════════════════════
```

## Використання

```
/qa                          # Standard tier, diff-aware scope
/qa --quick                  # Quick tier (critical + high only)
/qa --exhaustive             # Full coverage including cosmetic issues
/qa --full                   # Standard tier, test entire app (not just diff)
/qa /dashboard /settings     # Test specific pages
/qa https://staging.app.com  # Test a specific URL
```

## Поради

1. **Запускайте після кожної значної функції**, а не лише перед випуском
2. **Спершу з урахуванням diff**: тестуйте те, що змінилося, перш ніж розширювати обсяг
3. **Виправляйте critical і high, перш ніж продовжувати**: не накопичуйте невиправлені проблеми
4. **Докази у вигляді скриншотів**: завжди робіть знімки до/після для критичних виправлень
5. **Перевіряйте mobile**: більшість візуальних багів проявляється при ширині 375px

## Пов'язані команди

- `/investigate`: аналіз першопричини, коли QA знаходить складний баг
- `/ship`: чекліст перед деплоєм (запускайте після успішного QA)
- `/canary`: моніторинг після деплою (запускайте після випуску)

$ARGUMENTS
