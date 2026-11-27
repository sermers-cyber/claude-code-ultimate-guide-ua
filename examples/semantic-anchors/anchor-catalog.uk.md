---
title: "Каталог семантичних якорів"
description: "Добірка технічної лексики з прикладами, джерелами та межами застосування"
tags: [reference, semantic-anchors, architecture]
---

# Каталог семантичних якорів

> **Пов'язаний каталог**: [LLM-Coding/Semantic-Anchors](https://github.com/LLM-Coding/Semantic-Anchors) (Apache-2.0)
> **Обсяг**: вибрані терміни для воркфлоу Claude Code, а не повна копія каталогу спільноти

## Що таке семантичні якорі?

Семантичний якір називає в промпті усталений метод, патерн або фреймворк. Назва може бути корисним скороченням, якщо модель її розпізнає, але вона не задає обмежень вашого проєкту й не гарантує правильної реалізації. Поєднуйте термін з потрібною поведінкою та способом перевірити результат.

[Критерії якості каталогу спільноти](https://llm-coding.github.io/Semantic-Anchors/about/) питають, чи є термін точним, змістовним, послідовним і таким, що має відоме джерело. Його [план оцінювання](https://llm-coding.github.io/Semantic-Anchors/evaluations/) розрізняє розпізнавання та застосування. Цей каталог — набір прикладів, а не бенчмарк якості результату.

Використовуйте термін лише тоді, коли базовий метод підходить до завдання. Якщо Claude застосовує його неправильно, розгорніть назву в явні інструкції або пошліться на першоджерело. Не нагромаджуйте архітектурні патерни без доведеної потреби.

---

## Тестування та забезпечення якості

### Методології тестування

| Розмито | Семантичний якір | Що він активує |
|-------|-----------------|-------------------|
| «напиши тести» | "TDD London School (mockist)" | Ззовні всередину, моки співпрацівників, фокус на поведінці |
| «напиши тести» | "TDD Chicago School (classicist)" | Знизу вгору, реальні співпрацівники, перевірка стану |
| «протестуй граничні випадки» | "Property-Based Testing (QuickCheck)" | Генеративне тестування, shrinking, виявлення інваріантів |
| «ретельне тестування» | "Mutation Testing (Stryker/PIT)" | Знищення мутантів, вимірювання ефективності тестів |
| «тести поведінки» | "BDD Gherkin syntax (Given/When/Then)" | Стиль Cucumber, жива документація |

### Якість тестів

| Розмито | Семантичний якір | Ефект |
|-------|-----------------|--------|
| «хороші назви тестів» | "Roy Osherove naming: MethodName_Scenario_ExpectedBehavior" | Послідовні, описові назви |
| «обери рівні тестів» | "Test Pyramid (Fowler)" | Обговорення швидкості зворотного зв'язку та покриття між рівнями без фіксованого співвідношення |
| «швидкі тести» | "Sociable unit tests with test doubles at boundaries" | Швидкість за реалістичної поведінки |
| «читабельні тести» | "Arrange-Act-Assert (AAA) pattern" | Чітка структура тесту |
| «тести, які легко підтримувати» | "Object Mother / Test Data Builder pattern" | Повторно використовувані тестові фікстури |

---

## Архітектура та дизайн

### Архітектурні патерни

| Розмито | Семантичний якір | Коли використовувати |
|-------|-----------------|-------------|
| «чиста архітектура» | "Hexagonal Architecture (Ports & Adapters)" | Ізоляція домену, тестованість |
| «шарувата архітектура» | "Onion Architecture (Palermo)" | Залежності спрямовані до центру |
| «мікросервіси» | "Domain-Driven Design bounded contexts" | Межі сервісів |
| «розділи моделі читання й запису» | "CQRS" | Окремі моделі, коли ця ціна виправдана |
| «масштабовано» | "Event-Driven Architecture with message broker" | Асинхронна обробка, розв'язування залежностей |

### Додаткові якорі для програмування, які варто оцінити

Ці чотири терміни є в [каталозі спільноти](https://llm-coding.github.io/Semantic-Anchors/). Додавайте їх до промпту, коли завдання потребує базового методу, а потім опишіть локальні межі та очікувану перевірку.

| Термін | Корисний напрям | Джерело |
|---|---|---|
| Deep Modules | Ховайте суттєві деталі реалізації за невеликим стабільним інтерфейсом; перевірте, що викликачам усе ще треба знати | [John Ousterhout, *A Philosophy of Software Design*](https://web.stanford.edu/~ouster/cgi-bin/book.php) |
| Walking Skeleton | Побудуйте мінімальний наскрізний шлях через систему, перш ніж нарощувати функції; перевірте, що цей шлях працює | [Alistair Cockburn про Walking Skeleton](https://www.linkedin.com/posts/alistaircockburn_what-is-a-walking-skeleton-and-why-do-i-need-activity-7419086703577071616-D8Cs) |
| Mikado Method | Складіть карту залежностей перед структурною зміною, відкочуйте невдалі спроби й робіть передумови явними | [Ola Ellnestam і Daniel Brolund, *The Mikado Method*](https://www.manning.com/books/the-mikado-method) |
| Strangler Fig | Замінюйте застарілу поведінку по одній за певною межею; перевіряйте старий і новий шляхи під час міграції | [Martin Fowler, Strangler Fig](https://martinfowler.com/bliki/StranglerFigApplication.html) |

### Domain-Driven design (Evans)

| Розмито | Семантичний якір | Призначення |
|-------|-----------------|---------|
| «бізнес-логіка» | "DDD Aggregate pattern" | Транзакційна узгодженість |
| «доступ до даних» | "DDD Repository pattern" | Абстракція збереження |
| «мапінг об'єктів» | "DDD Value Objects" | Незмінні, рівність за значенням |
| «складні об'єкти» | "DDD Entity pattern" | Рівність на основі ідентичності |
| «бізнес-правила» | "DDD Domain Services" | Операції без стану |
| «інтеграція» | "DDD Anti-Corruption Layer (ACL)" | Ізоляція зовнішніх систем |

### Принципи SOLID

| Розмито | Семантичний якір | Конкретна настанова |
|-------|-----------------|-------------------|
| «одне призначення» | "SRP: one reason to change (Robert C. Martin)" | Фокус на зв'язності |
| «розширюваний» | "OCP: open for extension, closed for modification" | Архітектура плагінів |
| «замінний» | "LSP: subtypes must be substitutable" | Збереження контракту |
| «мінімальні інтерфейси» | "ISP: clients shouldn't depend on unused methods" | Розділення інтерфейсів |
| «слабко зв'язаний» | "DIP: depend on abstractions, not concretions" | Інверсія керування |

---

## Якість коду та рефакторинг

### Каталог рефакторингів (Fowler)

| Розмито | Семантичний якір | Тригер |
|-------|-----------------|---------|
| «винеси логіку» | "Extract Method refactoring" | Довгі методи |
| «прибери умовні оператори» | "Replace Conditional with Polymorphism" | Складні if/switch |
| «спрости створення» | "Replace Constructor with Factory Method" | Складне створення екземплярів |
| «прибери дублювання» | "Extract Class / Extract Superclass" | Схожі класи |
| «покращ іменування» | "Rename Method/Variable (intention-revealing names)" | Незрозумілі назви |

### Запахи коду (Fowler/Beck)

| Запах | Семантичний якір | Рішення |
|-------|-----------------|----------|
| «довгий метод» | "Extract Method where a named operation clarifies intent" | Перегляньте поведінку та читабельність |
| «великий клас» | "Extract Class following SRP" | Єдина відповідальність |
| «заздрість до функцій» | "Move Method to class that owns data" | Краща зв'язність |
| «одержимість примітивами» | "Replace Primitive with Value Object" | Типобезпека |
| «стрілянина дробом» | "Move Field/Method to consolidate changes" | Централізація логіки |

### Чистий код (Martin)

| Розмито | Семантичний якір | Застосування |
|-------|-----------------|-------------|
| «читабельно» | "Screaming Architecture: package structure reveals intent" | Іменування папок |
| «зрозумілі назви» | "Intention-revealing names (Clean Code Ch. 2)" | Самодокументування |
| «поясни складне рішення» | "Document the why, not the obvious mechanics" | Збереження міркувань, яких сам код не покаже |
| «маленькі функції» | "Functions should do one thing" | Перевірка відповідальності без фіксованого ліміту рядків |
| «без побічних ефектів» | "Command-Query Separation (CQS)" | Передбачувана поведінка |

---

## Обробка помилок

### Функціональні патерни

| Розмито | Семантичний якір | Переваги |
|-------|-----------------|----------|
| «обробка помилок» | "Railway Oriented Programming with Either<L,R>" | Композиційні помилки |
| «безпека щодо null» | "Option/Maybe monad (never return null)" | Явна відсутність значення |
| «накопичення помилок» | "Validation applicative functor" | Збирання всіх помилок |
| «асинхронні помилки» | "Task/Future monad with error channel" | Асинхронний потік помилок |

### Стратегії винятків

| Розмито | Семантичний якір | Сценарій використання |
|-------|-----------------|----------|
| «обробляй помилки» | "Checked exceptions at boundaries only" | Зовнішня інтеграція |
| «відновлення після помилок» | "Circuit Breaker pattern (Nygard)" | Відмовостійкість |
| «плавна деградація» | "Bulkhead pattern" | Ізоляція |
| «логіка повторних спроб» | "Exponential backoff with jitter" | Стійкість |

---

## Дизайн API

### Зрілість REST

Наведені нижче рівні стосуються [Richardson Maturity Model](https://martinfowler.com/articles/richardsonMaturityModel.html). Вони описують вибір у дизайні HTTP, а не оцінку, яку кожен API мусить максимізувати.

| Розмито | Семантичний якір | Рівень |
|-------|-----------------|-------|
| «REST API» | "REST Level 0: HTTP as tunnel" | Базовий |
| «правильний REST» | "REST Level 2: HTTP verbs + status codes" | Стандартний |
| «HATEOAS» | "REST Level 3: Hypermedia controls" | Повний REST |
| «версіонування API» | "URL path versioning (/v1/) or header versioning" | Еволюція |

### Якість API

| Розмито | Семантичний якір | Застосування |
|-------|-----------------|-------------|
| «послідовний API» | "JSON:API specification" | Формат відповіді |
| «задокументований API» | "OpenAPI 3.0 (Swagger)" | Дизайн від специфікації |
| «безпечний API» | "OAuth 2.0 + PKCE flow" | Автентифікація |
| «обмеження частоти запитів» | "Token bucket algorithm" | Керування трафіком |

---

## Документація

### Документація архітектури

| Розмито | Семантичний якір | Результат |
|-------|-----------------|--------|
| «задокументуй архітектуру» | "C4 Model (Context, Container, Component, Code)" | Діаграми |
| «документація архітектури» | "arc42 template structure" | Вичерпна документація |
| «проєктні рішення» | "ADR (Architecture Decision Records) - Nygard format" | Журнал рішень |
| «огляд системи» | "4+1 View Model (Kruchten)" | Кілька перспектив |

### Документація коду

| Розмито | Семантичний якір | Формат |
|-------|-----------------|--------|
| «документація API» | "JSDoc / TSDoc with @example tags" | Згенерована документація |
| «README» | "README-driven development (Tom Preston-Werner)" | Вступ до проєкту |
| «changelog» | "Keep a Changelog format (semver)" | Release notes |
| «внесок у проєкт» | "CONTRIBUTING.md with PR template" | Посібник для контриб'юторів |

---

## Вимоги та специфікації

### Синтаксис вимог

| Розмито | Семантичний якір | Формат |
|-------|-----------------|--------|
| «вимоги» | "EARS syntax (Easy Approach to Requirements)" | Структуровані вимоги |
| «user stories» | "Connextra format: As a [role] I want [goal] so that [benefit]" | Перспектива користувача |
| «критерії приймання» | "BDD Gherkin: Given/When/Then" | Тестовані критерії |
| «сценарії використання» | "Cockburn's use case template (brief/casual/fully dressed)" | Потоки взаємодії |

### Дослідження та картування

| Розмито | Семантичний якір | Техніка |
|-------|-----------------|-----------|
| «зрозумій користувачів» | "User Story Mapping (Jeff Patton)" | Візуалізація шляху користувача |
| «пріоритезуй функції» | "MoSCoW method (Must/Should/Could/Won't)" | Тріаж пріоритетів |
| «потреби користувачів» | "Jobs-to-be-Done framework (Christensen)" | Фокус на результаті |
| «моделювання подій» | "Event Storming (Brandolini)" | Дослідження домену |

---

## Безпека

### OWASP і поширені вразливості

| Розмито | Семантичний якір | Захист |
|-------|-----------------|------------|
| «безпечний код» | "OWASP Top 10 mitigations" | Вичерпний чеклист |
| «валідація вводу» | "Allowlist validation + parameterized queries" | Запобігання ін'єкціям |
| «автентифікація» | "OWASP ASVS Level 2 requirements" | Стандарти автентифікації |
| «керування секретами» | "HashiCorp Vault or cloud KMS" | Зберігання секретів |

### Патерни безпеки

| Розмито | Семантичний якір | Реалізація |
|-------|-----------------|----------------|
| «безпечно за замовчуванням» | "Principle of least privilege" | Мінімальні дозволи |
| «ешелонований захист» | "Multiple security layers (network, app, data)" | Багатошарова безпека |
| «безпечний зв'язок» | "TLS 1.3 with certificate validation" | Безпека транспорту; pinning потребує окремої моделі загроз |
| «журналювання аудиту» | "Immutable audit trail with tamper detection" | Відповідність вимогам |

---

## Продуктивність

### Патерни оптимізації

| Розмито | Семантичний якір | Застосування |
|-------|-----------------|-------------|
| «кешування» | "Cache-aside pattern with TTL" | Продуктивність читання |
| «пакетна обробка» | "Bulk operations with chunking" | Продуктивність запису |
| «ліниве завантаження» | "Virtual proxy pattern" | Оптимізація ресурсів |
| «мемоізація» | "Function memoization with LRU eviction" | Кешування обчислень |

### Масштабованість

| Розмито | Семантичний якір | Техніка |
|-------|-----------------|-----------|
| «горизонтальне масштабування» | "Stateless services + external state store" | Масштабування вшир |
| «масштабування бази даних» | "Read replicas + write-through caching" | Продуктивність БД |
| «асинхронна обробка» | "Message queue with competing consumers" | Пропускна здатність |
| «балансування навантаження» | "Round-robin with health checks" | Розподіл |

---

## Патерни промптингу

### Техніки проти заякорювання

LLM можуть зациклюватися на своїй першій пропозиції, звужуючи простір рішень. Ці патерни протидіють упередженню заякорювання:

| Патерн | Шаблон промпту | Ефект |
|---------|-----------------|--------|
| Чистий аркуш | "Ignore any prior ideas. Generate 4 novel approaches to [X]" | Примушує до різноманітності |
| Цикл рефлексії | "Generate 3 options, then critique each, then recommend" | Самокорекція |
| Кількісне порівняння | "Rank by [metric1], [metric2], [metric3] with scores 1-10" | Об'єктивні компроміси |
| Адвокат диявола | "What are the strongest arguments against your recommendation?" | Виявлення прихованих витрат |
| Перевертання обмеження | "Now solve with [opposite constraint]" | Розширення простору рішень |

### Промпти для дослідження

Використовуйте їх, коли потрібно кілька підходів, перш ніж на чомусь зупинитися:

| Мета | Промпт із семантичним якорем |
|------|------------------------|
| Вибір архітектури | "Compare [A], [B], [C] using C4 model criteria: context fit, container complexity, component count" |
| Компроміс продуктивності | "Analyze time complexity (Big O), space complexity, and cache-friendliness for each approach" |
| Відповідність команді | "Evaluate learning curve, debugging difficulty, and ecosystem maturity (1-10 scale)" |
| Оцінка ризиків | "For each option: what's the worst-case failure mode and recovery cost?" |

### Промпти для ітерацій

Для поступового вдосконалення скриптів і автоматизації:

| Етап | Патерн промпту |
|-------|----------------|
| Початковий | "Create a [language] script that [goal]. Include basic error handling." |
| Обмеження | "Add: [specific constraint]. Remove: [unwanted behavior]." |
| Зміцнення | "Add input validation, logging, and handle edge case: [specific case]." |
| Оптимізація | "Optimize for [metric]. Target: [specific threshold]." |
| Документування | "Add usage examples and inline comments for non-obvious logic." |

---

## Шаблон CLAUDE.md із семантичними якорями

```markdown
# Project Architecture

## Principles (Semantic Anchors)

### Architecture
- **Pattern**: Hexagonal Architecture (Ports & Adapters)
- **Domain modeling**: Domain-Driven Design tactical patterns (Aggregates, Value Objects, Domain Events)
- **Documentation**: ADR (Architecture Decision Records) for significant decisions

### Code Quality
- **Design**: SOLID principles, especially SRP and DIP
- **Refactoring**: Apply Fowler's catalog - Extract Method, Replace Conditional with Polymorphism
- **Naming**: Intention-revealing names, Screaming Architecture for packages

### Testing
- **Methodology**: TDD London School - outside-in, mock collaborators
- **Structure**: Arrange-Act-Assert (AAA) pattern
- **Coverage**: Test Pyramid - 70% unit, 20% integration, 10% E2E

### Error Handling
- **Pattern**: Railway Oriented Programming with Result<T, E>
- **Never**: Return null, throw for control flow
- **Always**: Use Option/Maybe for optional values

### API Design
- **Style**: REST Level 2 with proper HTTP verbs and status codes
- **Documentation**: OpenAPI 3.0 spec-first
- **Security**: OAuth 2.0 + PKCE for authentication

### Requirements
- **Format**: EARS syntax for formal requirements
- **User stories**: Connextra format with acceptance criteria
- **Discovery**: Event Storming for domain exploration
```

---

## Короткий довідник

### Приклади «до/після»

| До (розмито) | Після (із якорем) |
|----------------|------------------|
| «Зроби чисто» | "Apply SRP: each class has one reason to change" |
| «Додай обробку помилок» | "Use Railway Oriented Programming with Either monad" |
| «Напиши хороші тести» | "Follow TDD London School with mock collaborators" |
| «Задокументуй API» | "Generate OpenAPI 3.0 spec from annotations" |
| «Перевір цю межу вводу» | "Check applicable OWASP ASVS input-validation requirements" |
| «Відокрем цю операцію» | "Apply Extract Method without changing public behavior" |
| «Моделі читання й запису мають різні потреби» | "Consider CQRS; assess Event Sourcing separately" |

---

## Поради щодо використання

1. **Поєднуйте якорі**: "Apply Hexagonal Architecture with DDD tactical patterns and Railway Oriented error handling"

2. **Вказуйте версії/авторів**: "Following Kent Beck's TDD (2003)" конкретніше, ніж "TDD"

3. **Посилайтеся на книжки**: "Clean Code Chapter 2 naming conventions" активує конкретні знання

4. **Називайте патерни явно**: "Strategy pattern" > "pluggable behavior"

5. **Використовуйте з XML-тегами**: поєднуйте якорі з тегами `<constraints>` і `<quality_criteria>` для максимального ефекту

---

> **Використовуйте обережно**: віддавайте перевагу терміну, який ви можете визначити й перевірити для цього завдання. Якщо модель застосовує його неправильно, розпишіть потрібну поведінку й пошліться на першоджерело методу.
