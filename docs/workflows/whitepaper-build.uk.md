# Довідник зі збірки whitepapers та експорту посібника

Команди й деталі стеку для генерації PDF, EPUB і карток-підсумків із вихідних файлів `.qmd`.

## Генерація whitepapers (PDF + EPUB)

```bash
# --- PDF (default format: whitepaper-typst → Typst → PDF) ---

# Single file
cd whitepapers/fr && quarto render 00-introduction-serie.qmd

# All FR whitepapers
cd whitepapers/fr && quarto render *.qmd

# All EN whitepapers
cd whitepapers/en && quarto render *.qmd

# Preview with hot-reload
cd whitepapers/fr && quarto preview 00-introduction-serie.qmd

# Batch with error summary (loop)
cd whitepapers/fr && for f in *.qmd; do echo "→ $f" && quarto render "$f" 2>&1 | grep -E "(Output created|ERROR)"; done

# --- EPUB (format: epub → Pandoc → EPUB3) ---

# Single file
cd whitepapers/fr && quarto render 00-introduction-serie.qmd --to epub

# All EPUBs (FR + EN) → epub-output/{fr,en}/
cd whitepapers && ./render-epub.sh all
cd whitepapers && ./render-epub.sh fr   # French only
cd whitepapers && ./render-epub.sh en   # English only
```

**Стек PDF**: Quarto → вбудований Typst → PDF. Шаблон: `whitepapers/_extensions/whitepaper/`. Палітра Bold Guy (теплий бежевий + палений помаранчевий).

**Стек EPUB**: Quarto → Pandoc → EPUB3. CSS: `whitepapers/epub-styles.css`. Обкладинка: `_extensions/whitepaper/assets/claude-code-ai-logo.jpg`.

**Доступний skill**: `/pdf-generator` для контекстної допомоги (шаблон YAML, стек, усунення проблем).

**Формат whitepaper**: використовуйте `--to whitepaper-typst`, щоб вибрати шаблон проєкту. Картки-підсумки та шпаргалки використовують власні формати.

## Картки-підсумки (тематичні пам'ятки)

Односторінкові аркуші A4 для друку, щось середнє між шпаргалкою та whitepapers.

```bash
# Single card
cd whitepapers/recap-cards/fr && quarto render 01-commandes-essentielles.qmd --to recap-card-typst

# All FR cards (via script)
cd whitepapers/recap-cards && ./render-recap-cards.sh fr

# All cards (FR + EN)
cd whitepapers/recap-cards && ./render-recap-cards.sh all
```

**Стек**: розширення `recap-card` (`whitepapers/_extensions/recap-card/`). Формат `recap-card-typst`. Та сама палітра Bold Guy.

**Джерела**: `whitepapers/recap-cards/fr/*.qmd` (FR), `whitepapers/recap-cards/en/*.qmd` (EN).

**58 карток для кожної мови** в серіях Technical, Methodology і Design.

## Повна збірка двомовних публікацій

Запускайте з кореня клонованого репозиторію:

```bash
# Inventory only: 146 PDFs and 28 EPUB companions
python3 scripts/render-publications.py --list

# Build both languages; resume only when all recorded input/output hashes match
python3 scripts/render-publications.py --resume

# Check every output, source hash, one-page card, EPUB and PDF page boundary
python3 scripts/validate-publications.py

# Full guides only, using the same templates as the public downloads
python3 scripts/render-publications.py --collections guides

# A single language or collection
python3 scripts/render-publications.py --lang en --collections whitepapers cards
```

Повний каталог містить два повні посібники, 26 whitepapers, 116 карток-підсумків
і дві щоденні шпаргалки. Супровідні EPUB генеруються для посібників і
whitepapers. Результати, журнали рендерингу та `manifest.json` потрапляють у
`dist/publications/`, який Git ігнорує. Маніфест записує хеші джерел і
результатів; успішний рендеринг не підтверджує змістової точності.

