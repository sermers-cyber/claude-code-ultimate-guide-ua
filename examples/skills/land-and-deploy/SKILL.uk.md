---
name: land-and-deploy
description: Злити PR, дочекатися CI, перевірити деплой, запустити canary. Повний конвеєр приземлення змін.
argument-hint: "[--skip-checks] [--env staging|production]"
effort: high
disable-model-invocation: true
---

# Land and deploy

Повний конвеєр приземлення змін: злити PR, дочекатися CI, перевірити розгортання, виконати перевірку працездатності.

Продовжує з того місця, де зупинився `/ship`. `/ship` створює PR. Ця команда зливає його й перевіряє продакшен.

**За замовчуванням неінтерактивно.** Користувач сказав «приземли», тож приземляйте. Зупиняйтеся лише на критичній перевірці готовності та жорстких блокерах.

## Інструкції

### Крок 1: Передпольотна перевірка

```bash
# Verify GitHub CLI is authenticated
gh auth status

# Detect PR from current branch (or use argument if provided)
gh pr view --json number,state,title,url,mergeStateStatus,mergeable,baseRefName,headRefName
```

**Умови зупинки:**
- GitHub CLI не автентифіковано → «Спершу виконайте `gh auth login`»
- PR не існує → «Для цієї гілки PR не знайдено. Спершу виконайте `/ship`.»
- PR уже злито → «PR уже злито.»
- PR закрито → «PR закрито. Спершу відкрийте його знову.»

---

### Крок 2: Перевірка стану CI

```bash
# Check current CI status
gh pr checks --json name,state,status,conclusion

# Check for merge conflicts
gh pr view --json mergeable -q .mergeable
```

**Умови зупинки:**
- Обов'язкові перевірки ПАДАЮТЬ → покажіть невдалі перевірки, зупиніться
- `mergeable` має значення `CONFLICTING` → «PR має конфлікти злиття. Розв'яжіть їх і запуште перед приземленням.»
- Обов'язкові перевірки ОЧІКУЮТЬ → переходьте до Кроку 3 (очікування CI)
- Усі перевірки пройдено → пропустіть до Кроку 3.5 (перевірка готовності)

---

### Крок 3: Очікування CI (якщо перевірки в очікуванні)

```bash
# Watch CI checks with 15-minute timeout
gh pr checks --watch --fail-fast
```

- CI пройшов → переходьте до Кроку 3.5
- CI впав → зупиніться, покажіть збої
- Тайм-аут (15 хв) → «CI виконується вже 15 хвилин. Дослідіть вручну.»

Запишіть тривалість очікування CI для звіту про деплой.

---

### Крок 3.5: Перевірка готовності перед злиттям

**Це єдине критичне підтвердження перед незворотним злиттям.** Зберіть усі докази, а потім отримайте явне схвалення.

#### Перевірка застарілості рев'ю

```bash
# How many commits since the last review in this branch?
git log --oneline $(git merge-base HEAD origin/main)..HEAD | wc -l

# What changed after any review was done?
git log --oneline -10
```

