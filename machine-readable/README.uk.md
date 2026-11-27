# Машиночитні довідники

Файли, оптимізовані для споживання LLM/ШІ. Числові розміри округлено від поточного розміру файлів у байтах (KiB). Оцінки токенів обчислено як кількість символів, поділену на чотири: це грубе бюджетне наближення, а не підрахунок токенів для конкретної моделі.

## Зміст

| Файл | Опис | Розмір | Оцінка токенів |
|------|-------------|------|-------------|
| [reference.yaml](./reference.yaml) | Головний індекс: шляхи до файлів, якорі розділів і номери рядків у `guide/ultimate-guide.md` та тематичних посібниках. Також містить дерева рішень, довідник CLI та змінних середовища, конфігурацію дозволів і MCP, шаблони агентів і skills, послідовність питань для онбордингу. | ~304 KiB | ~76K |
| [claude-code-releases.yaml](./claude-code-releases.yaml) | Стисла історія офіційних релізів Claude Code: ключові зміни за версіями, `breaking_summary`, згрупований за категоріями, і довідник `milestones`. Джерело істини для `guide/core/claude-code-releases.md`. | ~170 KiB | ~43K |
| [cowork-reference.yaml](./cowork-reference.yaml) | Індекс для Claude Cowork (Claude Desktop, нетехнічна аудиторія). Шляхи вказують на окремий репозиторій [claude-cowork-guide](https://github.com/FlorianBruniaux/claude-cowork-guide), а не на цей. | ~21 KiB | ~4K |
| [agentsec-security-feed.v1.json](./agentsec-security-feed.v1.json) | Метадані бази AgentSec, покриття детекторів, лічильники безпеки та перевірені картки інцидентів, які споживає лендинг. | ~125 KiB | ~32K |
| [agent-harnesses.json](./agent-harnesses.json) | Незмінна нормалізована Agent Harness Map: зафіксований знімок 160 upstream-проєктів, 33 доповнення з посібника, 42 строгі runtime, 16 суміжних площин керування, стани доказів і URL проєктів. | Генерується | Генерується |
| `agent-harnesses-github.json` | Необов'язковий перевірений супровідний файл зі спостереженнями GitHub: зірки, стан архіву, мова, сигнал SPDX, гілка та мітка часу останнього push, прив'язані до контрольної суми каталогу. Не комітиться, доки повний перевірений збір не буде схвалено. | Мінливий | Мінливий |
| [agent-harnesses-github.schema.json](./agent-harnesses-github.schema.json) | JSON Schema для мінливого супровідного файлу зі спостереженнями GitHub. | Генерується | Н/Д |
| [agent-harnesses.schema.json](./agent-harnesses.schema.json) | JSON Schema для перевірки нормалізованого каталогу harness перед публікацією. | Генерується | Н/Д |
| [translations.json](./translations.json) | Датований реєстр канонічних, підтримуваних проєктом і спільнотних видань: URL, мейнтейнери, статус, вихідні коміти, атрибуція, покриття, зафіксоване відставання та корені двомовної публікації. | ~11 KiB | ~3K |
| [distribution-channels.yaml](./distribution-channels.yaml) | JSON-сумісний YAML-реєстр каналів публікації, URL з атрибуцією, станів ресурсів, дат і полів 30-денних результатів. | ~8 KiB | ~2K |
| [navigation.json](./navigation.json) | Спільний контракт навігації `Start`, `Build`, `Scale`, `Resources` і `Updates` для README репозиторію та публічної карти сайту лендингу. Кожен публічний маршрут може вказувати на свій канонічний вихідний файл у репозиторії. | Генерується | <2K |
| [navigation.schema.json](./navigation.schema.json) | JSON Schema для спільного контракту навігації. | Генерується | Н/Д |
| [llms.txt](./llms.txt) | Стандартний контекстний файл LLM для індексації репозиторію: покриття тем, точки входу, ключові URL. | ~11 KiB | ~3K |

`reference.yaml` є повним індексом, а не підсумком. Шукайте потрібну тему й переходьте за знайденим шляхом або номером рядка, замість того щоб завантажувати весь індекс у контекст.

Кореневі `llms.txt` і `llms-full.txt` виконують ту саму роль ШІ-індексації для краулерів. Тримайте кореневий `llms.txt`, `machine-readable/llms.txt` і `mcp-server/content/llms.txt` побайтово ідентичними.

## Використання

### Знайти тему без завантаження всього посібника

```bash
# Find where a topic lives, then read only that file or line range
grep -i "memory_systems" machine-readable/reference.yaml
grep -i "hooks_events" machine-readable/reference.yaml
grep -i "lean_ai_flow_adaptation" machine-readable/reference.yaml
```

### Посилання в Claude Code

```
@machine-readable/reference.yaml
```

### Отримати віддалено

```bash
curl -sL https://raw.githubusercontent.com/FlorianBruniaux/claude-code-ultimate-guide/main/machine-readable/reference.yaml
curl -sL https://raw.githubusercontent.com/FlorianBruniaux/claude-code-ultimate-guide/main/machine-readable/agent-harnesses.json
curl -sL https://raw.githubusercontent.com/FlorianBruniaux/claude-code-ultimate-guide/main/machine-readable/translations.json
curl -sL https://raw.githubusercontent.com/FlorianBruniaux/claude-code-ultimate-guide/main/machine-readable/distribution-channels.yaml
curl -sL https://raw.githubusercontent.com/FlorianBruniaux/claude-code-ultimate-guide/main/machine-readable/navigation.json
```

### Публічний контракт навігації

[`navigation.json`](./navigation.json) тримає зведення репозиторію та публічний сайт узгодженими, не перетворюючи жодне з них на джерело для прози посібника. Він містить добірні групи за намірами, публічні маршрути, короткі описи та вихідні шляхи. Канонічним для свого вмісту лишається Markdown.

Перевірте маніфест і згенерований блок у `README.md`:

```bash
python3 scripts/sync-navigation.py
```

Після редагування маніфесту перегенеруйте лише позначений блок README:

```bash
python3 scripts/sync-navigation.py --write
```

Збірка лендингу копіює той самий маніфест до власного каталогу даних, перш ніж Astro відрендерить читабельну карту сайту. Сторінки лише для лендингу можуть використовувати `null` у `source_path`. Кожне ненульове джерело має існувати в цьому репозиторії, а оголошений якір джерела має вказувати на заголовок.

### Статус перекладів

[`translations.json`](./translations.json) розрізняє канонічне англійське видання, підтримуване французьке видання та незалежно підтримувані спільнотні адаптації. Стан `stale` є правдивим опублікованим статусом, а не збоєм збірки. Некоректні контрольні суми, походження джерела, зафіксоване відставання, поля атрибуції, відсутні мовні пари або стан, що суперечить доказам, справді провалюють перевірку цілісності.

```bash
python3 scripts/check-translations.py --check
python3 scripts/check-translations.py --check --require-current-maintained
```

Пакет MCP надає свій вбудований реєстр як `claude-code-guide://translations`. Другий коміт у послідовності оновлення нижче відновлює побайтову рівність із канонічним реєстром.

Канонічна провенансність є двокомітною операцією. Спершу закомітьте `guide/ultimate-guide.md` і пов'язані індекси, потім запустіть `python3 scripts/check-translations.py --update-local`, віддзеркальте результат у `mcp-server/content/translations.json`, перевірте побайтову рівність і закомітьте ці два реєстри окремо. Засіб оновлення відмовляється працювати з брудним канонічним посібником, бо незакомічений хеш файлу не можна віднести до старішого коміту. Див. [Translation Status Workflow](../docs/workflows/translations.uk.md#після-зміни-англійського-повного-посібника).

### Статус розповсюдження

[`distribution-channels.yaml`](./distribution-channels.yaml) відокремлює виробництво ресурсів від зовнішньої публікації. Ресурс зі статусом `ready` пройшов локальні перевірки, але не був поданий і не опублікований. Відсутні виміри лишаються `null`.

```bash
python3 scripts/check-distribution-channels.py
python3 -m unittest scripts/test-check-distribution-channels.py
```

Пакет MCP надає той самий реєстр як `claude-code-guide://distribution-channels`.

### Розрізнення понять

Почніть із [AI Concept Boundaries](../guide/core/ai-concept-boundaries.uk.md), коли питання змішує контекст із пам'яттю, модель з її harness, агента з workflow, інструмент з MCP, інструкції з примусовим доступом, результати оцінювання з доказами з продакшну або архітектуру, розмір, модальність і мітки задач моделі. Кожне розрізнення веде до детального розділу посібника та має оригінальну [перевірку за сценарієм](../guide/core/ai-concept-boundaries.uk.md#перевірте-своє-розуміння).

[Оцінка Lexigraph](../docs/resource-evaluations/lexigraph-ai-lexicon.uk.md) фіксує джерело, атрибуцію CC BY 4.0, прогалини експорту та причини вибіркової адаптації. Сторінка про поняття адаптує структуру навчання та окремі розрізнення; вона не імпортує корпус, банк тестових питань чи інфографіку. Для поведінки runtime використовуйте продуктові довідки посібника.

### Контролі harness і нагляд

- [Запускна симуляція контролю та відновлення](../examples/workflows/review-control-demo.py): 13 локальних тестів, симульований пункт призначення, без заяв про живу приймальну перевірку на GitHub.
- [Walkinglabs](../docs/resource-evaluations/learn-harness-engineering-2026.uk.md) і [AutoHarness](../docs/resource-evaluations/autoharness-2026.uk.md): розглянуті навчальні випадки та випадки супроводу з цільовими доказами збоїв.
- [Позиційна стаття про людський нагляд](../docs/resource-evaluations/human-oversight-agents-2608-23642.uk.md) і [двомовна інфографіка](https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/images/harness-review/README.md): практики для оцінювання, а не спостережені локальні результати участі людини.

### Передачі, володіння контекстом і покращення harness

| Потреба | Точка входу |
|---|---|
| Контракт архітектор-інженер, ADR, стани задач/запусків, зворотний зв'язок рецензії | [Dual-instance planning](../guide/workflows/dual-instance-planning.uk.md), [шаблон плану](../guide/workflows/dual-instance-planning.uk.md#шаблон-плану) і [вихідна оцінка](../docs/resource-evaluations/honkonen-architect-engineer.uk.md) |
| Стабільні контракти проти організаційних знань і живого стану | [Межа знань](../guide/ultimate-guide.uk.md#9252-what-the-agent-cant-see-doesnt-exist) |
| Локальні вимоги до якості, семантичні власники, канонічні приклади, завершення міграції | [Відновлювана планка якості](../guide/ultimate-guide.uk.md#make-the-local-quality-bar-recoverable) |
| Спостереження агента до просування в пам'ять | [Телеметрія MLD](../guide/core/memory-systems.uk.md#mld-спостереження-для-того-хто-будує-harness) і [цикл оновлення на основі доказів](../guide/core/context-engineering.uk.md#цикл-оновлення-the-update-loop) |
| Ізоляція кандидатів, права публікації, фіксація ревізій і строк дії | [Публікація курованого контексту](../guide/core/context-engineering.uk.md#контракт-публікації-для-курованого-контексту) |
| Повторна кваліфікація після оновлень; окремі годинники зворотного зв'язку, запуску, уваги, приймання | [Епохи оцінювання та чотири годинники](../guide/roles/agent-evaluation.uk.md#епохи-оцінювання-та-чотири-годинники) |

Ці доповнення адаптують практичні матеріали. [Антологія Lopopolo](../docs/resource-evaluations/lopopolo-harness-engineering.uk.md) є корпусом контексту, а не виконуваним runtime. Команди `eng` від Honkonen належать до його власного інструментарію. Жодне з джерел не встановлює виміряних локальних здобутків у якості, вартості чи доставці.

### Пам'ять агента: типи, область дії та фактичне використання

| Потреба | Точка входу |
|---|---|
| Класифікувати пам'ять за змістом, формою, областю дії та життєвим циклом | [Типи пам'яті: координати, а не стек](../guide/core/memory-systems.uk.md#типи-памяті-координати-а-не-стек) |
| Дізнатися, чи пам'ять лишається на одній машині, чи доходить до команди (Claude Code, Codex, Gemini CLI, Copilot, Kiro) | [Де живе пам'ять](../guide/core/memory-systems.uk.md#де-живе-память-локально-у-репозиторії-спільно) |
| Перевірити, що ін'єктована пам'ять змінює поведінку агента | [Шестиетапний конвеєр](../guide/core/memory-systems.uk.md#від-захопленого-до-дієвого-шестиетапний-конвеєр) і [бенчмарки використання 2026](../guide/core/memory-systems.uk.md#вимірювання-того-чи-використовується-память-2026) |
| Обрати чи провести аудит міжсесійного інструмента (claude-mem, agentmemory, memorix, basic-memory) | [Міжсесійні інструменти](../guide/core/memory-systems.uk.md#3-інструменти-між-сесіями-один-користувач) і [порівняльна таблиця](../guide/core/memory-systems.uk.md#39-головна-порівняльна-таблиця) |
| Докази отруєння постійної пам'яті | [Отруєння пам'яті](../guide/core/memory-systems.uk.md#71-отруєння-памяті-через-prompt-injection) |

Факти про інструменти зчитано з тегів релізів і документації постачальників 2026-11-03. Типові значення, версії та кількість зірок змінюються; перевіряйте перед цитуванням.

### Ландшафт agent harness

Використовуйте читабельні для людини сторінки відповідно до питання, яке ставите:

| Потреба | Точка входу |
|---|---|
| Архітектура runtime, компоненти, контролі, реалізація в Claude Code і протокол оцінювання оптимізаторів | [Agent Harness Engineering](../guide/core/agent-harness.uk.md) |
| Контрольні тести, абляції рецензентів, незалежні критерії приймання та вартість за прийняту задачу | [Agent Evaluation](../guide/roles/agent-evaluation.uk.md#зафіксуйте-оракул-і-правило-прийняття-рішення) і [вихідна оцінка](../docs/resource-evaluations/harness-evidence-marmelab-2026.uk.md) |
| Контракти циклів, контракти графів, розподіл суджень, довговічність, спостережуваність і вибір структури керування | [Loop & Graph Engineering](../guide/core/loop-graph-engineering.uk.md) |
| Класичні патерни проєктування, зіставлені з механізмами agent harness, із режимами збоїв, перевірками, джерелами та посиланнями в кожній картці на пов'язані workflow, шаблони, а також інструменти й статті автора | [AI Design Patterns](../guide/core/ai-design-patterns.uk.md) і [`ai-design-patterns.json`](./ai-design-patterns.json) |
| Датована міжпродуктова карта, класифікація, вибір, протокол тест-драйву та дослідницький шар мета-harness | [Agent Harness Landscape](../guide/ecosystem/agent-harness-landscape.uk.md) |
| Детальні профілі вибраних кодувальних агентів | [Agent Tools: Beyond Claude Code](../guide/ecosystem/agentic-tools.uk.md) |
| Термінологія runtime, репозиторію, evaluation harness та оркестратора | [Глосарій](../guide/core/glossary.uk.md) |
| Поведінка Claude Code на рівні версій | [claude-code-releases.yaml](./claude-code-releases.yaml) |
| Стабільні маршрути до тем і розділів | [reference.yaml](./reference.yaml) |

`agent-harnesses.json` генерується із закоміченого знімка `best-of-Agent-Harnesses@ece314654d2c23fe7bd69fc6ef7088f093207e49` та добірних ручних перевизначень. Сирий вихідний файл перевіряється за `best-of-agent-harnesses-ece314654d2c.manifest.json` і SHA-256 `4c02e547e11b056aa4d7e519305b7f4ca4f02550c27018d70757a59d26ace65f` перед розбором. Записи, похідні від upstream, зберігають атрибуцію джерела CC-BY-SA-4.0 та його знімок зірок від 2026-08-23.

Файл тримає чотири набори окремо:

- `upstream_snapshot`: 160 вихідних проєктів у 12 категоріях;
- `guide_supplement`: офіційні продукти й перевірені репозиторії, відсутні в цьому знімку;
- `strict_runtime_map`: проєкти, докази яких свідчать, що вони володіють циклом агента;
- `adjacent_control_planes`: обгортки, менеджери флотів, контролери задач і шари виконання, що викликають інший runtime.

Поле `interfaces` використовує шість значень: `cli`, `tui`, `ide`, `desktop`, `web` і `chat`. Upstream-теги `cli`, `tui`, `ide` і `browser` детерміновано відображаються на цей словник. Добірні винятки потребують офіційного джерела, зафіксованого на коміті, у `agent-harnesses-overrides.json`. Інтерфейс не кодує місце виконання чи володіння циклом.

Докази використовують `confirmed`, `claimed`, `unknown` або `not_applicable`. `unknown` не означає, що можливості немає. `owns_loop` використовує `confirmed`, `claimed`, `unknown` або `no`. Екстрактор ніколи не запускає агента й не надсилає текст README моделі. Він видає детерміновані пропозиції `unknown` для ручної перевірки. Зовнішні пропозиції лишаються вхідними даними для перевірки й ніколи не публікуються автоматично.

Кожна пропозиція екстракції прив'язує свій вхід до канонічного URL репозиторію GitHub, шляху README відносно репозиторію та SHA-256 фактично прочитаних байтів. Сирий вміст README і локальні шляхи файлової системи до пропозиції не копіюються.

Перебудуйте й перевірте без доступу до мережі:

```bash
python3 scripts/build-agent-harnesses.py \
  --source machine-readable/sources/best-of-agent-harnesses-ece314654d2c.json \
  --overrides machine-readable/agent-harnesses-overrides.json \
  --output machine-readable/agent-harnesses.json
python3 scripts/build-agent-harnesses.py \
  --source machine-readable/sources/best-of-agent-harnesses-ece314654d2c.json \
  --overrides machine-readable/agent-harnesses-overrides.json \
  --output machine-readable/agent-harnesses.json \
  --check
uv run --offline --with jsonschema python scripts/test-agent-harnesses.py
```

Команда тестів `uv` є обов'язковим бар'єром перевірки. Вона завжди завантажує `jsonschema` і перевіряє як закомічений каталог, так і ворожі свідчення для схеми; виконавець тестів одразу завершується, якщо `jsonschema` недоступний.

Оновлюйте вихідні дані upstream свідомо за допомогою `scripts/collect-agent-harnesses.py`. Збирач відхиляє будь-який початковий знімок, у якому вже немає рівно 160 проєктів, 12 категорій і потрібної ліцензії. Новий upstream-коміт вимагає переглянутого оновлення контракту, а не тихої зміни кількості.

### Супровідний файл метаданих GitHub

Запланований workflow `Collect Agent Harness GitHub Metadata` працює лише на читання. Він виводить 179 канонічних URL репозиторіїв з `agent-harnesses.json`, надсилає послідовні запити до GitHub API із зафіксованою версією API `2022-11-28` і завантажує артефакт-кандидат на 14 днів. Кеш Actions, ключований за контрольною сумою, зберігає перевірені ETag між запусками, не перетинаючи ревізій каталогу. Він ніколи не комітить і не відкриває pull request.

Збирач завершується з помилкою за замкненою схемою (fail closed) у разі відсутнього токена, неповного результату, HTTP-помилки (включно з 404 чи 429), перейменування, дубліката, розбіжності кількості або розбіжності контрольної суми каталогу. Він записує атомарно лише після того, як усі репозиторії пройшли перевірку. `license_spdx` є спостереженням GitHub і ніколи не замінює редакційний `license_signal`; супровідний файл ніколи не змінює `freshness.checked_at`.

Щоб зібрати кандидата локально, спершу запишіть його поза репозиторієм:

```bash
GITHUB_TOKEN=... python3 scripts/collect-agent-harnesses-github.py \
  --catalog machine-readable/agent-harnesses.json \
  --output /tmp/agent-harnesses-github.json \
  --captured-at "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
```

Просування є окремою людською перевіркою. Спершу перевірте повний супровідний файл і відрендеріть його в тимчасову сторінку. Це перевіряє перерахункову контрольну суму каталогу, версію схеми, точні поля, мітки часу, ідентичності репозиторіїв, кількість, порядок і невід'ємні зірки, не змінюючи опублікованої сторінки:

```bash
cp guide/ecosystem/agent-harness-landscape.md /tmp/agent-harness-landscape-candidate.md
python3 scripts/build-agent-harness-page.py \
  --catalog machine-readable/agent-harnesses.json \
  --github-sidecar /tmp/agent-harnesses-github.json \
  --page /tmp/agent-harness-landscape-candidate.md
```

Після перегляду різниці метаданих скопіюйте кандидата і в `machine-readable/agent-harnesses-github.json`, і в `mcp-server/content/agent-harnesses-github.json`, а тоді перевірте побайтове дзеркало. Будівник сторінки може явно спожити просунутий супровідний файл, зберігаючи резервний варіант із каталогу:

```bash
python3 scripts/build-agent-harness-page.py \
  --catalog machine-readable/agent-harnesses.json \
  --github-sidecar machine-readable/agent-harnesses-github.json \
  --page guide/ecosystem/agent-harness-landscape.md \
  --check
diff -q machine-readable/agent-harnesses-github.json mcp-server/content/agent-harnesses-github.json
```

## Супровід

`version` угорі `reference.yaml` має збігатися з кореневим файлом `VERSION`; `updated` фіксує дату ревізії індексу. Запустіть `./scripts/sync-version.sh --check` перед комітом.

`latest` у `claude-code-releases.yaml` також керує реченням про версію Claude Code в усіх трьох дзеркалах `llms.txt`. Оновлення релізу має змінювати кореневий `llms.txt`, `machine-readable/llms.txt` і `mcp-server/content/llms.txt` разом. Тест документації MCP перевіряє і побайтову рівність, і збіг версій:

```bash
(cd mcp-server && node --test --test-name-pattern='canonical MCP guide is complete' test/render-product-docs.test.mjs)
```

Той самий тест виконується в `npm run release:check` у CI. Він доводить локальну узгодженість реєстру та індексів, а не те, що реєстр релізів збігається з актуальним changelog Anthropic.

Тримайте `reference.yaml` побайтово ідентичним до `mcp-server/content/reference.yaml` після редагування індексу. Оновлюйте описи для виявлення, коли змінюється покриття, і зберігайте вихідні оцінки окремо від доказів реалізації.

Якорі та номери рядків зсуваються, коли файли посібника реструктуризуються. Після великого редагування `guide/` перевірте, що кожен `path#anchor` у `reference.yaml` і далі веде до справжнього заголовка, а кожен `path:N` лишається в межах свого файлу.

Додавання, видалення чи перейменування ключа `deep_dive` змінює палітру Cmd+K на сайті лендингу. Перебудуйте її з репозиторію лендингу командою `pnpm build:search`.

Зміна публічної групи навігації, маршруту, мітки чи вихідного шляху вимагає `python3 scripts/sync-navigation.py --write` тут і збірки лендингу з актуальним репозиторієм посібника, доступним через `GUIDE_REPO_PATH` або типовий сусідній шлях.

---

*Назад до [головного README](../README.uk.md)*
