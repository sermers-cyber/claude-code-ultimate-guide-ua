---
name: update-releases
description: "Синхронізувати релізи Claude Code з GitHub CHANGELOG у YAML посібника та TypeScript лендингу"
argument-hint: "[--since <version>] [--dry-run]"
---

# Оновлення релізів Claude Code

Отримай найновіші релізи Claude Code з офіційного GitHub CHANGELOG і синхронізуй обидва файли:
1. **YAML посібника**: `/Users/florianbruniaux/Sites/perso/claude-code-ultimate-guide/machine-readable/claude-code-releases.yaml`
2. **TS лендингу**: `/Users/florianbruniaux/Sites/perso/claude-code-ultimate-guide-landing/src/data/releases.ts`

## Крок 1: Розібрати аргументи

- `--since <version>` — обробити лише версії, строго новіші за цю
- `--dry-run` — показати заплановані зміни, нічого не записувати
- Без аргументів — визначити автоматично за полем `latest:` у поточному YAML

## Крок 2: Прочитати поточний стан

Прочитай YAML посібника, щоб отримати:
- `latest`: поточна остання версія (наприклад, "2.1.66")
- Повний список уже відстежуваних версій

## Крок 3: Отримати офіційний CHANGELOG

Використай WebFetch, щоб отримати:
`https://raw.githubusercontent.com/anthropics/claude-code/main/CHANGELOG.md`

Розбери всі блоки `## X.Y.Z`. Для кожного блоку витягни:
- Рядок версії (semver, без префікса "v")
- Усі марковані пункти як список highlights

## Крок 4: Отримати дати з реєстру npm

Для кожної нововиявленої версії отримай дату публікації з npm:

```bash
npm view @anthropic-ai/claude-code time --json 2>/dev/null
```

Розбери JSON, щоб отримати дати ISO, і перетвори на:
- Формат YAML: `YYYY-MM-DD`
- Формат лендингу: `Mon D, YYYY` (наприклад, `Mar 5, 2026`)

Якщо отримати дані з npm для версії не вдалося, використай сьогоднішню дату й зазнач це.

## Крок 5: Визначити нові версії

Порівняй версії з CHANGELOG із YAML. Версії, що є в CHANGELOG, але відсутні в YAML, нові.

Якщо передано `--since <version>`, розглядай лише версії, новіші за вказану.

Покажи користувачеві:
```
Current latest: v2.1.66
New versions found: N
  - 2.1.67 (Mar 5, 2026): [first highlight]
  - 2.1.68 (Mar 6, 2026): [first highlight]
```

Якщо нових версій немає → покажи "Already up to date. Latest: vX.Y.Z" і заверши.

Якщо вказано `--dry-run`, покажи повний запланований diff для обох файлів і заверши, нічого не записуючи.

Запитай: **"Update guide YAML + landing releases.ts? (y/n)"**

## Крок 6: Оновити YAML посібника

Додай нові версії на початок масиву `releases:` (найновіші першими). Формат кожного запису:

```yaml
- version: "X.Y.Z"
  date: "YYYY-MM-DD"
  highlights:
    - "⭐ Feature description"  # add ⭐ for: new commands, new MCP features, major additions
    - "Regular improvement"
    - "Fixed: bug description"
  breaking: []  # or list breaking changes if present
```

**Евристика для ⭐**: додавай префікс ⭐, якщо highlight згадує нову slash-команду, новий тип hook, новий API/змінну середовища, нову можливість MCP або суттєву зміну воркфлоу. Виправлення помилок ⭐ НЕ отримують.

Онови поля верхнього рівня:
```yaml
latest: "X.Y.Z"  # newest version
updated: "YYYY-MM-DD"  # today
```

## Крок 7: Оновити releases.ts лендингу

Додай нові релізи на початок масиву `releases`. Формат кожного запису:

```typescript
{
  version: 'vX.Y.Z',
  date: 'Mon D, YYYY',
  highlights: [
    '⭐ <strong>Feature Name</strong> — description with <code>command</code>',
    'Improvement description',
    'Fixed: bug description',
  ],
  latest: true,         // only on the newest version
  initiallyVisible: true,  // true if significant (has ⭐ or 3+ highlights), false if bugfix-only
  featured: true,          // only if has a ⭐ highlight
  featuredLabel: '⭐ Feature Name',  // label for the newest featured ⭐ item
},
```

**Правила HTML-форматування:**
- Нові slash-команди → `<code>/command</code>`
- Нові змінні середовища → `<code>ENV_VAR=value</code>`
- Технічні терміни → `<code>term</code>`
- Основні можливості → `⭐ <strong>Name</strong> — description`
- Виправлення помилок починаються з → `Fixed: description`

**Прапорець `latest`:** став `latest: true` лише на найновішій версії. Прибери `latest: true` з попереднього запису, який його мав.

**Логіка `initiallyVisible`:**
- `true`, якщо: є пункти з ⭐, АБО 3+ highlights, АБО це найновіша версія
- `false`, якщо: одиничне виправлення/патч

## Крок 8: Обробити зміни, що ламають сумісність

Якщо highlights якоїсь нової версії містять: "removed", "deprecated", "renamed", "migrated", "security fix", "breaking" → перевір, чи слід додати це до `breakingChanges` у `releases.ts`.

Якщо так, додай у `breakingChanges`:
```typescript
{ badge: 'Type', description: 'What changed with <code>code</code> (vX.Y.Z)' }
```

Варіанти badge: `Security`, `Removed`, `OAuth`, `Install`, `Syntax`, `Behavior`

## Крок 9: Підсумок

Покажи фінальний підсумок:

```
✅ Guide YAML updated: +N versions (latest: vX.Y.Z)
✅ Landing releases.ts updated: +N releases
⚠️  Breaking changes added: [list if any, else "none"]

Next steps:
  cd /Users/florianbruniaux/Sites/perso/claude-code-ultimate-guide
  git diff machine-readable/claude-code-releases.yaml

  cd /Users/florianbruniaux/Sites/perso/claude-code-ultimate-guide-landing
  pnpm build  # validate before pushing
```
