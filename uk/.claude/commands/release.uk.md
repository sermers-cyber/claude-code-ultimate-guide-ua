---
name: release
description: Випустити версію посібника (CHANGELOG + VERSION + README + синхронізація лендінгу + commit + push)
argument-hint: "<patch|minor|major>"
---

# Робочий процес релізу посібника

Випустити нову версію Claude Code Ultimate Guide.

## Використання

```
/release patch    # 3.20.4 → 3.20.5
/release minor    # 3.20.4 → 3.21.0
/release major    # 3.20.4 → 4.0.0
```

## Крок 1: Валідація

1. Розбери `$ARGUMENTS` — має бути рівно одне з: `patch`, `minor`, `major`. Якщо відсутнє чи недійсне, запитай.
2. Виконай `git status` у репозиторії посібника. Якщо робоче дерево чисте й немає staged-змін, перерви: "Nothing to release."
3. Прочитай файл `VERSION` → поточна версія.

## Крок 2: Обчислити нову версію

Застосуй semver-приріст до поточної версії:
- `patch`: X.Y.Z → X.Y.(Z+1)
- `minor`: X.Y.Z → X.(Y+1).0
- `major`: X.Y.Z → (X+1).0.0

Запиши нову версію в `VERSION`.
Покажи: `3.20.4 → 3.20.5 (patch)`

## Крок 3: Підготувати запис CHANGELOG

**НЕ генеруй автоматично з diff.** Натомість:

1. Виконай `git diff --stat` і `git diff --name-only`, щоб визначити змінені області
2. Виконай `git log --oneline` від останнього тега/релізу, щоб побачити нещодавні коміти
3. Прочитай змінені файли, щоб зрозуміти, що змінилося
4. **Підготуй** структурований запис CHANGELOG:

```markdown
## [X.Y.Z] - YYYY-MM-DD

### Added
- [new features, new files, new sections]

### Changed
- [modifications to existing content]

### Fixed
- [corrections, bug fixes]
```

5. **Покажи чернетку користувачеві** і попроси підтвердження або правки
6. Лише після схвалення встав у `CHANGELOG.md` після рядка `## [Unreleased]`

## Крок 4: Оновити лічильники

Обчисли поточні метрики:

```bash
# Quiz questions count (sum across all YAML files)
grep -r '  - id:' quiz/questions/ | wc -l
# Templates count
find examples/ -type f \( -name "*.md" -o -name "*.sh" -o -name "*.ps1" -o -name "*.yml" -o -name "*.yaml" -o -name "*.json" \) -not -name "README.md" -not -name "index.md" | wc -l
# Guide lines
wc -l guide/ultimate-guide.md
```

Оновлюй ці лічильники всюди, де вони з'являються:
- `README.md`
- `machine-readable/reference.yaml`
- `CLAUDE.md` (посилання на VERSION у таблиці Key Files)
- `llms.txt` (корінь) — Version, Last Updated, Lines, Templates, Quiz (3 входження загалом)
- `llms-full.txt` (корінь) — ті самі поля Metadata + ці додаткові входження:
  - Розділ "For Learning": текст URL `Interactive Quiz (N questions)`
  - Заголовок розділу "Template Library (N templates)"
  - Відповідь у FAQ (перший запис FAQ, рядок, що починається з "A: The most comprehensive...")
  - Коментар у дереві репозиторію: `quiz/ # N-question interactive quiz`
- `machine-readable/llms.txt` — має бути ідентичним кореневому `llms.txt` завжди

Оновлюй лише значення, які справді змінилися. Не чіпай лічильники, що досі правильні.

**Бар'єр верифікації — виконай після оновлення, перш ніж переходити до Кроку 5:**

```bash
VERSION=$(cat VERSION)
QUIZ=$(grep -r '  - id:' quiz/questions/ | wc -l | tr -d ' ')
TEMPLATES=$(find examples/ -type f \( -name "*.md" -o -name "*.sh" -o -name "*.ps1" -o -name "*.yml" -o -name "*.yaml" -o -name "*.json" \) -not -name "README.md" -not -name "index.md" | wc -l | tr -d ' ')

echo "=== llms.txt check ==="
grep "Version:\|Quiz Questions:\|Production Templates:" llms.txt

echo "=== llms-full.txt check ==="
grep "Version:\|Quiz Questions:\|Production Templates:\|Template Library\|question interactive" llms-full.txt

echo "=== machine-readable/llms.txt check ==="
grep "Version:\|Quiz Questions:\|Production Templates:" machine-readable/llms.txt

echo "=== Expected: VERSION=$VERSION QUIZ=$QUIZ TEMPLATES=$TEMPLATES ==="
```

Усі три файли мають показувати однакові значення. У разі будь-якої розбіжності виправ, перш ніж продовжувати.

## Крок 5: Синхронізувати версію

```bash
./scripts/sync-version.sh
```

