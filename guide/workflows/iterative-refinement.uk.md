---
title: "Iterative Refinement"
description: "Prompt, observe, and reprompt until satisfied — the core loop of AI-assisted development"
tags: [workflow, guide, design-patterns]
---

# Iterative Refinement

> **Confidence**: Tier 2 — Перевірений патерн, який спостерігається у багатьох користувачів Claude Code.

Написання промпту, спостереження, повторне коригування (reprompt) до отримання задовільного результату. Це основний цикл (core loop) ефективної розробки з використанням штучного інтелекту.

---

## Table of Contents

1. [TL;DR](#tldr)
2. [The Loop](#the-loop)
3. [Feedback Patterns](#feedback-patterns)
4. [Autonomous Loops](#autonomous-loops)
5. [Integration with Claude Code](#integration-with-claude-code)
6. [Script Generation Workflow](#script-generation-workflow)
7. [Iteration Strategies](#iteration-strategies)
8. [Anti-Patterns](#anti-patterns)
9. [Community Patterns & Known Limitations](#community-patterns--known-limitations)
10. [See Also](#see-also)

---

## TL;DR

```
1. Initial prompt with clear goal
2. Claude produces output
3. Evaluate against criteria
4. Specific feedback: "Change X because Y"
5. Repeat until done
```

Ключовий висновок: **Конкретний зворотний зв'язок > розмитий зворотний зв'язок**

---

## The Loop

### Step 1: Initial Prompt

Почніть із чіткого наміру та обмежень:

```
Create a React component for a user profile card.
- Show avatar, name, bio
- Include edit button
- Use Tailwind CSS
- Mobile-responsive
```

### Step 2: Evaluate Output

Claude генерує код. Оцініть його:
- Чи відповідає він вимогам?
- Чого не вистачає?
- Що зроблено неправильно?
- Що можна покращити?

### Step 3: Specific Feedback

Надайте точкові виправлення:

```
Good start. Changes needed:
1. Avatar should be circular, not square
2. Edit button should only show for own profile (add isOwner prop)
3. Bio should truncate after 3 lines with "Show more"
```

### Step 4: Repeat

Продовжуйте до отримання задовільного результату:

```
Better. One more thing:
- Add loading skeleton state for when data is fetching
```

---

## Feedback Patterns

### Effective Feedback

| Pattern | Example |
|---------|---------|
| **Specific location** | "Line 23: change `===` to `==`" |
| **Clear action** | "Add error boundary around the form" |
| **Reason given** | "Remove the console.log because it leaks user data" |
| **Priority marked** | "Critical: fix the SQL injection. Nice-to-have: add pagination." |

### Ineffective Feedback

| Anti-Pattern | Why It Fails | Better Alternative |
|--------------|--------------|-------------------|
| "Make it better" | Відсутність напрямку | "Improve readability by extracting the validation logic" |
| "This is wrong" | Немає конкретики | "The date format should be ISO 8601, not Unix timestamp" |
| "I don't like it" | Суб'єктивність | "Use functional components instead of class components" |
| "Fix the bugs" | Занадто розмито | "Fix: 1) null check on line 12, 2) off-by-one in loop" |

---

## Autonomous Loops

Claude може ітерувати самостійно, якщо задати йому чіткі критерії завершення.

### The Ralph Wiggum Pattern

Названий на честь патерна циклу самовдосконалення:

```
Keep improving the code quality until:
1. All tests pass
2. No TypeScript errors
3. ESLint shows zero warnings

After each iteration, run the checks and fix any issues.
Stop when all criteria are met.
```

### Completion Criteria Examples

```
Iterate until:
- Response time < 100ms for 95th percentile
- Test coverage > 80%
- All accessibility checks pass
- Bundle size < 200KB
```

### Iteration Limits

Завжди встановлюйте ліміти, щоб запобігти нескінченним циклам:

```
Improve the algorithm performance.
Maximum 5 iterations.
Stop early if improvement < 5% between iterations.
```

---

## Integration with Claude Code

### With Task Tool

Відстежуйте ітерації покращення за допомогою `TaskCreate` та `TaskUpdate`:

```
TaskCreate: "Implement initial version"
TaskCreate: "Fix: handle empty arrays"
TaskCreate: "Fix: add input validation"
TaskCreate: "Optimization: memoize expensive calculations"
# Mark completed as you progress with TaskUpdate
```

### With Hooks

Налаштуйте автоматичну валідацію після кожної зміни за допомогою Claude Code hooks (налаштовуються через команду `/hooks` або в `settings.json`). Наприклад, hook `PostToolUse` для інструменту `Edit` може автоматично запускати лінтинг та тести. Claude бачитиме помилки та зможе самостійно їх виправляти.

### With /compact

Коли контекст розростається під час ітерацій:

```
/compact

Continue refining the search algorithm.
We've made good progress, focus on the remaining issues.
```

### Checkpointing

Після досягнення значного прогресу:

```
Good progress. Let's checkpoint:
- Commit what we have
- List remaining issues
- Continue with the next priority
```

---

## Script Generation Workflow

Генерація скриптів та автоматизації дає найвищий рівень повернення інвестицій (ROI) для iterative refinement — за відгуками практиків економія часу становить 70-90%. Скрипти є автономними, їх легко тестувати ізольовано, і вони приносять негайну користь.

### The 3-7 Iteration Pattern

Більшість готових до продакшену скриптів з'являються після 3-7 ітерацій:

| Iteration | Focus | Prompt Pattern |
|-----------|-------|----------------|
| 1 | Базовий функціонал | "Create a script that [goal]" |
| 2-3 | Обмеження + крайні випадки | "Add [constraint]. Handle [edge case]." |
| 4-5 | Зміцнення (hardening) | "Add error handling, logging, input validation" |
| 6-7 | Фінальний лоск (polish) | "Optimize for [metric]. Add usage docs." |

### Example: Kubernetes Pod Manager (PowerShell)

**Iteration 1 — Базовий**
```
Create a PowerShell function to list pods in a Kubernetes namespace.
```

**Iteration 2 — Додавання фільтрації**
```
Add: filter by label selector and pod status.
Show: pod name, status, age, restarts.
```

**Iteration 3 — Додавання дій**
```
Add: ability to delete pods matching filter.
Require: confirmation before deletion.
```

**Iteration 4 — Обробка помилок**
```
Handle: kubectl not found, invalid namespace, permission denied.
Add: verbose logging with -Verbose flag.
```

**Iteration 5 — Готовий до продакшену**
```
Add: dry-run mode, output to JSON for piping, help documentation.
Ensure: works on Windows, Linux, macOS.
```

### Common Pitfalls

| Pitfall | Example | Mitigation |
|---------|---------|------------|
| Вигадані команди | `apt-get` на macOS | Вказуйте ОС: "Ubuntu 22.04 only" |
| Прогалини в безпеці | Немає валідації вводу | Завжди вимагайте: "validate all user inputs" |
| Надмірне ускладнення | Зайві бібліотеки | Вимагайте: "minimal dependencies, stdlib preferred" |
| Зсув контексту (drift) | Забування вимог на 5 ітерації | Промпт перевірки: "Recap current requirements before next change" |
| Припущення щодо платформи | Використання bash-фіч у sh | Вказуйте: "POSIX-compliant" або "bash 4+" |

### Script Iteration Template

```
Current script: [paste or reference]

Iteration goal: [specific improvement]

Constraints:
- Must preserve: [existing behavior to keep]
- Must not: [things to avoid]
- Target environment: [OS, shell, runtime]

Success criteria: [how to verify this iteration works]
```

---

## Iteration Strategies

### Breadth-First

Вирішуйте всі проблеми на одному рівні, перш ніж заглиблюватися:

```
First pass: Fix all type errors
Second pass: Fix all lint warnings
Third pass: Improve test coverage
Fourth pass: Optimize performance
```

### Depth-First

Повністю завершуйте одну область перед переходом до наступної:

```
1. Perfect the authentication flow (all aspects)
2. Then move to user management
3. Then move to settings
```

### Priority-Based

Працюйте в порядку важливості:

```
Iterate in this order:
1. Security issues (critical)
2. Data integrity bugs (high)
3. UX problems (medium)
4. Code style (low)
```

---

## Anti-Patterns

### Moving Target

```
# Wrong
"Actually, let's change the approach entirely..."
(Repeated 5 times)

# Right
Commit to an approach, iterate within it.
If approach is wrong, explicitly restart.
```

### Perfectionism Loop

```
# Wrong
Keep improving forever

# Right
Set clear "good enough" criteria:
- Tests pass
- Handles main use cases
- No critical issues
→ Ship it, improve later
```

### Lost Context

```
# Wrong
After 50 iterations, forget what the goal was

# Right
Periodically restate the goal:
"Reminder: we're building a rate limiter.
Current state: basic implementation works.
Next: add Redis backend."
```

---

## Review Auto-Correction Loop

Спеціалізований ітеративний патерн для рев'ю коду, де Claude перевіряє → виправляє → знову перевіряє до досягнення збіжності.

### Pattern

```
┌─────────────────────────────────────────┐
│   Review Auto-Correction Loop           │
│                                          │
│   Review (identify issues)               │
│        ↓                                 │
│   Fix (apply corrections)                │
│        ↓                                 │
│   Re-Review (verify fixes)               │
│        ↓                                 │
│   Converge (minimal changes) → Done      │
│        ↑                                 │
│   └──── Repeat (max iterations)     │
└─────────────────────────────────────────┘
```

### Prompt Template

```
Review this PR with auto-correction:
1. Multi-agent review (3 scope-focused agents)
2. Fix all 🔴 Must Fix issues
3. Re-review to verify fixes didn't introduce new issues
4. Fix all 🟡 Should Fix issues
5. Re-review one final time
6. Stop when only 🟢 Can Skip remain

Max iterations: 3
Stop early if iteration produces <5 lines changed
```

### Safeguards

| Safeguard | Purpose | Implementation |
|-----------|---------|----------------|
| **Max iterations** | Запобігання нескінченним циклам | Жорсткий ліміт: 3 ітерації |
| **Quality gates** | Гарантія валідності виправлень | Запуск `tsc && lint` перед кожною ітерацією |
| **Protected files** | Запобігання ризикованим змінам | Пропуск автовиправлення для: package.json, migrations, .env |
| **Change threshold** | Зупинка при досягненні збіжності | Вихід, якщо ітерація змінює <5 рядків |
| **Rollback capability** | Відновлення після невдалих змін | Git commit перед кожною ітерацією |

### Example Session

**Iteration 1: Initial Review**
```
Claude: Found 8 issues:
- 🔴 3 Must Fix (SQL injection, empty catch, missing auth)
- 🟡 4 Should Fix (DRY violations, N+1 query)
- 🟢 1 Can Skip (naming style)
```

**Iteration 2: Fix Must Fix + Re-Review**
```
Claude: Fixed 3 Must Fix issues.
Re-review: All 🔴 resolved. No new issues introduced.
Remaining: 4 🟡 Should Fix, 1 🟢 Can Skip
```

**Iteration 3: Fix Should Fix + Re-Review**
```
Claude: Fixed 4 Should Fix issues.
Re-review: All 🟡 resolved. No new issues.
Remaining: 1 🟢 Can Skip (optional improvement)
```

**Convergence**
```
Claude: Converged. Only optional improvements remain.
Changes this iteration: 2 lines (below threshold).
Review complete. ✅
```

### Comparison: One-Pass vs Convergence Loop

| Aspect | One-Pass Review | Convergence Loop |
|--------|-----------------|------------------|
| **Detection** | Знаходить усі проблеми один раз | Знаходить проблеми → виправляє → перевіряє → повторює |
| **Follow-up awareness** | Перевіряє git log на "Co-Authored-By: Claude" | Кожна ітерація враховує попередню |
| **False positives** | Може пропонувати виправлення для вже виправленого коду | Re-review виявляє це |
| **Confidence** | Одноразова валідація | Кілька проходів валідації |
| **Time cost** | Найшвидше (1 рев'ю) | Повільніше (3+ рев'ю) |
| **Quality** | Добре для досвідчених розробників | Краще для критично важливого коду |

**Коли використовувати**:
- **One-pass**: Прості PR, досвідчена команда, обмеження за часом
- **Convergence loop**: Критичний з точки зору безпеки код, молодші колеги в команді, велика відповідальність на продакшені

### Integration with Multi-Agent Review

Поєднуйте convergence loop з multi-agent review для максимальної якості:

```
Each iteration:
├─ Agent 1: Consistency Auditor
├─ Agent 2: SOLID Principles Analyst
└─ Agent 3: Defensive Code Auditor
     ↓
  Fix issues
     ↓
  Re-run 3 agents
     ↓
  Verify fixes + check for new issues
     ↓
  Repeat until convergence
```

### Convergence Criteria

Припиняйте ітерації, якщо виконується ХОЧА Б ОДНА з умов:

1. **Не залишилося жодної проблеми** (ідеальний результат)
2. **Досягнуто ліміту ітерацій** (за замовчуванням 3 ітерації)
3. **Поріг змін** (ітерація змінила <5 рядків коду)
4. **Помилка перевірки якості (Quality gate)** (`tsc`/`lint` завершується з помилкою після виправлення)
5. **Ручна зупинка** (користувач просить зупинити процес)

### Anti-Patterns in Review Loops

| Anti-Pattern | Problem | Solution |
|--------------|---------|----------|
| **Infinite loop** | Немає критеріїв збіжності | Встановіть max iterations + поріг змін |
| **Scope creep** | Кожна ітерація додає нові вимоги | Зафіксуйте межі (scope) перед запуском циклу |
| **Breaking fixes** | Виправлення вносить нові баги | Re-review після кожного виправлення + quality gates |
| **Protected file changes** | Зміна package.json, migrations | Явний список виключень для захищених файлів |
| **Context loss** | Забування початкових проблем на 3 ітерації | Ведіть трекер проблем між ітераціями |

---

## Example Session

### Initial Request
```
Create a debounce function in TypeScript.
```

### Iteration 1
```
Looks good. Add:
- Generic type support for any function signature
- Option to execute on leading edge
```

### Iteration 2
```
Better. Issues:
- The return type should preserve the original function's return type
- Add cancellation support
```

### Iteration 3
```
Almost there. Final polish:
- Add JSDoc comments
- Export the types separately
- Add unit tests
```

### Completion
```
Perfect. Commit this as "feat: add debounce utility with full TypeScript support"
```

---

## Community Patterns & Known Limitations

Спільнота побудувала кілька власних патернів поверх ітераційного циклу Claude Code. Деякі вирішують реальні проблеми, інші виявляють поточні обмеження, про які варто знати.

### Ralph Loop (Test-Driven Autonomous Iteration)

Джерело: nathanonn.com, Лютий 2026.

Ralph Loop обмежує автономне ітерування лише одним тест-кейсом за цикл, замість того щоб запускати весь набір тестів щоразу. Це дозволяє зосередитися на конкретній проблемі та заважає агенту намагатися виправити кілька різних помилок одночасно.

Як це працює:

1. Оберіть один тест, який не проходить
2. Виправте його, переконайтеся, що він проходить
3. Збережіть прогрес у JSON-файл стану
4. Перейдіть до наступного невдалого тесту
5. Після 3 невдалих спроб на одному тесті позначте його як `known_issue` та пропустіть

```json
{
  "current_case": "test_auth_token_refresh",
  "attempts": 2,
  "known_issues": ["test_legacy_migration_edge_case"],
  "completed": ["test_login", "test_logout", "test_session_timeout"]
}
```

Файл стану є головною інновацією тут. Він переживає скидання контексту, операції `/compact` і навіть повні перезапуски сесій. Агент зчитує файл на початку кожного циклу, щоб знати, де саме він зупинився, які кейси виконано, а які слід пропустити.

Ліміт у 3 спроби запобігає пастці нескінченного циклу, яка часто виникає в простих автономних циклах. Замість того щоб витрачати токени на впертий тест-кейс, асистент рухається далі та залишає цю проблему для подальшого аналізу людиною.

### Auto-Continue Skill

Джерело: mcpmarket.com.

Система продовження роботи на основі впевненості (confidence-based continuation), яка вирішує, чи має агент продовжувати роботу, чи йому слід зупинитися та запитати користувача. Замість фіксованої кількості ітерацій вона оцінює ситуацію після кожного циклу:

**Автоматично продовжує роботу, коли**:
- Тести проходять
- Збірка успішна
- Не виявлено нових типів помилок
- Показник впевненості (confidence score) залишається вище порогу

**Зупиняється для отримання вводу від людини, коли**:
- Впевненість падає нижче порогу
- З'являється нова категорія помилки (а не просто новий випадок уже відомої помилки)
- Збірка або типізація ламається у спосіб, якого агент раніше не бачив

Це чудово поєднується зі Stop hooks у Claude Code. Навичка може запускати перевірку після завдання і приймати рішення про продовження на основі її результатів.

### Stop Hooks for Automatic Verification

Патерн, який перетворює систему hook'ів Claude Code на автоматичний якісний бар'єр (quality gate) між ітераціями:

1. Claude завершує завдання (або ітерацію)
2. Hook `PostToolUse` для `TodoWrite` запускає скрипт перевірки
3. Скрипт запускає type-check, lint та тести
4. Помилки автоматично передаються назад до Claude
5. Claude виправляє проблеми без втручання людини

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "TodoWrite",
        "command": "bash -c 'npm run typecheck 2>&1; npm run lint 2>&1; npm test 2>&1'"
      }
    ]
  }
}
```

Hook спрацьовує щоразу, коли Claude позначає завдання як виконане. Якщо перевірка виявляє помилку, Claude бачить цей вивід і може самостійно виправити її перед переходом до наступного кроку.

### Escalation Strategy

Що робити, коли 3 ітерації поспіль зазнають невдачі на одній і тій самій проблемі. Замість того щоб крутитися у вічному циклі або просто здатися, використовуйте структурований шлях ескалації:

1. **Decompose** (Декомпозиція): Розбийте завдання, на якому виникла помилка, на 2-3 менші підзавдання, які можна вирішувати незалежно
2. **Collect context** (Збір контексту): Зберіть усі повідомлення про помилки, трасування стека та спроби виправлення у структурований файл
3. **Model escalation** (Ескалація моделі): Якщо ви використовуєте Sonnet, спробуйте запустити цей конкретний кейс на Opus для глибшого логічного аналізу
4. **Human escalation** (Ескалація до людини): Якщо оновлення моделі не допомогло, створіть GitHub issue з повним контекстом помилки та позначте завдання як `known_issue`

```bash
# Escalation in practice
if [ "$ATTEMPT_COUNT" -ge 3 ]; then
    # Collect context
    cat errors.log attempts.log > escalation-context.md

    # Try with Opus
    claude --model claude-opus-4-6 \
        "Fix this failing test. Context: $(cat escalation-context.md)"

    # If still failing, create issue
    if [ $? -ne 0 ]; then
        gh issue create \
            --title "Auto-escalation: $TEST_NAME fails after 3 attempts" \
            --body "$(cat escalation-context.md)" \
            --label "known_issue,needs-human"
    fi
fi
```

Мета полягає в тому, щоб ніколи мовчки не кидати роботу. Кожна невдача повинна бути або вирішена, або ескальована, або явно зафіксована для подальшого відстеження.

### Known Limitations

Відверто про те, що поки не працює, щоб ви не витрачали час на вигадування рішень, яких не існує.

**Немає вбудованої логіки повторних спроб, перевірки та відновлення (retry/verify/resume)** (GitHub issue #28489): У безголовій (headless) автоматизації Claude Code відсутня вбудована підтримка логіки повторних спроб, валідаційних бар'єрів та відновлення сесій. Кожна команда, яка впроваджує автономні цикли, створює власну версію цих рішень. Файли стану, перевірки на основі hook'ів та скрипти ескалації — все це обхідні шляхи, розроблені спільнотою для покриття цієї прогалини у платформі.

**Ітерації агента можуть бути втрачені** (GitHub issue #28843): У воркфлоу, що тривають кілька днів, ітерації агента та накопичений ними контекст можуть бути втрачені. Якщо ви запускаєте автоматизацію, яка охоплює кілька сесій або днів, зберігайте чіткі файли стану через кожні N ітерацій. Не покладайтеся на пам'ять розмов Claude як на єдине джерело істини.

**Крихкість багатоденних воркфлоу**: Довготривала автоматизація вимагає дисципліни створення точок відновлення (checkpointing). Зберігайте стан на диск (JSON-файли, git-комміти, коментарі в ішью) через регулярні інтервали. Правило просте, але про нього легко забути: якщо ви не можете відновити прогрес агента виключно з файлів на диску, ваш воркфлоу зламається на межі зміни сесій.

---

## See Also

- [exploration-workflow.uk.md](./exploration-workflow.uk.md) — Досліджуйте альтернативи перед ітераціями
- [tdd-with-claude.uk.md](./tdd-with-claude.uk.md) — TDD як ітераційне вдосконалення через тести
- [plan-driven.uk.md](./plan-driven.uk.md) — Плануйте перед початком ітерацій
- [../core/methodologies.md](../core/methodologies.uk.md) — Методологія ітераційних циклів (Iterative Loops)

---
**Локалізація**: [Serhii (MacPlus Software)](https://macplus-software.com)
*Остання синхронізація: Травень 2026*