Вимоги: Python 3, Quarto 1.10.18 із вбудованим Typst, а також шрифти Inter і
JetBrains Mono. Розширення вибирають нативне підсвічування синтаксису Typst
(`syntax-highlighting: idiomatic`), щоб зберегти рядки коду з власними стилями
сирого тексту. Quarto 1.9 змінив підсвічувач за замовчуванням; див. його
[документацію щодо Typst](https://quarto.org/docs/output-formats/typst.html). `pdfinfo`, якщо його встановлено, також перевіряє читабельність і
записує кількість сторінок. Збірка обробляє незалежні джерела паралельно, тоді як
рендеринг PDF і EPUB для одного джерела лишається послідовним.

Препроцесор повного посібника перед рендерингом вилучає ручний англійський чи французький
зміст і внутрішні посилання-якорі. Зміст PDF формує Quarto.
Перехресні посилання на внутрішні якорі Markdown у цих експортах є простим текстом.

`scripts/generate-guide-exports.sh` лишається застарілим англійським експортом через Pandoc.
Для стилізованих публічних видань і CI використовуйте `scripts/render-publications.py`.

## Актуальність французького перекладу

`guide/ultimate-guide.fr.md` підтримується відповідно до зафіксованого англійського джерела.
Двомовна збірка відмовляється рендерити застарілий французький повний посібник. Перш ніж позначити
оновлення як завершене, перегляньте всю англійську різницю, відновіть пропущені
розділи, збережіть виконувані приклади й перегляньте французький текст. Самої лише
структурної кількості недостатньо.

```bash
# Only after the translation review and source commit are complete
python3 scripts/check-translations.py --update-local --record-french-refresh
python3 scripts/check-translations.py --check --require-current-maintained
python3 scripts/render-publications.py --collections guides --lang fr
```

Оновлення вересня 2026 року використовує воркери Codex. Наявний
`scripts/translate-guide.py` — це окремий застарілий інструмент для Anthropic API, і збірка його
не викликає. Його наявність не визначає модель, яку використовує Codex.

Обгортки повного посібника — це `whitepapers/guide-export.qmd` і
`whitepapers/guide-export-fr.qmd`. Попередньо оброблений Markdown генерується та ігнорується.
Реєстр доказів див. у [підтримці перекладів](translations.uk.md).

## Шаблони Typst: оновлюйте копію, яку використовує джерело

Зараз вихідні розташування використовують такі шаблони:

| Джерело | Шаблон |
| --- | --- |
| `whitepapers/fr/*.qmd` | `whitepapers/fr/_extensions/whitepaper/typst-template.typ` |
| `whitepapers/en/*.qmd` | `whitepapers/en/_extensions/whitepaper/typst-template.typ` |
| Обгортки повного посібника в `whitepapers/` | `whitepapers/_extensions/whitepaper/typst-template.typ` |

Редагування кореневої копії не оновлює копій FR чи EN. Спільне виправлення переглядайте
для всіх трьох шаблонів, зберігаючи задумані відмінності між ними. Не
припускайте, що батьківське розширення буде доступне після вилучення локальної копії.

Картки-підсумки використовують `whitepapers/_extensions/recap-card/`. Їхні теки джерел FR і EN
відкривають його через символьні посилання на теки `_extensions`. Підтримуйте ці
посилання робочими. Старіший `recap-card-template.typ` у розширенні whitepaper
уже відрізняється від окремого шаблону карток; порівнюйте зміни, перш ніж
копіювати між ними.

## Усунення проблем Quarto/Typst

Перш ніж порівнювати результати, зафіксуйте встановлений набір інструментів. Цільові відтворення
на Quarto 1.10.19, вбудованих Pandoc 3.10 і Typst 0.15.1 підтвердили наведені нижче випадки;
вони не перевіряють увесь каталог публікацій.

```bash
quarto --version
quarto pandoc --version
quarto typst --version
```

### Список стає частиною вступного абзацу

Зі стандартним рідером Pandoc Markdown пункти списку, що йдуть одразу після
абзацу без порожнього рядка, можуть лишитися всередині цього абзацу. Додайте в джерелі порожній
рядок перед першим маркером або прапорцем. Це проблема розбору,
а не звичайне подання щільного списку (пункти `BulletList`, що містять `Plain`).

`scripts/render-publications.py` уже вибирає
`markdown+lists_without_preceding_blankline`, а препроцесор повного посібника
вже вставляє роздільники. Для ручного рендерингу з кореня клонованого
репозиторію:

```bash
cd whitepapers/fr
quarto render 00-introduction-serie.qmd --to whitepaper-typst \
  -M from:markdown+lists_without_preceding_blankline
```

Опцію рідера задокументовано в
[посібнику Pandoc](https://pandoc.org/MANUAL.html#extension-lists_without_preceding_blankline).
Lua-фільтр списків не може відновити список, який рідер так і не розібрав.

### Буквальна згадка файлу стає цитуванням у заголовку callout

Голий `@file` у заголовку Markdown стає цитуванням і може зламати компіляцію Typst,
якщо бібліографії немає. Зберігайте згадки файлів як inline-код:

```markdown
::: {.callout-note title="Memo `@file`"}

Callout content.

:::
```

Це працює й тоді, коли заголовок є заголовком розділу всередині callout. Одна
зворотна коса риска перед `@file` в атрибуті `title` у лапках не запобігла
цитуванню в перевіреній версії. Справжні бібліографічні цитування лишайте без змін.

### Власний формат Typst не може завантажити свій шаблон

`recap-card-typst` вибирає розширення `recap-card` і базовий формат `typst`.
Зі стандартним шаблоном тут використовуються два partial-файли функції шаблону:
`typst-template.typ` і `typst-show.typ`; довільно перейменовані partial-файли відхилялися.
Існують й інші підтримувані слоти partial-файлів, як описано в
[документації Quarto щодо власних форматів Typst](https://quarto.org/docs/output-formats/typst-custom.html).

Quarto розгортає partial-файли в згенерований `.typ`. Не додавайте імпорт
`typst-template.typ` усередину `typst-show.typ`, щоб поєднати ці два файли.
Імпорти окремих бібліотек Typst — інший випадок, і для них потрібні шляхи до ресурсів,
які можна розв'язати. Тримайте ці два partial-файли звичайними файлами: символьне посилання для
`typst-template.typ` у відтворенні втратило своє визначення, хоча
наявні символьні посилання на теки `_extensions` працювали.

Для джерела зі збоєм виконайте рендеринг із `--debug` у робочій копії, перегляньте
збережений `.typ` і повний журнал компілятора, а потім знову запустіть валідатор
публікацій. Переглядайте й попередження про шрифти: компіляція із запасними шрифтами не
гарантує задуманої типографіки чи розбиття на сторінки.

## Чекліст розгортання PDF: 3 файли для оновлення

Під час публікації оновлених PDF на лендинг/портфоліо **завжди треба разом оновлювати 3 файли**. Якщо пропустити будь-який із них, віддаватимуться старі файли.

| Файл | Репозиторій | Роль |
|------|------|------|
| `florian-portfolio/public/guides/` | portfolio | Фізичні PDF-файли (копіювати з новою версійною назвою файлу) |
| `landing/src/data/whitepapers-data.ts` | landing | Кнопки прямого завантаження (`const V`, `hashedFileFr/En`) |
| `florian-portfolio/api/guides.mjs` | portfolio | **Посилання в листах**: `GUIDE_MANIFEST` стабільний ID → версійна назва файлу |

**Про `guides.mjs` найлегше забути.** Він визначає, яку URL надсилають листом, коли користувач підписується. Старі посилання в листах перенаправляються через `/api/guides?id=...`, тож оновлення цього файлу заднім числом виправляє посилання й для всіх минулих одержувачів листів.

```bash
# Verify all 3 are in sync after an update:
grep "const V" landing/src/data/whitepapers-data.ts          # should show new version
grep "08-agent-teams.en" florian-portfolio/api/guides.mjs    # should show new version
ls florian-portfolio/public/guides/ | grep "v3.40.0" | wc -l # should show 18+ files
```

## Версіонування електронних книг

Кожна електронна книга має власну версію, незалежну від версії посібника.

**Два поля frontmatter**:
- `version: "3.30.0"` → версія посібника (синхронізується через `./scripts/sync-version.sh`)
- `wp-version: "1.0.0"` → версія електронної книги (підвищується вручну)

**Воркфлоу оновлення**:
1. Підвищте `wp-version` у frontmatter файлу `.qmd`
2. Додайте запис у `whitepapers/CHANGELOG.md`
3. Перезберіть: `cd whitepapers/fr && quarto render XX.qmd --to whitepaper-typst`

**Конвенція semver**: MAJOR = структурне переписування, MINOR = нові розділи/кути зору, PATCH = дрібні виправлення.
