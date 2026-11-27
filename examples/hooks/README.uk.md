---
title: "Hooks Claude Code"
description: "Скрипти, керовані подіями, для автоматизації, блокування небезпечних дій і збагачення контексту"
tags: [hooks, security, template, config]
---

# Hooks Claude Code

Hooks — це скрипти, які автоматично виконуються на події Claude Code. Вони дають змогу автоматизувати роботу, блокувати небезпечні операції та збагачувати контекст.

## Доступні hooks

| Hook | Подія | Призначення | Платформа |
|------|-------|---------|----------|
| [bm25-routing/bm25-suggest.js](https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/examples/hooks/bm25-routing/bm25-suggest.js) | UserPromptSubmit | Лексична маршрутизація skills на основі BM25 з порогами, що самокалібруються | Node.js |
| [bash/smart-suggest.sh](./bash/smart-suggest.sh) | UserPromptSubmit | Поведінковий коуч на основі регулярних виразів із 3-рівневим пріоритетом (enforcement/discovery/contextual) | Bash |
| [dangerous-actions-blocker.sh](./bash/dangerous-actions-blocker.sh) | PreToolUse | Блокує небезпечні команди/правки | Bash |
| [security-check.sh](./bash/security-check.sh) | PreToolUse | Блокує секрети в командах | Bash |
| [prompt-injection-detector.sh](./bash/prompt-injection-detector.sh) | PreToolUse | Виявляє спроби ін'єкцій (+ANSI, нульові байти, вкладені команди) | Bash |
| [unicode-injection-scanner.sh](./bash/unicode-injection-scanner.sh) | PreToolUse | Виявляє символи нульової ширини, RTL override, ANSI escape, нульові байти | Bash |
| [repo-integrity-scanner.sh](./bash/repo-integrity-scanner.sh) | PreToolUse | Сканує README/package.json на приховані ін'єкції | Bash |
| [mcp-config-integrity.sh](./bash/mcp-config-integrity.sh) | SessionStart | Перевіряє хеш конфігурації MCP (CVE-2025-54135/54136) | Bash |
| [claudemd-scanner.sh](./bash/claudemd-scanner.sh) | SessionStart | Виявляє атаки ін'єкцією через CLAUDE.md | Bash |
| [output-secrets-scanner.sh](./bash/output-secrets-scanner.sh) | PostToolUse | Виявляє витік секретів і змінних середовища у виводі інструментів | Bash |
| [auto-format.sh](./bash/auto-format.sh) | PostToolUse | Автоформатування після правок | Bash |
| [rtk-baseline.sh](./bash/rtk-baseline.sh) | SessionStart | Зберігає базовий рівень RTK для відстеження економії за сесію | Bash |
| [session-summary.sh](./bash/session-summary.sh) | SessionEnd | Повна аналітика сесії (15 налаштовуваних розділів) | Bash |
| [session-summary-config.sh](./bash/session-summary-config.sh) | CLI-інструмент | Налаштування розділів session-summary, їхнього порядку, попередній перегляд | Bash |
| [learning-capture.sh](./bash/learning-capture.sh) | Stop | Запит на щоденну фіксацію навчання | Bash |
| [sandbox-validation.sh](./bash/sandbox-validation.sh) | PreToolUse | Перевіряє ізоляцію пісочниці | Bash |
| [file-guard.sh](./bash/file-guard.sh) | PreToolUse | Захищає чутливі файли від змін | Bash |
| [permission-request.sh](./bash/permission-request.sh) | PreToolUse | Явний процес дозволів для ризикованих операцій | Bash |
| [rtk-auto-wrapper.sh](./bash/rtk-auto-wrapper.sh) | PreToolUse | Автоматично обгортає команди в RTK для економії токенів | Bash |
| [setup-init.sh](./bash/setup-init.sh) | SessionStart | Ініціалізує середовище сесії | Bash |
| [auto-checkpoint.sh](./bash/auto-checkpoint.sh) | PostToolUse | Автоматично створює контрольні точки роботи з інтервалом | Bash |
| [typecheck-on-save.sh](./bash/typecheck-on-save.sh) | PostToolUse | Запускає перевірки TypeScript під час збереження | Bash |
| [test-on-change.sh](./bash/test-on-change.sh) | PostToolUse | Запускає тести під час змін файлів | Bash |
| [output-validator.sh](./bash/output-validator.sh) | PostToolUse | Евристична валідація виводу | Bash |
| [session-logger.sh](./bash/session-logger.sh) | PostToolUse | Логує операції для моніторингу | Bash |
| [privacy-warning.sh](./bash/privacy-warning.sh) | PostToolUse | Попереджає про можливі витоки приватних даних | Bash |
| [tts-selective.sh](./bash/tts-selective.sh) | PostToolUse | Синтез мовлення для вибраних виводів | Bash |
| [subagent-stop.sh](./bash/subagent-stop.sh) | Stop | Прибирає ресурси subagent | Bash |
| [pre-commit-secrets.sh](./bash/pre-commit-secrets.sh) | Git hook | Не пускає секрети в коміти | Bash |
| [pre-commit-evaluator.sh](./bash/pre-commit-evaluator.sh) | Git hook | Валідація перед комітом за схемою LLM-as-a-Judge | Bash |
| [notification.sh](./bash/notification.sh) | Notification | Контекстні звукові сповіщення macOS | Bash (macOS) |
| [auto-rename-session.sh](./bash/auto-rename-session.sh) | SessionEnd | Генерування назви сесії за допомогою AI через Haiku | Bash |
| [security-gate.sh](./bash/security-gate.sh) | PreToolUse | Виявляє вразливі патерни коду перед записом у вихідні файли | Bash |
| [velocity-governor.sh](./bash/velocity-governor.sh) | PreToolUse | Обмежує частоту викликів інструментів, щоб уникнути throttling API | Bash |
| [security-check.ps1](./powershell/security-check.ps1) | PreToolUse | Блокує секрети в командах | PowerShell |
| [auto-format.ps1](./powershell/auto-format.ps1) | PostToolUse | Автоформатування після правок | PowerShell |

