---
name: pr-triage
description: "4-фазове управління беклогом PR з аудитом, глибоким рев'ю коду, валідованими коментарями та необов'язковим налаштуванням worktree. Використовуйте для тріажу pull requests, наздоганяння відкладених рев'ю коду або керування беклогом відкритих PR. Аргументи: 'all' для рев'ю всіх, номери PR для фокусу (наприклад '42 57'), 'en'/'fr' для мови, без аргументу = лише аудит."
allowed-tools: Bash Read
effort: medium
---

# Тріаж PR

4-фазовий воркфлоу для мейнтейнерів: автоматичний аудит усіх відкритих PR, глибоке рев'ю за бажанням через паралельних agents, валідована публікація коментарів і необов'язкове налаштування worktree для локального рев'ю.

## Коли використовувати цей skill

| Skill | Використання | Результат |
|-------|--------------|-----------|
| `/pr-triage` | Сортувати, рев'ювати й коментувати беклог PR | Таблиця тріажу + рев'ю + опубліковані коментарі |
| `/review-pr` | Глибоко рев'ювати один PR | Inline-рев'ю PR |

**Тригери**:
- Вручну: `/pr-triage` або `/pr-triage all` або `/pr-triage 42 57`
- Проактивно: коли відкрито >5 PR без рев'ю або виявлено застарілий PR >14 днів

---

## Мова

- Перевірте аргумент, переданий skill
- Якщо `en` або `english` → таблиці та підсумок англійською
- Якщо `fr`, `french` або без аргументу → французька (за замовчуванням)
- Примітка: коментарі GitHub (Фаза 3) ЗАВЖДИ англійською (міжнародна аудиторія)

---

## Конфігурація

Пороги, що використовуються в усьому воркфлоу. Змініть їх під свій проєкт:

| Параметр | За замовчуванням | Опис |
|----------|------------------|------|
| `staleness_days` | 14 | Днів без активності до позначення як застарілого |
| `overlap_threshold` | 50% | Відсоток спільних файлів для позначення як перетину |
| `cluster_min_prs` | 3 | Кількість PR автора для пропозиції кластера |
| `xl_cutoff_additions` | 1000 | Кількість доданих рядків, понад яку PR класифікується як XL |
| `xl_cutoff_files` | 10 | Кількість змінених файлів, понад яку PR «завеликий» |

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
gh repo view --json nameWithOwner -q .nameWithOwner
gh pr list --state open --limit 50 \
  --json number,title,author,createdAt,updatedAt,additions,deletions,changedFiles,isDraft,mergeable,reviewDecision,statusCheckRollup,body
gh api "repos/{owner}/{repo}/collaborators" --jq '.[].login'
```

**Fallback для співавторів**: якщо `gh api .../collaborators` повертає 403/404:
```bash
gh pr list --state merged --limit 10 --json author --jq '.[].author.login' | sort -u
```
Якщо все ще неоднозначно, запитайте через `AskUserQuestion`.

Для кожного PR отримайте рев'ю та змінені файли:

```bash
gh api "repos/{owner}/{repo}/pulls/{num}/reviews" \
  --jq '[.[] | .user.login + ":" + .state] | join(", ")'
gh pr view {num} --json files --jq '[.files[].path] | join(",")'
```

**Примітки**: Отримання файлів потребує 1 виклику API на PR; для 20+ PR надавайте пріоритет кандидатам на перетин. Поле `author` є об'єктом; завжди витягуйте `.author.login`.

### Аналіз

**Класифікація за розміром**:
| Мітка | Додано рядків |
|-------|---------------|
| XS | < 50 |
| S | 50–200 |
| M | 200–500 |
| L | 500–1000 |
| XL | > 1000 |

Формат розміру: `+{additions}/-{deletions}, {files} files ({label})`

**Виявлення**:
- **Перетини**: порівняйте списки файлів між PR; якщо >50% файлів спільні → перехресне посилання
- **Кластери**: автор із 3+ відкритими PR → запропонуйте порядок рев'ю (найменші першими)
- **Застарілість**: немає активності >14 днів → позначити "stale"
- **Статус CI**: через `statusCheckRollup` → `clean` / `unstable` / `dirty`
- **Рев'ю**: approved / changes_requested / none

**Зв'язок PR ↔ Issue**:
- Скануйте `body` кожного PR на `fixes #N`, `closes #N`, `resolves #N` (без урахування регістру)
- Якщо знайдено, покажіть у таблиці: `Fixes #42` у стовпці Action/Status

