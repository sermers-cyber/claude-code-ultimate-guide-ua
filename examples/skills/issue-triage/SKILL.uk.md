---
name: issue-triage
description: "Триетапне керування беклогом issues: аудит, глибокий аналіз і підтверджені дії триажу. Використовуйте для триажу issues у GitHub, сортування звітів про баги, очищення застарілих тікетів або виявлення дублікатів. Аргументи: 'all' для аналізу всіх, номери issues для фокусування (напр. '42 57'), 'en'/'fr' для мови, без аргументу = лише аудит."
allowed-tools: Bash
effort: medium
---

# Issue triage

Триетапний робочий процес для мейнтейнерів: автоматичний аудит усіх відкритих issues, опційний глибокий аналіз через паралельних агентів і підтверджені дії триажу (коментарі, лейбли, закриття).

## Коли використовувати цей skill

| Skill | Використання | Результат |
|-------|-------|--------|
| `/issue-triage` | Сортувати, аналізувати й діяти щодо беклогу issues | Таблиці триажу + аналіз + виконані дії |
| `/pr-triage` | Сортувати, переглядати й коментувати беклог PR | Таблиця триажу + рев'ю + опубліковані коментарі |

**Тригери**:
- Вручну: `/issue-triage` або `/issue-triage all` або `/issue-triage 42 57`
- Проактивно: коли понад 10 відкритих issues без лейбла або виявлено застарілі issues понад 30 днів

---

## Мова

- Перевірте аргумент, переданий skill
- Якщо `en` або `english` → таблиці й підсумок англійською
- Якщо `fr`, `french` або без аргументу → французькою (за замовчуванням)
- Примітка: коментарі та лейбли GitHub (Фаза 3) ЗАВЖДИ англійською (міжнародна аудиторія)

---

## Конфігурація

Пороги, що використовуються в усьому робочому процесі. Змініть їх відповідно до вашого проєкту:

| Параметр | За замовчуванням | Опис |
|-----------|---------|-------------|
| `staleness_days` | 30 | Днів без активності, після яких issue позначається як застаріле |
| `very_stale_days` | 90 | Днів без активності, після яких issue позначається як дуже застаріле |
| `jaccard_threshold` | 60% | Мінімальна схожість за Жаккаром, щоб позначити дві issues як дублікати |
| `closed_compare_count` | 20 | Кількість останніх закритих issues для порівняння під час виявлення дублікатів |
| `open_limit` | 100 | Максимум відкритих issues для отримання й аналізу |

---

## Передумови

```bash
git rev-parse --is-inside-work-tree
gh auth status
```

Якщо будь-яка з перевірок не проходить, зупиніться й поясніть, чого бракує.

---

## Фаза 1: Аудит (виконується завжди)

### Збір даних (паралельні команди)

```bash
# Repo identity
gh repo view --json nameWithOwner -q .nameWithOwner

# Open issues (exclude PRs, limit 100)
gh issue list --state open --limit 100 \
  --json number,title,author,createdAt,updatedAt,labels,body,comments,assignees,milestone

# Recent closed issues (for duplicate detection)
gh issue list --state closed --limit 20 \
  --json number,title,body,labels,stateReason

# Open PRs (bodies for cross-reference detection)
gh pr list --state open --limit 50 --json number,title,body

# Collaborators (to distinguish reporter types)
gh api "repos/{owner}/{repo}/collaborators" --jq '.[].login'
```

**Запасний варіант для колабораторів**: якщо `gh api .../collaborators` повертає 403/404:
```bash
# Extract authors from last 10 merged PRs
gh pr list --state merged --limit 10 --json author --jq '.[].author.login' | sort -u
```
Якщо все ще неоднозначно, запитайте через `AskUserQuestion`.

**Примітка**: поле `comments` у `gh issue list --json comments` повертає кількість, а не вміст. Для Фази 2 отримайте повний вміст окремо: `gh issue view {num} --json comments`.

### Виміри аналізу

Виконайте всі 6 вимірів для кожної відкритої issue:

#### 1. Категоризація

Класифікуйте кожну issue, прочитавши `title` + перші 200 символів `body`:

| Категорія | Лейбл | Критерії |
|----------|-------|----------|
| Баг | `bug` | Описує зламану поведінку, неочікуваний результат, крах |
| Запит функції | `enhancement` | Просить нову функціональність |
| Питання / підтримка | `question` | Користувач питає, як щось працює |
| Документація | `documentation` | Відсутня або хибна документація |
| Поза межами проєкту | `wontfix` | Явно поза межами проєкту |
| Незрозуміло | `needs-info` | Тіло порожнє, надто розпливчасте для категоризації |

