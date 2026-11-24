---
title: "Claude Code: Візуальні діаграми мультиагентних патернів"
description: "Концептуальні топології, ізольовані worktrees, планування, делегування та обмін повідомленнями"
tags: [multi-agent, patterns, worktrees, orchestration, scaling]
---

# Мультиагентні патерни

Координуйте незалежну роботу з чіткою відповідальністю за файли та перевірками інтеграції. Нативні можливості, концептуальні патерни та виміряні результати слід розрізняти.

---

### Agent teams: концептуальні топології оркестрації

Оркестратор, конвеєр і маршрутизація до спеціалістів є концептуальними патернами, а не трьома нативними режимами Agent Teams. Нативні Agent Teams використовують лідера та teammates, що спілкуються між собою; ця функція експериментальна й вимкнена за замовчуванням. Вона додає витрати на координацію та токени. Послідовні завдання й редагування одних і тих самих файлів часто краще підходять для однієї сесії або цілеспрямованих subagent.

```mermaid
flowchart TD
    CHOOSE["Оберіть патерн координації"] --> ORCH["Оркестратор + виконавці<br/>Нативні teams: лідер + teammates<br/>Експериментально, за вибором"]
    CHOOSE --> PIPE["Патерн конвеєра<br/>Етапи залежать від попередніх результатів"]
    CHOOSE --> ROUTE["Патерн маршрутизації до спеціалістів<br/>Вибір виконавця за завданням"]
    ORCH --> FRONT["Виконавець володіє файлами frontend"]
    ORCH --> BACK["Виконавець володіє файлами backend"]
    FRONT --> INTEG["Лідер інтегрує та перевіряє"]
    BACK --> INTEG
    PIPE --> REQ["Вимоги"]
    REQ --> IMPL["Реалізація"]
    IMPL --> REVIEW["Огляд за критеріями"]
    ROUTE --> SELECT{"Потрібна експертиза?"}
    SELECT --> CODE["Виконавець коду"]
    SELECT --> TEST["Виконавець тестів"]
    SELECT --> DOC["Виконавець документації"]
    classDef default fill:#F5E6D3,color:#333,stroke:#E87E2F
    click CHOOSE href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/workflows/agent-teams.md" "View this pattern in the guide"
    click ORCH href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/workflows/agent-teams.md" "View this pattern in the guide"
    click PIPE href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/workflows/agent-teams.md" "View this pattern in the guide"
    click ROUTE href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/workflows/agent-teams.md" "View this pattern in the guide"
    click FRONT href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/workflows/agent-teams.md" "View this pattern in the guide"
    click BACK href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/workflows/agent-teams.md" "View this pattern in the guide"
    click INTEG href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/workflows/agent-teams.md" "View this pattern in the guide"
    click REQ href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/workflows/agent-teams.md" "View this pattern in the guide"
    click IMPL href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/workflows/agent-teams.md" "View this pattern in the guide"
    click REVIEW href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/workflows/agent-teams.md" "View this pattern in the guide"
    click SELECT href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/workflows/agent-teams.md" "View this pattern in the guide"
    click CODE href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/workflows/agent-teams.md" "View this pattern in the guide"
    click TEST href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/workflows/agent-teams.md" "View this pattern in the guide"
    click DOC href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/workflows/agent-teams.md" "View this pattern in the guide"
```

<details>
<summary>ASCII версія</summary>

```
Концептуальні патерни координації
├─ Оркестратор → виконавці з явним володінням файлами → перевірки інтеграції
│  Нативні Agent Teams: лідер + teammates, що спілкуються, експериментальний opt-in
├─ Конвеєр → вимоги → реалізація → огляд
│  Патерн workflow; часто достатньо однієї сесії або subagent
└─ Роутер → потрібний спеціаліст (код / тести / документація)
   Патерн workflow, а не окремий нативний режим team

Teams витрачають більше токенів і потребують координації.
```

</details>

