---
title: "Module 05: Skills & Automation"
description: "Модуль 05 навчального шляху: створення skills для Claude Code з обмеженою областю дії через SKILL.md, progressive disclosure, керування викликом, оцінювання та критерії виведення з обігу. 1.5 години, рівень intermediate."
---

# Module 05: Skills & automation

**Час**: 1.5 години | **Складність**: ⭐⭐ Intermediate

**Попередній:** [Module 04: Agents & Specialization](04-agents.uk.md)

## Мета

Створити skill проєкту, який надає Claude релевантні знання або повторно використовувану процедуру без завантаження всього свого вмісту в кожну session.

---

## Що ви дізнаєтеся

- Що skills завантажують і коли
- Як створити коректний `SKILL.md`
- Як `description` керує виявленням skill моделлю
- Як керувати викликом із боку користувача та моделі
- Як вибрати область власності (ownership scope)
- Як відокремити judgment від гарантованої оркестрації
- Як оцінювати, підтримувати та виводити skill з обігу

---

## Що таке skills?

**Skill** — це каталог із файлом `SKILL.md` та необов'язковими допоміжними файлами. Його опис (description) оголошується Claude. Повні інструкції завантажуються лише тоді, коли ви або Claude викликаєте skill.

Через це skills корисні для повторюваних процедур, чеклістів і довідкових матеріалів, які були б надто дорогими або відволікаючими в завжди завантаженому `CLAUDE.md`.

### Приклад: Skill для тестування

Замість того щоб пояснювати підхід до тестування в кожній session, створіть skill проєкту, чий опис вказує, коли він застосовується:

```markdown
---
name: testing-standards
description: Apply this project's Jest and Testing Library conventions when creating, reviewing, or debugging tests.
---

# Testing Standards

- Use descriptive test names.
- Follow Arrange, Act, Assert.
- Mock external boundaries, not implementation details.
- Run the relevant test file before the full suite.
```

Claude бачить назву й опис під час session. Він завантажує тіло, коли поточний запит відповідає опису або коли ви вводите `/testing-standards`.

### Skills проти CLAUDE.md, agents і воркфлоу

| Механізм | Найкраще підходить для | Завантаження або виконання |
|-----------|----------|----------------------|
| `CLAUDE.md` | Короткі факти й правила, релевантні для більшості sessions | Завантажується на початку session |
| Skill | Повторно використовувані знання, judgment або адаптивна процедура | Опис оголошується; тіло завантажується під час виклику |
| Agent | Ізольований контекст, спеціалізовані інструменти або паралельна робота | Працює в окремому контексті |
| Hook або скриптований воркфлоу | Передумови, порядок, повтори, правила зупинки та перевірки, які мають бути примусовими | Виконується кодом або harness |

Нумеровані кроки самі по собі не є причиною залишати формат skill. Переносьте операцію в hook, скрипт або воркфлоу, коли коректність залежить від гарантованого порядку, обов'язкового артефакту, політики повторів або жорсткої зупинки. Залишайте judgment у skill, наприклад оцінку неоднозначності чи вибір між прийнятними компромісами.

---

## Спершу оберіть область власності

