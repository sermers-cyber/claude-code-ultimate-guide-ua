---
title: "Робочий процес керування завданнями"
description: "Координація завдань між кількома сесіями за допомогою Tasks API та TodoWrite для складних проектів"
tags: [workflow, guide, agents]
---

# Робочий процес керування завданнями

**Версія**: Claude Code v2.1.16+
**Необхідні умови**: Розуміння робочих процесів з кількома сесіями, базові навички роботи з CLI
**Час**: 15–30 хв для ознайомлення, застосовується до всіх складних проектів

## Огляд

Керування завданнями в Claude Code суттєво еволюціонувало у версії v2.1.16 з появою **Tasks API**, який доповнив оригінальний інструмент **TodoWrite**. Цей посібник пояснює, коли використовувати кожну із систем та як ефективно координувати завдання у кількох сесіях для складних проектів.

**Коли використовувати цей робочий процес:**
- Проекти, які охоплюють кілька сесій написання коду
- Сценарії координації кількох агентів (multi-agent coordination)
- Складні ієрархії завдань із залежностями
- Необхідність відновити роботу після стиснення контексту (context compaction) або переривання сесії

**Коли НЕ використовувати:**
- Односесійні, прості впровадження
- Швидкі виправлення або дослідницьке написання коду
- Завдання, які можна виконати менш ніж за 10 хвилин

---

## Швидка довідка: порівняння систем

| Функція | TodoWrite (застаріла) | Tasks API (v2.1.16+) |
|---------|-------------------|---------------------|
| **Збереження даних** | Лише в пам'яті сесії | На диску (`~/.claude/tasks/`) |
| **Кілька сесій** | ❌ Втрачається після завершення сесії | ✅ Зберігається між сесіями |
| **Залежності** | ❌ Впорядкування вручну | ✅ Блокування завдань (A блокує B) |
| **Координація** | Один агент | ✅ Мультиагентна система з трансляцією (broadcast) |
| **Відстеження статусу** | pending/in_progress/completed | pending/in_progress/completed |
| **Коли використовувати** | Прості списки справ для однієї сесії | Складні багатосесійні проекти |

**Прапорець міграції** (v2.1.19+):
```bash
# Використовувати стару систему (TodoWrite)
CLAUDE_CODE_ENABLE_TASKS=false claude

# Використовувати нову систему (Tasks API) — увімкнено за замовчуванням починаючи з v2.1.19
claude
```

---

## Фаза робочого процесу 1: Планування завдань

**Мета**: Декомпонувати складну роботу на одиниці, які можна відстежувати та виконувати.

### Крок 1: Аналіз обсягу робіт

Перед створенням завдань розберіться, що саме ви будуєте:

```bash
# Шаблон дослідження
claude
> "Analyze this codebase for implementing JWT authentication:
  - Glob for existing auth patterns
  - Grep for security-related code
  - Identify integration points"
```

### Крок 2: Розробка ієрархії завдань

Розподіліть роботу на логічні фази із залежностями:

**Приклад: Система автентифікації**
```
Authentication System (parent)
├── 1. Login endpoint (no dependencies)
├── 2. Token refresh (depends on #1)
├── 3. Logout endpoint (depends on #1)
└── 4. Integration tests (depends on #1, #2, #3)
```

### Крок 3: Створення структури завдань

Використовуйте `TaskCreate`, щоб матеріалізувати свій план:

```bash
# Сесія 1: Фаза планування
export CLAUDE_CODE_TASK_LIST_ID="auth-system-v2"
claude

# Всередині сесії Claude:
> "Create a task hierarchy for JWT authentication:

  Parent task: 'Implement JWT authentication system'
  - Description: Add JWT-based auth with refresh tokens and secure storage

  Child tasks:
  1. 'Create login endpoint' (no dependencies)
  2. 'Implement token refresh logic' (depends on task 1)
  3. 'Create logout endpoint' (depends on task 1)
  4. 'Write integration tests' (depends on tasks 1, 2, 3)

  Use TaskCreate with proper metadata."
```

**Очікуваний вивід від Claude:**
```json
{
  "tasks": [
    {
      "id": "task-auth-parent",
      "title": "Implement JWT authentication system",
      "status": "pending",
      "children": ["task-login", "task-refresh", "task-logout", "task-tests"]
    },
    {
      "id": "task-login",
      "title": "Create login endpoint",
      "status": "pending",
      "dependencies": [],
      "metadata": {"priority": "high", "estimated_duration": "2h"}
    },
    {
      "id": "task-refresh",
      "title": "Implement token refresh logic",
      "status": "pending",
      "dependencies": ["task-login"],
      "metadata": {"priority": "high", "estimated_duration": "1h"}
    }
    // ... інші завдання
  ]
}
```

