---
name: track-mentions
description: Шукати нові згадки Claude Code Ultimate Guide в інтернеті та оновлювати трекер
argument-hint: "[--add-all | --dry-run]"
---

# Робочий процес відстеження згадок

Знайти нові згадки Claude Code Ultimate Guide в інтернеті (GitHub + cc.bruniaux.com) і оновити `docs/media-mentions/mentions.yaml`.

## Використання

```
/track-mentions            # Шукати + показати нові згадки, підтвердити перед додаванням
/track-mentions --dry-run  # Лише шукати + показати, без змін у YAML
/track-mentions --add-all  # Шукати + автоматично додати всі знайдені згадки
```

## Крок 1: Завантажити наявний трекер

Прочитай `docs/media-mentions/mentions.yaml`, щоб отримати:
- Поточну кількість `meta.total_mentions`
- Усі наявні поля `url` → побудуй набір для дедуплікації

## Крок 2: Запустити глибоке дослідження Perplexity

Використай `mcp__perplexity__perplexity_deep_research` з `reasoning_effort: "high"` і цим запитом
(НЕ згадуй конкретні дати чи "останні 30 днів" — це викликає відмову через обізнаність про дати):

```
Find all articles, blog posts, newsletters, Reddit threads, Twitter/X posts, LinkedIn posts,
YouTube videos, podcasts, GitHub issues/repos, and directories that mention "Claude Code
Ultimate Guide" by Florian Bruniaux (GitHub: FlorianBruniaux/claude-code-ultimate-guide,
website: cc.bruniaux.com). Search broadly for third-party content only — exclude the GitHub
repo itself and cc.bruniaux.com own pages.

For each result provide: URL, publication date if available, author/platform name, language,
and one sentence on how they reference the guide.

Also search explicitly for:
- "cc.bruniaux.com" cited as a resource on third-party sites
- "claude-code-ultimate-guide florian bruniaux" in blog posts and tutorials
- "FlorianBruniaux" in dev tutorials referencing the guide
- The guide mentioned in non-English content (French, Spanish, German, Korean, Portuguese, etc.)
```

**Якщо Perplexity не повертає результатів** (модель відмовляється, посилаючись на межу знань), перейди на
WebSearch із цими паралельними запитами:
```
"claude code ultimate guide" -site:github.com -site:cc.bruniaux.com 2026
site:reddit.com "cc.bruniaux.com" OR "claude code ultimate guide"
site:dev.to OR site:hashnode.com OR site:medium.com "claude code ultimate guide" "florian" OR "bruniaux"
"claude code ultimate guide" twitter OR x.com
```
Потім застосуй `WebFetch` до кожного URL-кандидата, щоб перевірити, що посібник явно згадано за назвою чи URL.

## Крок 3: Дедуплікація

Для кожного результату від Perplexity:
1. Нормалізуй URL (прибери кінцевий слеш, домен у нижньому регістрі)
2. Звір з наявними URL у YAML
3. Пропусти, якщо вже відстежується

## Крок 4: Звіт про нові згадки

Покажи таблицю для перегляду:

```
Знайдено нових згадок: N

| # | Платформа | Автор | Назва | URL | Дата |
|---|----------|--------|-------|-----|------|
| 1 | article  | ...    | ...   | ... | ...  |
```

Якщо `--dry-run`: зупинись тут, без змін.

## Крок 5: Додати в YAML (якщо не --dry-run)

Для кожної нової згадки (усі, якщо `--add-all`, інакше запитуй підтвердження щодо кожної):

1. Призначи наступний послідовний id (доповнений нулями до 3 цифр)
2. Визнач `platform` за типом джерела:
   - Блог/розсилка → `article`
   - reddit.com → `reddit`
   - linkedin.com/posts/* (власний профіль florian-bruniaux) → `linkedin-own`
   - linkedin.com/posts/* (інші) → `linkedin-other`
   - twitter.com / x.com → `twitter`
   - youtube.com → `video`
   - github.com/issues або github.com/discussions → `forum`
   - news.ycombinator.com → `forum`
   - Кураторський список / реєстр / каталог → `directory`
   - podcasts.apple.com / spotify.com → `podcast`
   - instagram.com → `instagram`
3. Встанови `reach: unknown` (якщо у сніпеті не видно кількість переглядів)
4. Встанови `status: active`
5. Встанови `first_seen: <сьогоднішня дата>`
6. Запиши запис у YAML під відповідним коментарем розділу

## Крок 6: Оновити meta

- Збільш `meta.total_mentions` на кількість доданих записів
- Встанови `meta.last_updated` на сьогоднішню дату

## Крок 7: Оновити таблицю статистики в README

Перерахуй записи за платформами та онови таблицю статистики в `docs/media-mentions/README.md`.

## Крок 8: Коміт

```bash
git add docs/media-mentions/
git commit -m "docs: track-mentions — add N new mentions (YYYY-MM-DD)"
```

## Примітки

- Пропускай власні ресурси (сторінки cc.bruniaux.com, сам репозиторій GitHub, профіль FlorianBruniaux)
- Пропускай згадки, де посібник цитується лише за змістом чи контекстом, а не за назвою чи URL
- У неоднозначних випадках (посібник не названо, але URL є) додавай із приміткою
- Якщо Perplexity знаходить 0 нових згадок, повідом: "Нових згадок з останнього запуску не знайдено."
