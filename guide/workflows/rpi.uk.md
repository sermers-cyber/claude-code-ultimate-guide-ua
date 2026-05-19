---
title: "RPI: Research → Plan → Implement"
description: "Трифазний патерн розробки функціоналу з чіткими етапами валідації між фазами"
tags: [workflow, architecture, design-patterns, validation]
---

# RPI: Research → Plan → Implement

> **Confidence**: Рівень 2 — Синтезовано на основі патернів виробничих команд. Структура на основі етапів узгоджується з рекомендаціями Anthropic щодо декомпозиції завдань для agents та керування agentic loop.

Створюйте функції в трьох заблокованих фазах: спочатку досліджуйте технічну можливість (Research), потім плануйте реалізацію (Plan), і лише після цього пишіть код (Implement). Кожна фаза створює конкретний артефакт. Кожен перехідний етап (gate) вимагає чіткого рішення GO перед початком наступної фази.

---

## Зміст

1. [Стисло (TL;DR)](#tldr)
2. [Коли використовувати RPI](#коли-використовувати-rpi)
3. [Як працюють етапи валідації (Gates)](#як-працюють-етапи-валідації-gates)
4. [Фаза 1: Research](#фаза-1-research)
5. [Фаза 2: Plan](#фаза-2-plan)
6. [Фаза 3: Implement](#фаза-3-implement)
7. [Шаблони Slash-команд](#шаблони-slash-команд)
8. [Практичний приклад](#практичний-приклад)
9. [Порівняння з іншими робочими процесами](#порівняння-з-іншими-робочими-процесами)
10. [Поради та вирішення проблем](#поради-та-вирішення-проблем)
11. [Дивіться також](#дивіться-також)

---

## TL;DR

```
Phase 1 — Research:
  Claude explores feasibility, surfaces risks, asks decision questions
  Output: RESEARCH.md
  Gate: You decide GO / NO-GO

Phase 2 — Plan:
  Claude writes architecture decisions, user stories, test plan
  Output: PLAN.md
  Gate: You approve the plan before any code is written

Phase 3 — Implement:
  Claude implements step by step, tests pass before each next step
  Output: working code + passing tests
  Gate: each implementation step validated before the next begins
```

**Найкраще підходить для**: функціоналу з незрозумілою технічною можливістю реалізації, обсягом роботи понад один день, невідомої технічної сфери або будь-чого, де пізнє виявлення помилкового припущення обходиться дорого.

---

## Коли використовувати RPI

### Використовуйте RPI, коли:

- **Технічна можливість невідома**: у вас є ідея, але ви не впевнені, чи її реально втілити технічно
- **Обсяг роботи великий**: реалізація займає більше одного дня
- **Вимоги є нечіткими**: ви знаєте бажаний результат, але не знаєте шляху до нього
- **Ризик неправильного напрямку високий**: безпека, платежі, міграції даних, інтеграції з зовнішніми системами
- **Ви вже стикалися з несподіванками раніше**: функція здавалася простою, а виявилася пов'язаною з 6 іншими системами

### Пропускайте RPI, коли:

| Сценарій | Кращий підхід |
|----------|----------------|
| Виправлення є очевидним (друкарська помилка, неправильний колір) | Безпосереднє редагування (Direct edit) |
| Функція добре зрозуміла, вимоги чіткі | [Spec-First](./spec-first.uk.md) або [dual-instance](./dual-instance-planning.uk.md) |
| Режим дослідження — ви ще самі не знаєте, чого хочете | Exploration workflow |
| Крихітна зміна, один файл | Просто зробіть це |

### Евристика прийняття рішень

Запитайте себе: «Якщо фаза дослідження виявить серйозну проблему, чи буду я радий, що не витратив 2 дні на її реалізацію спочатку?»

Якщо відповідь «так», запускайте RPI. Фаза дослідження зазвичай займає 30-60 хвилин і може заощадити багато годин роботи.

---

## Як працюють етапи валідації (Gates)

RPI має два людських етапи валідації (human gates) та один автоматизований етап на кожен крок реалізації.

```
[Idea]
   |
   v
[Phase 1: Research]
   |
   +- NO-GO -> Stop. Document why. Archive RESEARCH.md.
   |
   +- GO -------------------------------------------------------->
                                                                 |
                                                       [Phase 2: Plan]
                                                                 |
                                          +- Needs revision -> iterate with Claude
                                          |
                                          +- Approved -------------------------------->
                                                                                      |
                                                                          [Phase 3: Implement]
                                                                              Step 1 -> Test gate
                                                                              Step 2 -> Test gate
                                                                              Step 3 -> Test gate
                                                                                   |
                                                                                [Done]
```

**Gate 1 (після Research)**: Ви читаєте RESEARCH.md і приймаєте рішення GO/NO-GO. Це найважливіший етап — він повністю запобігає створенню неправильних речей.

**Gate 2 (після Plan)**: Ви перевіряєте PLAN.md перед тим, як писати будь-який код. Незначні виправлення вносяться тут із нульовими витратами часу на кодування.

**Етапи кроків (Step gates, під час Implement)**: кожен крок реалізації повинен мати успішно пройдені тести, перш ніж Claude перейде до наступного кроку. Процес автоматизований, втручання людини не потрібне, якщо крок не зазнає невдачі.

---

## Фаза 1: Research

### Що охоплює дослідження

Фаза дослідження відповідає на п'ять запитань:

1. **Що вже існує?** Відповідний код, бібліотеки, попередні спроби в кодовій базі.
2. **Що потрібно створити?** Межі обсягу роботи, компоненти, які потрібно створити або змінити.
3. **Які існують ризики?** Технічні ризики, безпека, інтеграція, продуктивність.
4. **Які точки прийняття рішень?** Архітектурні рішення, які впливають на весь план.
5. **Яка оцінка трудовитрат?** Приблизне визначення обсягу перед затвердженням плану.

Claude досліджує кодову базу, читає відповідні файли, перевіряє залежності та виявляє будь-які обмеження, що могли б змінити план. Результатом є RESEARCH.md.

### Початок дослідження

Створіть папку для функції та запустіть дослідження:

```bash
mkdir -p .claude/features/[feature-name]
```

Потім у Claude:

```
/rpi:research [feature description]
```

Або без slash-команди:

```
Run RPI Phase 1 (Research) for: [feature description]

Save output to .claude/features/[feature-name]/RESEARCH.md
Use Plan Mode to explore without modifying code.
```

### Шаблон RESEARCH.md

```markdown
# Research: [Feature Name]

**Date**: [YYYY-MM-DD]
**Requested**: [One-sentence description of the feature]
**Status**: PENDING DECISION

---

## What Exists Today

### Relevant Code
- [file path]: [what it does, why it matters]
- [file path]: [what it does, why it matters]

### Relevant Libraries
- [library]: [currently used / available / needs to be added]

### Prior Attempts or Related Work
- [any existing partial implementation, related PR, note in codebase]

---

## What Needs to Be Built

### New Files
- [file path]: [purpose]
- [file path]: [purpose]

### Files to Modify
- [file path]: [what changes, why]

### External Dependencies
- [dependency]: [reason needed, version constraint if any]

---

## Risks

| Risk | Likelihood | Impact | Notes |
|------|-----------|--------|-------|
| [risk description] | Low/Med/High | Low/Med/High | [mitigation or blocker] |

---

## Architecture Decision Points

Questions that need a decision before planning can start:

1. **[Decision]**: Option A (pros: X, cons: Y) vs Option B (pros: X, cons: Y)
2. **[Decision]**: [Options and trade-offs]

---

## Effort Estimate

- Research-to-plan: [time]
- Implementation: [time range]
- Testing: [time]
- **Total estimate**: [range]

**Confidence in estimate**: Low / Medium / High
**Why**: [reason for confidence level]

---

## Recommendation

[GO / NO-GO / NEEDS CLARIFICATION]

[1-3 sentences explaining the recommendation]

---

**Decision**: [ ] GO  [ ] NO-GO  [ ] NEEDS CLARIFICATION
**Notes**: [human fills this in]
```

### Як виглядає рішення NO-GO

Не кожна фаза дослідження закінчується рішенням GO. Поширені причини рішення NO-GO:

- **Технічний блокувальник**: зовнішній API не підтримує необхідну операцію.
- **Виявлено розширення меж проєкту (scope creep)**: «проста функція» вимагає переписування рівня авторизації.
- **Існує краща альтернатива**: дослідження виявляє наявну бібліотеку або зміну конфігурації, яка вирішує проблему простіше.
- **Наразі ризик занадто високий**: функція корисна, але обрано невідповідний час для її впровадження.

Архівуйте документи досліджень із рішенням NO-GO — вони є цінними записами про прийняті рішення та їх причини.

---

## Фаза 2: Plan

### Що охоплює план

Фаза 2 починається лише після того, як ви позначите RESEARCH.md рішенням GO. Claude читає документ дослідження та створює точний план реалізації (PLAN.md).

Хороший план є настільки конкретним, що інший інженер (або Claude у новій сесії) зможе виконати його без додаткових запитань.

```
/rpi:plan .claude/features/[feature-name]/RESEARCH.md
```

Або без slash-команди:

```
Run RPI Phase 2 (Plan) using:
- Research: .claude/features/[feature-name]/RESEARCH.md

Save output to .claude/features/[feature-name]/PLAN.md
Do not write any code yet. Plan only.
```

### Шаблон PLAN.md

```markdown
# Plan: [Feature Name]

**Date**: [YYYY-MM-DD]
**Research**: [link to RESEARCH.md]
**Estimated effort**: [from research]
**Risk level**: Low / Medium / High

---

## Summary

[2-4 sentences: what this implements, major design decisions taken, what it does NOT include]

---

## Architecture Decisions

[Record decisions made from the research decision points]

1. **[Decision]**: Chose [Option] because [reason]
2. **[Decision]**: Chose [Option] because [reason]

---

## Implementation Steps

Steps must be sequential and independently testable.

### Step 1: [Name]

**Files**: [list of files to create or modify]
**What to build**: [precise description]
**Test gate**: [specific test or check that must pass before Step 2 starts]

### Step 2: [Name]

**Files**: [list of files to create or modify]
**What to build**: [precise description]
**Test gate**: [specific test or check that must pass before Step 3 starts]

[...continue for all steps]

---

## Success Criteria

- [ ] [Testable criterion — describes observable behavior, not implementation]
- [ ] [Testable criterion]
- [ ] All step test gates pass

---

## Out of Scope

Explicitly list what this plan does NOT cover:
- [thing excluded]
- [thing excluded]

---

## Risks Accepted

[From RESEARCH.md risks, list which are accepted and how they're mitigated]

---

## Rollback Plan

If implementation fails mid-way:
- [what to undo]
- [how to restore previous state]

---

**Plan approved?** [ ] YES — proceed to implementation
**Revision notes**: [human fills this in if changes needed]
```

### Перевірка плану

Уважно прочитайте PLAN.md перед затвердженням. Мета полягає в тому, щоб виявити проблеми проєктування зараз, а не під час реалізації. Конкретні речі, які слід перевірити:

- Кроки реалізації (Implementation steps) розташовані у правильному порядку, без прихованих залежностей.
- Етапи тестування (Test gates) є конкретними та придатними для запуску (а не просто «виглядає правильно»).
- Межі проєкту (Out of scope) чітко визначені (це запобігає надмірному розширенню функціоналу з боку Claude).
- Існує план відкату (Rollback plan) для всього, що стосується даних або спільного стану.

Якщо план потребує змін, попросіть Claude переглянути його перед затвердженням. Це безкоштовно — доопрацювання після затвердження забере час реалізації.

---

## Фаза 3: Implement

### Патерн крокових етапів (Step-Gate)

Реалізація виконується крок за кроком. Кожен крок має свій етап тестування (test gate). Claude не починає наступний крок, поки не пройдено поточний етап.

```
/rpi:implement .claude/features/[feature-name]/PLAN.md
```

Або без slash-команди:

```
Run RPI Phase 3 (Implement) using:
- Plan: .claude/features/[feature-name]/PLAN.md

Rules:
- Implement one step at a time
- After each step, run the test gate specified in the plan
- Do not start the next step until the test gate passes
- If a test gate fails, stop and report the failure — do not improvise a fix
- Commit after each step that passes its gate
```

### Що відбувається під час реалізації

Claude послідовно виконує кроки плану. Для кожного кроку:

1. Реалізує зазначені файли та зміни.
2. Запускає етап тестування (test gate) — юніт-тести, інтеграційну перевірку або ручну верифікацію.
3. Якщо етап пройдено: робить commit із повідомленням, що посилається на крок, та повідомляє про готовність до наступного кроку.
4. Якщо етап не пройдено: повідомляє про помилку, надає конкретні вихідні дані тесту та ймовірну причину. Не намагається виправляти, доки ви не підтвердите.

Патерн покрокових комітів (step-commit) дає вам чисту історію git, яка відображає план. Якщо щось піде не так на кроці 4, ви зможете без проблем повернутися до коміту кроку 3.

### Протокол збою на кроковому етапі (Step-Gate Failure Protocol)

Коли етап тестування кроку не проходить, Claude звітує:

```
Step [N] gate failed.

Gate: [what was supposed to pass]
Output:
[actual test output]

Likely cause: [Claude's diagnosis]
Options:
1. Fix: [specific change that would likely fix it]
2. Revise plan: [if the plan step itself has a flaw]
3. Stop and investigate: [if the failure reveals something unexpected]

Which should I do?
```

Рішення за вами. Claude не виправляє помилку автоматично, щоб продовжити роботу — саме так реалізації відхиляються від планів.

---

## Шаблони Slash-команд

Збережіть їх у `.claude/commands/`, щоб запускати кожну фазу безпосередньо.

### `/rpi:research`

Збережіть у `.claude/commands/rpi-research.md`:

```markdown
# RPI Phase 1: Research

Run feasibility research for the requested feature.

## Instructions

1. Enter Plan Mode (do not modify files during research)
2. Explore the codebase to answer these questions:
   - What already exists that's relevant?
   - What files will need to change or be created?
   - What are the technical risks?
   - What decisions need to be made before planning?
   - What is a rough effort estimate?
3. Save output to `.claude/features/$ARGUMENTS/RESEARCH.md` using the template below
4. End with a clear recommendation: GO, NO-GO, or NEEDS CLARIFICATION
5. Ask the user for their GO/NO-GO decision before proceeding

## Constraints

- Do NOT write any code
- Do NOT modify any files
- Do NOT start planning implementation steps
- If uncertain about scope, surface it as a decision point
```

### `/rpi:plan`

Збережіть у `.claude/commands/rpi-plan.md`:

```markdown
# RPI Phase 2: Plan

Create an implementation plan based on approved research.

## Pre-check

Before starting:
1. Read the RESEARCH.md file specified in $ARGUMENTS
2. Verify it has a GO decision marked
3. If no GO decision found, stop and ask the user to decide first

## Instructions

1. Read RESEARCH.md carefully
2. Create PLAN.md in the same feature folder
3. Architecture decisions: resolve all decision points from research
4. Implementation steps: each step must have a concrete test gate
5. Success criteria: observable, testable, not implementation-internal
6. Out-of-scope: explicit list of what this plan does NOT cover
7. Do NOT write any implementation code
8. After writing the plan, ask the user to review and approve

## Constraints

- Do NOT write implementation code
- Steps must be sequential and independently testable
- Test gates must be runnable commands or precise manual checks, not vague descriptions
- Each step should be achievable in a single focused session
```

### `/rpi:implement`

Збережіть у `.claude/commands/rpi-implement.md`:

```markdown
# RPI Phase 3: Implement

Implement the feature following an approved plan, one step at a time.

## Pre-check

Before starting:
1. Read the PLAN.md file specified in $ARGUMENTS
2. Verify it has an approval marked
3. If no approval found, stop and ask the user to approve first

## Instructions

For each step in the plan:
1. Read the step description carefully
2. Implement only what the step specifies — nothing more
3. Run the test gate exactly as written in the plan
4. If the gate passes:
   - Commit with message: "feat([feature]): step [N] — [step name]"
   - Announce step completion and readiness for next step
5. If the gate fails:
   - Report the exact failure output
   - Diagnose the likely cause
   - Present options (fix, revise plan, stop)
   - Wait for human decision before proceeding

## Constraints

- Never skip a test gate
- Never start the next step before the current gate passes
- Never modify files outside the scope of the current step
- If you encounter something unexpected that changes the plan, stop and report it
- Commit after each passing step — not at the end
```

---

## Практичний приклад

**Запит**: "Add rate limiting to the public API endpoints."

### Фаза 1: Результат дослідження (скорочено)

```markdown
# Research: API Rate Limiting

**Date**: 2026-03-12
**Status**: PENDING DECISION

## What Exists Today

- `src/middleware/` — has auth middleware, no rate limiting
- `package.json` — express-rate-limit not installed, redis available
- `src/routes/api.ts` — 14 public endpoints, unauthenticated routes mixed with authenticated ones

## What Needs to Be Built

- Rate limiter middleware for public endpoints
- Separate limits for authenticated vs unauthenticated users
- Redis store for distributed rate limiting (app runs on 3 instances)

## Risks

| Risk | Likelihood | Impact | Notes |
|------|-----------|--------|-------|
| Redis connection failure disables all API access | Low | High | Need fallback to in-memory if Redis unavailable |
| Rate limit too aggressive — breaks existing integrations | Medium | High | Need to survey current usage patterns first |

## Architecture Decision Points

1. **Library**: express-rate-limit (maintained, battle-tested) vs custom middleware
2. **Bypass for trusted IPs**: Allow internal services to bypass rate limiting?

## Effort Estimate

- Implementation: 2-4 hours
- Testing: 2 hours
- **Total**: 4-6 hours

**Recommendation**: GO — standard problem, good library options, main risk is Redis fallback which is solvable.
```

**Рішення людини**: GO. Використовувати express-rate-limit. Без IP bypass на цьому етапі.

### Фаза 2: План (скорочено)

```markdown
# Plan: API Rate Limiting

**Risk level**: Medium (shared Redis state, potential to block legitimate traffic)

## Architecture Decisions

1. Library: express-rate-limit with rate-limit-redis store
2. No IP bypass initially — revisit if internal service issues arise
3. Unauthenticated: 100 requests/15 minutes. Authenticated: 1000 requests/15 minutes.
4. Redis failure fallback: in-memory store (accepts single-instance inconsistency)

## Implementation Steps

### Step 1: Install dependencies and configure Redis store

**Files**: `package.json`, `src/config/rate-limit.ts`
**Test gate**: `npm install` completes, `src/config/rate-limit.ts` exports config without errors

### Step 2: Implement rate limiter middleware

**Files**: `src/middleware/rate-limit.ts`
**Test gate**: Unit test — limiter blocks 101st request from same IP within 15 minutes

### Step 3: Apply to routes

**Files**: `src/routes/api.ts`
**Test gate**: Integration test — unauthenticated route returns 429 after 100 requests; authenticated route does not

### Step 4: Add Redis fallback

**Files**: `src/config/rate-limit.ts`
**Test gate**: Test with Redis unavailable — API still responds (200, not 500), in-memory limiting active
```

**Огляд людиною**: Затверджено.

### Фаза 3: Реалізація

Claude реалізує крок 1, запускає етап перевірки (`npm install` + перевірка імпорту), робить коміт `feat(rate-limit): step 1 — dependencies and config`. Потім виконує крок 2, крок 3, крок 4 послідовно. Кожен коміт є чистим. Кожен етап тестування має бути успішно пройдений перед продовженням.

---

## Порівняння з іншими робочими процесами

| Робочий процес | Структура фаз | Людські етапи валідації | Найкраще підходить для |
|----------|----------------|------------|----------|
| **RPI** | Research + Plan + Implement | GO/NO-GO + затвердження плану | Невідома технічна можливість, >1 дня роботи, високий ризик хибного напрямку |
| **Dual-Instance** | Plan + Implement (окремі інстанси Claude) | Затвердження плану | Відомі функції, що потребують ретельного виконання, велика кількість специфікацій |
| **Spec-First** | Spec + Implement | Немає (специфікація є неявним етапом) | Дизайнерська робота, контракти API, узгодження роботи команди |
| **TDD** | Test-first + Implement | Немає (тести є єдиним етапом валідації) | Покриття тестами як рушій розробки, рефакторинг, інкрементальна поведінка |
| **Direct** | Немає | Немає | Прості зміни, очевидний обсяг роботи, менше 2 годин |

### RPI порівняно з Dual-Instance

Dual-instance розділяє планування та реалізацію на два інстанси Claude із суворим розподілом ролей. Це добре працює, коли ви вже точно знаєте, що створюєте, і хочете отримати високоякісний план. RPI додає фазу дослідження технічної можливості перед плануванням, що робить його кращим для неоднозначних запитів. Якщо у вас вже є чітка специфікація, пропустіть Research та використовуйте dual-instance або spec-first.

### RPI порівняно зі Spec-First

Spec-first орієнтований на проєктування: ви визначаєте, що має робити система, а потім Claude реалізує це. RPI орієнтований на реалізацію з етапами валідації: ви описуєте мету, Claude досліджує, як її досягти, а потім ви обоє узгоджуєте план перед тим, як торкатися коду. Використовуйте spec-first, коли дизайн зрозумілий. Використовуйте RPI, коли технічний шлях не визначений.

### RPI порівняно з Direct Coding

Для будь-вого завдання тривалістю менше 2 годин із чітким обсягом роботи просто попросіть Claude виконати його. RPI створює додаткові накладні витрати, які не виправдані для невеликих завдань. Тільки фаза дослідження займає 30-60 хвилин. Ці витрати окупаються на багатоденних функціях, де пізнє виявлення неправильного припущення коштує набагато дорожче.

---

## Поради та вирішення проблем

### Claude переходить безпосередньо до реалізації у фазі дослідження

**Проблема**: Claude починає писати код під час фази дослідження.

**Рішення**: явно використовуйте Plan Mode (Shift+Tab двічі) для фази дослідження. Додайте цей рядок у команду дослідження:

```
You are in Plan Mode. Do not modify files. Do not write implementation code.
Research only. Output goes to RESEARCH.md.
```

Або додайте до вашого CLAUDE.md:

```markdown
## RPI Rules
- /rpi:research runs in Plan Mode only — no file modifications
- /rpi:plan produces only PLAN.md — no implementation code
- /rpi:implement runs one step at a time, waits for test gate before next step
```

### Фаза дослідження триває занадто довго

**Проблема**: Claude досліджує всю кодову базу замість того, щоб зосередитися на важливому.

**Рішення**: чітко обмежте межі дослідження:

```
/rpi:research payment-processing

Focus area: src/payments/, src/routes/checkout.ts
Do not explore: frontend, auth, unrelated backend modules
Time budget: complete research in one session
```

### План містить занадто багато кроків

**Проблема**: PLAN.md містить 12 кроків, що робить реалізацію громіздкою.

**Рішення**: план, який містить понад 6-8 кроків, зазвичай потребує зменшення обсягу роботи, а не детальнішого дроблення кроків. Запитайте Claude:

```
The plan has too many steps. What is the minimal viable scope that delivers
the core value? Revise the plan to implement only that, with a clear
"Future work" section for the rest.
```

### Етапи тестування (Test Gates) є розмитими

**Проблема**: етап тестування кроку містить опис на кшталт «переконайтеся, що це працює» замість конкретної команди.

**Рішення**: відхиляйте нечіткі етапи перевірки перед затвердженням плану. Напишіть у відповідь:

```
Step 3's test gate is "verify rate limiting works." Make it specific:
what command do I run, and what output do I expect to see when it passes?
```

Хороший етап тестування (Test gate):

```
Test gate: `npm test src/middleware/rate-limit.test.ts` — all 4 tests pass
```

Поганий етап тестування:

```
Test gate: rate limiting is working correctly
```

### Етап тестування кроку постійно завершується збоєм

**Проблема**: етап тестування кроку 2 постійно зазнає невдачі навіть після спроб виправлення.

**Рішення**: два збої означають необхідність перегляду плану, а не подальших спроб виправлення.

```
Stop implementation. The Step 2 gate has failed twice.
Review the plan — is the test gate achievable given the Step 1 output?
Do we need to revise the plan before continuing?
```

---

## Структура файлів (File Structure Summary)

```
.claude/
└── features/
    └── [feature-name]/
        ├── RESEARCH.md     # Phase 1 output (human annotates GO/NO-GO)
        └── PLAN.md         # Phase 2 output (human annotates approval)

.claude/commands/
├── rpi-research.md         # /rpi:research slash command
├── rpi-plan.md             # /rpi:plan slash command
└── rpi-implement.md        # /rpi:implement slash command
```

Архівування завершених функцій:

```bash
mkdir -p .claude/features/_archive
mv .claude/features/payment-processing .claude/features/_archive/
```

Архів є корисним ресурсом для навчання: завершені файли RESEARCH.md та PLAN.md показують хід міркувань під час розробки попередніх функцій.

---

## Дивіться також

- [dual-instance-planning.uk.md](./dual-instance-planning.uk.md) — Двоінстансний патерн для реалізації з великою кількістю специфікацій
- [spec-first.uk.md](./spec-first.uk.md) — Робочий процес спочатку з дизайном (Design-first), що використовує CLAUDE.md як контракт
- [tdd-with-claude.uk.md](./tdd-with-claude.uk.md) — Поєднання з TDD для крокової реалізації на основі тестів
- [task-management.uk.md](./task-management.uk.md) — Керування багатофазними завданнями між сесіями
- **Основний посібник**: розділ «Advanced Patterns» — огляд патернів з кількома інстансами та плануванням

---
**Локалізація**: [Serhii (MacPlus Software)](https://macplus-software.com)
*Остання синхронізація: Травень 2026*