Якщо тіло порожнє → категорія завжди `Unclear` (ніколи не припускайте).

#### 2. Перехресні посилання на PR

Скануйте тіло кожного відкритого PR на посилання на номер issue:
- Патерни: `fixes #N`, `closes #N`, `resolves #N`, `fix #N`, `close #N` (без урахування регістру, `N` = номер issue)
- Використовуйте regex локально на вже отриманих полях `body`; НЕ робіть N додаткових викликів API
- Якщо знайдено: позначте issue як «PR-linked» з номером PR

#### 3. Виявлення дублікатів за схожістю Жаккара

**Алгоритм (самодостатній, без зовнішніх бібліотек)**:

Для кожної відкритої issue обчисліть схожість Жаккара з усіма іншими відкритими issues ТА з 20 останніми закритими issues.

```
Step 1: Normalize title + first 300 chars of body:
  - Lowercase the full text
  - Strip category prefixes: "feat:", "fix:", "bug:", "chore:", "docs:", "test:", "refactor:"
  - Remove punctuation: .,!?;:'"()[]{}-_/\@#

Step 2: Tokenize:
  - Split on whitespace
  - Remove stop words: the a an is in on to for of and or with this that it can not no be
  - Remove tokens shorter than 3 characters

Step 3: Compute Jaccard:
  tokens_A = set of tokens from issue A
  tokens_B = set of tokens from issue B
  jaccard = |tokens_A ∩ tokens_B| / |tokens_A ∪ tokens_B|

Step 4: Flag:
  - If jaccard >= 0.60: mark as potential duplicate
  - Report: "Similar to #N (Jaccard: 0.72)"
  - Keep the OLDER issue as canonical; newer = duplicate candidate
```

Схожість Жаккара обчислюється під час виконання на отриманих даних; жодних викликів API, окрім збору даних у Фазі 1.

#### 4. Класифікація ризику

Призначте Червоний / Жовтий / Зелений за сигналами в title + body:

| Рівень | Колір | Критерії |
|-------|-------|----------|
| Критичний | Червоний | Вразливість безпеки, втрата даних, регресія, що блокує користувачів, крах у продакшені |
| Потребує уваги | Жовтий | Відсутня валідація, погіршення продуктивності, недокументована несумісна зміна, Unclear без відповіді понад 7 днів |
| Звичайний | Зелений | Усе інше |

#### 5. Застарілість

| Статус | Критерій |
|--------|-----------|
| Активна | Оновлена протягом 30 днів |
| Застаріла | Немає активності 30-90 днів |
| Дуже застаріла | Немає активності понад 90 днів |

Використовуйте поле `updatedAt`. Застарілість НЕ залежить від кількості коментарів; issue з коментарями й давнім `updatedAt` усе одно застаріла.

#### 6. Рекомендації

Одна рекомендована дія на issue:

| Ситуація | Дія |
|-----------|--------|
| Категорія = Unclear, тіло порожнє | Коментар із запитом подробиць |
| Жаккар >= 0.60 із відомою issue | Закрити як дублікат, послатися на оригінал |
| Дуже застаріла + немає виконавця | Коментар із запитом статусу, запропонувати закриття |
| Ризик = Червоний | Закріпити на початку триажу, негайно ескалювати |
| Категорія = OOS | Закрити з поясненням |
| PR-linked | Дії не потрібні (відстежується через PR) |
| Звичайна + з лейблом | Дії не потрібні |

### Результат: таблиці триажу

```
## Open Issues ({count})

### Critical: Immediate Attention (Risk: Red)
| # | Title | Category | Reporter | Days Open | Action |
|---|-------|----------|----------|-----------|--------|

### PR-Linked (tracked in open PRs)
| # | Title | Category | PR | Days Open |
|---|-------|----------|----|-----------|

### Active Issues
| # | Title | Category | Labels | Reporter | Days | Action |
|---|-------|----------|--------|----------|------|--------|

### Duplicate Candidates
| # | Title | Similar To | Jaccard | Action |
|---|-------|------------|---------|--------|

### Stale Issues
| # | Title | Category | Last Activity | Reporter | Action |
|---|-------|----------|---------------|----------|--------|

### Summary
- Total open: {N}
- Critical (Red): {count}
- PR-linked: {count}
- Duplicate candidates: {count}
- Stale (30–90d): {count}
- Very stale (>90d): {count}
- Unlabeled: {count}
- Recommended actions: {comment: N, label: N, close: N}
```

