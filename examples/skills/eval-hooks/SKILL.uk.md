---
name: eval-hooks
description: "Аудит hooks Claude Code і Codex на коректність, безпеку та правильність у settings.json, hooks.json, config.toml, plugin, а також у hooks у frontmatter skills чи агентів. Визначає кожну команду, перевіряє назви подій, типи обробників, matchers, стратегію exit-кодів і JSON-рішень та timeouts за задокументованими правилами кожного хоста, а потім розглядає hooks по одному. Використовуйте під час налаштування hooks, налагодження hook, що ніколи не спрацьовує, ніколи не блокує або підвішує агента, або для періодичної перевірки гігієни hooks. Не для написання нового hook з нуля."
allowed-tools: Read Glob Bash Edit
effort: medium
argument-hint: "[claude | codex | path to a hooks or settings file; default: all locations]"
---

# Оцінювач hooks

Знайдіть кожен hook Claude Code і Codex в межах обсягу, перевірте кожен із них за файловою системою та задокументованою семантикою hooks відповідного хоста, а потім проведіть інтерактивну сесію, щоб підтвердити або покращити їх.

Мета не лише в оцінці; потрібно, щоб кожен hook працював, мав правильний обсяг дії та був безпечним у виконанні.

Джерела істини: офіційний довідник hooks Claude Code (https://code.claude.com/docs/en/hooks) і документація hooks Codex (https://developers.openai.com/codex/hooks). Коли правило нижче розходиться з актуальною документацією, перемагає документація; повідомте про розбіжність, а не оцінюйте за застарілим текстом.

## Коли використовувати

- Перше додавання hooks (перевірте перед комітом)
- Hook ніколи не спрацьовує або спрацьовує на кожен виклик інструмента
- Агент помітно зависає перед виконанням інструмента
- Policy hook має блокувати, але не блокує
- Після копіювання hooks з іншого проєкту, машини чи хоста
- Періодична гігієна: «чи всі ці hooks досі роблять щось корисне?»

## Обсяг

| Аргумент | Що аудитувати |
|---|---|
| немає | Кожне розташування Claude Code і Codex зі списку нижче, що існує |
| `claude` або `codex` | Лише цей хост |
| шлях до файлу | Лише цей файл (settings JSON, `hooks.json`, `config.toml`, файл skill чи агента) |
| `audit-only` або користувач просить без змін | Лише кроки 1-4 і 6: перелічіть кожну запропоновану зміну замість запитань чи редагування й опустіть рядки відгуку користувача зі звіту |

Аудитуйте кожен хост за його власними правилами. Ніколи не оцінюйте hook Codex за семантикою Claude Code чи навпаки.

Коли доступний звіт `ctxharness doctor --format json`, згенерований під час цього завдання, звіряйтеся з ним: кожна знахідка рівня hooks, яку він повідомляє, має з'явитися в аудиті, а кожна додаткова знахідка потребує доказів `file:line`.

---

## Claude Code: ключові поняття

### Типи подій (33)

| Подія | Коли спрацьовує | Ефект exit 2 |
|---|---|---|
| `SessionStart` | Сесія починається або відновлюється | stderr лише користувачу |
| `Setup` | `--init-only` або `--init` / `--maintenance` у режимі `-p` | Ігнорується |
| `UserPromptSubmit` | Prompt надіслано, до обробки | Блокує й стирає prompt |
| `UserPromptExpansion` | Введена команда розгортається в prompt | Блокує розгортання |
| `PreToolUse` | Перед виконанням виклику інструмента | Блокує виклик інструмента |
| `PermissionRequest` | Виклик інструмента потребує рішення про дозвіл | **Не враховується**: відхиляйте через JSON-об'єкт `decision` |
| `PermissionDenied` | Auto mode відхиляє виклик інструмента | Ігнорується (читається лише `hookSpecificOutput.retry`) |
| `PostToolUse` | Після успішного виклику інструмента | stderr до Claude; інструмент уже виконався |
| `PostToolUseFailure` | Після невдалого виклику інструмента | stderr до Claude |
| `PostToolBatch` | Після повного пакета паралельних викликів інструментів | Зупиняє агентний цикл |
| `Notification` | Claude Code надсилає сповіщення | Ігнорується |
| `MessageDisplay` | Під час показу тексту асистента | Показується оригінальний текст |
| `SubagentStart` | Запускається subagent | stderr лише користувачу |
| `SubagentStop` | Subagent завершується | Не дає subagent зупинитися |
| `TaskCreated` | Створюється завдання | Скасовує створення |
| `TaskCompleted` | Завдання позначається виконаним | Не дає завершити |
| `Stop` | Claude завершує відповідь | Не дає зупинитися, хід триває |
| `StopFailure` | Хід завершується помилкою API | Ігнорується (крім `terminalSequence`) |
| `TeammateIdle` | Учасник команди агентів ось-ось простоюватиме | Тримає учасника в роботі |
| `InstructionsLoaded` | Завантажується файл CLAUDE.md або `.claude/rules/*.md` | Ігнорується |
| `ConfigChange` | Конфігураційний файл змінюється посеред сесії | Блокує зміну (крім `policy_settings`) |
| `CwdChanged` | Змінюється робочий каталог | stderr лише користувачу |
| `DirectoryAdded` | Каталог додається через `/add-dir` або `register_repo_root` в SDK | stderr у debug-лог; уже додано |
| `FileChanged` | Відстежуваний файл змінюється на диску | stderr лише користувачу |
| `WorktreeCreate` | Створюється worktree | Будь-який ненульовий exit провалює створення |
| `WorktreeRemove` | Worktree видаляється | Будь-який ненульовий exit провалює видалення, якщо каталог лишається |
| `PreCompact` | Перед compaction | Блокує compaction |
| `PostCompact` | Після compaction | stderr лише користувачу |
| `PreModelSwitch` | Перед запитаним перемиканням моделі | Блокує перемикання |
| `PostModelSwitch` | Після зміни моделі сесії | stderr лише користувачу |
| `Elicitation` | MCP-сервер запитує введення користувача | Відхиляє elicitation |
| `ElicitationResult` | Після відповіді користувача на elicitation | Блокує відповідь (стає відмовою) |
| `SessionEnd` | Сесія завершується | stderr лише користувачу |

### Exit-коди та JSON-вивід

- **Exit 2** блокує для подій, у чиєму рядку це вказано. Жоден JSON не може його скасувати, навіть `permissionDecision: "allow"`.
- **JSON читається за будь-якого exit-коду**, а не лише 0. Для подій зі стандартною моделлю рішень чинний JSON-рішення діє за exit 0 або будь-якого іншого коду, крім 2: `hookSpecificOutput.permissionDecision: "deny"` (PreToolUse, PreModelSwitch), `hookSpecificOutput.decision.behavior: "deny"` (PermissionRequest), `decision: "block"` верхнього рівня (UserPromptSubmit, UserPromptExpansion, PostToolUse, PostToolUseFailure, PostToolBatch, Stop, SubagentStop, ConfigChange, PreCompact, TaskCreated, PreModelSwitch).
- **Будь-який інший ненульовий код без чинного JSON** є неблокувальною помилкою: дія продовжується, а транскрипт показує перший рядок stderr. Відсутній або невиконуваний скрипт завершується з кодом на кшталт 127 і потрапляє в цю категорію, тому помилка в шляху мовчки вимикає policy-бар'єр.
- **stdout за exit 0** стає контекстом лише для `UserPromptSubmit`, `UserPromptExpansion`, `SessionStart` і `PostModelSwitch`; в інших випадках іде в debug-лог.

Policy hook побудований правильно, коли використовує **або** exit 2, **або** JSON-рішення, яке підтримує його подія. Лише exit 1 є дефектом.

### Типові timeouts (секунди)

| Обробник | Типове значення |
|---|---|
| `command`, `http`, `mcp_tool` | 600 |
| те саме, на `UserPromptSubmit`, `PreModelSwitch`, `PostModelSwitch` | 30 |
| те саме, на `MessageDisplay` | 10 |
| `prompt` | 30 |
| `agent` | 60 |
| `SessionEnd` | Загальний бюджет 1,5; `timeout` окремого hook піднімає його до найбільшого налаштованого значення, максимум до 60. Timeouts hooks plugin не піднімають його. `CLAUDE_CODE_SESSIONEND_HOOKS_TIMEOUT_MS` перевизначає його |

`command`, `http` або `mcp_tool` hook на `PreToolUse`, що перевищив timeout, **не** блокує виклик інструмента; на `PreModelSwitch` він блокує перемикання. `timeout` не застосовується до запущеного hook з `async: true`; він застосовується з `asyncRewake`.

### Типи обробників і де вони дозволені

| Тип обробника | Дозволений на |
|---|---|
| `command`, `mcp_tool` | Кожній події |
| `http` | Кожній події, крім `SessionStart` і `Setup` |
| `prompt` | `PermissionDenied`, `PostToolBatch`, `PostToolUse`, `PostToolUseFailure`, `PreToolUse`, `Stop`, `SubagentStop`, `TaskCompleted`, `TaskCreated`, `TeammateIdle`, `UserPromptExpansion`, `UserPromptSubmit`, `PermissionRequest` |
| `agent` (експериментальний) | Те саме, що й `prompt`, крім `PermissionRequest`, де hook agent пропускається |

На `PermissionDenied` hooks prompt і agent запускаються, але їхній вивід відкидається.

### Поля обробників

| Поле | Застосовується до | Примітки |
|---|---|---|
| `type` | усі | `command`, `http`, `mcp_tool`, `prompt`, `agent` |
| `if` | усі | Одне правило дозволу, наприклад `Bash(git *)`. Обчислюється лише на `PreToolUse`, `PostToolUse`, `PostToolUseFailure`, `PermissionRequest`, `PermissionDenied`; на будь-якій іншій події hook ніколи не запускається. Це фільтр за принципом «найкращих зусиль», а не механізм примусу |
| `timeout` | усі | Секунди |
| `statusMessage` | усі | Текст спінера |
| `once` | усі | Враховується лише у frontmatter skill; ігнорується у файлах налаштувань і frontmatter агента |
| `command` | command | Shell-рядок або виконуваний файл, коли задано `args` |
| `args` | command | Exec-форма: без shell, кожен елемент є одним аргументом. Бажана за посилання на `${CLAUDE_PROJECT_DIR}` або `${CLAUDE_PLUGIN_ROOT}` |
| `shell` | command | `bash` або `powershell`; ігнорується, коли задано `args` |
| `async` | command | Працює у фоні; не може блокувати чи ухвалювати рішення |
| `asyncRewake` | command | Працює у фоні й будить Claude, коли процес завершується з кодом 2 |
| `url`, `headers`, `allowedEnvVars` | http | Блокує лише через JSON-тіло 2xx; самі коди статусу ніколи не блокують |
| `server`, `tool`, `input` | mcp_tool | Використовує вже підключений сервер |
| `prompt`, `model` | prompt, agent | `$ARGUMENTS` отримує вхідні дані hook |

### Matchers

| Значення matcher | Як обчислюється |
|---|---|
| `"*"`, `""` або відсутній | Збігається з усім |
| Лише літери, цифри, `_`, `-`, пробіли, `,`, `\|` | Точний рядок або список, розділений `\|` чи `,` (дефіси потребують v2.1.195+) |
| Будь-який інший символ | Незакріплений регулярний вираз JavaScript (`Edit.*` також збігається з `NotebookEdit`; закріплюйте через `^...$`) |

`FileChanged` і `StopFailure` використовують вужчий точний набір (літери, цифри, `_`, `|`). Кожна подія фільтрує інше поле:

| Подія | Що фільтрує matcher |
|---|---|
| `PreToolUse`, `PostToolUse`, `PostToolUseFailure`, `PermissionRequest`, `PermissionDenied` | назву інструмента (`Bash`, `Edit\|Write`, `mcp__server__.*`) |
| `SessionStart` | `startup`, `resume`, `clear`, `compact`, `fork` |
| `Setup` | `init`, `maintenance` |
| `SessionEnd` | `clear`, `resume`, `logout`, `prompt_input_exit`, `other` |
| `Notification` | тип сповіщення |
| `SubagentStart`, `SubagentStop` | тип агента |
| `PreCompact`, `PostCompact` | `manual`, `auto` |
| `PreModelSwitch`, `PostModelSwitch` | канонічну назву цільової моделі |
| `ConfigChange` | джерело конфігурації |
| `DirectoryAdded` | `slash_command`, `register_repo_root` |
| `FileChanged` | літеральні імена файлів для відстеження |
| `StopFailure` | тип помилки |
| `InstructionsLoaded` | причину завантаження |
| `UserPromptExpansion` | назву команди |
| `Elicitation`, `ElicitationResult` | назву MCP-сервера |

**Без підтримки matcher** (matcher мовчки ігнорується): `UserPromptSubmit`, `PostToolBatch`, `Stop`, `TeammateIdle`, `TaskCreated`, `TaskCompleted`, `WorktreeCreate`, `WorktreeRemove`, `CwdChanged`, `MessageDisplay`.

### Модель виконання

- Усі hooks, що збіглися, запускаються **паралельно**.
- Той самий обробник, визначений у кількох файлах налаштувань, запускається **один раз**. Копія того самого обробника з plugin чи skill лишається окремою.
- Hooks `PermissionRequest` також запускаються в сесіях, які не можуть показати запит, наприклад фонові subagents у режимі `-p`; якщо жоден hook не ухвалив рішення, виклик відхиляється.
- Кілька рішень `PreToolUse` розв'язуються як `deny > defer > ask > allow`. Документація не визначає, який `updatedInput` перемагає, коли кілька hooks переписують той самий виклик.
- Продовження `Stop` і `SubagentStop` через `decision: "block"` або `additionalContext` обмежені вхідним полем `stop_hook_active` і лімітом у 8 послідовних продовжень.
- Hooks типу command працюють без керувального термінала: інтерактивні команди (`read`, `fzf`, `gum`, будь-який TUI) не можуть отримати введення. Для сповіщень використовуйте `terminalSequence` у JSON-виводі.

---

## Claude Code: скановані розташування

| Розташування | Обсяг | Примітки |
|---|---|---|
| Керовані налаштування політики | Організація | Не можна вимкнути користувацьким, проєктним чи локальним `disableAllHooks` |
| `~/.claude/settings.json` | Користувач | Не читається хмарними сесіями |
| `.claude/settings.json` | Проєкт, комітиться | |
| `.claude/settings.local.json` | Проєкт, особисте | |
| Plugin `hooks/hooks.json` | Поки plugin увімкнено | |
| Frontmatter skill `hooks:` | Решта сесії після виклику skill | `once: true` враховується лише тут |
| Frontmatter subagent `hooks:` | Поки працює цей subagent | `Stop` стає `SubagentStop`. Hooks проєктних subagents запускаються лише після прийняття довіри до робочої області, зокрема й у `-p` |

`~/.claude/settings.local.json` **не** є задокументованим розташуванням налаштувань. Якщо він існує, повідомте про нього як про недокументований і не оцінюйте його hooks як активні.

Також зафіксуйте з ефективних налаштувань:

- `disableAllHooks: true` вимикає кожен некерований hook; лише значення на керованому рівні вимикає керовані hooks.
- `allowManagedHooksOnly` блокує hooks користувача, проєкту, локальні й plugin (plugins, примусово ввімкнені в керованому `enabledPlugins`, виключені).
- `allowedHttpHookUrls` і `httpHookAllowedEnvVars` обмежують HTTP hooks з усіх джерел.
- Інтерактивні сесії притримують кожен hook із файлів налаштувань, доки не прийнято довіру до робочої області; сесії `-p` і SDK вважають теку довіреною.

---

## Codex: ключові поняття

### Розташування

| Розташування | Примітки |
|---|---|
| `~/.codex/hooks.json` | Користувач |
| `~/.codex/config.toml` вбудований `[hooks]` | Користувач |
| `<repo>/.codex/hooks.json`, `<repo>/.codex/config.toml` | Завантажуються лише коли шар проєктного `.codex/` довірений |
| Plugin `hooks/hooks.json` або запис `hooks` у `.codex-plugin/plugin.json` | Шляхи маніфеста мають лишатися всередині кореня plugin |
| Керований `requirements.toml` `[hooks]` | Довірений за політикою; `allow_managed_hooks_only = true` пропускає hooks користувача, проєкту, сесії та plugin |

Завантажується кожне джерело; вищі шари не замінюють нижчі. Шар, що містить і `hooks.json`, і вбудований `[hooks]`, зливається з попередженням під час запуску: позначте це й порадьте одне представлення на шар. `[features] hooks = false` вимикає hooks (`codex_hooks` є застарілим псевдонімом).

### Перевірка довіри

Кожен некерований hook, зокрема hooks plugin, має бути переглянутий і схвалений у `/hooks`, перш ніж запуститися. Довіра фіксується щодо поточного хешу hook, тож відредагований hook пропускається, доки його не схвалять знову. Під час аудиту повідомляйте, що змінений hook потребує перегляду; не вважайте, що він запускається. Браузер `/hooks` є авторитетним поданням довіри. Поточні збірки Codex також зберігають її в `[hooks.state]` у `config.toml`, що не задокументовано: повідомляйте те, що там бачите, не друкуючи значень хешів, і ніколи не трактуйте `[hooks.state]` як подію. `--dangerously-bypass-hook-trust` обходить перевірку лише для одного виклику: позначайте будь-яку автоматизацію, що на нього покладається.

Перш ніж читати стан довіри як поведінку під час виконання, перевірте, як запускається `codex`: `type codex` і `which -a codex`. Інтеграція термінала може поставити першою в `PATH` обгортку, що додає `--dangerously-bypass-hook-trust` і перевизначення `-c hooks...` до кожного виклику; тоді Codex перелічує цей прапорець серед попереджень під час запуску. Спостерігалося з cmux, чия обгортка пропускає ін'єкцію, коли `CMUX_CODEX_HOOKS_DISABLED=1`. За такої обгортки кожен hook запускається без перегляду: повідомте, що знахідки про довіру не описують те, що реально запускається.

### Події (12) і matchers

| Подія | Що фільтрує matcher |
|---|---|
| `PreToolUse`, `PostToolUse`, `PermissionRequest` | назву інструмента (`Bash`, `apply_patch`, назви MCP; `Edit` або `Write` також збігаються з `apply_patch`) |
| `SessionStart` | `startup`, `resume`, `clear`, `compact` |
| `SessionEnd` | наразі лише `other` |
| `PreCompact`, `PostCompact` | `manual`, `auto` |
| `SubagentStart`, `SubagentStop` | тип subagent |
| `UserPromptSubmit`, `Stop`, `Interrupt` | не підтримується (matcher ігнорується) |

Matchers Codex є рядками регулярних виразів. `Interrupt` і `SessionEnd` не запускаються для subagents.

### Обробники та вивід

- Запускаються лише обробники `command` і `mcp_tool`. Обробники `prompt` і `agent` розбираються й пропускаються: позначайте їх як мертву конфігурацію.
- `timeout` у секундах, типово 600. `SessionEnd` і `Interrupt` типово 1 і дозволяють щонайбільше 3.
- Необов'язкові поля: `statusMessage`, `async`, `additionalContextLimit` (типово 2 500 токенів; `0` пропускає все й може затопити контекст), `commandWindows` / `command_windows`.
- Команди запускаються з `cwd` сесії. Для локальних скриптів репозиторію визначайте шлях від кореня git, а не відносним шляхом `.codex/hooks/...`.
- `PreToolUse` ігнорує звичайний текстовий stdout. Він блокує через `permissionDecision: "deny"`, застарілий `decision: "block"` або exit 2 з причиною в stderr. Він переписує виклик через `permissionDecision: "allow"` разом із `updatedInput` (рядок `command` для `Bash` і `apply_patch`, замінні аргументи для інструментів MCP), у тій самій формі, що й у Claude Code. `permissionDecision: "ask"`, `continue`, `stopReason` і `suppressOutput` там не підтримуються: Codex позначає запуск hook як невдалий і **продовжує виклик інструмента**. Позначайте будь-який policy hook Codex, що на них покладається.
- Фонові (`async`) hooks не можуть блокувати, схвалювати чи переписувати; одночасно працює не більше восьми; `SessionEnd` завжди запускається синхронно.
- `SessionEnd` не підтримує hooks інструментів MCP.
- Plugins, написані для Claude Code, можуть друкувати вивід, який Codex відхиляє. Спостерігалося на Codex 0.159.2: hook `SessionStart`, що друкує два JSON-об'єкти (`{"async": true, ...}`, а потім об'єкт метрик), завершується помилкою `hook returned invalid session start JSON output`, а hook `Stop`, що друкує `{"metrics": ...}`, завершується помилкою `hook returned invalid stop hook JSON output`. Прочитайте файл hooks, названий у `.codex-plugin/plugin.json` plugin, який може відрізнятися від `hooks/hooks.json` (наприклад, `hooks/codex-hooks.json`), запустіть кожен hook plugin один раз із прикладом payload для його події та розберіть stdout відповідно до контракту цієї події. Порадьте вимкнути plugin у Codex, коли кілька його подій дають збій.