**Категоризація**:

_Внутрішні PR_: автор у списку співавторів

_Зовнішні, готові_: additions ≤ 1000 І files ≤ 10 І `mergeable` ≠ `CONFLICTING` І CI clean/unstable

_Зовнішні, проблемні_: будь-що з:
- additions > 1000 АБО files > 10
- АБО `mergeable` == `CONFLICTING` (конфлікт мерджу)
- АБО CI dirty (statusCheckRollup містить збої)
- АБО перетин з іншим відкритим PR (>50% спільних файлів)

### Вивід: Таблиця тріажу

```
## Open PRs ({count})

### Internal PRs
| PR | Title | Size | CI | Status |
| -- | ----- | ---- | -- | ------ |

### External: Ready for Review
| PR | Author | Title | Size | CI | Reviews | Action |
| -- | ------ | ----- | ---- | -- | ------- | ------ |

### External: Problematic
| PR | Author | Title | Size | Problem | Recommended Action |
| -- | ------ | ----- | ---- | ------- | ------------------ |

### Summary
- Quick wins: {XS/S PRs ready to merge}
- Risks: {overlaps, XL sizes, CI dirty}
- Clusters: {authors with 3+ PRs}
- Stale: {PRs with no activity >14d}
- Overlaps: {PRs touching the same files}
```

0 PR → покажіть `No open PRs.` і зупиніться.

### Навігація після Фази 1

Після показу таблиці тріажу запитайте через `AskUserQuestion`:

```
question: "What would you like to do next?"
header: "Next Step"
options:
  - label: "Phase 2: Deep review"
    description: "Analyze selected PRs with code-reviewer agents and generate comment drafts"
  - label: "Phase 4: Create worktrees"
    description: "Set up local worktrees for hands-on review (skips comment generation)"
  - label: "Done"
    description: "End the workflow here"
```

Примітка: Фаза 3 (публікація коментарів) тут НЕ пропонується, бо вона потребує чернеток, згенерованих у Фазі 2. Якщо користувач обирає "Phase 4", Фази 2 → 3 залишаються доступними згодом.

### Автоматичне копіювання

Після показу таблиці тріажу скопіюйте її в буфер обміну командою, відповідною платформі:

```bash
UNAME=$(uname -s)
if [ "$UNAME" = "Darwin" ]; then
  pbcopy <<'EOF'
{full triage table}
EOF
elif command -v xclip &>/dev/null; then
  echo "{full triage table}" | xclip -selection clipboard
elif command -v wl-copy &>/dev/null; then
  echo "{full triage table}" | wl-copy
elif command -v clip.exe &>/dev/null; then
  echo "{full triage table}" | clip.exe
fi
```

Підтвердіть: `Triage table copied to clipboard.` (EN) / `Tableau copié dans le presse-papier.` (FR)

---

## Фаза 2: Глибоке рев'ю (за бажанням)

### Вибір PR

**Якщо передано аргумент**:
- `"all"` → усі зовнішні PR
- Номери (`"42 57"`) → лише ці PR
- Без аргументу → запропонуйте через `AskUserQuestion`

**Якщо аргументу немає**, покажіть:

```
question: "Which PRs do you want to review in depth?"
header: "Deep Review"
multiSelect: true
options:
  - label: "All external"
    description: "Review {N} external PRs with parallel code-reviewer agents"
  - label: "Problematic only"
    description: "Focus on {M} risky PRs (CI dirty, too large, overlaps)"
  - label: "Ready only"
    description: "Review {K} PRs ready to merge"
  - label: "Skip"
    description: "Stop here, audit only"
```

