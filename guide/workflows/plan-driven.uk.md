---
title: "Plan-Driven Development"
description: "Use /plan mode for non-trivial tasks to explore and propose implementation plans"
tags: [workflow, guide, architecture]
---

# Plan-Driven Development

> **Confidence**: Tier 1 — Базується на вбудованому режимі `/plan` (Plan Mode) в Claude Code.

Використовуйте режим `/plan` (Plan Mode) для будь-яких нетривіальних завдань. Claude досліджує кодову базу (у режимі "тільки для читання"), а потім пропонує план реалізації на ваше затвердження.

---

## Table of Contents

1. [TL;DR](#tldr)
2. [The /plan Workflow](#the-plan-workflow)
3. [When to Use](#when-to-use)
4. [Plan File Structure](#plan-file-structure)
5. [Integration with Other Workflows](#integration-with-other-workflows)
6. [Tips](#tips)
7. [Advanced: Custom Markdown Plans (Boris Tane Pattern)](#advanced-custom-markdown-plans-boris-tane-pattern)
8. [See Also](#see-also)

---

## TL;DR

```
1. Enter Plan Mode (Shift+Tab twice) or ask complex question
2. Claude explores codebase (read-only)
3. Claude writes plan to .claude/plans/
4. You review and approve
5. Claude executes
```

---

## The /plan Workflow

### Step 1: Enter Plan Mode

Перемкніться у Plan Mode за допомогою клавіш `Shift+Tab` (натисніть двічі для перемикання по колу: Normal → Auto-Accept → Plan):
```
# Натисніть Shift+Tab двічі, щоб увійти в Plan Mode
# (В інтерфейсі з'явиться індикатор Plan Mode)
```

Або поставте складне запитання, яке автоматично активує Plan Mode:
```
How should I refactor the authentication system to support OAuth?
```

### Step 2: Claude Explores

У Plan Mode Claude:
- Читає відповідні файли
- Шукає патерни та шаблони
- Розуміє існуючу архітектуру
- НЕ МОЖЕ робити жодних змін у коді

### Step 3: Claude Writes Plan

Claude створює файл плану за шляхом `.claude/plans/[name].md`:

```markdown
# Plan: Refactor Authentication for OAuth

## Summary
Add OAuth support while maintaining existing email/password auth.

## Files to Modify
- src/auth/providers/index.ts (add OAuth provider)
- src/auth/middleware.ts (handle OAuth tokens)
- src/config/auth.ts (OAuth config)

## Files to Create
- src/auth/providers/oauth.ts
- src/auth/providers/google.ts

## Implementation Steps
1. Create OAuth provider interface
2. Implement Google OAuth provider
3. Update middleware to detect token type
4. Add OAuth routes
5. Update config schema

## Risks
- Breaking existing sessions during migration
- Token format differences between providers
```

### Step 4: You Review

Перевірте план за такими критеріями:
- Повнота (чи покриті всі вимоги)
- Правильність (чи правильний підхід обрано для вашої кодової бази)
- Обсяг роботи (scope) (чи немає тут надлишкового проєктування — over-engineering)

### Step 5: Approve and Execute

```
Looks good. Proceed with the plan.
```

Або вимагайте змін:
```
Modify the plan: also add support for GitHub OAuth, not just Google.
```

---

## When to Use

### Use Plan Mode

| Scenario | Why |
|----------|-----|
| Зміни у кількох файлах | Бачити всі задіяні файли заздалегідь |
| Архітектурні зміни | Перевірити підхід перед написанням коду |
| Нові фічі | Гарантувати повну та послідовну реалізацію |
| Незнайома кодова база | Дозволити Claude спочатку її дослідити |
| Ризиковані операції | Зробити рев'ю перед виконанням |

### Skip Plan Mode

| Scenario | Why |
|----------|-----|
| Однорядкові виправлення | Очевидні та мають низький ризик |
| Виправлення друкарських помилок | Планування не потрібне |
| Прості запитання | Дослідження, а не реалізація |
| Додавання коментарів | Тривіальні зміни |

---

## Plan File Structure

Плани зберігаються в каталозі `.claude/plans/` з автоматично згенерованими назвами.

### Typical Plan Sections

```markdown
# Plan: [Title]

## Summary
[1-2 sentence overview]

## Context
[Why this change is needed]

## Files to Modify
[List of existing files that will change]

## Files to Create
[List of new files]

## Files to Delete
[List of files to remove, if any]

## Implementation Steps
[Ordered list of steps]

## Testing Strategy
[How to verify the changes]

## Risks & Mitigations
[What could go wrong and how to handle it]

## Open Questions
[Things to clarify before proceeding]
```

---

## Integration with Other Workflows

### Plan + TDD

```
# Увійдіть у Plan Mode (натисніть Shift+Tab двічі), потім:

I need to implement a rate limiter.
Plan the test cases first, then the implementation.
```

Claude спланує і тести, і реалізацію у правильному для TDD порядку.

### Plan + Spec-First

```
# Увійдіть у Plan Mode (натисніть Shift+Tab двічі), потім:

Review the Payment Processing spec in CLAUDE.md.
Create an implementation plan that satisfies all acceptance criteria.
```

### Plan + Task Tool

Після затвердження плану Claude може розбити його на окремі завдання (tasks):

```
Approved. Create tasks from this plan and start implementing.
```

---

## Tips

### Be Specific About Scope

```
# Too vague (після входу в Plan Mode через подвійне натискання Shift+Tab)
Improve the API

# Better
Add pagination to the /users endpoint with cursor-based navigation.
Maintain backwards compatibility with existing clients.
```

### Request Plan Modifications

```
The plan looks good but:
- Add error handling for network failures
- Skip the caching optimization for now
- Include rollback procedure
```

### Use for Architecture Decisions

```
# Увійдіть у Plan Mode (натисніть Shift+Tab двічі), потім:

I'm considering two approaches for state management:
A) Redux Toolkit
B) Zustand

Explore the codebase and recommend which fits better.
```

### Save Plans for Documentation

Файли планів у `.claude/plans/` слугують документацією для прийнятих архітектурних рішень:
- Чому було обрано саме ці підходи
- Які файли мали змінитися
- Обґрунтування черговості реалізації

---

## Advanced: Custom Markdown Plans (Boris Tane Pattern)

> **Джерело**: Boris Tane, Engineering Lead у Cloudflare — ["How I use Claude Code"](https://boristane.com/blog/how-i-use-claude-code/) (Лютий 2026). 9 місяців використання у реальних проєктах (production).
> **Confidence**: Tier 2 — Патерн, перевірений практиками розробки, не є офіційною документацією Anthropic.

Коли стандартного Plan Mode недостатньо, застосовується ітеративне спільне планування розробником та агентом перед написанням будь-якого коду.

### Why Custom Plans Over /plan

| Factor | Plan Mode (native) | Custom .md plan |
|--------|----------------|-----------------|
| **Persistence** | Втрачається при стисканні контексту (/compact) | Зберігається на диску, можна ділитися |
| **Review surface** | Текстовий чат, лінійний вигляд | Структурований файл, підтримка diffs |
| **Iteration** | Обговорення туди-сюди у діалозі | Анотування файлу, повторний запуск |
| **Shared state** | Тільки на одну сесію | Спільний змінний стан між людиною та агентом |
| **Best for** | Стандартні фічі, завдання <30 хв | Складні фічі, великі архітектурні рішення |

**Правило вибору**: Використовуйте вбудований Plan Mode (Shift+Tab двічі) для завдань із відомими межами (scope). Використовуйте кастомні плани у форматі `.md`, коли ви очікуєте непорозумінь або хочете отримати чітке узгодження підходу перед написанням першого рядка коду.

---

### The Three-Phase Workflow

```
┌─────────────────────────────────────────────────────────────────┐
│  Phase 1: RESEARCH                                              │
│  → Emphatic prompt → research.md (written, not verbal)          │
├─────────────────────────────────────────────────────────────────┤
│  Phase 2: PLANNING (Annotation Cycle)                           │
│  → plan.md draft → human annotates → agent updates → repeat    │
│  → Exit: plan approved, no open questions                       │
├─────────────────────────────────────────────────────────────────┤
│  Phase 3: IMPLEMENTATION                                        │
│  → Mechanical execution, decisions already made                 │
└─────────────────────────────────────────────────────────────────┘
```

---

### Phase 1: Emphatic Research

Без додаткових вказівок Claude може досліджувати поверхово. Використовуйте переконливі, сильні слова, щоб змусити його зануритися глибше:

```
Research the authentication system in this codebase deeply.
Understand the intricacies of how sessions are managed, in great detail.
Cover edge cases, existing patterns, and any non-obvious dependencies.

Write your findings to research.md — do not implement anything.
```

**Чому це працює**: Слова "deeply", "in great detail", "intricacies" перемикають Claude з поверхневого сканування на ретельне дослідження. Результат обов'язково має бути записаний у файл — усні підсумки зникнуть під час стискання контексту (/compact).

**Файл research.md має містити**:
- Існуючі патерни та домовленості (conventions)
- Шляхи до файлів та ключові функції
- Неоочевидні залежності
- Виявлені обмеження та ризики

---

### Phase 2: The Annotation Cycle

Ядро патерна Бориса Тане. Ви ітеруєте над `plan.md` до повної готовності, **перед початком будь-кої реалізації**.

```
┌──────────────────────────────────────────────────────────────┐
│                    ANNOTATION CYCLE                           │
│                                                              │
│  Human prompt ──→ Agent writes plan.md                       │
│       ↑                    ↓                                 │
│  Annotate plan    Human reviews plan.md                      │
│  (add comments,          ↓                                   │
│   ask questions,   Issues found?                             │
│   flag trade-offs)       ├─ Yes → Annotate → loop           │
│                          └─ No  → Approved → Phase 3        │
│                                                              │
│  Typical: 1-6 iterations before approval                     │
└──────────────────────────────────────────────────────────────┘
```

**Запобіжний промпт** — завжди додавайте його, щоб уникнути передчасного написання коду:

```
Based on research.md, write a plan for implementing [feature].

Include: approach, affected file paths, code snippets for key decisions,
trade-offs considered, and open questions.

Write to plan.md. Do NOT implement anything yet.
```

**Що має містити plan.md**:

```markdown
# Plan: [Feature Name]

## Approach
[Strategy and rationale]

## Files Affected
- path/to/file.ts — what changes and why
- path/to/other.ts — what changes and why

## Key Implementation Details
[Code snippets for non-obvious parts — not the full implementation]

## Trade-offs
- Option A vs B: chose A because X
- Considered but rejected: Y (reason)

## Open Questions
- [ ] Should we handle edge case Z?
- [ ] Does this affect the mobile client?
```

**Приклад анотації**:

```markdown
## Approach
Use JWT tokens stored in httpOnly cookies.
<!-- Human annotation: ✓ Agreed. But also consider refresh token rotation -->

## Open Questions
- [ ] Should we handle token expiry in middleware?
<!-- Human annotation: Yes, centralize this — don't leave it to each route -->
```

**Критерії виходу** — план готовий, коли:
- Не залишилося відкритих питань
- Компроміси (trade-offs) задокументовані та узгоджені
- Шляхи до файлів конкретизовані (а не просто "якийсь файл авторизації")
- Ключові фрагменти коду (snippets) показують підхід наочно, а не просто описують його словами

> "Файл Markdown діє як спільний змінний стан між вами та агентом." — Boris Tane

---

### Phase 3: Mechanical Implementation

Після затвердження плану реалізація стає чисто механічним виконанням — творчих рішень більше не приймається.

```
Implement everything in plan.md.
Work through each item sequentially.
Mark tasks as completed as you go with [x].
Do not stop between tasks to ask for confirmation — keep going until done.
```

**Зворотний зв'язок під час реалізації**:
- Пишіть лаконічно: використовуйте короткі фрази або скріншоти замість довгих абзаців
- Рішення вже прийнято — перенаправляйте всі зміни меж завдань назад до `plan.md`
- Якщо виникає щось непередбачуване: зупиніться, оновіть `plan.md`, а потім продовжуйте

**Зміна мислення**: Фаза 3 є суто механічною. Уся розумова робота відбулася у Фазі 2.

---

### Complementary Techniques

| Technique | What | When |
|-----------|------|------|
| **Cherry-picking** | Реалізація підмножини з plan.md | План занадто великий, шипінг частинами |
| **Scope trimming** | Видалення пунктів із плану перед кодуванням | Зниження ризику, фокус на головному |
| **Reference-based guidance** | Посилання на існуючий код: "зроби як в auth.ts" | Забезпечення послідовності та стандартів |
| **Revert & re-scope** | `git revert` + перезапуск із вужчим планом | Реалізація пішла не так, чисте скидання стану |

---

## See Also

- [exploration-workflow.uk.md](./exploration-workflow.uk.md) — Досліджуйте альтернативи перед плануванням
- [../ultimate-guide.md](../ultimate-guide.md) — Розділ 2.3 Plan Mode
- [tdd-with-claude.uk.md](./tdd-with-claude.uk.md) — Поєднання з TDD
- [spec-first.uk.md](./spec-first.uk.md) — Поєднання зі Spec-First
- [iterative-refinement.uk.md](./iterative-refinement.uk.md) — Ітерації після розробки плану
- [task-management.uk.md](./task-management.uk.md) — Відстеження виконання плану між сесіями через Tasks API
- [dual-instance-planning.uk.md](./dual-instance-planning.uk.md) — Просунутий рівень: Використання двох інстансів Claude (планувальник + виконавець) для орієнтованих на якість воркфлоу

---
**Локалізація**: [Serhii (MacPlus Software)](https://macplus-software.com)
*Остання синхронізація: Травень 2026*
