---
name: "source-command-track-mentions"
description: "Шукати нові онлайн-згадки Claude Code Ultimate Guide або публічного портфоліо проєктів Florian Bruniaux і оновлювати відповідний трекер"
---

# source-command-track-mentions

Використовуй цей skill, коли користувач просить виконати мігровану вихідну команду `track-mentions`.

## Command Template

# Воркфлоу Track Mentions

Знайди нові онлайн-згадки або Claude Code Ultimate Guide, або ширшого публічного портфоліо проєктів.
Каталог посібника зберігається в `docs/media-mentions/mentions.yaml`. Міжпроєктний каталог зберігається в
`~/Sites/perso/florian-portfolio/src/data/mentions.json`.

## Використання

```
/track-mentions            # Search + report new mentions, confirm before adding
/track-mentions --dry-run  # Search + report only, no YAML changes
/track-mentions --scheduled # Unattended report-only run, equivalent to --dry-run
/track-mentions --add-all  # Add all confirmed results after explicit approval in this session
/track-mentions --all-projects # Search the active GitHub portfolio and update the portfolio catalog
/track-mentions --commit   # Commit only the validated tracker files after an approved update
```

`--scheduled` завжди переважає прапорці запису. Запуск за розкладом не повинен редагувати файли, створювати коміт,
виконувати push, відкривати pull request чи публікувати оновлення трекера.

## Крок 1: Завантажити наявний трекер

Для режиму посібника за замовчуванням прочитай `docs/media-mentions/mentions.yaml`, щоб отримати:
- Поточне значення `meta.total_mentions`
- Усі наявні поля `url` → побудуй набір для дедуплікації
- `docs/media-mentions/review-queue.yaml` → залиш недоступних кандидатів у стані очікування, а відхилені URL виключи

Для `--all-projects`:

1. Прочитай публічний профіль GitHub `FlorianBruniaux` і перелічи активні репозиторії, якими володіє цей обліковий запис.
2. Виключи форки, репозиторії лише для лендингів, допоміжні репозиторії на кшталт `homebrew-tap` і RTK.
3. Прочитай `~/Sites/perso/florian-portfolio/src/data/mentions.json`, щоб отримати відстежувані проєкти, URL джерел
   і наявні призначення для кількох проєктів.
4. Вважай один канонічний URL одним джерелом, навіть якщо він називає кілька проєктів.

## Крок 2: Виконати глибоке дослідження через Perplexity

Використай `mcp__perplexity__perplexity_research` із `reasoning_effort: "high"`. Додай нормалізовані URL
із підтвердженого каталогу та черги перегляду як `<KNOWN_URLS>`. Шукай широко під час кожного запуску, замість
того щоб покладатися на те, що тижневе часове вікно охопить сторінки, проіндексовані із запізненням.

```
Find all articles, blog posts, newsletters, Reddit threads, Twitter/X posts, LinkedIn posts,
YouTube videos, podcasts, GitHub issues/repos, and directories that mention "Claude Code
Ultimate Guide" by Florian Bruniaux (GitHub: FlorianBruniaux/claude-code-ultimate-guide,
website: cc.bruniaux.com). Search broadly for third-party content only - exclude the GitHub
repo itself and cc.bruniaux.com own pages.

Return exactly three groups:
- `new_confirmed`: evidence is accessible and contains an explicit project identifier
- `already_tracked`: canonical URL matches `<KNOWN_URLS>`
- `rejected_or_unverified`: title collision, inaccessible evidence, owned property, or uncertain attribution

For each result provide: canonical URL, publication date if available, author/platform name, language,
project identifier found, evidence location, one sentence on how the source references the guide,
classification, confidence, and metadata problems.

Also search explicitly for:
- "cc.bruniaux.com" cited as a resource on third-party sites
- "claude-code-ultimate-guide florian bruniaux" in blog posts and tutorials
- "FlorianBruniaux" in dev tutorials referencing the guide
- The guide mentioned in non-English content (French, Spanish, German, Korean, Portuguese, etc.)

Known canonical URLs for deduplication:
<KNOWN_URLS>
```

**Якщо Perplexity не повертає результатів** (модель відмовляється, посилаючись на межу знань), перейди до
WebSearch із цими паралельними запитами:
```
"Claude Code Ultimate Guide" -site:github.com -site:cc.bruniaux.com
site:reddit.com "cc.bruniaux.com" OR "Claude Code Ultimate Guide"
site:dev.to OR site:hashnode.com OR site:medium.com "Claude Code Ultimate Guide" "florian" OR "bruniaux"
"Claude Code Ultimate Guide" twitter OR x.com
```
Потім використай `WebFetch` для кожного URL-кандидата, щоб перевірити, що посібник прямо згадано за назвою чи URL.

Вважай результат підтвердженим, лише коли сама сторінка, її публічні метадані або проіндексований фрагмент
містять принаймні один ідентифікатор проєкту: назву посібника, канонічний слаг репозиторію або
`cc.bruniaux.com`. Збігу загальної назви, як-от "ultimate Claude Code guide", недостатньо.

Класифікуй кожен підтверджений результат перед тим, як повідомляти про нього:
- `editorial`: стаття, розсилка, подкаст або відео з незалежним коментарем
- `social`: допис третьої сторони в LinkedIn, X, Instagram або Facebook
- `forum`: Reddit, Hacker News, форум або обговорення спільноти
- `translation`: перекладений або адаптований репозиторій, що вказує оригінал
- `mirror`: скопійований або повторно опублікований вміст посібника
- `adoption`: репозиторій третьої сторони помітно вбудовує, конфігурує або використовує проєкт
- `registry`: запис у реєстрі пакетів чи протоколів, що підтверджує охоплення дистрибуцією
- `automated_directory`: згенерований індекс, каталог, MCP-довідник або сервіс документації репозиторіїв

