---
title: "Claude Code: Візуальні діаграми системи конфігурації"
description: "Пріоритет managed settings, skills і commands, subagents та життєвий цикл hooks"
tags: [configuration, hooks, agents, skills, commands]
---

# Система конфігурації

Задокументований пріоритет налаштувань і спрощений огляд розширюваності та hooks.

---

### Пріоритет конфігурації (5 рівнів)

Для одного й того самого ключа налаштувань задокументований стек має п'ять рівнів, від найвищого. Списки можуть зливатися, а для чутливих до безпеки налаштувань діють винятки. Пріоритет змінних оточення визначається окремо для кожного налаштування; CLAUDE.md належить до контексту інструкцій, а не до цього стеку налаштувань.

```mermaid
flowchart TD
    A[1. Managed settings<br/>Політика організації] --> B[2. Аргументи командного рядка<br/>Прапорці сесії та --settings]
    B --> C[3. Локальні налаштування проєкту<br/>.claude/settings.local.json]
    C --> D[4. Спільні налаштування проєкту<br/>.claude/settings.json]
    D --> E[5. Налаштування користувача<br/>~/.claude/settings.json]
    E -.-> FALL[Вбудоване резервне значення<br/>Якщо жодне джерело не задає значення]
    ENV[Змінні оточення<br/>Пріоритет визначається для кожного ключа] -.-> B
    style A fill:#6DB3F2,color:#222
    click A href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#34-precedence-rules" "Precedence rules"
    style B fill:#6DB3F2,color:#222
    click B href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#34-precedence-rules" "Precedence rules"
    style C fill:#6DB3F2,color:#222
    click C href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#34-precedence-rules" "Precedence rules"
    style D fill:#6DB3F2,color:#222
    click D href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#34-precedence-rules" "Precedence rules"
    style E fill:#6DB3F2,color:#222
    click E href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#34-precedence-rules" "Precedence rules"
    style FALL fill:#6DB3F2,color:#222
    click FALL href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#34-precedence-rules" "Precedence rules"
    style ENV fill:#6DB3F2,color:#222
    click ENV href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#34-precedence-rules" "Precedence rules"
```

<details>
<summary>ASCII версія</summary>

```
Найвищий пріоритет
1. Managed settings
2. Аргументи командного рядка
3. .claude/settings.local.json
4. .claude/settings.json
5. ~/.claude/settings.json
Резерв: вбудоване значення, якщо нічого не налаштовано

Змінні оточення: визначаються для кожного ключа, це не універсальний шостий рівень.
CLAUDE.md: інструкції, поза цим стеком налаштувань.
Списки можуть зливатися; див. задокументовані винятки для чутливих до безпеки налаштувань.
```

</details>