## Події hooks

33 події в 9 групах. Події з позначкою **[B]** можуть блокувати через exit 2 або JSON-рішення. `PermissionRequest` ігнорує exit 2 і блокує лише через свій об'єкт `decision`.

**Життєвий цикл**

| Подія | Коли | Типові сценарії використання |
|-------|------|-------------------|
| `SessionStart` | Сесія починається або відновлюється | Ініціалізація, налаштування середовища, сканування конфігурації |
| `Setup` | Одноразова ініціалізація через `--init-only` або `--init`/`--maintenance` у режимі `-p` | Встановлення залежностей, перевірка передумов |
| `SessionEnd` | Сесія завершується | Прибирання, підсумок сесії |

**Дії агента**

| Подія | Коли | Типові сценарії використання |
|-------|------|-------------------|
| `Stop` **[B]** | Claude завершує відповідь | Перевірки якості після відповіді, цикли продовження |
| `StopFailure` | Хід завершується через помилку API | Сповіщення про rate limits, спостережуваність |
| `PreToolUse` **[B]** | Перед виконанням інструмента | Валідація, блокування небезпечних операцій |
| `PostToolUse` | Після успішного виконання інструмента | Форматування, логування, прибирання |
| `PostToolUseFailure` | Після збою інструмента | Логування помилок, дії з відновлення |
| `PostToolBatch` **[B]** | Після повного пакета паралельних викликів інструментів, перед наступним викликом моделі | Додавання контексту на рівні пакета, забезпечення політик |

**Дозволи**

| Подія | Коли | Типові сценарії використання |
|-------|------|-------------------|
| `PermissionRequest` **[B]** | З'являється діалог дозволу (відмова через `decision`, а не exit 2) | Власна логіка схвалення, автоматичне схвалення безпечних операцій |
| `PermissionDenied` | Виклик інструмента відхилено в auto mode | Аудит відмов класифікатора, за потреби сигнал повторити |

**Compaction**

| Подія | Коли | Типові сценарії використання |
|-------|------|-------------------|
| `PreCompact` **[B]** | Перед compaction контексту | Блокування небажаного auto-compact, збереження стану |
| `PostCompact` | Після завершення compaction | Відновлення контексту, логування підсумку compaction |

**Кілька агентів**

| Подія | Коли | Типові сценарії використання |
|-------|------|-------------------|
| `SubagentStart` | Запускається subagent | Передавання контексту в subagent |
| `SubagentStop` **[B]** | Subagent завершує роботу | Прибирання, перевірка якості перед виходом subagent |
| `TeammateIdle` **[B]** | Агент-учасник команди от-от перейде в режим очікування | Координація команди, перевірки якості |
| `TaskCreated` **[B]** | Завдання створено через TaskCreate | Забезпечення домовленостей щодо іменування, аудит |
| `TaskCompleted` **[B]** | Завдання позначено як завершене | Забезпечення критеріїв завершення (тести, lint) |

**Конфігурація**

