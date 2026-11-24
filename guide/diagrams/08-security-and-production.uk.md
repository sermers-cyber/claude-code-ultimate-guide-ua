---
title: "Claude Code: діаграми безпеки та production"
description: "Примусові засоби захисту, межі пісочниці, докази та CI-шлюзи релізу"
tags: [security, production, sandbox, ci-cd, defense]
---

# Безпека та production

Під час роботи з Claude Code у чутливих середовищах спирайтеся на примусово застосовувані межі виконання та спостережувані докази. Жодна діаграма не гарантує універсальної ізоляції чи безпеки розгортання.

---

### Трирівнева модель захисту

Запобігання, виявлення та реагування знижують різні ризики. Налаштуйте примусові дозволи та ізоляцію процесу до запуску недовіреної роботи. CLAUDE.md спрямовує модель, але не є примусовою межею безпеки. Для захисту конфіденційних файлів потрібні правила дозволів для файлових інструментів та обмеження на рівні операційної системи, а не припущення про наявність ignore-файлу. Журнали потрібно налаштувати й перевірити їхнє покриття. Режим bypass permissions доречний лише в ізольованому середовищі, а не тільки тому, що завдання названо CI.

```mermaid
flowchart TD
    THREAT["Недовірений код або вміст"] --> PREV["Запобігання до виконання"]
    PREV --> VET["Перевірка MCP/skills/plugins<br/>перегляд оновлень і фіксація версій"]
    PREV --> PERM["Мінімальні дозволи інструментів<br/>керовані політики deny/ask"]
    PREV --> FILES["Захист конфіденційних файлів<br/>deny для файлових інструментів + обмеження доступу ОС"]
    PREV --> ISOLATE["Ізоляція всього процесу за потреби<br/>контейнер / VM, обмежена мережа"]
    VET --> RUN["Виконання в межах налаштованих обмежень"]
    PERM --> RUN
    FILES --> RUN
    ISOLATE --> RUN
    RUN --> DETECT["Виявлення<br/>hooks + збір аудиту + сповіщення<br/>перевірте покриття журналів"]
    DETECT --> INCIDENT{"Підозріла дія або витік?"}
    INCIDENT -->|Ні| CONTINUE["Продовжуйте моніторинг<br/>Залишковий ризик зберігається"]
    INCIDENT -->|Так| RESP["Реагування<br/>зупинити доступ, зберегти докази<br/>відкат і ротація розкритих секретів"]
    RESP --> REVIEW["Розслідуйте витік<br/>і посильте контролі"]
    classDef default fill:#F5E6D3,color:#333,stroke:#E87E2F
    click THREAT href "https://github.com/gerasimsergey/claude-code-ultimate-guide-ua/blob/main/guide/security/security-hardening.uk.md" "Переглянути цей патерн у посібнику"
    click PREV href "https://github.com/gerasimsergey/claude-code-ultimate-guide-ua/blob/main/guide/security/security-hardening.uk.md" "Переглянути цей патерн у посібнику"
    click VET href "https://github.com/gerasimsergey/claude-code-ultimate-guide-ua/blob/main/guide/security/security-hardening.uk.md" "Переглянути цей патерн у посібнику"
    click PERM href "https://github.com/gerasimsergey/claude-code-ultimate-guide-ua/blob/main/guide/security/security-hardening.uk.md" "Переглянути цей патерн у посібнику"
    click FILES href "https://github.com/gerasimsergey/claude-code-ultimate-guide-ua/blob/main/guide/security/security-hardening.uk.md" "Переглянути цей патерн у посібнику"
    click ISOLATE href "https://github.com/gerasimsergey/claude-code-ultimate-guide-ua/blob/main/guide/security/security-hardening.uk.md" "Переглянути цей патерн у посібнику"
    click RUN href "https://github.com/gerasimsergey/claude-code-ultimate-guide-ua/blob/main/guide/security/security-hardening.uk.md" "Переглянути цей патерн у посібнику"
    click DETECT href "https://github.com/gerasimsergey/claude-code-ultimate-guide-ua/blob/main/guide/security/security-hardening.uk.md" "Переглянути цей патерн у посібнику"
    click INCIDENT href "https://github.com/gerasimsergey/claude-code-ultimate-guide-ua/blob/main/guide/security/security-hardening.uk.md" "Переглянути цей патерн у посібнику"
    click CONTINUE href "https://github.com/gerasimsergey/claude-code-ultimate-guide-ua/blob/main/guide/security/security-hardening.uk.md" "Переглянути цей патерн у посібнику"
    click RESP href "https://github.com/gerasimsergey/claude-code-ultimate-guide-ua/blob/main/guide/security/security-hardening.uk.md" "Переглянути цей патерн у посібнику"
    click REVIEW href "https://github.com/gerasimsergey/claude-code-ultimate-guide-ua/blob/main/guide/security/security-hardening.uk.md" "Переглянути цей патерн у посібнику"
```