Спільне використання skill не вимагає спільної підтримки однієї універсальної копії. Стаття Фредеріка Камблора [Un Skill n'est pas une librairie](https://devx.writizzy.blog/p/un-skill-nest-pas-une-lib) дає корисне застереження: присвоєння, локальний контекст і тихий дрейф поведінки можуть коштувати дорожче, ніж копіювання файлу та його спеціалізація.

Використовуйте одну з чотирьох областей:

| Область | Розташування або канал | Контракт підтримки |
|-------|---------------------|----------------------|
| Особиста | `~/.claude/skills/` | Оптимізовано під звички однієї людини; жодних обіцянок сумісності |
| Проєкт або команда | `.claude/skills/` у Git | Спільні конвенції з названим власником і шляхом рев'ю |
| Інструмент або вендор | Plugin або підтримуваний репозиторій | Версіонована підтримка користувачів інструмента |
| Маркетплейс або глобальна | Реєстр або публічний репозиторій | За замовчуванням джерело для виявлення; приймайте лише після рев'ю та локального оцінювання |

З погляду безпеки ставтеся до будь-якого завантаженого skill як до виконуваної залежності, бо він може містити дозволи інструментів, скрипти та інструкції. З погляду власності ставтеся до нього як до контекстно-залежного матеріалу: записуйте його область, власника, припущення та сигнал виведення з обігу. Ці правила доповнюють одне одного.

---

## Створення вашого першого skill

Skills розміщуються в каталогах `.claude/skills/{skill-name}/`. Обов'язковий файл — `SKILL.md`.

### Розташування файлу

```text
my-project/
└── .claude/
    └── skills/
        └── testing-standards/
            └── SKILL.md
```

### Базова структура

```markdown
---
name: testing-standards
description: Apply this project's Jest and Testing Library conventions when creating, reviewing, or debugging tests.
metadata:
  version: 1.0.0
---

# Testing Standards

## When to apply

Use for unit tests, component tests, mocks, fixtures, or coverage changes.
Do not use for end-to-end tests maintained by the QA repository.

## Test structure

1. Arrange the smallest realistic input.
2. Act through the public interface.
3. Assert behavior and user-visible effects.

## Verification

Run the changed test file, then the relevant package suite.
```

`name` і `description` є основними полями для виявлення. Власні метадані, як-от версія, належать до `metadata`. Поля `triggers`, `auto_invoke` і `keywords` не є frontmatter skills Claude Code.

---

## Виявлення та виклик skill

### Пишіть опис як правило маршрутизації

Claude використовує `description`, щоб вирішити, чи релевантний skill. Включайте:

- Що робить skill
- Ситуації, у яких його слід використовувати
- Важливі антитригери, коли суміжні завдання належать іншому місцю

```yaml
description: Review PostgreSQL schema and query changes for indexes, locking, and migration safety. Use for SQL migrations and slow-query investigations; do not use for application-level API design.
```

### Керуйте тим, хто може його викликати

За замовчуванням і ви, і Claude можете викликати skill.

```yaml
# Manual only. Appropriate for deploy, commit, or message-sending workflows.
disable-model-invocation: true
```

```yaml
# Model only. Appropriate for background knowledge with no useful slash command.
user-invocable: false
```

Режиму `auto_invoke: true` на початку session не існує. У звичайній session Claude отримує описи доступних skills і завантажує тіло skill лише під час виклику. Викликане тіло залишається в розмові; дозволи інструментів із `allowed-tools` діють лише протягом ходу, що викликав skill.

### Тримайте дозволи інструментів вузькими

`allowed-tools` попередньо схвалює відповідні інструменти на хід, що викликає skill. Воно не прибирає інші інструменти з набору Claude.

```yaml
allowed-tools: Read Grep Glob Bash(npm test *)
```

Перегляньте це поле, перш ніж використовувати сторонній skill. Широкий дозвіл на Bash може суттєво змінити його ризик.

---

## Progressive disclosure

Тримайте `SKILL.md` сфокусованим і виносьте детальні матеріали в допоміжні файли:

```text
testing-standards/
├── SKILL.md
├── references/
│   ├── mocking.md
│   └── integration-tests.md
└── scripts/
    └── select-tests.sh
```

Посилайтеся на кожен допоміжний файл із `SKILL.md` і вказуйте, коли його відкривати чи виконувати. Офіційні рекомендації радять тримати `SKILL.md` до 500 рядків.

---

## Поширені шаблони skills

### Шаблон 1: Конвенції проєкту

Використовуйте skill проєкту, коли порада залежить від архітектури репозиторію, рішень команди або локальних інструментів.

```markdown
---
name: python-standards
description: Apply this repository's Python typing, import, packaging, and pytest conventions when editing Python code.
---

# Python Standards

- Use type hints on public functions.
- Keep tests next to their package under `tests/`.
- Follow the repository's configured formatter and linter.
- Verify with the narrowest relevant pytest target first.
```

### Шаблон 2: Доменні знання

```markdown
---
name: payment-processing
description: Apply this product's payment state machine, idempotency, and audit rules when changing checkout or refund flows.
user-invocable: false
---

# Payment Processing Rules

- Never log card data or payment secrets.
- Reuse the existing idempotency key at retry boundaries.
- Treat provider callbacks as untrusted and potentially duplicated.
- Verify state transitions against the canonical state machine.
```

### Шаблон 3: Ручний воркфлоу

```markdown
---
name: release-check
description: Prepare and verify a release candidate for this repository.
disable-model-invocation: true
---

# Release Check

1. Read the repository release instructions.
2. Verify the version and working tree.
3. Run the required checks.
4. Report blockers without publishing.
```

Модель може адаптувати ці кроки. Якщо публікація ніколи не має відбуватися до певного шлюзу, забезпечуйте цей шлюз скриптом, hook, CI-завданням або воркфлоу, а не лише прозовим текстом.

---

## Пакування та поширення skills

Skills проєкту можна комітити разом із репозиторієм:

```text
my-project/
└── .claude/
    └── skills/
        ├── testing-standards/
        │   └── SKILL.md
        ├── api-design/
        │   └── SKILL.md
        └── security-checklist/
            └── SKILL.md
```

Колеги отримують файли через Git, але виявлення не доводить коректну активацію чи вивід. Записуйте власника й припущення в кожному skill, а потім запускайте репрезентативні випадки в нових sessions.

Використовуйте публічні каталоги, щоб знаходити шаблони. Перш ніж приймати сторонній skill:

1. Прочитайте його повні інструкції, скрипти й дозволи інструментів.
2. Вирішіть, чи споживати його без змін, робити fork, чи витягнути лише корисний шаблон.
3. Вкажіть локального власника та очікування щодо підтримки.
4. Порівняйте репрезентативні промпти із skill і без нього.
5. Зафіксуйте або запишіть переглянуту версію, якщо оновлення можуть змінити поведінку.

---

## Вправа: створіть доменний skill

### Сценарій

Ви будуєте сайт електронної комерції. Claude потрібна модель продуктів проєкту, коли він змінює код каталогу та складу.

### Крок 1: Створіть каталог

```bash
mkdir -p .claude/skills/product-data-model
```

Збережіть наступне як `.claude/skills/product-data-model/SKILL.md`:

```markdown
---
name: product-data-model
description: Apply the product, SKU, price, and inventory model when changing catalog queries or stock behavior in this repository.
metadata:
  owner: commerce-team
  version: 1.0.0
---

# Product Data Model

## When to apply

Use for catalog, SKU, pricing, and inventory changes.

## Core rules

- A Product owns one or more SKUs.
- Price and inventory belong to the SKU, not Product.
- Inventory cannot become negative.
- Store monetary values using the repository's decimal type.

## Verification

- Check the schema and existing migrations before proposing SQL.
- Exercise out-of-stock and concurrent-order cases.
```

### Крок 2: Тестуйте виявлення та вивід окремо

Відкривайте нові sessions для кожного випадку:

| Промпт | Очікувана маршрутизація |
|--------|------------------|
| "Add a query for products with fewer than five units" | Skill має викликатися |
| "Change the marketing page headline" | Skill не має викликатися |

У позитивному випадку перевіряйте й результат: skill має маршрутизуватися правильно, а запропонована зміна має відповідати реальній схемі репозиторію. Сам лише тригер не є успіхом.

---

## Оцінювання та ітерації

Тестуйте дві незалежні властивості:

1. **Коректність тригера**: чи викликає Claude skill на релевантних промптах і уникає його на нерелевантних?
2. **Якість виводу**: чи задовольняє результат явні твердження (assertions) після виклику?

Запускайте кожен промпт у новій session зі skill увімкненим і вимкненим. Запуск без skill є базовою лінією. Записуйте модель, версію Claude Code, набір промптів, кількість запусків, твердження, кількість успіхів, використання токенів і дисперсію. Структурний валідатор доводить формат, а не якість поведінки.

Офіційний plugin `skill-creator` може зберігати випадки в `evals/evals.json`, запускати ізольовані порівняння, створювати докази оцінювання, робити бенчмарк skill проти його відсутності, порівнювати версії наосліп і налаштовувати описи. Оцінювання LLM і самокритика залишаються генераторами доказів, а не незалежним підтвердженням. Переглядайте важливі результати детермінованими перевірками або кваліфікованою людиною.

Обирайте пороги прийняття за ризиком і вартістю збою конкретного skill. Універсальна цільова частка успіхів приховує знаменник, дисперсію та серйозність окремих збоїв.

---

## Життєвий цикл skill

1. **Область**: оберіть особисту, проєктну/командну, інструментальну/вендорську або маркетплейсну/глобальну власність.
2. **Базова лінія**: зберіть репрезентативні промпти до додавання skill.
3. **Створення**: напишіть найменший корисний `SKILL.md` і допоміжні файли.
4. **Оцінювання**: протестуйте маршрутизацію та якість виводу в нових sessions.
5. **Спостереження**: фіксуйте реальні промахи, здогадки та активації в хибному контексті.
6. **Рев'ю**: пропонуйте зміни, а потім повторно запускайте базову лінію перед їх прийняттям.
7. **Виведення з обігу**: вимикайте або видаляйте skills, які не використовуються, застаріли, надлишкові чи шкідливі.

Запустіть `/skill-doctor` у терміналі, щоб перевірити вартість контексту та невикористані skills. Його звіт виключає вбудовані й enterprise skills, недоступний через Remote Control і вимагає отримання feature flags. Сприймайте позначку «не використовується» як сигнал для рев'ю, а не як автоматичний наказ видалити.

Не архівуйте виведений з обігу skill у `.claude/skills/`, бо вкладене виявлення може залишати його видимим. Збережіть його в історії Git або перенесіть поза каталоги, де відбувається виявлення skills, із датованою приміткою про виведення з обігу.

---

## Найкращі практики

### Робіть

- Тримайте одну чітку відповідальність на skill.
- Пишіть опис як правило маршрутизації.
- Записуйте область, власника, припущення та критерії виведення з обігу.
- Тримайте основний файл коротким і посилайтеся на допоміжні матеріали.
- Переглядайте сторонні інструкції, скрипти та дозволи перед використанням.
- Порівнюйте зі skill і без нього в нових sessions.
- Розміщуйте гарантовані шлюзи в коді, hooks, CI або воркфлоу.

### Не робіть

- Не розміщуйте тимчасові чи одноразові інструкції в `CLAUDE.md`; використовуйте поточний промпт.
- Не вважайте встановлення з маркетплейсу контрактом підтримки.
- Не робіть висновків про якість виводу з успішного виклику.
- Не приймайте самокритику як валідацію без зовнішніх перевірок.
- Не тримайте неактивні skills у каталогах, де відбувається виявлення.
- Не додавайте загальні гілки, що розмивають типовий випадок проєкту.

---

## Валідація: Ви готові, якщо...

✓ Ваш skill збережено в `.claude/skills/{name}/SKILL.md`

✓ Його `description` охоплює тригери та важливі антитригери

✓ Ви можете пояснити його область власності та контракт підтримки

✓ Ви протестували релевантні й нерелевантні промпти в нових sessions

✓ Ви порівняли вивід зі skill і без нього

✓ Ви знаєте, які гарантії належать hook, скрипту, CI-завданню чи воркфлоу

✓ Ви визначили, як переглядати та виводити skill з обігу

---

## Джерела

- [Claude Code: Extend Claude with skills](https://code.claude.com/docs/en/skills)
- [Agent Skills open standard](https://agentskills.io/)
- [Frédéric Camblor: Un Skill n'est pas une librairie](https://devx.writizzy.blog/p/un-skill-nest-pas-une-lib)

---

## Що далі?

**Module 06: Hooks & Events** охоплює:

- Автоматизацію реакцій на системні події
- Валідацію перед комітом (pre-commit)
- Сповіщення після виконання дій
- Побудову автоматизації, що примусово виконується

---

**Завершили Module 05?** → Готові до [Module 06: Hooks & Events](06-hooks.uk.md)

---
**Локалізація**: [Serhii (MacPlus Software)](https://macplus-software.com)
*Остання синхронізація: Листопад 2026*
