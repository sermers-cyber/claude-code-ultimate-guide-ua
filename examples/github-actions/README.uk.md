---
title: "Воркфлоу GitHub Actions для Claude Code"
description: "Готові до використання CI/CD-воркфлоу, що інтегрують Claude Code у GitHub Actions"
tags: [ci-cd, devops, template, workflows]
---

# Воркфлоу GitHub Actions для Claude Code

Готові до використання воркфлоу GitHub Actions, що інтегрують Claude Code у ваш CI/CD-конвеєр.

## Передумови

1. **Встановіть Claude GitHub App** у свою організацію/репозиторій (потрібно, щоб Actions могли коментувати PR/issues)
2. **Додайте секрет з API-ключем**: у репозиторії перейдіть до Settings → Secrets and variables → Actions → New repository secret
   - Name: `ANTHROPIC_API_KEY`
   - Value: ваш API-ключ Anthropic з [console.anthropic.com](https://console.anthropic.com)
3. **Скопіюйте воркфлоу**: покладіть ці файли `.yml` у каталог `.github/workflows/`
4. **Протестуйте**: відкрийте тестовий PR або issue, щоб побачити їх у дії

## Доступні воркфлоу

### 1. Рев'ю коду (на основі prompt, `claude-code-review.yml`)

Винесений prompt, протокол проти галюцинацій і тригер на вимогу `/claude-review`.

Логіка рев'ю міститься в `.github/prompts/code-review.md`, тож ви можете вдосконалювати критерії, не чіпаючи YAML воркфлоу. Prompt просить Claude перевіряти кожну знахідку за допомогою `Read`/`Grep`. Ця інструкція не є виконуваним механізмом контролю приймання.

**Можливості:**
- Запускається на відкриття/синхронізацію/готовність PR **і** на коментар `/claude-review`
- Винесений prompt: редагуйте `code-review.md`, щоб налаштувати критерії під свій стек
- Протокол проти галюцинацій: жодних вигаданих номерів рядків чи неперевірених тверджень
- Структурований вивід: таблиця `🔴 MUST FIX` / `🟡 SHOULD FIX` / `🟢 CAN SKIP` + inline-коментарі
- `claude_args` обмежує запитувані інструменти переглядом файлів і публікацією рев'ю; перевірте доступність інструментів і дозволи в цільовому репозиторії
- Підтримка OAuth-токена (API-ключ не потрібен, якщо встановлено Claude GitHub App)

**Налаштування:**
```bash
# Copy both files into your repo
cp examples/github-actions/claude-code-review.yml .github/workflows/
mkdir -p .github/prompts
cp examples/github-actions/prompts/code-review.md .github/prompts/

# Add secret: CLAUDE_CODE_OAUTH_TOKEN (or ANTHROPIC_API_KEY)
# Install Claude GitHub App: https://github.com/apps/claude
```

**Налаштування під себе:**
Відредагуйте `.github/prompts/code-review.md`, щоб додати домовленості свого стеку:
```markdown
## Контекст стеку
- TypeScript strict mode, без `any`
- React Server Components, без `useEffect` для отримання даних
- Усі записи в БД мають проходити через шар репозиторіїв
- Нові маршрути API потребують інтеграційних тестів
```

**Межа приймання:**
Цей шаблон має рекомендаційний характер. Колишній gate обирав найновіше рев'ю, не прив'язуючи його до автора, запуску чи ревізії, вважав відсутній заголовок рівня серйозності нулем і міг бути пропущений після збою того, хто створює рев'ю. Його вилучено. Не перетворюйте рекомендаційне завдання на вердикт приймання.

Заміна потребує автентифікованих доказів для відповідної ревізії та обсягу, явних станів відмови й невідомого, а також окремо перевіреної політики репозиторію. [Симуляція контролю й відновлення](https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/examples/workflows/review-control-demo.py) тестує локальні випадки ухвалення рішень і відновлення з фіктивним пунктом призначення; це не робочий адаптер GitHub. Див. [посібник із рев'ю кількома провайдерами](../../guide/workflows/multi-provider-code-review.uk.md).

---

### 2. Рев'ю коду (пакетне, `claude-code-review-batched.yml`)

Для PR, що перевищують поріг кількості файлів (типово 75), один прохід рев'ю або завершується за тайм-аутом, або надто розпорошує увагу Claude між непов'язаними файлами. Цей воркфлоу розбиває дифф на пакети за доменами (migrations, backend-core, api-routes, frontend, tests-and-tooling), переглядає кожен пакет у паралельному matrix-завданні, а потім зводить усе в одну підсумкову таблицю серйозності.

**Можливості:**
- Завдання `check-size` рахує змінені файли й за порогом вирішує, чи запускати решту воркфлоу
- Matrix-завдання `review-batch`: по одному паралельному запуску на домен, обмеженому через `append_system_prompt`
- Завдання `synthesis` об'єднує коментарі всіх пакетів в одну таблицю без дублікатів
- Той самий файл prompt, що й у непакетному воркфлоу (`.github/prompts/code-review.md`), тож не потрібно підтримувати дубльовані критерії рев'ю

**Налаштування:**
```bash
cp examples/github-actions/claude-code-review-batched.yml .github/workflows/

# Edit the `matrix.domain` globs to match your actual directory layout.
# The shipped ones (prisma/migrations, src/server/services, src/components...)
# are a generic starting point, not a fit for every stack.
```

Запускайте його разом із `claude-code-review.yml`, а не замість нього. Обидва спрацьовують на ті самі події PR; те, який із них справді виконує рев'ю, вирішує поріг завдання `check-size`, тож тримайте `BATCH_THRESHOLD` узгодженим, якщо ви ще десь фільтруєте за кількістю файлів.

---

### 3. Автоматичне рев'ю PR (`claude-pr-auto-review.yml`)

**Розширена версія** з вичерпними критеріями рев'ю та розумною фільтрацією.

Створює структуроване рев'ю з inline-коментарями, щойно PR відкривається чи оновлюється.

**Можливості:**
- Автоматичне рев'ю коду під час відкриття/оновлення PR
- 8 напрямів уваги: коректність, безпека, продуктивність, читабельність, підтримуваність, тестування, найкращі практики, зміни, що ламають сумісність
- Зворотний зв'язок за пріоритетами: 🔴 Critical, 🟡 Important, 🟢 Suggestion, 💡 Tip
- Розумна фільтрація файлів (пропускає артефакти збирання, lock-файли)
- Пропускає чернеткові PR, щоб заощадити кошти
- Підсумкове рев'ю з оцінкою ризиків
- Обробка помилок і резервні сповіщення
- Inline-коментарі до конкретних рядків

**Використання:**
```bash
# Copy the workflow file
cp examples/github-actions/claude-pr-auto-review.yml .github/workflows/

# Open a PR - Claude will automatically review it
```

**Налаштування під себе:**
Додайте контекст, специфічний для проєкту, розкоментувавши розділ `append_system_prompt`:
```yaml
append_system_prompt: |
  Project conventions:
  - Use TypeScript strict mode
  - Follow functional programming patterns
  - All functions must have JSDoc comments
  - Test coverage must be >80%
```

---

### 4. Рев'ю безпеки (`claude-security-review.yml`)

Виконує сфокусоване сканування безпеки й публікує знахідки безпосередньо в PR.

**Можливості:**
- Аналіз безпеки для кожного PR
- Виявляє потенційні вразливості
- Враховує OWASP Top 10
- Публікує знахідки як коментарі до PR

**Конфігурація:**
```yaml
# Optional parameters in the workflow file:
exclude-directories: "docs,examples"    # Skip certain directories
claudecode-timeout: "20"                # Timeout in minutes
claude-model: "claude-3-5-sonnet-20240620"  # Model to use
```

**Використання:**
```bash
# Copy the workflow file
cp examples/github-actions/claude-security-review.yml .github/workflows/

# Every PR will be automatically scanned for security issues
```

---

### 5. Тріаж issues (`claude-issue-triage.yml`)

Коли відкривається нове issue, Claude пропонує мітки/рівень серйозності й публікує акуратний коментар із тріажем.

**Можливості:**
- Автоматична класифікація issues
- Пропозиції міток
- Оцінка серйозності (low, medium, high, critical)
- Виявлення дублікатів
- Коментар із тріажем у Markdown

**Автоматичне застосування міток (необов'язково):**
Щоб автоматично застосовувати запропоновані мітки, відредагуйте файл воркфлоу й змініть:
```yaml
- name: Apply labels (optional)
  if: ${{ false }}  # Change to true to auto-apply labels
```

**Використання:**
```bash
# Copy the workflow file
cp examples/github-actions/claude-issue-triage.yml .github/workflows/

# Open a new issue - Claude will automatically triage it
```

---

---

## Налаштування рев'ю кількома моделями

Якщо запускати Claude разом з іншими автоматизованими рецензентами (Gemini, Greptile, CodeRabbit), виявляються проблеми, які пропускає будь-яка окрема модель. Схема така: кожен сервіс робить рев'ю незалежно, а потім Claude зводить консенсус.

**Чому кілька моделей?**
Кожна модель має сліпі зони. Зауваження, які незалежно висунули 2+ рецензенти, мають високу цінність; унікальні знахідки кожної моделі дають покриття, якого інакше не було б.

### Рекомендований стек ($30/місяць фіксовано)

| Сервіс | Вартість | Сильна сторона |
|---------|------|----------|
| **Claude Code Review** (цей воркфлоу) | Входить до плану Anthropic | Глибоке міркування, розуміння кодової бази |
| **Gemini Code Assist** | $0 (входить до Google Workspace) | Незалежна LLM, інші навчальні дані |
| **Greptile** | ~$30/місяць фіксовано | Міжфайловий контекст, графи залежностей |

**Альтернатива**: CodeRabbit Pro ($15/розробник/місяць) додає інтерактивні запитання-відповіді та діаграми послідовностей.

### Налаштування

**Крок 1: встановіть Gemini Code Assist**

1. GitHub Marketplace → знайдіть "Gemini Code Assist"
2. Встановіть і авторизуйте у своєму репозиторії
3. Gemini автоматично переглядатиме нові PR (публікує як `gemini-code-assist[bot]`)
4. Необов'язкова конфігурація через `.gemini/config.yaml`:
   ```yaml
   code_review:
     comment_severity_threshold: MEDIUM
     max_comments_per_review: 20
   ```

**Крок 2: встановіть Greptile**

1. [greptile.com](https://greptile.com) → підключіть обліковий запис GitHub
2. Оберіть репозиторій, Greptile проіндексує кодову базу (~5 хв)
3. Налаштуйте в дашборді: цільові гілки, пріоритетні шляхи
4. Рев'ю публікуються як коментарі `greptile[bot]` до PR
5. Скопіюйте `.greptile/config.json`, `.greptile/rules.md` і `.greptile/files.json` з цього каталогу в корінь свого репозиторію й заповніть заглушки. Саме в `rules.md` міжфайловий RAG-пошук Greptile виправдовує себе: бізнес-інваріанти, що охоплюють кілька файлів (скінченний автомат, який забезпечується в одному сервісі, але не в іншому, правило обмеження області, яке має виконуватися для кожного запиту до чутливої таблиці). Не повторюйте правил, уже охоплених `.github/prompts/code-review.md` чи `.coderabbit.yaml`; розподіліть чекліст між трьома інструментами так, щоб кожен відповідав за окремий набір.

**Крок 3: увімкніть завдання synthesis**

У `claude-code-review.yml` приберіть `false &&` з умови завдання synthesis:

```yaml
# Before (disabled):
if: |
  false &&
  (github.event_name == 'pull_request' ...

# After (enabled):
if: |
  (github.event_name == 'pull_request' ...
```

**Крок 4: налаштуйте CodeRabbit (необов'язково)**

Скопіюйте `.coderabbit.yaml` з цього каталогу в корінь свого репозиторію. Відредагуйте `path_instructions` відповідно до свого стеку.

### Як працює зведення

Завдання `multi-reviewer-synthesis` у `claude-code-review.yml`:

1. Чекає 5 хвилин після рев'ю Claude (зовнішні боти публікують упродовж 2-3 хв)
2. Збирає всі рев'ю й коментарі через GitHub API
3. Мовчки пропускає роботу, якщо опублікувалося менше ніж 2 рецензенти
4. Claude визначає консенсус (ту саму знахідку позначили 2+ рецензенти) й унікальні знахідки
5. Публікує в PR структурований коментар зі зведенням

### Масштабування на великі PR і повторні push

Щойно репозиторій отримує реальне навантаження, з'являються дві проблеми: PR, що зачіпають десятки файлів за раз, і PR, у які роблять push п'ять разів до злиття. Базовий воркфлоу вище не розв'язує жодної з них.

**Великі PR**: понад певний поріг кількості файлів переходьте на `claude-code-review-batched.yml` (див. воркфлоу 2). Розбиття диффу за доменами тримає кожен пакет сфокусованим, а не змушує один прохід утримувати в контексті весь PR.

**Повторні push**: повторне рев'ю повного диффу після кожного push спалює токени на код, який Claude уже перевірив. Крок дельта-рев'ю порівнює SHA, вбудований у попередній коментар рев'ю (публікуйте його як HTML-коментар, наприклад `<!-- reviewed-sha: abc123 -->`), із SHA поточного push і обмежує наступне рев'ю лише файлами, зміненими відтоді. Цей репозиторій не постачає такий крок як готовий шаблон, бо він залежить від того, як ви вже відстежуєте стан рев'ю (коментар бота, мітка, окремий check run); схема така: прочитати останній маркер, виконати `git diff <last-sha>..HEAD --name-only`, передати цей список файлів в `append_system_prompt` так само, як пакетний воркфлоу обмежує обсяг за доменом.

### Файли в цьому каталозі

```
examples/github-actions/
├── README.md                        # Цей файл
├── claude-code-review.yml           # Рекомендаційне рев'ю + необов'язкове завдання synthesis
├── claude-code-review-batched.yml    # Matrix-рев'ю з розбиттям за доменами для великих PR
├── .coderabbit.yaml                 # Конфігурація CodeRabbit (скопіюйте в корінь репозиторію)
├── .greptile/
│   ├── config.json                  # Конфігурація рев'ю Greptile (скопіюйте в корінь репозиторію)
│   ├── rules.md                     # Звід міжфайлових інваріантів (скопіюйте в корінь репозиторію)
│   └── files.json                   # RAG-індекс «документ → glob» (скопіюйте в корінь репозиторію)
├── claude-pr-auto-review.yml        # Автоматичне рев'ю з inline-prompt (альтернатива)
├── claude-security-review.yml       # Сфокусоване сканування безпеки
├── claude-issue-triage.yml          # Воркфлоу тріажу issues
└── prompts/
    └── code-review.md               # Винесений prompt рев'ю (скопіюйте до .github/prompts/)
```

---

## Налаштування під себе

### Вибір моделі
Задайте параметр `CLAUDE_MODEL` або `claude-model` у воркфлоу:
```yaml
env:
  CLAUDE_MODEL: claude-3-5-sonnet-20240620
```

### Дозволи
Кожен воркфлоу оголошує мінімально потрібні дозволи:
- `pull-requests: write` для рев'ю PR
- `issues: write` для тріажу issues
- `contents: read` для читання вмісту репозиторію

Змінюйте їх, лише якщо ваша організація вимагає суворіших політик.

### Фільтрація за обсягом
Використовуйте фільтри `paths:`, щоб обмежити, коли запускаються воркфлоу:
```yaml
on:
  pull_request:
    paths:
      - 'src/**'
      - '!docs/**'
```

## Усунення несправностей

**У PR не з'являються коментарі:**
- Переконайтеся, що встановлено Claude GitHub App
- Перевірте, що воркфлоу має дозвіл `pull-requests: write`

**403 під час застосування міток:**
- Переконайтеся, що завдання має дозвіл `issues: write`
- Перевірте, що `GITHUB_TOKEN` має доступ до цього репозиторію

**Помилки Anthropic API:**
- Переконайтеся, що `ANTHROPIC_API_KEY` задано на рівні репозиторію
- Перевірте, що строк дії ключа не минув

**Синтаксичні помилки YAML:**
- Перевірте відступи: два пробіли на рівень вкладеності, без табуляцій
- Використовуйте валідатор YAML: [yamllint.com](https://www.yamllint.com/)

## Просунуте використання

### Поєднання воркфлоу
Запускайте кілька воркфлоу разом для всебічної автоматизації:
- Рев'ю PR + рев'ю безпеки для кожного PR
- Тріаж issues + автоматичне призначення міток для нових issues

### Власні prompts
Відредагуйте розділ `direct_prompt` у воркфлоу, щоб налаштувати фокус Claude:
```yaml
direct_prompt: |
  Review this PR focusing on:
  1. TypeScript type safety
  2. React performance patterns
  3. Accessibility compliance
  4. Test coverage
```

### Інтеграція з іншими actions
Поєднуйте з наявними воркфлоу:
```yaml
jobs:
  tests:
    runs-on: ubuntu-latest
    steps:
      - name: Run tests
        run: npm test

  claude-review:
    needs: tests  # Run after tests pass
    runs-on: ubuntu-latest
    steps:
      - uses: anthropics/claude-code-action@main
        # ...
```

## Міркування щодо вартості

Ці воркфлоу витрачають кредити Anthropic API:
- **Рев'ю PR**: ~$0.10-$0.50 за рев'ю (залежно від розміру диффу)
- **Рев'ю безпеки**: ~$0.20-$0.80 за сканування
- **Тріаж issues**: ~$0.05-$0.20 за issue

**Поради, як знизити витрати:**
- Використовуйте фільтри `paths:`, щоб пропускати зміни документації/конфігурації
- Задавайте умови: `if: github.event.pull_request.draft == false`
- Переглядайте логи й коригуйте вибір моделі

## Приклади в цьому каталозі

```
examples/github-actions/
├── README.md                        # Цей файл
├── claude-code-review.yml           # Рекомендаційне рев'ю на основі prompt + необов'язкове завдання synthesis
├── claude-code-review-batched.yml    # Matrix-рев'ю з розбиттям за доменами для великих PR
├── .coderabbit.yaml                 # Конфігурація CodeRabbit (скопіюйте в корінь репозиторію)
├── .greptile/                       # Шаблони конфігурації Greptile (скопіюйте в корінь репозиторію)
├── claude-pr-auto-review.yml        # Автоматичне рев'ю з inline-prompt (альтернатива)
├── claude-security-review.yml       # Воркфлоу сканування безпеки
├── claude-issue-triage.yml          # Воркфлоу тріажу issues
└── prompts/
    └── code-review.md               # Винесений prompt рев'ю (скопіюйте до .github/prompts/)
```

## Ресурси

- [Документація Claude Code](https://claude.ai/code)
- [Документація GitHub Actions](https://docs.github.com/en/actions)
- [Документація Anthropic API](https://docs.anthropic.com/)
- [Claude GitHub App](https://github.com/apps/claude)

## Ліцензія

Ці воркфлоу надано як приклади. Адаптуйте їх під свої потреби.