**Поведінка щодо Draft PR**:
- Draft PR ВИКЛЮЧЕНО з "All external" і "Ready only"
- Draft PR ВКЛЮЧЕНО до "Problematic only" (вони потребують уваги)
- Щоб зарев'ювати draft: введіть його номер явно (наприклад `42`)

Якщо "Skip" → завершіть воркфлоу.

### Виконання рев'ю

Для кожного обраного PR запустіть agent `code-reviewer` через **інструмент Task паралельно**:

```
subagent_type: code-reviewer
model: sonnet
prompt: |
  Review PR #{num}: "{title}" by @{author}

  **Metadata**: +{additions}/-{deletions}, {changedFiles} files ({size_label})
  **CI**: {ci_status} | **Reviews**: {existing_reviews} | **Draft**: {isDraft}

  **PR Body**:
  {body}

  **Diff**:
  {gh pr diff {num} output}

  Apply your security and architecture expertise. Use the project-specific checklist
  from the SKILL.md Configuration section if available.

  Return structured review:
  ### Critical Issues
  ### Important Issues
  ### Suggestions
  ### What's Good

  Be specific: quote file:line, explain the issue, suggest the fix.
```

**Fallback, якщо паралельні agents недоступні**: виконуйте рев'ю послідовно, по одному PR. Повідомте користувача: `Running sequential review (parallel agents not available).`

Отримайте diff через:
```bash
gh pr diff {num}
gh pr view {num} --json body,title,author -q '{body: .body, title: .title, author: .author.login}'
```

Зберіть усі звіти. Покажіть підсумок після завершення всіх рев'ю.

---

## Фаза 3: Коментарі (обов'язкова валідація)

### Генерація чернеток

Для кожного зарев'юваного PR згенеруйте коментар GitHub за шаблоном `templates/review-comment.md`.

**Правила**:
- Мова: **англійська** (міжнародна аудиторія)
- Тон: професійний, конструктивний, фактичний
- Завжди додавайте принаймні 1 позитивний пункт
- Цитуйте рядки коду, коли доречно (формат `file:42`)

### Показ і валідація

**Покажіть УСІ підготовлені коментарі** у форматі:

```
---
### Draft: PR #{num}: {title}

{full comment}

---
```

Потім запросіть валідацію через `AskUserQuestion`:

```
question: "These comments are ready. Which ones do you want to post?"
header: "Post Comments"
multiSelect: true
options:
  - label: "All ({N} comments)"
    description: "Post on all reviewed PRs"
  - label: "PR #{x}: {title_truncated}"
    description: "Post only on this PR"
  - label: "None"
    description: "Cancel, post nothing"
```

(Згенеруйте один варіант на PR + "All" + "None")

### Публікація

Для кожного підтвердженого коментаря:

```bash
gh pr comment {num} --body-file - <<'REVIEW_EOF'
{comment}
REVIEW_EOF
```

Підтверджуйте кожну публікацію: `Comment posted on PR #{num}: {title}`

Якщо "None" → `No comments posted. Workflow complete.`

---

## Чекліст для конкретного проєкту

Додайте чекліст вашого стеку до prompt agent у Фазі 2. Приклади за стеком:

**Node.js / TypeScript**:
- Немає типу `any` без явного обґрунтування
- Обробка помилок `async/await` (try/catch або `.catch()`)
- Немає необроблених promise rejections
- Валідація вхідних даних на межах API

**Python**:
- Type hints для всіх публічних функцій
- Конкретність винятків (без голого `except:`)
- Очищення ресурсів (оператори `with`, менеджери контексту)
- Без змінних аргументів за замовчуванням

**Rust**:
- `Result<T, E>` з `.context()` для ланцюга помилок (без `.unwrap()` у продакшен-коді)
- Без `clone()` на гарячих шляхах без обґрунтування
- `lazy_static!` або `once_cell` для статичних regex
- Анотації lifetime там, де володіння неочевидне

**Go**:
- Явна обробка помилок (без відкидання через `_` без коментаря)
- `defer` для очищення ресурсів
- Поширення context у конкурентному коді
- Без витоків goroutine

