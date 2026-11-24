---
title: "Майстерність інструментів пошуку: поєднання rg, grepai, Serena, ast-grep, scip-search та lilmd"
description: "Опануйте пошук у коді та навігацію документацією, поєднуючи правильні інструменти для максимальної ефективності"
tags: [workflow, search, guide, mcp]
---

# Майстерність інструментів пошуку: поєднання rg, grepai, Serena, ast-grep, scip-search та lilmd

> **Опануйте пошук у коді та навігацію документацією, поєднуючи правильні інструменти для максимальної ефективності**

**Автор**: Florian BRUNIAUX | Внесок від Claude (Anthropic)
**Час читання**: ~25 хвилин
**Останнє оновлення**: Травень 2026

---

## Зміст

1. [Швидка довідкова матриця](#швидка-довідкова-матриця)
2. [Порівняння інструментів](#порівняння-інструментів)
3. [Дерево прийняття рішень](#дерево-прийняття-рішень)
4. [Комбіновані робочі процеси](#комбіновані-робочі-процеси)
5. [Реальні сценарії використання](#реальні-сценарії-використання)
6. [Оптимізація продуктивності](#оптимізація-продуктивності)
7. [Поширені помилки](#поширені-помилки)
8. [Розширений набір інструментів: scip-search та lilmd](#розширений-набір-інструментів-scip-search-та-lilmd)

---

## Швидка довідкова матриця

| Мені потрібно... | Використовуйте цей інструмент | Приклад команди |
|--------------|---------------|-----------------|
| Знайти точний текст | `rg` (інструмент Grep) | `rg "authenticate" --type ts` |
| Знайти за змістом | `grepai` | `grepai search "user login flow"` |
| Знайти визначення функції | `Serena` | `serena find_symbol --name "login"` |
| Знайти структурний патерн | `ast-grep` | `ast-grep "async function $F"` |
| Подивитися, хто викликає функцію | `grepai` | `grepai trace callers "login"` |
| Отримати структуру файлу | `Serena` | `serena get_symbols_overview` |
| Рефакторинг у багатьох файлах | `Serena + ast-grep` | Комбінований робочий процес |
| Дослідити невідому кодову базу | `grepai → Serena` | Патерн виявлення |
| Знайти посилання на символ без MCP (безпечно для worktree) | `scip-search` | `scip-search refs AuthService.login` |
| Орієнтуватися у великому документі Markdown | `lilmd` | `lilmd read docs/arch.md "Authentication"` |

---

## Порівняння інструментів

### Повна матриця характеристик

| Характеристика | rg (ripgrep) | grepai | Serena | ast-grep |
|---------|--------------|--------|--------|----------|
| **Тип пошуку** | Регулярні вирази/текст | Семантичний (за змістом) | З урахуванням символів (Symbol-aware) | Структура AST |
| **Технологія** | Співставлення патернів | Векторні представлення (Ollama) | Парсинг символів | Абстрактне синтаксичне дерево (AST) |
| **Швидкість** | ⚡ ~20ms | 🐢 ~500ms | ⚡ ~100ms | 🕐 ~200ms |
| **Налаштування** | ✅ Немає (вбудовано) | ⚠️ Ollama + встановлення | ⚠️ MCP конфігурація | ⚠️ npm встановлення |
| **Інтеграція** | ✅ Нативна (`Grep`) | ⚠️ MCP сервер | ⚠️ MCP сервер | ⚠️ Плагін |
| **Конфіденційність** | ✅ 100% локально | ✅ 100% локально | ✅ 100% локально | ✅ 100% локально |
| **Необхідний контекст** | Немає | Немає | Індексація проєкту | Немає |
| **Мови** | Усі (текст) | Усі | TS/JS/Py/Rust/Go | TS/JS/Py/Rust/Go/C++ |
| **Граф викликів** | ❌ Ні | ✅ Так | ❌ Ні | ❌ Ні |
| **Відстеження символів** | ❌ Ні | ❌ Ні | ✅ Так | ❌ Ні |
| **Пам'ять сесії** | ❌ Ні | ❌ Ні | ✅ Так | ❌ Ні |
| **Хибні спрацьовування** | Середній рівень | Низький рівень | Дуже низький | Дуже низький |
| **Складність вивчення** | Низька | Середня | Низька | Висока |

### Порівняння витрат токенів

| Інструмент | Типовий запит | Витрачено токенів | Повернуто результатів |
|------|---------------|-----------------|------------------|
| **rg** | "authenticate" | ~500 | Тільки точні збіги |
| **grepai** | "auth flow" | ~2000 | Збіги на основі наміру |
| **Serena** | find_symbol | ~1000 | Символ + контекст |
| **ast-grep** | AST pattern | ~1500 | Структурні збіги |

**Ключовий висновок**: `rg` у 4 рази ефективніший за витратами токенів, але в 10 разів менш «інтелектуальний» порівняно з семантичними інструментами.

### Розширений довідник інструментів

Два інструменти, що закривають прогалини в базовому наборі, детально розглянуто в [розділі «Розширений набір інструментів»](#розширений-набір-інструментів-scip-search-та-lilmd):

| Інструмент | Категорія | Порівняно з наявним набором |
|------|----------|-------------------|
| **scip-search** | Пошук за індексом символів (SCIP) | Як Serena, але без стану, без MCP, безпечний для worktree |
| **lilmd** | Навігація за розділами Markdown | Аналога в наборі немає (працює з документацією, а не з кодом) |

---

## Дерево прийняття рішень

### Level 1: What Do You Know?

```
Do you know the EXACT text/pattern?
│
├─ YES → Use rg (ripgrep)
│  ├─ Known function name: rg "createSession"
│  ├─ Known import: rg "import.*React"
│  └─ Known pattern: rg "async function"
│
└─ NO → Go to Level 2
```

### Level 2: What Are You Looking For?

```
What's your search intent?
│
├─ "Find by MEANING/CONCEPT"
│  → Use grepai
│  └─ Example: grepai search "payment validation logic"
│
├─ "Find FUNCTION/CLASS definition"
│  → Use Serena
│  └─ Example: serena find_symbol --name "UserController"
│
├─ "Find by CODE STRUCTURE"
│  → Use ast-grep
│  └─ Example: async without error handling
│
└─ "Understand DEPENDENCIES"
   → Use grepai trace
   └─ Example: grepai trace callers "validatePayment"
```

### Level 2 (worktree / no MCP)

Коли ви працюєте в середовищі CI, у git worktree або в будь-якому контексті, де сервери MCP недоступні:

```
Known symbol name, no MCP available?
│
└─ Use scip-search (pre-built SCIP index, millisecond cold start)
   └─ scip-search refs "AuthService.login" --format json
```

### Level 3: Optimization

```
Found too many results?
│
├─ rg → Add --type filter or narrow path
├─ grepai → Add --path filter or use trace
├─ Serena → Filter by symbol type (function/class)
└─ ast-grep → Add constraints to pattern
```

---

## Комбіновані робочі процеси

### Робочий процес 1: Дослідження невідомої кодової бази

**Мета**: швидко розібратися в новому проєкті.

**Покроковий опис**:

```bash
# 1. SEMANTIC DISCOVERY (grepai)
# Find files related to authentication
grepai search "user authentication and session management"
# → Output: auth.service.ts, session.middleware.ts, user.controller.ts

# 2. STRUCTURAL OVERVIEW (Serena)
# Understand each file's structure
serena get_symbols_overview --file auth.service.ts
# → Output:
#   - class AuthService
#     - login(email, password)
#     - logout(sessionId)
#     - validateSession(token)

# 3. DEPENDENCY MAPPING (grepai trace)
# See how login is used
grepai trace callers "login"
# → Output: Called by UserController, ApiGateway, AdminPanel

# 4. EXACT SEARCH (rg)
# Find specific implementation details
rg "validateSession" --type ts -A 5
# → Output: Full function with 5 lines of context
```

**Результат**: повне розуміння системи за 4 команди (замість читання понад 30 файлів).

---

### Робочий процес 2: Великомасштабний рефакторинг

**Мета**: перейменувати `createSession` → `initializeUserSession` у понад 50 файлах.

**Покроковий опис**:

```bash
# 1. IMPACT ANALYSIS (grepai trace)
# Understand full scope
grepai trace callers "createSession"
# → Output: 47 callers across 23 files
grepai trace callees "createSession"
# → Output: Calls validateUser, createToken, storeSession

# 2. STRUCTURAL VALIDATION (ast-grep)
# Ensure consistent usage pattern
ast-grep "createSession($$$ARGS)"
# → Output: All invocations with their argument patterns

# 3. SYMBOL-AWARE REFACTORING (Serena)
# Precise renaming
serena find_symbol --name "createSession" --include-body true
# → Get exact definition + all references

serena replace_symbol_body \
  --name "createSession" \
  --new-name "initializeUserSession"
# → Rename across all files maintaining structure

# 4. VERIFICATION (rg)
# Confirm no old references remain
rg "createSession" --type ts
# → Should return 0 results
```

**Результат**: безпечний рефакторинг із повним урахуванням залежностей.

---

### Робочий процес 3: Аудит безпеки

**Мета**: знайти вразливості безпеки.

**Покроковий опис**:

```bash
# 1. SEMANTIC DISCOVERY (grepai)
# Find security-sensitive code
grepai search "SQL query construction"
grepai search "user input validation"
grepai search "password handling"

# 2. STRUCTURAL PATTERNS (ast-grep)
# Find specific vulnerability patterns

# SQL injection risks
ast-grep 'db.query(`${$VAR}`)'

# XSS risks
ast-grep 'innerHTML = $VAR'

# Missing error handling
ast-grep -p 'async function $F($$$) { $$$BODY }' \
  --without 'try { $$$TRY } catch'

# 3. DEPENDENCY TRACING (grepai)
# See where vulnerable code is called
grepai trace callers "executeQuery"
# → Identify all entry points

# 4. EXACT VERIFICATION (rg)
# Confirm findings
rg "innerHTML\s*=" --type ts
rg "password" --type ts | rg -v "hashed"
```

**Результат**: всебічний аудит безпеки за лічені хвилини.

---

## Реальні тести продуктивності

### grepai порівняно з grep (Січень 2026)

**Контекст**: Тест продуктивності на Excalidraw (155 тис. рядків TypeScript)
**Автор**: YoanDev (розробник grepai — можлива упередженість)
**Методологія**: 5 однакових запитань для пошуку та дослідження коду

| Метрика | grep | grepai | Різниця |
|----------|------|--------|------------|
| Виклики інструментів | 139 | 62 | **-55%** |
| Вхідні токени | 51k | 1.3k | **-97%** |

**Основний висновок**: семантичний пошук радикально зменшує кількість токенів, оскільки виявляє релевантні файли з першої спроби, уникаючи ітераційного дослідження.

**Обмеження**:
- Тест проведено автором інструменту.
- Валідація лише на одному проєкті (тільки TypeScript).
- Наразі немає незалежних підтверджених результатів тестування.

**Джерело**: [yoandev.co/grepai-benchmark](https://yoandev.co/grepai-benchmark)

> **Примітка**: цей тест відображає стан продуктивності на січень 2026 року. Показники можуть змінюватися з оновленнями Claude Code та grepai.

---

### Робочий процес 4: Міграція фреймворку

**Мета**: мігрувати класові компоненти React → hooks.

**Покроковий опис**:

```bash
# 1. INVENTORY (ast-grep)
# Find all class components
ast-grep 'class $C extends React.Component'
# → Output: 34 components to migrate

# 2. DEPENDENCY ANALYSIS (grepai)
# Understand component relationships
for component in $(ast-grep 'class $C extends' --json | jq -r '.[].name'); do
  grepai trace callers "$component"
done
# → Build migration order (leaf components first)

# 3. PATTERN DETECTION (ast-grep)
# Identify lifecycle methods used
ast-grep 'componentDidMount() { $$$BODY }'
ast-grep 'componentWillReceiveProps($$$) { $$$BODY }'
# → Map to equivalent hooks

# 4. INCREMENTAL MIGRATION (Serena + ast-grep)
# Migrate one component at a time
serena find_symbol --name "UserProfile" --include-body true
# → Get full component code

# Use ast-grep to transform
ast-grep --rewrite \
  --from 'class $C extends React.Component' \
  --to 'const $C = () => { }'

# 5. VERIFICATION (rg + grepai)
# Ensure migration successful
rg "React.Component" --type tsx  # Should decrease
grepai search "component lifecycle methods"  # Find any missed
```

**Результат**: систематична міграція з мінімальним ризиком порушення працездатності.

---

### Робочий процес 5: Оптимізація продуктивності

**Мета**: виявити та усунути вузькі місця продуктивності.

**Покроковий опис**:

```bash
# 1. HOTSPOT DISCOVERY (grepai)
# Find performance-critical code
grepai search "heavy computation or loops"
grepai search "database queries in loops"

# 2. PATTERN DETECTION (ast-grep)
# Find N+1 query patterns
ast-grep 'for ($$$) { await db.query($$$) }'

# Find missing memoization
ast-grep 'useMemo' --invert-match \
  --in 'const $VAR = $$$'

# 3. CALL GRAPH ANALYSIS (grepai trace)
# Find hot paths
grepai trace graph "renderUserList" --depth 3
# → Visualize dependency tree

# 4. SYMBOL TRACKING (Serena)
# Track function changes
serena write_memory "perf_baseline" \
  "renderUserList: 450ms avg"

# After optimization
serena write_memory "perf_optimized" \
  "renderUserList: 45ms avg (10x improvement)"

# 5. VERIFICATION (rg)
# Confirm optimizations applied
rg "useMemo|useCallback" --type tsx
```

**Результат**: покращення продуктивності на основі точних даних.

---

## Реальні сценарії використання

### Сценарій 1: «Я не знаю, що саме шукаю»

**Проблема**: новий проєкт, документація відсутня, потрібно додати нову функцію.

**Рішення**: спочатку семантичне дослідження.

```bash
# Start broad with meaning
grepai search "user profile management"
# → Discover relevant files

# Then narrow with structure
serena get_symbols_overview --file user-profile.service.ts
# → Understand available functions

# Finally, exact search for details
rg "updateProfile" --type ts -C 3
```

---

### Сценарій 2: «Ця функція викликається звідусіль»

**Проблема**: потрібно змінити функцію, але є побоювання зламати інші частини системи.

**Рішення**: спочатку складання карти залежностей.

```bash
# 1. See all callers
grepai trace callers "calculateTotal"
# → 47 callers found

# 2. Analyze caller contexts
for file in $(grepai trace callers "calculateTotal" --json | jq -r '.[].file'); do
  serena get_symbols_overview --file "$file"
done

# 3. Identify safe vs risky call sites
ast-grep 'calculateTotal($ARGS)' --json
# → Group by argument patterns

# 4. Make change with confidence
# Now you know all impact points
```

---

### Сценарій 3: «Знайти весь код, який робить X»

**Проблема**: потрібно застосувати однаковий патерн по всій кодовій базі.

**Рішення**: поєднання семантичного та структурного пошуку.

```bash
# Example: Find all error handling code

# 1. Semantic discovery
grepai search "error handling and exception management"

# 2. Structural patterns
ast-grep 'try { $$$TRY } catch ($ERR) { $$$CATCH }'
ast-grep 'throw new Error($MSG)'

# 3. Verify consistency
rg "catch\s*\(" --type ts | wc -l
# Compare with ast-grep count to find anomalies
```

---

### Сценарій 4: «Мені потрібно розібратися в цьому модулі»

**Проблема**: складний модуль із незрозумілими зонами відповідальності.

**Рішення**: багатоінструментальний аналіз.

```bash
# 1. Get symbol overview (Serena)
serena get_symbols_overview --file payment.module.ts
# → See all exports, classes, functions

# 2. Understand dependencies (grepai)
grepai trace callees "PaymentModule"
# → What does this module use?

grepai trace callers "PaymentModule"
# → Who uses this module?

# 3. Find implementation patterns (ast-grep)
ast-grep 'export class $C' --file payment.module.ts
ast-grep 'async $METHOD($$$)' --file payment.module.ts

# 4. Read specific implementations (rg)
rg "processPayment" --type ts -A 20
```

---

## Оптимізація продуктивності

### Вибір найшвидшого інструменту

**Загальні правила**:

1. **Відомий точний текст** → Завжди використовуйте `rg` у першу чергу.
2. **Невідомий точний текст** → Використовуйте `grepai`, потім `rg` для перевірки.
3. **Рефакторинг** → `Serena` для безпечної роботи із символами.
4. **Масштабні міграції** → `ast-grep` для структурної точності.

### Тести продуктивності

**Завдання**: знайти код авторизації в кодовій базі на 500 тис. рядків.

| Стратегія | Час | Якість результатів |
|----------|------|-----------------|
| Тільки `rg "auth"` | 0.2s | понад 5000 хибнопозитивних збігів |
| Тільки `grepai "auth"` | 2.5s | 50 релевантних результатів |
| `grepai → rg` (комбіновано) | 2.7s | 50 релевантних, перевірених результатів |
| Тільки символи `Serena` | 1.5s | 12 функцій авторизації |
| Патерни `ast-grep` | 3.0s | 8 потоків авторизації |

**Переможець**: символи `Serena` (найшвидше + найвища якість) для відомих назв функцій.

### Стратегія паралелізації

**Для великих кодових баз (>100 тис. рядків)**:

```bash
# Run searches in parallel

# Terminal 1: Semantic discovery
grepai search "authentication flow" > /tmp/grepai-results.json &

# Terminal 2: Symbol indexing
serena get_symbols_overview --file src/**/*.ts > /tmp/symbols.json &

# Terminal 3: Pattern detection
ast-grep 'async function $F' --json > /tmp/ast-results.json &

# Wait for all, then combine results
wait
jq -s '.[0] + .[1] + .[2]' \
  /tmp/grepai-results.json \
  /tmp/symbols.json \
  /tmp/ast-results.json
```

---

## Поширені помилки

### Помилка 1: Використання семантичного пошуку для точних збігів

❌ **Неправильно**:
```bash
grepai search "createSession"  # Slow, overkill
```

✅ **Правильно**:
```bash
rg "createSession" --type ts  # Fast, precise
```

**Правило**: якщо ви знаєте точний текст, ніколи не використовуйте семантичний пошук.

---

### Помилка 2: Використання rg для концептуального пошуку

❌ **Неправильно**:
```bash
rg "auth.*login.*session" --type ts  # Misses variations
```

✅ **Правильно**:
```bash
grepai search "authentication and session management"
```

**Правило**: регулярні вирази не розуміють значення, використовуйте семантичні інструменти.

---

### Помилка 3: Ігнорування графу викликів перед рефакторингом

❌ **Неправильно**:
```bash
# Directly refactor without checking callers
rg "oldFunction" --type ts | sed 's/oldFunction/newFunction/g'
```

✅ **Правильно**:
```bash
# Check impact first
grepai trace callers "oldFunction"
# See 47 callers across 23 files
# Then plan refactoring strategy
```

**Правило**: завжди відстежуйте залежності перед зміною спільного коду.

---

### Помилка 4: Відсутність комбінування інструментів

❌ **Неправильно**:
```bash
# Use only one tool for complex task
ast-grep 'async function $F' --json | jq '.[].file' | xargs -I {} vim {}
# Blindly edit without understanding context
```

✅ **Правильно**:
```bash
# Combine for full understanding
ast-grep 'async function $F' --json > /tmp/async.json
for file in $(jq -r '.[].file' /tmp/async.json); do
  serena get_symbols_overview --file "$file"  # Context
  grepai trace callers "$(jq -r '.[].name' /tmp/async.json)"  # Usage
done
```

**Правило**: складні завдання потребують кількох різних точок зору.

---

### Помилка 5: Надмірне ускладнення простих пошукових запитів

❌ **Неправильно**:
```bash
# Setup grepai + Ollama just to find a TODO comment
grepai search "TODO comments in the code"
```

✅ **Правильно**:
```bash
rg "TODO" --type ts
```

**Правило**: використовуйте найпростіший інструмент, який вирішує завдання.

---

## Шпаргалка з вибору інструментів

### Швидка матриця прийняття рішень

| Ваша ситуація | Використовуйте це | НЕ це |
|----------------|----------|----------|
| «Знайти функцію `login`» | `rg "login"` | `grepai search "login"` |
| «Знайти код, пов'язаний з логіном» | `grepai "login flow"` | `rg "login.*"` |
| «Безпечно перейменувати функцію» | `serena find_symbol` | `rg + sed` |
| «Хто викликає цю функцію?» | `grepai trace callers` | `rg + grep` |
| «Отримати структуру файлу» | `serena overview` | `rg "class\|function"` |
| «Знайти асинхронні функції без try/catch» | `ast-grep` | `rg "async.*{"` |
| «Міграція класів React» | `ast-grep` | `rg` + вручну |
| «Знайти коментарі TODO» | `rg "TODO"` | Будь-який інший інструмент |

---

## Розширений набір інструментів: scip-search та lilmd

Два CLI-інструменти, що закривають прогалини в наборі rg/grepai/Serena.

### scip-search

scip-search виконує запити до заздалегідь побудованих індексів символів SCIP (Sourcegraph Code Intelligence Protocol). Якщо grepai шукає за семантичним змістом, а Serena вимагає живого з'єднання MCP, то scip-search працює зі статичним бінарним індексом із холодним стартом за мілісекунди.

| Атрибут | Деталі |
|-----------|---------|
| **Джерело** | [github.com/liza-mas/scip-search](https://github.com/liza-mas/scip-search) |
| **Встановлення** | `curl -fsSL https://raw.githubusercontent.com/liza-mas/scip-search/main/install.sh \| bash` |
| **Формат індексу** | SCIP (Go, TypeScript, Python, Java, Rust та інші) |
| **Вивід** | Однорядковий текст, JSON або лише розташування |

**Робочий процес**: scip-search замінює 5-10 звернень rg/read, типових для пошуку символу.

```bash
# Step 1: generate SCIP index once per language
scip-typescript index --output index.scip

# Step 2: find a symbol definition
scip-search find AuthService

# Step 3: get all references with line numbers
scip-search refs AuthService.login --format json

# Step 4: read only the returned line ranges
```

**Порівняно з Serena**: Serena підключається до language server і має пам'ять сесії. scip-search не має стану й працює зі знімком: без MCP, без постійного процесу. Тому він надійний у worktree та в ефемерних середовищах CI, де LSP-бекенд Serena може бути недоступним.

**Порівняно з grepai**: grepai знаходить за семантичним наміром («логіка валідації платежів»). scip-search знаходить за точним або майже точним ідентифікатором символу. Вони працюють послідовно: grepai відкриває поняття, scip-search підтверджує символ.

**Сумісність із worktree**: індекси є файлами окремого репозиторію без спільного стану. Запуск `scip-typescript index` усередині worktree створює локальний індекс для цього worktree.

---

### lilmd

lilmd розглядає файли Markdown як бази даних. Він повертає зміст із діапазонами рядків і дає змогу читати окремі розділи. Agent, що читає посібник на 2000 рядків, отримує один розділ одним викликом замість читання всього файлу.

| Атрибут | Деталі |
|-----------|---------|
| **Джерело** | [github.com/molefrog/lilmd](https://github.com/molefrog/lilmd) |
| **Встановлення** | `npm install -g lilmd` |
| **Середовище виконання** | Node або Bun |

**Ключові команди**:

```bash
# TOC with line ranges (inclusive, 1-indexed)
lilmd docs/architecture.md

# Read a section by name (fuzzy match by default)
lilmd read docs/architecture.md "Authentication"

# Read a nested section
lilmd read docs/architecture.md "Security > JWT"

# Exact match (prefix with =)
lilmd read docs/architecture.md "=Authentication Flow"
```

**Цінність для agent**: вивід змісту містить діапазони рядків для кожного заголовка. Agent розбирає їх і запитує лише потрібний розділ замість завантаження всього файлу. Природний конвеєр: `rg` (знайти файл), потім `lilmd` (отримати зміст із діапазонами), потім `Read lines:N-M` (завантажити конкретний розділ). Це працює також для CHANGELOG.md, великих файлів README та документів бази знань.

**Сумісність із worktree**: без стану й індексу, працює окремо для кожного файлу. Підходить будь-де.

---

## Пріоритет налаштування

**Рекомендований порядок налаштування**:

1. **Початок**: `rg` (вже вбудований в інструмент `Grep`) ✅
2. **Далі**: `Serena` MCP (розуміння символів, пам'ять сесії)
3. **Потім**: `grepai` (семантичний пошук + граф викликів)
4. **Якщо worktree входять до вашого робочого процесу**: `scip-search` (пошук символів без стану, MCP не потрібен)
5. **Для великої документації**: `lilmd` (точкове читання розділів Markdown, без налаштування)
6. **Нарешті**: `ast-grep` (структурні патерни, великий рефакторинг)

**Обґрунтування**: 90% пошукових запитів успішно виконуються за допомогою `rg` + `Serena`. Додавайте `grepai` для семантичних потреб. Додавайте `scip-search` для середовищ worktree або CI, де MCP недоступний. Додавайте `ast-grep` лише для великомасштабного рефакторингу.

---

## Підсумок: набір із 6 інструментів

```
┌─────────────────────────────────────────────────────────┐
│                   SEARCH TOOL MASTERY                   │
│ ├─────────────────────────────────────────────────────────┤
│ │
│ rg (ripgrep) → Fast, exact text matching │
│ ├─ Use: 90% of searches │
│ └─ Speed: ~20ms │
│ │
│ grepai → Semantic + Call graph │
│ ├─ Use: Concept discovery, dependency tracing │
│ └─ Speed: ~500ms (finds what rg cannot) │
│ │
│ Serena → Symbol-aware + Session memory │
│ ├─ Use: Refactoring, structure understanding │
│ └─ Speed: ~100ms │
│ │
│ ast-grep → AST structural patterns │
│ ├─ Use: Large migrations, complex patterns │
│ └─ Speed: ~200ms │
│ │
│ scip-search → Symbol index (stateless, SCIP) │
│ ├─ Use: CI / worktrees / no MCP environments │
│ └─ Speed: ~5ms cold start │
│ │
│ lilmd → Markdown section navigation │
│ ├─ Use: Large docs, TOC + line ranges per section │
│ └─ Speed: instant, no index │
│ │
│ ═══════════════════════════════════════════════════ │
│ │
│ Master the combination, not individual tools. │
│ Each tool has a sweet spot. Use the right one. │
│ │
└─────────────────────────────────────────────────────────┘
```

---

## Додаткові матеріали

- [Serena MCP Guide](#serena-semantic-code-analysis)
- [grepai Documentation](#grepai-recommended-semantic-search)
- [ast-grep Patterns Skill](https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/examples/skills/ast-grep-patterns.md)
- [Architecture: Grep vs RAG History](../core/architecture.uk.md)
- [scip-search GitHub](https://github.com/liza-mas/scip-search)
- [lilmd GitHub](https://github.com/molefrog/lilmd)

---

**Останнє оновлення**: Травень 2026
**Сумісність**: Claude Code 2.1.7+

---
**Локалізація**: [Serhii (MacPlus Software)](https://macplus-software.com)
*Остання синхронізація: Травень 2026*