---

## Фаза робочого процесу 2: Виконання завдань

**Мета**: Систематично виконувати завдання з відстеженням прогресу.

### Шаблон виконання

```
TaskList → TaskGet (наступне очікуване) → Виконання → TaskUpdate → Валідація → Повторення
```

### Крок 1: Пошук наступного завдання

```bash
# Сесія 2: Початок реалізації
export CLAUDE_CODE_TASK_LIST_ID="auth-system-v2"
claude

> "TaskList to show all pending tasks"
```

**Вивід:**
```
Tasks for 'auth-system-v2':
✅ task-login: Create login endpoint [completed]
⏳ task-refresh: Implement token refresh logic [pending, blocked by: none]
⏳ task-logout: Create logout endpoint [pending, blocked by: none]
⏳ task-tests: Write integration tests [pending, blocked by: task-refresh, task-logout]
```

### Крок 2: Отримання деталей завдання

```bash
> "TaskGet task-refresh to see full requirements"
```

**Вивід:**
```json
{
  "id": "task-refresh",
  "title": "Implement token refresh logic",
  "description": "Create endpoint POST /auth/refresh that validates refresh token and issues new access token",
  "status": "pending",
  "dependencies": ["task-login"],
  "metadata": {
    "priority": "high",
    "estimated_duration": "1h",
    "files": ["src/auth/refresh.ts", "src/middleware/auth.ts"]
  }
}
```

### Крок 3: Виконання та оновлення

```bash
> "Mark task-refresh as in_progress, then implement the token refresh endpoint according to requirements"

# Claude виконує: TaskUpdate task-refresh status=in_progress
# Claude реалізує функціонал...
# Після завершення:

> "Mark task-refresh as completed"
# Claude виконує: TaskUpdate task-refresh status=completed
```

### Крок 4: Валідація

```bash
> "Run tests for token refresh functionality"

# Якщо тести пройдено:
# ✅ Завдання залишається в статусі completed

# Якщо тести провалено:
> "TaskUpdate task-refresh status=in_progress, add error details to metadata and fix issues"
```

---

## Фаза робочого процесу 3: Керування сесіями

**Мета**: Безперешкодне відновлення роботи між сесіями та межами контексту.

### Механізм збереження даних

**Місце збереження**: `~/.claude/tasks/<task-list-id>/`

Завдання зберігаються попри:
- Завершення сесії
- Стиснення контексту (`/compact`)
- Перезапуск системи
- Перерву в роботі на кілька днів

#### ⚠️ Обмеження видимості полів

**TaskList повертає лише**: `id`, `subject`, `status`, `owner`, `blockedBy`

**Відсутні у виводі TaskList**:
- `description` (потребує виконання TaskGet для кожного завдання)
- `metadata` (кастомні поля, такі як пріоритет, оцінка часу)
- `activeForm` (текст індикатора прогресу)

**Адаптація робочого процесу**:

```bash
# НЕ РЕКОМЕНДУЄТЬСЯ: Намагатися прочитати всі описи через TaskList
TaskList  # Показує лише теми (subjects)

# РЕКОМЕНДУЄТЬСЯ: Отримувати інформацію вибірково
TaskList                    # Отримати огляд (які завдання існують, їхні статуси)
TaskGet(task-auth-login)    # Отримати повні деталі для конкретного завдання
TaskGet(task-auth-tests)    # Отримати деталі для наступного завдання
```

**Коли це має значення**:
- Складні проекти з детальними описами завдань (>50 слів на завдання)
- Координація між кількома агентами, що потребує видимості спільного контексту
- Необхідність швидко переглянути всі нотатки до завдань, щоб визначити точку відновлення роботи

**Усвідомлення вартості (API-виклики)**:
- TaskList = 1 виклик API
- Отримання описів для N завдань = 1 + N викликів
- Для 20 завдань це дає 20-разове збільшення накладних витрат, якщо вам потрібні всі описи

**Способи мінімізації**:
- Використовуйте поле `subject` для критично важливої інформації (яку видно в TaskList)
- Пишіть стислі `description` (максимум 50-100 слів)
- Зберігайте детальні плани у markdown-файлах (`docs/plan-*.md`)