| Подія | Коли | Типові сценарії використання |
|-------|------|-------------------|
| `ConfigChange` **[B]** | Файл конфігурації змінюється під час сесії | Корпоративний аудит, блокування несанкціонованих змін |
| `InstructionsLoaded` | Завантажено CLAUDE.md або файл правил | Аудит того, які файли інструкцій активні |

**Файлова система**

| Подія | Коли | Типові сценарії використання |
|-------|------|-------------------|
| `CwdChanged` | Змінюється робочий каталог | Перезавантаження direnv, перемикання інструментів |
| `FileChanged` | Відстежуваний файл змінюється на диску | Перезавантаження середовища, запуск watchers |
| `WorktreeCreate` **[B]** | Створюється worktree | Власне налаштування VCS (SVN, Perforce) |
| `DirectoryAdded` | Робочий каталог додано через `/add-dir` або SDK `register_repo_root` | Завантаження середовища для конкретного репозиторію, аудит доданих коренів |
| `WorktreeRemove` **[B]** | Worktree вилучається (будь-який ненульовий код завершення зриває вилучення) | Прибирання стану VCS, облікових даних |

**Взаємодія з користувачем**

| Подія | Коли | Типові сценарії використання |
|-------|------|-------------------|
| `UserPromptSubmit` **[B]** | Користувач надсилає повідомлення | Збагачення контексту, валідація prompt |
| `UserPromptExpansion` **[B]** | Slash-команда розгортається в prompt | Блокування команди, додавання контексту skill |
| `Notification` | Claude надсилає сповіщення | Звукові сигнали, зовнішні сповіщення |
| `MessageDisplay` | Під час показу тексту асистента | Прибирання markdown на екрані, приховування секретів |
| `Elicitation` **[B]** | MCP-сервер запитує ввід користувача | Попередня відповідь у headless-автоматизації |
| `ElicitationResult` **[B]** | Користувач відповідає на elicitation | Аудит або зміна відповідей перед передаванням у MCP |

**Модель**

| Подія | Коли | Типові сценарії використання |
|-------|------|-------------------|
| `PreModelSwitch` **[B]** | Перед застосуванням запитаної зміни моделі | Забезпечення дозволених моделей, попередження про вартість |
| `PostModelSwitch` | Після зміни моделі сесії | Логування змін моделі, додавання контексту для конкретної моделі |

## Просунуті запобіжники (НОВЕ у v3.3.0)

Просунуті патерни захисту, натхненні продакшн-системами на LLM.

### prompt-injection-detector.sh

**Подія**: `PreToolUse`

Виявляє та блокує спроби prompt injection, перш ніж вони дійдуть до Claude:

**Виявлені патерни**:
- Перевизначення ролі: "ignore previous instructions", "you are now", "pretend to be"
- Спроби jailbreak: "DAN mode", "developer mode", "no restrictions"
- Ін'єкція розділювачів: `</system>`, `[INST]`, `<<SYS>>`
- Видавання себе за авторитет: "anthropic employee", "authorized to bypass"
- Корисні навантаження в Base64 (декодуються й скануються)
- Маніпулювання контекстом: неправдиві твердження про попередні повідомлення

**Конфігурація**:
```json
{
  "hooks": {
    "PreToolUse": [{
      "hooks": [{
        "type": "command",
        "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/prompt-injection-detector.sh",
        "timeout": 5000
      }]
    }]
  }
}
```

### output-validator.sh

**Подія**: `PostToolUse`

Евристична валідація виводу Claude (без виклику LLM, чистий bash):

**Перевірки валідації**:
- Шляхи-заглушки: `/path/to/`, `/your/project/`
- Вміст-заглушки: `TODO:`, `your-api-key`, `example.com`
- Потенційні секрети у виводі (патерни регулярних виразів)
- Ознаки невпевненості (численні "I'm not sure", "probably")
- Незавершені реалізації: `NotImplementedError`, `throw new Error`
- Неперевірені твердження про посилання

**Поведінка**: попереджає через `systemMessage`, не блокує. Для глибшої валідації використовуйте агента `output-evaluator`.

### session-logger.sh

**Подія**: `PostToolUse`

Логує всі операції Claude у файли JSONL для моніторингу та відстеження витрат:

**Розташування логів**: `~/.claude/logs/activity-YYYY-MM-DD.jsonl`

**Дані, що логуються**:
- Часова мітка, ID сесії, назва інструмента
- Шляхи до файлів і команди (обрізані)
- Назва проєкту
- Оцінки токенів (вхід/вихід)

**Аналіз**: для аналізу логів використовуйте скрипт `session-stats.sh`.