Не зараховуй власні сторінки проєкту, власні соціальні дописи автора, сторінки тем GitHub, згенеровані
з власних метаданих репозиторію, або реферальні параметри запиту як зароблені згадки третіх сторін.
Тримай автоматизовані довідники окремо від органічних згадок. Позначай некоректні команди встановлення, назви
пакетів, кількість зірок, кількість рядків, авторство чи можливості, замість того щоб мовчки їх копіювати.

## Крок 3: Дедуплікація

Для кожного результату з Perplexity:
1. Нормалізуй URL (прибери кінцевий слеш, переведи домен у нижній регістр)
2. Звір з наявними URL у YAML
3. Звір з URL в очікуванні та відхиленими URL у `review-queue.yaml`
4. Розв'яжи очевидні перенаправлення та порівняй канонічне призначення
5. Пропусти, якщо вже відстежується
6. Тримай недоступних кандидатів в очікуванні; ніколи не підвищуй їх лише за повторним фрагментом

## Крок 4: Повідомити про нові згадки

Покажи таблицю для перегляду:

```
New mentions found: N

| # | Kind | Platform | Author | Title | Evidence | Metadata issues | URL | Date |
|---|------|----------|--------|-------|----------|-----------------|-----|------|
| 1 | ...  | ...      | ...    | ...   | Confirmed | None          | ... | ...  |
```

Після таблиці повідом окремі підрахунки:
- органічні згадки: `editorial`, `social` і `forum`
- адаптації: `translation` і `mirror`
- помітне впровадження: `adoption`
- охоплення дистрибуцією: `registry`
- автоматизовані індекси: `automated_directory`

Перелічи ймовірних або недоступних кандидатів окремо. Ніколи не додавай їх як підтверджені записи без
схвалення користувача та явної примітки про невизначеність.

Якщо `--dry-run` або `--scheduled`: зупинись тут, жодних змін.

## Крок 5: Додати до відповідного каталогу (якщо не --dry-run)

У режимі за замовчуванням додай записи до `docs/media-mentions/mentions.yaml` за наведеними нижче правилами.

У режимі `--all-projects` додай один запис до JSON портфоліо з масивом `projects`, що містить кожен
явно названий id проєкту, і явним `group`. Ніколи не дублюй джерело, щоб збільшити підсумки за проєктами.
Додай новознайдений активний проєкт до масиву `projects` верхнього рівня, навіть якщо його перевірена
кількість згадок дорівнює нулю.

Запис потребує явного схвалення користувача в поточній інтерактивній сесії. `--add-all` не вважається
схваленням, якщо його відтворює автоматизація. Для кожної схваленої нової згадки:

1. Признач наступний послідовний id (з нулями до 3 цифр)
2. Визнач `platform` за типом джерела:
   - Блог/розсилка → `article`
   - reddit.com → `reddit`
   - linkedin.com/posts/* (власний профіль florian-bruniaux) → `linkedin-own`
   - linkedin.com/posts/* (інші) → `linkedin-other`
   - twitter.com / x.com → `twitter`
   - youtube.com → `video`
   - github.com/issues або github.com/discussions → `forum`
   - news.ycombinator.com → `forum`
   - Курований список / реєстр / довідник → `directory`
   - podcasts.apple.com / spotify.com → `podcast`
   - instagram.com → `instagram`
3. Встанови `reach: unknown` (якщо у фрагменті не видно кількості переглядів)
4. Встанови `status: active`
5. Встанови `first_seen: <today's date>`
6. Запиши запис у YAML під відповідним коментарем розділу

## Крок 6: Оновити meta

- Збільш `meta.total_mentions` на кількість доданих записів
- Встанови `meta.last_updated` на сьогоднішню дату

## Крок 7: Оновити таблицю статистики в README

Перерахуй записи за платформами й онови таблицю статистики в `docs/media-mentions/README.md`.

## Крок 8: Валідація

Виконай:

```bash
python3 scripts/check-media-mentions.py
```

Не виконуй коміт, якщо ID, канонічні URL, підсумки, платформи чи межі review-queue не проходять валідацію.

## Крок 9: Коміт лише на запит

Без `--commit` повідом про змінені файли й зупинись. З `--commit` додай до індексу лише валідовані файли
трекера. Ніколи не використовуй широкий `git add` у брудному робочому дереві.

```bash
git add docs/media-mentions/mentions.yaml docs/media-mentions/README.md docs/media-mentions/review-queue.yaml
git commit -m "docs: track-mentions - add N new mentions (YYYY-MM-DD)"
```

## Примітки

- Пропускай власні ресурси (сторінки cc.bruniaux.com, сам репозиторій GitHub, профіль FlorianBruniaux)
- Пропускай згадки, де посібник цитується лише за підтекстом чи контекстом, а не за назвою чи URL
- Неоднозначні або недоступні випадки клади в `review-queue.yaml`; не додавай їх до `mentions.yaml`
- Тримай відхилені хибнопозитивні результати в черзі перегляду, щоб подальші запуски за розкладом не знаходили їх знову
- Якщо Perplexity знаходить 0 нових згадок, повідом "No new mentions found since last run."
