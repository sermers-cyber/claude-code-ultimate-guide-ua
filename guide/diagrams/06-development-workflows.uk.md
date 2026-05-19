---
title: "Claude Code — Візуальні діаграми робочих процесів розробки"
description: "Цикл TDD, конвеєр спочатку-специфікація, робочий процес на основі плану, цикл ітераційного вдосконалення"
tags: [workflows, tdd, spec-first, plan-driven, iterative]
---

# Робочі процеси розробки

Перевірені патерни для структурування сесій розробки за допомогою AI.

---

### TDD Red-Green-Refactor з Claude

Розробка через тестування (TDD), адаптована для Claude Code: спочатку напишіть тест, що падає, а потім попросіть Claude реалізувати лише те, що необхідно для його проходження. Це запобігає надмірному ускладненню (over-engineering) та гарантує, що тести справді перевіряють поведінку.

```mermaid
flowchart TD
    A([Початок: Потрібна нова функція]) --> B(Написання тесту, що падає,<br/>разом із людиною)
    B --> C(Запуск тестів)
    C --> D{Тести падають<br/>як очікувалося?}
    D -->|No: tests pass<br/>before impl!| E(Fix test — це занадто слабко)
    E --> B
    D -->|Yes: RED ✓| F(Попросіть Claude впровадити<br/>мінімальний код для проходження)
    F --> G(Повторний запуск тестів)
    G --> H{Тести проходять?}
    H -->|No| I(Діагностика з Claude<br/>виправлення реалізації)
    I --> G
    H -->|Yes: GREEN ✓| J{Код потребує<br/>рефакторингу?}
    J -->|Yes| K(Рефакторинг з Claude)
    K --> L(Запуск тестів: усе ще green?)
    L -->|No| I
    L -->|Yes: REFACTOR ✓| M{Потрібні ще<br/>функції?}
    J -->|No| M
    M -->|Yes| B
    M -->|No| N([Функція готова ✓])

    style B fill:#E85D5D,color:#fff
    style F fill:#E85D5D,color:#fff
    style D fill:#E87E2F,color:#fff
    style H fill:#E87E2F,color:#fff
    style J fill:#E87E2F,color:#fff
    style G fill:#7BC47F,color:#333
    style K fill:#6DB3F2,color:#fff
    style N fill:#7BC47F,color:#333

    click A href "https://github.com/gerasimsergey/claude-code-ultimate-guide-ua/blob/main/guide/workflows/tdd-with-claude.md" "TDD — Нова функція"
    click B href "https://github.com/gerasimsergey/claude-code-ultimate-guide-ua/blob/main/guide/workflows/tdd-with-claude.md" "Написання тесту, що падає (RED)"
    click C href "https://github.com/gerasimsergey/claude-code-ultimate-guide-ua/blob/main/guide/workflows/tdd-with-claude.md" "Запуск тестів"
    click D href "https://github.com/gerasimsergey/claude-code-ultimate-guide-ua/blob/main/guide/workflows/tdd-with-claude.md" "Тести падають як очікувалося?"
    click E href "https://github.com/gerasimsergey/claude-code-ultimate-guide-ua/blob/main/guide/workflows/tdd-with-claude.md" "Виправте тест — занадто слабкий"
    click F href "https://github.com/gerasimsergey/claude-code-ultimate-guide-ua/blob/main/guide/workflows/tdd-with-claude.md" "Claude впроваджує мінімальний код"
    click G href "https://github.com/gerasimsergey/claude-code-ultimate-guide-ua/blob/main/guide/workflows/tdd-with-claude.md" "Повторний запуск тестів"
    click H href "https://github.com/gerasimsergey/claude-code-ultimate-guide-ua/blob/main/guide/workflows/tdd-with-claude.md" "Тести проходять? (GREEN)"
    click I href "https://github.com/gerasimsergey/claude-code-ultimate-guide-ua/blob/main/guide/workflows/tdd-with-claude.md" "Діагностика з Claude"
    click J href "https://github.com/gerasimsergey/claude-code-ultimate-guide-ua/blob/main/guide/workflows/tdd-with-claude.md" "Код потребує рефакторингу?"
    click K href "https://github.com/gerasimsergey/claude-code-ultimate-guide-ua/blob/main/guide/workflows/tdd-with-claude.md" "Рефакторинг з Claude"
    click L href "https://github.com/gerasimsergey/claude-code-ultimate-guide-ua/blob/main/guide/workflows/tdd-with-claude.md" "Запуск тестів: усе ще green?"
    click M href "https://github.com/gerasimsergey/claude-code-ultimate-guide-ua/blob/main/guide/workflows/tdd-with-claude.md" "Потрібні ще функції?"
    click N href "https://github.com/gerasimsergey/claude-code-ultimate-guide-ua/blob/main/guide/workflows/tdd-with-claude.md" "Функція готова ✓"
```

