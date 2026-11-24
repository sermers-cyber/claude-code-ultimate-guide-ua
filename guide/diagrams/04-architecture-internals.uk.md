---
title: "Claude Code: Діаграми внутрішньої архітектури"
description: "Агентний цикл, ілюстративні сімейства інструментів, контекст запиту, межі subagent і конвеєри моделей"
tags: [architecture, internals, master-loop, tools]
---

# Внутрішня архітектура

Концептуальні діаграми циклу «модель - інструменти», сімейств інструментів і меж контексту.

---

### Головний цикл (The master loop)

Спрощений цикл «модель - інструменти»: Claude запитує інструменти, дозволені операції виконуються, а їхні результати повертаються в розмову. Ходи також можуть завершуватися через помилки, скасування або ліміти. Незалежні операції можуть виконуватися паралельно; фіксований ліміт паралельності не стверджується.

```mermaid
flowchart TD
    A([Введення користувача]) --> B[Підготовка контексту запиту<br/>Інструкції, історія, доступні інструменти]
    B --> C{{Запит до моделі}}
    C --> D{Виклики інструментів?}
    D -->|Так| PERM{Дозволено?}
    PERM -->|Так| E[Виконання дозволених інструментів]
    PERM -->|Ні| DENY[Повернення відмови в розмову]
    E --> F[Додавання результатів інструментів]
    DENY --> F
    F --> C
    D -->|Ні| I[Відображення відповіді]
    I --> J{Наступна дія користувача?}
    J -->|Нове повідомлення| B
    J -->|Вихід| K([Сесія завершується])
    E -.->|Помилка, скасування або ліміт| STOP[Обробка переривання або збою]
    style A fill:#6DB3F2,color:#222
    click A href "https://github.com/gerasimsergey/claude-code-ultimate-guide-ua/blob/main/guide/core/architecture.uk.md#1-основний-цикл-the-master-loop" "Головний цикл"
    style B fill:#6DB3F2,color:#222
    click B href "https://github.com/gerasimsergey/claude-code-ultimate-guide-ua/blob/main/guide/core/architecture.uk.md#1-основний-цикл-the-master-loop" "Головний цикл"
    style C fill:#6DB3F2,color:#222
    click C href "https://github.com/gerasimsergey/claude-code-ultimate-guide-ua/blob/main/guide/core/architecture.uk.md#1-основний-цикл-the-master-loop" "Головний цикл"
    style D fill:#6DB3F2,color:#222
    click D href "https://github.com/gerasimsergey/claude-code-ultimate-guide-ua/blob/main/guide/core/architecture.uk.md#1-основний-цикл-the-master-loop" "Головний цикл"
    style PERM fill:#6DB3F2,color:#222
    click PERM href "https://github.com/gerasimsergey/claude-code-ultimate-guide-ua/blob/main/guide/core/architecture.uk.md#1-основний-цикл-the-master-loop" "Головний цикл"
    style E fill:#6DB3F2,color:#222
    click E href "https://github.com/gerasimsergey/claude-code-ultimate-guide-ua/blob/main/guide/core/architecture.uk.md#1-основний-цикл-the-master-loop" "Головний цикл"
    style DENY fill:#6DB3F2,color:#222
    click DENY href "https://github.com/gerasimsergey/claude-code-ultimate-guide-ua/blob/main/guide/core/architecture.uk.md#1-основний-цикл-the-master-loop" "Головний цикл"
    style F fill:#6DB3F2,color:#222
    click F href "https://github.com/gerasimsergey/claude-code-ultimate-guide-ua/blob/main/guide/core/architecture.uk.md#1-основний-цикл-the-master-loop" "Головний цикл"
    style I fill:#6DB3F2,color:#222
    click I href "https://github.com/gerasimsergey/claude-code-ultimate-guide-ua/blob/main/guide/core/architecture.uk.md#1-основний-цикл-the-master-loop" "Головний цикл"
    style J fill:#6DB3F2,color:#222
    click J href "https://github.com/gerasimsergey/claude-code-ultimate-guide-ua/blob/main/guide/core/architecture.uk.md#1-основний-цикл-the-master-loop" "Головний цикл"
    style K fill:#6DB3F2,color:#222
    click K href "https://github.com/gerasimsergey/claude-code-ultimate-guide-ua/blob/main/guide/core/architecture.uk.md#1-основний-цикл-the-master-loop" "Головний цикл"
    style STOP fill:#6DB3F2,color:#222
    click STOP href "https://github.com/gerasimsergey/claude-code-ultimate-guide-ua/blob/main/guide/core/architecture.uk.md#1-основний-цикл-the-master-loop" "Головний цикл"
```