**Загальне** (незалежно від стеку):
- Без секретів чи захардкожених облікових даних
- Нові публічні функції мають тести
- Зміни, що ламають сумісність, задокументовано в тілі PR
- Додані залежності мають чітке обґрунтування

---

---

## Фаза 4: Налаштування worktree (за бажанням)

Створює локальні git worktrees для кожного обраного PR, щоб ви могли запускати, тестувати або рев'ювати код без перемикання гілок.

**Ніколи не запускається автоматично.** Лише через навігацію після Фази 1 або за явним запитом користувача.

### Крок 4.1: Перевірка кешу + список PR

**Перевірка кешу**: перед використанням даних із Фази 1 переконайтеся, що їм менше 30 хвилин:

```bash
CACHE_FILE="/tmp/pr-triage-prs.json"
CACHE_AGE=$(( $(date +%s) - $(stat -f %m "$CACHE_FILE" 2>/dev/null || echo 0) ))
if [ "$CACHE_AGE" -gt 1800 ]; then
  echo "STALE_CACHE"
fi
```

Якщо `STALE_CACHE` → повторіть збір даних Фази 1, перш ніж продовжувати.

**Фільтр**: виключіть Draft PR та PR від ботів (Dependabot, renovate тощо):

```bash
python3 -c "
import json
prs = json.load(open('/tmp/pr-triage-prs.json'))
filtered = [
  p for p in prs
  if not p['isDraft']
  and not any(bot in p['author']['login'].lower() for bot in ['dependabot', 'renovate', 'snyk'])
]
import sys; json.dump(filtered, sys.stdout, indent=2)
" > /tmp/pr-triage-phase4.json
```

Якщо після фільтрації 0 PR → покажіть `No reviewable PRs available for worktree (all are drafts or bots).` + завершіть Фазу 4.