<details>
<summary>ASCII версія</summary>

```
Написання тесту, що падає (RED)
        │
    Run tests
        │
  Падають як очікувалося?
  ├─ No  → Виправити тест (занадто слабкий)
  └─ Yes → Попросити Claude: написати мін. код
                │
           Запуск тестів
                │
           Проходять? (GREEN)
           ├─ No  → Діагностика + виправлення
           └─ Yes → Рефакторинг?
                    ├─ Yes → Рефакторинг (REFACTOR) → перезапуск тестів
                    └─ No  → Наступна функція
```

</details>

> **Джерело**: [TDD з Claude](../workflows/tdd-with-claude.uk.md)

---

### Конвеєр розробки "Спочатку специфікація" (Spec-First)

Створюйте специфікацію перед кодом. Claude використовує spec-файл як єдине джерело істини — це запобігає розбіжностям між запланованим і фактично побудованим кодом.

```mermaid
flowchart LR
    A([Ідея / Вимога]) --> B(Написання spec.md<br/>природною мовою)
    B --> C(Claude переглядає специфікацію<br/>на чіткість + повноту)
    C --> D{Специфікація схвалена<br/> людиною?}
    D -->|No: gaps found| E(Вдосконалення специфікації<br/>усунення прогалин)
    E --> C
    D -->|Yes| F(Генерація тестів<br/>на основі специфікації)
    F --> G(Генерація реалізації<br/>на основі специфікації + тестів)
    G --> H(Запуск набору тестів)
    H --> I{Усі тести<br/>проходять?}
    I -->|No| J(Claude виправляє<br/>реалізацію)
    J --> H
    I -->|Yes| K(Перевірка людиною<br/>специфікація проти результату)
    K --> L{Відповідає<br/>специфікації?}
    L -->|No| M(Оновлення специфікації<br/>або реалізації)
    M --> K
    L -->|Yes| N([Merge ✓])

    style A fill:#F5E6D3,color:#333
    style B fill:#6DB3F2,color:#fff
    style D fill:#E87E2F,color:#fff
    style I fill:#E87E2F,color:#fff
    style L fill:#E87E2F,color:#fff
    style N fill:#7BC47F,color:#333

    click A href "https://github.com/gerasimsergey/claude-code-ultimate-guide-ua/blob/main/guide/workflows/spec-first.md" "Ідея / Вимога"
    click B href "https://github.com/gerasimsergey/claude-code-ultimate-guide-ua/blob/main/guide/workflows/spec-first.md" "Write spec.md"
    click C href "https://github.com/gerasimsergey/claude-code-ultimate-guide-ua/blob/main/guide/workflows/spec-first.md" "Claude reviews spec"
    click D href "https://github.com/gerasimsergey/claude-code-ultimate-guide-ua/blob/main/guide/workflows/spec-first.md" "Spec approved by human?"
    click E href "https://github.com/gerasimsergey/claude-code-ultimate-guide-ua/blob/main/guide/workflows/spec-first.md" "Refine spec"
    click F href "https://github.com/gerasimsergey/claude-code-ultimate-guide-ua/blob/main/guide/workflows/spec-first.md" "Generate tests from spec"
    click G href "https://github.com/gerasimsergey/claude-code-ultimate-guide-ua/blob/main/guide/workflows/spec-first.md" "Generate implementation"
    click H href "https://github.com/gerasimsergey/claude-code-ultimate-guide-ua/blob/main/guide/workflows/spec-first.md" "Run test suite"
    click I href "https://github.com/gerasimsergey/claude-code-ultimate-guide-ua/blob/main/guide/workflows/spec-first.md" "All tests pass?"
    click J href "https://github.com/gerasimsergey/claude-code-ultimate-guide-ua/blob/main/guide/workflows/spec-first.md" "Claude fixes implementation"
    click K href "https://github.com/gerasimsergey/claude-code-ultimate-guide-ua/blob/main/guide/workflows/spec-first.md" "Human review"
    click L href "https://github.com/gerasimsergey/claude-code-ultimate-guide-ua/blob/main/guide/workflows/spec-first.md" "Matches spec?"
    click M href "https://github.com/gerasimsergey/claude-code-ultimate-guide-ua/blob/main/guide/workflows/spec-first.md" "Update spec or implementation"
    click N href "https://github.com/gerasimsergey/claude-code-ultimate-guide-ua/blob/main/guide/workflows/spec-first.md" "Merge ✓"
```

