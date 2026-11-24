---
title: "Фрагменти журналу змін (Changelog Fragments): обов'язкове документування для кожного PR"
description: "3-рівневий патерн контролю для Claude Code, який гарантує, що кожен PR документується під час написання коду, а не під час релізу: нагадування через hook, перевірки шаблону PR і контроль у CI."
---

# Фрагменти журналу змін: Обов'язкове документування для кожного PR (Changelog Fragments)

3-рівневий патерн контролю, який гарантує, що кожен PR документується під час написання коду, а не під час релізу.

---

## Проблема

Поодинокі файли CHANGELOG.md створюють проблеми в активних командах. Три відкриті гілки з новими функціями, які одночасно зачіпають один і той самий файл, призводять до конфліктів злиття (merge conflicts) при кожному злитті. Хтось вирішує конфлікт, пропускає рядок, і примітки до релізу виходять неправильними ще до їхньої публікації.

Глибша проблема полягає в часі. «Документування під час релізу» звучить розумно, поки ви не опинитеся перед PR #840 через три тижні після його злиття, намагаючись відновити, що саме змінилося для користувачів. Commit містить `fix session handling`. Розробник знаходиться в іншому часовому поясі. Контекст втрачено.

Контроль без шлюзів CI перетворює роботу над журналом змін на постійне нагадування. Хтось повинен розшукувати людей перед кожним релізом, під тиском часу, заповнюючи прогалини на основі git log.

Рішення: один YAML-фрагмент на кожен PR, написаний під час реалізації, перевірений CI та автоматично зібраний під час релізу.

---

## 3-рівнева архітектура

Система працює, тому що контроль відбувається на трьох незалежних рівнях. Кожен рівень виявляє свій тип збоїв.

### Рівень 1: Правило робочого процесу CLAUDE.md

Перший рівень — це правило, яке завантажується в контекст Claude Code під час кожної сесії. Воно кодує весь робочий процес створення фрагментів, щоб Claude міг виконати його автономно, коли його попросять створити PR.

```markdown
# git-workflow.md (loaded via CLAUDE.md)

## Changelog Fragment — Required Before Every PR

Before creating a PR, always generate a changelog fragment.

### Steps

1. **Infer from git diff** — analyze `git diff main...HEAD` to determine:
   - `type`: feat | fix | perf | refactor | security | docs | chore
   - `scope`: the functional area affected (auth, sessions, api, etc.)
   - `title`: one-line user-facing summary (< 80 chars)

2. **Create the fragment** — run `pnpm changelog:add` or write directly:
   ```
   changelog/fragments/{PR_NUMBER}-{slug}.yml
   ```

3. **Validate** — run `pnpm changelog:validate changelog/fragments/{file}.yml`

4. **Commit alongside the PR** — include the fragment in the same branch

### Fragment schema

```yaml
pr: 886                    # must match filename prefix
type: fix                  # feat|fix|perf|refactor|security|docs|chore
scope: "visiochat"
title: "Fix empty chat after SSE race condition"   # < 80 chars
description: |             # optional — explain user impact, not implementation
  SSE workplan fires before AI stream completes, causing ChatWrapper
  to mount with 0 messages.
breaking: false
migration: false           # set true if PR adds a DB migration
```

### Bypass

Add label `skip-changelog` for PRs with no user impact (CI config, deps updates, release commits).
```

Це правило робить Claude Code учасником процесу контролю, а не просто інструментом для написання коду. Коли розробник каже «створи PR», Claude виводить вміст фрагмента з diff і створює його перед відкриттям PR.

### Рівень 2: Hook UserPromptSubmit (поведінкове виявлення)

Другий рівень перехоплює намір до того, як він перетвориться на дію. Коли розробник вводить щось, що вказує на намір створити PR, hook перевіряє, чи було згадано фрагмент журналу змін.

```bash
# .claude/hooks/smart-suggest.sh (excerpt — Tier 0 enforcement)

# PR creation intent detected
if echo "$PROMPT_LC" | grep -qE '(create.*pr|open.*pr|make.*pr|pull.?request|push.*pr)'; then
    # Fragment not mentioned → redirect to creation step first
    if ! echo "$PROMPT_LC" | grep -qE '(changelog|fragment|skip-changelog)'; then
        suggest "pnpm changelog:add" \
            "REQUIRED before merge — creates changelog/fragments/{PR}-{slug}.yml"
    else
        # Already mentioned → suggest the PR command normally
        suggest "/pr" "PR creation with structured description"
    fi
fi
```

Hook використовує `UserPromptSubmit`: не блокує виконання, видає максимум одну пропозицію на prompt, не проявляє себе за відсутності збігів. Він запускається перед тим, як Claude Code обробить prompt, тому розробник бачить нагадування прямо у терміналі ще до того, як Claude почне щось робити.

Умовна логіка (`якщо X без Y`) є ключовим патерном тут. Логіка адаптується до контексту, а не блокує кожен запит безумовно. Якщо розробник уже згадав фрагмент, він отримує звичайну пропозицію. Якщо ні — отримує нагадування про обов'язкове правило.

**Повний hook із 3-рівневою архітектурою**: [examples/hooks/bash/smart-suggest.sh](../../examples/hooks/bash/smart-suggest.sh)

### Рівень 3: Контроль на рівні CI (GitHub Actions)

Третій рівень — це жорсткий шлюз (hard gate). Два незалежних завдання (jobs) запускаються для кожного PR, спрямованого на головну гілку.