**Змінні середовища**:
| Змінна | Типово | Опис |
|----------|---------|-------------|
| `CLAUDE_LOG_DIR` | `~/.claude/logs` | Каталог логів |
| `CLAUDE_LOG_TOKENS` | `true` | Увімкнути оцінку токенів |
| `CLAUDE_SESSION_ID` | auto | Власний ID сесії |

Повну документацію див. у [посібнику зі спостережуваності](../../guide/ops/observability.uk.md).

### pre-commit-evaluator.sh

**Тип**: Git pre-commit hook (не hook Claude)

Оцінювання за схемою LLM-as-a-Judge перед кожним комітом. **Лише за явним увімкненням** через вартість API.

**Встановлення**:
```bash
cp pre-commit-evaluator.sh .git/hooks/pre-commit
chmod +x .git/hooks/pre-commit
export CLAUDE_PRECOMMIT_EVAL=1  # Enable evaluation
```

**Вартість**: ~$0.01-0.05 за коміт (модель Haiku)

**Обхід**: `git commit --no-verify` або `CLAUDE_SKIP_EVAL=1 git commit`

---

## Hooks безпеки

### dangerous-actions-blocker.sh

**Подія**: `PreToolUse` (Bash, Edit, Write)

Всебічний захист від небезпечних операцій:

**Bash - заблоковані команди**:
- Знищення системи: `rm -rf /`, `rm -rf ~`, `sudo rm`
- Дискові операції: `dd if=`, `mkfs`, `> /dev/sda`
- Fork-бомби: `:(){:|:&};:`
- Видалення баз даних: `DROP DATABASE`, `DROP TABLE`
- Примусові push: `git push --force main/master`
- Публікація пакетів: `npm publish`, `pnpm publish`
- Патерни секретів: `password=`, `api_key=`, `token=`

**Edit/Write - захищені файли**:
- Середовище: `.env`, `.env.local`, `.env.production`
- Облікові дані: `credentials.json`, `serviceAccountKey.json`
- SSH-ключі: `id_rsa`, `id_ed25519`, `id_ecdsa`
- Конфігурація: `.npmrc`, `.pypirc`, `secrets.yml`

**Edit/Write - дозволені шляхи**:
- `$CLAUDE_PROJECT_DIR` (поточний проєкт)
- `~/.claude/` (конфігурація Claude)
- `/tmp/` (тимчасові файли)
- Додаткові шляхи через змінну середовища `$ALLOWED_PATHS`

**Коди завершення**:
```bash
exit 0  # Allow operation
exit 2  # Block (stderr message shown to Claude)
```

**Конфігурація**:
```bash
# Add custom allowed paths (colon-separated)
export ALLOWED_PATHS="/custom/path:/another/path"
```

### security-check.sh

**Подія**: `PreToolUse` (Bash)

Зосереджений на виявленні секретів у командах:
- Патерни паролів
- API-ключі (поширені формати на кшталт `sk-xxx`, `pk-xxx`)
- Облікові дані AWS
- Приватні ключі
- Жорстко прописані токени

### claudemd-scanner.sh

**Подія**: `SessionStart`

На початку сесії сканує файли CLAUDE.md на можливі атаки prompt injection:

**Виявлені патерни**:
- Варіанти "ignore previous instructions"
- Shell-ін'єкції: `curl | bash`, `wget | sh`, `eval(`
- Вміст, закодований у Base64 (можлива обфускація)
- Приховані інструкції в HTML-коментарях
- Підозріло довгі рядки (>500 символів)
- Не-ASCII символи поруч із чутливими ключовими словами (гомогліфні атаки)

**Файли, що скануються**:
- `CLAUDE.md` (корінь проєкту)
- `.claude/CLAUDE.md` (локальне перевизначення)
- Будь-які файли `.md` у каталозі `.claude/`

**Чому це важливо**: коли ви клонуєте незнайомий репозиторій, шкідливий CLAUDE.md може впровадити інструкції, що скомпрометують вашу систему. Цей hook попереджає вас, перш ніж Claude обробить потенційно небезпечні інструкції.

**Конфігурація**:
```json
{
  "hooks": {
    "SessionStart": [{
      "hooks": [{
        "type": "command",
        "command": ".claude/hooks/claudemd-scanner.sh",
        "timeout": 5000
      }]
    }]
  }
}
```

### output-secrets-scanner.sh

**Подія**: `PostToolUse`

Доповнює `security-check.sh`, скануючи **вивід** інструментів (а не вхідні дані) на витік секретів.

**Виявлені патерни**:
- API-ключі: OpenAI, Anthropic, AWS, GCP, Azure, Stripe, Twilio, SendGrid
- Токени: GitHub, GitLab, NPM, PyPI, JWT
- Приватні ключі: RSA, EC, DSA, OpenSSH, PGP
- URL баз даних із вбудованими паролями
- Загальні патерни `api_key=`, `secret=`, `password=`

