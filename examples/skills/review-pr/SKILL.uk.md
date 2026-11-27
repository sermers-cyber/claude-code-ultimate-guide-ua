---
name: review-pr
description: Виконати всебічне рев'ю коду pull request
argument-hint: "[PR_number|URL]"
effort: high
disable-model-invocation: true
---

# Рев'ю pull request

Виконайте всебічне рев'ю коду pull request.

## Інструкції

1. Отримайте інформацію про PR: `gh pr view $ARGUMENTS --json title,body,files,additions,deletions`
2. Перегляньте кожен змінений файл
3. Надайте структурований відгук

## Чекліст рев'ю

### Якість коду
- [ ] Код читабельний і добре організований
- [ ] Функції відповідного розміру
- [ ] Немає дублювання коду
- [ ] Змістовні імена змінних/функцій

### Функціональність
- [ ] Логіка правильна
- [ ] Граничні випадки оброблено
- [ ] Обробка помилок вичерпна
- [ ] Немає очевидних багів

### Безпека
- [ ] Немає захардкожених секретів
- [ ] Є валідація вхідних даних
- [ ] Немає вразливостей до ін'єкцій
- [ ] Перевірки авторизації на місці

### Тестування
- [ ] Для нового коду додано тести
- [ ] Наявні тести досі проходять
- [ ] Граничні випадки протестовано

### Документація
- [ ] Код самодокументований або прокоментований
- [ ] README оновлено за потреби
- [ ] Зміни API задокументовано

## Формат виводу

```markdown
## PR Review: #[number] - [title]

### Summary
[1-2 sentence overview]

### Approval Status
[ ] Approved
[ ] Approved with suggestions
[ ] Changes requested

### Findings

#### Critical (Must Fix)
- [ ] [Issue description] - `file:line`

#### Suggestions (Should Consider)
- [ ] [Improvement] - `file:line`

#### Nitpicks (Optional)
- [ ] [Minor suggestion] - `file:line`

### Positive Highlights
- [What's done well]

### Questions
- [Clarifications needed]
```

## Використання

```
/review-pr 123
/review-pr https://github.com/owner/repo/pull/123
```

---

## Розширене: Multi-Agent рев'ю

Для рев'ю продакшен-рівня, що потребують спеціалізованих поглядів і захисту від галюцинацій.

### Попередня перевірка

Перед рев'ю перевірте, чи це повторний прохід, щоб не повторювати пропозиції:

```bash
# Detect if Claude already reviewed this PR
git log --oneline -10 | grep "Co-Authored-By: Claude"
```

Якщо виявлено, зазначте: "Схоже, це повторний прохід. Зосереджуся на нових проблемах і не повторюватиму попередні пропозиції."

### Виявлення дрейфу обсягу

Звіряйте diff PR з початковим планом, щоб виловити ненавмисні зміни.

```bash
# Detect current branch
BRANCH=$(git branch --show-current)

# Search for a plan file associated with this branch
ls ~/.claude/plans/ 2>/dev/null | grep -i "$BRANCH" | head -3

# Files actually changed in this PR
git diff --stat origin/main...HEAD | head -30
```

Якщо для цієї гілки існує файл плану:
1. Прочитайте файл плану: який обсяг було заявлено?
2. Порівняйте заявлений обсяг із фактичним `git diff --stat`
3. Позначте змінені файли, які НЕ згадувалися в плані

Формат виводу:
```
SCOPE DRIFT CHECK
─────────────────────────────────────────
Plan scope:    [what the plan said would change]
Actual diff:   [files actually changed]
Drift:         [files changed outside plan scope, if any]
Verdict:       IN SCOPE / DRIFT DETECTED
```

Якщо файлу плану немає: зазначте "Файл плану для цієї гілки не знайдено, перевірку дрейфу обсягу пропущено."

### Multi-agent спеціалізація

