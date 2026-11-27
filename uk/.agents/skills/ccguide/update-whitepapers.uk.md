---
name: update-whitepapers
description: Оновити whitepapers (FR + EN) на основі останніх записів CHANGELOG за допомогою паралельної команди агентів
argument-hint: "[--since <version>] [--wp <00-08|cheatsheet>]"
---

# Воркфлоу оновлення whitepapers

Проаналізуй останні записи CHANGELOG і онови зачеплені whitepapers (FR + EN) за допомогою паралельної команди агентів.

## Використання

```
/update-whitepapers                        # Update WPs based on latest CHANGELOG entry
/update-whitepapers --since 3.27.0         # Update WPs for all changes since v3.27.0
/update-whitepapers --wp 03                # Force update WP03 only (FR + EN)
/update-whitepapers --wp 07,08             # Force update WP07 + WP08
```

## Крок 1: Розібрати аргументи

Розбери `$ARGUMENTS`:
- `--since <version>` → проаналізуй усі записи CHANGELOG від цієї версії до останньої
- `--wp <list>` → пропусти аналіз, примусово онови вказані WP (через кому: `03`, `07,08`, `cheatsheet`)
- Без аргументів → використай лише найновіший запис CHANGELOG (останній блок `## [X.Y.Z]`)

## Крок 2: Прочитати CHANGELOG

Прочитай `CHANGELOG.md`. Витягни відповідні записи:
- Якщо `--since <version>`: витягни всі блоки `## [X.Y.Z]` із версією, більшою за вказану
- Якщо `--since` немає: витягни лише перший (найновіший) блок `## [X.Y.Z]`

Покажи витягнуті записи користувачеві для підтвердження.

## Крок 3: Зіставити зміни з whitepapers

Якщо не вказано `--wp`, проаналізуй текст changelog і зістав зміни із зачепленими whitepapers за цією матрицею:

| Ключові слова / теми | Зачеплені WP |
|----------------------|--------------|
| hooks, security, permissions, threat, injection, scanner, allowlist, blocklist | WP03, WP07 |
| context, thinking, architecture, pricing, tokens, model, API, memory | WP04, WP07 |
| CLAUDE.md, settings.json, customization, project, persona, agent-type, MCP | WP02, WP07 |
| prompts, slash commands, commands, output format, `#`, `!` | WP01, WP07 |
| team, multi-agent, orchestration, subagent, background, worktree | WP05, WP08 |
| privacy, ZDR, retention, data, enterprise, telemetry | WP06, WP07 |
| release, version, new feature, introduction | WP00, WP07 |
| cheatsheet | cheatsheet |
| agent teams, Agent Teams | WP08, WP05 |

Завжди включай WP07 (довідковий посібник), якщо виявлено будь-яку суттєву зміну можливостей: це універсальний довідник.

Склади список зачеплених WP. Видали дублікати. Покажи список:
```
Affected whitepapers: WP00, WP03, WP07, WP08
Changes to integrate: [summary of relevant changes]
```

Запитай: "Launch team to update these WPs? (y/n)"

Якщо користувач підтверджує, продовжуй. Якщо вказано `--wp`, пропусти підтвердження.

## Крок 4: Запустити команду агентів

### Налаштування

```bash
# Team name includes timestamp for uniqueness
TEAM_NAME="wp-update-$(date +%Y%m%d-%H%M)"
```

Створи команду: `TeamCreate(team_name=TEAM_NAME)`

Створи одне завдання на кожен зачеплений WP.

### Паралельний запуск агентів

Для кожного зачепленого WP запусти одного агента (`run_in_background: true`) за цим шаблоном промпту:

---
**Шаблон промпту агента:**

```
You are wp-updater for [WP_ID].

You have changelog changes to integrate into two files:
- FR: whitepapers/fr/[FR_FILENAME]
- EN: whitepapers/en/[EN_FILENAME]

## Changes to integrate

[CHANGELOG_EXCERPT]

## Instructions

1. Read the FR file completely
2. Identify sections that need updating based on the changelog
3. Apply targeted edits using the Edit tool (do NOT rewrite entire sections unless necessary)
4. Read the EN file completely
5. Apply the same changes in English
6. Be surgical: only change what's factually outdated or newly relevant
7. Do not change the structure, tone, or style
8. Keep version numbers in frontmatter at [CURRENT_VERSION]

When done, send message to team-lead: "wp-updater [WP_ID] done: [list of sections updated]"
```
---

### Зіставлення WP → файл

| ID WP | Ім'я файлу FR | Ім'я файлу EN |
|-------|---------------|---------------|
| WP00 | fr/00-introduction-serie.qmd | en/00-series-introduction.qmd |
| WP01 | fr/01-prompts-efficaces.qmd | en/01-effective-prompts.qmd |
| WP02 | fr/02-personnalisation.qmd | en/02-customization.qmd |
| WP03 | fr/03-securite.qmd | en/03-security.qmd |
| WP04 | fr/04-architecture.qmd | en/04-architecture.qmd |
| WP05 | fr/05-equipe.qmd | en/05-team.qmd |
| WP06 | fr/06-privacy.qmd | en/06-privacy.qmd |
| WP07 | fr/07-guide-reference.qmd | en/07-reference-guide.qmd |
| WP08 | fr/08-agent-teams.qmd | en/08-agent-teams.qmd |
| cheatsheet | fr/cheatsheet.qmd | en/cheatsheet.qmd |

Усі шляхи вказано відносно теки `whitepapers/` усередині поточної робочої директорії.
Агент має визначати абсолютні шляхи під час виконання, виходячи з кореня проєкту (поточної робочої директорії).

## Крок 5: Дочекатися та зібрати результати

Дочекайся, поки всі агенти повідомлять про завершення. Відстежуй:
- ✅ Завершені агенти
- ❌ Агенти зі збоєм (якщо є)

Коли всі агенти завершать, покажи зведену таблицю:

```
WP00 ✅ — Updated: intro section (9 WPs → 10 WPs)
WP03 ✅ — Updated: hooks count (14 → 17), new scanner hook added
WP07 ✅ — Updated: flags table, reference section
WP08 ✅ — No changes needed
```

## Крок 6: Оновити версію у frontmatter

Якщо changelog містить підвищення версії:
- Прочитай файл `VERSION` → отримай поточну версію
- Онови поле `version:` у frontmatter УСІХ оновлених файлів (FR + EN)

## Крок 7: Прибирання

Завершіть роботу всіх агентів через `SendMessage(type: shutdown_request)`.
Видали команду через `TeamDelete()`.

## Крок 8: Перевірка після оновлення

Виконай швидкі перевірки:
```bash
# No leftover stale versions
grep -r "3\.26\." whitepapers/fr/*.qmd whitepapers/en/*.qmd

# Frontmatter versions consistent
grep "^version:" whitepapers/fr/*.qmd whitepapers/en/*.qmd | sort -u
```

Покажи результати. Познач будь-які невідповідності.

## Важливі примітки

- **Лише точкові правки** — агенти використовують інструмент Edit, а не повне переписування
- **FR і EN завжди оновлюються разом** — ніколи одне без іншого
- **WP07 є довідковим вузлом** — майже завжди включається
- **Джерело істини**: CHANGELOG.md + `guide/ultimate-guide.md` (якщо потрібен глибший контекст)
- **Жодних галюцинацій**: агенти мають цитувати конкретні рядки changelog, на основі яких діють