<details>
<summary>ASCII версія</summary>

```
Введення користувача -> контекст запиту -> модель
                    ^             |
                    |        виклики інструментів?
                    |          Так -> дозволи -> виконати або відмовити -> додати результат
                    +-------------------------------------------------------------+
                               Ні -> показати відповідь -> наступне повідомлення або вихід
Помилки, скасування та ліміти можуть перервати цикл.
Незалежні операції можуть виконуватися паралельно.
```

</details>

> **Джерело**: [Головний цикл](../core/architecture.uk.md#1-основний-цикл-the-master-loop)
>
> **Офіційний довідник**: [Задокументований агентний цикл](https://code.claude.com/docs/en/how-claude-code-works#the-agentic-loop).

---

### Категорії інструментів і вибір

Ці шість категорій, визначених автором, упорядковують приклади із задокументованого переліку інструментів. Доступність залежить від версії Claude Code, моделі, поверхні та конфігурації; це не повний перелік інструментів і не нативна таксономія з шести категорій.

```mermaid
flowchart TD
    ROOT[Ілюстративні сімейства інструментів] --> READ[Читання та пошук<br/>Glob, Grep, Read]
    ROOT --> WRITE[Зміна файлів<br/>Write, Edit, NotebookEdit]
    ROOT --> EXEC[Виконання та делегування<br/>Bash, Agent]
    ROOT --> WEB[Доступ до вебу<br/>WebSearch, WebFetch]
    ROOT --> TRACK[Відстеження завдань, коли доступно<br/>TaskCreate, TaskGet,<br/>TaskList, TaskUpdate]
    ROOT --> CONTROL[Керування робочим процесом<br/>EnterPlanMode, ExitPlanMode,<br/>EnterWorktree, ExitWorktree,<br/>AskUserQuestion]
    style ROOT fill:#6DB3F2,color:#222
    click ROOT href "https://github.com/gerasimsergey/claude-code-ultimate-guide-ua/blob/main/guide/core/architecture.uk.md#2-арсенал-інструментів" "Арсенал інструментів"
    style READ fill:#6DB3F2,color:#222
    click READ href "https://github.com/gerasimsergey/claude-code-ultimate-guide-ua/blob/main/guide/core/architecture.uk.md#2-арсенал-інструментів" "Арсенал інструментів"
    style WRITE fill:#6DB3F2,color:#222
    click WRITE href "https://github.com/gerasimsergey/claude-code-ultimate-guide-ua/blob/main/guide/core/architecture.uk.md#2-арсенал-інструментів" "Арсенал інструментів"
    style EXEC fill:#6DB3F2,color:#222
    click EXEC href "https://github.com/gerasimsergey/claude-code-ultimate-guide-ua/blob/main/guide/core/architecture.uk.md#2-арсенал-інструментів" "Арсенал інструментів"
    style WEB fill:#6DB3F2,color:#222
    click WEB href "https://github.com/gerasimsergey/claude-code-ultimate-guide-ua/blob/main/guide/core/architecture.uk.md#2-арсенал-інструментів" "Арсенал інструментів"
    style TRACK fill:#6DB3F2,color:#222
    click TRACK href "https://github.com/gerasimsergey/claude-code-ultimate-guide-ua/blob/main/guide/core/architecture.uk.md#2-арсенал-інструментів" "Арсенал інструментів"
    style CONTROL fill:#6DB3F2,color:#222
    click CONTROL href "https://github.com/gerasimsergey/claude-code-ultimate-guide-ua/blob/main/guide/core/architecture.uk.md#2-арсенал-інструментів" "Арсенал інструментів"
```

<details>
<summary>ASCII версія</summary>

```
READ / SEARCH : Glob, Grep, Read
MODIFY        : Write, Edit, NotebookEdit
EXECUTE       : Bash, Agent
WEB           : WebSearch, WebFetch
TASK TRACKING : TaskCreate, TaskGet, TaskList, TaskUpdate, коли доступно
CONTROL       : EnterPlanMode / ExitPlanMode, EnterWorktree / ExitWorktree,
                AskUserQuestion

Ілюстративні сімейства, а не повний чи універсально доступний перелік.
Переглядайте директорії через команду оболонки; звіряйтеся з актуальним довідником інструментів.
```

</details>

> **Джерело**: [Арсенал інструментів](../core/architecture.uk.md#2-арсенал-інструментів)
>
> **Офіційний довідник**: [Актуальні інструменти та їх доступність](https://code.claude.com/docs/en/tools-reference).
>
> TodoWrite є альтернативним інструментом чекліста в підтримуваних конфігураціях, а не універсально активним типовим варіантом. Agent є актуальною назвою інструмента subagent; Task залишається псевдонімом у налаштуваннях і визначеннях.

---

### Збірка системного промпту

Ця концептуальна діаграма запиту групує стабільні інструкції разом зі змінним контекстом розмови. Вона не визначає точного внутрішнього порядку збірки, меж кешу чи моменту повторного читання кожного входу. Файли інструкцій і пам'ять можуть потрапляти в контекст розмови; визначення MCP можуть завантажуватися на вимогу.

```mermaid
flowchart TD
    S[Системні інструкції] --> REQ[Запит до моделі]
    T[Визначення доступних інструментів<br/>Визначення MCP завантажуються за потреби] --> REQ
    U[Інструкції користувача та проєкту<br/>Релевантні правила й auto memory] --> CTX[Контекст розмови]
    W[Релевантний контекст середовища та файлів] --> CTX
    H[Повідомлення користувача та результати інструментів] --> CTX
    CTX --> REQ
    REQ --> API[Claude API або налаштований провайдер]
    NOTE[Повторне використання кешу залежить від стабільних префіксів<br/>і контракту провайдера] -.-> API
    style S fill:#6DB3F2,color:#222
    click S href "https://github.com/gerasimsergey/claude-code-ultimate-guide-ua/blob/main/guide/core/architecture.uk.md#вміст-системного-промпту" "Вміст системного промпту"
    style T fill:#6DB3F2,color:#222
    click T href "https://github.com/gerasimsergey/claude-code-ultimate-guide-ua/blob/main/guide/core/architecture.uk.md#вміст-системного-промпту" "Вміст системного промпту"
    style U fill:#6DB3F2,color:#222
    click U href "https://github.com/gerasimsergey/claude-code-ultimate-guide-ua/blob/main/guide/core/architecture.uk.md#вміст-системного-промпту" "Вміст системного промпту"
    style W fill:#6DB3F2,color:#222
    click W href "https://github.com/gerasimsergey/claude-code-ultimate-guide-ua/blob/main/guide/core/architecture.uk.md#вміст-системного-промпту" "Вміст системного промпту"
    style H fill:#6DB3F2,color:#222
    click H href "https://github.com/gerasimsergey/claude-code-ultimate-guide-ua/blob/main/guide/core/architecture.uk.md#вміст-системного-промпту" "Вміст системного промпту"
    style CTX fill:#6DB3F2,color:#222
    click CTX href "https://github.com/gerasimsergey/claude-code-ultimate-guide-ua/blob/main/guide/core/architecture.uk.md#вміст-системного-промпту" "Вміст системного промпту"
    style REQ fill:#6DB3F2,color:#222
    click REQ href "https://github.com/gerasimsergey/claude-code-ultimate-guide-ua/blob/main/guide/core/architecture.uk.md#вміст-системного-промпту" "Вміст системного промпту"
    style API fill:#6DB3F2,color:#222
    click API href "https://github.com/gerasimsergey/claude-code-ultimate-guide-ua/blob/main/guide/core/architecture.uk.md#вміст-системного-промпту" "Вміст системного промпту"
    style NOTE fill:#6DB3F2,color:#222
    click NOTE href "https://github.com/gerasimsergey/claude-code-ultimate-guide-ua/blob/main/guide/core/architecture.uk.md#вміст-системного-промпту" "Вміст системного промпту"
```

<details>
<summary>ASCII версія</summary>

```
Системні інструкції ----------------------+
Доступні / завантажені визначення інструментів -+--> Запит до моделі -> налаштований провайдер
Контекст розмови --------------------------+
  - релевантні файли інструкцій, правила та доступна пам'ять
  - інформація про середовище та файли
  - повідомлення та результати інструментів

Концептуальне групування; не буквальний порядок промпту і не розкладка кешу.
Ізоляція та повторне використання кешу визначаються контрактом провайдера.
```

</details>

> **Джерело**: [Вміст системного промпту](../core/architecture.uk.md#вміст-системного-промпту)
>
> **Офіційний довідник**: [Завантаження контексту](https://code.claude.com/docs/en/how-claude-code-works#context-claude-code-adds-on-its-own) та [ізоляція кешу](https://platform.claude.com/docs/en/build-with-claude/prompt-caching#cache-storage-and-sharing).
>
> Кеші публічного Anthropic API не спільні між організаціями. Ізоляція за робочими просторами також діє в провайдерів, названих у документації з кешування. Повторне використання приватного вмісту CLAUDE.md між користувачами чи організаціями не стверджується.

---

### Ізоляція контексту sub-agent

Ізоляція розмови й ізоляція файлової системи це різні межі. Звичайний subagent має свіжий контекст; fork успадковує розмову батьківського агента. Обидва повертають фінальний результат, тоді як дозволені операції можуть впливати на спільні файли чи зовнішні сервіси.

```mermaid
flowchart TD
    P[Батьківська розмова] --> A{Тип делегування Agent}
    A -->|Звичайний subagent| F[Свіжий контекст<br/>Промпт завдання та визначення агента]
    A -->|Fork| INHERIT[Успадкована розмова<br/>Промпт, інструменти та історія батьківського агента]
    F --> S[Операції інструментів subagent]
    INHERIT --> S
    S --> SHARE[Спільний checkout або зовнішні сервіси<br/>Наслідки залишаються видимими]
    S --> WT[Необов'язкова ізоляція: worktree<br/>Окремий checkout репозиторію]
    SHARE --> RESULT[Фінальний результат потрапляє в батьківський контекст]
    WT --> RESULT
    RESULT --> P
    style P fill:#6DB3F2,color:#222
    click P href "https://github.com/gerasimsergey/claude-code-ultimate-guide-ua/blob/main/guide/core/architecture.uk.md#4-архітектура-під-агентів" "Архітектура під-агентів"
    style A fill:#6DB3F2,color:#222
    click A href "https://github.com/gerasimsergey/claude-code-ultimate-guide-ua/blob/main/guide/core/architecture.uk.md#4-архітектура-під-агентів" "Архітектура під-агентів"
    style F fill:#6DB3F2,color:#222
    click F href "https://github.com/gerasimsergey/claude-code-ultimate-guide-ua/blob/main/guide/core/architecture.uk.md#4-архітектура-під-агентів" "Архітектура під-агентів"
    style INHERIT fill:#6DB3F2,color:#222
    click INHERIT href "https://github.com/gerasimsergey/claude-code-ultimate-guide-ua/blob/main/guide/core/architecture.uk.md#4-архітектура-під-агентів" "Архітектура під-агентів"
    style S fill:#6DB3F2,color:#222
    click S href "https://github.com/gerasimsergey/claude-code-ultimate-guide-ua/blob/main/guide/core/architecture.uk.md#4-архітектура-під-агентів" "Архітектура під-агентів"
    style SHARE fill:#6DB3F2,color:#222
    click SHARE href "https://github.com/gerasimsergey/claude-code-ultimate-guide-ua/blob/main/guide/core/architecture.uk.md#4-архітектура-під-агентів" "Архітектура під-агентів"
    style WT fill:#6DB3F2,color:#222
    click WT href "https://github.com/gerasimsergey/claude-code-ultimate-guide-ua/blob/main/guide/core/architecture.uk.md#4-архітектура-під-агентів" "Архітектура під-агентів"
    style RESULT fill:#6DB3F2,color:#222
    click RESULT href "https://github.com/gerasimsergey/claude-code-ultimate-guide-ua/blob/main/guide/core/architecture.uk.md#4-архітектура-під-агентів" "Архітектура під-агентів"
```

<details>
<summary>ASCII версія</summary>

```
Батьківський -> Agent
  звичайний -> свіжий контекст із делегованим завданням і визначенням
  fork      -> успадкована розмова та конфігурація батьківського агента
       |
       +-> спільні файли й зовнішні сервіси: дозволені наслідки зберігаються
       +-> необов'язковий worktree: окремий checkout для змін у репозиторії
       |
       +-> фінальний результат потрапляє в батьківський контекст

Проміжні виклики інструментів не потрапляють у батьківський контекст.
Worktree не ізолює зовнішні сервіси.
```

</details>

> **Джерело**: [Архітектура під-агентів](../core/architecture.uk.md#4-архітектура-під-агентів)
>
> **Офіційний довідник**: [Контекст fork і необов'язкова ізоляція worktree](https://code.claude.com/docs/en/sub-agents#how-forks-differ-from-other-subagents).

---

### Три конвеєри моделей: dense, MoE та VLM

Це концептуальне спрощення. Dense проти mixture-of-experts (MoE) описує, як побудовано шари, а текстова модель проти vision-language (VLM) описує, які входи приймає модель. Це різні осі, що можуть поєднуватися: модель MoE також може приймати зображення. Anthropic публічно не документує внутрішню архітектуру Claude, тому діаграми показують опубліковані відкриті архітектури, а не Claude. Таблицю осей дивіться в розділі [архітектура, клас розміру, модальність і завдання](../core/ai-concept-boundaries.uk.md#архітектура-клас-розміру-модальність-і-завдання).

```mermaid
flowchart LR
    subgraph DENSE["Dense-декодерна LLM"]
        D1["Текст"] --> D2["Токенізатор"]
        D2 --> D3["Ембединги токенів"]
        D3 --> D4["Стек шарів transformer<br/>attention + feed-forward"]
        D4 --> D5["Ймовірності наступного токена"]
        D5 --> D6["Вибраний токен"]
        D6 -.->|"додається до входу, повтор"| D3
    end
    subgraph MOE["Варіант шару MoE"]
        M1["Стани токенів<br/>після attention"] --> M2["Router<br/>оцінює N експертів для кожного токена"]
        M2 -->|"top-k, Mixtral: 2 з 8"| M3["Вибрані експерти<br/>замінюють блок feed-forward"]
        M2 -.->|"не вибрані"| M4["Неактивні експерти"]
        M3 --> M5["Зважена сума<br/>за вагами router"]
        M5 --> M6["Вихід шару"]
        M7["Примітка: зберігаються всі експерти,<br/>обчислюють лише k"] -.- M3
    end
    subgraph VLM["Vision-language модель"]
        V1["Зображення"] --> V2["Візуальний енкодер"]
        V2 --> V3["Проєкція в простір<br/>ембедингів LLM"]
        V4["Текстові токени<br/>після ембедингу"] --> V5["Об'єднана послідовність"]
        V3 --> V5
        V5 --> V6["Мовна модель<br/>dense або MoE"]
        V6 --> V7["Текстовий вихід"]
    end
    style D1 fill:#6DB3F2,color:#222
    style D2 fill:#6DB3F2,color:#222
    style D3 fill:#6DB3F2,color:#222
    style D4 fill:#6DB3F2,color:#222
    style D5 fill:#6DB3F2,color:#222
    style D6 fill:#6DB3F2,color:#222
    style M1 fill:#6DB3F2,color:#222
    style M2 fill:#6DB3F2,color:#222
    style M3 fill:#6DB3F2,color:#222
    style M4 fill:#6DB3F2,color:#222
    style M5 fill:#6DB3F2,color:#222
    style M6 fill:#6DB3F2,color:#222
    style M7 fill:#6DB3F2,color:#222
    style V1 fill:#6DB3F2,color:#222
    style V2 fill:#6DB3F2,color:#222
    style V3 fill:#6DB3F2,color:#222
    style V4 fill:#6DB3F2,color:#222
    style V5 fill:#6DB3F2,color:#222
    style V6 fill:#6DB3F2,color:#222
    style V7 fill:#6DB3F2,color:#222
```

<details>
<summary>ASCII версія</summary>

```
Dense : текст -> токенізатор -> ембединги токенів
        -> стек шарів transformer (attention + feed-forward)
        -> ймовірності наступного токена -> вибраний токен
        -> додається до входу, повтор

Варіант шару MoE:
        стани токенів після attention -> router (оцінює N експертів для кожного токена)
        -> top-k, Mixtral: 2 з 8 -> вибрані експерти
           (замінюють блок feed-forward) -> зважена сума за вагами
           router -> вихід шару
        не вибрані -> неактивні експерти
        Примітка: зберігаються всі експерти, обчислюють лише k.

VLM   : зображення -> візуальний енкодер -> проєкція в простір ембедингів LLM
        текстові токени після ембедингу ----------------+
        спроєктоване зображення + текст після ембедингу -> об'єднана послідовність
        -> мовна модель (dense або MoE) -> текстовий вихід
```

</details>

> **Джерело**: [Архітектура, клас розміру, модальність і завдання](../core/ai-concept-boundaries.uk.md#архітектура-клас-розміру-модальність-і-завдання)

> Експерти це не окремі повноцінні моделі: вони розташовані всередині кожного шару, замість блоку feed-forward.
>
> Джерела: [технічний звіт Phi-3](https://ar5iv.labs.arxiv.org/html/2404.14219) (архітектура transformer-декодера), [глосарій Anthropic](https://platform.claude.com/docs/en/about-claude/glossary) (авторегресивна мовна модель), [Attention Is All You Need](https://ar5iv.labs.arxiv.org/html/1706.03762) (оригінальний transformer, енкодер-декодер), [Mixtral of Experts](https://arxiv.org/html/2401.04088), [Switch Transformers](https://ar5iv.labs.arxiv.org/html/2101.03961), [LLaVA](https://ar5iv.labs.arxiv.org/html/2304.08485), [документація Claude щодо зору](https://platform.claude.com/docs/en/build-with-claude/vision) (зображення споживають токени).

---
**Локалізація**: [Serhii (MacPlus Software)](https://macplus-software.com)
*Остання синхронізація: Листопад 2026 (v3.46.0)*
