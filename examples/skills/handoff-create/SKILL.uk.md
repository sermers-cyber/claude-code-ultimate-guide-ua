---
name: handoff-create
description: Створити структурований документ передачі (handoff) із поточної сесії. Фіксує обсяг, релевантні файли з номерами рядків, ключові відкриття, виконану роботу, поточний стан, наступні кроки та фрагменти коду. Використовуйте перед завершенням сесії або передачею роботи іншому агентові.
argument-hint: "[optional-filename]"
effort: low
disable-model-invocation: true
---

Створи структурований документ передачі з нашої поточної розмови й збережи його в `claudedocs/handoffs/handoff_YYYYMMDD_HHMMSS.md` (або використай ім'я файлу, передане як `$ARGUMENTS[0]`, якщо воно є).

Створи директорію `claudedocs/handoffs/`, якщо її не існує.

## Структура документа

Включи рівно ці розділи:

```markdown
# Handoff: [Task Name] - [YYYY-MM-DD HH:MM]

## Task

[One sentence: what is being accomplished]

## Scope

[In-scope behavior and exclusions. Include the contract revision, base commit and relevant working-tree state, acceptance criteria, applicable ADRs, blockers, permitted actions, and next owner. Mark unknowns explicitly.]

## Files

[All relevant files touched or needed. Format: `path/to/file:line` when a specific line matters]

- `src/auth/middleware.ts:45` - token validation logic
- `tests/auth.spec.ts` - test suite for this change
- `docs/api.md` - needs update after implementation

## Discoveries

[Key findings and insights from the work so far. Things the next agent needs to know that are not obvious from the code]

- [Discovery 1]
- [Discovery 2]

## Work Done

[Historical completion claims. Append-only: never remove prior entries. Include revisions, checks actually run, and evidence links when available.]

- [x] Task A completed (commit: abc1234)
- [x] Task B completed

## Status

[Last observed state and observation time: what is done, what remains, checks and their scope, blockers. Distinguish ticket state, run state, and acceptance.]

## Next Steps

[Actionable checklist of remaining tasks, in order]

1. [ ] Step 1
2. [ ] Step 2
3. [ ] Step 3

## Code

[Relevant code snippets with context. Focus on the parts a resuming agent needs to understand immediately]

\`\`\`typescript
// Key implementation detail
\`\`\`
```

## Правила

- Вклади загалом не більше 600 слів. Агент, що відновлює роботу, має змогу завантажити документ і продовжити за 30 секунд читання.
- Використовуй справжні шляхи й символи; додавай `:line` лише тоді, коли номер рядка перевірено на зафіксованій ревізії.
- Зроби handoff самодостатнім, не копіюючи розвідувальний транскрипт. Зберігай посилання на джерела й відрізняй спостереження від інтерпретації.
- Handoff фіксує наявну авторизацію; він не надає нових дозволів.
- «Work Done» лише доповнюється. Ніколи не видаляй попередні записи.
- Не включай повний git diff чи повний вміст файлів. Додавай лише ті фрагменти коду, що неочевидні.

Після збереження підтвердь шлях до файлу.
