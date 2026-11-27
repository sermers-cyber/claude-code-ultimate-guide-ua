---
name: plan-pipeline-execute
description: "Виконання перевіреного плану: ізоляція через worktree, каркас TDD, паралельні agents за рівнями, quality gate зі smoke-тестом, створення та мерж PR. Охоплює все аж до змердженого PR."
effort: high
disable-model-invocation: true
---

# /plan-pipeline:execute: Виконання до змердженого PR

Виконайте перевірений план в ізольованому worktree. Запустіть agent для кожного завдання, перевірте якість, створіть і змерджіть PR. Охоплює все аж до очищення.

Виконайте `/clear` перед цією командою.

---

## Передумова

Перевірений план має існувати в `docs/plans/plan-{name}.md`, з усіма розв'язаними проблемами (результат `/plan-pipeline:validate`).

---

## Крок 1: Налаштування worktree

Створіть ізольований git worktree:

```bash
git worktree add .worktrees/{plan-name} -b feature/{plan-name}
```

Уся робота відбувається всередині worktree. Головна гілка залишається чистою весь час.

---

## Крок 2: Каркас TDD

*Лише для завдань, позначених у плані як TDD.*

Для кожного TDD-завдання, до будь-якої реалізації:
1. Напишіть тест(и), що падають і визначають критерії прийняття
2. Запустіть тести, щоб підтвердити, що вони падають (red)
3. Закомітьте тести, що падають
4. Позначте тестовий файл у завданні, щоб agent реалізації його знайшов

Не пишіть код реалізації на цьому кроці.

---

## Крок 3: Паралельне виконання за рівнями

Розберіть список завдань із плану. Згрупуйте завдання за шарами (Шар 1 = фундамент, Шар 2 залежить від Шару 1 тощо).

**Для кожного шару:**
1. Визначте всі завдання шару
2. Запустіть по одному agent на завдання паралельно (інструмент Task, run_in_background: true)
3. Кожен agent отримує: опис свого завдання, файли для зміни, критерії прийняття та відповідні ADR
4. Стежте за всіма agents, читаючи через `Read` шлях виводу, про який повідомив agent (TaskOutput видалено у v2.1.278)
5. Кожен agent комітить після завершення завдання: `git commit -m "feat: {task-description}"`
6. Дочекайтеся завершення всіх завдань шару, перш ніж починати наступний шар

**Виявлення дрейфу**: після кожного шару порівняйте фактичні зміни зі специфікацією плану. Якщо реалізація суттєво відхиляється від плану (нові файли, яких немає в плані, файли з плану, яких не торкнулися), позначте це й запитайте, як діяти далі. Не продовжуйте мовчки за наявності дрейфу.

**Інструкції agent для кожного завдання:**
```
You are implementing one task from a validated plan.
Task: {description}
Files to modify: {file list}
Acceptance criteria: {criteria}
Relevant ADRs: {adr list}

First principles:
- Build state-of-the-art. No workarounds, no legacy patterns.
- Fix at the correct architectural level, never with component-level hacks.
- If you discover that the plan is wrong or missing context, stop and report. Do not improvise architecture.

Commit your changes when complete with message: "feat: {task-description}"
```

---

## Крок 4: Quality gate

Запустіть паралельно:
- Лінтер
- Перевірка типів (за потреби)
- Повний набір тестів

Якщо все проходить: переходьте до smoke-тесту.

Якщо щось падає: запустіть debug-agent `quality-fixer` з виводом збою. Він має до **3 спроб автовиправлення**. Після кожної спроби перезапускайте quality gate. Якщо після 3 спроб усе ще падає: зупиніться, повідомте про збій із повним виводом помилки й чекайте втручання людини.

**Інтеграційний smoke-тест** *(пропустіть для суто frontend-планів або планів лише з документацією)*:

Виконайте smoke-команди, визначені в розділі плану `## Integration Verification`. Додатково:
- Якщо GraphQL: запустіть інтроспекційний запит, щоб переконатися, що схема доступна
- Якщо сервіси Docker: проскануйте логи контейнерів на записи рівня ERROR
- Якщо є нові API-маршрути: перевірте, що кожен повертає очікувані коди статусу

Збої smoke-тесту налагоджує agent `quality-fixer-smoke` з тим самим лімітом у 3 спроби.

