---
title: "Iterative Refinement"
description: "Prompt, observe, and reprompt until satisfied: the core loop of AI-assisted development"
tags: [workflow, guide, design-patterns]
---

# Iterative refinement

> **Confidence**: Tier 2 (перевірений патерн, який спостерігається у багатьох користувачів Claude Code).

Написання промпту, спостереження, повторне коригування (reprompt) до отримання задовільного результату. Це основний цикл (core loop) ефективної розробки з використанням штучного інтелекту.

---

## Table of contents

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

## The loop

### Step 1: Initial prompt

Почніть із чіткого наміру та обмежень:

```
Create a React component for a user profile card.
- Show avatar, name, bio
- Include edit button
- Use Tailwind CSS
- Mobile-responsive
```

### Step 2: Evaluate output

Claude генерує код. Оцініть його:
- Чи відповідає він вимогам?
- Чого не вистачає?
- Що зроблено неправильно?
- Що можна покращити?

### Step 3: Specific feedback

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

## Feedback patterns

### Effective feedback

| Pattern | Example |
|---------|---------|
| **Specific location** | "Line 23: change `===` to `==`" |
| **Clear action** | "Add error boundary around the form" |
| **Reason given** | "Remove the console.log because it leaks user data" |
| **Priority marked** | "Critical: fix the SQL injection. Nice-to-have: add pagination." |

### Ineffective feedback

| Anti-Pattern | Why It Fails | Better Alternative |
|--------------|--------------|-------------------|
| "Make it better" | Відсутність напрямку | "Improve readability by extracting the validation logic" |
| "This is wrong" | Немає конкретики | "The date format should be ISO 8601, not Unix timestamp" |
| "I don't like it" | Суб'єктивність | "Use functional components instead of class components" |
| "Fix the bugs" | Занадто розмито | "Fix: 1) null check on line 12, 2) off-by-one in loop" |

---

## Autonomous loops

Claude може ітерувати самостійно, якщо задати йому чіткі критерії завершення.

### Choose what starts the next iteration

| Потреба | Механізм | Доказ завершення |
|---|---|---|
| Уточнити вимогу або оцінити дизайн | Ручний зворотний зв'язок | Людина приймає результат відповідно до сформульованої вимоги |
| Виконати обмежене, але перевірюване завдання за кілька ходів | `/goal` | Evaluator оцінює умову за доказами в розмові |
| Періодично перевіряти зовнішній стан | `/loop` | Кожна перевірка фіксує своє спостереження; скасування та завершення терміну дії не збігаються з прийняттям завдання |

Для ілюстративного виправлення бага спочатку визначте перевірку, яка падає через повідомлений дефект. Вкажіть, що та сама перевірка має проходити після виправлення, назвіть дозволені файли й вимагайте відповідні регресійні перевірки. Задайте ліміт ходів і вихід за відсутності прогресу, зберігаючи фінальні докази, якщо спрацює будь-який із них. Ліміт є прикладом політики, а не виміряним оптимумом чи доказом того, що evaluator примусово забезпечує жорсткий лічильник.

