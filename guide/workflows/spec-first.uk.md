---
title: "Розробка спочатку зі специфікацією (Spec-First) з Claude"
description: "Визначайте специфікації в CLAUDE.md перед початком реалізації для структурованої розробки"
tags: [workflow, architecture, config]
---

# Розробка спочатку зі специфікацією (Spec-First) з Claude

> **Confidence**: Рівень 2, валідовано багатьма виробничими командами та узгоджується з офіційними рекомендаціями SDD.

Визначайте, що саме ви хочете отримати, в CLAUDE.md ПЕРЕД тим, як просити Claude писати код. Одна добре структурована ітерація дорівнює 8 неструктурованим.

---

## Зміст

1. [Стисло (TL;DR)](#tldr)
2. [Патерн](#патерн)
3. [Інтерв'ю перед специфікацією (grill me)](#інтервю-перед-специфікацією-grill-me)
4. [Гранулярність завдань: вибір обсягу роботи для агентів](#гранулярність-завдань-вибір-обсягу-роботи-для-агентів)
5. [Шаблони специфікацій для CLAUDE.md](#шаблони-специфікацій-для-claudemd)
6. [Покроковий робочий процес](#покроковий-робочий-процес)
   - [Від ідеї до прототипу, бізнес-пілот і рев'ю на 7-й день](#від-ідеї-до-прототипу-бізнес-пілот-і-ревю-на-7-й-день)
7. [Інтеграція з інструментами](#інтеграція-з-інструментами)
8. [Коли використовувати](#коли-використовувати)
9. [Антипатерни](#антипатерни)
10. [Дивіться також](#дивіться-також)

---

## TL;DR

```
1. Write spec in CLAUDE.md
2. Claude reads spec automatically
3. Implementation follows spec exactly
4. Verify against spec
```

CLAUDE.md — ЦЕ і є ваш файл специфікації. Ставтеся до нього як до контракту.

---

## Патерн

Розробка спочатку зі специфікацією (Spec-First Development) змінює типовий процес кодування з ШІ:

```
Traditional:        Spec-First:
───────────         ──────────
Prompt → Code       Spec → Prompt → Code → Verify
  │                   │               │       │
  └─ Hope it's       └── Contract    └── Follows spec
     what you want        defined          └── Check against spec
```

Специфікація стає єдиним джерелом правди (source of truth), яке:
- Обмежує те, що створює Claude
- Документує рішення для команди
- Дозволяє перевірити повноту реалізації

Для більших ініціатив один файл специфікації можна розділити ще вище за течією. [Плейбук AI-native SDLC](https://claude.com/blog/the-ai-native-sdlc-playbook) від Anthropic (2026) називає ланцюжок із трьох документів, кожен із яких затверджує інший рев'юер, перш ніж буде написано наступний документ:

```
intent.md → spec.md → plan.md
   │            │          │
 PM gate    Tech gate   Approval before
(the "why")  (the "what")  code generation (the "how")
```

`intent.md` формулює проблему простою мовою, поки ще немає жодного технічного обрамлення (див. «З intent.md» нижче). `spec.md` є технічною специфікацією, яку цей посібник уже охоплює в решті цього розділу. `plan.md` є поточковим планом реалізації (порядок, ризик, докази), що затверджується до того, як Claude напише код, і відрізняється від самої специфікації.

> **Примітка щодо термінів: agentic SDLC, AI-native SDLC, «ADLC»**. Плейбук стверджує, що «agentic SDLC, AI SDLC або просто agentic software development» описують те саме зрушення. Деякі практики перейменовують його на «ADLC, Agentic Development Lifecycle». З цією абревіатурою слід бути обережним: Salesforce ([Agentforce architecture guide](https://architect.salesforce.com/docs/architect/fundamentals/guide/agent-development-lifecycle.html)) та IBM ([What is the ADLC?](https://www.ibm.com/think/topics/agent-development-lifecycle-adlc)) уже використовують ADLC для *Agent* Development Lifecycle, тобто процесу створення, тестування й експлуатації ШІ-агентів як продукту. В одному випадку ADLC означає, що агенти будують ваше програмне забезпечення, в іншому ви будуєте агентів. Якщо ви оцінюєте агентів як продукт, дивіться натомість [agent-evaluation.md](../roles/agent-evaluation.uk.md).

---

## Інтерв'ю перед специфікацією (grill me)

Перед написанням специфікації дозвольте Claude розпитувати вас, доки відкриті рішення не буде закрито. «Grill me» тепер позначає три різні практики, що відрізняються тим, хто кого розпитує і коли:

| Патерн | Хто питає | Коли | Результат |
|---|---|---|---|
| Gatekeeper ([Prompting as provocation](../ultimate-guide.uk.md#281-prompting-as-provocation)) | Claude екзаменує вас за готовим diff | Після реалізації, перед PR | Зміна, яку ви можете захистити |
| Interview-first spec (офіційна найкраща практика) | Claude інтерв'юює вас через `AskUserQuestion` | Перед реалізацією | `SPEC.md`, потім нова сесія для його реалізації |
| skill `/grill-me` (Matt Pocock) | Claude інтерв'юює вас уздовж дерева рішень | Перед будь-яким планом, специфікацією чи кодом, зокрема для рішень не про код | Закриті рішення в розмові; нічого не записується, якщо ви не попросите |

### Interview-first spec

Офіційні best practices рекомендують його для більших функцій ([Let Claude interview you](https://code.claude.com/docs/en/best-practices)):

```text
I want to build [brief description]. Interview me in detail using the AskUserQuestion tool.

Ask about technical implementation, UI/UX, edge cases, concerns, and tradeoffs. Don't ask obvious questions, dig into the hard parts I might not have considered.

Keep interviewing until we've covered everything, then write a complete spec to SPEC.md.
```

Коли специфікацію написано, документація радить розпочати нову сесію для її реалізації, з чистим контекстом і специфікацією як довідником.

### Skill `/grill-me`

Перша версія в [mattpocock/skills](https://github.com/mattpocock/skills) (MIT, лютий 2026) складалася з двох речень: «Interview me relentlessly about every aspect of this plan until we reach a shared understanding. Walk down each branch of the design tree, resolving dependencies between decisions one-by-one.» Пізніші версії додали такі механізми:

- **Рекомендована відповідь**: кожне запитання супроводжується рекомендацією агента, тож користувач реагує, а не складає відповідь з нуля.
- **Факти проти рішень**: агент сам з'ясовує все, на що можуть відповісти кодова база чи інструменти; користувачеві йдуть лише рішення.
- **Раунди за фронтом**: кожен раунд ставить усі рішення, чиї передумови вже закриті. Запитання, що залежить від іншого відкритого запитання, чекає на наступний раунд.
- **Шлюз підтвердження**: агент не діє, доки користувач не підтвердить спільне розуміння.

Логіка тепер живе в skill `grilling`, а `grill-me` є точкою входу, яку викликає користувач. Він не пише файлів: щоб зберегти рішення, попросіть специфікацію в тій самій сесії. Автор також радить тримати plan mode вимкненим під час grilling, бо plan mode змушує агента поспішати з планом замість того, щоб розпитувати.

### Режими відмови

Задокументовано автором ([grill-me docs](https://github.com/mattpocock/skills/blob/main/docs/productivity/grill-me.md), [grilling docs](https://github.com/mattpocock/skills/blob/main/docs/productivity/grilling.md), [9 things people get wrong](https://www.aihero.dev/things-people-get-wrong-with-grill-me-and-grill-with-docs)):

- **Пасивна згода**: прийняття кожної рекомендації дає план, який написав агент. За словами автора: «A session with no pushback from you is a session you didn't need.»
- **Питання, які розмова не вирішить**: макет, відчуття чи продуктивність під навантаженням потребують одноразового прототипу, а не більше запитань.
- **Надто великий обсяг**: сотні запитань означають, що роботу слід розділити.
- **Слабші та швидші моделі** все одно пропускають шлюз підтвердження. Задокументоване рішення: рядок у `CLAUDE.md` чи `AGENTS.md`, що забороняє агентові реалізовувати без дозволу.

Формат раундів є типовим, але деякі користувачі, зокрема ті, хто читає повільно або працює другою мовою, повідомляють, що їм краще підходить одне запитання за раз. Задокументований спосіб відмови від раундів у автора: один рядок у `CLAUDE.md`: `When grilling, ask one question at a time.`

### Докази

Контрольованого дослідження grill-me чи interview-first воркфлоу (переробки, дефекти, вартість) станом на жовтень 2026 року не знайдено. Суміжні бенчмарк-дослідження підтверджують саму передумову, але не розмір виграшу в реальному воркфлоу. Коли десятеро учасників відповідали на уточнювальні запитання моделі, [ClarifyGPT](https://github.com/ClarifyGPT/ClarifyGPT) підняв Pass@1 для GPT-4 на MBPP-sanitized із 70,96% до 80,80%. [HumanEvalComm](https://github.com/jie-jw-wu/human-eval-comm) переписує задачі HumanEval так, щоб вони були неоднозначними, суперечливими або неповними: на цих змінених задачах Pass@1 для ChatGPT становить 31,34% проти 65,58% на оригіналах, а уточнювальне запитання він ставить у 14,21% випадків.

### Що обрати

- Diff готовий, далі PR: промпт Gatekeeper.
- Більша функція, якій потрібна письмова специфікація: промпт interview-first.
- Нечітка ідея з кількома залежними рішеннями або рішення не про код: `/grill-me`.
- Невелика, оборотна або вже вирішена зміна: жоден із них. Поставте єдине блокувальне запитання або просто зробіть.

> **Джерело**: [Оцінка патернів grill-me](https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/docs/resource-evaluations/grill-me-interview-patterns.md)

---

## Гранулярність завдань: вибір обсягу роботи для агентів

Перед написанням специфікації переконайтеся, що завдання має правильний розмір. Агенти працюють найкраще з **вертикальними зрізами (vertical slices)**: тонкими наскрізними блоками роботи, які проходять через усі рівні архітектури, але реалізують рівно один завершений сценарій поведінки користувача (наприклад, «скидання пароля через email», а не «система автентифікації»).

**Практичне правило**: одна сесія агента = один вертикальний зріз. Якщо в описі завдання між двома сценаріями використання стоїть сполучник «та», розділіть його.

### Контрольний список якості PRD

Запускайте цю перевірку перед передачею будь-кого завдання агенту. Шість вимірів для перевірки:

| Вимір | Запитання | Попереджувальний знак (Red flag) |
|-----------|----------------|----------|
| **Чіткість проблеми** | Чи є формулювання проблеми однозначним? | «Покращити продуктивність» |
| **Тестовані критерії** | Чи можна перевірити виконання автоматично? | «Працює добре» |
| **Межі обсягу роботи** | Що саме знаходиться ПОЗА межами (out of scope) проєкту? | Нічого не вказано як виключене |
| **Візуальна готовність** | Як саме виглядає «готове» завдання для користувача? | Лише внутрішній технічний опис |
| **Чіткість вимог** | У специфікації немає деталей реалізації? | «Використовувати Redis для кешування» |
| **Термінологія** | Чи використовуються однакові терміни скрізь? | Змішування слів «користувач» та «акаунт» |

Завдання, яке не відповідає двом або більше вимірам, потребує доопрацювання перед тим, як агент почане працювати над ним. Аналіз специфікації дозволяє виявити неоднозначність, яка інакше спливе як неправильна реалізація в середині сесії.

```
❌ Too big, ambiguous:
"Add user authentication to the app"

  ✅ One vertical slice:
"Users can log in with email + password.
- POST /auth/login returns JWT on success, 401 on failure
- Invalid credentials show 'Email or password incorrect' (not which is wrong)
- Session expires after 24h
- Out of scope: OAuth, password reset, remember me"
```

### Список функцій (Feature List): машиночитаний контроль обсягу роботи

Список функцій — це файл JSON, який відстежує обсяг роботи та стан виконання кожної функції між сесіями агентів. На відміну від PRD, який описує загальний намір, список функцій є робочим контрактом для агента: він зчитується на початку сесії, оновлюється в кінці сесії та зберігається під час передачі завдань.

Кожен запис про функцію має три обов'язкові поля. Поле `description` повідомляє агенту, що саме потрібно створити. Поле `verify` — це команда оболонки (shell command), яка повертає 0 у разі успішного виконання. Це важливо, оскільки змушує визначати «готовність» як щось виконуване, а не просто описове. Поле `status` відстежує прогрес через односпрямований кінцевий автомат: `not_started` → `active` → `blocked` → `passing`. Запис може рухатися лише вперед, ніколи назад. Коли функція досягає статусу `passing`, у полі `evidence` фіксується те, що це доводить (назва тесту, вихідні дані команди або конкретний рядок логу).

Тут діє правило WIP=1: лише одна функція може перебувати в статусі `active` у будь-який момент часу. Кілька одночасно активних функцій призводять до частково виконаної роботи та неповної валідації.

Зберігайте `feature_list.json` у корені проєкту поруч із `AGENTS.md`. На початку сесії агент читає його, щоб знати, що було зроблено і що обрати далі. Наприкінці сесії агент записує оновлений стан і докази перед створенням коміту.

Список функцій працює разом із `claudedocs/handoffs/`. Разом ці два артефакти дають наступній сесії як робочий стан (які функції готові та перевірені), так і наративний контекст (що сталося, що було випробувано, що залишилося відкритим). Жоден з них не замінює інший.

Мінімальний приклад, що показує дві функції на різних етапах:

```json
{
  "features": [
    {
      "id": "feat-001",
      "name": "Document Import",
      "description": "Allow users to import PDF and TXT files from local filesystem",
      "verify": "npm test -- --grep 'document import'",
      "status": "passing",
      "evidence": "npm test: 12 passed, 0 failed (2026-05-01 14:22)"
    },
    {
      "id": "feat-002",
      "name": "Document Chunking",
      "description": "Split imported documents into ~500-character chunks with metadata",
      "verify": "npm test -- --grep 'chunking'",
      "status": "not_started",
      "evidence": "",
      "dependencies": ["feat-001"]
    }
  ]
}
```

Поле `evidence` для `feat-001` точно показує, що саме було запущено і коли. Запис `feat-002` перебуває в статусі `not_started` з порожнім полем `evidence`, очікуючи, поки `feat-001` буде підтверджено як `passing` перед тим, як стати `active`. Цей патерн описано в інженерному блозі Anthropic у статті [harness design for long-running applications](https://www.anthropic.com/engineering/harness-design-long-running-apps). Готовий до використання шаблон доступний у `examples/workflows/feature-list.json`.

---

## Шаблони специфікацій для CLAUDE.md

### Специфікація функції (Найбільш поширена)

```markdown
## Feature: [Name]

### Description
[2-3 sentences explaining the feature purpose]

### Capabilities
- MUST: [Required functionality]
- MUST: [Another requirement]
- SHOULD: [Nice to have]
- MUST NOT: [Explicit exclusions]

### Tech Stack
- Required: [lib1, lib2, lib3]
- Forbidden: [lib4, lib5]

### Acceptance Criteria
- [ ] Criterion 1: [Specific, testable condition]
- [ ] Criterion 2: [Another condition]
- [ ] Criterion 3: [Edge case handling]

### API Contract (if applicable)
- Endpoint: POST /api/[resource]
- Request: { field1: string, field2: number }
- Response: { id: string, created: timestamp }
- Errors: 400 (validation), 404 (not found), 500 (server)
```

### Специфікація архітектури

```markdown
## Architecture: [Component Name]

### Purpose
[Why this component exists]

### Boundaries
- Owns: [What this component is responsible for]
- Delegates to: [What other components handle]
- Does NOT: [Explicit non-responsibilities]

### Dependencies
- Upstream: [Components that call this]
- Downstream: [Components this calls]

### Data Flow
```
Input → Validation → Processing → Output
         │              │
         └─ Errors ─────┘
```

### Constraints
- Performance: [Response time, throughput]
- Security: [Auth requirements, data handling]
- Scalability: [Expected load, limits]
```

### Специфікація API

```markdown
## API: [Endpoint Name]

### Endpoint
`POST /api/v1/[resource]`

### Authentication
Bearer token required. Scopes: `read:resource`, `write:resource`

### Request
```json
{
  "field1": "string (required, max 255 chars)",
  "field2": "number (optional, default: 0)",
  "nested": {
    "subfield": "boolean"
  }
}
```

### Response
```json
{
  "id": "uuid",
  "created_at": "ISO 8601 timestamp",
  "data": { ... }
}
```

### Error Codes
| Code | Meaning | Response Body |
|------|---------|---------------|
| 400 | Validation failed | `{ "errors": [...] }` |
| 401 | Not authenticated | `{ "message": "..." }` |
| 403 | Not authorized | `{ "message": "..." }` |
| 404 | Resource not found | `{ "message": "..." }` |
```

---

## Покроковий робочий процес

### Крок 1: Напишіть специфікацію

Перед будь-яким запитом на реалізацію додайте специфікацію до CLAUDE.md:

```markdown
## Feature: User Authentication

### Capabilities
- MUST: Email/password login
- MUST: JWT token generation
- MUST: Password hashing with bcrypt
- SHOULD: Remember me functionality
- MUST NOT: Store plain text passwords

### Tech Stack
- Required: bcrypt, jsonwebtoken
- Forbidden: passport.js (too heavy for this use case)

### Acceptance Criteria
- [ ] User can login with valid credentials
- [ ] Invalid credentials return 401
- [ ] Token expires after 24h (or 7d with remember me)
- [ ] Passwords hashed with cost factor 12
```

### Крок 2: Вкажіть посилання на специфікацію в запиті

```
Implement the User Authentication feature as specified in CLAUDE.md.
Follow the acceptance criteria exactly.
```

Claude автоматично прочитає CLAUDE.md і дотримуватиметься специфікації.

### Крок 3: Перевірте відповідність специфікації

Після реалізації виконайте перевірку:

```
Review the implementation against the User Authentication spec.
Check off each acceptance criterion that's satisfied.
List any gaps.
```

### Крок 4: Оновіть специфікацію за потреби

Якщо вимоги змінюються під час реалізації:

```
Update the User Authentication spec to include:
- MUST: Rate limiting (5 attempts per minute)
Then implement the rate limiting.
```

### Від ідеї до прототипу, бізнес-пілот і рев'ю на 7-й день

Використовуйте артефакт, який можна перевірити, коли взаємодія з пропозицією здатна закрити відкрите продуктове рішення. Це може бути Claude Artifact, локальний макет або невеликий запускний прототип. Очевидне виправлення помилки не потребує шлюзу з прототипом. Наведений нижче приклад внутрішнього інструменту є запропонованим протоколом на синтетичних тікетах підтримки, а не звітом про розгорнутий інструмент чи виміряну вигоду.

Ідея полягає в поданні тріажу тікетів, яке допомагає підтримці виявляти випадки, що потребують інженерів. Тримайте формулювання проблеми, посилання на прототип, докази приймання та запис подальших дій у наявному issue або специфікації. Замовник володіє бізнес-пілотом, інженерний рев'юер володіє технічним прийманням, а названий мейнтейнер володіє інструментом після релізу.

| Етап | Дія та збережені докази | Умова продовження |
|---|---|---|
| Ідея | Зафіксуйте повторювану проблему тріажу, поточний ручний процес, цільових користувачів, гіпотезу та винятки. Використайте фіксований набір синтетичних тікетів з очікуваними рішеннями маршрутизації. | Замовник погоджує, що буде корисним результатом і хто його тестуватиме. |
| Прототип | Попросіть Claude побудувати найменше інтерактивне подання тріажу на синтетичних даних. Покажіть звичайний випадок, ескалацію та невизначений випадок. Позначте змокані інтеграції та збережіть відомі обмеження. | Замовник може оглянути воркфлоу й вирішити, чи фінансувати реалізацію. Переконлива демонстрація не є технічним прийманням. |
| Бізнес-пілот | Після потрібних інженерних перевірок і затвердження релізу дайте замовнику спробувати дозволений воркфлоу в погодженому середовищі. Зафіксуйте, чи придатна маршрутизація, де потрібне ручне виправлення та які випадки лишилися неперевіреними. | Окремо фіксуйте технічну верифікацію та бізнес-приймання. Відкриті дефекти зберігають власний статус. |
| Рев'ю на 7-й день | Через сім днів після того, як функція стала доступною користувачам пілота, перегляньте дозволені докази використання й зберіть відгуки замовника. Зафіксуйте охоплення, фактичне використання, успішну маршрутизацію, виправлення та витрати на підтримку порівняно з ручною базою. | Оберіть: продовжити, переглянути, подовжити пілот із новою датою рев'ю, затвердженою власником, або вивести з ужитку. Відсутність охоплення чи доказів означає «непереконливо», а не успіх. |

Перед релізом напишіть запис подальших дій із функцією та випущеною ревізією, власником пілота, датою доступності, датою рев'ю, цільовими користувачами, критерієм успіху та місцем зберігання доказів. 7-й день є каденцією пілота, а не універсальним порогом впровадження. Для рідкісних воркфлоу погодьте вікно рев'ю, яке може містити реальну нагоду скористатися функцією. Дивіться [метрики впровадження функцій](../ops/team-metrics.uk.md#рівень-адаптації-фіч-feature-adoption-rate).

Створіть нагадування в затвердженому планувальнику чи трекері issue й збережіть його ідентифікатор і статус виконання в цьому записі. Claude може підготувати payload нагадування або звіт про рев'ю з авторизованих джерел. Прохання в розмові не доводить, що майбутнє завдання існує або буде виконане. Оновлення дати доступності має також оновлювати дату рев'ю.

Приклад промпту для рев'ю:

```text
Perform the day-7 review for the feature in the linked follow-up record.
Read the linked specification, released revision, technical checks,
business-trial feedback and usage evidence available within my access.
Separate technical verification, business acceptance and observed use.
Report eligible users and actual exposure before calculating adoption.
Distinguish observations, assumptions, missing evidence and untested cases.
Recommend continue, revise, extend the trial or retire, with supporting evidence.
Leave the decision to the trial owner. Do not change code or send messages.
```

Тримайте цей цикл достатньо малим, щоб він закривав одне продуктове рішення. Успішний набір тестів підтверджує лише поведінку, яку він перевіряє. Успішний бізнес-пілот не доводить сталого використання, а спрацювання нагадування не доводить, що хтось перевіряв функцію.

---

## Інтеграція з інструментами

### З intent.md (висхідна постановка проблеми)

[Плейбук AI-native SDLC](https://claude.com/blog/the-ai-native-sdlc-playbook) від Anthropic (2026) ставить один документ перед специфікацією: `intent.md` формулює проблему природною мовою, його пише й затверджує той, хто володіє проблемою (зазвичай PM), до появи будь-якого технічного обрамлення. Claude починає чернетку `spec.md` лише після затвердження `intent.md`.

```markdown
# Intent: Reduce checkout abandonment on mobile

## Author
Jane Doe, Product (jane@company.com)

## Problem
32% of mobile checkouts are abandoned at the payment step, versus 11% on desktop.
Support tickets point to the card form timing out on slow connections.

## Constraints
- Must not change the payment provider (Stripe, contractual)
- Must ship before the Q3 promo (2026-09-01)

## Open questions
- Retry silently, or show a "reconnecting" state?
- Is Apple Pay / Google Pay in scope?

## Gate
Approved by: [PM name], [date]
```

Шлюз навмисно неформальний: PM підписує формулювання проблеми, а не якісь деталі реалізації. Після затвердження `spec.md` успадковує обмеження й відкриті запитання як початкову межу. `plan.md`, третій документ у ланцюжку, є поточковим планом реалізації (вивід `/speckit.plan` зі Spec Kit або окремий файл, якщо Spec Kit не використовується) із власним шлюзом: технічний рев'юер затверджує його до того, як Claude напише будь-який код.

### Зі Spec Kit (для нових проєктів / Greenfield)

```bash
# Install Spec Kit (requires Python 3.11+ and uv)
uv tool install specify-cli
specify init my-project --integration claude

# Use slash commands
/speckit.constitution  # Define project guardrails
/speckit.specify       # Write feature specs
/speckit.plan          # Create implementation plan
/speckit.implement     # Build from spec
```

### З OpenSpec (для наявних проєктів / Brownfield)

```bash
# Install OpenSpec
npm install -g @fission-ai/openspec@latest
openspec init

# Use slash commands
/openspec:proposal "Add dark mode"  # Create change proposal
/openspec:apply add-dark-mode       # Implement changes
/openspec:archive add-dark-mode     # Merge to specs
```

### З BMAD-METHOD (багаторольове планування)

BMAD-METHOD ([канонічний репозиторій](https://github.com/bmad-code-org/BMAD-METHOD)) може масштабувати обсяг планування відповідно до зміни. Його [актуальна документація воркфлоу](https://docs.bmad-method.org/) дозволяє очевидне невелике виправлення відправити просто в `bmad-build`. Більша чи невизначена зміна може почати з `bmad-spec` або використати повніші артефакти планування перед реалізацією. Наявність спеціалізованих агентів не означає, що кожна зміна потребує багаторольового ланцюжка.

```bash
# From the project root, install the method and choose a workflow suited to the change.
npx bmad-method install
```

Використовуйте повніше планування, коли рішення виграє від розділення потреби користувача, архітектури та досвіду на артефакти, придатні до рев'ю. Оновлюйте ці артефакти, коли докази змінюють вимогу. Сам метод не забезпечує ізольованого паралельного виконання; використовуйте окремі worktrees, якщо паралельні зміни інакше конфліктуватимуть.

Про стратегічний сценарій (коли накладні витрати BMAD на governance окупаються, а коли ні) дивіться [methodologies.md, розділ «Рівень 1: Стратегічна оркестрація»](../core/methodologies.uk.md#рівень-1-стратегічна-оркестрація).

### З spec-kitty (ізольоване паралельне виконання)

Spec-kitty ([Priivacy-ai/spec-kitty](https://github.com/Priivacy-ai/spec-kitty), MIT) додає те, чого бракує Spec Kit і BMAD-METHOD: кожен пакет роботи виконується у власному git worktree, а локальна kanban-панель відстежує цикл `next → review → accept → merge` і веде журнал аудиту кожного рішення про злиття. Спільнота менша, ніж у Spec Kit чи BMAD-METHOD (1449 зірок станом на 2026-07-27), але це найпряміша з нині доступних відкритих реалізацій принципу «ізольовані агенти, злиття під контролем людини».

```bash
pipx install spec-kitty-cli
```

### З Plan Mode

```
[Press Shift+Tab to enter Plan Mode]

I need to implement the Payment Processing feature.
Review the spec in CLAUDE.md and create an implementation plan.
```

---

## Коли використовувати

### Використовуйте Spec-First

| Сценарій | Чому |
|----------|-----|
| Нові функції | Визначення перед створенням |
| Проєкт API | Контракт має бути чітким |
| Архітектурні рішення | Документування обмежень |
| Співпраця в команді | Спільне розуміння |
| Складні вимоги | Зменшення неоднозначності |

### Пропускайте Spec-First

| Сценарій | Чому |
|----------|-----|
| Швидкі виправлення | Накладні витрати того не варті |
| Дослідження коду | Ви ще самі не знаєте, чого хочете |
| Прототипування | Вимоги часто змінюватимуться |
| Зміни в один рядок | Очевидний намір |

---

## Антипатерни

### Розмиті специфікації

```markdown
# Wrong
## Feature: User Management
- Handle users

# Right
## Feature: User Management
### Capabilities
- MUST: Create user with email, password, name
- MUST: Update user profile (name, avatar)
- MUST: Soft delete (mark as inactive, don't remove data)
- MUST NOT: Allow duplicate emails
```

### Специфікація після коду

```
# Wrong workflow
1. Ask Claude to implement feature
2. Write spec documenting what was built

# Right workflow
1. Write spec defining what should be built
2. Ask Claude to implement from spec
```

### Ігнорування заборонених речей (Forbidden)

```markdown
# Don't forget exclusions
### Tech Stack
- Required: React, TypeScript
- Forbidden: jQuery, vanilla JS, class components
             ↑ These constraints prevent drift
```

---

## Модульний дизайн специфікацій

**Патерн**: розділяйте великі специфікації на кілька окремих файлів замість того, щоб втискати все в один єдиний CLAUDE.md.

### Проблема: Монолітний CLAUDE.md

Коли розмір специфікації перевищує ~200 рядків, виникає кілька проблем:

- **Засмічення контексту (context pollution)**: Claude важко витягувати релевантну інформацію з роздутого контексту.
- **Когнітивне перевантаження**: розробники не можуть швидко знайти потрібні дані.
- **Труднощі з підтримкою**: оновлення однієї області вимагає навігації по непов'язаних розділах.
- **Зниження продуктивності**: великі файли CLAUDE.md уповільнюють завантаження та обробку контексту.

### Коли розділяти

| Поріг | Дія |
|-----------|--------|
| **<100 рядків** | Один файл CLAUDE.md є цілком прийнятним |
| **100-200 рядків** | Розгляньте можливість розділення, якщо існують окремі домени |
| **>200 рядків** | **Розділяйте негайно** — ви перевищили поріг когнітивного навантаження |
| **Багатокомандні проєкти** | Розділяйте за доменами/власністю незалежно від розміру |

### Стратегії розділення

**1. Розділення на основі функцій (Feature-Based Split)**

```
CLAUDE.md              # Core project context
CLAUDE-auth.md         # Authentication spec
CLAUDE-api.md          # API endpoints spec
CLAUDE-billing.md      # Payment processing spec
```

**2. Розділення на основі ролей (Role-Based Split)**

```
CLAUDE.md              # Shared conventions
CLAUDE-frontend.md     # UI/UX specifications
CLAUDE-backend.md      # API/database specs
CLAUDE-infra.md        # DevOps/deployment specs
```

**3. Розділення на основі процесів (Workflow-Based Split)**

```
CLAUDE.md              # Daily development rules
CLAUDE-testing.md      # Test specifications
CLAUDE-release.md      # Release process spec
CLAUDE-security.md     # Security requirements
```

### Патерн реалізації

**Основний CLAUDE.md** (залишається лаконічним):
```markdown
# Project: [NAME]

## Tech Stack
[Core technologies]

## Commands
[Daily commands]

## Rules
[Universal rules]

## Detailed Specs
- Authentication: See @CLAUDE-auth.md
- API Design: See @CLAUDE-api.md
- Testing: See @CLAUDE-testing.md
```

**CLAUDE-auth.md** (сфокусована специфікація):
```markdown
# Authentication Specification

## Capabilities
- MUST: JWT-based authentication
- MUST: Refresh token rotation
- MUST NOT: Store tokens in localStorage

## API Contract
[Detailed auth endpoints...]

## Security Requirements
[Specific auth security rules...]
```

**Переваги**:
- Claude може посилатися на конкретні файли за допомогою `@CLAUDE-auth.md`.
- Швидше завантаження контексту (тільки релевантні специфікації).
- Простіша підтримка (редагування одного домену без впливу на інші).
- Краща співпраця в команді (закріплення відповідальності за окремі файли специфікацій).

**Джерело**: Addy Osmani, ["How to write a good spec for AI agents"](https://addyosmani.com/blog/good-spec/) (Січень 2026)

---

## Операційні межі (Operational Boundaries)

**Патерн**: визначте чіткі межі для того, що ШІ-агенти повинні виконувати автоматично, про що повинні запитувати, а до чого ніколи не мають торкатися.

### Трирівнева система

Традиційні специфікації використовують бінарні обмеження (MUST/MUST NOT), але операційна робота вимагає трьох рівнів:

| Рівень | Значення | Відображення в Claude Code |
|------|---------|---------------------|
| **Always (Завжди)** | Виконувати автоматично без запитань | Режим автопідтвердження (Auto-accept mode) |
| **Ask First (Запитати)** | Отримати підтвердження користувача перед виконанням | Режим за замовчуванням (Default mode) |
| **Never (Ніколи)** | Заблокувати або вимагати Plan Mode | Режим планування (Plan mode) / Блокування хуками |

### Шаблон операційних меж (Operational Boundaries Template)

```markdown
## Boundaries

### Always (Auto-accept)
- Run tests after code changes
- Format code with Prettier
- Update imports when moving files
- Fix linting errors
- Add type annotations for untyped code

### Ask First (Confirm)
- Modify database schemas
- Add new dependencies
- Change API contracts
- Refactor >50 lines of code
- Update configuration files

### Never (Block)
- Push to production branch
- Commit secrets or API keys
- Delete data without backup
- Modify CI/CD workflows without review
- Bypass security checks
```

### Відображення на дозволи Claude Code

**Always → Permission Allowlist**:
```json
// In .claude/settings.json
{
  "permissions": {
    "allow": [
      "Bash(npm test*)",
      "Bash(npx prettier*)",
      "Bash(npx tsc*)"
    ]
  }
}
```

**Ask First → Default Mode**:
- Стандартна поведінка, запит підтвердження для кожної дії.
- Використовуйте для дій із помірним ризиком або впливом.

**Never → Plan Mode + Hooks**:
```bash
# Hook configured via settings.json (PreToolUse event)
#!/bin/bash
if [[ "$TOOL_NAME" == "Bash" ]] && [[ "$INPUT" =~ "git push origin main" ]]; then
  echo "BLOCKED: Direct push to main blocked. Use feature branches."
  exit 2  # Send feedback to Claude (non-zero exit blocks the action)
fi
```

### Структура прийняття рішень

Для кожної дії запитайте себе:
1. **Чи може це призвести до втрати даних?** → Ask First або Never.
2. **Чи можна це скасувати за допомогою git?** → Можливо Always.
3. **Чи впливає це на інших розробників?** → Ask First.
4. **Чи є це ризиком для безпеки?** → Never.
5. **Чи є це частиною стандартного робочого процесу?** → Always.

### Приклад: Розробка API

```markdown
### Always
- Run unit tests (npm test)
- Validate request schemas
- Generate API documentation
- Check response formats

### Ask First
- Add new API endpoints
- Change existing endpoint signatures
- Modify authentication requirements
- Update rate limiting rules

### Never
- Expose internal endpoints publicly
- Log sensitive user data
- Disable authentication checks
- Remove rate limiting
```

### Підтримка та оновлення

Переглядайте межі щоквартально:
- **Підвищення**: дії, які ніколи не викликали проблем (Ask First → Always).
- **Пониження**: дії, які призвели до проблем (Always → Ask First).
- **Блокування**: повторювані помилки (Ask First → Never).

**Джерело**: Addy Osmani, ["How to write a good spec for AI agents"](https://addyosmani.com/blog/good-spec/) (Січень 2026)

---

## Шаблон специфікації команд (Command Spec Template)

**Патерн**: документуйте виконувані команди з очікуваними вихідними результатами та обробкою помилок.

### Чому специфікації команд важливі

Більшість специфікацій зосереджені на **функціях** («створити автентифікацію»), але **команди** («як протестувати автентифікацію») є не менш критичними для ШІ-агентів.

### Структура шаблону

```markdown
## Commands

### [Command Category]

**Purpose**: [What this command accomplishes]

#### Command: `[actual command]`
**When**: [Trigger condition]
**Expected Output**: [What success looks like]
**Error Handling**: [What to do on failure]
**Flags**: [Important options]

---
```

### Приклад: Команди тестування

```markdown
## Commands

### Testing

#### Command: `pnpm test`
**When**: Before every commit, after code changes
**Expected Output**:
- All tests pass (exit code 0)
- Coverage ≥80% (lines, branches, functions)
- No console warnings
**Error Handling**:
- If tests fail → Fix tests, don't skip
- If coverage drops → Add tests for uncovered code
- If warnings appear → Investigate before committing
**Flags**:
- `--coverage`: Generate coverage report
- `--watch`: Run in watch mode for development
- `--silent`: Suppress console output

#### Command: `pnpm test:e2e`
**When**: Before merging to main, in CI pipeline
**Expected Output**:
- All E2E scenarios pass
- Screenshots captured for failures
- Test duration <5 minutes
**Error Handling**:
- If flaky → Investigate race conditions, don't retry blindly
- If timeout → Check network mocks, async handling
- If screenshots differ → Review UI changes deliberately
**Flags**:
- `--headed`: Run with visible browser (debugging)
- `--project chromium`: Test specific browser
```

### Приклад: Збірка та розгортання (Build & Deployment)

```markdown
## Commands

### Build

#### Command: `pnpm build`
**When**: Before deployment, in CI pipeline
**Expected Output**:
- Build succeeds (exit code 0)
- Output in `dist/` directory
- No TypeScript errors
- Bundle size <500KB (main chunk)
**Error Handling**:
- If TypeScript errors → Fix types, don't use `@ts-ignore`
- If bundle too large → Analyze with `pnpm analyze`, code-split
- If missing assets → Check public/ directory, update paths
**Flags**:
- `--mode production`: Production optimizations
- `--analyze`: Generate bundle size report

### Deployment

#### Command: `pnpm deploy:staging`
**When**: After PR approval, before production
**Expected Output**:
- Deployment succeeds
- Health check returns 200 OK
- Staging URL: https://staging.example.com
**Error Handling**:
- If health check fails → Rollback automatically
- If database migration fails → Don't proceed, investigate
- If environment vars missing → Check .env.staging, update secrets
**Never**: Run `pnpm deploy:production` manually — use CI/CD only
```

### Приклад: Команди бази даних

```markdown
## Commands

### Database

#### Command: `pnpm db:migrate`
**When**: After pulling schema changes, before development
**Expected Output**:
- Migrations applied successfully
- Database schema matches models
- Seed data loaded (development only)
**Error Handling**:
- If migration fails → Check database connection, review SQL
- If conflicts detected → Resolve migrations, don't force
**Never**: Run migrations in production manually — CI/CD only

#### Command: `pnpm db:reset`
**When**: Development only, never in staging/production
**Expected Output**:
- Database dropped and recreated
- All migrations applied
- Seed data loaded
**Error Handling**:
- If production check fails → Abort immediately, verify environment
**Safety**: Requires `NODE_ENV=development` check
```

### Інтеграція з CLAUDE.md

Посилання на специфікації команд у вашому основному файлі CLAUDE.md:

```markdown
## Commands
- Build: `pnpm build` (see spec for error handling)
- Test: `pnpm test` (must pass before commit)
- Deploy: See CLAUDE-deployment.md for full procedures
```

**Джерело**: Addy Osmani, ["How to write a good spec for AI agents"](https://addyosmani.com/blog/good-spec/) (Січень 2026)

---

## Антипатерн: Монолітний CLAUDE.md

### Проблема

**Симптом**: ваш файл CLAUDE.md розрісся до 300+ рядків, змішуючи специфікації функцій, контракти API, вимоги до тестування, процедури розгортання та командні конвенції.

**Наслідки**:
- **Неефективність контексту**: Claude завантажує всі 300 рядків для кожного запиту, навіть для найпростіших завдань.
- **Уповільнення відповіді**: великий контекст = повільніша обробка.
- **Зниження точності**: важливі деталі губляться в шумі.
- **Накладні витрати на підтримку**: оновлення одного розділу вимагає навігації по непов'язаному вмісту.
- **Конфлікти в команді**: кілька розробників редагують один і той самий файл = конфлікти злиття (merge conflicts).

### Реальний приклад

**До** (монолітний):
```markdown
# CLAUDE.md (387 lines)

## Tech Stack
[20 lines]

## Authentication
[45 lines of auth spec]

## API Endpoints
[67 lines of API contracts]

## Database Schema
[52 lines of schema rules]

## Testing
[38 lines of test requirements]

## Deployment
[41 lines of deployment procedures]

## Security Rules
[55 lines of security requirements]

## Team Conventions
[33 lines of coding standards]

## Git Workflow
[28 lines of branching rules]

## Troubleshooting
[8 lines of common issues]
```

**Проблема**: Claude завантажує всі 387 рядків, навіть коли користувач просто просить: «Add a new API endpoint for user profile».

**Після** (модульний):
```
CLAUDE.md (82 lines)          # Core context: tech stack, commands, rules
CLAUDE-auth.md (45 lines)     # Authentication spec only
CLAUDE-api.md (67 lines)      # API contracts only
CLAUDE-database.md (52 lines) # Database schema only
CLAUDE-testing.md (38 lines)  # Test requirements only
CLAUDE-deploy.md (41 lines)   # Deployment procedures only
CLAUDE-security.md (55 lines) # Security requirements only
```

**Перевага**: Claude завантажує CLAUDE.md (82 рядки) + CLAUDE-api.md (67 рядків) = 149 рядків (скорочення на 61%).

### Стратегія розділення

**Крок 1: Визначення доменів**

Шукайте логічні межі у вашій специфікації:
- Чи служать ці розділи різним цілям?
- Чи володітимуть різні члени команди різними розділами?
- Чи посилаються на деякі розділи частіше, ніж на інші?

**Крок 2: Витяг у сфокусовані файли**

Перемістіть специфічний для домену вміст в окремі файли:

```bash
# Keep in CLAUDE.md (always loaded)
- Tech stack (unchanging baseline)
- Daily commands (frequent reference)
- Universal rules (apply to all work)

# Extract to domain files (load on demand)
- Feature specs → CLAUDE-[feature].md
- API contracts → CLAUDE-api.md
- Testing → CLAUDE-testing.md
- Deployment → CLAUDE-deploy.md
```

**Крок 3: Створіть покажчик в основному CLAUDE.md**

```markdown
# Project: [NAME]

## Tech Stack
[Core technologies]

## Commands
[Daily commands]

## Rules
[Universal rules]

## Detailed Specifications
Reference these files for domain-specific requirements:
- @CLAUDE-auth.md — Authentication & authorization
- @CLAUDE-api.md — API endpoint contracts
- @CLAUDE-database.md — Schema and migrations
- @CLAUDE-testing.md — Test requirements
- @CLAUDE-deploy.md — Deployment procedures
- @CLAUDE-security.md — Security requirements
```

**Крок 4: Посилайтеся за потреби**

Claude може посилатися на конкретні файли:
```
User: "Add a new API endpoint for user settings"
Claude: Reads CLAUDE.md + @CLAUDE-api.md (relevant context only)
```

### Правила підтримки

1. **Тримайте CLAUDE.md <100 рядків** (тільки основний контекст).
2. **Файли доменів <150 рядків кожен** (якщо вони більші, розділяйте далі).
3. **Щоквартальний перегляд**: об'єднуйте рідко використовувані файли, розділяйте розділи, які часто оновлюються.
4. **Use @file references**: явно завантажуйте лише те, що вам потрібно.

### Контрольний список міграції

- [ ] Визначити домени в поточному CLAUDE.md (>200 рядків?).
- [ ] Створити окремі файли доменів (CLAUDE-[domain].md).
- [ ] Перемістити вміст у сфокусовані файли.
- [ ] Оновити основний CLAUDE.md індексом/посиланнями.
- [ ] Протестувати: попросити Claude виконати завдання з конкретного домену.
- [ ] Перевірити: оцінити використання контексту за допомогою `/status`.
- [ ] Задокументувати: ознайомити команду з новою структурою.

**Джерело**: Addy Osmani, ["How to write a good spec for AI agents"](https://addyosmani.com/blog/good-spec/) (Січень 2026)

---

## SDD vs TDD vs BDD

Станом на 2026 рік розробка, керована специфікацією (SDD), достатньо перетворилася на продукт, щоб її можна було змістовно порівняти зі старішими методологіями. Важлива відмінність полягає в тому, який артефакт керує процесом, а не в тому, яка методологія звучить краще абстрактно.

| Методологія | Керівний артефакт | Коли виконується | Роль людини | Чи можлива регенерація? |
|-------------|-------------------|--------------|------------|-----------------|
| TDD | Набір тестів | Після появи коду | Спочатку пише тести, потім код | Ні: тести документують те, що було створено |
| BDD | Gherkin (файли .feature) | Після появи коду | Пише сценарії, потім автоматизує | Частково: сценарії можуть керувати генерацією коду |
| SDD | Файл специфікації (структурована природна мова) | До появи коду | Пише специфікацію, затверджує контракт | Так: код є похідним результатом специфікації |

Практичний наслідок колонки SDD: якщо специфікація є керівним артефактом, то код у принципі можна регенерувати зі специфікації. Tessl доводить це до логічної межі з файлами, позначеними `// GENERATED FROM SPEC - DO NOT EDIT`. Martin Fowler зауважує, що це «spec-first» (код починається зі специфікації), але ще не «spec-anchored» (специфікація й код автоматично лишаються синхронізованими з часом). Жоден інструмент не розв'язав дрейф специфікацій (spec drift) надійно в масштабі продакшену.

Частота збоїв багатофайлових завдань без структури специфікації: pass@1 падає до 19,4% для багатофайлових інфраструктурних завдань проти 87% для ізольованих функцій (внутрішні дані Augment Code, рецензованого дослідження не опубліковано). Спрямоване твердження є правдоподібним: агенти без постійного контексту завдання частіше зазнають невдачі на завданнях, що охоплюють кілька файлів і компонентів. Конкретні цифри походять від вендора.

### Архітектура Factory.ai Missions

Найдокументованіша мультиагентна реалізація SDD у продакшені. Архітектура:

1. **Orchestrator** перетворює вимоги на контракти поведінкової валідації до початку будь-якої реалізації.
2. **Workers** реалізують функції паралельно, кожен отримує обмежений опис завдання з контракту.
3. **Validator agents** (змагальні, незалежні) перевіряють кожну реалізацію за контрактом. Вони не мають контексту від workers, лише контракт і результат.

На задокументованому проєкті клона Slack валідатори виявили 81 проблему до злиття будь-якого коду, що породило 34% усієї роботи з реалізації у вигляді «виправних функцій». Медіанна тривалість місії: 2 години. Найдовша задокументована місія: 16 днів. Factory.ai виносить стан у спільні артефакти (контракти валідації, списки функцій, визначення skill), щоб переживати скидання контексту під час багатоденних місій.

Довідник CLI (при використанні Factory.ai):

```bash
droid exec --mission path/to/mission.yaml    # Start a mission
droid status                                  # Check active missions
droid validate --mission-id <id>             # Run validators manually
```

### Повноциклові фабрики ПЗ на основі ШІ

Упродовж 2026 року з'явилася окрема категорія продуктів: комерційні платформи, що запускають увесь цикл від специфікації до розгортання за єдиним інтерфейсом, а не інструмент, який ви вбудовуєте в наявний воркфлоу. Пропозиція близька до архітектури Missions від Factory.ai, описаної вище (специфікація → паралельна ізольована збірка → валідація → розгортання), але запакована як керований сервіс, часто з орієнтацією на не-розробників як основних користувачів.

| Продукт | Що робить | Фінансування / стадія | Джерело |
|---------|--------------|------------------|--------|
| [Maleus](https://maleus.ai) | Користувач описує потребу природною мовою, команда спеціалізованих агентів перетворює її на специфікації для затвердження людиною, а потім постачає робочий застосунок, яким клієнт володіє у власному репозиторії та інфраструктурі | Рання стадія, Париж, засновник Adrien Maret | [maleus.ai](https://maleus.ai) |
| [Factory.ai](https://factory.ai) | Розглянуто вище (архітектура Missions) | $150M Series C, оцінка $1,5 млрд, під керівництвом Khosla Ventures із Sequoia (квітень 2026) | [TechCrunch](https://techcrunch.com/2026/04/16/factory-hits-1-5b-valuation-to-build-ai-coding-for-enterprises/) |
| [Blitzy](https://blitzy.com) | Реверс-інжинірить наявну кодову базу в граф залежностей, потім координує тисячі агентів паралельно протягом багатоденних запусків (кодові бази від 1M до 100M+ рядків) | $200M залучено, оцінка $1,4 млрд, під керівництвом Northzone (травень 2026) | [SiliconANGLE](https://siliconangle.com/2026/05/05/blitzy-raises-200m-1-4b-valuation-deploy-thousands-coding-agents-parallel/) |
| [Devin](https://devin.ai) (Cognition) | Розглянуто в [agentic-tools.md §2.1](../ecosystem/agentic-tools.uk.md#21-devin-cognition) | Оцінка $25 млрд (раунд квітня 2026) | Дивіться agentic-tools.md |

Жоден із них не покриває повний стек governance від початку до кінця. Розрив між «швидко генерує працюючий застосунок» і «генерує застосунок, якому можна довіряти в продакшені без того, щоб людина перечитувала кожен рядок» зводиться до чотирьох запитань, які варто поставити перед упровадженням будь-якого з них:

1. **Детермінований шлюз чи самооцінка LLM?** Чи окремий не-LLM процес (лінтер, перевірка типів, набір тестів, валідація контрактів) блокує злиття, чи агент, що написав код, сам вирішує, чи він правильний? Незалежні validator agents від Factory.ai (вище) та еталонна реалізація Spec-to-Code Factory (див. «Дивіться також» нижче) є двома задокументованими прикладами жорсткого шлюзу, відокремленого від агента-генератора. Найсильніший емпіричний аргумент надходить із досліджень безпеки, а не з презентацій вендорів: *Refute-or-Promote* ([arXiv:2604.19049](https://arxiv.org/abs/2604.19049), Abhinav Agarwal, 2026) провів 31-денну змагальну мультиагентну кампанію пошуку дефектів, де агентам доручали спростовувати кандидатів, а не підтверджувати їх, з обов'язковим емпіричним шлюзом валідації (виконання proof-of-concept) перед тим, як будь-яка знахідка дійшла до людини. Вона відсіяла приблизно 79% зі 171 кандидата і все одно дала чотири реальні CVE. Важливий результат: десять виділених LLM-рев'юерів одностайно схвалили padding oracle Блейхенбахера, якого не існувало, і лише емпіричний шлюз це виявив. Консенсус LLM-рев'юерів не замінює детерміновану перевірку: він може бути впевнено й одностайно хибним.
2. **Чи є механізм «стоп-лінії»?** Після N невдалих спроб виправлення конвеєр зупиняється й ескалює до людини, чи продовжує повторювати спроби, спалюючи токени? Мало хто з платформ документує це явно; сприймайте його відсутність як реальний ризик продакшену, а не крайній випадок.
3. **Чи простежується кожне рішення?** Чи можна постфактум відновити, який агент (і яка версія моделі) зробив певну зміну та чи схвалила її людина? Це найважливіше в регульованих середовищах і відповідає патерну журналу аудиту, який spec-kitty реалізує в масштабі OSS (вище).
4. **Чи лишається специфікація авторитетною після першої генерації?** Дивіться «Дрейф специфікацій» одразу нижче: більшість платформ розв'язують генерацію, мало хто розв'язує синхронізацію специфікації та коду, коли застосунок розвивається далі першої версії.

Наведені вище комерційні продукти закриті й керовані, тож їхній governance доводиться приймати на віру. Один відкритий проєкт відповідає на перші три запитання в коді, який можна інспектувати: [Liza](https://github.com/liza-mas/liza) (Apache-2.0, 363 зірки станом на 2026-08-28) обгортає CLI кодувальних агентів у детерміновані супервізори на Go, що забезпечують переходи станів, межі ролей, lease, вердикти рев'юерів, повноваження на злиття та відновлення. Він поєднує виконавця зі змагальним рев'юером, записує стан на YAML-дошці (blackboard) та ізолює паралельні завдання в git worktrees. Ці механізми роблять Liza еталонною архітектурою механічного governance, а не доказом готовності до продакшену. Worktrees не створюють пісочниці для процесів, кілька адаптерів провайдерів використовують широкі неінтерактивні режими дозволів, а успішний upstream CI переглянутого коміту не вимірює якість завдань на реальних тікетах. Дивіться [профіль Liza з прив'язкою до доказів](../ecosystem/agentic-tools.uk.md#48-liza) та оновлений [`docs/resource-evaluations/liza-mas-framework.md`](https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/docs/resource-evaluations/liza-mas-framework.md).

#### Фабрика від консалтингу: друга когорта

Таблиця вище містить самі лише стартапи з венчурним фінансуванням, через що категорія здавалася вужчою, ніж вона є. Упродовж першої половини 2026 року з'явилася окрема когорта: усталені консалтингові компанії пакують власну агентну платформу як продукт, а не продають погодинні ставки поверх чужих інструментів. Пропозиція інвертує стартапову. Якщо Blitzy веде з тисяч паралельних агентів, а Devin з автономності, ця когорта веде з governance, а швидкість продає другою.

| Платформа | Власник | Що вона заявляє | Перевірка з перших рук |
|----------|--------|---------------------|------------------|
| [AI/works](https://www.thoughtworks.com/ai/works/) | Thoughtworks | Реверс-інжиніринг застарілих систем за допомогою ШІ у збагачені специфікації, потім агентні воркфлоу, що генерують код, тести та конвеєри розгортання й регенерують уражені компоненти при зміні вимог. Просуває модель «3-3-3»: 3 дні до концепції, 3 тижні до прототипу, 3 місяці до MVP у продакшені | Запущено у січні 2026 ([прес-реліз](https://www.prnewswire.com/news-releases/aiworks-heralds-a-new-era-of-agile-and-next-generation-software-development-302664456.html)), сторінку продукту прочитано |
| [Agent/works](https://www.thoughtworks.com/en-us/about-us/news/2026/thoughtworks-launches-agent-works) | Thoughtworks | Площина керування та кероване середовище виконання для корпоративних агентів у будь-якій хмарі: центральний реєстр, дозволи на основі можливостей і обмежені в часі, а також «provable compliance before execution» (аналіз кожного можливого шляху через воркфлоу агента, щоб підтвердити існування принаймні одного повністю відповідного шляху) | Запущено 16 червня 2026, анонсовано на Databricks Data + AI Summit. AI/works працює на ньому |
| [Solario](https://solario.io/en/) | Спільна ініціатива з WeScale (Париж) | Вісім доменних агентів (Architecture, Design, Coding, Security, Testing, Modernization, Operations, Governance), позиціонування «Context Before Code. Governance Before Scale». Продається як повні програми модернізації або як фреймворк, ліцензований командам клієнтів | Сайт прочитано у липні 2026. **Механізм не задокументовано**: не розкрито ні базову LLM, ні модель розгортання, ні ціни, ні названого клієнта |
| IAKA / Autonyx | Sopra Steria | Суверенна мультиагентна платформа для критичних середовищ (оборона, енергетика), що заявляє відстежуваність, пояснюваність і верифікованість на кожному кроці, з європейським розташуванням даних і розгортанням on-prem | Повідомлено, незалежно для цього посібника не перевірено |
| AI Refinery Distiller | Accenture (з NVIDIA) | Агентний фреймворк, що охоплює пам'ять агентів, мультиагентну співпрацю, керування воркфлоу, governance та спостережуваність | Повідомлено, незалежно для цього посібника не перевірено |

Заява «provable compliance before execution» від Agent/works є тією, за якою варто стежити. Якщо вона робить те, що каже формулювання, це ближче до перевірки моделей (model checking), ніж до governance на рівні промптів, і це була б єдина механічна відповідь на запитання 3 у цій когорті. Сприймайте її як заяву, доки хтось не опублікує, як насправді працює аналіз шляхів.

Усе інше тут не проходить той самий тест, що й стартапи, а Solario не проходить його найгірше. Платформа, чиє позиціонування цілком зводиться до «Governance Before Scale», не публікує жодного речення про те, як примусово виконуються її запобіжники, чи детермінований шлюз блокує злиття, чи LLM сама оцінює свій вивід, і яка модель лежить в основі. Для цієї категорії це не дрібна прогалина: це весь продукт. Застосуйте запитання 5 нижче, перш ніж підписувати: просіть точку входу в середовищі виконання, що забезпечує шлюз, а не слайд, що його називає.

Жодна з п'яти не має продакшен-розгортання з виміряними результатами, перевіреними третьою стороною, що є тим самим доказовим становищем, що й у кожного стартапу в таблиці вище.

#### Декоративний CI: пастка (запитання 1 на практиці)

Найпоширеніший спосіб, у який запитання 1 зазнає невдачі, це не «немає шлюзу взагалі». Це шлюз, який запускається, але не блокує. Команда налаштовує повний конвеєр CI (перевірка типів, тести, лінтер, сканування секретів), бачить червоний X на невдалих PR і вважає, що злиття захищене. Воно не захищене, якщо ці завдання не налаштовано як *required status checks* на захищеній гілці. Без цього GitHub показує збій і все одно дозволяє злити прямо поверх нього. Конвеєр декоративний: він звітує, але не блокує.

Це було виявлено наживо на реальній кодовій базі T3 (tRPC/Prisma) під час аудиту harness: `gh api repos/OWNER/REPO/branches/BRANCH/protection` повернув `404 Branch not protected`, тож `ci.yml`, хук husky `pre-push` і навіть воркфлоу LLM-рев'ю були лише рекомендаційними. Виправлення займає 30 хвилин у налаштуваннях GitHub, але це найвигідніший за ROI крок у всьому harness, бо кожен інший шлюз є театром, доки це не зроблено.

Два польові застереження, коли ви закриваєте цю прогалину:

- **Агрегуйте, перш ніж вимагати.** Якщо ваші завдання CI використовують `paths-ignore` (щоб PR лише з документацією їх пропускав), пряме позначення цих завдань як required status checks дає зворотний ефект: перевірка лишається вічно «очікуваною» й ніколи не задовольняється, блокуючи PR назавжди. Додайте одне агрегувальне завдання-«gate», що залежить від справжніх завдань і завершується з кодом 0 на ігнорованих шляхах, і вимагайте лише його.
- **Детермінований блокувальник, LLM лише консультує.** Воркфлоу, що робить `exit 1`, коли будь-який рядок у заповненій LLM таблиці ЧЕРВОНИЙ, усе одно є самооцінкою LLM, лише розібраною детерміновано. Тримайте LLM-рев'ю як сигнал, але віддайте повноваження на злиття детермінованим завданням (перевірка типів, тести). PR із червоною таблицею LLM, але зеленими тестами має бути можливо злити; PR зі зламаними типами й зеленим вердиктом LLM не повинен зливатися.

### Дрейф специфікацій: відкрита проблема

Найважливіший ризик у продакшені: коли специфікація й код розходяться, агенти регенерують помилки, які вже було виправлено. Патерни пом'якшення:

- Версіонуйте специфікацію як артефакт git до будь-якого коміту реалізації.
- Команда Cursor `/evolve`: оновлює специфікацію, коли реалізація свідомо відхиляється від неї.
- Intent (агент): записує зміни назад у специфікацію під час реалізації, тримаючи обидва в синхроні.
- GitHub Spec Kit: зберігає специфікації в `.specify/` як версіоновані файли, які може читати CI.

Жоден інструмент не має надійного, широко прийнятого механізму автоматичної синхронізації специфікації та коду на довгих часових проміжках. Станом на травень 2026 року це основна відкрита проблема SDD.

---

## Дивіться також

- [workflows/agentic-software-factories.md](./agentic-software-factories.uk.md): оглядова карта всього спектра від однієї сесії до закритої платформи, а також дерево рішень про те, коли закрита фабрика справді перевершує нативний стек
- [../core/methodologies.md](../core/methodologies.uk.md): SDD та інші методології
- [Spec Kit Documentation](https://github.blog/ai-and-ml/generative-ai/spec-driven-development-with-ai-get-started-with-a-new-open-source-toolkit/)
- [OpenSpec Documentation](https://github.com/Fission-AI/OpenSpec)
- [tdd-with-claude.md](./tdd-with-claude.uk.md): Поєднання з TDD
- [Spec-to-Code Factory](https://github.com/SylvainChabaud/spec-to-code-factory) — Implémentation référence complète avec enforcement outillé (6 gates via Node.js, invariants "No Spec No Code" + "No Task No Commit", ~900K tokens/projet)
- [Superpowers](https://github.com/obra/superpowers): набір plugin (262 тис. зірок станом на 2026-07-27, раніше понад 95 тис.) із skill `brainstorming`, який впроваджує розробку спочатку зі специфікацією (spec-first) як обов'язковий етап: агент відмовляється писати код, поки специфікація не буде перевірена та затверджена. Встановлення: `/plugin install superpowers@claude-plugins-official`.

---
**Локалізація**: [Serhii (MacPlus Software)](https://macplus-software.com)
*Остання синхронізація: Травень 2026*