---

## Крок 5: Документація перед PR

*У worktree, перед створенням PR.*

**Узгодження PRD**: порівняйте реалізовану поведінку з початковим PRD. Занотуйте будь-які відхилення чи доповнення, виявлені під час реалізації. Оновіть PRD фактичними даними. Ці оновлення надходять в тому самому PR, що й функція.

**Архівація плану**: перенесіть `docs/plans/plan-{name}.md` до `docs/plans/completed/plan-{name}.md`. Оновіть заголовок статусу.

Закомітьте оновлення документації: `docs: reconcile PRD and archive plan for {feature-name}`.

---

## Крок 6: Push і PR

Запуште гілку worktree й створіть PR:

```bash
git push origin feature/{plan-name}
gh pr create \
  --title "{feature-name}: {one-line summary from plan}" \
  --body "$(cat .pr-body.md)"
```

Шаблон тіла PR:
```markdown
## Summary
{plan summary paragraph}

## Changes
{auto-generated from task list: bullet per task with files affected}

## ADRs
{list of ADRs created during this plan}

## Test Plan
{from plan test plan section}

## Smoke Test Results
{output from integration verification}
```

Мерджте через squash:
```bash
gh pr merge --squash --delete-branch
```

---

## Крок 7: Метрики після мерджу

Перемкніться назад на develop/main. Оновіть `docs/plans/metrics/{name}.json` даними виконання:
- Кількість завдань і розбивка за шарами
- Кількість TDD-завдань
- Статистика diff (змінені файли, додані/видалені рядки)
- Результати quality gate (пройдено/не пройдено, спроби виправлення)
- Результати smoke-тесту
- Оцінка дрейфу (0-1, наскільки реалізація відповідала плану)
- Дані PR (номер, merge-коміт, часова мітка)

Закомітьте оновлення метрик.

---

## Крок 8: Очищення worktree

```bash
git worktree remove .worktrees/{plan-name}
```

---

## Використання

```
/plan-pipeline:execute
```

Бере найновіший перевірений план. Або вкажіть:

```
/plan-pipeline:execute plan-user-authentication
```

## Результат

```
Setting up worktree: .worktrees/user-authentication
Branch: feature/user-authentication

TDD scaffolding: 2 tasks marked TDD
  ✓ Written failing tests for: auth-token-validation
  ✓ Written failing tests for: refresh-token-rotation
  Committed: "test: failing tests for auth pipeline (TDD)"

Executing Layer 1 (3 tasks, parallel)...
  [agent-1] Implementing: JWT token generation service
  [agent-2] Implementing: User session model
  [agent-3] Implementing: Auth middleware
  ✓ Layer 1 complete. 3 commits.

Drift check: Layer 1... ✓ No drift detected.

Executing Layer 2 (2 tasks, parallel)...
  [agent-4] Implementing: Login endpoint
  [agent-5] Implementing: Refresh endpoint
  ✓ Layer 2 complete. 2 commits.

Quality gate...
  ✓ Lint passed
  ✓ Type check passed
  ✓ Tests: 47 passed, 0 failed

Smoke test...
  ✓ GraphQL introspection: OK
  ✓ POST /api/auth/login: 200
  ✓ POST /api/auth/refresh: 200

Pre-PR docs...
  ✓ PRD reconciled (1 minor deviation noted)
  ✓ Plan archived to docs/plans/completed/

PR created: #142 "user-authentication: JWT auth with refresh token rotation"
PR merged (squash). Branch deleted.

Metrics committed. Worktree cleaned.
✅ Feature complete.
```

## Коли використовувати

Після того, як `/plan-pipeline:validate` підтвердив, що всі проблеми розв'язано. Ніколи не пропускайте валідацію: виконання неперевіреного плану оминає незалежний огляд, який у середньому виловлює ~18 проблем.

## Позиція в конвеєрі

```
/plan-pipeline:ceo-review    → продуктовий напрям зафіксовано
/plan-pipeline:eng-review    → архітектуру зафіксовано
/plan-pipeline:start         → створити план реалізації
/plan-pipeline:validate      → перевірити перед виконанням
/plan-pipeline:execute       → виконати до змердженого PR          ← ви тут
```
