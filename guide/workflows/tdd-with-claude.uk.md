---
title: "TDD з Claude Code"
description: "Робочий процес розробки через тестування (TDD) з явними вказівками для циклів red-green-refactor"
tags: [workflow, tdd, testing]
---

# TDD з Claude Code

> **Рівень впевненості**: Tier 1, на основі офіційних рекомендацій Anthropic та широкої перевірки спільнотою.

Розробка через тестування (Test-Driven Development) з Claude потребує явних інструкцій. Зазвичай Claude намагається спочатку написати код реалізації, а вже потім тести. TDD вимагає протилежного підходу.

---

## Зміст

1. [TL;DR](#tldr)
2. [Проблема](#проблема)
3. [Налаштування](#налаштування)
4. [Цикл Red-Green-Refactor](#цикл-red-green-refactor)
5. [Інтеграція з функціями Claude Code](#інтеграція-з-функціями-claude-code)
6. [Антипатерни](#антипатерни)
7. [Розширені шаблони](#розширені-шаблони)
8. [Див. також](#див-також)

---

## TL;DR

```
Red → Green → Refactor

Але ви ПОВИННІ давати Claude чіткі вказівки:
"Write a FAILING test for [feature]. Do NOT write implementation yet."
```

---

## Проблема

Без явних вказівок Claude буде діяти так:
1. Спочатку напише код реалізації.
2. Потім напише тести, які успішно пройдуть для цієї реалізації.

Це суперечить самій суті TDD: тести мають визначати дизайн коду, а не просто перевіряти вже готове рішення.

---

## Налаштування

### Конфігурація CLAUDE.md

Додайте до файлу `CLAUDE.md` вашого проекту:

```markdown
## Testing Conventions

### TDD Workflow
- Always write failing tests BEFORE implementation
- Use AAA pattern: Arrange-Act-Assert
- One assertion per test when possible
- Test names describe behavior: "should_return_empty_when_no_items"

### Test-First Rules
- When I ask for a feature, write tests first
- Tests should FAIL initially (no implementation exists)
- Only after tests are written, implement minimal code to pass
```

### Хук для автозапуску тестів (опціонально)

Створіть `.claude/hooks/test-on-save.sh`:

```bash
#!/bin/bash
# Автоматичний запуск тестів при зміні файлів тестів
if [[ "$1" == *test* ]] || [[ "$1" == *spec* ]]; then
  npm test --watchAll=false 2>&1 | head -20
fi
```

---

## Цикл Red-Green-Refactor

### Фаза 1: Red (Створення тесту, що не проходить)

**Вказівка (Prompt)**:
```
Write a failing test for [feature description].
Do NOT write the implementation yet.
The test should fail because the function/method doesn't exist.
```

**Приклад**:
```
Write a failing test for a function that calculates the total price
of items in a cart, applying a 10% discount if total exceeds $100.
Do NOT implement the function yet.
```

**Очікувана поведінка Claude**:
- Створює файл тесту з тестовими сценаріями.
- Тести посилаються на функцію, якої ще немає.
- Запуск тестів завершується помилкою через відсутність функції.

**Перевірка**:
```bash
npm test  # Має завершитися помилкою "calculateCartTotal is not defined"
```

### Фаза 2: Green (Мінімальна реалізація)

**Вказівка (Prompt)**:
```
Now implement the minimum code to make these tests pass.
Only write enough code to pass the current tests, nothing more.
```

**Очікувана поведінка Claude**:
- Створює файл реалізації.
- Пише мінімально необхідний код, щоб тести пройшли.
- Уникає надмірного ускладнення (over-engineering).

**Перевірка**:
```bash
npm test  # Тести мають пройти успішно
```

### Фаза 3: Refactor (Очищення коду)

**Вказівка (Prompt)**:
```
Refactor the implementation to improve code quality.
Tests must stay green after refactoring.
Focus on: [readability / performance / removing duplication]
```

**Очікувана поведінка Claude**:
- Покращує якість коду без зміни його поведінки.
- Запускає тести для підтвердження того, що вони досі проходять.
- Документує всі важливі зміни.

---

## Інтеграція з функціями Claude Code

### З TodoWrite

Відстежуйте фази TDD у вашому списку завдань:

```
User: "Implement user authentication with TDD"

Claude створює завдання:
- [ ] RED: Write failing tests for login
- [ ] GREEN: Implement login to pass tests
- [ ] REFACTOR: Clean up login implementation
- [ ] RED: Write failing tests for logout
- [ ] GREEN: Implement logout
- [ ] REFACTOR: Clean up
```

### З Plan Mode (Режим планування)

Використовуйте режим планування для розробки стратегії тестування:

```
[Натисніть Shift+Tab для переходу в Plan Mode]

I need to implement a shopping cart with TDD.
Plan the test cases before we start writing any code.
```

Claude дослідить кодову базу в режимі «тільки для читання» та запропонує план тестування перед початком написання будь-якого коду.

### З хуками (Hooks)

Налаштуйте автоматичний запуск тестів після редагування файлів за допомогою хука PostToolUse:

```json
// У .claude/settings.json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "npm test --watchAll=false 2>&1 | head -20"
          }
        ]
      }
    ]
  }
}
```

### З суб-агентами (Sub-Agents)

Делегуйте написання тестів спеціалізованому агенту:

```
Use the test-writer agent to create comprehensive tests for
the UserService class, covering all edge cases.
Then I'll implement to pass those tests.
```

---

## Антипатерни

### Розрив верифікації (The Verification Gap)

**Розрив верифікації** — це стан відмови, коли агент звітує про завершення роботи над функцією до того, як пакет тестів підтвердить її працездатність. Це найпоширеніша причина зниження надійності роботи агентів у багатосесійних проектах, і її можна повністю запобігти за допомогою правильного проектування середовища тестування.

Три основні симптоми цього стану: агент виводить повідомлення про успіх до запуску будь-якої тестової команди; тести запускаються, але stderr ігнорується або не читається; проходять лише юніт-тести, тоді як критерії прийняття вимагали наскрізної (end-to-end) поведінки.

Рішення полягає у трирівневому стеку верифікації. Усі його рівні мають проходити успішно перед тим, як будь-яка функція буде позначена як `passing` у списку функцій:

1. **Lint** — перевірка синтаксису та стилю (найшвидша, виявляє очевидні помилки перед запуском тестів).
2. **Юніт- та інтеграційні тести** — функціональна коректність окремих компонентів.
3. **End-to-end тести** — поведінковий контракт з точки зору користувача або зовнішнього клієнта.

Кожен рівень виявляє свій клас помилок. Юніт-тести можуть проходити успішно навіть тоді, коли межі між компонентами зламані. End-to-end тести виявляють помилки передачі стану та проблеми життєвого циклу, які юніт-тести не здатні помітити. Пропуск будь-якого рівня створює розрив верифікації.

**Принцип незалежного оцінювача (independent evaluator)**: екземпляр агента, який пише код, не повинен бути тим самим викликом, який підтверджує його готовність. Це не через недовіру до моделі, а через те, як контекст впливає на оцінку. Агент, який щойно витратив дві години на створення функції, схильний інтерпретувати неоднозначний вивід занадто оптимістично. Хук PostToolUse або другий агент, який незалежно зчитує код виходу (exit code), позбавлені такої суб'єктивності. Хук у файлі `examples/hooks/bash/verification-gate.sh` реалізує саме такий шаблон.

Команда Anthropic задокументувала цей збій у своїх дослідженнях архітектури середовищ: у звичайному запуску (без додаткового середовища перевірки) їхній агент повідомив про готовність редактора ігор уже через 20 хвилин. При цьому нічого не працювало. Після додавання незалежного оцінювача до середовища та сама модель працювала 6 годин і видала повністю робочий результат (Джерело: [https://www.anthropic.com/engineering/harness-design-long-running-apps](https://www.anthropic.com/engineering/harness-design-long-running-apps)).

Тут також працює правило WIP=1: тримаючи лише одну функцію в статусі `active` одночасно, ви гарантуєте, що розрив верифікації (якщо він виникне) вплине лише на одну функцію, а не на кілька одночасно.

### Чого НЕ слід робити

| Антипатерн | Чому це неправильно | Правильний підхід |
|--------------|----------------|------------------|
| "Write tests for this feature" | Claude спочатку створить реалізацію | "Write FAILING tests that don't exist yet" |
| "Add tests and implementation" | Втрачається перевага підходу "тести спочатку" | Розділіть на дві окремі вказівки |
| "Make sure tests pass" | Спонукає до першочергової реалізації коду | "Write tests, then implement minimally" |
| Пропуск фази рефакторингу | Накопичується технічний борг | Завжди робіть рефакторинг після фази "green" |
| Робота над кількома функціями одночасно | Втрачається фокус | Одна функція на один цикл TDD |

### Типові помилки

**Помилка**: Прохання протестувати вже існуючий код.
```
# Неправильно
"Write tests for the existing calculateTotal function"

# Правильно
"Write tests for calculateTotal behavior, assuming function doesn't exist.
Then we'll verify the existing implementation passes."
```

**Помилка**: Об'єднання фаз "red" та "green".
```
# Неправильно
"Implement calculateTotal with tests"

# Правильно
"Write failing tests for calculateTotal. Stop there."
[Після написання тестів]
"Now implement to pass those tests."
```

---

## Розширені шаблони

### Property-Based Testing (Тестування на основі властивостей)

```
Write property-based tests for the sort function.
Properties to test:
- Output length equals input length
- All input elements exist in output
- Output is ordered
Use fast-check or similar library.
```

### Mutation Testing (Мутаційне тестування)

```
After tests pass, run mutation testing to find weak spots.
Identify tests that don't catch mutations.
```

> **Дивитися глибше**: JiTTesting автоматично застосовує мутаційне тестування під час створення Pull Request: згенеровані LLM, тимчасові тести, які не потребують обслуговування. Meta впровадила це у великих масштабах і отримала 4-кратне покращення виявлення регресій порівняно з традиційними тестами. Дивіться статтю [Just-in-Time Catching Test Generation at Meta](https://arxiv.org/abs/2601.22832) та [посібник з методологій](../core/methodologies.uk.md#jittesting-just-in-time-testing) щодо використання цього шаблону з Claude Code сьогодні.

### TDD з успадкованим кодом (Legacy Code)

```
I need to refactor legacyFunction.
First, write characterization tests that capture current behavior.
Then we'll refactor with confidence.
```

Характеризаційні тести фіксують те, що код робить сьогодні, а не те, що він мав би робити. Залишайте дивні виходи: у старій системі частина такої поведінки — це саме те, на що покладаються інші команди або бізнес, а агент охоче «виправить» її за зеленим набором тестів.

Не дозволяйте, щоб сесія, яка змінюватиме код, була єдиним автором тестів, що оцінюють цю зміну. Тоді вона напише набір, який закріплює реалізацію, що її вона ось-ось вигадає. Зафіксуйте поведінку в окремій сесії, в окремому коміті, який переглядають до початку рефакторингу, або нехай тести напише людина; потім починайте рефакторинг у новій сесії, якій сказано, що характеризаційні тести доступні лише для читання:

```
The tests in tests/characterization/ are read-only.
Refactor legacyFunction until they pass. If a test looks wrong,
stop and report it instead of editing it.
```

Хук `PreToolUse`, який забороняє `Edit` і `Write` у теці з характеризаційними тестами, перетворює цю інструкцію на гарантію. Джерело: Addy Osmani, [Brownfield Agentic Engineering](https://addyo.substack.com/p/brownfield-agentic-engineering) (вересень 2026); про зони та повноту міграції в успадкованих кодових базах див. [Legacy Codebase Modernization](https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#921-legacy-codebase-modernization).

#### Знайдіть шов, перш ніж писати перший тест

Характеризаційні тести припускають, що код можна запустити в тестовому середовищі. Успадкований код часто цьому опирається: він відкриває SMTP-з'єднання, читає годинник або звертається до бази даних просто зсередини функції, яку ви хочете зафіксувати. Відповідь Майкла Фезерса в *Working Effectively with Legacy Code* (2004, розділ 4) — **шов** (seam): «місце, де можна змінити поведінку програми, не редагуючи код у цьому місці». Кожен шов має **точку активації** (enabling point) — місце, де ви вирішуєте, яка поведінка виконуватиметься. Фезерс називає три види:

| Шов | Точка активації | Типове застосування |
|-----|-----------------|---------------------|
| Шов об'єкта (object seam) | Де об'єкт створюють або передають (конструктор, параметр, фабрика) | Перший вибір в об'єктно-орієнтованому коді |
| Шов компонування (link seam) | Поза кодом: classpath, лінкер, розв'язання модулів (`jest.mock()` — найближчий аналог у JavaScript) | Жорстко прописані імпорти, які не хочеться редагувати |
| Шов препроцесора (preprocessing seam) | Макроси та прапорці компілятора | C і C++ |

І шов, і точка активації працюють як [семантичні якорі](../ultimate-guide.uk.md#29-semantic-anchors): Claude знає цю книжку, тож їхня назва дає структуровану відповідь замість загального «додайте кілька моків».

Коли шов є, обирайте тестового двійника за тим, що тесту потрібно від залежності. Ґерард Мезарош у *xUnit Test Patterns* (2007) називає п'ять видів; [таблиця в skill для TDD](https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/examples/skills/tdd-workflow.md#test-doubles) містить чотири з них:

| Двійник | Застосовуйте, коли тесту потрібно... |
|---------|--------------------------------------|
| Dummy | Заповнити параметр, який шлях коду ніколи не використовує |
| Stub | Керувати непрямим входом (що повертає залежність: поточний час, помилку) |
| Spy | Записувати непрямі виходи й перевіряти їх потім |
| Mock | Звіряти непрямі виходи з очікуваннями, заданими наперед |
| Fake | Замінити важку залежність робочою легкою (репозиторій у пам'яті) |

Фезерс наводить дві причини розривати залежність: *сприйняття* (sensing: ви не бачите, що зробив код) і *відокремлення* (separation: код узагалі неможливо запустити). Як практичне правило, для сприйняття потрібен spy або mock, для відокремлення — stub, fake або dummy. Стежте за термінологією: Фезерс називає свого двійника для сприйняття «fake object»; за Мезарошем, це spy. Для характеризаційних тестів spy зазвичай кращий за mock: ви записуєте, що код робить сьогодні, а не приписуєте йому поведінку.

**Один приклад від початку до кінця.** Ця функція не може виконатися в тесті: вона надсилає справжні листи й читає справжній годинник.

```ts
// src/billing/reminders.ts (before)
export function sendOverdueReminders(invoices: Invoice[]) {
  const mailer = new SmtpMailer(process.env.SMTP_HOST);
  const today = new Date();
  for (const inv of invoices) {
    if (!inv.paid && inv.dueDate < today) {
      mailer.send(inv.customerEmail, `Invoice ${inv.id} is overdue`);
    }
  }
}
```

1. Попросіть аналіз до будь-яких правок:

   ```
   Find the seams in sendOverdueReminders (Feathers, Working Effectively
   with Legacy Code). For each dependency that blocks a unit test, name the
   seam type and its enabling point, and say whether the test needs sensing
   or separation. Then pick a test double from Meszaros' taxonomy and justify
   it in one line. Do not change any code yet.
   ```

   Очікуваний результат: жодна із залежностей ще не має шва, бо обидві створюються всередині функції. Годинник — це непрямий вхід (stub), поштовий клієнт — непрямий вихід, який потрібно сприймати (spy).

2. Нехай Claude зробить найменшу зміну, що створює шви, і більше нічого:

   ```
   Create the two object seams with Parameterize Method. Keep the current
   behavior as default arguments so no production caller changes.
   No other edits.
   ```

   ```ts
   type Mailer = Pick<SmtpMailer, 'send'>;

   export function sendOverdueReminders(
     invoices: Invoice[],
     mailer: Mailer = new SmtpMailer(process.env.SMTP_HOST),
     now: () => Date = () => new Date(),
   ) {
     const today = now();
     // loop unchanged; only the two local declarations moved into the signature
   }
   ```

   Жоден тест ще не захищає цю правку, тож diff має бути тривіально придатним до перегляду: сигнатура, один змінений рядок, один видалений.

3. Зафіксуйте поведінку через шви, в окремій сесії, як описано вище:

   ```ts
   const now = () => new Date('2026-03-10T09:00:00Z');  // stub

   function sentTo(dueDate: string): string[] {
     const sent: string[] = [];
     const spy: Mailer = { send: (to) => { sent.push(to); } };
     const inv = invoice({ dueDate: new Date(dueDate), paid: false });  // test data builder
     sendOverdueReminders([inv], spy, now);
     return sent;
   }

   it('reminds on the due date itself, not only after it', () => {
     expect(sentTo('2026-03-10T00:00:00Z')).toHaveLength(1);
   });

   it('does not remind before the due date', () => {
     expect(sentTo('2026-03-11T00:00:00Z')).toEqual([]);
   });
   ```

   Перший тест фіксує дивацтво, яке варто зберегти: дати платежу не мають часу доби, тому `dueDate < today` істинне в будь-який момент саме в день платежу.

4. Перевірте результат, перш ніж йому довіряти:
   - Приберіть аргумент `now` із тестів: другий має стати червоним, інакше шов годинника не використовується.
   - Змініть порівняння на цілі дні (`inv.dueDate.toISOString().slice(0, 10) < today.toISOString().slice(0, 10)`) — це «виправлення», яке міг би зробити агент: перший тест має стати червоним. Якщо він лишається зеленим, він нічого не фіксує. Порівнюйте в UTC, як тут; геттери дати в локальному часі роблять результат залежним від часового поясу машини.

---

## Приклад сесії

### Запит користувача
```
Implement a URL shortener service with TDD.
```

### Фаза 1: Red
```
Let's use TDD. First, write failing tests for:
1. Shortening a URL returns a short code
2. Retrieving a short code returns original URL
3. Invalid URLs are rejected
4. Expired links return error

Do NOT implement anything yet.
```

### Фаза 2: Green
```
Tests are written and failing. Now implement the minimum
code to make them pass. Use an in-memory store for now.
```

### Фаза 3: Refactor
```
Tests pass. Now refactor:
- Extract URL validation to separate function
- Add proper error types
- Improve variable names

Run tests after each change to ensure they stay green.
```

---

## Див. також

- [AI Design Patterns: Template Method](../core/ai-design-patterns.uk.md#template-method): skill, що перелічує кроки, зі Stop hook, який перевіряє останній
- [../core/methodologies.uk.md](../core/methodologies.uk.md): повний довідник з методологій
- [Tight Feedback Loops](../ultimate-guide.uk.md): розділ 9.5
- [examples/skills/tdd-workflow.md](https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/examples/skills/tdd-workflow.md): шаблон skill для TDD
- [Anthropic Best Practices](https://www.anthropic.com/engineering/claude-code-best-practices)
- [task-management.uk.md](./task-management.uk.md): відстеження циклів TDD між сесіями за допомогою Tasks API
- [Superpowers](https://github.com/obra/superpowers): набір plugin, який примусово впроваджує TDD як обов'язковий бар'єр, код, написаний до появи тесту, що падає, видаляється і створюється заново з нуля. Суворіше дотримання правил, ніж за допомогою звичайних prompt.
- [TDD with Claude Code](https://www.florian.bruniaux.com/guides/tdd-with-claude-code/): окремий практичний посібник про той самий робочий процес

---
**Локалізація**: [Serhii (MacPlus Software)](https://macplus-software.com)
*Остання синхронізація: Травень 2026*
