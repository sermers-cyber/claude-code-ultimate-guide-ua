# Вікторина зі знань про Claude Code

Перевірте своє розуміння Claude Code за допомогою інтерактивних питань із варіантами відповідей.

[![Node.js](https://img.shields.io/badge/Node.js-18+-green.svg)](https://nodejs.org/)
[![Platform](https://img.shields.io/badge/Platform-macOS%20%7C%20Linux%20%7C%20Windows-blue.svg)]()

## Швидкий старт

```bash
# Перейдіть до каталогу вікторини
cd quiz

# Встановіть залежності
npm install

# Запустіть вікторину
npm start

# Або запустіть безпосередньо
node src/index.js
```

## Можливості

- **4 профілі користувачів**: Junior, Senior, Power User, Product Manager
- **17 категорій тем**: від швидкого старту до просунутих патернів
- **473 відібрані питання**: практичні знання, а не дрібна ерудиція
- **Миттєвий зворотний зв'язок**: вчіться на помилках завдяки поясненням
- **Посилання на документацію**: прямі посилання на розділи посібника
- **Облік балів**: бачте сильні та слабкі сторони
- **Збереження сесій**: історія зберігається в `~/.claude-quiz/`
- **Кросплатформність**: працює на macOS, Linux і Windows

## Використання

### Інтерактивний режим (рекомендовано)

```bash
npm start
```

Вам буде запропоновано:
1. Обрати свій профіль (Junior/Senior/Power User/PM)
2. Обрати теми (усі або окремі розділи)
3. Відповідати на питання варіантами A/B/C/D

### Параметри командного рядка

```bash
node src/index.js [options]

Options:
  -p, --profile <type>   Pre-select profile (junior|senior|power|pm)
  -t, --topics <list>    Quiz specific sections (1-17, comma-separated)
  -c, --count <n>        Limit number of questions (1-50)
  -d, --dynamic          Enable dynamic question generation via claude -p
  -h, --help             Show help message
  -v, --version          Show version
```

### Приклади

```bash
# Інтерактивний режим
npm start

# Профіль Senior, типові теми
node src/index.js -p senior

# Power user, окремі теми (Agents, Hooks, MCP)
node src/index.js -p power -t 4,7,8

# Швидка вікторина з 10 питань
node src/index.js -c 10

# Профіль Junior із динамічною генерацією
node src/index.js -p junior -d
```

## Приклад сесії

Ось як виглядає типова сесія вікторини:

```
============================================================
   CLAUDE CODE KNOWLEDGE QUIZ
   Master Claude Code: The Complete Guide
============================================================

? Select your profile: Senior Developer (40 min to mastery)
? Select topics to quiz: Custom selection...
? Select topics (space to toggle, enter to confirm):
  ◉ [2] Core Concepts
  ◉ [4] Agents
  ◉ [7] Hooks

------------------------------------------------------------
Starting quiz: 20 questions for senior profile
------------------------------------------------------------

------------------------------------------------------------
Question 1/20 [Core Concepts]

At what context percentage should you use /compact?

  A) 0-50%
  B) 50-70%
  C) 70-90%
  D) Only at 100%

? Your answer: C

✓ CORRECT!

Progress: █░░░░░░░░░░░░░░░░░░░ 1/20 | Score: 1/1 (100%)

------------------------------------------------------------
Question 2/20 [Hooks]

What exit code should a PreToolUse hook return to BLOCK an operation?

  A) 0
  B) 1
  C) 2
  D) -1

? Your answer: A

✗ INCORRECT. The correct answer is C) 2

Explanation:
Exit code 2 blocks the operation. Exit code 0 allows it to proceed.
Other exit codes are treated as errors and logged but don't block.

See: https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#72-creating-hooks
     (Line 4164)

Progress: ██░░░░░░░░░░░░░░░░░░ 2/20 | Score: 1/2 (50%)
? Continue to next question? Yes

... (more questions) ...

============================================================
   QUIZ COMPLETE
============================================================

Overall Score: 16/20 (80%)

By Category:
  Core Concepts       6/7  (86%)  [████████░░]
  Agents              5/7  (71%)  [███████░░░]
  Hooks               5/6  (83%)  [████████░░]

Weak Areas (< 75%):
  - Agents: Review section 4 in the guide

Recommended Reading:
  4. guide/ultimate-guide.md#4-agents

Time: 9 minutes 2 seconds

------------------------------------------------------------
? What would you like to do? (Use arrow keys)
❯ Retry wrong questions only
  New quiz (different questions)
  Exit
```

## Профілі

| Профіль | Питань | Зони фокусу |
|---------|-----------|-------------|
| **Junior Developer** | 15 | Розділи 1-3, 6 (основи) |
| **Senior Developer** | 20 | Розділи 2-4, 7, 9 (архітектура, автоматизація) |
| **Power User** | 25 | Усі розділи |
| **Product Manager** | 10 | Розділи 1-3, 16-17 (концептуальний і командний огляд) |

## Теми

| # | Тема | Ключові поняття |
|---|-------|--------------|
| 1 | Quick Start & Installation | Встановлення, перший workflow, базові команди |
| 2 | Core Concepts | Керування контекстом, Plan Mode, цикл взаємодії |
| 3 | Memory & Settings | CLAUDE.md, каталог .claude/, дозволи |
| 4 | Agents | Власні агенти, спеціалізація, оркестрація |
| 5 | Skills | Багаторазові знання, композиція skills |
| 6 | Commands | Slash-команди, власні команди |
| 7 | Hooks | Система подій, hooks безпеки, коди виходу |
| 8 | MCP Servers | Context7, Serena, Sequential, plugins |
| 9 | Advanced Patterns | The Trinity, CI/CD, композиція |
| 10 | Reference | Скорочення, усунення несправностей, щоденний workflow |
| 11 | Learning with AI | Навчальні workflow, звички рецензування, розвиток навичок |
| 12 | Architecture Internals | Архітектура runtime, контекст, інструменти та виконання |
| 13 | Security Hardening | Моделі загроз, безпечна конфігурація та перевірки безпеки |
| 14 | Privacy & Observability | Обробка даних, контроль приватності та телеметрія |
| 15 | AI Ecosystem | Додаткові інструменти та патерни інтеграції |
| 16 | Agent Harness & Context | Середовища виконання агентів і context engineering |
| 17 | Team Metrics for AI-Augmented Engineering | DORA, SPACE та метрики доставки з ШІ |

## Перебіг вікторини

```
┌─────────────────────────────────────────────┐
│          CLAUDE CODE KNOWLEDGE QUIZ         │
└─────────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────┐
│  Select Profile (Junior/Senior/Power/PM)    │
└─────────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────┐
│  Select Topics (All or Specific 1-17)       │
└─────────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────┐
│  Question 1/20 [Category]                   │
│                                             │
│  What is the recommended action when...?    │
│                                             │
│    A) Option A                              │
│    B) Option B                              │
│    C) Option C                              │
│    D) Option D                              │
└─────────────────────────────────────────────┘
                     │
            ┌────────┴────────┐
            ▼                 ▼
     ┌──────────┐      ┌──────────────────┐
     │ CORRECT! │      │ INCORRECT        │
     │          │      │ Correct: C       │
     │          │      │ Explanation...   │
     │          │      │ See: guide#...   │
     └──────────┘      └──────────────────┘
            │                 │
            └────────┬────────┘
                     ▼
              (Next Question)
                     │
                     ▼
┌─────────────────────────────────────────────┐
│           QUIZ COMPLETE                     │
│                                             │
│  Overall Score: 16/20 (80%)                 │
│                                             │
│  By Category:                               │
│    Core Concepts:  6/7  (86%)  [████████░░] │
│    Agents:         5/7  (71%)  [███████░░░] │
│    Hooks:          5/6  (83%)  [████████░░] │
│                                             │
│  Weak Areas: Agents (review section 4)      │
└─────────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────┐
│  [R] Retry wrong questions only             │
│  [N] New quiz (different questions)         │
│  [E] Exit                                   │
└─────────────────────────────────────────────┘
```

## Збереження сесій

Сесії вікторини автоматично зберігаються в `~/.claude-quiz/`:

```
~/.claude-quiz/
  sessions/
    2026-01-12_143052.json   # Дані окремої сесії
    2026-01-12_150623.json
  stats.json                  # Агрегована статистика
```

### Дані сесії містять:
- Обраний профіль і теми
- Відповіді на питання (правильно/неправильно/пропущено)
- Витрачений час
- Розподіл за категоріями
- Питання з помилками та правильні відповіді

## Динамічна генерація питань

Коли ввімкнено прапорець `--dynamic` і встановлено Claude CLI, вікторина може генерувати додаткові питання на льоту за допомогою `claude -p`:

```bash
node src/index.js -d
```

Для цього потрібно:
- Встановлений Claude CLI (`npm install -g @anthropic-ai/claude-code`)
- Налаштований активний API-ключ

Динамічні питання доповнюють статичний пул, коли:
- Статичний пул вичерпано для обраних тем
- Користувач просить нові питання
- Потрібна різноманітність для повторних вікторин

## Банк питань: джерело істини

Файли в `questions/*.yaml` **генеруються, а не редагуються вручну**. Єдиним
джерелом істини для питань вікторини є вебвікторина в репозиторії лендингу: по одному
Markdown-файлу на питання в `src/content/questions/`. YAML для CLI
перегенерується з нього.

Це зроблено свідомо. Банк CLI та веббанк колись розійшлися на два окремі
набори питань (різна загальна кількість, різні відповіді в тих самих слотах id). Одне
канонічне джерело плюс генератор не дозволяють цьому повторитися.

### Перегенерація YAML для CLI

З цього каталогу `quiz/`:

```bash
# Переписати questions/*.yaml із веббанку (сусідній репозиторій лендингу)
pnpm sync-from-web

# Перевірка в CI / перед push: завершується помилкою, якщо YAML розсинхронізовано з веббанком
pnpm sync-from-web:check
```

Генератор міститься в [`scripts/generate-from-web.mjs`](./scripts/generate-from-web.mjs).
За замовчуванням він читає `../../claude-code-ultimate-guide-landing/src/content/questions`;
передайте `--web <dir>`, щоб указати інше місце. Він зберігає заголовок кожної категорії
(назву, `source_file`) і замінює лише питання.

## Внесок питань

Додавайте чи редагуйте питання у **веббанку** (`src/content/questions/<NN-slug>/`),
а потім перегенеруйте YAML для CLI. Не редагуйте `questions/*.yaml` вручну: наступний
`sync-from-web` перезапише вашу зміну.

### Рекомендації щодо якості

**Добрі питання перевіряють:**
- Практичне застосування ("Коли слід...")
- Ухвалення рішень ("Який підхід найкращий для...")
- Розуміння ("Чому Claude...")
- Усунення несправностей ("Що б ви зробили, якби...")

**Уникайте:**
- Дрібної ерудиції ("Який точний синтаксис команди...")
- Суто завчання ("Перелічіть усі гарячі клавіші...")
- Деталей, що залежать від версії й можуть змінитися

### Подання питань

1. Зробіть fork репозиторію лендингу
2. Додайте питання у форматі Markdown у `src/content/questions/<NN-category-slug>/`
3. Переконайтеся, що `doc_reference` вказує на чинний розділ посібника
4. Запустіть `pnpm sync-from-web` у `quiz/`, щоб перегенерувати YAML для CLI
5. Подайте PR і з новим Markdown, і з перегенерованим YAML

## Усунення несправностей

### "No questions available"

- Перевірте, що для обраних тем є питання в каталозі `questions/`
- Переконайтеся, що YAML-файли чинні (скористайтеся валідатором YAML)
- Спробуйте обрати інші теми або "All topics"

### "Cannot find module 'yaml'"

```bash
cd quiz
npm install
```

### Вікторина зависає на вводі

- Переконайтеся, що запускаєте в інтерактивному терміналі
- Спробуйте натиснути Enter, якщо все застрягло
- Скористайтеся Ctrl+C, щоб вийти й перезапустити

## Ліцензія

Така сама, як у батьківського репозиторію: [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/)

---

**Частина**: [claude-code-ultimate-guide](https://github.com/FlorianBruniaux/claude-code-ultimate-guide)