**Завдання `check-fragment`**: спочатку перевіряє ярлики обходу (bypass labels) із закритого списку, а потім вимагає наявності `changelog/fragments/{PR_NUMBER}-*.yml` та успішного проходження структурної перевірки.

```yaml
- name: Check fragment exists and is valid
  env:
    PR_NUMBER: ${{ github.event.pull_request.number }}
    PR_LABELS: ${{ toJson(github.event.pull_request.labels.*.name) }}
  run: |
    SKIP_LABELS=("skip-changelog" "dependencies" "release" "chore: deps")
    for LABEL in "${SKIP_LABELS[@]}"; do
      if echo "$PR_LABELS" | grep -q "\"$LABEL\""; then
        echo "Bypass label detected — fragment not required"
        exit 0
      fi
    done

    FRAGMENT=$(ls "changelog/fragments/${PR_NUMBER}-"*.yml 2>/dev/null | head -1)
    if [ -z "$FRAGMENT" ]; then
      echo "Fragment missing. Run: pnpm changelog:add"
      exit 1
    fi

    pnpm tsx changelog/scripts/validate.ts "$FRAGMENT"
```

**Завдання `check-migration-flag`** (запускається незалежно, без можливості обходу): виявляє нові файли міграцій SQL за допомогою `git diff --name-only --diff-filter=A`. Якщо міграції присутні, а у фрагменті вказано `migration: false`, завдання завершується помилкою. Це завдання не можна обійти за допомогою ярликів. PR із ярликом `skip-changelog`, який додає міграцію, все одно запустить перевірку.

Ці два завдання спроектовані як незалежні. PR може обійти створення фрагмента (через ярлик), але все одно не пройти перевірку міграції.

---

## Збірка фрагментів під час релізу

Фрагменти накопичуються в `changelog/fragments/` у міру злиття PR. Під час релізу одна команда збирає їх у розділ CHANGELOG з відповідною версією.

```bash
pnpm changelog:assemble --version 1.8.0 [--dry-run]
```

Що це робить:
1. Зчитує всі `changelog/fragments/*.yml`
2. Групує за типом у фіксованому порядку (feat, fix, perf, refactor, security, docs, chore)
3. Виносить записи з `breaking: true` в окремий розділ `🔨 Breaking Changes`
4. Додає до записів із `migration: true` інлайн-позначку `⚠️ Migration DB.`
5. Замінює плейсхолдер `## [Next Release]` у `CHANGELOG.md`
6. Архівує фрагменти в `changelog/fragments/released/{version}/`

Вивід:
```markdown
## [1.8.0] - 2026-03-15

### 🔨 Breaking Changes
- **Remove legacy token format (#871)** — Tokens issued before v1.6.0 are invalid.

### ✨ New Features
- **Add real-time presence indicators (#892)**

### 🔧 Bug Fixes
- **Fix empty chat after SSE race condition (#886)** — SSE workplan fires before
  AI stream completes, causing ChatWrapper to mount with 0 messages.
```

---

## Чому саме 3 рівні, а не 1

Кожен рівень виявляє свій тип збоїв:

| Рівень | Виявлений збій | Коли |
|-------|---------------|------|
| Правило CLAUDE.md | Claude забуває робочий процес | Кожна сесія |
| Hook UserPromptSubmit | Розробник вводить «створи PR» не замислюючись | До обробки промпту |
| Шлюз CI | Фрагмент було пропущено або пошкоджено | Перед злиттям |

Один лише шлюз CI виявляє проблему занадто пізно. Розробнику доводиться знову перемикати контекст після того, як його PR уже відкритий. Hook перехоплює це на етапі виявлення наміру. Правило CLAUDE.md дозволяє Claude вирішувати це завдання автономно під час виконання роботи.

Ці рівні не конфліктують між собою. Вони підсилюють один одного. Розробник, який бачить пропозицію від hook, запустить `pnpm changelog:add`. Claude виконає правило CLAUDE.md та валідує результат. CI підтверджує, що все гаразд, перед злиттям.

---

## Впровадження цього патерну

Скрипти TypeScript (add, validate, assemble, audit) є специфічними для стеку Méthode Aristote. Проте 3-рівневий патерн контролю лишається універсальним: він працює з будь-яким форматом фрагментів, будь-якою системою CI та будь-яким збирачем.

**Мінімально необхідне налаштування:**

1. **Визначте схему вашого фрагмента** (YAML, JSON або все, що підходить вашому стеку)
2. **Додайте правило у CLAUDE.md**, яке кодує робочий процес створення, щоб Claude міг обробляти його автономно
3. **Додайте hook `UserPromptSubmit`** із шаблоном `якщо намір-PR без згадки-фрагмента → запропонувати`
4. **Додайте завдання CI**, яке перевіряє наявність фрагмента перед злиттям

Цей шаблон hook можна узагальнити для будь-якого обов'язкового кроку робочого процесу. Замініть «фрагмент журналу змін» на «ADR», «прапорець міграції», «перевірку покриття тестами». Логіка умовного виявлення залишається тією самою.

---

## Пов'язане

- Приклад hook: [examples/hooks/bash/smart-suggest.sh](../../examples/hooks/bash/smart-suggest.sh)
- Документація по hooks: [UserPromptSubmit Hooks](../ultimate-guide.uk.md) (пошук за словом "UserPromptSubmit")
- Скрипти валідатора та збирача фрагментів: доступні в репозиторії Méthode Aristote

---
**Локалізація**: [Serhii (MacPlus Software)](https://macplus-software.com)
*Остання синхронізація: Травень 2026*
