---
name: update-infos-release
description: Оновити відстеження релізів Claude Code (посібник + лендінг + підвищення версії)
argument-hint: "[bump-type]"
---

# Робочий процес керування релізами

Автоматизувати відстеження релізів Claude Code та керування версією посібника.

## Використання

```
/update-infos-release          # Лише оновити релізи CC (без підвищення версії посібника)
/update-infos-release patch    # Оновити CC + підвищити patch посібника (3.9.11 → 3.9.12)
/update-infos-release minor    # Оновити CC + підвищити minor посібника (3.9.11 → 3.10.0)
/update-infos-release major    # Оновити CC + підвищити major посібника (3.9.11 → 4.0.0)
```

## Кроки робочого процесу

### 1. Перевірити нові релізи Claude Code

```bash
./scripts/update-cc-releases.sh
```

Якщо виявлено нові версії, продовжуй. Інакше зупинись.

### 2. Оновити відстеження релізів Claude Code

**Файли для оновлення:**
- `machine-readable/claude-code-releases.yaml`
- `guide/core/claude-code-releases.md`
- `mcp-server/content/claude-code-releases.yaml` (побайтово ідентична копія)
- `llms.txt`, `machine-readable/llms.txt`, `mcp-server/content/llms.txt` (речення про відстежувану версію)
- Лендінг: `src/data/releases.ts`, `src/data/seo-editorial-contract.mjs` (`LATEST_CLAUDE_CODE_RELEASE_DATE`) та його закріплений тест `src/data/seo-editorial-contract.test.ts`