> **Джерело**: [Посібник: Agent teams: концептуальні топології оркестрації](../workflows/agent-teams.uk.md); [Доступність Agent Teams та компроміси](https://code.claude.com/docs/en/agent-teams)

---

### Патерн Git worktree з кількома інстансами

Worktrees дають одночасним інстансам окремі файли робочої копії та гілки. Частина метаданих репозиторію лишається спільною, а інтеграція змін усе ще може спричиняти конфлікти злиття. Команди нижче виконуються з кореня клонованого репозиторію; кожна команда створює показаний шлях.

```mermaid
flowchart TD
    REPO["Корінь репозиторію"] --> WA["git worktree add -b feature-A<br/>../worktrees/feature-A"]
    REPO --> WB["git worktree add -b feature-B<br/>../worktrees/feature-B"]
    REPO --> WC["git worktree add -b bugfix-C<br/>../worktrees/bugfix-C"]
    WA --> CA["Claude 1: ../worktrees/feature-A<br/>Коміти у feature-A"]
    WB --> CB["Claude 2: ../worktrees/feature-B<br/>Коміти у feature-B"]
    WC --> CC["Claude 3: ../worktrees/bugfix-C<br/>Коміти у bugfix-C"]
    CA --> INTEGRATE["Інтеграція змін<br/>Розв'язання конфліктів, якщо є"]
    CB --> INTEGRATE
    CC --> INTEGRATE
    INTEGRATE --> CHECK["Запуск інтеграційних перевірок і огляд"]
    CHECK --> MERGE["Merge, коли критерії виконано"]
    classDef default fill:#F5E6D3,color:#333,stroke:#E87E2F
    click REPO href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#912-git-best-practices--workflows" "View this pattern in the guide"
    click WA href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#912-git-best-practices--workflows" "View this pattern in the guide"
    click WB href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#912-git-best-practices--workflows" "View this pattern in the guide"
    click WC href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#912-git-best-practices--workflows" "View this pattern in the guide"
    click CA href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#912-git-best-practices--workflows" "View this pattern in the guide"
    click CB href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#912-git-best-practices--workflows" "View this pattern in the guide"
    click CC href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#912-git-best-practices--workflows" "View this pattern in the guide"
    click INTEGRATE href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#912-git-best-practices--workflows" "View this pattern in the guide"
    click CHECK href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#912-git-best-practices--workflows" "View this pattern in the guide"
    click MERGE href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#912-git-best-practices--workflows" "View this pattern in the guide"
```

<details>
<summary>ASCII версія</summary>

```
З кореня клонованого репозиторію:
git worktree add -b feature-A ../worktrees/feature-A
git worktree add -b feature-B ../worktrees/feature-B
git worktree add -b bugfix-C ../worktrees/bugfix-C

Кожен шлях → свій інстанс Claude → коміти у власну гілку
         → інтеграція → розв'язання конфліктів, якщо є
         → інтеграційні перевірки + огляд → merge

Окремі робочі файли; спільні метадані репозиторію.
Одночасне редагування ізольоване, конфлікти злиття залишаються можливими.
```

</details>

> **Джерело**: [Посібник: патерн Git worktree з кількома інстансами](../ultimate-guide.uk.md#912-git-найкращі-практики-та-робочі-процеси); [Семантика Git worktree](https://git-scm.com/docs/git-worktree)

---

### Патерн планування з двома інстансами (Dual-Instance)

Використовуйте дві сесії, коли корисна окрема межа планування. Планувальнику без інструментів потрібні релевантні документи, передані в його prompt. Або ж режим Plan дозволяє дослідження з обмеженими діями. Налаштовуйте обмеження явно: сама лише друга сесія не вимикає інструменти. Виконавцю потрібні затверджений план і необхідний контекст, а не автоматичне успадкування розмови планувальника.

```mermaid
flowchart TD
    DOCS["Користувач надає вимоги<br/>та релевантні документи"] --> PLANNER["Сесія планувальника<br/>Явно налаштовано без інструментів<br/>або обмежений режим Plan"]
    PLANNER --> PLAN["План: файли, кроки, перевірки<br/>та обмеження відкату"]
    PLAN --> REVIEW{"Людина схвалює?"}
    REVIEW -->|Ні| PLANNER
    REVIEW -->|Так| TRANSFER["Передача затвердженого плану<br/>та необхідного контексту"]
    TRANSFER --> EXEC["Сесія виконавця<br/>Налаштовані дозволи на інструменти"]
    EXEC --> VERIFY["Запуск перевірок і порівняння з планом"]
    VERIFY --> REPORT["Звіт про результати та межі доказів"]
    classDef default fill:#F5E6D3,color:#333,stroke:#E87E2F
    click DOCS href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/workflows/dual-instance-planning.md" "View this pattern in the guide"
    click PLANNER href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/workflows/dual-instance-planning.md" "View this pattern in the guide"
    click PLAN href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/workflows/dual-instance-planning.md" "View this pattern in the guide"
    click REVIEW href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/workflows/dual-instance-planning.md" "View this pattern in the guide"
    click TRANSFER href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/workflows/dual-instance-planning.md" "View this pattern in the guide"
    click EXEC href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/workflows/dual-instance-planning.md" "View this pattern in the guide"
    click VERIFY href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/workflows/dual-instance-planning.md" "View this pattern in the guide"
    click REPORT href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/workflows/dual-instance-planning.md" "View this pattern in the guide"
```

<details>
<summary>ASCII версія</summary>

```
Надані документи → планувальник
                     (явна конфігурація без інструментів
                      або обмежений режим Plan для дослідження)
                   → план → огляд людиною
                            ├─ Доопрацювати → планувальник
                            └─ Схвалити → передати план + необхідний контекст
                                       → виконавець з налаштованими інструментами
                                       → перевірки + звіт про результат

Дві сесії самі по собі не забезпечують обмеження інструментів і не передають контекст.
```

</details>

> **Джерело**: [Посібник: патерн планування з двома інстансами](../workflows/dual-instance-planning.uk.md); [Plan permission mode](https://code.claude.com/docs/en/permissions), [Subagent tool restrictions](https://code.claude.com/docs/en/sub-agents)

---

### Патерн горизонтального масштабування

Розпаралелюйте незалежну роботу з явним володінням файлами, а потім вимірюйте результат після координації та інтеграції. Більше інстансів не гарантує пропорційного прискорення: витрати та залежності можуть переважити користь. Перш ніж стверджувати про продуктивність, виміряйте прискорення та вартість на власному навантаженні.

```mermaid
flowchart TD
    TASK["Велике завдання"] --> SPLIT["Визначте незалежні підзавдання<br/>та володіння файлами"]
    SPLIT --> A["Виконавець A<br/>Власні файли та критерії"]
    SPLIT --> B["Виконавець B<br/>Власні файли та критерії"]
    SPLIT --> C["Виконавець C<br/>Власні файли та критерії"]
    A --> AGG["Агрегація результатів і доказів"]
    B --> AGG
    C --> AGG
    AGG --> REVIEW["Розв'язання залежностей/конфліктів<br/>та інтеграційні перевірки"]
    REVIEW --> MEASURE["Виміряйте виграш у часі та вартість токенів<br/>для цього навантаження"]
    classDef default fill:#F5E6D3,color:#333,stroke:#E87E2F
    click TASK href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#917-scaling-patterns-multi-instance-workflows" "View this pattern in the guide"
    click SPLIT href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#917-scaling-patterns-multi-instance-workflows" "View this pattern in the guide"
    click A href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#917-scaling-patterns-multi-instance-workflows" "View this pattern in the guide"
    click B href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#917-scaling-patterns-multi-instance-workflows" "View this pattern in the guide"
    click C href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#917-scaling-patterns-multi-instance-workflows" "View this pattern in the guide"
    click AGG href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#917-scaling-patterns-multi-instance-workflows" "View this pattern in the guide"
    click REVIEW href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#917-scaling-patterns-multi-instance-workflows" "View this pattern in the guide"
    click MEASURE href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#917-scaling-patterns-multi-instance-workflows" "View this pattern in the guide"
```

<details>
<summary>ASCII версія</summary>

```
Велике завдання → незалежні підзавдання з явним володінням файлами
            → паралельні виконавці A / B / C
            → агрегація доказів
            → розв'язання залежностей і конфліктів
            → інтеграційні перевірки
            → вимірювання виграшу в часі та вартості токенів

Гарантованого множника немає; координація зменшує виграш.
```

</details>

> **Джерело**: [Посібник: патерн горизонтального масштабування](../ultimate-guide.uk.md#917-scaling-patterns-multi-instance-workflows); [Team size, cost and diminishing returns](https://code.claude.com/docs/en/agent-teams)

---

### Матриця рішень для Multi-Instance

Обирайте за залежностями, потребою в комунікації та ізоляції, а вже потім за кількістю виконавців. Нативний інструмент делегування називається Agent; Task було його колишньою назвою, яка лишається псевдонімом для сумісності в налаштуваннях і визначеннях. Для використання subagent не потрібні чотири інстанси.

```mermaid
flowchart TD
    TASK["Завдання для виконання"] --> INDEP{"Незалежна робота, яку варто делегувати?"}
    INDEP -->|Ні| SINGLE["Одна сесія<br/>Планування та виконання за потреби"]
    INDEP -->|Так| COMM{"Виконавцям потрібне обговорення<br/>та спільна координація?"}
    COMM -->|Ні| SUB["Інструмент Agent<br/>Цілеспрямовані subagent повертають результати<br/>Колишня назва: Task"]
    COMM -->|Так| TEAM["Експериментальні Agent Teams<br/>Лідер + teammates, що спілкуються"]
    SUB --> EDIT{"Одночасні редагування файлів?"}
    TEAM --> EDIT
    EDIT -->|Так| WT["Окреме володіння файлами<br/>Worktrees для ізоляції checkout"]
    EDIT -->|Ні| READ["Паралельне дослідження або огляд"]
    WT --> SIZE["Оберіть кількість за незалежністю завдань,<br/>вартістю та координацією"]
    READ --> SIZE
    classDef default fill:#F5E6D3,color:#333,stroke:#E87E2F
    click TASK href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#917-scaling-patterns-multi-instance-workflows" "View this pattern in the guide"
    click INDEP href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#917-scaling-patterns-multi-instance-workflows" "View this pattern in the guide"
    click SINGLE href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#917-scaling-patterns-multi-instance-workflows" "View this pattern in the guide"
    click COMM href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#917-scaling-patterns-multi-instance-workflows" "View this pattern in the guide"
    click SUB href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#917-scaling-patterns-multi-instance-workflows" "View this pattern in the guide"
    click TEAM href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#917-scaling-patterns-multi-instance-workflows" "View this pattern in the guide"
    click EDIT href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#917-scaling-patterns-multi-instance-workflows" "View this pattern in the guide"
    click WT href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#917-scaling-patterns-multi-instance-workflows" "View this pattern in the guide"
    click READ href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#917-scaling-patterns-multi-instance-workflows" "View this pattern in the guide"
    click SIZE href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#917-scaling-patterns-multi-instance-workflows" "View this pattern in the guide"
```

<details>
<summary>ASCII версія</summary>

```
Чи варто делегувати незалежну роботу?
├─ Ні → одна сесія, етапи за потреби
└─ Так → потрібне обговорення між виконавцями / спільна координація?
         ├─ Ні → subagent інструмента Agent повертають результати
         │       (Task — історичний псевдонім для сумісності)
         └─ Так → експериментальні Agent Teams
                    │
         Одночасні редагування файлів?
         ├─ Так → володіння файлами + окремі worktrees
         └─ Ні → паралельне дослідження/огляд
                    │
         Кількість за незалежністю, вартістю та координацією, а не за правилом 4+.
```

</details>

> **Джерело**: [Посібник: матриця рішень для Multi-Instance](../ultimate-guide.uk.md#917-scaling-patterns-multi-instance-workflows); [Agent tool rename and delegation](https://code.claude.com/docs/en/sub-agents), [Teams versus subagents](https://code.claude.com/docs/en/agent-teams)

---

### Обмін повідомленнями між сесіями: виявлення та доставка

Придатні незалежні сесії можуть виявляти одна одну через ListAgents і надсилати текст через SendMessage. Доставка в межах однієї машини використовує локальні сокети або іменовані канали (named pipes); доставка на іншу машину та в хмару використовує інфраструктуру Anthropic. Явне значення hold у crossSessionInbound утримує повідомлення, доки відповідний accept їх не випустить. Діалоги схвалення належать до деяких значень за замовчуванням у режимах дозволів у підтримуваних терміналах, а не до явного налаштування hold. Доступність залежить від версії, провайдера та вимог Remote Control.

```mermaid
flowchart TD
    SESSIONS["Придатні сесії<br/>Прив'язують inbox і реєструються локально"] --> LIST["ListAgents / list-agents<br/>Доступні peers і agents"]
    LIST --> SEND["SendMessage text<br/>Ціль визначено"]
    SEND --> WHERE{"Розташування цілі?"}
    WHERE -->|Та сама машина| LOCAL["Unix socket / named pipe<br/>Локальна доставка"]
    WHERE -->|Інша машина або хмара| REMOTE["Інфраструктура Anthropic<br/>Remote Control або хмарна сесія"]
    LOCAL --> SETTING{"Явне налаштування inbound?"}
    REMOTE --> SETTING
    SETTING -->|accept| DELIVER["Доставлено отримувачу Claude"]
    SETTING -->|hold| HOLD["Не доставлено<br/>Пізніший відповідний accept випустить"]
    SETTING -->|refuse| DROP["Відкинуто"]
    SETTING -->|Не задано| DEFAULT["Значення за замовчуванням режиму дозволів<br/>Доставити або утримати до схвалення,<br/>якщо діалог підтримується"]
    DEFAULT --> DELIVER
    DEFAULT --> WAIT["Черга схвалення/утримання за замовчуванням<br/>Залежить від поверхні та терміну дії"]
    DELIVER --> BOUND["Дозволи отримувача лишаються чинними<br/>Текст від peer не може схвалювати дозволи<br/>чи авторизувати зміни конфігурації"]
    classDef default fill:#F5E6D3,color:#333,stroke:#E87E2F
    click SESSIONS href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/workflows/cross-session-messaging.md" "View this pattern in the guide"
    click LIST href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/workflows/cross-session-messaging.md" "View this pattern in the guide"
    click SEND href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/workflows/cross-session-messaging.md" "View this pattern in the guide"
    click WHERE href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/workflows/cross-session-messaging.md" "View this pattern in the guide"
    click LOCAL href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/workflows/cross-session-messaging.md" "View this pattern in the guide"
    click REMOTE href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/workflows/cross-session-messaging.md" "View this pattern in the guide"
    click SETTING href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/workflows/cross-session-messaging.md" "View this pattern in the guide"
    click DELIVER href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/workflows/cross-session-messaging.md" "View this pattern in the guide"
    click HOLD href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/workflows/cross-session-messaging.md" "View this pattern in the guide"
    click DROP href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/workflows/cross-session-messaging.md" "View this pattern in the guide"
    click DEFAULT href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/workflows/cross-session-messaging.md" "View this pattern in the guide"
    click WAIT href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/workflows/cross-session-messaging.md" "View this pattern in the guide"
    click BOUND href "https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/workflows/cross-session-messaging.md" "View this pattern in the guide"
```

<details>
<summary>ASCII версія</summary>

```
Придатні сесії → реєстр/inbox → ListAgents → SendMessage
Розташування цілі?
├─ Та сама машина → Unix socket / named pipe, локальна доставка
└─ Інша машина/хмара → інфраструктура Anthropic
                               │
Явний crossSessionInbound?
├─ accept → доставлено
├─ hold   → не доставлено; пізніший відповідний accept випустить
├─ refuse → відкинуто
└─ не задано → значення за замовчуванням залежить від режиму
            ├─ доставити
            └─ утримати до схвалення, залежно від терміналу/поверхні та терміну дії

Текст від peer не схвалює дозволи й не авторизує зміни конфігурації.
Доступність визначається вимогами версії/провайдера/Remote Control.
```

</details>

> **Джерело**: [Посібник: обмін повідомленнями між сесіями](../workflows/cross-session-messaging.uk.md); [Messaging controls and availability](https://code.claude.com/docs/en/cross-session-messaging)

---
**Локалізація**: [Serhii (MacPlus Software)](https://macplus-software.com)
*Остання синхронізація: Травень 2026*
