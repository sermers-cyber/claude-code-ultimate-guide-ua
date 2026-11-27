---
name: plan-pipeline-validate
description: "2-шарова валідація плану: миттєві структурні перевірки + спеціалізовані agents за тригерами. Автоматично виправляє проблеми за допомогою ADR і перших принципів. Кожну проблему потрібно розв'язати до виконання."
effort: medium
disable-model-invocation: true
---

# /plan-pipeline:validate: 2-шарова валідація

Незалежно перевірте план, створений `/plan-pipeline:start`. Код не пишеться. Виконайте `/clear` після цієї команди, перш ніж запускати `/plan-pipeline:execute`.

Валідацію навмисно відокремлено від планування: валідатори, які не писали план, не прив'язані до його припущень.

---

## Передумова

Закомічений файл плану має існувати в `docs/plans/plan-{name}.md`. Якщо планів кілька, перелічіть їх і запитайте користувача, який перевіряти.

---

## Шар 1: Структурна валідація

Виконується негайно, agents не потрібні. Перевірте документ плану на:

**Формат і повнота**
- [ ] Усі обов'язкові розділи на місці (Summary, Decisions, Architecture, Tasks, Test Plan, Out of Scope)
- [ ] Кожне завдання має: опис, зачеплені файли, критерії прийняття, призначення шару

**Ланцюг залежностей**
- [ ] Немає циклічних залежностей між завданнями
- [ ] Завдання у вищих шарах залежать лише від завдань у нижчих шарах
- [ ] Усі заявлені залежності існують у плані

**Існування файлів**
- [ ] Кожен файл, указаний для зміни, справді існує в кодовій базі (використайте Glob)
- [ ] Нові файли лежать у відповідних каталогах згідно з конвенціями проєкту

**Узгодженість з ADR**
- [ ] Рішення плану відповідають ADR, створеним під час `/plan-pipeline:start`
- [ ] Немає суперечності з наявними ADR у `docs/adr/`

**Відповідність CLAUDE.md**
- [ ] План дотримується всіх жорстких правил із CLAUDE.md
- [ ] Немає порушень перших принципів (жодних обхідних шляхів, жодних shims зворотної сумісності)

**Покриття тестами**
- [ ] Кожна нова функція/компонент має відповідне тестове завдання
- [ ] Для завдань із позначкою TDD тест, що падає, написано до завдання реалізації

Зафіксуйте всі проблеми Шару 1 із серйозністю (BLOCKER / WARNING / INFO), перш ніж переходити до Шару 2.

---

## Шар 2: Огляд спеціалістами

Оберіть agents, застосувавши правила тригерів до вмісту плану. Введення від користувача не потрібне; тригери об'єктивні.

**Пул валідаційних agents:**

| Agent | Тригер | Модель |
|-------|--------|--------|
| `security-reviewer` | Auth, платежі, PII, RBAC, нові публічні API | Opus |
| `db-migration-reviewer` | Нові таблиці, стовпці, індекси або файли міграцій | Opus |
| `performance-reviewer` | Нові запити, resolvers, маршрути або додані залежності | Sonnet |
| `design-system-reviewer` | Нові UI-компоненти або зміни візуального стилю | Sonnet |
| `ux-reviewer` | Нові сторінки, форми, модальні вікна або патерни взаємодії | Sonnet |
| `cross-platform-reviewer` | Зміни, що торкаються і web, і mobile, або спільних пакетів | Sonnet |
| `native-app-reviewer` | Мобільні екрани, зміни в native UI-пакеті | Sonnet |
| `integration-reviewer` | Нові зовнішні сервіси, бібліотеки або конфігурація OTEL | Opus |

Запустіть agents, що спрацювали, паралельно (інструмент Task, run_in_background: true). Кожен agent отримує: файл плану, відповідні ADR і цільові запитання за своєю галуззю.

Стежте через `Read` для шляху виводу, про який повідомив agent (TaskOutput видалено у v2.1.278). Повідомляйте користувачу про прогрес.