[Довідник goal](https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#goal-autonomous-completion-mode-v21139) пояснює обмеження evaluator і відновлення. [Посібник про цикли й графи](../core/loop-graph-engineering.uk.md#поєднуйте-повторюваний-тріаж-з-обмеженою-роботою) описує допуск із повторюваного тригера. Починайте з одного з цих механізмів; повторюваний prompt із вбудованою командою сам по собі не є перевіреною оркестрацією.

### The Ralph Wiggum pattern

Названий на честь патерна циклу самовдосконалення:

```
Keep improving the code quality until:
1. All tests pass
2. No TypeScript errors
3. ESLint shows zero warnings

After each iteration, run the checks and fix any issues.
Stop when all criteria are met.
```

### Completion criteria examples

```
Iterate until:
- Response time < 100ms for 95th percentile
- Test coverage > 80%
- All accessibility checks pass
- Bundle size < 200KB
```

### Iteration limits

Завжди встановлюйте ліміти, щоб запобігти нескінченним циклам:

```
Improve the algorithm performance.
Maximum 5 iterations.
Stop early if improvement < 5% between iterations.
```

---

## Integration with Claude Code

### With task tool

Відстежуйте ітерації покращення за допомогою `TaskCreate` та `TaskUpdate`:

```
TaskCreate: "Implement initial version"
TaskCreate: "Fix: handle empty arrays"
TaskCreate: "Fix: add input validation"
TaskCreate: "Optimization: memoize expensive calculations"
# Mark completed as you progress with TaskUpdate
```

### With hooks

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

## Script generation workflow

Генерація скриптів та автоматизації дає найвищий рівень повернення інвестицій (ROI) для iterative refinement: за відгуками практиків економія часу становить 70-90%. Скрипти є автономними, їх легко тестувати ізольовано, і вони приносять негайну користь.

### The 3-7 iteration pattern

Більшість готових до продакшену скриптів з'являються після 3-7 ітерацій:

| Iteration | Focus | Prompt Pattern |
|-----------|-------|----------------|
| 1 | Базовий функціонал | "Create a script that [goal]" |
| 2-3 | Обмеження + крайні випадки | "Add [constraint]. Handle [edge case]." |
| 4-5 | Зміцнення (hardening) | "Add error handling, logging, input validation" |
| 6-7 | Фінальний лоск (polish) | "Optimize for [metric]. Add usage docs." |

### Example: Kubernetes pod manager (PowerShell)

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

### Common pitfalls

| Pitfall | Example | Mitigation |
|---------|---------|------------|
| Вигадані команди | `apt-get` на macOS | Вказуйте ОС: "Ubuntu 22.04 only" |
| Прогалини в безпеці | Немає валідації вводу | Завжди вимагайте: "validate all user inputs" |
| Надмірне ускладнення | Зайві бібліотеки | Вимагайте: "minimal dependencies, stdlib preferred" |
| Зсув контексту (drift) | Забування вимог на 5 ітерації | Промпт перевірки: "Recap current requirements before next change" |
| Припущення щодо платформи | Використання bash-фіч у sh | Вказуйте: "POSIX-compliant" або "bash 4+" |

### Script iteration template

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

## Iteration strategies

### Breadth-first

Вирішуйте всі проблеми на одному рівні, перш ніж заглиблюватися:

```
First pass: Fix all type errors
Second pass: Fix all lint warnings
Third pass: Improve test coverage
Fourth pass: Optimize performance
```

### Depth-first

Повністю завершуйте одну область перед переходом до наступної:

```
1. Perfect the authentication flow (all aspects)
2. Then move to user management
3. Then move to settings
```

### Priority-based

Працюйте в порядку важливості:

```
Iterate in this order:
1. Security issues (critical)
2. Data integrity bugs (high)
3. UX problems (medium)
4. Code style (low)
```

---

## Anti-patterns

### Moving target

```
# Wrong
"Actually, let's change the approach entirely..."
(Repeated 5 times)

# Right
Commit to an approach, iterate within it.
If approach is wrong, explicitly restart.
```

### Perfectionism loop

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

### Lost context

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

## Review auto-correction loop

Спеціалізований ітеративний патерн, де Claude перевіряє, виправляє та повторно перевіряє в межах фіксованого бюджету. Прийняття вимагає доказів; зупинка циклу не доводить успіху.

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
│   Verify acceptance → Accepted          │
│        ↑                                 │
│        └──── Budget left? Repeat / Stop  │
└─────────────────────────────────────────┘
```

### Prompt template

```
Review this PR with auto-correction:
1. Multi-agent review (3 scope-focused agents)
2. Fix all 🔴 Must Fix issues
3. Re-review to verify fixes didn't introduce new issues
4. Fix all 🟡 Should Fix issues
5. Re-review one final time
6. Accept only when all blocking findings are resolved with evidence,
   required behavior checks pass on the current revision, and the
   designated reviewer accepts the result under the recorded criteria.

Max iterations: 3
Stop as EXHAUSTED when the budget is consumed without acceptance.
Stop as NO_PROGRESS after two passes resolve no blocking finding and
produce no new verification evidence. A small diff is not acceptance.
Keep FAILED, TIMEOUT, ABORTED and UNKNOWN distinct from acceptance.
```

### Safeguards

| Safeguard | Purpose | Implementation |
|-----------|---------|----------------|
| **Max iterations** | Запобігання нескінченним циклам | Жорсткий ліміт: 3 ітерації |
| **Quality gates** | Перевірка заданих властивостей | Після кожного виправлення запускайте перевірку типів проєкту, lint і відповідні тести поведінки; фіксуйте ревізію та результати |
| **Protected files** | Запобігання ризикованим змінам | Пропуск автовиправлення для: package.json, migrations, .env |
| **Progress check** | Обмеження непродуктивної роботи | Відстежуйте розв'язані блокувальні знахідки та нові докази перевірки; відсутність прогресу є причиною зупинки, а не прийняттям |
| **Recovery capability** | Збереження стану, який можна відновити | Зафіксуйте контрольну точку перед виправленнями; відкат коду не відновлює змінені дані чи зовнішні ефекти |

### Example session

Ілюстративна розмова, а не виміряний результат рев'ю. У реальному запуску кожне твердження про розв'язання потребує пов'язаної перевірки або арбітражу.

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

**Acceptance**
```
Claude: Required behavior checks pass on the recorded current revision.
Blocking findings have verified resolutions; the designated reviewer accepts.
Only explicitly deferred optional improvements remain.
Outcome: ACCEPTED within the stated criteria and evidence boundary.
```

### Comparison: One-Pass vs convergence loop

| Aspect | One-Pass Review | Convergence Loop |
|--------|-----------------|------------------|
| **Detection** | Одна можливість знайти проблеми | Знаходить проблеми → виправляє → перевіряє → повторює; обидва підходи можуть пропустити дефекти |
| **Follow-up awareness** | Перевіряє git log на "Co-Authored-By: Claude" | Кожна ітерація враховує попередню |
| **False positives** | Може пропонувати виправлення для вже виправленого коду | Re-review виявляє це |
| **Confidence** | Одноразова валідація | Кілька проходів валідації |
| **Time cost** | Найшвидше (1 рев'ю) | Повільніше (3+ рев'ю) |
| **Quality** | Потребує оцінювання результату | Потребує оцінювання результату; більша кількість проходів сама по собі не доводить покращення |

**Коли використовувати**:
- **One-pass**: Прості PR, досвідчена команда, обмеження за часом
- **Bounded loop**: зміни, що потребують кількох проходів виправлення; чутливі шляхи й надалі підпорядковуються політиці власника та затвердження

### Integration with multi-agent review

Призначайте рецензентам окремі зони відповідальності й оцінюйте їхні знахідки; саме додавання agent не забезпечує незалежності чи якості:

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
  Accept with evidence, or repeat within budget and stop with an explicit reason
```

### Convergence criteria

Фіксуйте прийняття окремо від виконання та причини зупинки:

1. **Прийнято**: потрібні перевірки проходять на зафіксованій ревізії, блокувальні знахідки мають перевірені рішення, а уповноважений рецензент приймає результат відповідно до чинних критеріїв. Це не доводить повноти самих критеріїв.
2. **Вичерпано або немає прогресу**: збережіть нерозв'язані знахідки та контрольні точки; не повідомляйте про завершення.
3. **Збій або тайм-аут**: збережіть невдалий етап і наявні докази; відсутні результати не означають чистого рев'ю.
4. **Перервано**: збережіть стан після санкціонованої зупинки.
5. **Невідомо**: не вдається встановити відповідальність, покриття чи результат; застосуйте шлях відновлення або ескалації, передбачений політикою.

Якщо рев'ю виявляє неповну вимогу, версіонуйте критерії з указанням причини та санкціонованого рішення, а потім повторно запустіть уражені перевірки. Не послаблюйте критерій мовчки, щоб дійти до зеленого результату. Див. [розподіл судження](../core/loop-graph-engineering.uk.md#5-розподіляйте-судження-явно).

### Anti-Patterns in review loops

| Anti-Pattern | Problem | Solution |
|--------------|---------|----------|
| **Infinite loop** | Немає обмежених умов зупинки | Задайте бюджети та перевірки прогресу незалежно від прийняття |
| **Scope creep** | Кожна ітерація мовчки змінює вимоги | Версіонуйте відкриття через призначений орган; визнавайте недійсним уражене прийняття |
| **Breaking fixes** | Виправлення вносить нові баги | Re-review після кожного виправлення + quality gates |
| **Protected file changes** | Зміна package.json, migrations | Явний список виключень для захищених файлів |
| **Context loss** | Забування початкових проблем на 3 ітерації | Ведіть трекер проблем між ітераціями |

---

## Example session

### Initial request
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

## Community patterns & known limitations

Спільнота побудувала кілька власних патернів поверх ітераційного циклу Claude Code. Деякі вирішують реальні проблеми, інші виявляють поточні обмеження, про які варто знати.

### Ralph loop (test-driven autonomous iteration)

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

### Auto-continue skill

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

### Stop hooks for automatic verification

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

### Escalation strategy

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
    claude --model claude-opus-5-5 \
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

### Known limitations

Відверто про те, що поки не працює, щоб ви не витрачали час на вигадування рішень, яких не існує.

**Відокремлюйте нативне продовження від контролю доставки**: `/goal` підтримує неінтерактивне виконання та відновлює активні цілі під час відновлення сесії. Його evaluator читає розмову, а не запускає незалежну перевірку. Класифікація повторних спроб, довговічні загальні бюджети, повноваження на прийняття та безпечне повторне відтворення зовнішніх ефектів усе ще потребують явного контракту. Звіряйтеся з [поточною документацією goal](https://code.claude.com/docs/en/goal), а не вважайте історичні повідомлення про проблеми загальною відсутністю підтримки повторних спроб, перевірки чи відновлення.

**Ітерації агента можуть бути втрачені** (GitHub issue #28843): У воркфлоу, що тривають кілька днів, ітерації агента та накопичений ними контекст можуть бути втрачені. Якщо ви запускаєте автоматизацію, яка охоплює кілька сесій або днів, зберігайте чіткі файли стану через кожні N ітерацій. Не покладайтеся на пам'ять розмов Claude як на єдине джерело істини.

**Крихкість багатоденних воркфлоу**: Довготривала автоматизація вимагає дисципліни створення точок відновлення (checkpointing). Зберігайте стан на диск (JSON-файли, git-комміти, коментарі в ішью) через регулярні інтервали. Правило просте, але про нього легко забути: якщо ви не можете відновити прогрес агента виключно з файлів на диску, ваш воркфлоу зламається на межі зміни сесій.

---

## See also

- [exploration-workflow.md](./exploration-workflow.uk.md): досліджуйте альтернативи перед ітераціями
- [tdd-with-claude.md](./tdd-with-claude.uk.md): TDD як ітераційне вдосконалення через тести
- [plan-driven.md](./plan-driven.uk.md): плануйте перед початком ітерацій
- [../core/methodologies.md](../core/methodologies.uk.md): методологія ітераційних циклів (Iterative Loops)

---
**Локалізація**: [Serhii (MacPlus Software)](https://macplus-software.com)
*Остання синхронізація: Травень 2026*