> **Джерело**: [Правила пріоритету](../ultimate-guide.uk.md#34-правила-пріоритету)
>
> **Офіційний довідник**: [Settings precedence](https://code.claude.com/docs/en/settings#settings-precedence) та [environment-variable precedence](https://code.claude.com/docs/en/env-vars#precedence).
>
> Для вибору моделі використовується змінна ANTHROPIC_MODEL. CLAUDE_CONFIG_DIR змінює каталог конфігурації. Вибір моделі через CLI залишається обмеженим managed-параметром availableModels і не перевизначає політику організації.

---

### Skills проти commands проти agents: коли що використовувати

Власні commands об'єднано зі skills. Обидва формати файлів створюють slash-команду; skills також підтримують вбудовані ресурси та виклик самим Claude. Subagent використовують окреме вікно контексту для делегованої роботи. Для цих механізмів існують рівні користувача й проєкту.

```mermaid
flowchart LR
    Q{Потрібен окремий контекст<br/>для делегованих міркувань?} -->|Так| A[Визначення subagent<br/>.claude/agents/name.md<br/>Інструмент Agent, власний prompt та інструменти]
    Q -->|Ні| S[Skill<br/>.claude/skills/name/SKILL.md<br/>Ресурси та керування викликом]
    C[Сумісний формат command<br/>.claude/commands/name.md] --> S
    S --> I[Slash-команда або виклик Claude<br/>Залежно від конфігурації]
    A --> R[Підсумок повертається до батьківського]
    I --> U[Рівень користувача або проєкту]
    R --> U
    style Q fill:#6DB3F2,color:#222
    click Q href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#51-understanding-skills" "Understanding skills"
    style A fill:#6DB3F2,color:#222
    click A href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#51-understanding-skills" "Understanding skills"
    style S fill:#6DB3F2,color:#222
    click S href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#51-understanding-skills" "Understanding skills"
    style C fill:#6DB3F2,color:#222
    click C href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#51-understanding-skills" "Understanding skills"
    style I fill:#6DB3F2,color:#222
    click I href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#51-understanding-skills" "Understanding skills"
    style R fill:#6DB3F2,color:#222
    click R href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#51-understanding-skills" "Understanding skills"
    style U fill:#6DB3F2,color:#222
    click U href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#51-understanding-skills" "Understanding skills"
```

<details>
<summary>ASCII версія</summary>

```
Багаторазові інструкції / workflow:
  .claude/skills/name/SKILL.md -> /name або виклик Claude залежно від конфігурації
  .claude/commands/name.md    -> сумісний формат /name
  Обидва можуть діяти на рівні користувача або проєкту.

Делегована робота:
  .claude/agents/name.md -> інструмент Agent -> власний контекст, prompt і дозволені інструменти
  Підсумок повертається до батьківського; ефекти на файли й сервіси можуть бути спільними.
```

</details>

> **Джерело**: [Розуміння скілів](../ultimate-guide.uk.md#51-розуміння-skills)
>
> **Офіційний довідник**: [Skills and command compatibility](https://code.claude.com/docs/en/skills) та [subagent definitions](https://code.claude.com/docs/en/sub-agents).

---

### Життєвий цикл agent та ізоляція області видимості

Окреме вікно контексту не пускає проміжну активність інструментів у батьківську розмову, але не ізолює ефекти на файли чи сервіси. Звичайні subagent починають з чистого аркуша; fork успадковують розмову. Worktree може відокремити зміни в репозиторії.

```mermaid
sequenceDiagram
    participant P as Батьківський Claude
    participant A as Інструмент Agent
    participant S as Subagent
    participant FS as Файли та сервіси
    P->>A: Делегує завдання
    alt Звичайний subagent
        A->>S: Prompt завдання та конфігурація agent
        Note over S: Чистий контекст розмови
    else Fork
        A->>S: Копія батьківської розмови та конфігурації
    end
    S->>FS: Дозволені читання, редагування або зовнішні виклики
    Note over S,FS: Ефекти можуть бути спільними<br/>Необов'язковий worktree відокремлює зміни в репозиторії
    FS->>S: Результати
    S->>A: Фінальний підсумок
    A->>P: Підсумок потрапляє до батьківського контексту
```

<details>
<summary>ASCII версія</summary>

```
Батьківський -> інструмент Agent -> Subagent
  Звичайний: prompt завдання + визначення; чистий контекст розмови
  Fork:      успадковує батьківську розмову та конфігурацію
  Tools:     дозволені операції з файлами/сервісами; ефекти можуть бути спільними
  Необов'язковий worktree: окремий checkout репозиторію, зовнішні сервіси не ізольовані
Subagent -> фінальний підсумок -> батьківський контекст
```

</details>

> **Джерело**: [Архітектура під-агентів](../core/architecture.uk.md#4-архітектура-під-агентів)
>
> **Офіційний довідник**: [Forks and ordinary subagents](https://code.claude.com/docs/en/sub-agents#how-forks-differ-from-other-subagents).

---

### Конвеєр подій hooks

Цей спрощений життєвий цикл розрізняє події сесії, події ходу та події інструментів. PermissionRequest є умовною подією. Типи hook і керування рішеннями залежать від події; це не вичерпний перелік подій.

```mermaid
flowchart TD
    INIT([Сесія починається]) --> START[SessionStart]
    START --> A[Prompt надіслано]
    A --> UPS[UserPromptSubmit]
    UPS -->|Exit 2 або блокування| REJECT[Prompt заблоковано<br/>Причину показано користувачу]
    UPS -->|Продовжити| MODEL[Модель обробляє контекст]
    MODEL --> TOOL{Виклик інструмента?}
    TOOL -->|Так| B[PreToolUse]
    TOOL -->|Ні, відповідь завершено| STOP[Stop]
    B -->|Блокування| BLOCK[Інструмент заблоковано]
    B -->|Продовжити| NEED{Потрібен запит дозволу?}
    NEED -->|Ні, дозволено| C[Інструмент виконується]
    NEED -->|Так| PR[PermissionRequest]
    PR -->|Дозволено| C
    PR -->|Відхилено| BLOCK
    C --> RESULT{Інструмент виконано успішно?}
    RESULT -->|Так| E[PostToolUse]
    RESULT -->|Ні| FAIL[PostToolUseFailure]
    E --> MODEL
    FAIL --> MODEL
    BLOCK --> MODEL
    STOP --> WAIT[Очікування наступного ходу або завершення сесії]
    WAIT -->|Наступний prompt| A
    WAIT -->|Сесія завершується| END[SessionEnd]
    INST[InstructionsLoaded<br/>Асинхронно, коли завантажуються файли інструкцій] -.-> A
    SS[SubagentStop<br/>Коли subagent завершує роботу] -.-> WAIT
    PRE[PreCompact] --> COMPACT[Стиснення] --> POST[PostCompact]
    style INIT fill:#6DB3F2,color:#222
    click INIT href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#71-the-event-system" "The event system"
    style START fill:#6DB3F2,color:#222
    click START href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#71-the-event-system" "The event system"
    style A fill:#6DB3F2,color:#222
    click A href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#71-the-event-system" "The event system"
    style UPS fill:#6DB3F2,color:#222
    click UPS href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#71-the-event-system" "The event system"
    style REJECT fill:#6DB3F2,color:#222
    click REJECT href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#71-the-event-system" "The event system"
    style B fill:#6DB3F2,color:#222
    click B href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#71-the-event-system" "The event system"
    style BLOCK fill:#6DB3F2,color:#222
    click BLOCK href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#71-the-event-system" "The event system"
    style NEED fill:#6DB3F2,color:#222
    click NEED href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#71-the-event-system" "The event system"
    style C fill:#6DB3F2,color:#222
    click C href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#71-the-event-system" "The event system"
    style PR fill:#6DB3F2,color:#222
    click PR href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#71-the-event-system" "The event system"
    style RESULT fill:#6DB3F2,color:#222
    click RESULT href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#71-the-event-system" "The event system"
    style E fill:#6DB3F2,color:#222
    click E href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#71-the-event-system" "The event system"
    style FAIL fill:#6DB3F2,color:#222
    click FAIL href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#71-the-event-system" "The event system"
    style MODEL fill:#6DB3F2,color:#222
    click MODEL href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#71-the-event-system" "The event system"
    style TOOL fill:#6DB3F2,color:#222
    click TOOL href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#71-the-event-system" "The event system"
    style STOP fill:#6DB3F2,color:#222
    click STOP href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#71-the-event-system" "The event system"
    style WAIT fill:#6DB3F2,color:#222
    click WAIT href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#71-the-event-system" "The event system"
    style END fill:#6DB3F2,color:#222
    click END href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#71-the-event-system" "The event system"
    style INST fill:#6DB3F2,color:#222
    click INST href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#71-the-event-system" "The event system"
    style SS fill:#6DB3F2,color:#222
    click SS href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#71-the-event-system" "The event system"
    style PRE fill:#6DB3F2,color:#222
    click PRE href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#71-the-event-system" "The event system"
    style COMPACT fill:#6DB3F2,color:#222
    click COMPACT href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#71-the-event-system" "The event system"
    style POST fill:#6DB3F2,color:#222
    click POST href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#71-the-event-system" "The event system"
```

<details>
<summary>ASCII версія</summary>

```
SessionStart -> prompt -> UserPromptSubmit
  заблоковано (exit 2 / рішення): причину показано користувачу; prompt не обробляється
  продовжити -> модель обробляє контекст -> виклик інструмента?
    ні, відповідь завершено -> Stop -> наступний хід або SessionEnd
    так -> PreToolUse -> перевірка дозволів
              заблоковано -> інструмент заблоковано -> модель
              потрібен запит -> PermissionRequest -> allow / deny
              уже дозволено -> виконання
  успіх інструмента -> PostToolUse -> модель
  збій інструмента -> PostToolUseFailure -> модель

Окремі події: InstructionsLoaded (асинхронна), SubagentStop
Стиснення: PreCompact -> стиснення -> PostCompact
Типи hook: command, http, mcp_tool, prompt, agent; підтримка залежить від події.
```

</details>

> **Джерело**: [Система подій](../ultimate-guide.uk.md#71-система-подій)
>
> **Офіційний довідник**: [Hook lifecycle and decisions](https://code.claude.com/docs/en/hooks#hook-lifecycle).
>
> InstructionsLoaded також спрацьовує під час відкладеного (lazy) завантаження інструкцій. Stop спрацьовує на кожну відповідь, SessionEnd на кожну сесію; для помилок API є StopFailure. Деякі спеціальні інструменти пропускають звичайні hooks інструментів. Офіційний довідник перелічує ці винятки та підтримувані типи hook для кожної події.

---
**Локалізація**: [Serhii (MacPlus Software)](https://macplus-software.com)
*Остання синхронізація: Травень 2026*