### Шаблон відновлення роботи

```bash
# Через кілька днів, в іншому сеансі терміналу
export CLAUDE_CODE_TASK_LIST_ID="auth-system-v2"
claude

> "TaskList to show current state"

# Вивід показує саме те місце, де ви зупинилися:
# ✅ task-login [completed]
# ✅ task-refresh [completed]
# ⏳ task-logout [pending]
# ⏳ task-tests [pending, blocked by: task-logout]

> "Continue with next pending task that isn't blocked"
```

### Координація в кількох терміналах

**Сценарій використання**: Запуск кількох екземплярів Claude для паралельної роботи над одним проектом

```bash
# Термінал 1: Робота над frontend
export CLAUDE_CODE_TASK_LIST_ID="auth-system-v2"
claude
> "Work on task-logout endpoint"

# Термінал 2: Написання тестів (одночасно)
export CLAUDE_CODE_TASK_LIST_ID="auth-system-v2"
claude
> "TaskList - check what's completed so I can write tests"

# Обидва термінали бачать оновлення стану в реальному часі
```

**⚠️ Попередження**: Використовуйте унікальні ідентифікатори списків завдань для конкретних репозиторіїв, щоб уникнути змішування завдань між різними проектами:
```bash
# ❌ НЕПРАВИЛЬНО: Загальний ID для кількох репозиторіїв
export CLAUDE_CODE_TASK_LIST_ID="my-project"

# ✅ ПРАВИЛЬНО: Специфічний для репозиторію ID з контекстом
export CLAUDE_CODE_TASK_LIST_ID="mycompany-api-auth-refactor"
```

---

## Інтеграція: TDD + Керування завданнями

Поєднуйте розробку через тестування (Test-Driven Development) із відстеженням завдань для систематичного покриття тестами.

### Шаблон: Виконання завдань за принципом «спочатку тести»

```bash
export CLAUDE_CODE_TASK_LIST_ID="tdd-feature-x"
claude

# Створення завдань за підходом "тести спочатку"
> "Create task hierarchy for feature X:

  For each feature component:
  1. Task: 'Write failing tests for [component]'
  2. Task: 'Implement [component] to pass tests' (depends on #1)
  3. Task: 'Refactor [component]' (depends on #2)

  Use TDD red-green-refactor cycle per task."
```

### Приклад: Функція входу (Login) за методологією TDD

```bash
# Фаза 1: Red (тести, що не проходять)
TaskCreate: {
  title: "Write failing tests for login endpoint",
  description: "Test cases: valid credentials, invalid password, user not found, rate limiting",
  status: "pending"
}

# Виконання написання тестів
> "Implement task-login-tests, ensure all tests fail initially"

# Фаза 2: Green (мінімальна реалізація)
TaskCreate: {
  title: "Implement login endpoint (minimal)",
  description: "Make tests pass with simplest possible implementation",
  dependencies: ["task-login-tests"],
  status: "pending"
}

# Фаза 3: Refactor (рефакторинг)
TaskCreate: {
  title: "Refactor login endpoint",
  description: "Optimize, remove duplication, improve readability",
  dependencies: ["task-login-impl"],
  status: "pending"
}
```

