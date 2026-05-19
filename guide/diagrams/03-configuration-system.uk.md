---
title: "Claude Code — Візуальні діаграми системи конфігурації"
description: "Пріоритет конфігурації, порівняння навичок, команд та агентів, життєвий цикл агента, конвеєр hooks"
tags: [configuration, hooks, agents, skills, commands]
---

# Система конфігурації

Як Claude Code завантажує налаштування, вирішує конфлікти та організовує розширюваність.

---

### Пріоритет конфігурації (5 рівнів)

Claude Code визначає налаштування за суворою ієрархією пріоритетів. Вищі рівні перевизначають нижчі. Розуміння цього запобігає виникненню багів на кшталт "чому моя конфігурація не працює?".

```mermaid
flowchart TD
    A["1️⃣ CLI Flags<br/>--model, --dangerously-skip-permissions<br/>--max-turns, --system-prompt"] --> B["2️⃣ Environment Variables<br/>ANTHROPIC_API_KEY<br/>CLAUDE_MODEL, CLAUDE_CONFIG"]
    B --> C["3️⃣ Project Config<br/>.claude/settings.json<br/>.claude/settings.local.json"]
    C --> D["4️⃣ Global Config<br/>~/.claude/settings.json<br/>~/.claude/CLAUDE.md"]
    D --> E["5️⃣ Built-in Defaults<br/>Hardcoded in Claude Code binary"]

    A1["Найвищий пріоритет<br/>Перевизначає все<br/>Використання: автоматизація, CI/CD"] --> A
    E1["Найнижчий пріоритет<br/>Резервні значення<br/>Використання: базова поведінка"] --> E

    style A fill:#E87E2F,color:#fff
    style B fill:#6DB3F2,color:#fff
    style C fill:#6DB3F2,color:#fff
    style D fill:#F5E6D3,color:#333
    style E fill:#B8B8B8,color:#333
    style A1 fill:#B8B8B8,color:#333
    style E1 fill:#B8B8B8,color:#333

    click A href "https://github.com/gerasimsergey/claude-code-ultimate-guide-ua/blob/main/guide/ultimate-guide.md#34-precedence-rules" "CLI Flags — найвищий пріоритет"
    click B href "https://github.com/gerasimsergey/claude-code-ultimate-guide-ua/blob/main/guide/ultimate-guide.md#33-settings--permissions" "Змінні середовища (Environment Variables)"
    click C href "https://github.com/gerasimsergey/claude-code-ultimate-guide-ua/blob/main/guide/ultimate-guide.md#33-settings--permissions" "Конфігурація проекту (Project Config)"
    click D href "https://github.com/gerasimsergey/claude-code-ultimate-guide-ua/blob/main/guide/ultimate-guide.md#31-memory-files-claudemd" "Глобальна конфігурація (Global Config)"
    click E href "https://github.com/gerasimsergey/claude-code-ultimate-guide-ua/blob/main/guide/ultimate-guide.md#34-precedence-rules" "Вбудовані значення за замовчуванням (Built-in Defaults)"
    click A1 href "https://github.com/gerasimsergey/claude-code-ultimate-guide-ua/blob/main/guide/ultimate-guide.md#34-precedence-rules" "Найвищий пріоритет"
    click E1 href "https://github.com/gerasimsergey/claude-code-ultimate-guide-ua/blob/main/guide/ultimate-guide.md#34-precedence-rules" "Найнижчий пріоритет"
```

<details>
<summary>ASCII версія</summary>

```
ПРІОРИТЕТ (від найвищого до найнижчого)
══════════════════════════════════════
1. CLI Flags            ← --model, --system-prompt
2. Environment Vars     ← ANTHROPIC_API_KEY
3. Project .claude/     ← settings.json, settings.local.json
4. Global ~/.claude/    ← settings.json, CLAUDE.md
5. Вбудовані defaults   ← жорстко закодовані значення
```

</details>

