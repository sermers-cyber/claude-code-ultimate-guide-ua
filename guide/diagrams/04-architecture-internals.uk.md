---
title: "Claude Code — Візуальні діаграми архітектури та нутрощів"
description: "Головний цикл (master loop), категорії інструментів, збірка системного промпту, ізоляція sub-agents"
tags: [architecture, internals, master-loop, tools]
---

# Архітектурні нутрощі

Що відбувається "під капотом" під час роботи Claude Code.

---

### Головний цикл (The Master Loop)

Основне виконання Claude Code складається з двох вкладених циклів: **внутрішнього циклу агента (inner agent loop)**, який продовжує викликати API, доки повертаються виклики інструментів, та **зовнішнього циклу розмови (outer conversation loop)**, який починає новий раунд, коли користувач дає відповідь.

```mermaid
flowchart TD
    A([Введення користувача]) --> B(Побудова System Prompt<br/>+ контекст + інструменти)
    B --> C

    subgraph AGENT_LOOP["Agent Loop — повторюється, доки є виклики інструментів"]
        C{{Виклик Claude API}} --> D{Відповідь<br/>містить виклики інструментів?}
        D -->|Yes| E(Паралельне виконання інструментів<br/>Glob, Grep, Bash...)
        E --> F(Додавання результатів інструментів<br/>до розмови)
        F --> C
    end

    D -->|No| H(Вилучення текстової відповіді)
    H --> I([Відображення користувачу])
    I --> J{Користувач надсилає<br/>наступне повідомлення?}
    J -->|Yes| B
    J -->|No| K([Сесія завершується])

    style A fill:#F5E6D3,color:#333
    style C fill:#E87E2F,color:#fff
    style D fill:#E87E2F,color:#fff
    style E fill:#6DB3F2,color:#fff
    style F fill:#6DB3F2,color:#fff
    style I fill:#7BC47F,color:#333
    style J fill:#E87E2F,color:#fff
    style K fill:#B8B8B8,color:#333

    click A href "https://github.com/gerasimsergey/claude-code-ultimate-guide-ua/blob/main/guide/ultimate-guide.md#12-first-workflow" "Введення користувача"
    click B href "https://github.com/gerasimsergey/claude-code-ultimate-guide-ua/blob/main/guide/core/architecture.md#1-the-master-loop" "Побудова System Prompt"
    click C href "https://github.com/gerasimsergey/claude-code-ultimate-guide-ua/blob/main/guide/core/architecture.md#1-the-master-loop" "Виклик Claude API"
    click D href "https://github.com/gerasimsergey/claude-code-ultimate-guide-ua/blob/main/guide/core/architecture.md#1-the-master-loop" "Відповідь містить виклики інструментів?"
    click E href "https://github.com/gerasimsergey/claude-code-ultimate-guide-ua/blob/main/guide/core/architecture.md#2-the-tool-arsenal" "Паралельне виконання інструментів"
    click F href "https://github.com/gerasimsergey/claude-code-ultimate-guide-ua/blob/main/guide/core/architecture.md#1-the-master-loop" "Додавання результатів інструментів"
    click H href "https://github.com/gerasimsergey/claude-code-ultimate-guide-ua/blob/main/guide/core/architecture.md#1-the-master-loop" "Вилучення текстової відповіді"
    click I href "https://github.com/gerasimsergey/claude-code-ultimate-guide-ua/blob/main/guide/ultimate-guide.md#12-first-workflow" "Відображення користувачу"
    click J href "https://github.com/gerasimsergey/claude-code-ultimate-guide-ua/blob/main/guide/core/architecture.md#1-the-master-loop" "Користувач надсилає наступне повідомлення?"
    click K href "https://github.com/gerasimsergey/claude-code-ultimate-guide-ua/blob/main/guide/core/architecture.md#1-the-master-loop" "Сесія завершується"
```

<details>
<summary>ASCII версія</summary>

```
Введення користувача
     │
Побудова промпту (system + context + tools)
     │
 ┌── Agent Loop ──────────────────────┐
 │ Claude API ◄────────────────────┐  │
 │      │                          │  │
 │ Виклики інструментів?           │  │
 │  ├─ Yes → Виконати інструменти ─┘  │
 │  └─ No  → вихід з циклу            │
 └────────────────────────────────────┘
               │
       Відображення відповіді
               │
       Користувач надсилає далі? ──► Yes → перебудувати промпт → цикл
               └─ No → Сесія завершується
```