0 issues → виведіть `No open issues.` і зупиніться.

**Правила захисту** (застосовуються до всіх фаз):
- Ніколи не закривайте issue, автором якої є колаборатор, без явного підтвердження користувача
- Ніколи не змінюйте лейбли issue, що вже має лейбли (додавайте лише відсутні)
- Якщо тіло порожнє → завжди запитуйте подробиці перед будь-якою іншою дією
- Ніколи не закривайте автоматично Червону issue без підтвердження користувача

### Автоматичне копіювання

Після показу таблиць триажу скопіюйте їх у буфер обміну командою, що відповідає платформі:

```bash
UNAME=$(uname -s)
if [ "$UNAME" = "Darwin" ]; then
  pbcopy <<'EOF'
{full triage tables}
EOF
elif command -v xclip &>/dev/null; then
  echo "{full triage tables}" | xclip -selection clipboard
elif command -v wl-copy &>/dev/null; then
  echo "{full triage tables}" | wl-copy
elif command -v clip.exe &>/dev/null; then
  echo "{full triage tables}" | clip.exe
fi
```

Підтвердьте: `Triage tables copied to clipboard.` (EN) / `Tableaux copiés dans le presse-papier.` (FR)

---

## Фаза 2: Глибокий аналіз (опційно)

### Вибір issues

**Якщо передано аргумент**:
- `"all"` → усі issues з рекомендованими діями
- Номери (`"42 57"`) → лише ці issues
- Без аргументу → запропонуйте через `AskUserQuestion`

**Якщо аргументу немає**, покажіть:

```
question: "Which issues do you want to analyze in depth?"
header: "Deep Analysis"
multiSelect: true
options:
  - label: "All ({N} issues with recommended actions)"
    description: "Launch parallel analysis agents for each actionable issue"
  - label: "Critical only ({M} Red issues)"
    description: "Focus on high-risk issues requiring immediate action"
  - label: "Duplicate candidates ({K} issues)"
    description: "Verify Jaccard similarity with full body + comments"
  - label: "Stale only ({J} stale issues)"
    description: "Decide which stale issues to close vs. revive"
  - label: "Skip"
    description: "Stop here, audit only"
```

Якщо «Skip» → завершіть робочий процес.

### Виконання аналізу

Для кожної вибраної issue запустіть агента аналізу через **інструмент Task паралельно**:

```
subagent_type: general
model: sonnet
prompt: |
  Analyze GitHub issue #{num}: "{title}"

  **Metadata**: Category={category}, Risk={risk}, Days open={days}, Labels={labels}
  **Reporter**: @{author} ({collaborator? "collaborator" : "external"})
  **Assignees**: {assignees or "none"}

  **Body**:
  {body}

  **Comments** (fetch via: gh issue view {num} --json comments):
  {comments[].body, truncate at 5000 chars total}

  **Duplicate candidates**: {jaccard_results or "none found"}
  **Linked PRs**: {pr_refs or "none"}

  Tasks:
  1. Verify the category assigned in Phase 1 (correct? suggest alternative if not)
  2. If duplicate candidate: confirm or deny similarity with rationale
  3. If Unclear/needs-info: identify exactly what information is missing
  4. Suggest the most appropriate action with exact text if a comment is needed
  5. Estimate effort to fix if it's a Bug or Feature Request (XS/S/M/L/XL)

  Return structured output:
  ### Verification
  ### Duplicate Analysis
  ### Missing Information
  ### Recommended Action
  ### Effort Estimate
```

**Запасний варіант, якщо паралельні агенти недоступні**: виконуйте аналіз послідовно, по одній issue. Повідомте користувача: `Running sequential analysis (parallel agents not available).`

Отримайте повні коментарі так:
```bash
gh issue view {num} --json comments --jq '.comments[].body'
```

Зберіть усі звіти. Після завершення всіх аналізів покажіть підсумок.

---

## Фаза 3: Дії (обов'язкове підтвердження)

### Генерація чернеток

Для кожної проаналізованої issue згенеруйте відповідну дію за шаблоном `templates/issue-comment.md`.

**3 типи дій**:

| Тип | Команда | Коли |
|------|---------|------|
| Коментар | `gh issue comment {num} --body-file -` | Потрібна інформація, нагадування про застарілу, пояснення OOS |
| Лейбл | `gh issue edit {num} --add-label "{label}"` | Issue без лейбла з чіткою категорією |
| Закриття | `gh issue close {num} --reason "not planned"` | Дублікат, OOS, дуже застаріла |