**Покажіть згруповано за автором** (використовуйте відображуване ім'я, якщо воно є, інакше login):

```
## PRs available for worktree (non-draft)

### Alice Martin (@alice)
  [1] #123: feat(auth): add OAuth2 support
      Branch: feat/oauth2  |  Size: M  |  CI: clean

### Bob Chen (@bob)
  [2] #456: fix(api): handle empty response
      Branch: fix/empty-response  |  Size: S  |  CI: dirty ⚠️
```

### Крок 4.2: Вибір

Запитайте через `AskUserQuestion` (multiSelect):

```
question: "Which PRs do you want to create a worktree for?"
header: "Worktree Setup"
multiSelect: true
options:
  - label: "All"
    description: "Create worktrees for all {N} listed PRs"
  - label: "[1] #{num}: {title} ({author})"
    description: "Branch: {branch} | Size: {size} | CI: {ci}"
  - label: "None"
    description: "Cancel, return to menu"
```

Якщо "None" → завершіть Фазу 4.

### Крок 4.3: Послідовне створення

**Модель виконання**: Claude виконує **одну bash-команду на PR**, читає її вивід, оновлює свій внутрішній стан (created / existing / failed), потім переходить до наступного. Ніколи не цикл bash, що обгортає всі PR.

Для кожного обраного PR Claude явно задає змінні, а потім виконує:

```bash
PR_NUM="123"
BRANCH_NAME="feat/oauth2"
WORKTREE_NAME="${BRANCH_NAME//\//-}"
REPO_ROOT="$(cd "$(git rev-parse --git-common-dir)/.." && pwd)"
WORKTREE_DIR="$REPO_ROOT/.worktrees/$WORKTREE_NAME"

# Already exists?
if [ -d "$WORKTREE_DIR" ]; then
  echo "STATUS:EXISTING:$PR_NUM:$WORKTREE_DIR"
  exit 0
fi

# .gitignore check (fail-fast)
if ! grep -qE "^\.worktrees/?$" "$REPO_ROOT/.gitignore" 2>/dev/null; then
  echo "STATUS:GITIGNORE_MISSING:$PR_NUM"
  exit 1
fi

# Fetch remote branch
if ! git fetch origin "$BRANCH_NAME" 2>/tmp/wt-fetch-$PR_NUM.log; then
  echo "STATUS:FETCH_FAILED:$PR_NUM"
  exit 1
fi

mkdir -p "$REPO_ROOT/.worktrees"

# Create worktree (branch local exists or not)
if ! git branch --list "$BRANCH_NAME" | grep -q "$BRANCH_NAME"; then
  git worktree add -b "$BRANCH_NAME" "$WORKTREE_DIR" "origin/$BRANCH_NAME" \
    2>/tmp/wt-err-$PR_NUM.log
else
  git worktree add "$WORKTREE_DIR" "$BRANCH_NAME" \
    2>/tmp/wt-err-$PR_NUM.log
fi

if [ $? -ne 0 ]; then
  if grep -q "already checked out" /tmp/wt-err-$PR_NUM.log; then
    echo "STATUS:ALREADY_CHECKED_OUT:$PR_NUM"
  else
    echo "STATUS:CREATE_FAILED:$PR_NUM"
  fi
  exit 1
fi

# Optional: symlink node_modules (Node.js projects, avoids reinstall)
[ -d "$REPO_ROOT/node_modules" ] && ln -sf "$REPO_ROOT/node_modules" "$WORKTREE_DIR/node_modules"

# Copy project-specific files listed in .worktreeinclude (if present)
if [ -f "$REPO_ROOT/.worktreeinclude" ]; then
  while IFS= read -r entry || [ -n "$entry" ]; do
    [[ "$entry" =~ ^#.*$ || -z "$entry" ]] && continue
    entry="$(echo "$entry" | xargs)"
    [ -e "$REPO_ROOT/$entry" ] && {
      mkdir -p "$(dirname "$WORKTREE_DIR/$entry")"
      cp -R "$REPO_ROOT/$entry" "$WORKTREE_DIR/$entry"
    }
  done < "$REPO_ROOT/.worktreeinclude"
fi

echo "STATUS:CREATED:$PR_NUM:$WORKTREE_DIR"
```

**Обробка статусів** (Claude підтримує внутрішній стан між PR):

| Статус | Дія Claude |
|--------|------------|
| `STATUS:CREATED:NUM:PATH` | Додати до списку "created" |
| `STATUS:EXISTING:NUM:PATH` | Додати до списку "existing" → запропонувати pull на Кроці 4.4 |
| `STATUS:FETCH_FAILED:NUM` | Попередити + перейти до наступного PR |
| `STATUS:GITIGNORE_MISSING:NUM` | Fail-fast: показати інструкції з виправлення + зупинити Фазу 4 |
| `STATUS:ALREADY_CHECKED_OUT:NUM` | Попередити: "Branch already checked out in another worktree. Run `git worktree list` to locate it." |
| `STATUS:CREATE_FAILED:NUM` | Попередити + перейти до наступного PR |

**Інструкції з виправлення GITIGNORE_MISSING**:
```
.worktrees/ is not in .gitignore. Add it to avoid accidentally committing worktree files:
  echo ".worktrees/" >> .gitignore
Then re-run Phase 4.
```

### Крок 4.4: Оновлення наявних worktrees

Якщо зібрано будь-які `STATUS:EXISTING`, запропонуйте єдиний prompt:

```
Existing worktrees detected:
  PR #123: .worktrees/feat-oauth2
  PR #789: .worktrees/fix-session-leak

- [Pull all] git pull --ff-only in all existing worktrees
- [#123] Pull PR #123 only
- [Skip] Leave as-is
```

Для кожного обраного pull Claude виконує (одна команда на worktree):

```bash
PR_NUM="123"
BRANCH_NAME="feat/oauth2"
WORKTREE_DIR="/abs/path/.worktrees/feat-oauth2"

cd "$WORKTREE_DIR" && git pull origin "$BRANCH_NAME" --ff-only 2>/tmp/wt-pull-$PR_NUM.log
echo "PULL_STATUS:$?:$PR_NUM"
```

Якщо `PULL_STATUS` ≠ 0:
```
⚠️ PR #123: --ff-only failed (branches have diverged)
   Manual fix: cd .worktrees/feat-oauth2 && git pull --rebase
```

### Крок 4.5: Підсумок

```
## Worktrees ready

| PR | Author | Branch | Path | Status |
|----|--------|--------|------|--------|
| #123 | Alice | feat/oauth2 | .worktrees/feat-oauth2 | Created |
| #456 | Bob | fix/empty-response | .worktrees/fix-empty-response | Created |
| #789 | Alice | fix/session-leak | .worktrees/fix-session-leak | Updated (pull) |
| #321 | Carol | feat/chat | .worktrees/feat-chat | Fetch failed ⚠️ |

Note: if a PR modifies package.json, install dependencies manually:
  cd .worktrees/<branch-name> && npm install   # or pnpm/yarn/bun

Next steps:
  cd .worktrees/<branch-name>
  claude
```

### Конвенція `.worktreeinclude`

Створіть файл `.worktreeinclude` у корені репозиторію зі списком файлів, які Фаза 4 копіює в кожен новий worktree. Корисно для локальних конфігураційних файлів, що не відстежуються в git:

```
# .worktreeinclude
.env.local
.env.test
config/local.json
```

---

## Граничні випадки

| Ситуація | Поведінка |
|----------|-----------|
| 0 відкритих PR | Показати `No open PRs.` + зупинитися |
| Draft PR | Показати в таблиці, пропустити для рев'ю, якщо не обрано явно |
| Невідомий CI | Показати `?` у стовпці CI |
| Тайм-аут agent рев'ю | Показати часткову помилку, продовжити з іншими |
| `gh pr diff` порожній | Пропустити цей PR, повідомити користувача |
| Дуже великий PR (>5000 additions) | Попередити: "Partial review, diff truncated" |
| API співавторів 403/404 | Fallback до авторів останніх 10 змерджених PR |
| Паралельні agents недоступні | Виконати послідовні рев'ю, повідомити користувача |
| Фаза 4: у `.gitignore` немає `.worktrees/` | Fail-fast, показати інструкції з виправлення, зупинити Фазу 4 |
| Фаза 4: гілку вже checked out | Попередити з підказкою `git worktree list`, пропустити цей PR |
| Фаза 4: застарілий кеш (>30 хв) | Повторно отримати список PR перед створенням worktrees |
| Фаза 4: PR змінює `package.json` | Попередити в підсумку, що install треба виконати вручну |
| Фаза 4: 0 не-draft PR | Показати повідомлення + завершити Фазу 4 |

---

## Примітки

- Завжди визначайте owner/repo через `gh repo view`, ніколи не хардкодьте
- Використовуйте `gh` CLI (не `curl` до GitHub API), окрім списку співавторів
- `statusCheckRollup` може бути null → трактувати як `?`
- `mergeable` може бути `MERGEABLE`, `CONFLICTING` або `UNKNOWN` → `UNKNOWN` трактувати як `?`
- Ніколи не публікуйте без явного підтвердження користувача в чаті
- Підготовлені коментарі мають бути видимі ДО будь-якого `gh pr comment`

---

## Пов'язане: /review-pr

| | `/pr-triage` | `/review-pr` |
|--|-------------|--------------|
| **Обсяг** | Увесь беклог PR | Один PR |
| **Коли використовувати** | Наздоганяння після накопичення, періодичний тріаж | Рев'ю конкретного вхідного PR |
| **Фази** | 4 (аудит + глибоке рев'ю + коментарі + worktrees) | 1 (лише рев'ю) |
| **Agents** | Паралельні sub-agents на PR | Одна сесія |
| **Результат** | Таблиця тріажу + звіти рев'ю + коментарі GitHub + локальні worktrees | Inline-рев'ю |
| **Валідація** | AskUserQuestion перед публікацією | Ручне рішення |

**Правило вибору**: використовуйте `/pr-triage` для тріажу беклогу (5+ PR), `/review-pr` для сфокусованого рев'ю одного PR. Використовуйте Фазу 4, коли хочете запустити код локально, а не лише читати diff.