Запустіть 3 паралельні спеціалізовані agents (див. [Subagents з розділеними ролями](../../../guide/ultimate-guide.uk.md#subagents-з-розділеними-ролями-split-role)):

**Agent 1: Аудитор узгодженості**
```
Focus: DRY violations, duplicate logic, pattern inconsistencies
Check for:
- Duplicated code blocks (>5 lines similar)
- Inconsistent naming conventions
- Pattern violations (if project uses X pattern, enforce it)
```

**Agent 2: Аналітик принципів SOLID**
```
Focus: Single Responsibility Principle violations, complexity
Check for:
- Functions >50 lines (likely doing too much)
- Nested conditionals >3 levels deep
- Cyclomatic complexity >10
- Mixed concerns in single component
```

**Agent 3: Аудитор захисного коду**
```
Focus: Silent failures, masked bugs, hidden fallbacks, LLM output trust boundary
Check for:
- Empty catch blocks: try { } catch (e) { } // swallows error
- Silent fallbacks: return data || DEFAULT // hides missing data
- Unchecked null/undefined: user.name without validation
- Ignored promise rejections: async fn without .catch()

LLM Output Trust Boundary (especially relevant in AI-assisted codebases):
- LLM-generated values (emails, URLs, names, IDs) written to DB or passed to
  downstream functions without format validation; add lightweight guards
  (email regex, URL parsing, .trim()) before persisting
- Structured tool output (arrays, objects from AI tools) accepted without
  type/shape checks before database writes or rendering
- AI-generated SQL or code strings executed without sanitization
```

### Правила проти галюцинацій

**Перевіряйте, перш ніж стверджувати**:
- Використовуйте `Grep` або `Glob`, щоб перевірити патерни перед їх рекомендацією
- Якщо пропонуєте "використати наявний патерн UserService", спершу переконайтеся, що UserService існує
- Ніколи не стверджуйте "проєкт використовує X", не перевіривши фактичну кодову базу

**Правило входжень**:
- Патерн із >10 входженнями = усталений (рівень Suggestion)
- Патерн із <3 входженнями = не усталений (Can Skip або запитати мейнтейнера)
- Читайте повний контекст файлу, а не лише рядки diff

**Маркери невпевненості**:
- Використовуйте "❓ To verify:", коли не впевнені щодо конвенцій проєкту
- Використовуйте "💡 Consider:" для необов'язкових покращень
- Використовуйте "🔴 Must fix:" лише для критичних багів/безпеки

### Узгодження

Після того, як agents повідомили висновки:

1. **Дедуплікація**: Приберіть пропозиції, що перетинаються між agents
2. **Пріоритет наявним патернам**: Якщо кодова база використовує патерн X, рекомендуйте X (а не ідеальний патерн Y)
3. **Позначайте пропущені пропозиції**: "Skipping [suggestion] because project uses [alternative pattern]"
4. **Відстежуйте міркування**: Документуйте, чому пропозицію залишено або пропущено

### Класифікація серйозності

```
🔴 Must Fix (Blockers)
- Security vulnerabilities
- Data loss risks
- Breaking changes without migration
- Silent failures masking bugs

🟡 Should Fix (Improvements)
- SOLID violations causing maintenance issues
- DRY violations (>3 duplicates)
- Performance bottlenecks (N+1 queries)
- Missing error handling for critical paths

🟢 Can Skip (Nice-to-haves)
- Style inconsistencies (if no linter)
- Minor naming improvements
- Overly nested code (if <3 levels)
- Documentation gaps (if code self-documenting)
```

### Евристика «спершу виправ»

Визначте, чи виправляти кожну знахідку автоматично, чи виносити її на рішення користувача.

```
AUTO-FIX (apply without asking):          ASK (needs human judgment):
├─ Dead code / unused variables            ├─ Security changes (auth, XSS, injection)
├─ N+1 queries (missing eager loading)     ├─ Race conditions
├─ Stale comments contradicting code       ├─ Design decisions
├─ Magic numbers → named constants         ├─ Large fixes (>20 lines changed)
├─ Missing import / path mismatches        ├─ Enum completeness
├─ Variables assigned but never read       ├─ Anything removing functionality
└─ Obvious version/doc mismatches          └─ User-visible behavior changes
```

**Правило**: Якщо старший інженер застосував би виправлення за 30 секунд без обговорення, це AUTO-FIX. Якщо розумні інженери могли б не погодитися, це ASK.

Після того, як agents повідомили висновки:
1. Негайно застосуйте всі пункти AUTO-FIX мінімальними цільовими правками
2. Згрупуйте всі пункти ASK в єдине рішення користувача (а не одне запитання на пункт)

### Цикл автовиправлення (необов'язково)

Для автоматичної збіжності:

```
Review → Identify issues → Fix → Re-review → Repeat until minimal changes

Safeguards:
- Max 3 iterations to prevent infinite loops
- Run tsc/lint check before each iteration
- Skip auto-fix for protected files (package.json, migrations, etc.)
```

**Приклад prompt**:
```
Review this PR with auto-fix enabled:
1. Review using 3 agents above
2. Fix all 🔴 Must Fix issues
3. Re-review to verify fixes
4. Repeat for 🟡 Should Fix (max 2 more iterations)
5. Stop when only 🟢 Can Skip remain
```

### Умовне завантаження контексту

Завантажуйте додатковий контекст залежно від вмісту diff (незалежно від стеку):

| Якщо diff містить... | Тоді перевірте... |
|----------------------|-------------------|
| Запити до бази даних | Індекси, патерни N+1, оптимізацію запитів |
| Ендпоінти API | Auth middleware, валідацію вхідних даних, rate limiting |
| Логіку автентифікації | Хешування паролів, керування сесіями, CSRF-токени |
| Завантаження файлів | Ліміти розміру, валідацію MIME, безпеку сховища |
| Операції з датою/часом | Обробку часових поясів, граничні випадки DST |
| Виклики зовнішніх API | Конфігурацію тайм-аутів, логіку повторів, обробку помилок |
| Змінні середовища | Наявність у .env.example, валідацію під час старту |

### Інтеграція з наявними інструментами

**Плагін SE-CoVe**: Використовуйте для загальної перевірки фактів у твердженнях рев'ю (доповнює правила проти галюцинацій вище)

**Worktrunk**: Для аналізу патернів у всій кодовій базі перед пропозицією змін

**AST-grep**: Для структурного зіставлення патернів (наприклад, знайти всі схожі блоки try/catch)

---

## Джерела

- Базовий шаблон: Claude Code Ultimate Guide
- Multi-agent рев'ю: [Pat Cullen](https://gist.github.com/patyearone/c9a091b97e756f5ed361f7514d88ef0b) (січ. 2026)
- Патерни проти галюцинацій: система рев'ю коду [Méthode Aristote](https://github.com/FlorianBruniaux)

$ARGUMENTS