</details>

> **Джерело**: [Архітектура: Головний цикл](../core/architecture.uk.md#master-loop) — Рядок ~72
>
> *Підтверджено джерелом (2026-03-31): Внутрішній цикл є асинхронним генератором `queryLoop()`. Інструменти виконуються через `StreamingToolExecutor` (до 10 паралельно). Цикл завершується з однієї з 10 кінцевих причин (`completed`, `max_turns`, `aborted_tools` тощо).*

---

### Категорії інструментів та вибір

Claude Code має 6 категорій інструментів, кожна з яких оптимізована для різних операцій. Розуміння того, який інструмент вибирає Claude (і чому), допомагає писати інструкції, що спрямовують до кращого вибору інструментів.

```mermaid
flowchart TD
    ROOT["Інструменти Claude Code"] --> READ
    ROOT --> WRITE
    ROOT --> EXECUTE
    ROOT --> WEB
    ROOT --> WORKFLOW
    ROOT --> CONTROL

    subgraph READ["📖 Інструменти читання (Read Tools)"]
        R1[Glob<br/>Пошук файлів за патерном]
        R2[Grep<br/>Пошук у вмісті файлів]
        R3[Read<br/>Читання вмісту файлу]
        R4[LS<br/>Список директорії]
    end

    subgraph WRITE["✏️ Інструменти запису (Write Tools)"]
        W1[Write<br/>Створення нового файлу]
        W2[Edit<br/>Зміна існуючого файлу]
        W3[MultiEdit<br/>Групові зміни]
    end

    subgraph EXECUTE["⚙️ Інструменти виконання (Execute Tools)"]
        E1[Bash<br/>Команди оболонки]
        E2[Task<br/>Запуск sub-agent]
    end

    subgraph WEB["🌐 Веб-інструменти (Web Tools)"]
        WB1[WebSearch<br/>Пошук в Інтернеті]
        WB2[WebFetch<br/>Отримання вмісту URL]
    end

    subgraph WORKFLOW["📋 Інструменти робочого процесу (Workflow Tools)"]
        WF1[TodoWrite<br/>Керування списком завдань]
        WF2[NotebookEdit<br/>Jupyter notebooks]
    end

    subgraph CONTROL["🎛️ Інструменти керування потоком (Control Flow Tools)"]
        CF1[EnterPlanMode / ExitPlanMode<br/>Перемикання режиму планування]
        CF2[EnterWorktree / ExitWorktree<br/>Навігація у worktree]
        CF3[AskUserQuestion<br/>Запит введення від користувача]
    end

    style ROOT fill:#E87E2F,color:#fff
    style R1 fill:#6DB3F2,color:#fff
    style R2 fill:#6DB3F2,color:#fff
    style R3 fill:#6DB3F2,color:#fff
    style R4 fill:#6DB3F2,color:#fff
    style W1 fill:#F5E6D3,color:#333
    style W2 fill:#F5E6D3,color:#333
    style W3 fill:#F5E6D3,color:#333
    style E1 fill:#E85D5D,color:#fff
    style E2 fill:#E87E2F,color:#fff
    style WB1 fill:#7BC47F,color:#333
    style WB2 fill:#7BC47F,color:#333
    style WF1 fill:#B8B8B8,color:#333
    style WF2 fill:#B8B8B8,color:#333
    style CF1 fill:#B8B8B8,color:#333
    style CF2 fill:#B8B8B8,color:#333
    style CF3 fill:#B8B8B8,color:#333

    click ROOT href "https://github.com/gerasimsergey/claude-code-ultimate-guide-ua/blob/main/guide/core/architecture.md#2-the-tool-arsenal" "Інструменти Claude Code"
    click R1 href "https://github.com/gerasimsergey/claude-code-ultimate-guide-ua/blob/main/guide/core/architecture.md#2-the-tool-arsenal" "Glob — Пошук файлів за патерном"
    click R2 href "https://github.com/gerasimsergey/claude-code-ultimate-guide-ua/blob/main/guide/core/architecture.md#2-the-tool-arsenal" "Grep — Пошук у вмісті файлів"
    click R3 href "https://github.com/gerasimsergey/claude-code-ultimate-guide-ua/blob/main/guide/core/architecture.md#2-the-tool-arsenal" "Read — Читання вмісту файлу"
    click R4 href "https://github.com/gerasimsergey/claude-code-ultimate-guide-ua/blob/main/guide/core/architecture.md#2-the-tool-arsenal" "LS — Список директорії"
    click W1 href "https://github.com/gerasimsergey/claude-code-ultimate-guide-ua/blob/main/guide/core/architecture.md#2-the-tool-arsenal" "Write — Створення нового файлу"
    click W2 href "https://github.com/gerasimsergey/claude-code-ultimate-guide-ua/blob/main/guide/core/architecture.md#2-the-tool-arsenal" "Edit — Зміна існуючого файлу"
    click W3 href "https://github.com/gerasimsergey/claude-code-ultimate-guide-ua/blob/main/guide/core/architecture.md#2-the-tool-arsenal" "MultiEdit — Групові зміни"
    click E1 href "https://github.com/gerasimsergey/claude-code-ultimate-guide-ua/blob/main/guide/core/architecture.md#2-the-tool-arsenal" "Bash — Команди оболонки"
    click E2 href "https://github.com/gerasimsergey/claude-code-ultimate-guide-ua/blob/main/guide/ultimate-guide.md#41-what-are-agents" "Task — Запуск sub-agent"
    click WB1 href "https://github.com/gerasimsergey/claude-code-ultimate-guide-ua/blob/main/guide/core/architecture.md#2-the-tool-arsenal" "WebSearch"
    click WB2 href "https://github.com/gerasimsergey/claude-code-ultimate-guide-ua/blob/main/guide/core/architecture.md#2-the-tool-arsenal" "WebFetch"
    click WF1 href "https://github.com/gerasimsergey/claude-code-ultimate-guide-ua/blob/main/guide/core/architecture.md#2-the-tool-arsenal" "TodoWrite — Список завдань"
    click WF2 href "https://github.com/gerasimsergey/claude-code-ultimate-guide-ua/blob/main/guide/core/architecture.md#2-the-tool-arsenal" "NotebookEdit — Jupyter"
    click CONTROL href "https://github.com/gerasimsergey/claude-code-ultimate-guide-ua/blob/main/guide/core/architecture.md#2-the-tool-arsenal" "Інструменти керування потоком"
    click CF1 href "https://github.com/gerasimsergey/claude-code-ultimate-guide-ua/blob/main/guide/core/architecture.md#2-the-tool-arsenal" "EnterPlanMode / ExitPlanMode"
    click CF2 href "https://github.com/gerasimsergey/claude-code-ultimate-guide-ua/blob/main/guide/core/architecture.md#2-the-tool-arsenal" "EnterWorktree / ExitWorktree"
    click CF3 href "https://github.com/gerasimsergey/claude-code-ultimate-guide-ua/blob/main/guide/core/architecture.md#2-the-tool-arsenal" "AskUserQuestion"
```

<details>
<summary>ASCII версія</summary>

```
READ:     Glob (пошук), Grep (пошук у вмісті), Read (вміст), LS (список)
WRITE:    Write (створити), Edit (змінити), MultiEdit (групове)
EXECUTE:  Bash (оболонка), Task (sub-agent)  ← найпотужніші/найризикованіші
WEB:      WebSearch, WebFetch
WORKFLOW: TodoWrite, NotebookEdit
CONTROL:  EnterPlanMode/ExitPlanMode, EnterWorktree/ExitWorktree, AskUserQuestion
```

</details>

> **Джерело**: [Архітектура: Інструменти](../core/architecture.uk.md#tools) — Рядок ~213
>
> *Спрощено — доступні додаткові інструменти. Див. [Архітектура: Арсенал інструментів](../core/architecture.uk.md#tools) для повного списку.*

---

### Збірка системного промпту

Перед кожним викликом API Claude Code збирає системний промпт з кількох джерел у певному порядку. Промпт розділений на дві зони кешування маркером межі.

```mermaid
sequenceDiagram
    participant CC as Claude Code
    participant G as Global CLAUDE.md
    participant P as Project CLAUDE.md
    participant T as Реєстр інструментів (Tool Registry)
    participant A as Claude API

    Note over CC: СТАТИЧНА зона (кешується глобально — спільна для всіх користувачів)
    CC->>CC: 1. Завантаження базових інструкцій + правил безпеки
    CC->>G: 2. Читання ~/.claude/CLAUDE.md
    G->>CC: Глобальні уподобання, правила
    CC->>P: 3. Читання проектного(их) CLAUDE.md
    P->>CC: Конвенції проекту, контекст
    CC->>T: 4. Отримання списку доступних інструментів
    T->>CC: Схеми інструментів (Glob, Grep, Bash...)
    Note over CC: ── МАРКЕР МЕЖІ (BOUNDARY MARKER) ──────────
    Note over CC: ДИНАМІЧНА зона (кешується для кожної сесії окремо)
    CC->>CC: 5. Додавання робочої директорії + git-інформації
    CC->>CC: 6. Додавання можливостей MCP-серверів (не кешується — обчислюється щоразу)
    CC->>CC: 7. Додавання пам'яті (MEMORY.md), керівництва з сесій, мови
    CC->>A: System prompt (зібраний)<br/>+ повідомлення користувача
    Note over A: Один великий виклик із<br/>впровадженим усім контекстом
```

<details>
<summary>ASCII версія</summary>

```
СТАТИЧНА зона (кешується глобально):
1. Базові інструкції (жорстко закодовані)
2. ~/.claude/CLAUDE.md
3. /project/CLAUDE.md + піддиректорії
4. Список визначень інструментів
────── МАРКЕР МЕЖІ (BOUNDARY MARKER) ──────────
ДИНАМІЧНА зона (кеш на сесію):
5. Робоча директорія + git status
6. Можливості MCP-серверів (завжди обчислюються наново)
7. Пам'ять, керівництво з сесій, мова
──────────────────────────────────────────────
→ Усе об'єднано → Виклик Claude API
```

</details>

> **Джерело**: [Архітектура: Системний промпт](../core/architecture.uk.md#system-prompt) — Рядок ~354
>
> *Підтверджено джерелом (2026-03-31): Двозонна архітектура за допомогою маркера `SYSTEM_PROMPT_DYNAMIC_BOUNDARY`. Статична зона має `cacheScope: 'global'` (спільна для всіх користувачів). Інструкції MCP явно не кешуються — коментар у коді: "servers connect/disconnect between turns".*

---

### Ізоляція контексту sub-agents

Sub-agents повністю ізольовані від батьківського агента — вони не можуть читати розмову батьківського агента чи змінювати його стан. Ця ізоляція є водночас захистом (безпека) та обмеженням (навмисний дизайн).

```mermaid
sequenceDiagram
    participant P as Батьківський Claude
    participant T as Інструмент Task
    participant S as Sub-Agent
    participant EXT as Зовнішні сервіси (External Services)

    Note over P: Має повну історію розмов
    P->>T: Task(prompt="do X", tools=[Read,Write,Bash])
    Note over T: Створює новий інстанс Claude
    T->>S: spawn(лише промпт + права на інструменти)
    Note over S: НЕ отримує:<br/>- Батьківську розмову<br/>- Результати батьківських інструментів<br/>- Батьківський стан

    S->>EXT: читання файлів, bash, web (якщо дозволено)
    EXT->>S: Результати

    Note over S: Незалежне міркування<br/>з обмеженим контекстом

    S->>T: return "task complete: details..."
    Note over T: Назад передається тільки текст
    T->>P: Рядок результату (Result string)
    Note over P: Батьківський агент отримує тільки текст<br/>Спільного стану немає
```

<details>
<summary>ASCII версія</summary>

```
Батьківський (повний контекст)
    │
    Task(prompt, tools=[...])
    │
    ▼
Sub-Agent (ІЗОЛЬОВАНИЙ)
  Введення: тільки промпт + дозволи на інструменти
  Може: використовувати надані інструменти незалежно
  Не може: бачити батьківську розмову, змінювати батьківський стан
  Вихід: ТІЛЬКИ текстовий результат
    │
    ▼
Батьківський отримує: текстовий рядок
```

</details>

> **Джерело**: [Архітектура: Sub-Agents](../core/architecture.uk.md#sub-agents) — Рядок ~444

---
**Локалізація**: [Serhii (MacPlus Software)](https://macplus-software.com)
*Остання синхронізація: Травень 2026*