**Повний довідник з робочого процесу**: Див. [TDD з Claude](tdd-with-claude.uk.md#інтеграція-з-керуванням-завданнями)

---

## Інтеграція: Планування + Керування завданнями

Перетворюйте стратегічні плани на виконувані ієрархії завдань.

### Шаблон: Перетворення плану на завдання

```bash
# Крок 1: Вхід у режим планування (Plan Mode)
claude
> [Натисніть Shift+Tab для входу в Plan Mode]

# Крок 2: Створення архітектурного плану
> "Design architecture for microservices migration:
  - Identify service boundaries
  - Plan data migration strategy
  - Design API contracts"

# Крок 3: Вихід із режиму планування зі створенням завдань
> "Convert this plan into a task hierarchy using TaskCreate"
```

### Приклад: Міграція на мікросервіси

**Вивід плану:**
```
Phase 1: Analysis (Week 1)
- Map monolith dependencies
- Identify bounded contexts
- Design service boundaries

Phase 2: Infrastructure (Week 2)
- Set up service templates
- Configure API gateway
- Establish monitoring

Phase 3: Migration (Week 3-6)
- Extract user service
- Extract order service
- Migrate database schemas
```

**Перетворення на завдання:**
```bash
TaskCreate: {
  title: "Microservices migration",
  children: [
    {
      title: "Phase 1: Analysis",
      children: [
        {title: "Map monolith dependencies", priority: "critical"},
        {title: "Identify bounded contexts", dependencies: ["map-deps"]},
        {title: "Design service boundaries", dependencies: ["bounded-contexts"]}
      ]
    },
    {
      title: "Phase 2: Infrastructure",
      dependencies: ["phase-1"],
      children: [
        {title: "Set up service templates"},
        {title: "Configure API gateway", dependencies: ["templates"]},
        {title: "Establish monitoring"}
      ]
    }
    // ... Phase 3
  ]
}
```

**Повний довідник з робочого процесу**: Див. [Розробка на основі плану](plan-driven.uk.md#розробка-за-планом)

---

## Посібник із міграції з TodoWrite

### Коли мігрувати

**Залишайтеся на TodoWrite, якщо:**
- ✅ Уся робота завершується за одну сесію
- ✅ Немає потреби в координації кількох агентів
- ✅ Прості лінійні списки завдань (без залежностей)
- ✅ Використовується Claude Code версії < v2.1.16

**Мігруйте на Tasks API, якщо:**
- ✅ Робота триває протягом кількох сесій
- ✅ Потрібно зберігати завдання протягом днів або тижнів
- ✅ Складні графи залежностей
- ✅ Спільна робота в кількох терміналах
- ✅ Бажаєте продовжувати роботу після стиснення контексту

### Кроки міграції

#### Крок 1: Пошук використання TodoWrite

```bash
# Знайдіть наявне використання TodoWrite у вашому CLAUDE.md або робочих процесах
grep -r "TodoWrite" .claude/
```

#### Крок 2: Перетворення списків TodoWrite на завдання (Tasks)

**До (TodoWrite):**
```markdown
- [ ] Implement user authentication
- [ ] Add password hashing
- [ ] Create session management
- [ ] Write tests
```

**Після (Tasks API):**
```bash
export CLAUDE_CODE_TASK_LIST_ID="user-auth-2026"
claude

> "Create tasks:
  1. 'Implement user authentication' (parent)
     - Child: 'Add password hashing'
     - Child: 'Create session management' (depends on hashing)
     - Child: 'Write tests' (depends on auth, hashing, sessions)"
```

#### Крок 3: Оновлення інструкцій у CLAUDE.md

**До:**
```markdown
For complex tasks:
- Use TodoWrite to create task list
- Execute tasks sequentially
```

**Після:**
```markdown
For complex tasks:
- Set CLAUDE_CODE_TASK_LIST_ID=<project-name>
- Use TaskCreate for hierarchical planning
- Execute with TaskUpdate status tracking
- Resume with TaskList in new sessions
```

#### Крок 4: Тестування міграції

```bash
# Створення тестового списку завдань
export CLAUDE_CODE_TASK_LIST_ID="migration-test"
claude

> "Create 3 test tasks with dependencies, mark one completed, then exit"

# Повторний запуск у новій сесії
export CLAUDE_CODE_TASK_LIST_ID="migration-test"
claude

> "TaskList - verify tasks persisted correctly"

# Очікуваний результат: відображення всіх 3 завдань у правильних статусах
```

---

## Шаблони та антишаблони

### ✅ Ефективні шаблони (Good Patterns)

#### 1. Ієрархічна декомпозиція завдань

```bash
Project (parent)
└── Feature A (child of project)
    ├── Component A1 (child of Feature A)
    │   ├── Implementation (leaf task)
    │   └── Tests (leaf task, depends on Implementation)
    └── Component A2
        └── ...
```

**Чому це працює**: Відображає природну структуру проекту, робить залежності явними.

#### 2. Пріоритет залежностей при впорядкуванні

```bash
# Завжди визначайте залежності під час створення завдань
TaskCreate: {
  title: "Deploy to production",
  dependencies: ["run-tests", "code-review", "backup-database"],
  metadata: {blocking_reason: "Safety checks required"}
}
```

**Чому це працює**: Запобігає передчасному виконанню та забезпечує дотримання критеріїв якості.

#### 3. Детальні оновлення статусу

```bash
# Неправильно: велике завдання позначається як виконане без проміжних статусів
TaskCreate: {title: "Build entire auth system"}
# ... години потому ...
TaskUpdate: {id: "auth-system", status: "completed"}

# Правильно: регулярні оновлення статусу в міру просування роботи
TaskUpdate: {id: "auth-system", status: "in_progress", progress: "25%"}
TaskUpdate: {id: "auth-system", status: "in_progress", progress: "50%"}
TaskUpdate: {id: "auth-system", status: "in_progress", progress: "75%"}
TaskUpdate: {id: "auth-system", status: "completed"}
```

**Чому це працює**: Забезпечує видимість прогресу та полегшує відновлення роботи з правильного місця.

#### 4. Завдання з багатими метаданими

```bash
TaskCreate: {
  title: "Optimize database queries",
  description: "Reduce query time for user dashboard from 2s to <200ms",
  metadata: {
    priority: "high",
    estimated_duration: "3h",
    related_files: ["src/db/queries.ts", "src/db/indexes.sql"],
    performance_baseline: "2000ms",
    performance_target: "200ms",
    related_issue: "https://github.com/org/repo/issues/123"
  }
}
```

**Чому це працює**: Забезпечує насичений контекст для продовження роботи, полегшує делегування та покращує документування.

### ❌ Антишаблони (Anti-Patterns)

#### 1. Монолітні завдання (>10 кроків)

```bash
# ❌ НЕПРАВИЛЬНО: Завдання занадто велике, важко відстежувати прогрес
TaskCreate: {
  title: "Implement entire payment system",
  description: "Stripe integration, webhooks, refunds, disputes, reporting, admin UI, ..."
}

# ✅ ПРАВИЛЬНО: Розподіл на фази
TaskCreate: {
  title: "Payment system - Phase 1: Core integration",
  children: [
    {title: "Stripe SDK setup"},
    {title: "Payment intent creation"},
    {title: "Webhook handling"}
  ]
}
```

#### 2. Відсутність залежностей

```bash
# ❌ НЕПРАВИЛЬНО: Завдання можуть виконуватися у неправильному порядку
TaskCreate: {title: "Deploy to production"} # Немає залежностей
TaskCreate: {title: "Write tests"} # Немає залежностей

# ✅ ПРАВИЛЬНО: Явне впорядкування
TaskCreate: {
  title: "Deploy to production",
  dependencies: ["write-tests", "run-tests", "code-review"]
}
```

#### 3. «Сирітські» завдання без контексту

```bash
# ❌ НЕПРАВИЛЬНО: У майбутньому ви не згадаєте, про що йшлося
TaskCreate: {
  title: "Fix the bug",
  description: "That one from yesterday"
}

# ✅ ПРАВИЛЬНО: Самодостатній контекст
TaskCreate: {
  title: "Fix login timeout on Safari",
  description: "Users on Safari 17.2+ experience session timeout after 5min. Expected: 30min timeout. Root cause: cookie SameSite=Strict not supported.",
  metadata: {
    browser: "Safari 17.2+",
    error_message: "Session expired",
    related_commit: "a1b2c3d",
    slack_thread: "https://slack.com/archives/C123/p456"
  }
}
```

#### 4. Невідповідність статусу

```bash
# ❌ НЕПРАВИЛЬНО: Завдання позначено як виконане, хоча тести не проходять
TaskUpdate: {id: "login-feature", status: "completed"}
# Тести запускаються пізніше: 3 помилки

# ✅ ПРАВИЛЬНО: Перевірка перед завершенням
> "Run tests for login feature"
# Якщо тести пройдено:
TaskUpdate: {id: "login-feature", status: "completed", metadata: {test_results: "pass"}}
# Якщо тести провалено:
TaskUpdate: {id: "login-feature", status: "in_progress", metadata: {test_results: "3 failures", error_log: "..."}}
```

---

## Усунення несправностей

### Питання: Завдання не зберігаються між сесіями

**Симптом**: `TaskList` виявляється порожнім після перезапуску Claude.

**Рішення**:
```bash
# Переконайтеся, що CLAUDE_CODE_TASK_LIST_ID встановлено перед запуском
export CLAUDE_CODE_TASK_LIST_ID="your-project-name"
claude

# Перевірте, чи існує каталог збереження
ls ~/.claude/tasks/your-project-name/
```

### Питання: Кілька проектів спільно використовують списки завдань

**Симптом**: Відображення завдань із проекту А під час роботи над проектом Б.

**Причина**: Використання однакового ідентифікатора списку завдань (task list ID) у різних репозиторіях.

**Рішення**:
```bash
# Використовуйте специфічні для репозиторію ID з контекстом
cd ~/projects/api
export CLAUDE_CODE_TASK_LIST_ID="api-v2-migration"
claude

cd ~/projects/frontend
export CLAUDE_CODE_TASK_LIST_ID="frontend-redesign"
claude
```

### Питання: TodoWrite все ще використовується замість Tasks API

**Симптом**: Завдання не зберігаються навіть із встановленим ID списку завдань.

**Причина**: У середовищі встановлено `CLAUDE_CODE_ENABLE_TASKS=false`.

**Рішення**:
```bash
# Перевірте оточення
env | grep CLAUDE_CODE_ENABLE_TASKS

# Видаліть змінну, якщо вона присутня
unset CLAUDE_CODE_ENABLE_TASKS

# Або увімкніть систему явно (у версіях v2.1.19+ увімкнено за замовчуванням)
export CLAUDE_CODE_ENABLE_TASKS=true
```

### Питання: Залежності завдань не враховуються

**Симптом**: Claude виконує заблоковані завдання до завершення їхніх залежностей.

**Причина**: Залежності неправильно описані в TaskCreate.

**Рішення**:
```bash
# Переконайтеся, що залежності використовують правильні ID завдань
TaskCreate: {
  title: "Task B",
  dependencies: ["task-a-id"], # ✅ Використовуйте фактичний ID завдання
  # NOT dependencies: ["Task A"] # ❌ Назва завдання не спрацює
}

# Перевірте залежності:
TaskGet task-b-id
# Повинно містити: "blockedBy": ["task-a-id"]
```

---

## Розширене використання: кастомні метадані завдань

Додавайте специфічні для предметної області метадані для вдосконалення робочих процесів.

### Угоди щодо метаданих

**Завдання з оптимізації продуктивності:**
```json
{
  "metadata": {
    "type": "performance",
    "baseline_metric": "2000ms",
    "target_metric": "200ms",
    "profiling_tool": "Chrome DevTools",
    "measurement_location": "dashboard load time"
  }
}
```

**Завдання з безпеки:**
```json
{
  "metadata": {
    "type": "security",
    "severity": "critical",
    "cve_id": "CVE-2024-1234",
    "affected_versions": "< 2.1.0",
    "mitigation": "Update package X to v3.0+"
  }
}
```

**Завдання з виправлення багів:**
```json
{
  "metadata": {
    "type": "bugfix",
    "issue_url": "https://github.com/org/repo/issues/456",
    "reported_by": "user@example.com",
    "reproduction_steps": "1. Login 2. Navigate to dashboard 3. Click export",
    "error_message": "TypeError: Cannot read property 'map' of undefined"
  }
}
```

### Фільтрування за метаданими

```bash
# Фільтрування завдань за типом (потребує написання скрипта, не є вбудованою функцією)
TaskList | jq '.tasks[] | select(.metadata.type == "security")'

# Пошук очікуваних завдань із високим пріоритетом
TaskList | jq '.tasks[] | select(.metadata.priority == "high" and .status == "pending")'
```

---

## Протокол життєвого циклу сесії

Кожна сесія агента слідує одній і тій самій послідовності з десяти кроків: від запуску до коміту. Явне визначення цих кроків, а не залишення їх неявними, — це те, що робить сесії надійно відновлюваними після переривання. Інженерна команда Anthropic спостерігала це безпосередньо: в експерименті з редактором ігор звичайний запуск Claude зазнав невдачі на півдорозі, тоді як те саме навантаження, загорнуте в структуровану оболонку сесії, було успішно завершене (джерело: [Anthropic Engineering Blog](https://www.anthropic.com/engineering/harness-design-long-running-apps)).

| Крок | Дія | Артефакт |
|------|--------|----------|
| START | Читання інструкцій проекту | `AGENTS.md` або `CLAUDE.md` |
| INIT | Запуск скрипта ініціалізації середовища | `init.sh` / `npm install && npm run check` |
| READ | Завантаження стану попередньої сесії | `progress.md` |
| SELECT | Вибір однієї функції, активація статусу | `feature_list.json` |
| EXECUTE | Реалізація виключно цієї функції | Вихідні файли |
| VERIFY | Запуск трирівневої верифікації (лінтинг, тести, e2e) | Коди виходу (exit codes) |
| WRAP UP | Запис завершення та доказів | `progress.md`, `feature_list.json` |
| CLEANUP | Видалення тимчасових файлів, перевірка чистоти репозиторію | Стан репозиторію |
| COMMIT | Фіксація межі сесії в git | Історія Git |
| HANDOFF | Запис або оновлення звіту про передачу роботи | `claudedocs/handoffs/` |

### Артефакт безперервності: `progress.md`

`progress.md` — це компактна відправна точка для наступної сесії. Він фіксує активну функцію, переглянуту ревізію, блокери та наступну дію. Документ передачі роботи може містити більше контексту: рішення, критерії приймання, докази та відповідальних. Обидва артефакти можуть слугувати і людині, і агентові. Обирайте за потрібною інформацією, а не за жорстким розподілом аудиторій.

```markdown
# Session Progress

last_updated: 2026-05-04
active_feature: feat-002
last_commit: a3f92c1
session_count: 3

## Status
- feat-001: passing (verified 2026-05-01)
- feat-002: active (in progress)
- feat-003: not_started

## Next action
Finish chunking implementation, then run: npm test -- --grep 'chunking'

## Blockers
None
```

На кроці READ використовуйте його як шлях до завдання, а потім перевірте актуальний стан і чинні дозволи, перш ніж діяти. Записані коміт і статус — це історичні твердження: вони не доводять, що тести досі проходять, і не означають, що попередню зовнішню дію слід повторювати.

### Як це узгоджується з тріадою передачі роботи

Тріада передачі роботи (створити, відновити, оновити) та `progress.md` можуть співіснувати, якщо їхні ролі чіткі: компактний покажчик і повніший контракт. Оберіть авторитетного власника для кожного факту та посилайтеся на нього з похідних підсумків. Сам по собі запис обох артефактів на кроці WRAP UP не запобігає розбіжностям. Під час відновлення звірте ревізію, докази приймання, блокери та наступного власника. Див. [передачі роботи між двома інстансами](dual-instance-planning.uk.md#шаблон-плану) і [контракти між сесіями](cross-session-messaging.uk.md).

### Крок COMMIT як межа сесії

Коміт на кроці COMMIT — це не просто операція VCS. Це твердження того, що репозиторій перебуває в стані, придатному для перезапуску. Правило таке ж, як і в тріаді передачі роботи: комітьте лише тоді, коли функція повністю завершена та верифікована. Наполовину реалізована функція, залишена в неробочому стані, означає, що наступна сесія почнеться зі зламаного середовища, і крок `npm run check` на етапі INIT одразу зазнає невдачі, виявивши проблему перед початком будь-якої нової роботи. Ця невдача є інформативною, але краще запобігти їй, відклавши коміт до успішного завершення кроку VERIFY.

Про режим збою, який виникає у разі пропуску кроку VERIFY, див. розділ «Розрив верифікації» в [TDD з Claude](tdd-with-claude.uk.md#розрив-верифікації-the-verification-gap).

---

## Пов'язані робочі процеси

- **[TDD з Claude](tdd-with-claude.uk.md)** — розробка через тестування з відстеженням завдань
- **[Розробка на основі плану](plan-driven.uk.md)** — від стратегічного планування до ієрархій завдань
- **[Ітеративне вдосконалення](iterative-refinement.uk.md)** — поетапні покращення за допомогою завдань
- **[Дослідницький робочий процес](exploration-workflow.uk.md)** — фаза дослідження перед створенням завдань

---

## Довідкові матеріали

**Документація інструменту**: Див. розділ [Ultimate Guide Section 5.X](#task-management-system)

**Джерела:**
- Офіційне: [Claude Code CHANGELOG v2.1.16](https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md)
- Офіційне: [System Prompts - TaskCreate](https://github.com/Piebald-AI/claude-code-system-prompts)
- Спільнота: [paddo.dev - From Beads to Tasks](https://paddo.dev/blog/from-beads-to-tasks/)
- Спільнота: [llbbl.blog - Two Changes in Claude Code](https://llbbl.blog/2026/01/25/two-changes-in-claude-code.html)

**Відстеження версій**: Цей посібник описує роботу з Claude Code v2.1.16+ (випущено 2026-01-22). Перевіряйте останні зміни в [claude-code-releases.yaml](../../machine-readable/claude-code-releases.yaml).

---
**Локалізація**: [Serhii (MacPlus Software)](https://macplus-software.com)
*Остання синхронізація: Травень 2026*