> **Джерело**: [Система конфігурації](../ultimate-guide.uk.md#configuration) — Рядок ~3760

---

### Skills проти Commands проти Agents — Коли що використовувати

Три механізми розширення з різними цілями та компромісами. Вибір неправильної абстракції призводить до надмірної складності (over-engineering) або недостатньо потужної автоматизації.

```mermaid
flowchart LR
    subgraph SKILLS["📦 Skills (.claude/skills/)"]
        S1[Зібрана можливість<br/>з ресурсами]
        S2[Викликається через /skillname]
        S3[Переносний між проектами]
        S4["Використовувати для: багаторазових<br/>міжпроектних можливостей"]
    end

    subgraph COMMANDS["⚡ Commands (.claude/commands/)"]
        C1[Простий шаблон<br/>або скрипт]
        C2[Slash-команда проекту]
        C3[Тільки для конкретного проекту]
        C4["Використовувати для: автоматизації<br/>проекту, ярликів"]
    end

    subgraph AGENTS["🤖 Agents (.claude/agents/)"]
        A1[Повністю автономний агент]
        A2[Власний набір інструментів та CLAUDE.md]
        A3[Запускається через інструмент Task]
        A4["Використовувати для: складних<br/>делегованих завдань"]
    end

    Q{Що ви<br/>створюєте?} --> |Багаторазова функція| SKILLS
    Q --> |Ярлик проекту| COMMANDS
    Q --> |Складне підзавдання| AGENTS

    style S1 fill:#6DB3F2,color:#fff
    style S4 fill:#7BC47F,color:#333
    style C1 fill:#F5E6D3,color:#333
    style C4 fill:#7BC47F,color:#333
    style A1 fill:#E87E2F,color:#fff
    style A4 fill:#7BC47F,color:#333
    style Q fill:#E87E2F,color:#fff

    click S1 href "https://github.com/gerasimsergey/claude-code-ultimate-guide-ua/blob/main/guide/ultimate-guide.md#51-understanding-skills" "Skills: Зібрана можливість"
    click S2 href "https://github.com/gerasimsergey/claude-code-ultimate-guide-ua/blob/main/guide/ultimate-guide.md#51-understanding-skills" "Skills: Викликається через /skillname"
    click S3 href "https://github.com/gerasimsergey/claude-code-ultimate-guide-ua/blob/main/guide/ultimate-guide.md#51-understanding-skills" "Skills: Переносний між проектами"
    click S4 href "https://github.com/gerasimsergey/claude-code-ultimate-guide-ua/blob/main/guide/ultimate-guide.md#51-understanding-skills" "Skills: Багаторазові можливості"
    click C1 href "https://github.com/gerasimsergey/claude-code-ultimate-guide-ua/blob/main/guide/ultimate-guide.md#62-creating-custom-commands" "Commands: Простий шаблон"
    click C2 href "https://github.com/gerasimsergey/claude-code-ultimate-guide-ua/blob/main/guide/ultimate-guide.md#62-creating-custom-commands" "Commands: Slash-команда проекту"
    click C3 href "https://github.com/gerasimsergey/claude-code-ultimate-guide-ua/blob/main/guide/ultimate-guide.md#62-creating-custom-commands" "Commands: Тільки для конкретного проекту"
    click C4 href "https://github.com/gerasimsergey/claude-code-ultimate-guide-ua/blob/main/guide/ultimate-guide.md#62-creating-custom-commands" "Commands: Автоматизація проекту"
    click A1 href "https://github.com/gerasimsergey/claude-code-ultimate-guide-ua/blob/main/guide/ultimate-guide.md#41-what-are-agents" "Agents: Повністю автономний"
    click A2 href "https://github.com/gerasimsergey/claude-code-ultimate-guide-ua/blob/main/guide/ultimate-guide.md#41-what-are-agents" "Agents: Власний набір інструментів"
    click A3 href "https://github.com/gerasimsergey/claude-code-ultimate-guide-ua/blob/main/guide/ultimate-guide.md#41-what-are-agents" "Agents: Запускається через інструмент Task"
    click A4 href "https://github.com/gerasimsergey/claude-code-ultimate-guide-ua/blob/main/guide/ultimate-guide.md#41-what-are-agents" "Agents: Складні делеговані завдання"
    click Q href "https://github.com/gerasimsergey/claude-code-ultimate-guide-ua/blob/main/guide/ultimate-guide.md#41-what-are-agents" "Що ви створюєте?"
```

<details>
<summary>ASCII версія</summary>

```
                    Skills              Commands           Agents
Місце:         .claude/skills/     .claude/commands/  .claude/agents/
Тригер:        /skillname          /commandname       Інструмент Task
Область дії:   Міжпроектна         Цей проект         Будь-який контекст
Складність:    Середня (зібрана)   Низька (шаблон)    Висока (автономна)
Коли:          Багаторазові ф-ції  Швидкі ярлики      Складні завдання
```

</details>

> **Джерело**: [Система розширюваності](../ultimate-guide.uk.md#extensibility) — Рядок ~4495, ~5025, ~3900

---

### Життєвий цикл агента та ізоляція областей дії

Sub-agents працюють у повній ізоляції від батьківського агента. Вони отримують копію контексту, але не ділять спільний стан. Розуміння цього запобігає плутанині на кшталт "чому мій sub-agent не бачить X?".

```mermaid
sequenceDiagram
    participant P as Батьківський Claude
    participant T as Інструмент Task
    participant S as Sub-Agent
    participant FS as Файлова система

    P->>T: Task(prompt, tools_allowed)
    T->>S: Створює новий інстанс Claude
    Note over S: Отримує: промпт + права на інструменти<br/>НЕ отримує: розмову батьківського агента

    S->>FS: Читає файли (якщо дозволено)
    S->>FS: Редагує файли (якщо дозволено)
    S->>S: Незалежне міркування

    Note over S,FS: Повністю ізольоване виконання
    Note over S: Немає доступу до батьківського стану

    S->>T: Повертає: тільки текстовий результат
    T->>P: Рядок результату (Result string)
    P->>P: Продовжує роботу з результатом

    Note over P,T: Батьківський агент бачить тільки фінальний текст<br/>Побічні ефекти не повертаються назад
```

<details>
<summary>ASCII версія</summary>

```
Батьківський ──Task(prompt, tools)──► Sub-Agent
                                          │
                                     [ізольоване виконання]
                                     - читання файлів
                                     - редагування файлів
                                     - bash (якщо дозволено)
                                          │
Батьківський ◄───── текстовий результат ──┘
(без спільного використання стану, без побічних ефектів)
```

</details>

> **Джерело**: [Sub-Agents](../ultimate-guide.uk.md#sub-agents) — Рядок ~3900

---

### Конвеєр подій Hooks

Hooks дозволяють виконувати власний код у ключових точках життєвого циклу Claude Code — для перевірки безпеки, логування, примусового виконання правил або сповіщень. Порядок виконання має значення.

```mermaid
flowchart TD
    INIT([Старт сесії]) -.->|v2.1.69+| INST{InstructionsLoaded Hook}
    INST -.-> A

    A([Користувач надсилає повідомлення]) --> UPS{UserPromptSubmit Hook}
    UPS -->|Exit 0: proceed| B{PreToolUse Hook}
    UPS -->|Exit 2: feedback| A
    B -->|Exit 0: allow| C[Інструмент виконується]
    B -->|Exit 1: block| D([Інструмент заблоковано<br/>Claude зупиняється])
    C --> E{PostToolUse Hook}
    E --> F[Наступний інструмент або відповідь]
    F --> G{Потрібні ще інструменти?}
    G -->|Yes| B
    G -->|No| H([Сесія завершується])
    H --> I{Stop / SessionEnd Hook}
    I --> J([Завершено])

    K{PreCompact Hook} -.->|Перед /compact| L[Виконується /compact]
    L --> M{PostCompact Hook}

    NOTE["Типи hooks:<br/>bash (exit 0/1/2)<br/>http (POST JSON → URL, v2.1.63+)"] -.-> B

    style INST fill:#6DB3F2,color:#fff
    style UPS fill:#6DB3F2,color:#fff
    style B fill:#E87E2F,color:#fff
    style D fill:#E85D5D,color:#fff
    style E fill:#E87E2F,color:#fff
    style I fill:#E87E2F,color:#fff
    style K fill:#6DB3F2,color:#fff
    style M fill:#6DB3F2,color:#fff
    style C fill:#7BC47F,color:#333
    style J fill:#7BC47F,color:#333
    style NOTE fill:#F5E6D3,color:#333

    click INIT href "https://github.com/gerasimsergey/claude-code-ultimate-guide-ua/blob/main/guide/ultimate-guide.md#71-the-event-system" "Старт сесії"
    click INST href "https://github.com/gerasimsergey/claude-code-ultimate-guide-ua/blob/main/guide/ultimate-guide.md#71-the-event-system" "InstructionsLoaded Hook — v2.1.69+"
    click A href "https://github.com/gerasimsergey/claude-code-ultimate-guide-ua/blob/main/guide/ultimate-guide.md#71-the-event-system" "Користувач надсилає повідомлення"
    click UPS href "https://github.com/gerasimsergey/claude-code-ultimate-guide-ua/blob/main/guide/ultimate-guide.md#71-the-event-system" "UserPromptSubmit Hook"
    click B href "https://github.com/gerasimsergey/claude-code-ultimate-guide-ua/blob/main/guide/ultimate-guide.md#71-the-event-system" "PreToolUse Hook"
    click C href "https://github.com/gerasimsergey/claude-code-ultimate-guide-ua/blob/main/guide/core/architecture.md#2-the-tool-arsenal" "Інструмент виконується"
    click D href "https://github.com/gerasimsergey/claude-code-ultimate-guide-ua/blob/main/guide/ultimate-guide.md#71-the-event-system" "Інструмент заблоковано"
    click E href "https://github.com/gerasimsergey/claude-code-ultimate-guide-ua/blob/main/guide/ultimate-guide.md#71-the-event-system" "PostToolUse Hook"
    click F href "https://github.com/gerasimsergey/claude-code-ultimate-guide-ua/blob/main/guide/ultimate-guide.md#71-the-event-system" "Наступний інструмент або відповідь"
    click G href "https://github.com/gerasimsergey/claude-code-ultimate-guide-ua/blob/main/guide/ultimate-guide.md#71-the-event-system" "Потрібні ще інструменти?"
    click H href "https://github.com/gerasimsergey/claude-code-ultimate-guide-ua/blob/main/guide/ultimate-guide.md#71-the-event-system" "Сесія завершується"
    click I href "https://github.com/gerasimsergey/claude-code-ultimate-guide-ua/blob/main/guide/ultimate-guide.md#71-the-event-system" "Stop / SessionEnd Hook"
    click J href "https://github.com/gerasimsergey/claude-code-ultimate-guide-ua/blob/main/guide/ultimate-guide.md#72-creating-hooks" "Завершено"
    click K href "https://github.com/gerasimsergey/claude-code-ultimate-guide-ua/blob/main/guide/ultimate-guide.md#71-the-event-system" "PreCompact Hook"
    click L href "https://github.com/gerasimsergey/claude-code-ultimate-guide-ua/blob/main/guide/ultimate-guide.md#71-the-event-system" "Виконується /compact"
    click M href "https://github.com/gerasimsergey/claude-code-ultimate-guide-ua/blob/main/guide/ultimate-guide.md#71-the-event-system" "PostCompact Hook"
```

<details>
<summary>ASCII версія</summary>

```
Старт сесії
     │ (InstructionsLoaded Hook — v2.1.69+)
Повідомлення користувача
     │
 UserPromptSubmit ──exit 2──► зворотний зв'язок для Claude (цикл)
     │ exit 0
 PreToolUse ──exit 1──► ЗАБЛОКОВАНО
     │ exit 0
     ▼
Інструмент виконується
     │
PostToolUse
     │
Потрібні ще інструменти? ──yes──► PreToolUse (цикл)
     │ no
Сесія завершується
     │
  Stop / SessionEnd Hook
     │
 Завершено

Окремо: PreCompact ──► /compact ──► PostCompact

Типи hooks: bash (exit 0/1/2) | http POST JSON (v2.1.63+)
```

</details>

> **Джерело**: [Система Hooks](../ultimate-guide.uk.md#hooks) — Рядок ~5350 | UserPromptSubmit + HTTP hooks: v2.1.63+ | InstructionsLoaded: v2.1.69+

---
**Локалізація**: [Serhii (MacPlus Software)](https://macplus-software.com)
*Остання синхронізація: Травень 2026*