---

## Критерії оцінювання (10 балів на hook)

| # | Критерій | Макс | Що перевіряється |
|---|-----------|-----|-----------------|
| 1 | **подія й тип обробника** | 1 | Подія існує для цього хоста, а тип обробника на ній дозволений (hook agent у Claude на `PermissionRequest` або hook prompt у Codex отримують 0) |
| 2 | **matcher** | 2 | Немає matcher на події без підтримки matcher, або matcher використовує задокументовані значення цієї події (1); немає match-all чи широкого regex на події інструмента в парі з повільною командою (1) |
| 3 | **команда** | 3 | Непорожня (1); скрипт чи бінарний файл визначається на диску після підстановки `${CLAUDE_PROJECT_DIR}`, `${CLAUDE_PLUGIN_ROOT}` або кореня git (1); скрипт виконуваний, або передається інтерпретатору (`bash script.sh`, `python3 script.py`), або запускається в exec-формі з визначуваним виконуваним файлом (1) |
| 4 | **timeout** | 2 | Ефективний timeout (явний або задокументований типовий) відповідає події: hooks на інтерактивному шляху (`PreToolUse`, `PermissionRequest`, `UserPromptSubmit`, `PreModelSwitch`, `Stop`) менше 30 с або мають внутрішній захист за timeout (1); немає явного значення, що перевищує задокументований ліміт чи бюджет, наприклад `SessionEnd` Codex понад 3 або `SessionEnd` Claude понад 60 (1) |
| 5 | **розуміння блокування** | 2 | Для hook, призначеного примушувати політику: блокує через exit 2 або JSON-рішення, яке підтримують подія й хост, а не exit 1 (1); немає інтерактивної команди, немає покладання на timeout для блокування `PreToolUse`, немає непідтримуваного поля виводу Codex (1) |
| Бонус | **гігієна** | +1 | Немає зайвої копії того самого обробника в межах одного обсягу, і `$CLAUDE_PROJECT_DIR` або шлях від кореня git замість жорстко закодованого абсолютного проєктного шляху |

