---
title: "Dynamic Workflows"
description: "Багатоагентні конвеєри, оркестровані на JavaScript, з детермінованим потоком керування, паралельним розгалуженням і автоматичним відновленням"
tags: [workflow, agents, orchestration, parallel, ultracode]
---

# Dynamic workflows

> **JavaScript-скрипти, що оркеструють десятки й сотні субагентів в одній сесії**
> **Запроваджено**: v2.1.154 (2026-05-28) | **Ключове слово-тригер**: `ultracode` (перейменовано з `workflow` у v2.1.160, зміна, що ламає сумісність) | **Моніторинг**: `/workflows`

**Що це**: Dynamic workflow — це JavaScript-файл, що оркеструє кількох субагентів за допомогою невеликого набору примітивів (`agent`, `parallel`, `pipeline`, `phase`). Сам скрипт виконується як оркестратор і не споживає токенів; уся вартість у токенах походить від викликів `agent()`, які він робить. Середовище виконання обробляє ліміти паралелізму, валідацію схем, звітування про прогрес і відновлення після переривання.

**Коли запроваджено**: v2.1.154 (2026-05-28). Ключове слово-тригер було `workflow` до v2.1.160, де його перейменовано на `ultracode` (зміна, що ламає сумісність; наявні скрипти зі старим ключовим словом потрібно оновити).
**Час читання**: ~40 хв
**Передумови**: знайомство з [інструментом Agent](../core/tools-reference.uk.md#agent), базові знання JavaScript async/await

Ця сторінка документує одну з поверхонь реалізації в Claude Code. [Loop & Graph Engineering](../core/loop-graph-engineering.uk.md) пояснює, коли виправдана явна топологія і як визначати стан, переходи, правила зупинки, відновлення та судження незалежно від будь-якого фреймворку.

---

## Зміст

1. [Коли використовувати workflows (проти інструмента Agent і Skills)](#1-when-to-use-workflows-vs-agent-tool-vs-skills)
2. [Довідник примітивів](#2-primitive-reference)
3. [Поведінкові гарантії](#3-behavioral-guarantees)
4. [pipeline() проти parallel(): коли і чому](#4-pipeline-vs-parallel--when-and-why)
5. [Структуровані схемою виводи між фазами](#5-schema-structured-outputs-across-phases)
6. [Поширені патерни](#6-common-patterns)
7. [Реальний приклад workflow: dev-flow (від Issue до PR)](#7-real-workflow-example-dev-flow-issue-to-pr)
8. [Коли НЕ використовувати workflows](#8-when-not-to-use-workflows)
9. [Примітки щодо вартості та продуктивності](#9-cost-and-performance-notes)
10. [Дивіться також](#10-see-also)

---

## 1. Коли використовувати workflows (проти інструмента Agent і Skills)

Claude Code пропонує три споріднені поверхні для делегування та повторно використовуваних процедур: інструмент Agent, Skills і dynamic workflows. Неправильний вибір додає накладні витрати або залишає передбачену гарантію невиконаною.

**Використовуйте інструмент Agent безпосередньо**, коли завдання — це один субагент, що робить одну річ. Інструмент Agent є будівельним блоком. Обгортання одного виклику `agent()` у файл workflow додає зайвий обхід і скрипт, який треба підтримувати, без жодної вигоди.

**Використовуйте Skill**, коли знання чи процедура повторно використовуються в межах оголошеної сфери належності, а Claude має адаптувати судження до контексту. Skills керуються prompt і завантажуються в розмову. Вони не гарантують порядок, повторні спроби, обов'язкові артефакти, відновлення чи структуровану передачу даних між етапами.

**Використовуйте dynamic workflow**, коли виконуються три чи більше з цих умов: завдання має кілька етапів, що живлять один одного, деякі етапи можуть виконуватися паралельно, робота достатньо довга, щоб відновлення після переривання мало значення, потрібен відтворюваний шлях оркестрації або потрібні структуровані JSON-схеми для передачі даних між етапами. Детермінований шлях не робить вивід моделі детермінованим.

Межа рішення така: залишайте інтерпретацію, неоднозначність і судження про компроміси в prompt чи skills. Обов'язковий порядок, передумови, повторні спроби, правила зупинки та перевірки артефактів покладайте на harness. Нумеровані кроки самі по собі не вимагають коду; гарантія вимагає.

| Критерій | Інструмент Agent | Skill | Dynamic Workflow |
|-----------|-----------|-------|-----------------|
| Паралелізм | Ні | Ні | Так (parallel / pipeline) |
| Відновлення після переривання | Ні | Ні | Так (детермінований replay) |
| Структурована передача даних | Вручну | Вручну | Вбудована (валідація схеми) |
| Вартість токенів оркестратора | Помірна | Помірна | Нульова |
| Накладні витрати на налаштування | Немає | Низькі | Один JS-файл |
| Межа повторного використання | Один виклик | Оголошена персональна, проєктна, інструментальна або публічна сфера | Через вкладення `workflow()` |

---

## 2. Довідник примітивів

Файл workflow — це JavaScript-модуль із двох обов'язкових частин: експорту `meta` (структурний кістяк) та експортованої за замовчуванням функції (тіло виконання). Середовище виконання впроваджує в область видимості функції невеликий набір глобальних змінних.

### meta (обов'язково, чистий літерал)

`meta` має бути першим оператором у файлі. Вона оголошує ідентичність workflow і, за бажанням, іменовані фази, що відображаються в інтерфейсі `/workflows`.

```js
export const meta = {
  name: 'audit-and-verify',
  description: 'Review every changed file, then verify each finding',
  phases: [
    { title: 'Review' },
    { title: 'Verify' },
  ],
};
```

Поля `name` і `description` обов'язкові. `phases` необов'язкове, але рекомендоване: воно наповнює бічну панель прогресу в `/workflows`, щоб одразу бачити, яка фаза виконується.

`meta` має бути чистим літералом. Жодних змінних, шаблонних рядків, викликів функцій чи spread-операторів. Це обмеження існує, бо середовище виконання статично витягує `meta` до виконання скрипта, і саме це робить заголовки фаз видимими в інтерфейсі до початку workflow. Будь-який вираз, що потребує обчислення, ламає статичне видобування.

`meta` і виклики `phase()` утворюють «основу» (warp, фіксований структурний кістяк запуску). Виклики `agent()`, `parallel()` і `pipeline()` — це «піткання» (weft), що виконує реальну роботу, вплітаючись крізь цей кістяк.

### agent(prompt, options?)

`agent()` — основний будівельний блок. Кожен виклик створює окремий субагент з власним ізольованим вікном контексту. Субагенти не ділять стан; уся інформація має передаватися явно через prompt.

```js
export default async function ({ agent, parallel, pipeline, phase, log, args, budget }) {
  const summary = await agent('Summarize the diff in src/api/ added since yesterday.', {
    label: 'API diff summary',
    phase: 'Analyze',
    model: 'claude-sonnet-5-5',
  });

  return summary;
}
```

За замовчуванням `agent()` повертає звичайний текст. Коли надано `opts.schema` (об'єкт JSON Schema), середовище виконання валідує відповідь і автоматично повторює спробу, доки вивід не відповідатиме схемі. Саме цей механізм робить структуровані багатофазні конвеєри надійними: подальші етапи можуть покладатися на назви полів без крихкого парсингу регулярними виразами.

Ключові параметри:

| Параметр | Тип | Призначення |
|--------|------|---------|
| `schema` | об'єкт JSON Schema | Структурований вивід. Середовище виконання валідує та повторює спробу за невідповідності. |
| `phase` | string | Групує цей виклик під іменованою фазою в інтерфейсі `/workflows`. |
| `label` | string | Короткий підпис прогресу, що показується, поки агент працює. |
| `model` | string | Перевизначає модель для цього конкретного виклику. |
| `isolation` | `'worktree'` | Запускає агента в ізольованій копії репозиторію як git worktree. Дорого; використовуйте лише тоді, коли агенти паралельно змінюють файли і конфліктували б. |

### parallel(thunks[])

`parallel()` приймає масив функцій без аргументів (thunk), запускає всі одночасно й повертається, коли завершується найповільніша. Результати повертаються у порядку введення незалежно від порядку завершення.

```js
const MODULES = ['auth', 'payments', 'notifications'];

const reviews = await parallel(
  MODULES.map((mod) => () =>
    agent(`Review the ${mod} module for security issues.`, {
      phase: 'Review',
      label: mod,
    })
  )
);
```

`parallel()` — це бар'єрний примітив. Ніщо після нього не виконується, доки кожен агент у масиві не повернеться. Невдалі агенти повертають `null`, тому відфільтруйте перед використанням:

```js
const valid = reviews.filter(Boolean);
```

Використовуйте `parallel()`, коли всі результати мають бути доступні до початку наступного кроку: синтез за всіма знахідками, дедуплікація за виводами або рішення про дострокове завершення на основі загальної кількості.

### pipeline(items, ...stages)

`pipeline()` обробляє масив елементів через послідовність етапів перетворення. Кожен елемент проходить через усі етапи по порядку, але різні елементи можуть одночасно перебувати на різних етапах. У конвеєрі з 10 елементів і 3 етапів елемент 1 може бути на етапі 3, поки елемент 7 ще на етапі 1.

```js
const DIMENSIONS = [
  { id: 'security', prompt: 'Review for injection and auth issues.' },
  { id: 'performance', prompt: 'Review for N+1 queries and slow paths.' },
  { id: 'accessibility', prompt: 'Review for WCAG 2.1 AA compliance.' },
];

const results = await pipeline(
  DIMENSIONS,
  // Stage 1: generate findings
  (dim) =>
    agent(dim.prompt, {
      phase: 'Review',
      label: dim.id,
      schema: FINDINGS_SCHEMA,
    }),
  // Stage 2: verify each finding
  (findings) =>
    parallel(
      findings.issues.map((issue) => () =>
        agent(`Try to refute this finding: "${issue.title}". Is it a real problem?`, {
          phase: 'Verify',
          label: issue.title,
          schema: VERDICT_SCHEMA,
        })
      )
    )
);
```

Функції етапів отримують три аргументи: `(previousStageResult, originalItem, index)`. Використання `originalItem` на пізніших етапах є звичним, коли prompt етапу 2 потребує і результату етапу 1, і початкових вхідних даних.

Між етапами для різних елементів немає глобального бар'єра. Саме це робить `pipeline()` ефективним для незалежних елементів, що мають однакову послідовність етапів.

### phase(title)

`phase()` — це примітив спостережуваності. Він оновлює заголовок активної фази в інтерфейсі `/workflows` для всіх наступних викликів `agent()`, які не вказують власного `opts.phase`.

```js
phase('Discovery');
const files = await agent('Find all TypeScript files modified in the last 24 hours.');

phase('Analysis');
const issues = await parallel(/* ... */);

phase('Report');
const report = await agent('Synthesize these findings into an executive summary.');
```

Для детального групування всередині `pipeline()` або `parallel()` передавайте `phase` як параметр безпосередньо в `agent()`, а не викликайте глобальну функцію `phase()`, яка змагалася б із конкурентними викликами.

### Інші впроваджені глобальні змінні

Окрім `agent`, `parallel`, `pipeline` і `phase`, середовище виконання впроваджує ще чотири глобальні змінні:

**`log(message)`** видає повідомлення про прогрес на рівні workflow, видиме в інтерфейсі `/workflows` і в терміналі. Використовуйте його, щоб позначати основні переходи або повідомляти проміжні кількості.

```js
log(`Found ${specs.length} specs in approved status. Starting analysis.`);
```

**`args`** містить вхідні дані часу виконання, передані користувачем або батьківським workflow. Сприймайте його як звичайний об'єкт; його форма залежить від того, що надав викликач.

```js
const { issueNumber, targetBranch = 'main' } = args;
```

**`budget`** надає облік токенів для запущеного workflow. `budget.total` — налаштований максимум; `budget.spent()` повертає поточне використання; `budget.remaining()` повертає запас. Захищайте цим відкриті цикли:

```js
while (budget.remaining() > 50_000) {
  const batch = await agent('Find the next 10 unreviewed specs.');
  if (!batch.length) break;
  // process batch...
}
```

**`workflow(nameOrRef, args?)`** запускає іменований під-workflow всередині. Підтримується один рівень вкладення. Передайте рядок із назвою під-workflow або посилання імпорту:

```js
const auditResult = await workflow('security-audit', { target: 'src/api' });
```

---

## 3. Поведінкові гарантії

### Обмеження детермінізму

Скрипт оркестратора має бути чистим. Кілька конструкцій недоступні або викидають помилку:

- `Date.now()`, `Math.random()` і `new Date()` без аргументів заблоковано. Натомість передавайте часові позначки та seed через `args`.
- `require`, `fs`, `process` і будь-який мережевий виклик недоступні в області оркестратора. Уся взаємодія із середовищем відбувається всередині prompt `agent()`, де агент має повний доступ до інструментів.

Причина цих обмежень — відновлення. Коли перервана workflow перезапускається, середовище виконання програє скрипт оркестратора з початку й відтворює кешовані результати вже завершених викликів `agent()`. Якби оркестратор містив `Date.now()` чи `Math.random()`, відтворення давало б інші рішення про розгалуження, роблячи кешовані результати неузгодженими з новим шляхом виконання. Саме детермінізм робить відновлення безпечним.

### Валідація схеми та повторні спроби

Коли `agent()` викликається з `opts.schema`, середовище виконання валідує повернений текст як JSON щодо цієї схеми. Якщо валідація не проходить, воно повторює виклик агента з автоматичним prompt для виправлення. Цей цикл повторних спроб невидимий для оркестратора: `agent()` завершується лише тоді, коли вивід валідний. Практичний ефект: подальші етапи можуть деструктурувати `result.fieldName` без захисних перевірок, бо середовище виконання гарантує форму.

### Ліміти паралелізму та черга

Конкурентні виклики `agent()` обмежено значенням `min(16, cpu_cores - 2)`. Виклики понад ліміт автоматично ставляться в чергу й виконуються по мірі завершення запущених агентів. Це означає, що можна спокійно писати `parallel(items.map(...))` для великих масивів; середовище виконання запобігає «ефекту стада» без ручного розбиття на пакети в оркестраторі.

Два жорсткі ліміти захищають від скриптів, що вийшли з-під контролю:

- Загальна кількість викликів `agent()` у workflow: не більше 1000.
- Елементів в одному виклику `parallel()` або `pipeline()`: не більше 4096.

Якщо ваш дизайн workflow перевищував би 1000 агентів, завдання потрібно розкласти на під-workflows або обрати інший підхід.

### Відновлення та кешування результатів

Прогрес постійно фіксується контрольними точками. Коли workflow переривається (Ctrl+C, обрив мережі, перезапуск машини), відновлення програє скрипт оркестратора, але видає кешовані результати для кожного виклику `agent()`, що завершився до переривання. Агенти «холодного шляху» виконуються; агенти «теплого шляху» повертаються миттєво. Для workflow зі 200 агентів, перерваної на агенті 150, вартість відновлення — лише решта 50 агентів.

---

## 4. pipeline() проти parallel(): коли і чому

Це найпоширеніше джерело проблем із продуктивністю в проєктуванні workflow. Ці два примітиви схожі на вигляд, але мають принципово різну семантику.

**`parallel()` — це бар'єр.** Він запускає N агентів одночасно й блокується, доки не завершиться останній. Ніщо після рядка `await parallel(...)` не виконується, доки кожен агент у масиві не повернеться. Фактичний час дорівнює часу найповільнішого агента.

**`pipeline()` — це потокова обробка.** Елементи течуть крізь етапи без глобального бар'єра між етапами для різних елементів. Елемент 3 може увійти в етап 2, поки елемент 7 ще на етапі 1. Фактичний час залежить від глибини конвеєра й тривалості окремих етапів, а не від того, що найповільніший елемент має пройти всі етапи, перш ніж почне будь-який інший.

Концептуальне питання: «чи потребує крок N усіх результатів кроку N-1, перш ніж він може розпочатися?» Якщо так, правильний `parallel()`. Якщо елементи незалежні й кожному потрібен лише його власний результат попереднього етапу, правильний `pipeline()`.

### Дані про продуктивність

Бенчмарк спільноти, що порівнював ці два примітиви на еквівалентній роботі (3 елементи, по 2 етапи кожен), дав такі числа:

| Дизайн | Вартість у токенах | Фактичний час |
|--------|-----------|-----------|
| Бар'єр `parallel()`, 3 конкурентні агенти | ~78 844 токени | ~8.4 с |
| Невдало спроєктований `pipeline()`, 3 елементи × 2 етапи | ~158 982 токени | ~26.7 с |

Базова робота була ідентична. Версія з `pipeline()` додала удвічі більше токенів і втричі більшу затримку, бо дизайн змусив поставити бар'єр на межах етапів, якого дані не вимагали.

### Правило вибору

Починайте кожен workflow з кількома елементами з `pipeline()`. Додавайте бар'єр `parallel()` лише тоді, коли можете сформулювати конкретну причину: «prompt етапу 2 посилається на всі виводи етапу 1» або «потрібно достроково вийти, якщо загальна кількість за всіма елементами дорівнює нулю».

Конкретні приклади, де бар'єр `parallel()` виправданий:
- Дедуплікація всіх знахідок перед поданням результатів користувачеві
- Етап синтезу, prompt якого буквально каже «з огляду на всі знахідки попереднього етапу...»
- Перевірка дострокового виходу: якщо жоден елемент на етапі 1 не повернув знахідок, повністю пропустити етап 2

Конкретні приклади, де `pipeline()` — правильний вибір:
- Перевірити кожен файл на проблеми безпеки, потім незалежно верифікувати кожну знахідку по файлах
- Згенерувати підсумок для кожної специфікації, потім відформатувати кожен підсумок у картку звіту
- Проаналізувати кожен модуль, потім створити оцінкову картку для кожного модуля

### Патерни неправильного використання, яких слід уникати

**Використання `pipeline()` для незалежних вимірів, які належать до `parallel()`**: якщо виміри справді ортогональні (рев'ю безпеки проти рев'ю продуктивності проти рев'ю доступності) і жоден етап не потребує даних між вимірами, `parallel()` дає один бар'єр наприкінці й простіший.

**Використання `parallel()`, коли елементи незалежні**: якщо 50 файлів кожен незалежно проходять рев'ю + верифікацію, загортання всіх 100 викликів агентів в один `parallel([...50 рев'ю, ...50 верифікацій])` руйнує структуру етапів і робить код нечитабельним. `pipeline()` зберігає етапи явними.

**Відкриті цикли без захисту `budget`**: цикл виявлення `while(true)`, що породжує агентів, доки «не знайде більше елементів», досягне ліміту 1000 агентів і впаде. Захищайте кожен цикл:

```js
while (dry < 3 && budget.remaining() > 30_000) {
  // ...
}
```

---

## 5. Структуровані схемою виводи між фазами

Схеми перетворюють багатофазний конвеєр із ланцюжка перетворень «текст у текст» на типізований конвеєр з надійним доступом до полів на кожному етапі.

### Визначення схем

Об'єкти JSON Schema inline у файлі workflow:

```js
const FINDINGS_SCHEMA = {
  type: 'object',
  required: ['issues'],
  properties: {
    issues: {
      type: 'array',
      items: {
        type: 'object',
        required: ['title', 'description', 'severity'],
        properties: {
          title: { type: 'string' },
          description: { type: 'string' },
          severity: { type: 'string', enum: ['low', 'medium', 'high', 'critical'] },
        },
      },
    },
  },
};

const VERDICT_SCHEMA = {
  type: 'object',
  required: ['isReal', 'reason'],
  properties: {
    isReal: { type: 'boolean' },
    reason: { type: 'string' },
  },
};
```

### Виявлення → розуміння → план

Трифазний конвеєр, де кожна фаза спирається на попередню:

```js
export const meta = {
  name: 'spec-processor',
  description: 'Discover approved specs, understand each one, produce implementation plan',
  phases: [
    { title: 'Discovery' },
    { title: 'Understand' },
    { title: 'Plan' },
  ],
};

const DISCOVERY_SCHEMA = {
  type: 'object',
  required: ['specs'],
  properties: {
    specs: {
      type: 'array',
      items: {
        type: 'object',
        required: ['id', 'title', 'path'],
        properties: {
          id: { type: 'string' },
          title: { type: 'string' },
          path: { type: 'string' },
        },
      },
    },
  },
};

const UNDERSTANDING_SCHEMA = {
  type: 'object',
  required: ['id', 'summary', 'dependencies', 'estimatedComplexity'],
  properties: {
    id: { type: 'string' },
    summary: { type: 'string' },
    dependencies: { type: 'array', items: { type: 'string' } },
    estimatedComplexity: { type: 'string', enum: ['low', 'medium', 'high'] },
  },
};

export default async function ({ agent, parallel, phase, log }) {
  phase('Discovery');
  const discovery = await agent(
    'Find every spec file in docs/specs/ with status: approved in its frontmatter.',
    { schema: DISCOVERY_SCHEMA, label: 'Scanning specs' }
  );

  log(`Found ${discovery.specs.length} approved specs.`);

  phase('Understand');
  const understood = await parallel(
    discovery.specs.map((spec) => () =>
      agent(
        `Read the spec at ${spec.path} and identify its dependencies on other specs and modules.`,
        { schema: UNDERSTANDING_SCHEMA, label: spec.id }
      )
    )
  );

  const validUnderstood = understood.filter(Boolean);

  phase('Plan');
  const plan = await agent(
    `Given these ${validUnderstood.length} understood specs with their dependencies, 
    produce a topologically sorted implementation order. Specs with no dependencies come first.
    Specs: ${JSON.stringify(validUnderstood, null, 2)}`,
    { label: 'Building implementation plan' }
  );

  return plan;
}
```

### Патерн audit-and-verify

Дві ланцюжкові схеми реалізують змагальну верифікацію: перша хвиля генерує знахідки, друга намагається спростувати кожну з них:

```js
export default async function ({ agent, parallel, pipeline }) {
  const DIMENSIONS = [
    { id: 'security', prompt: 'Review the changed files for injection, auth, and access control issues.' },
    { id: 'performance', prompt: 'Review the changed files for slow queries, N+1 patterns, and unbounded loops.' },
    { id: 'data-integrity', prompt: 'Review the changed files for missing validations and race conditions.' },
  ];

  const results = await pipeline(
    DIMENSIONS,
    // Stage 1: generate findings per dimension
    (dim) =>
      agent(dim.prompt, {
        phase: 'Review',
        label: dim.id,
        schema: FINDINGS_SCHEMA,
      }),
    // Stage 2: verify each finding independently
    (findings) =>
      parallel(
        findings.issues.map((issue) => () =>
          agent(
            `A reviewer found this issue: "${issue.title}" (${issue.description}). 
            Try your hardest to refute it. Is it a real problem or a false positive?`,
            {
              phase: 'Verify',
              label: issue.title,
              schema: VERDICT_SCHEMA,
            }
          )
        )
      )
  );

  // Flatten and keep only confirmed findings
  const confirmed = results
    .flat()
    .filter((verdicts) => verdicts !== null)
    .flat()
    .filter((v) => v?.isReal);

  return confirmed;
}
```

Реальний запуск рев'ю PR з цим патерном скоротив 26 початкових знахідок до 16, оскільки етап змагальної верифікації відсіяв 10 хибнопозитивних.

---

## 6. Поширені патерни

### Змагальна верифікація

Друга хвиля агентів отримує завдання спростувати виводи першої хвилі. Це працює, бо агентам першої хвилі було доручено знаходити проблеми, а не оцінювати їхню серйозність чи обґрунтованість. Окремий агент-спростовувач, якому дано лише знахідку та вихідний матеріал, виловлює припущення рев'юера, що не виконуються в контексті.

Патерн узагальнюється за межі рев'ю коду: будь-яка ситуація, де перший прохід генерує кандидатів (баги, ключові слова, архітектурні ризики, помилки перекладу), виграє від окремого проходу спростування перед тим, як діяти на основі результатів.

### Loop-until-dry

Виявлення триває, доки K послідовних раундів не дадуть жодного нового елемента. Поєднання дедуплікації за множиною `seen`, лічильника `dry` і захисту `budget` дає безпечний цикл дослідження:

```js
const seen = new Set();
const confirmed = [];
let dry = 0;

while (dry < 2 && budget.remaining() > 30_000) {
  const raw = await agent(
    `Find up to 10 TypeScript files that are not yet covered by a test. 
    Already found: ${JSON.stringify([...seen])}. 
    Return an empty array if none remain.`,
    { schema: BATCH_SCHEMA }
  );

  const fresh = raw.files.filter((f) => !seen.has(f.path));

  if (!fresh.length) {
    dry++;
    continue;
  }

  dry = 0;
  fresh.forEach((f) => seen.add(f.path));
  confirmed.push(...fresh);
}
```

Множина дедуплікації має відстежувати елементи, відхилені в попередніх раундах, а не лише підтверджені. Якщо відстежувати тільки `confirmed`, один раз відхилені елементи знову спливатимуть у наступному раунді, і цикл ніколи не «висохне».

### Панелі суддів

Кілька незалежних агентів оцінюють той самий вивід, після чого виконується крок синтезу. Це корисно, коли судження одного агента недостатньо надійне для рішення з високими ставками (затвердження архітектури, підпис безпеки, бар'єр якості для автоматизованого розгортання).

```js
const JUDGE_SCHEMA = {
  type: 'object',
  required: ['score', 'confidence', 'rationale'],
  properties: {
    score: { type: 'number', minimum: 0, maximum: 10 },
    confidence: { type: 'string', enum: ['low', 'medium', 'high'] },
    rationale: { type: 'string' },
  },
};

export default async function ({ agent, parallel, log, budget }) {
  const artifact = await agent('Summarize the implementation in src/payments/ in detail.');

  const judges = await parallel([
    () => agent(`Judge this implementation for correctness: ${artifact}`, { schema: JUDGE_SCHEMA, label: 'judge-correctness' }),
    () => agent(`Judge this implementation for security: ${artifact}`, { schema: JUDGE_SCHEMA, label: 'judge-security' }),
    () => agent(`Judge this implementation for maintainability: ${artifact}`, { schema: JUDGE_SCHEMA, label: 'judge-maintainability' }),
  ]);

  const valid = judges.filter(Boolean);
  const avgScore = valid.reduce((sum, j) => sum + j.score, 0) / valid.length;
  log(`Panel scores: ${valid.map((j) => j.score).join(', ')} → avg ${avgScore.toFixed(1)}`);

  const synthesis = await agent(
    `Three judges reviewed the same implementation with these results: 
    ${JSON.stringify(valid, null, 2)}. 
    Produce a final verdict. Where judges disagree, explain the tension. 
    Recommend approve or request-changes with specific action items.`
  );

  return synthesis;
}
```

Версія із захистом budget запускає панелі суддів у циклі, доки не буде досягнуто консенсусу або не вичерпається бюджет:

```js
while (budget.total && budget.remaining() > 50_000) {
  const panel = await parallel([/* judges */]);
  const scores = panel.filter(Boolean).map((j) => j.score);
  const spread = Math.max(...scores) - Math.min(...scores);
  if (spread <= 1.5) break; // consensus reached
  // otherwise, run another round with the previous rationales as context
}
```

### Multi-strategy sweep

`parallel()` запускає кількох агентів, що підходять до тієї самої проблеми з різними стратегіями чи джерелами. Виводи синтезуються з перехресною верифікацією між джерелами. Типові застосування: дослідницькі завдання (офіційна документація + GitHub issues + пости в блогах), аналітичні завдання (суворий критик + оптимістичний читач + експерт предметної галузі).

```js
const strategies = [
  { label: 'official-docs', prompt: `Based only on official Anthropic documentation, explain...` },
  { label: 'community-reports', prompt: `Based only on GitHub issues and community reports, explain...` },
  { label: 'academic', prompt: `Based only on academic papers and benchmarks, explain...` },
];

const perspectives = await parallel(
  strategies.map((s) => () => agent(s.prompt, { label: s.label, schema: PERSPECTIVE_SCHEMA }))
);

const synthesis = await agent(
  `You have ${perspectives.filter(Boolean).length} independent perspectives on the same question. 
  Identify where they agree (high confidence), where they contradict (flag explicitly), 
  and produce a synthesis that is honest about uncertainty.
  Perspectives: ${JSON.stringify(perspectives.filter(Boolean), null, 2)}`
);
```

### Plan–execute–review

Трифазна структура, де перша фаза проєктує підхід (зазвичай швидко й дешево), друга фаза реалізує по файлах чи модулях (зазвичай дорога паралельна фаза), а третя перевіряє результат.

```js
// Phase 1: Plan (small cluster of agents or a single structured agent)
phase('Plan');
const plan = await agent(
  'Given the failing tests in __tests__/, design a step-by-step fix plan. Return a structured list of files to change and why.',
  { schema: PLAN_SCHEMA }
);

// Phase 2: Execute (implement per file in parallel where safe)
phase('Execute');
const changes = await parallel(
  plan.changes
    .filter((c) => !c.requiresSequentialOrder)
    .map((change) => () =>
      agent(`Apply this specific change: ${change.description}. File: ${change.file}. Do not touch other files.`, {
        label: change.file,
        isolation: 'worktree', // each agent gets isolated repo copy
      })
    )
);

// Phase 3: Review (adversarial check on the implemented changes)
phase('Review');
const verdict = await agent(
  'Run the test suite and review every changed file. Report pass/fail with specifics.',
  { schema: VERDICT_SCHEMA }
);
```

Зверніть увагу на параметр `isolation: 'worktree'` у фазі виконання. Коли кілька агентів паралельно писатимуть в один репозиторій, кожному потрібна ізольована копія, щоб уникнути конфліктів. Ізоляція через worktree дорога (повна копія репозиторію на агента) і її слід використовувати лише тоді, коли агенти справді одночасно змінюють файли.

---

## 7. Реальний приклад workflow: dev-flow (від Issue до PR)

Повний workflow, що бере номер GitHub issue і створює готовий до злиття pull request. Шість фаз, що охоплюють увесь цикл розробки:

```js
export const meta = {
  name: 'dev-flow',
  description: 'Issue to LGTM: analyze → plan → implement → test → evaluate → PR',
  phases: [
    { title: 'Setup' },
    { title: 'Analyze' },
    { title: 'Plan' },
    { title: 'Implement' },
    { title: 'Validate' },
    { title: 'Evaluate' },
    { title: 'PR' },
  ],
};

const ANALYSIS_SCHEMA = {
  type: 'object',
  required: ['summary', 'affectedModules', 'acceptanceCriteria', 'estimatedComplexity'],
  properties: {
    summary: { type: 'string' },
    affectedModules: { type: 'array', items: { type: 'string' } },
    acceptanceCriteria: { type: 'array', items: { type: 'string' } },
    estimatedComplexity: { type: 'string', enum: ['low', 'medium', 'high'] },
  },
};

const PLAN_SCHEMA = {
  type: 'object',
  required: ['steps'],
  properties: {
    steps: {
      type: 'array',
      items: {
        type: 'object',
        required: ['file', 'description', 'canParallelize'],
        properties: {
          file: { type: 'string' },
          description: { type: 'string' },
          canParallelize: { type: 'boolean' },
        },
      },
    },
  },
};

const VALIDATION_SCHEMA = {
  type: 'object',
  required: ['passed', 'failedTests', 'summary'],
  properties: {
    passed: { type: 'boolean' },
    failedTests: { type: 'array', items: { type: 'string' } },
    summary: { type: 'string' },
  },
};

export default async function ({ agent, parallel, phase, log, args }) {
  const { issueNumber, targetBranch = 'main' } = args;

  // Setup: read current state
  phase('Setup');
  const context = await agent(
    `Read the GitHub issue #${issueNumber} and the current state of the codebase. 
    Summarize the repo structure relevant to this issue.`,
    { label: `Issue #${issueNumber}` }
  );

  // Analyze: understand scope and acceptance criteria
  phase('Analyze');
  const analysis = await agent(
    `Given this context: ${context}
    Analyze issue #${issueNumber} in depth. 
    Identify every file that will need to change, define acceptance criteria, and estimate complexity.`,
    { schema: ANALYSIS_SCHEMA, label: 'Deep analysis' }
  );

  log(`Scope: ${analysis.affectedModules.length} modules, complexity: ${analysis.estimatedComplexity}`);

  // Plan: produce file-level implementation steps
  phase('Plan');
  const plan = await agent(
    `Based on this analysis: ${JSON.stringify(analysis, null, 2)}
    Produce a concrete, file-level implementation plan. 
    Mark which steps can be parallelized (no shared state) and which must be sequential.`,
    { schema: PLAN_SCHEMA, label: 'Implementation plan' }
  );

  // Implement: parallel where safe, sequential where not
  phase('Implement');
  const parallelSteps = plan.steps.filter((s) => s.canParallelize);
  const sequentialSteps = plan.steps.filter((s) => !s.canParallelize);

  if (parallelSteps.length > 0) {
    await parallel(
      parallelSteps.map((step) => () =>
        agent(
          `Implement this change: ${step.description}. 
          Only modify ${step.file}. Do not change any other file.`,
          { label: step.file, isolation: 'worktree' }
        )
      )
    );
  }

  for (const step of sequentialSteps) {
    await agent(
      `Implement this change: ${step.description}. File: ${step.file}.`,
      { label: step.file, phase: 'Implement' }
    );
  }

  // Validate: run tests and check acceptance criteria
  phase('Validate');
  const validation = await agent(
    `Run the full test suite. Then check each acceptance criterion: 
    ${analysis.acceptanceCriteria.map((c, i) => `${i + 1}. ${c}`).join('\n')}
    Report pass/fail per criterion.`,
    { schema: VALIDATION_SCHEMA, label: 'Test + AC check' }
  );

  log(`Tests: ${validation.passed ? 'PASS' : 'FAIL'}. Failed: ${validation.failedTests.length}`);

  if (!validation.passed) {
    // Attempt automated fix for failed tests
    phase('Evaluate');
    await agent(
      `These tests are failing: ${validation.failedTests.join(', ')}. 
      Diagnose and fix them without changing the acceptance criteria behavior.`
    );
  }

  // PR: open the pull request
  phase('PR');
  const pr = await agent(
    `Create a pull request from the current branch to ${targetBranch}.
    Title: derived from issue #${issueNumber} title.
    Body: summary of changes, acceptance criteria status, test results.
    Use gh pr create.`,
    { label: 'Opening PR' }
  );

  return pr;
}
```

Запуск цього workflow: скажіть Claude «ultracode dev-flow with issueNumber=42», і він автономно пройде весь цикл. Панель `/workflows` показує кожну фазу в міру її виконання.

---

## 8. Коли НЕ використовувати workflows

Dynamic workflows мають реальні накладні витрати: один JS-файл, який треба написати й підтримувати, термінальна панель для моніторингу та трохи довший час запуску, поки середовище виконання ініціалізується. Деякі ситуації цих витрат не виправдовують.

**Один агент, одне завдання.** Якщо роботу можна виразити одним викликом інструмента Agent, зробіть саме так. Workflow, що обгортає один виклик `agent()`, нічого не додає.

**Прості рефакторинги та виправлення багів.** Перейменування змінної у 20 файлах, виправлення друкарської помилки в конфігурації, додавання пропущеного імпорту: це завдання для одного агента, навіть якщо вони зачіпають кілька файлів. Накладні витрати оркестрації додають секунди й шум у логи.

**Повторно використовувані процедури, де кроки обирає Claude.** Якщо ви хочете, щоб Claude адаптував підхід залежно від того, що знайде під час виконання (а не фіксований граф етапів), правильний інструмент — Skill. Skills керуються prompt і компонуються; workflows керуються кодом і структурні.

**Відкрите дослідження без дисципліни budget.** Workflow, що запускає `agent()` у циклі без захисту `budget`, непередбачувано вичерпає ліміт у 1000 агентів. Якщо завдання справді не має обмеженої умови зупинки, безпечніша інтерактивна сесія під наглядом.

**Недетермінована логіка оркестрації.** Якщо скрипт workflow використовує `Math.random()` чи `Date.now()`, відновлення не працюватиме правильно. Скрипти, які неможливо зробити детермінованими, не повинні бути workflows.

**Слабкі або відсутні схеми між фазами.** Схеми технічно не обов'язкові, але workflows без них деградують до крихкого парсингу тексту. Якщо ви не можете визначити, які дані кожна фаза має передавати наступній, завдання, імовірно, краще виконати в одній розмовній сесії, де Claude синтезує все.

| Ситуація | Кращий підхід |
|-----------|----------------|
| Один агент, одне чітке завдання | Інструмент Agent безпосередньо |
| Повторно використовувана процедура, керована prompt | Skill |
| Проста правка в багатьох файлах | Один агент із редагуванням кількох файлів |
| Відкритий чат і дослідження | Інтерактивна сесія |
| Складна скоординована робота, кілька команд | Agent Teams (експериментально) |
| Багатоетапне, паралелізоване, відтворюване | Dynamic Workflow |

---

## 9. Примітки щодо вартості та продуктивності

Сам скрипт оркестратора коштує нуль токенів. Уся вартість у токенах походить від викликів `agent()`. З цього випливає корисний наслідок: оркестратор можна робити настільки складним, наскільки потрібно (цикли, умовні конструкції, визначення схем, допоміжні функції), без жодних додаткових витрат.

Паралельне розгалуження різко скорочує фактичний час для незалежних підзадач. Перевірений приклад із cookbook спільноти: 6 паралельних агентів виправили 5 README за 37 секунд, тоді як послідовне виконання тієї самої роботи зайняло б приблизно від 3 до 5 хвилин.

Послідовні етапи в `pipeline()` додають необхідну затримку на етап. Вартість виправдана, коли етапи мають справжні залежності за даними. Вона не виправдана, коли етапи є незалежними вимірами, що випадково мають спільну структуру коду; тоді дешевший `parallel()` з єдиним бар'єром наприкінці.

Практична модель вартості для типового workflow:

| Компонент | Вартість у токенах | Внесок у фактичний час |
|-----------|-----------|------------------------|
| JS оркестратора | 0 | Мілісекунди |
| Кожен виклик `agent()` | 2K–20K залежно від prompt і контексту | Послідовно: домінує; паралельно: амортизується |
| Повторна спроба через валідацію схеми | 1–2x на кожну невдалу валідацію | Рідко за добре спроєктованих схем |
| `isolation: 'worktree'` | Накладні витрати на копіювання Git | +2–5 с на агента у великих репозиторіях |

Правило великого пальця від спільноти Anthropic: «Якщо ви можете накреслити нетривіальну блок-схему з паралельними гілками, циклами й передачею даних між етапами, dynamic workflows, імовірно, доречні». Тест блок-схеми не дає вам хапатися за workflows у справді простих завданнях.

### Моніторинг і налагодження

Відкрийте `/workflows` у будь-якій сесії Claude Code, щоб побачити:
- Усі запущені та нещодавно завершені workflows
- Поточну фазу й підпис активного агента для запущених workflows
- Кількість агентів і стан завершення по фазах
- Повідомлення `log()`, випущені оркестратором

Коли workflow дає несподівані результати, найефективніший підхід до налагодження — додати виклики `log()` до і після основних етапів, щоб підтвердити проміжні дані, а потім додати чи посилити схеми, щоб ловити некоректні проміжні виводи рано, а не дозволяти їм поширитися до фінальної фази.

---

## 10. Дивіться також

- **[AI Design Patterns](../core/ai-design-patterns.uk.md#orchestrator-workers)**: Orchestrator-workers і Scatter-Gather як іменовані патерни з їхніми режимами відмов і перевірками
- **[Довідник інструментів, розділ Workflow](../core/tools-reference.uk.md#workflow-dynamic-workflows-v21154)**: канонічний опис інструмента, ключове слово-тригер і CLI-прапорці
- **[Agent Teams](./agent-teams.uk.md)**: експериментальна багатоагентна координація для завдань із переважно читанням, із peer-to-peer повідомленнями; відрізняється від workflows (без JS-оркестратора, координація через git)
- **[Plan-Driven Workflow](./plan-driven.uk.md)**: патерн «спочатку план, потім виконання» з людиною в циклі; доречний, коли ви хочете переглянути план до початку виконання
- **[Керування завданнями](./task-management.uk.md)**: Tasks API для збереження між сесіями; доповнює workflows, відстежуючи високорівневий стан поза сесією
- **[Spec-First](./spec-first.uk.md)**: написання специфікацій перед кодом; фаза виявлення в багатьох workflows виграє від наявних структурованих специфікацій