**Чому це важливо**: Claude може прочитати файл `.env` і додати облікові дані у свою відповідь або в коміт. Цей hook перехоплює секрети до того, як вони витечуть.

**Конфігурація**:
```json
{
  "hooks": {
    "PostToolUse": [{
      "hooks": [{
        "type": "command",
        "command": ".claude/hooks/output-secrets-scanner.sh",
        "timeout": 5000
      }]
    }]
  }
}
```

## Hooks продуктивності

### rtk-baseline.sh

**Подія**: `SessionStart`

На початку сесії фіксує накопичену статистику RTK для відстеження дельти. Працює в парі з `session-summary.sh`, який наприкінці сесії обчислює економію RTK за цю сесію.

**Конфігурація**:
```json
{
  "hooks": {
    "SessionStart": [{
      "hooks": [{
        "type": "command",
        "command": "~/.claude/hooks/rtk-baseline.sh",
        "timeout": 5000
      }]
    }]
  }
}
```

### session-summary.sh (v3)

**Подія**: `SessionEnd`

Повна аналітика сесії з 15 налаштовуваними розділами, CLI-інструментом конфігурації та логуванням у JSONL.

**Встановлення як plugin (рекомендовано)**:
```bash
claude plugin marketplace add FlorianBruniaux/claude-code-plugins
claude plugin install session-summary@florian-claude-tools
```
Hooks підключаються автоматично, ручне налаштування не потрібне. Подробиці див. у [репозиторії plugin](https://github.com/FlorianBruniaux/claude-code-plugins).

**Розділи** (усі налаштовуються через змінні середовища або файл конфігурації):

| Розділ | Типово | Опис |
|---------|---------|-------------|
| `meta` | завжди | ID сесії, назва, гілка |
| `duration` | завжди | Загальний час, активний час, ходи, причина виходу |
| `tools` | завжди | Розподіл викликів інструментів (OK/ERR) |
| `errors` | увімк. | Подробиці помилок, згруповані за інструментом |
| `files` | увімк. | Прочитані/відредаговані/створені файли з найчастіше редагованими |
| `features` | увімк. | MCP-сервери, агенти, skills, команди, plan mode |
| `git` | увімк. | Підсумок git diff (+/- рядки, змінені файли) |
| `loc` | увімк. | Рядки коду, написані через Edit/Write |
| `models` | завжди | Використання моделей (запити, токени) |
| `cache` | завжди | Частка влучань у кеш |
| `cost` | завжди | Оцінка вартості (ccusage або таблиця цін) |
| `rtk` | увімк. | Економія токенів RTK (дельта від початку сесії) |
| `ratio` | увімк. | Співвідношення розмови (інтерактивні/автоматичні ходи) |
| `thinking` | вимк. | Кількість блоків thinking |
| `context` | вимк. | Оцінка контекстного вікна (піковий %) |

**Файл логу**: `~/.claude/logs/session-summaries.jsonl` (структурований JSONL з усіма метриками)

**Пріоритет конфігурації**: `env vars (SESSION_SUMMARY_*)` > `config file (~/.config/session-summary/config.sh)` > `defaults`

**Змінні середовища**:
| Змінна | Типово | Опис |
|----------|---------|-------------|
| `NO_COLOR` | - | Вимкнути кольори ANSI |
| `SESSION_SUMMARY_SKIP` | `0` | Встановіть `1`, щоб вимкнути підсумок |
| `SESSION_SUMMARY_LOG` | `~/.claude/logs` | Перевизначити каталог логів |
| `SESSION_SUMMARY_FILES` | `1` | Перемикач розділу файлів |
| `SESSION_SUMMARY_RTK` | `auto` | `auto` / `1` / `0` |
| `SESSION_SUMMARY_GIT` | `1` | Перемикач git diff |
| `SESSION_SUMMARY_ERRORS` | `1` | Перемикач подробиць помилок |
| `SESSION_SUMMARY_LOC` | `1` | Перемикач рядків коду |
| `SESSION_SUMMARY_RATIO` | `1` | Перемикач співвідношення розмови |
| `SESSION_SUMMARY_FEATURES` | `1` | Перемикач використаних можливостей |
| `SESSION_SUMMARY_THINKING` | `0` | Перемикач блоків thinking |
| `SESSION_SUMMARY_CONTEXT` | `0` | Перемикач оцінки контексту |
| `SESSION_SUMMARY_SECTIONS` | (усі) | Порядок розділів через кому |

**CLI-інструмент конфігурації** (`session-summary-config.sh`):
```bash
session-summary-config show              # Current config with section status
session-summary-config set git=0         # Disable a section
session-summary-config set thinking=1    # Enable a section
session-summary-config reset             # Reset to defaults
session-summary-config sections          # Show section order
session-summary-config sections "meta,duration,tools,cost"  # Minimal output
session-summary-config preview           # Demo output with current config
session-summary-config install           # Install hooks in settings.json
session-summary-config log 5             # Last 5 session summaries
```

**Вимоги**:
- `jq` (обов'язково, для розбору JSON)
- `ccusage` (необов'язково, для точного обчислення вартості)
- `rtk` (необов'язково, для відстеження економії токенів)

**Скриншот** (вивід реальної сесії):

![Session Summary v3](../../docs/images/session-summary-v3.png)

**Приклад виводу** (усі розділи ввімкнено):
```
═══ Session Summary ═══════════════════
ID:       abc-123-def-456...
Name:     Fix session summary hook
Branch:   main
Duration: Wall 5m 28s | Active 1m 33s | 12 turns | Exit: user

Tool Calls: 29 (OK 27 / ERR 2)
  Edit: 13  Bash: 8  Read: 6  Grep: 1  Glob: 1

Errors: 2
  Bash: "command not found: rtk" (x1)
  Edit: "old_string not unique" (x1)

Files: 3 read · 2 edited · 1 created
  session-summary.sh (8 edits), settings.json (3 edits)

Features: MCP (perplexity x4, chrome x12) · Agents (Explore x3, Plan x1) · Skills (commit)

Git: +142 -37 lines · 4 files changed
Code: +87 -12 net (via Edit/Write)

Model Usage         Reqs    Input    Output
claude-opus-4-6       59      93K      628
Cache: 85% hit rate (3.9M read / 322K created)
Est. Cost: $0.045

RTK Savings: 24 cmds · ~12.4K tokens saved (73%)
Turns: 12 (8 interactive · 4 auto) · Avg 6.7s/turn
═══════════════════════════════════════
```

**Конфігурація**:
```json
{
  "hooks": {
    "SessionEnd": [{
      "hooks": [{
        "type": "command",
        "command": "~/.claude/hooks/session-summary.sh"
      }]
    }]
  }
}
```

**Швидке встановлення**: через систему plugins (див. вище) або вручну: `session-summary-config.sh install` (копіює hooks + оновлює settings.json)

**Порівняння з патчем `/cost` від tweakcc**:

[tweakcc](https://github.com/Piebald-AI/tweakcc) (1K+ зірок) патчить `cli.js` Claude Code, щоб знову ввімкнути `/cost` для передплатників Pro/Max. Інший підхід — інші компроміси:

| | tweakcc `/cost` | session-summary.sh |
|---|---|---|
| Підхід | Патчить бінарний файл Claude Code | Офіційний API hooks (без змін) |
| Переживає оновлення CC | Ні (потрібно повторно застосовувати після кожного оновлення) | Так |
| Запуск | Вручну (команда `/cost`) | Автоматично під час виходу із сесії |
| Метрики | Вартість, тривалість, токени, LOC | 15 розділів (вартість, токени, інструменти, помилки, файли, можливості, git diff, LOC, кеш, RTK, співвідношення...) |
| Історія | Ні | JSONL-лог з усіма метриками |
| Залежності | Node.js | jq (нативно для bash) |

tweakcc — ширший інструмент (теми, prompts, набори інструментів), і патч `/cost` — лише одна з багатьох його функцій. Цей hook зосереджений саме на аналітиці сесій із глибшими метриками й без жодних змін у внутрішніх механізмах Claude Code.

### auto-format.sh / auto-format.ps1

**Подія**: `PostToolUse` (Edit, Write)

Автоматично форматує файли після редагування:

| Розширення | Форматувальник |
|-----------|-----------|
| `.ts`, `.tsx`, `.js`, `.jsx` | Prettier |
| `.json`, `.css`, `.scss`, `.md` | Prettier |
| `.prisma` | `prisma format` |
| `.py` | Black / autopep8 |
| `.go` | `go fmt` |

**Тиха робота**: жодного виводу, збої ігноруються, щоб не блокувати Claude.

**Вимоги**: встановіть форматувальники у своєму проєкті:
```bash
# Node.js projects
npm install -D prettier

# Python projects
pip install black

# Go projects (built-in)
go fmt
```

### notification.sh

**Подія**: `Notification` (лише macOS)

Контекстні звукові сповіщення залежно від вмісту сповіщення:

| Контекст | Звук | Що запускає |
|---------|-------|--------------|
| Успіх | Hero.aiff | "completed", "done", "success" |
| Помилка | Basso.aiff | "error", "failed", "problem" |
| Очікування | Submarine.aiff | "waiting", "permission", "input" |
| Попередження | Sosumi.aiff | "warning", "attention", "alert" |
| Типово | Ping.aiff | Інші сповіщення |

**Можливості**:
- Не блокує (відтворюється у фоні)
- Нативні сповіщення macOS
- Автоматичне визначення контексту за ключовими словами
- Підтримка кількох мов (англійська/французька)

**Вимоги**: macOS з `afplay` і `osascript` (вбудовані)

## Конфігурація

Hooks налаштовуються в `.claude/settings.json`:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash|Edit|Write",
        "hooks": [{
          "type": "command",
          "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/dangerous-actions-blocker.sh",
          "timeout": 5000
        }]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [{
          "type": "command",
          "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/auto-format.sh",
          "timeout": 10000
        }]
      }
    ],
    "Notification": [
      {
        "hooks": [{
          "type": "command",
          "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/notification.sh",
          "timeout": 5000
        }]
      }
    ]
  }
}
```

**Патерни matcher**:
- `".*"` - відповідає всім інструментам
- `"Bash"` - відповідає лише інструменту Bash
- `"Edit|Write"` - відповідає інструментам Edit АБО Write
- `"Bash|Edit|Write"` - відповідає кільком інструментам

## Створення власних hooks

### Базовий шаблон

```bash
#!/bin/bash
# Hook: [EventType] - Description
# Exit 0 = success/allow, Exit 2 = block (PreToolUse only)

set -e

# Read JSON from stdin
INPUT=$(cat)

# Extract data
TOOL_NAME=$(echo "$INPUT" | jq -r '.tool_name // empty')
TOOL_INPUT=$(echo "$INPUT" | jq -r '.tool_input // empty')

# Your logic here...

# Return optional JSON
cat << EOF
{
  "systemMessage": "Message displayed to Claude",
  "hookSpecificOutput": {
    "additionalContext": "Extra context added"
  }
}
EOF

exit 0
```

### Змінні середовища

Доступні в скриптах hooks:

| Змінна | Опис |
|----------|-------------|
| `CLAUDE_PROJECT_DIR` | Шлях до поточного проєкту |
| `CLAUDE_FILE_PATHS` | Файли, передані з прапорцем `-f` |
| `CLAUDE_TOOL_INPUT` | Вхідні дані інструмента як JSON |
| `HOME` | Домашній каталог користувача |

### Найкращі практики

1. **Короткий тайм-аут**: максимум 5-10 с, щоб не блокувати Claude
2. **М'яка обробка збоїв**: використовуйте `|| true` для некритичних операцій
3. **Мінімальне логування**: уникайте stdout, крім структурованого JSON
4. **Вимагайте jq**: розбирайте JSON за допомогою `jq` для надійності
5. **Ретельно тестуйте**: перевірте з різними вхідними даними перед розгортанням
6. **Документуйте поведінку**: зрозумілі коментарі про те, що робить hook
7. **Обробляйте помилки**: належні повідомлення про помилки для налагодження

### Приклад: збагачення контекстом Git

Створіть `git-context.sh` (подія UserPromptSubmit):

```bash
#!/bin/bash
# Hook: UserPromptSubmit - Add Git context to prompts

set -e

INPUT=$(cat)

# Get Git information
BRANCH=$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo "unknown")
LAST_COMMIT=$(git log -1 --oneline 2>/dev/null || echo "none")
UNCOMMITTED=$(git status --short 2>/dev/null | wc -l | tr -d ' ')
STAGED=$(git diff --cached --name-only 2>/dev/null | wc -l | tr -d ' ')