**Пороги:**
- ✅ Добре: ≥8/10 (≥80%)
- ⚠️ Потребує доопрацювання: 5-7/10 (50-79%)
- ❌ Виправити: <5/10 (<50%)

**Спостережні hooks** (логування, ін'єкція контексту, форматування, події, що не можуть блокувати): пропускайте критерій 5 й оцінюйте максимум за 8 балів. Позначайте 🔵. Чи «призначений примушувати політику», визначайте за скриптом і відповіддю користувача, а не лише за назвою події.

---

## Інструкції з виконання

### Крок 1: Виявлення

Перелічіть розташування, що існують для кожного хоста в обсязі. Claude Code:

```bash
ls ~/.claude/settings.json .claude/settings.json .claude/settings.local.json 2>/dev/null
ls ~/.claude/settings.local.json 2>/dev/null && echo "undocumented location"
```

Codex:

```bash
ls ~/.codex/hooks.json ~/.codex/config.toml .codex/hooks.json .codex/config.toml 2>/dev/null
type codex; which -a codex   # a wrapper first on PATH can inject hooks and bypass trust
```

Plugins входять до типового обсягу, бо їхні hooks працюють, поки plugin увімкнено. Для Claude Code візьміть увімкнені plugins із `enabledPlugins` в ефективних налаштуваннях, а встановлену версію кожного з `~/.claude/plugins/installed_plugins.json`; кеш plugin може містити кілька версій і тимчасові checkout, тож читайте лише встановлену. Перелічіть кожен hook plugin; оцінюйте їх лише на прохання користувача, оскільки цей код не належить користувачу. Для Codex читайте `hooks/hooks.json` plugin або запис `hooks` у `.codex-plugin/plugin.json`.

Також прочитайте блоки `hooks:` у `.claude/skills/**/SKILL.md` і `.claude/agents/**/*.md`, ідучи за символічними посиланнями на каталоги skills. Керовані налаштування й `requirements.toml` у цьому аудиті лише для читання: повідомляйте про них, ніколи не редагуйте.

Зазначте, які hooks належать зовнішньому інсталятору (наприклад, інструмент із командою `install-hooks` чи `upgrade`). Такий інсталятор може відновити свої записи після ручного очищення, тому радьте зміну через цей інструмент або зафіксуйте ризик дрейфу поруч із пропозицією.

Побудуйте плоский список записів hooks:
- `host`: `claude` або `codex`
- `source_file` і `scope`
- `event_type`, `matcher` (або відсутній)
- `type` і його поля, специфічні для типу (`command`, `args`, `url`, `server`/`tool`, `prompt`)
- `timeout` (секунди, явний або типовий), `async`, `asyncRewake`, `if`, `once`

Якщо hooks не знайдено в жодному розташуванні, повідомте про це й зупиніться.

Готово, коли: кожне існуюче розташування перелічене з його хостом і обсягом, а кожен hook має запис (або аудит зупинився з «hooks не знайдено»).

### Крок 2: Визначення команд (лише hooks типу command)

Розбийте `command` у shell-формі на shell-слова, перш ніж його визначати. Розбиття першого слова через `awk` хибне: воно зберігає лапки й ділить `"$CLAUDE_PROJECT_DIR"/.claude/hooks/x.sh` на два слова. Використовуйте розбірник shell-слів:

```bash
python3 - "$command" "$PROJECT_ROOT" <<'EOF'
import os, shlex, shutil, sys
cmd, root = sys.argv[1], sys.argv[2]
words = shlex.split(cmd.split(';')[-1].split('&&')[-1])
words = [os.path.expanduser(w.replace('${CLAUDE_PROJECT_DIR}', root).replace('$CLAUDE_PROJECT_DIR', root)) for w in words]
while words and (words[0] == 'env' or '=' in words[0].split('/')[0]):
    words.pop(0)  # skip env and VAR=value prefixes
exe = words[0] if words else ''
path = exe if '/' in exe else (shutil.which(exe) or '')
print('executable', exe, 'found' if path and os.path.exists(path) else 'not found', 'x' if path and os.access(path, os.X_OK) else '-')
if os.path.basename(exe) in {'bash', 'sh', 'zsh', 'node', 'python3', 'python', 'deno', 'bun'}:
    script = next((w for w in words[1:] if not w.startswith('-')), '')
    print('script', script, 'found' if os.path.isfile(script) else 'not found', 'readable' if os.access(script, os.R_OK) else '-')
EOF
```

- З `args` (exec-форма) `command` визначається в `PATH` або як шлях; елементи `args` є літеральними.
- Для `bash script.sh`, `node script.js`, `python3 script.py` перевірте, що скрипт існує й читається; `chmod +x` не потрібен.
- Перед перевіркою підставте `${CLAUDE_PROJECT_DIR}` кореневим каталогом проєкту, а `$(git rev-parse --show-toplevel)` коренем репозиторію.
- Для ланцюга команд на кшталт `export PATH=...; tool ...` визначайте останню команду, що виконує роботу, і зазначте ланцюг.
- Ім'я, визначене в `PATH`, зараз доводить лише `PATH` поточного shell, а не середовище, яке хост дає hooks. Позначте його як визначене й скажіть, що `PATH` часу виконання не перевірено.

Позначайте:
- **Не знайдено**: за цим шляхом нічого немає; для policy hook це мовчки вимикає бар'єр
- **Не виконуваний**: скрипт, що запускається напряму, без `chmod +x`
- **Відносний шлях**: визначається від `cwd` сесії, який змінюється
- **Інтерактивна команда** (`read`, `fzf`, `gum`, TUI): у hooks немає керувального термінала

Готово, коли: кожен hook типу command позначений як знайдений чи ні, виконуваний чи ні, із визначеним шляхом.

### Крок 3: Перевірка стратегії блокування

Для hooks на подіях, що можуть блокувати (див. таблиці вище), чия команда є локальним скриптом:

1. Прочитайте скрипт.
2. Класифікуйте:
   - **exit 2 на шляху блокування**: ✅
   - **JSON-рішення, яке підтримують подія й хост** (`permissionDecision: "deny"`, `decision.behavior: "deny"`, `decision: "block"`): ✅, незалежно від exit-коду
   - **exit 1 або загальний ненульовий код на шляху блокування, без JSON**: ⚠️ дія продовжується
   - **exit 2 на `PermissionRequest`** (Claude Code): ⚠️ не враховується; використовуйте об'єкт `decision`
   - **`permissionDecision: "ask"` або `continue: false` у Codex на `PreToolUse`**: ⚠️ не підтримується, виклик інструмента продовжується
   - **Жодного рішення**: 🔵 спостережний, нормально, якщо так задумано
3. Позначайте повільні операції (`curl`, `sleep`, мережеві виклики) без внутрішнього захисту за timeout у hooks на інтерактивному шляху.
4. Перш ніж позначати повільну операцію щодо короткого `timeout`, перевірте, чи вона працює відокремлено (`( ... ) &` з `disown`, `nohup`, `setsid`). Відокремлена робота переживає hook, тож короткий timeout там правильний; повідомте натомість про відокремлену роботу.
5. Для скомпільованого бінарного файлу або скрипта, надто великого для повного читання, не вгадуйте його логіку рішень. Зафіксуйте версію (`--version` або `--help`), класифікуйте стратегію блокування як `UNKNOWN` і запропонуйте behavior canary (приклад payload на stdin, а потім exit-код і stdout).
6. Перш ніж рекомендувати чи відкидати специфічний для хоста варіант hook (наприклад, підкоманду `codex` замість `claude`), запустіть обидва на тому самому прикладі payload з кількох робочих каталогів, зокрема зі scratch-репозиторію поза вашими звичними проєктами, і порівняйте кожен вивід із контрактом хоста. Вивід може залежати від каталогу: у rtk 0.50.0 `rtk hook claude` повертав `updatedInput` з `permissionDecision: "allow"` в одному репозиторії і без рішення в scratch-репозиторії, що Codex відхиляє (`PreToolUse hook returned updatedInput without permissionDecision:allow`); `rtk hook codex` повертав рішення в обох. Обробник з назвою Claude під Codex не є дефектом лише тоді, коли його вивід відповідає контракту Codex у кожному перевіреному каталозі.
7. Коли статичні перевірки проходять, але поведінка викликає сумнів, запустіть живий canary: одноразовий git-репозиторій, свіжа сесія, один невеликий prompt на редагування. Порахуйте рядки `Hook failed` і, для інструмента створення контрольних точок, записи на одне редагування. Повідомте версію хоста й точні повідомлення про збої.

Готово, коли: кожен hook на основі скрипта на події, що блокує, має одну з класифікацій вище або `UNKNOWN` із запропонованим canary, а кожен вердикт щодо специфічного для хоста варіанта вказує каталоги, в яких його тестували.

### Крок 4: Перевірка дублікатів і мертвої конфігурації

- Claude Code: той самий обробник у кількох файлах налаштувань запускається один раз. Повідомляйте це як зайву конфігурацію для очищення, а не як подвійне виконання. Копія того самого обробника з plugin чи skill запускається окремо: повідомляйте її як справжній дублікат.
- Matcher на події без підтримки matcher (мовчки ігнорується).
- `if` на не-інструментальній події (hook ніколи не запускається).
- `once` поза frontmatter skill (ігнорується).
- Тип обробника, не дозволений на його події (пропускається).
- `async: true` разом із полем рішення (не має ефекту).
- Два чи більше hooks `PreToolUse` на тому самому matcher, що повертають `updatedInput` (переможець не задокументований).
- Hook Stop, що завжди продовжує, не читаючи `stop_hook_active`.
- Codex: шар і з `hooks.json`, і з вбудованим `[hooks]`; hooks, що очікують перегляду довіри. Коли обидва представлення запускають той самий інструмент на тій самій події, навіть через різні командні рядки (скрипт-обгортка й бінарний файл, який він викликає), повідомляйте про справжній подвійний запуск і називайте інсталятор, якому належить кожен запис.
- Секрети у джерелах hooks чи налаштуваннях: літерали, схожі на токени, облікові дані в `headers` або `env`. Повідомляйте файл і рядок із редагованим значенням і радьте винести значення з джерела та змінити (rotate) його.

Готово, коли: кожна знахідка прикріплена до запису hook, або список явно порожній.

### Крок 5: Інтерактивний перегляд (серце skill)

Опрацьовуйте hooks **по одному**. Не збирайте їх у пакет і не пропускайте взаємодію.

**Для кожного hook:**

Покажіть:
```
Hook: PreToolUse → Bash [claude, project settings]
type: command
command: ${CLAUDE_PROJECT_DIR}/.claude/hooks/confirm-git-push.sh
timeout: (none, default 600s)
Script: found (executable ✅)
Blocking strategy: JSON permissionDecision "deny" ✅
```

Поставте три запитання:
1. «Чи спрацьовує цей hook у потрібний час і з потрібним обсягом? (y = так / n = змінити matcher або подію)»
2. «Чи команда досі працює правильно? (y / зламана / не впевнений)»
3. «Є що змінити (matcher, команду, timeout, видалити)? (опишіть або пропустіть)»

**Для lifecycle hooks (без matcher):**

Покажіть:
```
Hook: SessionEnd [claude, user settings]
type: command
command: ~/.claude/hooks/session-summary.sh
timeout: (none, 1.5s SessionEnd budget)
Script: found (executable ✅)
```

Запитайте:
1. «Чи цей hook досі корисний? (y / n)»
2. «Чи команда працює в межах timeout? (y / зламана / не впевнений)»

**Якщо користувач вносить зміни під час взаємодії**: застосуйте їх через Edit, підтвердьте кожну зміну, а потім переходьте до наступного hook. Ніколи не редагуйте керовані налаштування чи `requirements.toml`. Після редагування hook Codex нагадайте користувачу, що його треба схвалити в `/hooks` знову.

Готово, коли: кожен hook має три відповіді користувача (або дві для lifecycle hooks), а кожне погоджене редагування застосоване й підтверджене.

### Крок 6: Звіт

Після перегляду всіх hooks:

```
# Hooks Audit: [project or global]
Date: [today] | Scanned: N hooks across M files (Claude Code: X, Codex: Y)

## Summary

| Status | Count |
|--------|-------|
| ✅ Good (≥80%) | N |
| ⚠️ Needs work (50-79%) | N |
| ❌ Fix (<50%) | N |
| 🔵 Observational | N |
| ✅ User confirmed useful | N |
| ⚠️ User flagged for update | N |
| 🗑️ User marked as stale | N |

---

## Per-Hook Results

### PreToolUse → Bash [claude, user settings] (7/10 ⚠️)

type: command
command: `~/.claude/hooks/confirm-git-push.sh`
timeout: (none, default 600s)

| Criterion | Score | Notes |
|-----------|-------|-------|
| event and handler type | ✅ 1/1 | PreToolUse, command |
| matcher | ✅ 2/2 | scoped to Bash |
| command | ✅ 3/3 | found, executable |
| timeout | ⚠️ 1/2 | 600s default on the interactive path, script calls the network without a guard |
| blocking awareness | ⚠️ 0/2 | block path exits 1 without JSON: the tool call proceeds |

**Priority fixes:**
1. Replace `exit 1` with `exit 2`, or print a `permissionDecision: "deny"` JSON object
2. Add `"timeout": 10` or an internal timeout around the network call

User feedback: ✅ scope correct
Content: exit strategy fixed ✅

---

### PostToolUse → Edit|Write [claude, user settings] (8/8 ✅) 🔵

type: command
command: `~/.claude/hooks/anti-ai-markers.sh`
timeout: 2

Observational hook: exit 2 would only show stderr to Claude. All applicable criteria pass. User confirmed still useful.

---
```

Готово, коли: звіт перелічує кожен просканований hook з його оцінкою та примітками за критеріями.

### Крок 7: Підсумок виправлень

```
## What Changed This Session

confirm-git-push.sh hook:
  - Exit strategy changed to exit 2
  - Added timeout: 10

session-summary.sh hook:
  - User confirmed useful, no changes

rtk-baseline.sh hook (codex):
  - Edited; needs re-trust in /hooks
  - User flagged as stale (awaiting explicit deletion confirmation)

---
N hooks audited · N edits applied · N flagged as stale · N redundant copies · N awaiting Codex trust review
```

Для будь-якого hook, який користувач позначив як застарілий (stale): попросіть явне підтвердження перед видаленням. Ніколи не видаляйте без чіткого «так, видали».

Готово, коли: підсумкові лічильники збігаються з результатами по кожному hook, і жодне видалення не відбулося без явного підтвердження.

---

## Граничні випадки

- **Вбудований однорядковий виклик** (наприклад, `rtk hook claude`): пропустіть перевірки рівня скрипта, перевірте, що бінарний файл є в `PATH`
- **Вбудований `bash -c '...'`**: розберіть внутрішній скрипт на предмет інтерактивних команд і логіки exit
- **`exit 1` у policy hook без JSON**: ⚠️ неблокувальний, дія продовжується
- **Той самий hook у налаштуваннях користувача й проєкту (Claude Code)**: запускається один раз; зазначте обидва розташування як зайву конфігурацію
- **`timeout: 0`**: позначте як імовірно недійсний
- **Невідома подія** (наприклад, `PreToolCall`): ❌, повідомте точний рядок і запропонуйте задокументовану назву для цього хоста
- **Подія лише для Claude у файлі Codex** (наприклад, `PostToolUseFailure`, `PreModelSwitch`) або навпаки (`Interrupt` у налаштуваннях Claude): ❌ ніколи не спрацьовує на цьому хості
- **Скрипт не виконуваний і запускається напряму**: завершується неблокувальною помилкою; запропонуйте `chmod +x`
- **Matcher на події без підтримки matcher**: мовчки ігнорується, запропонуйте його прибрати
- **`async: true` з `decision` або `permissionDecision`**: ⚠️ не має ефекту
- **`asyncRewake: true`**: у фоні, будить Claude за exit 2 зі stderr (або stdout); використовуйте замість `async`, коли збій у фоні має дійти до Claude
- **Hook `prompt` або `agent`**: немає команди для визначення; перевірте, що `prompt` присутній і що подія дозволяє цей тип
- **Hook SessionEnd із важкою роботою**: типовий бюджет 1,5 с у Claude Code, типово 1 с і максимум 3 с у Codex; попередьте, що його можуть убити
- **`PermissionRequest` у `-p` або фонових subagents (Claude Code)**: hooks усе одно запускаються; якщо жоден не ухвалив рішення, виклик відхиляється. Не радьте через це переходити на `PreToolUse`
- **`if` на не-інструментальній події**: hook ніколи не запускається; приберіть `if` або змініть подію
- **Hook Stop без перевірки `stop_hook_active`**: продовження зупиняються на ліміті у 8 послідовних; прочитайте поле й завершіться з exit 0, коли воно `true`
- **Жорстко закодований абсолютний проєктний шлях**: запропонуйте `${CLAUDE_PROJECT_DIR}/...` (Claude Code, бажана exec-форма) або шлях від кореня git (Codex)
- **Hooks не спрацьовують як очікувалося**: Claude Code: відкрийте `/hooks` (браузер лише для читання, що показує джерело кожного hook) і запустіть із `--debug`. Codex: відкрийте `/hooks`, щоб побачити джерела, очікувані перегляди довіри та вимкнені hooks