**Процес:**
1. Прочитай найновіші нотатки релізу з виводу команди; підсумок, який вона друкує, може пропускати версії, тож перелічи кожен заголовок `## ` збереженого changelog, новіший за відстежувану версію
2. Датуй кожну версію за метаданими публікації в npm (`https://registry.npmjs.org/@anthropic-ai%2Fclaude-code`, поле `time`); пропускай версії без запису в upstream changelog
3. Онови YAML стислими основними моментами
4. Онови Markdown розширеними подробицями
5. Додай нові записи до `releases.ts` лендінгу (спершу найновіші, `latest: true` на найновішому, п'ять із `initiallyVisible: true`) і перенеси дату останнього релізу в `seo-editorial-contract.mjs` та його тест

**Правила стиснення для YAML:**
- ⭐ Основні функції позначаються емодзі зірки
- Breaking changes → масив `breaking:`
- Виправлення багів → один рядок
- 2-4 основні моменти максимум (зосередься на змінах, видимих користувачам)
- Пропускай внутрішні зміни/зміни SDK, якщо вони не breaking

### 3. Підвищення версії посібника (якщо запитано)

**Якщо вказано тип підвищення:**

```bash
# Read current version
cat VERSION

# Bump version
# patch: 3.9.11 → 3.9.12
# minor: 3.9.11 → 3.10.0
# major: 3.9.11 → 4.0.0

# Update VERSION file
echo "X.Y.Z" > VERSION

# Sync version across docs
./scripts/sync-version.sh
```

**Файли, що синхронізує скрипт:**
- `README.md`
- `guide/cheatsheet.md`
- `guide/ultimate-guide.md`
- `machine-readable/reference.yaml`

### 4. Оновити CHANGELOG.md

**Додай запис:**

```markdown
## [X.Y.Z] - YYYY-MM-DD

### Documentation

- **Claude Code Releases**: Updated tracking to vA.B.C
  - [Feature 1]
  - [Feature 2]
  - [Feature 3]

[Якщо підвищено версію посібника:]
### Version Bump

- Bumped guide version: [old] → [new]
- Reason: [major features added / significant updates / breaking changes in CC]
```

### 4.5. Перевірити автоматичне джерело RSS для Claude Code

Реалізація RSS лендінгу в `src/pages/rss.xml.ts` автоматично видає елементи релізів Claude Code з `src/data/releases.ts`. Онови цей реєстр релізів у межах дозволеного охоплення лендінгу; не додавай другий ручний елемент релізу Claude Code до `src/data/rss-entries.ts`.

Ручні записи RSS залишаються доступними для новин на боці посібника, зокрема для релізу самого посібника. Для цієї окремої гілки дотримуйся `docs/workflows/landing-sync.md`. Реліз CLI Claude Code і реліз посібника — різні події.

Огляни поточну реалізацію RSS, щоб побачити видане посилання на реліз, замість копіювання історичного прикладу якоря. Після дозволеної збірки лендінгу перевір згенерований фід на дублікати елементів оновленого релізу CLI та підтверди, що його посилання збігається з реалізацією. Недоступну збірку чи фід повідом як неперевірені.

Готово, коли оновлений реліз CLI постачає автоматичне джерело, жодного дубліката ручного елемента не внесено, а перевірка фіду пройдена або її обмеження зазначено.

### 4.7. Синхронізувати вміст MCP-сервера

`mcp-server/content/` — це вбудована копія 3 вихідних файлів, що публікується в npm як `claude-code-ultimate-guide-mcp`. Вона НЕ оновлюється автоматично, синхронізуй її щоразу, коли змінюється YAML відстеження:

```bash
cp machine-readable/claude-code-releases.yaml mcp-server/content/claude-code-releases.yaml
cp machine-readable/reference.yaml mcp-server/content/reference.yaml
cp llms.txt mcp-server/content/llms.txt

# Bump mcp-server/package.json version (patch, unless server code also changed → minor)
cd mcp-server && npm run build && cd ..
```

Закомічуй `mcp-server/content/*` + `mcp-server/package.json` (dist/ у gitignore, перебудовується під час публікації). Запитай користувача перед виконанням `npm publish` (незворотно, публічно).

### 5. Перевірити синхронізацію

```bash
./scripts/check-landing-sync.sh
```

**Очікуваний вивід:**
```
✅ Version guide:    X.Y.Z
✅ Templates:        N
✅ Quiz questions:   N
✅ Guide lines:      N
✅ Claude Code:      vA.B.C
```

Якщо є розбіжності, виправ їх перед комітом.

### 6. Commit і push

**Потрібно оновити два репозиторії:**

#### Репозиторій посібника

```bash
cd /path/to/claude-code-ultimate-guide

git add \
  VERSION \
  CHANGELOG.md \
  README.md \
  guide/cheatsheet.md \
  guide/ultimate-guide.md \
  guide/core/claude-code-releases.md \
  machine-readable/reference.yaml \
  machine-readable/claude-code-releases.yaml \
  mcp-server/content/claude-code-releases.yaml \
  llms.txt machine-readable/llms.txt mcp-server/content/llms.txt

# If version bump:
git commit -m "release: vX.Y.Z

- Update Claude Code releases tracking (vOLD → vNEW)
- [Bump type]: vOLD_GUIDE → vNEW_GUIDE
- Update CHANGELOG with release details

[attribution line provided by your host]"

# If CC releases only:
git commit -m "docs: update Claude Code releases to vA.B.C

- Update latest tracked version: vOLD → vNEW
- Add vNEW highlights: [feature1], [feature2], [feature3]
- [Any breaking changes or fixes]
- Update dates: YYYY-MM-DD

[attribution line provided by your host]"

git push
```

#### Репозиторій лендінгу

```bash
cd ../claude-code-ultimate-guide-landing

pnpm test   # the release-date contract test pins the latest date
git add src/data/releases.ts src/data/seo-editorial-contract.mjs src/data/seo-editorial-contract.test.ts

git commit -m "docs: sync Claude Code vA.B.C release history

- Add vNEW to releases.ts and move the latest release date

[attribution line provided by your host]"

git push
```

### 7. Підсумковий вивід

Покажи користувачеві:

```
✅ Оновлення релізу завершено

Репозиторій посібника:
- Версія: [стара] → [нова]
- Claude Code: vA.B.C
- Коміт: [hash]
- Файлів: [кількість] оновлено

Репозиторій лендінгу:
- Історія релізів Claude Code: vA.B.C
- Коміт: [hash]
- Файлів: [кількість] оновлено

Синхронізація: ✅ Усе синхронізовано

Наступні кроки:
1. Перевір запуск деплою: gh run list -R FlorianBruniaux/claude-code-ultimate-guide-landing --workflow deploy.yml --limit 1 (його smoke-завдання перевіряє, що /releases/ оголошує останню версію)
2. Перевір https://cc.bruniaux.com/releases/
3. [Якщо мажорний реліз] Оновити соцмережі / анонси
```

## Обробка помилок

**Якщо нових версій Claude Code немає:**
```
ℹ️ Нових релізів Claude Code не виявлено.
Відстежується зараз: vX.Y.Z
Остання доступна: vX.Y.Z

Перериваю. Нічого оновлювати.
```

**Якщо перевірка синхронізації не пройшла:**
```
❌ Перевірка синхронізації не пройшла:
[Перелік розбіжностей]

Виправте вручну перед комітом.
Виконайте: ./scripts/check-landing-sync.sh
```

**Якщо git-операції не вдалися:**
```
❌ Git-операція не вдалася: [помилка]

Потрібне ручне втручання.
Перевірте: git status
```

## Приклади

### Приклад 1: Лише оновити релізи CC

```
User: /update-infos-release

Output:
✅ Виявлено новий реліз Claude Code: v2.1.15
   Дата: 2026-01-22
   Основні моменти:
   - New feature X
   - Fix for Y
   - Improvement Z

Оновлюю файли відстеження...
✅ YAML оновлено
✅ Markdown оновлено
✅ releases.ts лендінгу оновлено

Перевіряю синхронізацію... ✅ Усе синхронізовано

Комічу зміни...
✅ Посібник: коміт abc1234
✅ Лендінг: коміт def5678

✅ Оновлення релізу завершено
```

### Приклад 2: Оновити CC + minor-підвищення

```
User: /update-infos-release minor

Output:
✅ Виявлено новий реліз Claude Code: v2.2.0
   Мажорний реліз зі значними функціями

Поточна версія посібника: 3.9.11
Підвищую до: 3.10.0 (minor)

Оновлюю файли...
✅ Відстеження Claude Code оновлено
✅ Версію посібника підвищено
✅ CHANGELOG оновлено
✅ Усі документи синхронізовано

Перевіряю синхронізацію... ✅ Усе синхронізовано

Комічу зміни...
✅ Посібник: коміт abc1234 (8 файлів)
✅ Лендінг: коміт def5678 (1 файл)

✅ Оновлення релізу завершено (v3.10.0)
```

## Нотатки щодо реалізації

- **Відновлення**: Якщо крок не вдається, зупинись і повідом про частковий стан. Зберігай уже наявні й паралельні правки; відновлюй лише зміни, що належать цій операції, після перевірки, що їхній поточний стан досі збігається з тим, що вона записала. Не використовуй `git reset --hard`.
- **Ідемпотентність**: Можна безпечно запускати кілька разів
- **Валідація**: Завжди перевіряй синхронізацію перед комітом
- **Підтвердження користувача**: Запитай перед підвищенням версії, якщо неоднозначно
- **Розумні значення за замовчуванням**: Без підвищення = лише оновлення CC

## Пов'язані команди

- `/version` - Перевірити поточні версії (посібник + CC)
- `/changelog` - Переглянути останні записи CHANGELOG
- `/sync` - Запустити перевірку синхронізації без оновлень