# Return enriched context
cat << EOF
{
  "systemMessage": "[Git] Branch: $BRANCH | Last: $LAST_COMMIT | Uncommitted: $UNCOMMITTED files | Staged: $STAGED files"
}
EOF

exit 0
```

Зареєструйте в налаштуваннях:
```json
{
  "hooks": {
    "UserPromptSubmit": [
      {
        "hooks": [{
          "type": "command",
          "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/git-context.sh",
          "timeout": 3000
        }]
      }
    ]
  }
}
```

## Встановлення

### На рівні проєкту (спільно з командою)

1. Створіть каталог hooks:
```bash
mkdir -p .claude/hooks
```

2. Скопіюйте hook із прикладів:
```bash
cp /path/to/examples/hooks/bash/dangerous-actions-blocker.sh .claude/hooks/
chmod +x .claude/hooks/*.sh
```

3. Налаштуйте в `.claude/settings.json` (див. розділ «Конфігурація» вище)

4. Закомітьте в репозиторій:
```bash
git add .claude/hooks/ .claude/settings.json
git commit -m "Add Claude Code hooks"
```

### Особисто/глобально (лише на вашій машині)

1. Створіть глобальний каталог hooks:
```bash
mkdir -p ~/.claude/hooks
```

2. Скопіюйте hook:
```bash
cp /path/to/examples/hooks/bash/notification.sh ~/.claude/hooks/
chmod +x ~/.claude/hooks/*.sh
```

3. Налаштуйте в `~/.claude/settings.json`

**Пріоритет**: hooks проєкту перевизначають глобальні hooks.

## Примітки щодо платформ

### macOS / Linux (bash)

- Використовуйте розширення `.sh`
- Потрібен `chmod +x` для виконання
- Роздільник шляхів: `/`
- Домашній каталог: `~` або `$HOME`

### Windows (PowerShell)

- Використовуйте розширення `.ps1`
- Може знадобитися політика виконання: `Set-ExecutionPolicy RemoteSigned`
- Роздільник шляхів: `\`
- Домашній каталог: `$env:USERPROFILE`

## Усунення несправностей

### Hook не виконується

**Причина**: не зареєстрований у settings.json або неправильний шлях

**Виправлення**: перевірте конфігурацію й використовуйте абсолютні шляхи або `$CLAUDE_PROJECT_DIR`

### Permission denied

**Причина**: hook не є виконуваним

**Виправлення**:
```bash
chmod +x .claude/hooks/*.sh
```

### Hook блокує все

**Причина**: код завершення 2 без умов

**Виправлення**: перевірте логіку, переконайтеся, що типовий випадок — `exit 0`

### Помилки тайм-ауту

**Причина**: hook працює задовго (>значення timeout)

**Виправлення**: оптимізуйте продуктивність hook або збільште timeout у налаштуваннях

### jq не знайдено

**Причина**: `jq` не встановлено

**Виправлення**: встановіть jq:
```bash
# macOS
brew install jq

# Ubuntu/Debian
sudo apt-get install jq

# Windows
choco install jq
```

## Просунуті приклади

### Логер активності

Логує всі операції Claude у файл JSONL:

```bash
#!/bin/bash
# PostToolUse - Log all activities

set -e

INPUT=$(cat)
TOOL=$(echo "$INPUT" | jq -r '.tool_name')
LOG_FILE="$HOME/.claude/logs/activity-$(date +%Y-%m-%d).jsonl"

mkdir -p "$(dirname "$LOG_FILE")"

# Create log entry
cat << EOF >> "$LOG_FILE"
{"timestamp":"$(date -u +%Y-%m-%dT%H:%M:%SZ)","tool":"$TOOL","session":"$CLAUDE_SESSION_ID"}
EOF

exit 0
```

### Детектор міграцій бази даних

Сповіщає, коли створюються міграції:

```bash
#!/bin/bash
# PostToolUse - Detect database migrations

set -e

INPUT=$(cat)
TOOL=$(echo "$INPUT" | jq -r '.tool_name')

if [[ "$TOOL" == "Write" ]]; then
    FILE=$(echo "$INPUT" | jq -r '.tool_input.file_path')

    if [[ "$FILE" == *"/migrations/"* ]]; then
        cat << EOF
{
  "systemMessage": "⚠️ Database migration created: $FILE\n\nReminder:\n1. Review migration carefully\n2. Test on dev database first\n3. Run 'prisma migrate deploy' after merge"
}
EOF
    fi
fi

exit 0
```

## Міркування щодо безпеки

1. **Ніколи не зберігайте секрети в hooks**: використовуйте змінні середовища
2. **Валідуйте вхідні дані**: завжди очищуйте дані зі stdin
3. **Обмежуйте область дії hook**: використовуйте конкретні matchers, а не `".*"`
4. **Переглядайте заблоковані операції**: логуйте, коли hooks блокують дії
5. **Тестуйте ізольовано**: спершу тестуйте hooks поза Claude
6. **Контроль версій**: комітьте hooks у репозиторій, щоб ділитися з командою

## Ресурси

- [Основний посібник - розділ 7: Hooks](../../guide/ultimate-guide.uk.md#7-hooks)
- [Документація Claude Code](https://code.claude.com/docs)
- [Довідник подій hooks](../../guide/ultimate-guide.uk.md#71-the-event-system)

---

*Докладні пояснення та просунуті патерни див. в [основному посібнику](../../guide/ultimate-guide.uk.md).*