<details>
<summary>ASCII версія</summary>

```
Ідея → Написання spec.md → Перегляд Claude
                             │
                       Схвалено? ─No→ Вдосконалити специфікацію
                             │ Yes
                       Згенерувати тести зі специфікації
                             │
                       Згенерувати реалізацію
                             │
                       Запуск тестів → Проходять? ─No→ Виправлення Claude
                             │ Yes
                       Перевірка людиною → Відповідає специфікації? ─No→ Виправити
                             │ Yes
                           Merge ✓
```

</details>

> **Джерело**: [Розробка спочатку специфікація (Spec-First)](../workflows/spec-first.uk.md)

---

### Робочий процес на основі плану з коментуванням (Plan-Driven)

Для складних завдань корисний режим планування (Plan Mode): Claude досліджує кодову базу, пропонує план, ви коментуєте його, і лише після цього Claude починає виконання схваленого плану. Це запобігає несподіванкам під час великих рефакторингів.

```mermaid
flowchart TD
    A([Дано складне завдання]) --> B(Вхід у Plan Mode<br/>Shift+Tab × 2)
    B --> C(Claude досліджує<br/>структуру кодової бази)
    C --> D(Claude пропонує план<br/>із списком файлів)
    D --> E(Людина переглядає план)
    E --> F{План<br/>прийнятний?}
    F -->|No: issues found| G(Людина коментує план<br/>робить виправлення)
    G --> H(Claude переглядає план)
    H --> E
    F -->|Yes| I(Схвалення плану<br/>Вихід з Plan Mode)
    I --> J(Claude виконує<br/>крок за кроком)
    J --> K(Claude звітує про<br/>прогрес)
    K --> L{Неочікувана<br/>проблема?}
    L -->|Yes| M(Claude позначає проблему<br/>запитує вказівки)
    M --> F
    L -->|No| N{Усі кроки<br/>завершені?}
    N -->|No| J
    N -->|Yes| O([Завдання виконано ✓])

    style A fill:#F5E6D3,color:#333
    style B fill:#6DB3F2,color:#fff
    style F fill:#E87E2F,color:#fff
    style L fill:#E87E2F,color:#fff
    style N fill:#E87E2F,color:#fff
    style G fill:#F5E6D3,color:#333
    style O fill:#7BC47F,color:#333

    click A href "https://github.com/gerasimsergey/claude-code-ultimate-guide-ua/blob/main/guide/workflows/plan-driven.md" "Дано складне завдання"
    click B href "https://github.com/gerasimsergey/claude-code-ultimate-guide-ua/blob/main/guide/ultimate-guide.md#23-plan-mode" "Enter Plan Mode"
    click C href "https://github.com/gerasimsergey/claude-code-ultimate-guide-ua/blob/main/guide/workflows/plan-driven.md" "Claude explores codebase"
    click D href "https://github.com/gerasimsergey/claude-code-ultimate-guide-ua/blob/main/guide/workflows/plan-driven.md" "Claude proposes plan"
    click E href "https://github.com/gerasimsergey/claude-code-ultimate-guide-ua/blob/main/guide/workflows/plan-driven.md" "Human reviews plan"
    click F href "https://github.com/gerasimsergey/claude-code-ultimate-guide-ua/blob/main/guide/workflows/plan-driven.md" "Plan acceptable?"
    click G href "https://github.com/gerasimsergey/claude-code-ultimate-guide-ua/blob/main/guide/workflows/plan-driven.md" "Human annotates plan"
    click H href "https://github.com/gerasimsergey/claude-code-ultimate-guide-ua/blob/main/guide/workflows/plan-driven.md" "Claude revises plan"
    click I href "https://github.com/gerasimsergey/claude-code-ultimate-guide-ua/blob/main/guide/ultimate-guide.md#23-plan-mode" "Approve plan — Exit Plan Mode"
    click J href "https://github.com/gerasimsergey/claude-code-ultimate-guide-ua/blob/main/guide/workflows/plan-driven.md" "Claude executes step by step"
    click K href "https://github.com/gerasimsergey/claude-code-ultimate-guide-ua/blob/main/guide/workflows/plan-driven.md" "Claude reports progress"
    click L href "https://github.com/gerasimsergey/claude-code-ultimate-guide-ua/blob/main/guide/workflows/plan-driven.md" "Unexpected issue?"
    click M href "https://github.com/gerasimsergey/claude-code-ultimate-guide-ua/blob/main/guide/workflows/plan-driven.md" "Claude flags issue"
    click N href "https://github.com/gerasimsergey/claude-code-ultimate-guide-ua/blob/main/guide/workflows/plan-driven.md" "All steps complete?"
    click O href "https://github.com/gerasimsergey/claude-code-ultimate-guide-ua/blob/main/guide/workflows/plan-driven.md" "Task done ✓"
```