<details>
<summary>ASCII версія</summary>

```
ЗАПОБІГАННЯ (до виконання)
  Перевіряйте сервери й оновлення; мінімальні дозволи; керовані політики
  deny для файлових інструментів + обмеження доступу ОС до конфіденційних файлів
  Ізоляція всього процесу та обмежена мережа за потреби
                        │
ВИЯВЛЕННЯ
  Налаштовані hooks/збір журналів/сповіщення; перевірте покриття
                        │
Підозріла дія або витік?
├─ Ні → моніторьте залишковий ризик
└─ Так → РЕАГУВАННЯ: зупинити доступ, зберегти докази,
                    відкат, ротація розкритих секретів, розслідування

CLAUDE.md спрямовує поведінку; він не є примусовою межею безпеки.
Bypass лише в ізольованому середовищі, а не в будь-якому CI-завданні.
```

</details>

> **Джерело**: [Посібник: трирівнева модель захисту](../security/security-hardening.uk.md); [Обмеження дотримання CLAUDE.md](https://code.claude.com/docs/en/memory), [Дозволи](https://code.claude.com/docs/en/permissions), [Безпека MCP](https://code.claude.com/docs/en/security)

---

### Дерево рішень щодо пісочниці

Оберіть межу, яка покриває процес, що несе ризик. Нативна пісочниця оболонки підтримує macOS (Seatbelt) та Linux/WSL2 (bubblewrap і socat); для нативної Windows потрібен WSL2 або інше ізольоване середовище. Файлові інструменти, локальні MCP-сервери та hooks працюють поза пісочницею оболонки. Невідомі MCP або hooks потребують перевірки та, за потреби, ізоляції всього процесу Claude Code. acceptEdits автоматично схвалює редагування, тому це не суворіша альтернатива ручним дозволам. Типове читання в нативній пісочниці може охоплювати облікові дані, якщо його явно не обмежити.

```mermaid
flowchart TD
    START["Оберіть межу виконання"] --> PROCESS{"Недовірені MCP, hooks<br/>або доступ до всього процесу?"}
    PROCESS -->|Так| WHOLE["Спочатку перевірте, потім ізолюйте весь процес<br/>контейнер / VM або окреме середовище<br/>обмежте облікові дані та мережу"]
    PROCESS -->|Ні, лише команди оболонки| PLATFORM{"Платформа?"}
    PLATFORM -->|macOS| MAC["Нативна пісочниця оболонки<br/>Seatbelt, вмикається через /sandbox"]
    PLATFORM -->|Linux або WSL2| LINUX["Нативна пісочниця оболонки<br/>залежності bubblewrap + socat"]
    PLATFORM -->|Нативна Windows| WIN["Використовуйте WSL2, контейнер або VM<br/>нативної пісочниці оболонки немає"]
    MAC --> CONFIG["Обмежте файлову систему й мережу<br/>перевірте фактичні межі"]
    LINUX --> CONFIG
    WIN --> CONFIG
    WHOLE --> CONFIG
    CONFIG --> PERM["Збережіть відповідні дозволи<br/>ручні + вузький allowlist за потреби<br/>перевіряйте зміни та докази"]
    PERM --> PROD{"Production або CI-середовище?"}
    PROD -->|Так| CI["Ефемерне/ізольоване виконання<br/>обмежені секрети та шлюзи розгортання"]
    PROD -->|Ні| LOCAL["Застосуйте межу відповідно до ризику проєкту<br/>стежте за залишковою експозицією"]
    classDef default fill:#F5E6D3,color:#333,stroke:#E87E2F
    click START href "https://github.com/gerasimsergey/claude-code-ultimate-guide-ua/blob/main/guide/security/sandbox-native.uk.md" "Переглянути цей патерн у посібнику"
    click PROCESS href "https://github.com/gerasimsergey/claude-code-ultimate-guide-ua/blob/main/guide/security/sandbox-native.uk.md" "Переглянути цей патерн у посібнику"
    click WHOLE href "https://github.com/gerasimsergey/claude-code-ultimate-guide-ua/blob/main/guide/security/sandbox-native.uk.md" "Переглянути цей патерн у посібнику"
    click PLATFORM href "https://github.com/gerasimsergey/claude-code-ultimate-guide-ua/blob/main/guide/security/sandbox-native.uk.md" "Переглянути цей патерн у посібнику"
    click MAC href "https://github.com/gerasimsergey/claude-code-ultimate-guide-ua/blob/main/guide/security/sandbox-native.uk.md" "Переглянути цей патерн у посібнику"
    click LINUX href "https://github.com/gerasimsergey/claude-code-ultimate-guide-ua/blob/main/guide/security/sandbox-native.uk.md" "Переглянути цей патерн у посібнику"
    click WIN href "https://github.com/gerasimsergey/claude-code-ultimate-guide-ua/blob/main/guide/security/sandbox-native.uk.md" "Переглянути цей патерн у посібнику"
    click CONFIG href "https://github.com/gerasimsergey/claude-code-ultimate-guide-ua/blob/main/guide/security/sandbox-native.uk.md" "Переглянути цей патерн у посібнику"
    click PERM href "https://github.com/gerasimsergey/claude-code-ultimate-guide-ua/blob/main/guide/security/sandbox-native.uk.md" "Переглянути цей патерн у посібнику"
    click PROD href "https://github.com/gerasimsergey/claude-code-ultimate-guide-ua/blob/main/guide/security/sandbox-native.uk.md" "Переглянути цей патерн у посібнику"
    click CI href "https://github.com/gerasimsergey/claude-code-ultimate-guide-ua/blob/main/guide/security/sandbox-native.uk.md" "Переглянути цей патерн у посібнику"
    click LOCAL href "https://github.com/gerasimsergey/claude-code-ultimate-guide-ua/blob/main/guide/security/sandbox-native.uk.md" "Переглянути цей патерн у посібнику"
```

<details>
<summary>ASCII версія</summary>

```
Що потребує ізоляції?
├─ Недовірені MCP/hooks/весь процес → спочатку перевірка + ізоляція всього процесу
│                                    обмежте секрети та мережу
└─ Команди оболонки → нативна пісочниця залежно від платформи
   ├─ macOS → Seatbelt, /sandbox
   ├─ Linux/WSL2 → bubblewrap + socat, /sandbox
   └─ Нативна Windows → WSL2/контейнер/VM
               │
Обмежте файлову систему/мережу; перевірте примусову межу
Збережіть відповідні дозволи та перевіряйте зміни
├─ Production/CI → ізольоване виконання + обмежені секрети + шлюзи релізу
└─ Локальний проєкт → межа відповідно до ризику проєкту

Пісочниця оболонки не охоплює файлові інструменти, MCP-сервери чи hooks.
acceptEdits автоматично приймає редагування, а не посилює перевірку перед ними.
Читання облікових даних потребує явних обмежень.
```

</details>

> **Джерело**: [Посібник: дерево рішень щодо пісочниці](../security/sandbox-native.uk.md); [Обсяг і платформи нативної пісочниці](https://code.claude.com/docs/en/sandboxing), [Режими дозволів](https://code.claude.com/docs/en/permissions)

---

### Парадокс верифікації

Прохання до генератора дати необґрунтовану думку не верифікує його роботу. Claude може запускати детерміновані тести та показувати результати; ці перевірки доводять лише те, що вони охоплюють. Критичну поведінку перевіряйте незалежно та розрізняйте перевірки коду, готовність до розгортання й спостережувану поведінку під час виконання. Самі лише пройдені перевірки не гарантують безпечного релізу.

```mermaid
flowchart TD
    CODE["Claude пише код"] --> OPINION["Самоперевірка лише на рівні думки<br/>Немає запускних доказів"]
    OPINION --> RISK["Дефекти можуть лишитися непоміченими"]
    CODE --> TEST["Запустіть тести поведінки/регресії<br/>перегляньте перевірки (assertions) та вивід"]
    CODE --> STATIC["Запустіть відповідні статичні перевірки та перевірки безпеки"]
    CODE --> HUMAN["Незалежне рев'ю критичної поведінки"]
    TEST --> GATE{"Докази відповідають критеріям прийняття?"}
    STATIC --> GATE
    HUMAN --> GATE
    GATE -->|Ні| FIX["Виправте та повторно запустіть відповідні перевірки"]
    FIX --> TEST
    GATE -->|Так| RELEASE["Рішення про реліз<br/>відомий обсяг доказів і залишкові ризики"]
    RELEASE --> RUNTIME["Перевірки розгортання<br/>верифікація під час виконання та моніторинг"]
    classDef default fill:#F5E6D3,color:#333,stroke:#E87E2F
    click CODE href "https://github.com/gerasimsergey/claude-code-ultimate-guide-ua/blob/main/guide/security/production-safety.uk.md" "Переглянути цей патерн у посібнику"
    click OPINION href "https://github.com/gerasimsergey/claude-code-ultimate-guide-ua/blob/main/guide/security/production-safety.uk.md" "Переглянути цей патерн у посібнику"
    click RISK href "https://github.com/gerasimsergey/claude-code-ultimate-guide-ua/blob/main/guide/security/production-safety.uk.md" "Переглянути цей патерн у посібнику"
    click TEST href "https://github.com/gerasimsergey/claude-code-ultimate-guide-ua/blob/main/guide/security/production-safety.uk.md" "Переглянути цей патерн у посібнику"
    click STATIC href "https://github.com/gerasimsergey/claude-code-ultimate-guide-ua/blob/main/guide/security/production-safety.uk.md" "Переглянути цей патерн у посібнику"
    click HUMAN href "https://github.com/gerasimsergey/claude-code-ultimate-guide-ua/blob/main/guide/security/production-safety.uk.md" "Переглянути цей патерн у посібнику"
    click GATE href "https://github.com/gerasimsergey/claude-code-ultimate-guide-ua/blob/main/guide/security/production-safety.uk.md" "Переглянути цей патерн у посібнику"
    click FIX href "https://github.com/gerasimsergey/claude-code-ultimate-guide-ua/blob/main/guide/security/production-safety.uk.md" "Переглянути цей патерн у посібнику"
    click RELEASE href "https://github.com/gerasimsergey/claude-code-ultimate-guide-ua/blob/main/guide/security/production-safety.uk.md" "Переглянути цей патерн у посібнику"
    click RUNTIME href "https://github.com/gerasimsergey/claude-code-ultimate-guide-ua/blob/main/guide/security/production-safety.uk.md" "Переглянути цей патерн у посібнику"
```

<details>
<summary>ASCII версія</summary>

```
Лише думка: згенерований код → «виглядає добре» → дефекти можуть лишитися

Докази: згенерований код → тести поведінки + відповідні статичні перевірки
                         → незалежне рев'ю критичних ділянок
                         → критерії прийняття виконано?
                           ├─ Ні → виправити й повторно запустити перевірки
                           └─ Так → рішення про реліз для відомого обсягу
                                    → перевірки розгортання
                                    → верифікація/моніторинг під час виконання

Запускна перевірка, виконана Claude, є доказом у межах свого покриття.
Пройдені перевірки не гарантують безпечного релізу.
```

</details>

> **Джерело**: [Посібник: парадокс верифікації](../security/production-safety.uk.md); [Запускна верифікація та змагальне рев'ю](https://code.claude.com/docs/en/best-practices)

---

### Конвеєр інтеграції CI/CD

CI має запускати lint, тести та перевірки безпеки як окремі завдання й використовувати їхні статуси як шлюзи. Claude Code може прочитати ці докази та підготувати дорадче рев'ю в неінтерактивному режимі друку (print mode) через claude -p або --print. Сам промпт не гарантує паралельного виконання чи надійного зведення pass/fail. Явно налаштуйте автентифікацію, дозволи інструментів і виводи завдань; рішення про реліз забезпечуйте через CI та рев'ю людини, а не думку агента.

```mermaid
flowchart TD
    PR["PR створено або оновлено"] --> ENV["CI налаштовує ізольований runner<br/>секрет автентифікації + мінімальні дозволи"]
    ENV --> LINT["CI-завдання lint<br/>зафіксувати статус завершення"]
    ENV --> TEST["CI-завдання тестів<br/>зафіксувати перевірки та статус завершення"]
    ENV --> SCAN["CI-завдання сканування безпеки<br/>зафіксувати знахідки та статус завершення"]
    LINT --> GATE{"Обов'язкові CI-завдання пройдено?"}
    TEST --> GATE
    SCAN --> GATE
    GATE -->|Ні| FAIL["Повідомити про невдалі завдання<br/>розробник виправляє й повторно запускає CI"]
    FAIL --> ENV
    LINT --> EVIDENCE["Зібрати докази завдань"]
    TEST --> EVIDENCE
    SCAN --> EVIDENCE
    EVIDENCE --> CLAUDE["claude -p<br/>Перегляд доказів перевірок якості"]
    CLAUDE --> REPORT["Дорадче рев'ю агента<br/>не замінює статус CI"]
    GATE -->|Так| HUMAN["Рев'ю людини та правила гілок"]
    REPORT --> HUMAN
    HUMAN --> RELEASE["Шлюз merge/релізу<br/>перевірки розгортання та під час виконання"]
    classDef default fill:#F5E6D3,color:#333,stroke:#E87E2F
    click PR href "https://github.com/gerasimsergey/claude-code-ultimate-guide-ua/blob/main/guide/ultimate-guide.uk.md#93-інтеграція-cicd" "Переглянути цей патерн у посібнику"
    click ENV href "https://github.com/gerasimsergey/claude-code-ultimate-guide-ua/blob/main/guide/ultimate-guide.uk.md#93-інтеграція-cicd" "Переглянути цей патерн у посібнику"
    click LINT href "https://github.com/gerasimsergey/claude-code-ultimate-guide-ua/blob/main/guide/ultimate-guide.uk.md#93-інтеграція-cicd" "Переглянути цей патерн у посібнику"
    click TEST href "https://github.com/gerasimsergey/claude-code-ultimate-guide-ua/blob/main/guide/ultimate-guide.uk.md#93-інтеграція-cicd" "Переглянути цей патерн у посібнику"
    click SCAN href "https://github.com/gerasimsergey/claude-code-ultimate-guide-ua/blob/main/guide/ultimate-guide.uk.md#93-інтеграція-cicd" "Переглянути цей патерн у посібнику"
    click GATE href "https://github.com/gerasimsergey/claude-code-ultimate-guide-ua/blob/main/guide/ultimate-guide.uk.md#93-інтеграція-cicd" "Переглянути цей патерн у посібнику"
    click FAIL href "https://github.com/gerasimsergey/claude-code-ultimate-guide-ua/blob/main/guide/ultimate-guide.uk.md#93-інтеграція-cicd" "Переглянути цей патерн у посібнику"
    click EVIDENCE href "https://github.com/gerasimsergey/claude-code-ultimate-guide-ua/blob/main/guide/ultimate-guide.uk.md#93-інтеграція-cicd" "Переглянути цей патерн у посібнику"
    click CLAUDE href "https://github.com/gerasimsergey/claude-code-ultimate-guide-ua/blob/main/guide/ultimate-guide.uk.md#93-інтеграція-cicd" "Переглянути цей патерн у посібнику"
    click REPORT href "https://github.com/gerasimsergey/claude-code-ultimate-guide-ua/blob/main/guide/ultimate-guide.uk.md#93-інтеграція-cicd" "Переглянути цей патерн у посібнику"
    click HUMAN href "https://github.com/gerasimsergey/claude-code-ultimate-guide-ua/blob/main/guide/ultimate-guide.uk.md#93-інтеграція-cicd" "Переглянути цей патерн у посібнику"
    click RELEASE href "https://github.com/gerasimsergey/claude-code-ultimate-guide-ua/blob/main/guide/ultimate-guide.uk.md#93-інтеграція-cicd" "Переглянути цей патерн у посібнику"
```

<details>
<summary>ASCII версія</summary>

```
PR → ізольований CI runner + секрет автентифікації + мінімальні дозволи
   → налаштовані завдання (паралельно, лише якщо CI це оголошує)
     ├─ Lint → статус завершення
     ├─ Тести → результати перевірок + статус завершення
     └─ Сканування безпеки → знахідки + статус завершення
           │
           ├─ Обов'язкові CI-завдання пройдено?
           │  ├─ Ні → повідомити про збій → виправити → повторно запустити CI
           │  └─ Так → рев'ю людини + правила гілок → шлюз релізу
           │                                      → перевірки під час виконання
           └─ Докази завдань → claude -p "Review quality-check evidence"
                              → дорадче рев'ю для людини

Шлюз — це статус CI-завдання; думка агента цим статусом не є.
```

</details>

> **Джерело**: [Посібник: конвеєр інтеграції CI/CD](../ultimate-guide.uk.md#93-інтеграція-cicd); [CLI режиму друку](https://code.claude.com/docs/en/cli-reference), [Запускна верифікація](https://code.claude.com/docs/en/best-practices)

---
**Локалізація**: [Serhii (MacPlus Software)](https://macplus-software.com)
*Остання синхронізація: Травень 2026*