Пороги застарілості:
- 0-3 коміти після рев'ю → АКТУАЛЬНЕ (зелений)
- 4+ комітів, що зачіпають код → ЗАСТАРІЛЕ (жовтий, рев'ю може не відображати поточний код)
- Рев'ю не знайдено → НЕ ВИКОНУВАЛОСЯ (жовтий)

#### Результати тестів

```bash
# Run tests now (fast tests only)
npm test 2>/dev/null || pnpm test 2>/dev/null || \
  pytest --tb=short -q 2>/dev/null || \
  go test ./... 2>/dev/null

# Check exit code
echo "Tests exit code: $?"
```

Тести, що падають = БЛОКЕР. Зливати з тестами, що падають, не можна.

#### Перевірка документації

```bash
# Were CHANGELOG and docs updated on this branch?
git diff --name-only $(git merge-base HEAD origin/main)...HEAD -- \
  README.md CHANGELOG.md ARCHITECTURE.md CONTRIBUTING.md CLAUDE.md VERSION
```

Якщо CHANGELOG.md і VERSION НЕ змінювалися, а diff містить нові функції → ПОПЕРЕДЖЕННЯ.

#### Звіт про готовність

Покажіть підсумок і запросіть явне підтвердження:

```
╔══════════════════════════════════════════════════════════╗
║              PRE-MERGE READINESS REPORT                  ║
╠══════════════════════════════════════════════════════════╣
║  PR: #NNN: [title]                                       ║
║  Branch: feature-branch → main                           ║
║                                                          ║
║  REVIEWS                                                 ║
║    Review:     CURRENT / STALE (N commits) / NOT RUN     ║
║                                                          ║
║  TESTS                                                   ║
║    Fast tests: PASS / FAIL (blocker)                     ║
║                                                          ║
║  DOCUMENTATION                                           ║
║    CHANGELOG:  Updated / NOT UPDATED (warning)           ║
║    VERSION:    Bumped / NOT BUMPED (warning)             ║
║                                                          ║
║  WARNINGS: N  |  BLOCKERS: N                             ║
╚══════════════════════════════════════════════════════════╝

Options:
  A) Merge (all checks green)
  B) Don't merge yet, address warnings first
  C) Merge anyway (I understand the risks)
```

Якщо користувач обирає B, перелічіть, що саме потрібно зробити, і зупиніться.

---

### Крок 4: Злити PR

```bash
# Merge (auto-detect method from repo settings, delete branch after)
gh pr merge --auto --delete-branch

# Fallback if auto-merge is not enabled
# gh pr merge --squash --delete-branch
```

Запишіть SHA коміту злиття та мітку часу.

Якщо злиття завершується помилкою дозволів → «У вас немає прав на злиття. Попросіть мейнтейнера злити.»

Якщо активна черга злиття, опитуйте, доки не злито:

```bash
# Poll every 30 seconds, timeout after 30 minutes
gh pr view --json state -q .state
```

---

### Крок 5: Визначення платформи

Визначте, як цей проєкт розгортається, щоб знати, що перевіряти.

```bash
# Detect platform from config files
[ -f fly.toml ]         && echo "PLATFORM: fly"
[ -f render.yaml ]      && echo "PLATFORM: render"
[ -f vercel.json ] || [ -d .vercel ] && echo "PLATFORM: vercel"
[ -f netlify.toml ]     && echo "PLATFORM: netlify"
[ -f Procfile ]         && echo "PLATFORM: heroku"
[ -f railway.toml ]     && echo "PLATFORM: railway"

# Detect GitHub Actions deploy workflows
for f in .github/workflows/*.yml .github/workflows/*.yaml; do
  [ -f "$f" ] && grep -qiE "deploy|release|production|cd" "$f" 2>/dev/null && echo "DEPLOY_WORKFLOW: $f"
done

# Classify diff scope (frontend / backend / docs / config)
git diff --name-only $(git merge-base HEAD~1 origin/main)...HEAD | \
  awk '{
    if (/\.(css|scss|tsx|jsx|html|svg)$/ || /components|pages|public\//) f=1;
    if (/api\/|server\/|backend\/|\.(go|py|rb|java)$/) b=1;
    if (/README|CHANGELOG|docs\/|\.(md)$/) d=1;
    if (/\.env|config\/|\.toml$|\.yaml$/) c=1;
  } END {
    if (f) print "SCOPE_FRONTEND=true";
    if (b) print "SCOPE_BACKEND=true";
    if (d) print "SCOPE_DOCS=true";
    if (c) print "SCOPE_CONFIG=true";
  }'
```

**Дерево рішень:**
- Diff лише з документацією → пропустіть перевірку деплою, переходьте до Кроку 8
- Немає workflow деплою + не надано URL → запитайте користувача, чи має цей проєкт веб-деплой
- Інакше → переходьте до Кроку 6

---

### Крок 6: Очікування деплою

**Workflow деплою в GitHub Actions:**

```bash
# Find the run triggered by the merge commit
gh run list --branch main --limit 10 --json databaseId,headSha,status,conclusion,workflowName

# Poll until complete (30s interval, 20 min timeout)
gh run view <run-id> --json status,conclusion
```

**Стратегії для конкретних платформ:**

| Платформа | Виявлення | Стратегія очікування |
|----------|-----------|---------------|
| Vercel / Netlify | Автодеплой під час push | Зачекайте 60 с на поширення, потім перевірте |
| Fly.io | Наявний `fly.toml` | `fly status --app <app>`, перевірте статус `started` |
| Render | Наявний `render.yaml` | Опитуйте продакшен-URL, доки не відповість 200 |
| Heroku | Наявний `Procfile` | `heroku releases --app <app> -n 1` |
| Railway | Наявний `railway.toml` | Опитуйте продакшен-URL |
| Лише GitHub Actions | `.github/workflows/` із кроком деплою | Опитуйте `gh run view` |

Якщо деплой не вдався → запропонуйте дослідити логи або створити коміт скасування (revert).

Запишіть тривалість деплою для звіту.

---

### Крок 7: Перевірка працездатності продакшену

Використайте обсяг diff (з Кроку 5), щоб визначити глибину перевірки:

| Обсяг diff | Глибина canary |
|------------|--------------|
| Лише документація | Уже пропущено на Кроці 5 |
| Лише конфігурація | Лише димова перевірка HTTP 200 |
| Лише бекенд | Перевірка статусу + часу відповіді |
| Фронтенд (будь-який) | Повна: статус + час відповіді + перевірка вмісту |
| Змішаний | Повна перевірка |

**Послідовність повної перевірки працездатності:**

```bash
# 1. Page loads (200 status)
curl -sf -o /dev/null -w "%{http_code}" "${PROD_URL}" 2>/dev/null

# 2. Response time check
curl -sf -o /dev/null -w "%{time_total}" "${PROD_URL}" 2>/dev/null

# 3. Health endpoint (if exists)
curl -sf "${PROD_URL}/health" 2>/dev/null || \
curl -sf "${PROD_URL}/api/health" 2>/dev/null

# 4. Content check: page is not blank
curl -sf "${PROD_URL}" 2>/dev/null | wc -c
```

Критерії проходження:
- Статус HTTP 200
- Час відповіді менше 10 секунд
- Сторінка має вміст (>500 байтів)
- Ендпоінт health повертає 200 (якщо налаштований)

Якщо будь-яка перевірка не пройдена → запропонуйте відкат:

```
Post-deploy health check detected issues:
  [finding, specific]

Options:
  A) Investigate (this may be normal: cache warming, eventual consistency)
  B) Rollback (revert the merge commit)
  C) Continue (I'll monitor manually)
```

---

### Крок 8: Відкат (за потреби)

```bash
# Fetch the latest base branch
git fetch origin main

# Create a revert commit
git checkout main
git revert <merge-commit-sha> --no-edit
git push origin main
```

Якщо конфлікти → «Revert має конфлікти. Виконайте `git revert <sha>` вручну, щоб їх розв'язати.»
Якщо діє захист гілок → «Створіть PR зі скасуванням: `gh pr create --title 'revert: <title>'`»

---

### Крок 9: Звіт про деплой

```
LAND & DEPLOY REPORT
═════════════════════════════════════════
PR:           #NNN: [title]
Branch:       feature-branch → main
Merged:       [timestamp] (squash / merge)
Merge SHA:    [short SHA]

Timing:
  CI wait:    [Xm Ys / skipped]
  Deploy:     [Xm Ys / no workflow detected]
  Health:     [Xs / skipped]
  Total:      [end-to-end duration]

CI:           PASSED / FAILED / SKIPPED
Deploy:       PASSED / FAILED / NO WORKFLOW
Production:   HEALTHY / DEGRADED / SKIPPED / REVERTED
  Status:     [HTTP status code]
  Response:   [Xms]

VERDICT: DEPLOYED AND VERIFIED / DEPLOYED (UNVERIFIED) / REVERTED
═════════════════════════════════════════
```

---

### Крок 10: Пропозиції щодо подальших дій

Після звіту про деплой запропонуйте доречні наступні кроки:

- Якщо продакшен-URL перевірено: «Запустіть `/canary <url>` для розширеного 10-хвилинного моніторингу.»
- Якщо випущено нові функції: «Запустіть `/document-release`, щоб оновити документацію проєкту.»

---

## Важливі правила

- **Ніколи не робіть force push.** Використовуйте `gh pr merge` (це безпечно).
- **Ніколи не пропускайте CI.** Перевірки, що падають = зупинка.
- **Одноразова перевірка продакшену.** Для розширеного моніторингу використовуйте `/canary`.
- **Відкат завжди можливий.** У кожній точці збою пропонуйте відкат як аварійний вихід.
- **Видаліть гілку функції** після злиття (через `--delete-branch`).
- **Мета**: користувач вводить `/land-and-deploy`, а наступне, що він бачить, це звіт про деплой.

## Використання

```
/land-and-deploy                                    # Auto-detect PR, no canary URL
/land-and-deploy https://app.example.com            # Auto-detect PR + verify this URL
/land-and-deploy 123                                # Specific PR number
/land-and-deploy 123 https://app.example.com        # PR number + verification URL
```

## Пов'язані команди

- `/ship`: запустіть це першим, щоб створити PR
- `/canary`: розширений цикл моніторингу після деплою
- `/review-pr`: перегляньте PR перед приземленням

$ARGUMENTS
