# Module 04: Agents & Specialization

**Час**: 1.5 години | **Складність**: ⭐⭐ Intermediate

## Мета

Створювати спеціалізованих agents для конкретних завдань. Навчитися фокусувати можливості штучного інтелекту на точкових проблемах.

---

## Що ви дізнаєтеся

- Що таке agents та чому вони корисні
- Створення власних agents за допомогою AGENT.md
- Обмеження можливостей agents (пісочниця / sandboxing)
- Використання agents для конкретних завдань
- Коли використовувати спеціалізованих agents проти прямого звернення до Claude

---

## Що таке Agents?

**Agent** — це спеціалізована версія Claude Code, налаштована під одне конкретне завдання.

### Приклад: Agent для перегляду коду (Code Reviewer Agent)

Замість того, щоб просити звичайного Claude переглянути код (що вимагає перемикання контексту в думках), ви використовуєте:

```bash
/agent code-reviewer
Review this function for bugs and performance issues
```

Спеціалізований code-reviewer agent:
- Працює виключно з code review
- Має набір tools, специфічних для перегляду коду
- Знає шаблони вразливостей безпеки
- Не відволікається на інші сторонні завдання

### Звичайний Claude проти Agents

| Аспект | Звичайний Claude | Agent |
|--------|------------------|-------|
| **Scope** | Загальне призначення | Спеціалізований |
| **Context** | Пам'ятає все | Сфокусована пам'ять під завдання |
| **Tools** | Усі доступні | Обмежений набір |
| **Швидкість**| Багатозадачність | Швидкий в одній справі |
| **Використання**| Дослідження, навчання | Повторювані, специфічні завдання |

---

## Створення вашого першого Agent

Agents визначаються у файлах `.claude/agents/AGENT.md`.

### Базова структура

```markdown
---
name: code-reviewer
type: agent
description: Reviews code for bugs, performance, and security
auto_invoke: false
requires_approval: true
---

# Code Reviewer Agent

## Purpose
Review code for:
- Bugs and logical errors
- Performance issues
- Security vulnerabilities
- Code style consistency
- Test coverage

## Tools
- Code analysis
- Git diff viewer
- Test runner
- Linting tools

## Instructions
When reviewing:
1. Check for null pointers and edge cases
2. Look for performance bottlenecks (O(n²), nested loops)
3. Scan for security issues (SQL injection, XSS)
4. Verify tests cover the change
5. Suggest improvements without being harsh

## Example Usage
/agent code-reviewer
Review src/auth.js for security issues
```

### Розташування файлу

Створіть файл у вашому проєкті:

```
my-project/
└── .claude/
    └── agents/
        └── code-reviewer.md
```

### Додавання доступу

У CLAUDE.md вашого проєкту зробіть посилання на нього:

```markdown
## Available Agents
Run agents with: /agent [name]

- **code-reviewer** - Code quality and security review
  Usage: /agent code-reviewer <description>
  
- **test-writer** - Generate tests for code
  Usage: /agent test-writer <file path>
```

---

## Шаблони проектування (Design Patterns) для Agents

### Шаблон 1: Перевірка якості (Quality Checker)

```markdown
---
name: quality-auditor
description: Audits code quality metrics
---

# Quality Auditor

## Purpose
Check code for:
- Test coverage (<80% = fail)
- Type safety (TypeScript strict mode)
- Code duplication
- Cyclomatic complexity

## Tools
- Code analysis
- Coverage reporter
- Type checker

## Output Format
- ✅ Passed: [metric] = X
- ⚠️ Warning: [metric] = X
- ❌ Failed: [metric] = X

## Scoring
Score /100 based on all metrics.
```

### Шаблон 2: Спеціаліст з безпеки (Security Specialist)

```markdown
---
name: security-auditor
description: Scans code for vulnerabilities
requires_approval: true
---

# Security Auditor

## Purpose
Find security vulnerabilities:
- Injection attacks (SQL, NoSQL, command)
- Authentication/authorization issues
- Cryptography mistakes
- Data exposure risks
- OWASP Top 10

## Tools
- Static analysis
- Dependency checker
- Secret detection

## Severity Levels
- CRITICAL: Stop work immediately
- HIGH: Fix before merge
- MEDIUM: Fix in next sprint
- LOW: Consider fixing
```

### Шаблон 3: Автор документації (Documentation Writer)

```markdown
---
name: doc-writer
description: Generates documentation
---

# Documentation Writer

## Purpose
Create or improve:
- README files
- API documentation
- Architecture docs
- User guides
- CHANGELOG entries

## Output Format
- Clear headings
- Code examples for each feature
- Link to related docs
- Numbered lists for sequences

## Style
- Beginner-friendly
- No jargon without explanation
- Show before/after examples
```

---

## Можливості та обмеження Agents

### Можливості за замовчуванням (Default Capabilities)

Усі agents вміють:
- Читати файли (з урахуванням git)
- Аналізувати код
- Писати документацію
- Перевіряти синтаксис
- Запускати тести

### Обмеження можливостей (Restricting Capabilities)

Використовуйте блок `capabilities`, щоб створити пісочницю (sandbox) для agent:

```markdown
---
name: code-reviewer
capabilities:
  - read_files      # Може читати код
  - run_tests       # Може запускати тести
  - check_syntax    # Може перевіряти синтаксис
  - write_comments  # Може пропонувати зміни, але...
  - NO: commit      # ...не може робити commit
  - NO: push        # ...не може робити push в git
---
```