<details>
<summary>ASCII версія</summary>

```
Складне завдання
     │
Plan Mode (Shift+Tab×2)
     │
Claude досліджує кодову базу
     │
Claude пропонує план
     │
Перевірка людиною ──No──► Коментарі + Claude переглядає ──► перегляд
     │ Yes
Схвалення + вихід з Plan Mode
     │
Claude виконує крок за кроком
     │
Неочікувано? ──Yes──► Позначити + запитати вказівки
     │ No
Готово? ──No──► продовжити
     │ Yes
Завершено ✓
```

</details>

> **Джерело**: [Робочий процес на основі плану](../workflows/plan-driven.uk.md)

---

### Цикл ітераційного вдосконалення

Результат рідко буває ідеальним з першої спроби. Цей цикл надає вам систематичний спосіб покращити результати за допомогою точкового зворотного зв'язку замість нечітких інструкцій на кшталт "зроби краще".

```mermaid
flowchart TD
    A([Початковий промпт]) --> B(Claude генерує результат)
    B --> C(Оцінка якості результату)
    C --> D{Достатньо<br/>добре?}
    D -->|Yes| E([Готово ✓])
    D -->|No| F(Визначення конкретної проблеми<br/>Що саме не так?)
    F --> G{Тип проблеми?}
    G -->|Стиль/тон| H(Додати: стильові обмеження)
    G -->|Бракує інформації| I(Додати: надати відсутній контекст)
    G -->|Неправильний підхід| J(Додати: перенаправити підхід)
    G -->|Задовгий/короткий| K(Додати: обмеження довжини)
    H --> L(Вдосконалення інструкції)
    I --> L
    J --> L
    K --> L
    L --> M(Claude вдосконалює результат)
    M --> N(Порівняння до/після)
    N --> O{Покращення<br/>виявлено?}
    O -->|Yes| C
    O -->|No| P(Потрібен інший<br/>підхід)
    P --> F

    style A fill:#F5E6D3,color:#333
    style D fill:#E87E2F,color:#fff
    style G fill:#E87E2F,color:#fff
    style O fill:#E87E2F,color:#fff
    style E fill:#7BC47F,color:#333
    style L fill:#6DB3F2,color:#fff
    style P fill:#E85D5D,color:#fff

    click A href "https://github.com/gerasimsergey/claude-code-ultimate-guide-ua/blob/main/guide/workflows/iterative-refinement.md" "Початковий промпт"
    click B href "https://github.com/gerasimsergey/claude-code-ultimate-guide-ua/blob/main/guide/workflows/iterative-refinement.md" "Claude generates output"
    click C href "https://github.com/gerasimsergey/claude-code-ultimate-guide-ua/blob/main/guide/workflows/iterative-refinement.md" "Evaluate output quality"
    click D href "https://github.com/gerasimsergey/claude-code-ultimate-guide-ua/blob/main/guide/workflows/iterative-refinement.md" "Good enough?"
    click E href "https://github.com/gerasimsergey/claude-code-ultimate-guide-ua/blob/main/guide/workflows/iterative-refinement.md" "Done ✓"
    click F href "https://github.com/gerasimsergey/claude-code-ultimate-guide-ua/blob/main/guide/workflows/iterative-refinement.md" "Identify specific issue"
    click G href "https://github.com/gerasimsergey/claude-code-ultimate-guide-ua/blob/main/guide/workflows/iterative-refinement.md" "Issue type?"
    click H href "https://github.com/gerasimsergey/claude-code-ultimate-guide-ua/blob/main/guide/workflows/iterative-refinement.md" "Add style constraints"
    click I href "https://github.com/gerasimsergey/claude-code-ultimate-guide-ua/blob/main/guide/workflows/iterative-refinement.md" "Provide missing context"
    click J href "https://github.com/gerasimsergey/claude-code-ultimate-guide-ua/blob/main/guide/workflows/iterative-refinement.md" "Redirect approach"
    click K href "https://github.com/gerasimsergey/claude-code-ultimate-guide-ua/blob/main/guide/workflows/iterative-refinement.md" "Add length constraint"
    click L href "https://github.com/gerasimsergey/claude-code-ultimate-guide-ua/blob/main/guide/workflows/iterative-refinement.md" "Refine instruction"
    click M href "https://github.com/gerasimsergey/claude-code-ultimate-guide-ua/blob/main/guide/workflows/iterative-refinement.md" "Claude refines output"
    click N href "https://github.com/gerasimsergey/claude-code-ultimate-guide-ua/blob/main/guide/workflows/iterative-refinement.md" "Compare before/after"
    click O href "https://github.com/gerasimsergey/claude-code-ultimate-guide-ua/blob/main/guide/workflows/iterative-refinement.md" "Improvement detected?"
    click P href "https://github.com/gerasimsergey/claude-code-ultimate-guide-ua/blob/main/guide/workflows/iterative-refinement.md" "Different approach needed"
```

