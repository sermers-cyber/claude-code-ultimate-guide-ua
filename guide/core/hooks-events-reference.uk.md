---
title: "Довідник подій hooks у Claude Code: усі 33 події, matchers і схеми"
description: "Повний довідник усіх 33 подій hooks у Claude Code: поля matcher, схеми вхідних даних, керування рішеннями та типові таймаути, з готовими до копіювання JSON-прикладами для кожної події."
tags: [reference, hooks]
---

# Довідник подій hooks

Повний довідник усіх 33 подій hooks у Claude Code: поля matcher, схеми вхідних даних, керування рішеннями та типові таймаути. Джерело: офіційна документація Anthropic ([довідник hooks](https://code.claude.com/docs/en/hooks)), звірено з Claude Code v2.1.284.

Про skill для аудиту дивіться `examples/skills/eval-hooks/SKILL.md`.

Див. також: [Event-Driven Agent Automation](../workflows/event-driven-agents.uk.md) про побудову робочих процесів на hooks і [Security Hardening: Startup Hooks](../security/security-hardening.uk.md#16-startup-hooks-code-execution-before-your-first-prompt) про ризики виконання коду через hooks.

---

## Швидкий довідник

| Подія | Коли спрацьовує | Поле matcher | Може блокувати? | Типовий таймаут |
|-------|-----------------|--------------|-----------------|-----------------|
| `SessionStart` | Сесія починається або відновлюється | `source` | Ні | 600s |
| `Setup` | `--init-only` або `-p --init/--maintenance` | `trigger` | Ні | 600s |
| `UserPromptSubmit` | Користувач надсилає prompt | немає | Так | **30s** |
| `UserPromptExpansion` | Slash-команда розгортається в prompt | `command_name` | Так | 600s |
| `PreToolUse` | Перед виконанням виклику інструмента | `tool_name` | Так | 600s |
| `PermissionRequest` | Виклик інструмента потребує рішення про дозвіл | `tool_name` | Не через exit 2; лише JSON-об'єкт `decision` | 600s |
| `PermissionDenied` | Класифікатор auto-режиму відхиляє виклик | `tool_name` | Ні (лише повторна спроба) | 600s |
| `PostToolUse` | Після успішного виклику інструмента | `tool_name` | Ні (stderr іде до Claude) | 600s |
| `PostToolUseFailure` | Після невдалого виклику інструмента | `tool_name` | Ні | 600s |
| `PostToolBatch` | Після завершення всієї паралельної пачки | немає | Так (зупиняє цикл) | 600s |
| `Notification` | Claude надсилає сповіщення | `notification_type` | Ні | 600s |
| `MessageDisplay` | Текст повідомлення асистента надходить потоком | немає | Ні | **10s** |
| `SubagentStart` | Subagent запущено через інструмент Agent | `agent_type` | Ні | 600s |
| `SubagentStop` | Subagent завершує роботу | `agent_type` | Так | 600s |
| `TaskCreated` | Завдання створюється через TaskCreate | немає | Так | 600s |
| `TaskCompleted` | Завдання позначається як виконане | немає | Так | 600s |
| `Stop` | Claude завершує відповідь | немає | Так (продовжує хід) | 600s |
| `StopFailure` | Хід завершується через помилку API | `error` | Ні (ігнорується) | 600s |
| `TeammateIdle` | Учасник команди агентів простоює | немає | Так | 600s |
| `InstructionsLoaded` | Завантажено CLAUDE.md або файл правил | `load_reason` | Ні | 600s |
| `ConfigChange` | Під час сесії змінюється файл конфігурації | `source` | Так (крім `policy_settings`) | 600s |
| `CwdChanged` | Змінюється робочий каталог | немає | Ні | 600s |
| `DirectoryAdded` | Каталог додано через `/add-dir` або SDK `register_repo_root` | `source` | Ні | 600s |
| `FileChanged` | Змінюється відстежуваний файл на диску | ім'я файлу (дослівно) | Ні | 600s |
| `WorktreeCreate` | Створюється worktree | немає | Так (будь-який ненульовий код) | 600s |
| `WorktreeRemove` | Видаляється worktree | немає | Так (будь-який ненульовий код призводить до помилки видалення, якщо каталог лишається) | 600s |
| `PreCompact` | Перед стисненням контексту | `trigger` | Так | 600s |
| `PostCompact` | Після завершення стиснення | `trigger` | Ні | 600s |
| `PreModelSwitch` | Перед застосуванням запитаної зміни моделі | канонічна цільова модель | Так | **30s** |
| `PostModelSwitch` | Після зміни моделі сесії, зокрема автоматичної | канонічна цільова модель | Ні | **30s** |
| `Elicitation` | MCP-сервер запитує введення від користувача | `mcp_server_name` | Так | 600s |
| `ElicitationResult` | Користувач відповідає на MCP elicitation | `mcp_server_name` | Так | 600s |
| `SessionEnd` | Сесія завершується | `reason` | Ні | **бюджет 1.5s** |

**Винятки щодо таймаутів**: типові 600s для `command`, `http` та `mcp_tool` зменшуються до 30s для `UserPromptSubmit`, `PreModelSwitch` і `PostModelSwitch` та до 10s для `MessageDisplay`. Hooks типу `prompt` мають типовий таймаут 30s. Hooks типу `agent` — 60s. `SessionEnd` має загальний бюджет 1.5s; `timeout` окремого hook піднімає його до найбільшого заданого значення, до 60s. Таймаути hooks із plugin бюджет не збільшують. Hook `command`, `http` або `mcp_tool` на `PreToolUse`, що вичерпав час, не блокує виклик інструмента; на `PreModelSwitch` він блокує перемикання.

---

## Значення matcher за подіями

Поле `matcher` фільтрує за різним полем залежно від типу події.

### Події інструментів: matcher фільтрує за `tool_name`

Події: `PreToolUse`, `PostToolUse`, `PostToolUseFailure`, `PermissionRequest`, `PermissionDenied`

Значення: `Bash`, `Edit`, `Write`, `Read`, `Glob`, `Grep`, `Agent`, `WebFetch`, `WebSearch`, `AskUserQuestion`, `ExitPlanMode` та MCP-інструменти у вигляді `mcp__<server>__<tool>`.

Правила зіставлення (для всіх подій, що підтримують matcher):
- Лише літери, цифри, `_`, `-`, пробіли, `,` та `|`: точний рядок або список точних рядків, розділених `|` чи `,` (`Edit|Write`, `Edit, Write`). Дефіси в наборі точного збігу потребують v2.1.195 або новішої.
- Містить будь-який інший символ: незакріплений JavaScript-регулярний вираз (`mcp__memory__.*`). `Edit.*` також збігається з `NotebookEdit`; для збігу всього рядка закріпіть вираз через `^...$`.
- `"*"`, `""` або відсутнє значення: збігається з усім.
- `FileChanged` і `StopFailure` використовують вужчий набір точного збігу (лише літери, цифри, `_`, `|`); дефіс, пробіл чи кома там залишають matcher на шляху регулярного виразу.

Щоб зіставити всі інструменти MCP-сервера: `mcp__memory__.*` (`.*` обов'язкове; `mcp__memory` без нього — це точний рядок, що не збігається з жодним інструментом).

### SessionStart: matcher фільтрує за `source`

| Значення | Коли |
|----------|------|
| `startup` | Нова сесія |
| `resume` | `--resume`, `--continue` або `/resume` |
| `clear` | `/clear` |
| `compact` | Автоматичне або ручне стиснення |
| `fork` | Розгалужена сесія |

### Setup: matcher фільтрує за `trigger`

| Значення | Коли |
|----------|------|
| `init` | `claude --init-only` або `claude -p --init` |
| `maintenance` | `claude -p --maintenance` |

### SessionEnd: matcher фільтрує за `reason`

| Значення | Коли |
|----------|------|
| `clear` | Команда `/clear` |
| `resume` | Інтерактивне перемикання через `/resume` |
| `logout` | Користувач вийшов із облікового запису |
| `prompt_input_exit` | Вихід, коли було видно поле введення prompt |
| `other` | Інші причини виходу |

`bypass_permissions_disabled` видалено у v2.1.234; приберіть його з matchers `SessionEnd`.

### Notification: matcher фільтрує за `notification_type`

Значення: `permission_prompt`, `idle_prompt`, `auth_success`, `elicitation_dialog`, `elicitation_url_dialog`, `elicitation_complete`, `elicitation_response`, `agent_needs_input`, `agent_completed`, `quota_auto_resume_fired`, `quota_auto_resume_stale`, `quota_auto_resume_disabled`

### SubagentStart / SubagentStop: matcher фільтрує за `agent_type`

Значення: `general-purpose`, `Explore`, `Plan` або власні імена агентів (поле `name` із frontmatter агента, а не ім'я файлу).

### PreCompact / PostCompact: matcher фільтрує за `trigger`

Значення: `manual` (з `/compact`), `auto` (автоматично)

### InstructionsLoaded: matcher фільтрує за `load_reason`

Значення: `session_start`, `nested_traversal`, `path_glob_match`, `include`, `compact`

### ConfigChange: matcher фільтрує за `source`

Значення: `user_settings`, `project_settings`, `local_settings`, `policy_settings`, `skills`

### StopFailure: matcher фільтрує за `error`

Значення: `rate_limit`, `overloaded`, `authentication_failed`, `oauth_org_not_allowed`, `account_on_hold`, `billing_error`, `invalid_request`, `model_not_found`, `server_error`, `max_output_tokens`, `cloud_credential_error` (v2.1.267+), `unknown`

### UserPromptExpansion: matcher фільтрує за `command_name`

Назва вашого skill або команди так, як її ввів користувач (без початкового `/`).

### Elicitation / ElicitationResult: matcher фільтрує за `mcp_server_name`

Налаштована назва вашого MCP-сервера.

### DirectoryAdded: matcher фільтрує за `source`

Значення: `slash_command` (`/add-dir`), `register_repo_root` (керівний запит SDK)

### PreModelSwitch / PostModelSwitch: matcher фільтрує за канонічною цільовою моделлю

Matcher порівнюється з канонічною назвою, виведеною з `to_model`, без урахування суфікса `[1m]`: `claude-opus-5`, `claude-opus-4-6|claude-opus-5`, `.*opus.*`. Якщо Claude Code не може вивести канонічну назву (наприклад, для ID, що існує лише на gateway), кожен hook PreModelSwitch виконується незалежно від matcher, тож блокувальний hook має також перевіряти `to_model`.

### FileChanged: matcher = дослівні імена файлів

Розбивається за `|`, кожен сегмент реєструється як дослівне ім'я файлу, що відстежується в поточному каталозі. Приклад: `".envrc|.env"`. На відміну від інших подій, регулярні вирази тут не застосовуються. Те саме значення формує список відстеження І фільтрує, які hooks виконуються.

### Події без підтримки matcher

`UserPromptSubmit`, `PostToolBatch`, `Stop`, `TeammateIdle`, `TaskCreated`, `TaskCompleted`, `WorktreeCreate`, `WorktreeRemove`, `CwdChanged`, `MessageDisplay`

Поле `matcher` для цих подій мовчки ігнорується.

---

## Поведінка коду виходу 2 для кожної події

Код виходу 2 — єдиний, що блокує лише самим кодом. Claude Code читає поля JSON-виводу зі stdout за будь-якого коду виходу, а не лише 0: для подій зі стандартною моделлю рішень чинне JSON-рішення (наприклад, `permissionDecision: "deny"` або `decision: "block"`) діє з кодом 0 чи будь-яким іншим кодом, окрім 2, а код 2 усе одно блокує, навіть якщо JSON каже `allow`. Код виходу 1 без чинного JSON — неблокувальна помилка: дія триває, а перший рядок stderr з'являється в транскрипті. `WorktreeCreate` і `WorktreeRemove` — винятки: для них будь-який ненульовий код означає невдачу.

| Подія | Що відбувається при exit 2 |
|-------|----------------------------|
| `PreToolUse` | Блокує виклик інструмента; stderr передається Claude |
| `PermissionRequest` | Не враховується: потік дозволів триває без змін, а stderr відкидається. Відхиляйте через JSON-об'єкт `decision` |
| `UserPromptSubmit` | Блокує prompt і стирає його з контексту |
| `UserPromptExpansion` | Блокує розгортання |
| `Stop` | Не дає зупинитися; продовжує хід |
| `SubagentStop` | Не дає subagent зупинитися |
| `TeammateIdle` | Учасник продовжує працювати; stderr повертається йому |
| `TaskCreated` | Скасовує створення завдання; stderr повертається |
| `TaskCompleted` | Не дає завершити; stderr повертається |
| `ConfigChange` | Блокує зміну конфігурації (крім `policy_settings`) |
| `PostToolBatch` | Зупиняє агентний цикл перед наступним викликом моделі |
| `PreCompact` | Блокує стиснення |
| `Elicitation` | Відхиляє elicitation |
| `ElicitationResult` | Блокує відповідь (фактична дія стає відмовою) |
| `WorktreeCreate` | **Будь-який** ненульовий код виходу призводить до помилки створення |
| `WorktreeRemove` | **Будь-який** ненульовий код виходу призводить до помилки видалення, якщо каталог після цього ще існує |
| `PreModelSwitch` | Блокує перемикання моделі та показує stderr користувачеві |
| `PostModelSwitch` | Показує stderr лише користувачеві; модель уже перемкнулася |
| `PostToolUse` | Показує stderr Claude (інструмент уже виконався) |
| `PostToolUseFailure` | Показує stderr Claude |
| `StopFailure` | Повністю ігнорується (вивід і код виходу ігноруються) |
| `SessionEnd` | Показує stderr лише користувачеві |
| `SessionStart`, `Setup`, `SubagentStart` | Показує stderr лише користувачеві |
| `Notification` | Показує stderr лише користувачеві |
| `InstructionsLoaded` | Код виходу ігнорується |
| `PermissionDenied` | Код виходу й stderr ігноруються |
| `CwdChanged`, `FileChanged` | Показує stderr лише користувачеві |
| `DirectoryAdded` | Stderr іде в debug-лог; каталог уже додано |
| `PostCompact` | Показує stderr лише користувачеві |
| `MessageDisplay` | Початковий текст відображається без змін |

---

## Формат керування рішеннями для кожної події

### Поле `decision` верхнього рівня

Використовується в: `UserPromptSubmit`, `UserPromptExpansion`, `PostToolUse`, `PostToolUseFailure`, `PostToolBatch`, `Stop`, `SubagentStop`, `ConfigChange`, `PreCompact`

```json
{ "decision": "block", "reason": "Explanation" }
```

Чинним є лише `"block"`. Щоб дозволити, опустіть `decision`. Для `Stop` і `SubagentStop` `reason` стає наступною інструкцією для Claude.

### PreToolUse

Використовує `hookSpecificOutput` для тоншого керування. Пріоритет у разі конфлікту hooks: `deny > defer > ask > allow`.

```json
{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "allow | deny | ask | defer",
    "permissionDecisionReason": "Shown to user (allow/ask) or to Claude (deny)",
    "updatedInput": { "field": "new value" },
    "additionalContext": "Context injected next to tool result"
  }
}
```

`defer` працює лише в неінтерактивному режимі `-p`. Процес завершується з `stop_reason: "tool_deferred"`, і викликаючий процес може відновити роботу пізніше. `defer` не працює, коли Claude робить кілька викликів інструментів одночасно.

### PreModelSwitch

Код виходу 2 або `decision: "block"` верхнього рівня скасовує перемикання. Для тоншого керування використовуйте `hookSpecificOutput.permissionDecision` зі значеннями `allow`, `deny` або `ask` (без `defer`, `updatedInput` чи `additionalContext`).

### TaskCreated

Код виходу 2 або `decision: "block"` верхнього рівня скасовує створення завдання. `continue: false` ігнорується.

### PermissionRequest

Hook, що завершується з кодом 2 без об'єкта `decision`, залишає потік дозволів без змін. Дозволяє чи відхиляє лише об'єкт `decision`. Hooks типу `agent` для цієї події пропускаються. У сесіях, що не можуть показати запит, як-от фонові subagents у режимі `-p`, ці hooks усе одно виконуються, а виклик відхиляється, якщо жоден hook не ухвалив рішення.

```json
{
  "hookSpecificOutput": {
    "hookEventName": "PermissionRequest",
    "decision": {
      "behavior": "allow | deny",
      "updatedInput": {},
      "updatedPermissions": [],
      "message": "Reason for deny",
      "interrupt": false
    }
  }
}
```

### PermissionDenied

Код виходу й stderr ігноруються. Щоб сигналізувати про повторну спробу:

```json
{
  "hookSpecificOutput": {
    "hookEventName": "PermissionDenied",
    "retry": true
  }
}
```

### PostToolUse

```json
{
  "hookSpecificOutput": {
    "hookEventName": "PostToolUse",
    "additionalContext": "Context injected next to tool result",
    "updatedToolOutput": { "stdout": "...", "stderr": "", "interrupted": false, "isImage": false }
  }
}
```

`updatedToolOutput` змінює те, що бачить Claude, а не те, що вже виконано. Має точно відповідати формі виводу інструмента. Для вбудованих інструментів із неправильною формою береться початковий вивід.

### WorktreeCreate

Command hooks друкують абсолютний шлях у stdout. HTTP hooks повертають:

```json
{ "hookSpecificOutput": { "hookEventName": "WorktreeCreate", "worktreePath": "/abs/path" } }
```

Будь-яка помилка або відсутній шлях призводить до помилки створення worktree.

### MessageDisplay

```json
{
  "hookSpecificOutput": {
    "hookEventName": "MessageDisplay",
    "displayContent": "Replacement text shown on screen"
  }
}
```

Змінює лише те, що з'являється на екрані. Claude і транскрипт зберігають оригінал.

### SessionStart (додаткові поля)

```json
{
  "hookSpecificOutput": {
    "hookEventName": "SessionStart",
    "additionalContext": "Context before first prompt",
    "sessionTitle": "branch-or-feature-name",
    "watchPaths": ["/absolute/path/to/watch"],
    "reloadSkills": true,
    "initialUserMessage": "First turn in -p mode"
  }
}
```

`reloadSkills: true` повторно сканує каталоги skills після завершення hooks, тож skills, встановлені hook, одразу доступні в тій самій сесії.

### Elicitation

```json
{
  "hookSpecificOutput": {
    "hookEventName": "Elicitation",
    "action": "accept | decline | cancel",
    "content": { "field_name": "value" }
  }
}
```

### ElicitationResult

Той самий формат, що й вивід Elicitation. Перевизначає те, що надіслав користувач.

### Універсальні поля (для всіх подій)

```json
{
  "continue": false,
  "stopReason": "Message shown to user (not Claude)",
  "suppressOutput": true,
  "systemMessage": "Warning shown to user",
  "terminalSequence": "\033]777;notify;Title;Body\007"
}
```

`continue: false` повністю зупиняє Claude і має пріоритет над усіма полями рішень.

`terminalSequence`: сповіщення робочого столу та заголовки вікон через послідовності OSC. Обмежено OSC `0/1/2/9/99/777` та BEL. Пряме записування в `/dev/tty` не працює починаючи з v2.1.139, бо hooks виконуються без керувального терміналу.

---

## Ключові вхідні поля для кожної події

Усі події отримують: `session_id`, `transcript_path`, `cwd`, `hook_event_name` і зазвичай `permission_mode`. Hooks subagents також отримують `agent_id` та `agent_type`.

| Подія | Додаткові вхідні поля події |
|-------|-----------------------------|
| `SessionStart` | `source`, `model`, за потреби `agent_type`, `session_title` |
| `Setup` | `trigger` (`"init"` або `"maintenance"`) |
| `UserPromptSubmit` | `prompt` |
| `UserPromptExpansion` | `expansion_type`, `command_name`, `command_args`, `command_source`, `prompt` |
| `PreToolUse` | `tool_name`, `tool_input`, `tool_use_id` |
| `PermissionRequest` | `tool_name`, `tool_input`, `permission_suggestions` |
| `PermissionDenied` | `tool_name`, `tool_input`, `tool_use_id`, `reason` |
| `PostToolUse` | `tool_name`, `tool_input`, `tool_response`, `tool_use_id`, `duration_ms` |
| `PostToolUseFailure` | `tool_name`, `tool_input`, `tool_use_id`, `error`, `is_interrupt`, `duration_ms` |
| `PostToolBatch` | `tool_calls` (масив із `tool_name`, `tool_input`, `tool_use_id`, `tool_response`) |
| `Notification` | `message`, `title`, `notification_type` |
| `MessageDisplay` | `turn_id`, `message_id`, `index`, `final`, `delta` |
| `SubagentStart` | `agent_id`, `agent_type` |
| `SubagentStop` | `stop_hook_active`, `agent_id`, `agent_type`, `agent_transcript_path`, `last_assistant_message` |
| `TaskCreated` | `task_id`, `task_subject`, `task_description`, `teammate_name`, `team_name` |
| `TaskCompleted` | `task_id`, `task_subject`, `task_description`, `teammate_name`, `team_name` |
| `Stop` | `stop_hook_active`, `last_assistant_message`, `background_tasks`, `session_crons` |
| `StopFailure` | `error`, `error_details`, `last_assistant_message` |
| `TeammateIdle` | `teammate_name`, `team_name` |
| `InstructionsLoaded` | `file_path`, `memory_type`, `load_reason`, `globs`, `trigger_file_path`, `parent_file_path` |
| `ConfigChange` | `source`, `file_path` |
| `CwdChanged` | `old_cwd`, `new_cwd` |
| `DirectoryAdded` | `directory`, `source` |
| `FileChanged` | `file_path`, `event` (`"change"`, `"add"`, `"unlink"`) |
| `WorktreeCreate` | `name` (slug нового worktree) |
| `WorktreeRemove` | `worktree_path` |
| `PreCompact` | `trigger`, `custom_instructions` |
| `PostCompact` | `trigger`, `compact_summary` |
| `PreModelSwitch` | `from_model`, `to_model`, `requested_model`, `source`, `context_tokens`, `prompt_cache_warm`, `cache_ttl`, `estimated_cache_write_usd`, `pricing` |
| `PostModelSwitch` | Те саме, що й `PreModelSwitch`; `source` додає `auto` і `resume` |
| `Elicitation` | `mcp_server_name`, `message`, `mode`, `url`, `elicitation_id`, `requested_schema` |
| `ElicitationResult` | `mcp_server_name`, `action`, `mode`, `elicitation_id`, `content` |
| `SessionEnd` | `reason` |

---

## Поля обробників hooks

### Спільні поля (для всіх типів)

| Поле | Опис |
|------|------|
| `type` | `command`, `http`, `mcp_tool`, `prompt` або `agent` |
| `if` | Синтаксис правил дозволів для звуження обробника. Лише події інструментів (`PreToolUse`, `PostToolUse`, `PostToolUseFailure`, `PermissionRequest`, `PermissionDenied`). Для будь-якої іншої події hook із заданим `if` ніколи не виконується |
| `timeout` | Секунди до скасування. Не застосовується до запущеного command hook з `async: true`; але застосовується з `asyncRewake` |
| `statusMessage` | Власне повідомлення спінера, поки hook виконується |
| `once` | Виконати один раз за сесію, потім видалити. Враховується лише у frontmatter skill, у файлах налаштувань ігнорується |

### Поля command hook

| Поле | Опис |
|------|------|
| `command` | Shell-команда або шлях до виконуваного файлу |
| `args` | Вектор аргументів: вмикає exec-форму (без участі shell) |
| `async` | `true` — виконувати у фоні без блокування |
| `asyncRewake` | Як `async: true`, але будить Claude при exit 2, показуючи stderr (або stdout, якщо stderr порожній) як системне нагадування |
| `shell` | `"bash"` (типово) або `"powershell"` (Windows) |

**Shell-форма** (`args` відсутній): `command` передається в `sh -c`. Підтримує конвеєри, `&&`, glob-шаблони.
**Exec-форма** (`args` присутній): `command` — виконуваний файл, кожен елемент `args` — один аргумент без змін. Використовуйте для шляхів із пробілами або коли посилаєтеся на `${CLAUDE_PROJECT_DIR}`.

### Поля HTTP hook

| Поле | Опис |
|------|------|
| `url` | URL кінцевої точки POST |
| `headers` | Додаткові заголовки (підтримує інтерполяцію `$VAR`) |
| `allowedEnvVars` | Змінні середовища, які можна інтерполювати у значеннях заголовків |

Відповіді не-2xx не блокують. Щоб заблокувати, поверніть 2xx із `decision: "block"` у JSON-тілі.

### Поля MCP tool hook

| Поле | Опис |
|------|------|
| `server` | Назва підключеного MCP-сервера |
| `tool` | Назва інструмента на цьому сервері |
| `input` | Аргументи інструмента. Рядкові значення підтримують підстановку `${path}` із вхідних даних hook |

Сервер уже має бути підключений. `SessionStart` і `Setup` зазвичай спрацьовують раніше, ніж сервери завершать підключення.

### Поля prompt hook

| Поле | Опис |
|------|------|
| `prompt` | Текст prompt. Використовуйте `$ARGUMENTS` для JSON-входу hook |
| `model` | Перевизначення моделі (типово: швидка модель, зазвичай Haiku) |
| `continueOnBlock` | Коли `ok: false`, повернути причину Claude й продовжити замість зупинки |

Повертає `{ "ok": true/false, "reason": "..." }`. Події, що приймають hooks типу `prompt`, дивіться в [Підтримка типів hooks для кожної події](#hook-type-support-per-event).

### Поля agent hook

| Поле | Опис |
|------|------|
| `prompt` | Опис завдання. Використовуйте `$ARGUMENTS` для JSON-входу hook |
| `model` | Перевизначення моделі |

Запускає subagent, який може використовувати Read, Grep, Glob (до 50 ходів), а потім повертає ту саму схему `{ "ok": true/false }`. Експериментально.

### Підтримка типів hooks для кожної події

| Група подій | Підтримувані типи обробників |
|-------------|------------------------------|
| `PermissionDenied`, `PostToolBatch`, `PostToolUse`, `PostToolUseFailure`, `PreToolUse`, `Stop`, `SubagentStop`, `TaskCompleted`, `TaskCreated`, `TeammateIdle`, `UserPromptExpansion`, `UserPromptSubmit` | `command`, `http`, `mcp_tool`, `prompt`, `agent` |
| `PermissionRequest` | `command`, `http`, `mcp_tool`, `prompt` (hook `agent` пропускається) |
| `ConfigChange`, `CwdChanged`, `DirectoryAdded`, `Elicitation`, `ElicitationResult`, `FileChanged`, `InstructionsLoaded`, `MessageDisplay`, `Notification`, `PostCompact`, `PostModelSwitch`, `PreCompact`, `PreModelSwitch`, `SessionEnd`, `StopFailure`, `SubagentStart`, `WorktreeCreate`, `WorktreeRemove` | `command`, `http`, `mcp_tool` |
| `SessionStart`, `Setup` | `command`, `mcp_tool` |

Для `PermissionDenied` hooks типів prompt і agent виконуються, але їхній вивід відкидається.

---

## Плейсхолдери шляхів

| Плейсхолдер | Розв'язується в |
|-------------|-----------------|
| `${CLAUDE_PROJECT_DIR}` | Кореневий каталог проєкту |
| `${CLAUDE_PLUGIN_ROOT}` | Каталог встановлення plugin (змінюється при оновленні) |
| `${CLAUDE_PLUGIN_DATA}` | Каталог постійних даних plugin (переживає оновлення) |

Для hooks, що посилаються на них, віддавайте перевагу exec-формі: кожен елемент `args` передається без змін, а лапки для пробілів чи спеціальних символів не потрібні.

---

## CLAUDE_ENV_FILE

Доступний у hooks `SessionStart`, `Setup`, `CwdChanged` та `FileChanged`. Записуйте рядки `export VAR=value` у цей шлях, щоб зберегти змінні для наступних команд Bash у сесії.

```bash
if [ -n "$CLAUDE_ENV_FILE" ]; then
  echo 'export NODE_ENV=production' >> "$CLAUDE_ENV_FILE"
fi
```

Використовуйте додавання (`>>`), щоб зберегти змінні, задані іншими hooks.

---

## Типові пастки

**Обмеження на продовження Stop hook**: і `decision: "block"`, і `additionalContext` проходять через вхідне поле `stop_hook_active` та обмеження у 8 послідовних продовжень. Читайте `stop_hook_active` зі stdin і завершуйтеся з кодом 0, коли воно `true`, щоб Claude зупинився чисто.

**Exit 1 не блокує**: без чинного JSON-виводу виклик PreToolUse чи UserPromptSubmit блокує лише exit 2. Exit 1 неблокувальний: дія триває. Hook також може заблокувати з кодом 0 плюс JSON-рішення на кшталт `permissionDecision: "deny"`. Шлях до скрипта, якого не існує, завершується кодом на кшталт 127, який теж неблокувальний, тож помилка в шляху мовчки вимикає бар'єр політики.

**asyncRewake проти async**: `asyncRewake: true` виконує hook у фоні І будить сесію, коли процес завершується з кодом 2, навіть якщо Claude простоює. Використовуйте, коли довга фонова перевірка має повідомити про збій посеред сесії.

**Бюджет SessionEnd**: загальний бюджет 1.5s. Встановлення `timeout: 30` для hook піднімає бюджет до 30s (максимум 60s), але hook без власного `timeout` зберігає типові 1.5s. Таймаути hooks із plugin бюджет не збільшують. `CLAUDE_CODE_SESSIONEND_HOOKS_TIMEOUT_MS=5000` перевизначає бюджет і, починаючи з v2.1.268, також задає таймаут hooks без власного.

**Пакетна доставка MessageDisplay**: в інтерактивному режимі спрацьовує кілька разів на повідомлення (раз на пачку рядків), у режимі `-p`/Agent SDK — раз після повного повідомлення. `final: true` позначає останню пачку; не покладайтеся на непорожній `delta` як на сигнал кінця.

**WorktreeCreate повністю замінює git**: hook має виконати все налаштування worktree. `.worktreeinclude` не обробляється. Копіюйте `.env` та інші локальні файли всередині hook.

**Поле if для подій без інструментів**: додавання `if` до `SessionStart`, `Stop` чи будь-якої події без інструментів мовчки не дає hook виконатися взагалі.

**Кілька hooks PreToolUse з updatedInput**: усі відповідні hooks виконуються паралельно. Конфліктні рішення розв'язуються як `deny > defer > ask > allow`, але документація не визначає, чий `updatedInput` переможе, коли кілька hooks переписують той самий виклик. Уникайте двох hooks на одному matcher, що обидва повертають `updatedInput`.

**PermissionRequest не блокує через exit 2**: використовуйте `hookSpecificOutput.decision.behavior: "deny"` у JSON-виводі. Exit 2 для цієї події не враховується, а hooks типу `agent` для неї пропускаються починаючи з v2.1.280.

**Дубльовані обробники**: той самий обробник, визначений у кількох файлах налаштувань, виконується один раз. Копія того самого обробника з plugin чи skill лишається окремою.

**Prompt hooks на PermissionDenied**: вивід відкидається. Єдине поле, яке ця подія читає, — `hookSpecificOutput.retry`, і hooks типів prompt та agent не можуть його задати. Для сигналів повторної спроби використовуйте command hook.

**Hooks без керувального терміналу**: починаючи з v2.1.139, hooks виконуються без `/dev/tty`. Щоб надіслати сповіщення робочого столу чи заголовки вікон, використовуйте `terminalSequence` у JSON-виводі замість прямого запису escape-послідовностей.

**Типовий таймаут UserPromptSubmit**: 30s, а не 600s. Завислий hook тут блокує все введення користувача. Задайте явний `timeout`, якщо потрібно більше часу.

**Hooks як патерни проєктування**: [AI Design Patterns](./ai-design-patterns.uk.md#observer) зіставляє hooks з Observer, Decorator, Command і Deterministic gate та вказує, де кожна аналогія перестає працювати.