Такий agent може переглядати код, але ніколи випадково не відправить зламані зміни до репозиторію.

### Популярні обмеження

```markdown
# Analyzer (тільки для читання)
capabilities:
  - read_files
  - run_tests
# Не може нічого змінювати

# Refactoring Agent (запис, без push)
capabilities:
  - read_files
  - write_files
  - run_tests
  - NO: commit
  - NO: push
# Може змінювати код, але ви перевіряєте його перед push

# Full Agent (без обмежень)
capabilities:
  - all
# Може робити що завгодно (використовуйте з обережністю)
```

---

## Використання Agents у вашому робочому процесі

### Виклик Agent

```bash
/agent code-reviewer
Review the changes I just made to src/auth.js
```

Claude перемикається на вказаного code-reviewer agent і дає відповідь.

### Ланцюжки Agents (Chaining Agents)

Запускайте декілька agents послідовно:

```bash
# Крок 1: Test Writer генерує тести
/agent test-writer
Write tests for src/utils/validators.js

# Крок 2: Code Reviewer перевіряє тести
/agent code-reviewer
Review the tests that were just written

# Крок 3: Security Auditor сканує код
/agent security-auditor
Check the tests and code for vulnerabilities
```

### Спеціалізований Agent в режимі планування (Plan Mode)

Для ризикованих операцій використовуйте `/plan` всередині сесії з agent:

```bash
/agent refactoring-specialist
/plan
Refactor the payment processing module to use async/await
```

---

## Вправа: Створення Agent для написання тестів (Test-Writer)

### Крок 1: Створіть файл конфігурації Agent

```bash
cat > .claude/agents/test-writer.md << 'EOF'
---
name: test-writer
description: Generates comprehensive tests
capabilities:
  - read_files
  - write_files
  - run_tests
---

# Test Writer Agent

## Purpose
Generate high-quality tests for:
- Unit tests (pure functions)
- Integration tests (component interactions)
- Edge cases and error conditions
- Performance tests

## Style
- Arrange-Act-Assert pattern
- Descriptive test names
- Each test focuses on ONE behavior
- 70%+ code coverage target

## Tools
- Test framework (Jest, pytest, etc)
- Mock libraries
- Assertion libraries

## Output
- Tests in same directory as source
- Naming: [file].test.js or [file].spec.js
- Include setup/teardown code
EOF
```

### Крок 2: Додайте посилання у CLAUDE.md

```markdown
## Available Agents
- test-writer: Generate tests for any function or module
  Usage: /agent test-writer <file path>
```

### Крок 3: Запустіть його

```bash
/agent test-writer
Write tests for src/utils/formatDate.js
```

Agent зробить наступне:
1. Прочитає `formatDate.js`
2. Зрозуміє логіку роботи
3. Згенерує комплексні тести
4. Покаже створений файл тестів

### Крок 4: Перевірка

Перегляньте тести перед схваленням:
- Чи покривають вони крайні випадки (edge cases)?
- Чи зрозумілі назви?
- Чи успішно вони проходять?

---

## Коли варто використовувати Agents

### Використовуйте Agents, коли:

✅ Ви виконуєте одну й ту саму задачу повторно (code review, тестування, аудит безпеки)

✅ Вам потрібен вузькоспрямований ШІ для конкретної задачі

✅ Ви хочете обмежити можливості інструментів (для безпеки)

✅ Ви будуєте командні процеси автоматизації (workflows)

✅ Задача має чіткі критерії успішного виконання

### Використовуйте звичайного Claude, коли:

✅ Ви досліджуєте тему або вчитеся

✅ Задача є новою та нестандартною

✅ Вам потрібна загальна допомога

✅ Ви займаєтеся налагодженням (debugging) чогось дуже складного

✅ Вам потрібен інтерактивний діалог "питання-відповідь"

---

## Найкращі практики

### РЕКОМЕНДУЄТЬСЯ

✅ Давати agents чіткі та вузькі завдання

✅ Фіксувати очікуваний формат виводу (output format) в інструкціях agent

✅ Обмежувати capabilities, якщо вони непотрібні

✅ Тестувати нових agents на простих прикладах задач перед запуском

✅ Зберігати ваших agents у репозиторії (в `.claude/agents/`)

### НЕ РЕКОМЕНДУЄТЬСЯ

❌ Створювати agents із завданнями, що перетинаються (це заплутує)

❌ Робити agents занадто універсальними (це нівелює сенс їх створення)

❌ Повністю довіряти результату роботи agent (завжди робіть перевірку)

❌ Створювати agent для разових задач (для цього краще підійде звичайний Claude)

---

## Валідація: Ви готові, якщо...

✓ Ви створили принаймні одного власного agent

✓ Ви розумієте різницю між agents та звичайним Claude

✓ Ви вмієте обмежувати capabilities для agent

✓ Ви знаєте, як викликати agent (`/agent name`)

✓ Ви протестували свого agent на реальній задачі

---

## Що далі?

**Module 05: Skills & Automation** охоплює:
- Створення багаторазових skills (модулів знань)
- Об'єднання можливостей (capabilities) для дистрибуції
- Автоматичний виклик skills (auto-invocation)
- Створення власної бази знань (custom knowledge base)

Це навчить вас пакувати знання та інструкції, щоб Claude пам'ятав їх у різних sessions.

---
**Локалізація**: [Serhii (MacPlus Software)](https://macplus-software.com)
*Остання синхронізація: Травень 2026*