Кожен agent має повернути структуровані висновки:
```
FINDING: [BLOCKER|WARNING|INFO]
Location: [plan section or file reference]
Issue: [concrete description]
Risk: [what breaks if this isn't addressed]
Suggestion: [specific fix or alternative]
```

---

## Фаза автовиправлення

Об'єднайте структурні проблеми Шару 1 і висновки спеціалістів Шару 2 в один список проблем. Кожну проблему потрібно розв'язати. Жодних пропусків.

**Тріаж кожної проблеми:**

**Група A: Автоматичне розв'язання**
- Проблема відповідає наявному рішенню ADR → послатися на ADR, позначити розв'язаною
- Проблема відповідає підтвердженому патерну в PATTERNS.md → послатися на патерн, позначити розв'язаною
- Проблему можна розв'язати з перших принципів у CLAUDE.md → застосувати правило, позначити розв'язаною

**Група B: Потрібне рішення людини**
- Нове архітектурне питання, не охоплене наявними рішеннями
- Суперечливі ADR без чіткого прецеденту
- Блокер без очевидного розв'язання

Для пунктів Групи B: представте проблему, поясніть, чому її не можна розв'язати автоматично, запропонуйте варіанти, дочекайтеся рішення. Зафіксуйте рішення в розділі плану `## Decisions` і створіть новий ADR, якщо воно архітектурно значуще.

**Застосуйте всі виправлення одним пакетом**, коли всі проблеми пройшли тріаж. Оновіть файл плану. Закомітьте оновлений план.

---

## Збереження проблем

Запишіть кожну проблему в `docs/plans/metrics/{name}.json` у `validation.issues`:

```json
{
  "id": "S-001",
  "layer": 1,
  "severity": "WARNING",
  "category": "test-coverage",
  "description": "No test task for the new webhook handler",
  "reporting_agent": "structural",
  "triage": "A",
  "resolution_source": "first-principles",
  "resolution": "Added test task in Layer 2 of the plan"
}
```

---

## Автоматичний перехід

Якщо всі проблеми розв'язано автоматично (лише Група A): автоматично запустіть `/plan-pipeline:execute` без запитання.

Якщо потрібне було рішення людини (Група B): запитайте "Усі проблеми розв'язано. Готові виконувати?" перед продовженням.

---

## Використання

```
/plan-pipeline:validate
```

Автоматично бере найновіший незакомічений план. Або вкажіть:

```
/plan-pipeline:validate plan-user-authentication
```

## Результат

```
Layer 1: Structural validation...
  ✓ Format complete
  ✓ Dependencies valid
  ⚠ WARNING S-001: Missing test task for webhook handler
  ✓ CLAUDE.md compliant

Layer 2: Triggering specialist agents...
  → security-reviewer (auth changes detected) [Opus]
  → db-migration-reviewer (new users table) [Opus]
  → performance-reviewer (new query in /api/users) [Sonnet]
  Monitoring... 1/3 complete... 2/3 complete... done.

  BLOCKER B-001 [security-reviewer]: JWT expiry not validated on refresh endpoint
  WARNING B-002 [db-migration-reviewer]: Migration lacks rollback strategy

Auto-fix phase:
  S-001 → auto-resolved (first principles: test coverage rule)
  B-001 → NEEDS INPUT (no existing ADR for JWT refresh strategy)
  B-002 → auto-resolved (ADR-0003: migration rollback pattern)

[User input requested for B-001]
Decision recorded. ADR-0011 created.

All 3 issues resolved. Plan updated.
→ Auto-starting /plan-pipeline:execute
```

## Коли використовувати

Завжди запускайте перед будь-яким викликом `/plan-pipeline:execute`. Вартість валідації ($0.20-3.00) мізерна порівняно з вартістю виявлення проблем посеред виконання.

## Позиція в конвеєрі

```
/plan-pipeline:ceo-review    → продуктовий напрям зафіксовано
/plan-pipeline:eng-review    → архітектуру зафіксовано
/plan-pipeline:start         → створити план реалізації
/plan-pipeline:validate      → перевірити перед виконанням     ← ви тут
/plan-pipeline:execute       → виконати до змердженого PR
```