**Правила**:
- Мова коментарів: **англійська** (міжнародна аудиторія)
- Додавані лейбли: лише наявні в репозиторії (отримайте через `gh label list`)
- Причина закриття: `"not planned"` для OOS/дубліката, `"completed"` лише якщо виправлення злито
- Ніколи не публікуйте коментар І не закривайте в одній дії, якщо користувач не бачив обидві чернетки
- Завжди додавайте коментар під час закриття (поясніть чому)

### Показ і підтвердження

**Покажіть УСІ підготовлені дії** у форматі:

```
---
### Draft: Issue #{num}: {title}

**Action**: {Comment / Label / Close + Comment}
**Reason**: {1 sentence}

{full comment text if applicable}

---
```

Потім запросіть підтвердження через `AskUserQuestion`:

```
question: "These actions are ready. Which ones do you want to execute?"
header: "Execute Triage Actions"
multiSelect: true
options:
  - label: "All ({N} actions)"
    description: "Execute all drafted triage actions"
  - label: "Issue #{x}: {title_truncated} ({action_type})"
    description: "Execute only this action"
  - label: "None"
    description: "Cancel, execute nothing"
```

(Згенеруйте по одному варіанту на issue + «All» + «None»)

### Виконання

Для кожної підтвердженої дії:

```bash
# Comment
gh issue comment {num} --body-file - <<'TRIAGE_EOF'
{comment}
TRIAGE_EOF

# Label
gh issue edit {num} --add-label "{label}"

# Close with comment
gh issue comment {num} --body-file - <<'TRIAGE_EOF'
{close comment}
TRIAGE_EOF
gh issue close {num} --reason "not planned"
```

Підтверджуйте кожну дію: `Action executed on issue #{num}: {title}`

Якщо «None» → `No actions executed. Workflow complete.`

---

## Граничні випадки

| Ситуація | Поведінка |
|-----------|----------|
| 0 відкритих issues | Показати `No open issues.` + зупинитися |
| Тіло порожнє | Категорія = Unclear, дія = запит подробиць, ніколи не припускати |
| Колаборатор як автор | Захистити від автозакриття, явно позначити в таблиці |
| Жаккар непереконливий (0.55-0.65) | Позначити як «possible duplicate, verify manually» |
| Лейбла немає в репозиторії | Пропустити дію з лейблом, повідомити користувача, щоб спершу створив лейбл |
| Issue закрито під час робочого процесу | Тихо пропустити, зазначити в підсумку |
| `gh api .../collaborators` 403/404 | Запасний варіант: автори останніх 10 злитих PR |
| Паралельні агенти недоступні | Виконати послідовний аналіз, повідомити користувача |
| Дуже велике тіло (>5000 символів) | Обрізати до 5000 символів із приміткою `[truncated]` |
| Призначено milestone | Включити в таблицю, ніколи не закривати issues з milestone без підтвердження |

---

## Примітки

- Завжди визначайте owner/repo через `gh repo view`, ніколи не хардкодьте
- Використовуйте `gh` CLI (а не `curl` до GitHub API), крім списку колабораторів
- `comments` у `gh issue list --json comments` = лише кількість; повний вміст потребує `gh issue view {num} --json comments`
- Ніколи не виконуйте жодної дії без явного підтвердження користувача в чаті
- Підготовлені дії мають бути видимі ДО будь-якого `gh issue comment` чи `gh issue close`
- Жаккар обчислюється локально: без зовнішнього API, без бібліотек, суто операції над множинами на отриманих даних
- Підпис на всіх коментарях: `*Triaged via Claude Code /issue-triage*`

---

## Пов'язане: /pr-triage

| | `/issue-triage` | `/pr-triage` |
|--|----------------|--------------|
| **Обсяг** | Беклог issues | Беклог PR |
| **Коли використовувати** | Наздогнати зворотний зв'язок від авторів, періодичне очищення issues | Наздогнати після накопичення PR |
| **Фази** | 3 (аудит + глибокий аналіз + дії) | 3 (аудит + глибоке рев'ю + коментарі) |
| **Агенти** | Паралельні субагенти на кожну issue | Паралельні субагенти на кожен PR |
| **Виявлення дублікатів** | Схожість Жаккара за title+body | Відсоток перетину файлів між PR |
| **Дії** | Коментар / лейбл / закриття | Коментар рев'ю в GitHub |
| **Підтвердження** | AskUserQuestion перед виконанням | AskUserQuestion перед публікацією |

**Правило вибору**: використовуйте `/issue-triage` для керування беклогом issues, `/pr-triage` для беклогу код-рев'ю.