<details>
<summary>ASCII версія</summary>

```
Промпт → Результат → Оцінка → Добре? ──Yes──► Готово
                                 │ No
                       Визначити конкретну проблему
                                 │
                          ┌──────┴──────────────┐
                         Стиль  Бракує  Неправ.  Довжина
                          └──────┬──────────────┘
                         Вдосконалити інструкцію
                                 │
                          Claude вдосконалює
                                 │
                         Краще? ──Yes──► Оцінити знову
                                 │ No
                          Інший підхід
```

</details>

> **Джерело**: [Ітераційне вдосконалення](../workflows/iterative-refinement.uk.md) — Рядок ~347

---

### AI Fluency — Шляхи високої проти низької адаптації (High vs Low Fluency)

Коли Claude генерує ідеально оформлений результат, спрацьовує когнітивне упередження: що більш завершеним здається результат, то менш критично оцінює його більшість користувачів. Це "Парадокс артефакту" (Artifact Paradox), задокументований Anthropic на основі 9 830 розмов. Ця схема демонструє, що відрізняє 30% високоадаптованих користувачів від 70% тих, хто бездумно приймає перші ж результати — та показує вимірювану різницю в якості результатів.

```mermaid
flowchart TD
    A([Користувач надсилає запит до Claude]) --> B(Claude генерує результат<br/>код · файл · конфігурація · план)
    B --> C["⚠️ Парадокс артефакту (Artifact Paradox)<br/>Візуально ідеальний результат викликає<br/>когнітивне упередження прийняття"]

    C -->|"70% користувачів"| D(Приймають перший результат<br/>без критичного перегляду)
    C -->|"30% користувачів"| E(Ітерують + задають питання<br/>визначають межі співпраці)

    D --> D1["Показники адаптації (Fluency) падають:<br/>−5.2 відс. п. виявлення прогалин<br/>−3.7 відс. п. перевірка фактів<br/>−3.1 відс. п. оскарження міркувань"]
    D1 --> D2([Приховані дефекти · пропущені вимоги])

    E --> E1("Оскаржують результат:<br/>'Що ти пропустив?<br/>Які припущення було зроблено?'")
    E1 --> E2(Виявляють прогалини<br/>Вдосконалюють із повним контекстом)
    E2 --> E3{Задоволені?}
    E3 -->|No — iterate again| E1
    E3 -->|Yes| E4([Перевірений, надійний результат ✓])

    E4 --> G["Виміряний вплив:<br/>в 5.6 разів більше виявлених проблем<br/>2.67 проти 1.33 середніх дій<br/>Джерело: Anthropic AI Fluency Index, 2026"]

    style A fill:#F5E6D3,color:#333
    style B fill:#E87E2F,color:#fff
    style C fill:#E85D5D,color:#fff
    style D fill:#E85D5D,color:#fff
    style D1 fill:#E85D5D,color:#fff
    style D2 fill:#E85D5D,color:#fff
    style E fill:#7BC47F,color:#333
    style E1 fill:#6DB3F2,color:#fff
    style E2 fill:#6DB3F2,color:#fff
    style E3 fill:#E87E2F,color:#fff
    style E4 fill:#7BC47F,color:#333
    style G fill:#7BC47F,color:#333

    click A href "https://www.anthropic.com/research/AI-fluency-index" "AI Fluency Index — Anthropic 2026"
    click B href "https://github.com/gerasimsergey/claude-code-ultimate-guide-ua/blob/main/guide/ultimate-guide.md#common-pitfalls--best-practices" "Claude generates output"
    click C href "https://www.anthropic.com/research/AI-fluency-index" "Artifact Paradox — Anthropic AI Fluency Index"
    click D href "https://github.com/gerasimsergey/claude-code-ultimate-guide-ua/blob/main/guide/ultimate-guide.md#common-pitfalls--best-practices" "Accept without review"
    click D1 href "https://www.anthropic.com/research/AI-fluency-index" "Fluency behaviors drop"
    click D2 href "https://github.com/gerasimsergey/claude-code-ultimate-guide-ua/blob/main/guide/ultimate-guide.md#common-pitfalls--best-practices" "Silent defects"
    click E href "https://github.com/gerasimsergey/claude-code-ultimate-guide-ua/blob/main/guide/ultimate-guide.md#23-plan-mode" "Iterate and question"
    click E1 href "https://github.com/gerasimsergey/claude-code-ultimate-guide-ua/blob/main/guide/ultimate-guide.md#rev-the-engine" "Challenge the output"
    click E2 href "https://github.com/gerasimsergey/claude-code-ultimate-guide-ua/blob/main/guide/workflows/iterative-refinement.md" "Identify gaps and refine"
    click E3 href "https://github.com/gerasimsergey/claude-code-ultimate-guide-ua/blob/main/guide/workflows/iterative-refinement.md" "Satisfied?"
    click E4 href "https://github.com/gerasimsergey/claude-code-ultimate-guide-ua/blob/main/guide/workflows/iterative-refinement.md" "Verified output"
    click G href "https://www.anthropic.com/research/AI-fluency-index" "Measured impact — AI Fluency Index"
```

