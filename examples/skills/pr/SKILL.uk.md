---
name: pr
description: Проаналізувати зміни, виявити проблеми з обсягом і створити добре структурований PR
argument-hint: "[--base <branch>] [--draft]"
effort: medium
when_to_use: "Використовуйте, коли готові відкрити PR: аналізує зміни й готує опис PR."
disable-model-invocation: true
---

# Створення pull request

Проаналізуйте зміни, виявіть проблеми з обсягом і створіть добре структурований PR відповідно до конвенцій проєкту.

## Процес

1. **Аналіз змін**: Обчисліть показник складності за файлами, комітами та каталогами
2. **Виявлення проблем з обсягом**: Попередьте, якщо PR завеликий або поєднує не пов'язані зміни
3. **Пропозиція розділення**: За потреби згрупуйте коміти за областями й запропонуйте окремі PR
4. **Збір інформації**: Запитайте тип, цільову гілку, статус draft, мітки
5. **Генерація вмісту**: Створіть TLDR + опис + чекліст
6. **Створення PR**: Виконайте `gh pr create` з належним форматуванням
7. **Нагадування про подальші кроки**: Покажіть чекліст після PR (SonarQube, Claude Review)

## Показник складності

Обчисліть складність PR, щоб визначити, чи потрібне розділення:

| Критерій | Вага | Опис |
|----------|------|------|
| Файли коду | x2 | `*.ts, *.tsx` (крім тестів) |
| Тестові файли | x0.5 | `*.test.ts, *.spec.ts` |
| Конфігураційні файли | x1 | `*.json, *.yml, *.md` |
| Каталоги | x3 | Окремі каталоги `src/*` |
| Коміти | x1 | Кількість комітів |

**Пороги**: 0-15 ✅ Нормально | 16-25 ⚠️ Великий | 26+ 🔴 Рекомендовано розділити

## Узгодженість обсягу

| Патерн | Вердикт |
|--------|---------|
| Одна область | ✅ OK |
| Пов'язані області (sessions + calendar) | ✅ OK |
| Не пов'язані області (payments + auth) | 🔴 Розділити |
| feat + fix в одній області | ✅ OK |
| feat + fix у різних областях | 🔴 Розділити |

## Формат пропозиції розділення

Коли рекомендовано розділення, покажіть:

```
🔴 Занадто широкий обсяг (оцінка: 32)

Коміти за областями :
├── payments (5 комітів, 8 файлів)
│   ├── feat(payments): add Stripe checkout
│   └── fix(payments): handle currency
│
└── notifications (3 коміти, 6 файлів)
    └── feat(notifications): add email templates

💡 Пропозиція :
1. PR #1 : feature/payments-stripe → коміти payments
2. PR #2 : feature/notifications → коміти notifications

Варіанти :
[A] Продовжити з одним PR (не рекомендовано)
[B] Розділити (напівавтоматично: надаються git-команди)
[C] Переглянути деталі файлів
```

**Напівавтоматичне розділення** надає команди для копіювання:
```bash
git checkout develop
git checkout -b feature/payments-stripe
git cherry-pick abc1234 def5678
git push -u origin feature/payments-stripe
```

## Запитання

1. **Тип**: feature | fix | tech | docs | security
2. **Цільова гілка**: Покажіть нещодавні гілки (develop, main, інші)
3. **Draft**: Так (WIP) | Ні (готовий до рев'ю)
4. **Мітки**: За типом + необов'язкові (breaking-change, security)

## Формат заголовка PR

```
<type>(<scope>): <description>
```

Приклади:
- `feat(payments): add Stripe checkout integration`
- `fix(sessions): resolve timezone calculation bug`

## Шаблон тіла PR

```markdown
## TLDR
<!-- 2 lines max - Executive summary -->

---

## Type
{Feature | Fix | Tech | Docs | Security}

## Description
{Context and changes}

## Technical Changes
{List of main modifications}

## Tests
- [ ] Unit tests added/passing
- [ ] Manual testing completed

## Checklist
- [ ] Code follows conventions
- [ ] No console.log left
- [ ] Types OK (`pnpm typecheck`)

---

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
```

## Доступні мітки

| Мітка | Колір | Коли використовувати |
|-------|-------|----------------------|
| `feature` | 🟢 | Нова функціональність |
| `fix` | 🔴 | Виправлення бага |
| `tech` | 🔵 | Рефакторинг, технічний борг |
| `docs` | 📘 | Лише документація |
| `security` | 🟣 | Виправлення безпеки |
| `breaking-change` | ⚫ | Зміни, що ламають сумісність |
| `WIP` | 🟡 | Робота триває (draft) |

## Команди для виконання

```bash
# 1. Get base branch (usually develop)
BASE_BRANCH="develop"

# 2. Calculate complexity score
CODE=$(git diff --name-only $BASE_BRANCH..HEAD | grep -E '\.(ts|tsx)$' | grep -v test | wc -l)
TESTS=$(git diff --name-only $BASE_BRANCH..HEAD | grep -E '\.test\.|\.spec\.' | wc -l)
DIRS=$(git diff --name-only $BASE_BRANCH..HEAD | cut -d'/' -f1-2 | sort -u | wc -l)
COMMITS=$(git rev-list --count $BASE_BRANCH..HEAD)
SCORE=$((CODE * 2 + TESTS / 2 + DIRS * 3 + COMMITS))

# 3. Get scopes from commits
git log --oneline $BASE_BRANCH..HEAD --format="%s" | sed -n 's/^\w*(\([^)]*\)).*/\1/p' | sort | uniq -c

# 4. Recent branches for selection
git branch --sort=-committerdate --format='%(refname:short)' | head -5

# 5. Create PR
gh pr create \
  --title "<type>(<scope>): <description>" \
  --body "$BODY" \
  --base $BASE_BRANCH \
  --label "<label>" \
  --draft  # if WIP
```

## Вивід після PR

Після створення PR ЗАВЖДИ показуйте:

```
✅ PR створено : https://github.com/org/repo/pull/XXX

📋 Наступні автоматичні кроки :
   • SonarQube проаналізує якість коду (баги, вразливості, code smells)
   • Claude Code Review надасть ШІ-фідбек щодо вашого PR

⏳ Не забудьте стежити за цими аналізами протягом найближчих хвилин.
   Якщо виявлено проблеми, виправте їх до запиту на рев'ю від людини.
```

## Граничні випадки

| Ситуація | Поведінка |
|----------|-----------|
| Немає області в комітах | Аналізувати за каталогами |
| Не-conventional коміти | Попередити + запитати тип вручну |
| Немає комітів (як у base) | Помилка: "Немає змін" |
| Один коміт | Використати повідомлення коміту як заголовок |
| Merge-коміти | Ігнорувати (`--no-merges`) |

## Використання

```
/pr
/pr --base main
/pr --draft
```

Ціль: $ARGUMENTS (необов'язково: --base, --draft)
