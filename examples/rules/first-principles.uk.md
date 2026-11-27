---
description: "Шаблон інваріантів сесії: жорсткі обмеження, порогові значення якості та антипатерни, яких Claude має дотримуватися протягом усієї сесії"
---

# Перші принципи: інваріанти сесії

Це шаблон для шару «Контракт» у ваших правилах Claude Code. Це обмеження, які мають залишатися чинними протягом усієї сесії, незалежно від того, яке завдання активне і скільки контексту накопичилося.

Налаштуйте розділи нижче відповідно до стандартів своєї команди. Замініть значення з прикладів власними пороговими значеннями.

> **Чому це важливо**: зі зростанням контексту розмови ранні інструкції втрачають вплив на поведінку Claude. Це називають «розпадом контексту» (context decay). Інваріанти сесії, розміщені в CLAUDE.md або у файлах правил, діють як якорі стиснення, що протистоять цьому розпаду, бо вони впроваджуються на початку кожного context window.

## Жорсткі обмеження

Ці правила ніколи не мають винятків. Якщо Claude ось-ось порушить одне з них, він мусить зупинитися й повідомити про конфлікт, а не продовжувати.

```markdown
# Hard Constraints (never-break rules)

## Data Safety
- Never delete production data without explicit user confirmation in the same message
- Never store secrets (API keys, passwords, tokens) in code files or commit them
- Never run DROP, TRUNCATE, or DELETE without WHERE on production databases

## Code Safety
- Never disable TypeScript strict mode or ESLint rules to make code compile
- Never catch errors silently (empty catch blocks, swallowed promises)
- Never use `any` type in TypeScript except in test fixtures

## Process Safety
- Never force-push to main/master
- Never skip pre-commit hooks (no --no-verify)
- Never amend a commit that has been pushed to a shared branch

## Scope Safety
- Never modify files outside the directories specified in the current task
- Never add dependencies without stating the reason and checking bundle size impact
- Never refactor code that isn't part of the current task (note it for later instead)
```

## Порогові значення якості

Порогові значення кращі за розмиті прикметники. «Добре покриття» для різних людей означає різне; «80% покриття рядків» однозначне. Визначте свої числа тут.

```markdown
# Quality Thresholds

## Testing
- Minimum test coverage: 80% line coverage for new code
- Every public function must have at least one test
- Every bug fix must include a regression test
- Integration tests required for any endpoint that touches the database

## Performance
- API response time: p95 < 200ms for read endpoints, < 500ms for writes
- Bundle size: Total JS < 250KB gzipped (check with `npx bundlesize`)
- No N+1 queries (use DataLoader or equivalent for batch fetching)
- Database queries: no query > 100ms in development (enable slow query log)

## Code Quality
- Cyclomatic complexity: no function > 15 (enforce via ESLint rule)
- File length: no file > 400 lines (split when approaching limit)
- Function length: no function > 50 lines
- Nesting depth: no code > 4 levels of indentation

## Dependencies
- No dependency with known critical CVE
- No dependency abandoned > 2 years (check last publish date)
- Maximum 3 direct dependencies per feature module
```

## Інваріанти воркфлоу

Процесні обмеження, що забезпечують узгодженість протягом сесії, особливо під час перемикання між завданнями або коли залучено субагентів.

```markdown
# Workflow Invariants

## Commit Discipline
- Every commit must pass all existing tests before being created
- Commit messages follow Conventional Commits format (feat:, fix:, docs:, etc.)
- One logical change per commit (don't mix refactor with feature)

## Review Before Action
- Read a file before modifying it (no blind edits)
- Run tests after every significant change (not just at the end)
- Verify imports after adding/removing dependencies

## Communication
- When uncertain between two approaches, present both with trade-offs (don't pick silently)
- When a task will take more than 5 tool calls, outline the plan first
- When hitting an unexpected error, diagnose before retrying
```

## Антипатерни, які треба виявляти

Патерни, які Claude має позначати, коли натрапляє на них у кодовій базі або у власному виводі. Вони працюють як правила автоматизованого рев'ю коду, але для поведінки AI під час сесії.

```markdown
# Anti-Patterns to Detect

## Code Smells to Flag
- God objects: classes with >10 public methods or >5 injected dependencies
- Feature envy: a function that references another module's internals more than its own
- Primitive obsession: passing >3 related primitives instead of a typed object
- Temporal coupling: functions that must be called in a specific order without enforcement

## Process Smells to Flag
- Yak shaving: spending >3 tool calls on something tangential to the task
- Gold plating: adding features, abstractions, or error handling not requested
- Shotgun surgery: a single change requiring edits in >5 files (suggests missing abstraction)
- Copy-paste programming: duplicating >5 lines instead of extracting a function

## AI-Specific Anti-Patterns
- Hallucinated APIs: calling a method that doesn't exist in the current version
- Stale context: referencing file contents from earlier in the conversation that may have changed
- Over-apology: spending tokens on apologies instead of fixing the issue
- Premature optimization: adding caching, lazy loading, or memoization without evidence of a perf problem
```

## Протидія розпаду контексту

Три практичні стратегії, щоб ці інваріанти залишалися ефективними в довгих сесіях:

1. **Розміщуйте в CLAUDE.md**: правила з CLAUDE.md впроваджуються на початку кожного context window і переживають автокомпакцію. Це найсильніша позиція для інваріантів.

2. **Використовуйте файли правил для обмежень конкретних галузей**: пороги тестування винесіть у `.claude/rules/testing.md`, правила безпеки — у `.claude/rules/security.md`. Вони завантажуються разом із CLAUDE.md, але кожен файл лишається сфокусованим.

3. **Патерн hook із LEARNINGS.md**: налаштуйте hook, який впроваджує накопичені в сесії висновки в субагентів, щоб обмеження, виявлені посеред сесії, поширювалися на делеговану роботу:

```json
// .claude/settings.json (hooks section)
{
  "hooks": {
    "PreToolUse": [{
      "matcher": "Task",
      "command": "cat .claude/LEARNINGS.md 2>/dev/null || true"
    }]
  }
}
```

Це гарантує, що коли Claude запускає субагентів через інструмент Task, вони отримують ті самі специфічні для сесії висновки й обмеження.

---

**Джерела**:
- Тришарова модель контексту (Contract / Working Set / Noise): codeaholicguy.com (лютий 2026)
- CLAUDE.md як «якорі стиснення контексту»: Craig Johnston (imti.co)
- Патерн «Пороги, а не відчуття» (thresholds, not vibes): конкретні числа замість розмитих прикметників
- Патерн hook із LEARNINGS.md: практика спільноти для передавання контексту субагентам