Це поширює версію в: README.md, cheatsheet.md, ultimate-guide.md, reference.yaml.

**Також оновлює**:
- Бейдж "Last Update" у README.md (дата + версія)
- Дату в підвалі README.md ("Updated daily · Feb 10, 2026")

## Крок 5.5: Синхронізувати вміст MCP-сервера

`mcp-server/content/` — це вбудована копія 3 вихідних файлів, що публікується в npm. Вона НЕ оновлюється автоматично, синхронізуй її вручну під час кожного релізу:

```bash
cp machine-readable/claude-code-releases.yaml mcp-server/content/claude-code-releases.yaml
cp machine-readable/reference.yaml mcp-server/content/reference.yaml
cp llms.txt mcp-server/content/llms.txt

# Bump mcp-server/package.json version (patch, unless tool code also changed → minor)
cd mcp-server && npm run build && cd ..
```

Закомічуй `mcp-server/content/*` + `mcp-server/package.json` (dist/ у gitignore, перебудовується під час публікації).

**Публікація** (незворотна, публічна — завжди підтверджуй із користувачем перед виконанням):
```bash
cd mcp-server && npm publish && cd ..
```

## Крок 6: Синхронізувати лендінг

Робоча директорія: `/Users/florianbruniaux/Sites/perso/claude-code-ultimate-guide-landing/`

1. Онови версію посібника в `index.html` (підвал + розділи FAQ)
2. Онови кількість питань вікторини в `index.html`, `quiz/index.html`, `learning/index.html`, якщо вона змінилася
3. Онови кількість шаблонів в `index.html`, `examples/index.html`, якщо вона змінилася
4. Якщо YAML-файли вікторини змінювалися, скомпілюй їх:
   ```bash
   ./scripts/compile-questions.sh
   ```
5. Онови `CLAUDE.md` у репозиторії лендінгу, якщо лічильники змінилися

**Бар'єр верифікації:**
```bash
./scripts/check-landing-sync.sh
```
Має пройти з 0 проблем. Якщо ні, виправ розбіжності й перезапускай, доки не пройде.

## Крок 6.5: Додати запис RSS

У репозиторії лендінгу додай запис до `src/data/rss-entries.ts`:

1. Прочитай щойно підготовлений запис CHANGELOG (Крок 3)
2. Підготуй запис типу `guide_release`:

```typescript
{
  type: 'guide_release',
  title: 'Claude Code Ultimate Guide vX.Y.Z',
  date: 'Mon DD, YYYY',   // today's date, same format as releases.ts
  description: '[1-2 sentences from CHANGELOG highlights, plain text no HTML]',
  link: 'https://cc.bruniaux.com/releases/',
},
```

3. **Додай на початок** масиву `rssEntries` (спершу найновіші).
4. Покажи чернетку користувачеві. За потреби скоригуй формулювання, потім запиши.

**Правило**: завжди додавай запис для patch/minor/major — навіть малі патчі варто відстежувати.

## Крок 7: Commit і push обох репозиторіїв

### Репозиторій посібника

```bash
cd /Users/florianbruniaux/Sites/perso/claude-code-ultimate-guide
git add [all modified files — list them explicitly]
git commit -m "release: vX.Y.Z - [short description from CHANGELOG]

[2-3 line summary of main changes]

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>"
git push
```

### Репозиторій лендінгу

```bash
cd /Users/florianbruniaux/Sites/perso/claude-code-ultimate-guide-landing
git add [all modified files — list them explicitly]
git commit -m "sync: guide vX.Y.Z - [short description]

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>"
git push
```

## Крок 8: Підсумок

Покажи:

```
Реліз vX.Y.Z завершено

Посібник: коміт [hash] ([N] файлів)
Лендінг:  коміт [hash] ([N] файлів)
Синхр.:   Усі перевірки пройдено

Зміни:
- [підсумок CHANGELOG, 2-3 пункти]

Порада: виконайте `/guide-recap latest`, щоб згенерувати дописи для соцмереж про цей реліз.
```

## Обробка помилок

- **Немає аргументу** → Запитай: "Який тип приросту? (patch/minor/major)"
- **Чисте робоче дерево** → Перерви: "Nothing to release. Commit changes first."
- **Перевірка синхронізації не пройшла** → Виправ і перевір знову (не коміть із помилками синхронізації)
- **Git push не вдався** → Покажи помилку, не відкочуй

## Зв'язок з іншими командами

| Команда | Призначення |
|---------|---------|
| `/release` | Випустити сам посібник (ЦЯ) |
| `/update-infos-release` | Відстежувати релізи Claude Code від Anthropic |
| `/sync` | Перевірити стан синхронізації (лише читання) |
| `/version` | Показати версії (лише читання) |
| `/changelog` | Переглянути записи CHANGELOG (лише читання) |

Без перетину: `/release` керує релізами посібника, `/update-infos-release` керує відстеженням релізів CC.