<details>
<summary>ASCII версія</summary>

```
Запит користувача → Результат Claude (код · файл · конфігурація · план)
                        ↓
              ⚠️ Парадокс артефакту (Artifact Paradox)
          Ідеальний вигляд → когнітивне упередження
                        ↓
    ┌───────────────────┴──────────────────────┐
70% користувачів                         30% користувачів
Прийняття без перевірки              Ітерація + запитання
        ↓                                     ↓
Дії з перевірки (Fluency) падають:   Оскарження: "Що ти пропустив?
−5.2 відс. п. виявлення прогалин             Які припущення зробив?"
−3.7 відс. п. перевірка фактів                        ↓
−3.1 відс. п. оскарження міркувань   Виявлення прогалин → вдосконалення
        ↓                                     ↓
Приховані дефекти                    Задоволені? ──No──► ітерація
                                            ↓ Yes
                                     Перевірений результат ✓
                                            ↓
                                     в 5.6 разів більше виявлених проблем
                                     2.67 проти 1.33 середніх дій
```

</details>

> **Джерело**: [Anthropic AI Fluency Index](https://www.anthropic.com/research/AI-fluency-index) (Swanson et al., 2026-02-23) — [Розділ керівництва: Загальні помилки](../ultimate-guide.uk.md#common-pitfalls--best-practices)

---
**Локалізація**: [Serhii (MacPlus Software)](https://macplus-software.com)
*Остання синхронізація: Травень 2026*
