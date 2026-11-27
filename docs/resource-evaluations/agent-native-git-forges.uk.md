# Агентно-нативні Git-форжі: Entire, Cursor Origin, Cloudflare Artifacts, Anthropic Scion

**Переглянуто:** 27 жовтня 2026 року. **Привід:** запуск Entire повноцінного Git-форжу 26 жовтня 2026 року. **Рішення:** інтегрувати короткий оглядовий розділ у [Сторонні інструменти](../../guide/ecosystem/third-party-tools.uk.md#агентно-нативні-git-форжі-2026) і виправити кожен наявний фрагмент посібника про Entire CLI відповідно до поточної документації Entire.

Оцінки вимірюють редакційну цінність для цього посібника, а не якість, безпеку чи продуктивність продукту. Для цієї оцінки жоден продукт не встановлювали й не запускали. Кожне твердження нижче перечитано в першоджерелі 27 жовтня 2026 року. Ширший вторинний огляд (преса, Hacker News, конкуренти) використовувався лише для пошуку кандидатів; твердження, знайдені тільки там, не включено.

## Прочитані джерела

| Джерело | Що воно встановило |
|---|---|
| [Допис про запуск Entire](https://entire.com/blog/the-git-forge-for-agent-human-collaboration) (26 жовтня 2026 року) | Trails, Gates, розподілений хостинг, режим дзеркала, Continuous Memory, CI від Buildkite і Depot, цифри ForgeMark |
| [entire.com/llms.txt](https://entire.com/llms.txt) і його сторінки `.md` (trails, code-hosting, cli, sessions, projects) | Охоплення продукту, позначки превʼю та експериментальних функцій, підтримка subagents, редагування чутливих даних |
| [Регіони хостингу](https://entire.com/regions) (чинні з 19 жовтня 2026 року) | Шість регіонів, а не чотири, названі в дописі про запуск |
| [Credit Terms](https://entire.com/credit-terms) (чинні з 26 жовтня 2026 року) | Передплачені кредити для оплати Paid Features |
| [Data Processing Agreement](https://entire.com/dpa) | SOC 2 і ISO 27001 згадано лише щодо постачальників хмарної інфраструктури Entire |
| [README Entire CLI](https://github.com/entireio/cli) і [довідник CLI](https://docs.entire.com/cli-reference) | Реальний набір команд (зокрема `blame`, `why`, `checkpoint delete`), способи встановлення, ліцензія MIT, підтримка Windows |
| [Session Storage](https://docs.entire.com/guides/checkpoints/checkpoint-storage) і [Security & Privacy](https://docs.entire.com/security) (перевірено Entire для CLI 0.10.2) | Зберігання в refs за замовчуванням з 0.10.0, застаріле зберігання в гілці, тіньові гілки, шари й обмеження редагування чутливих даних |
| [Anthropic, Redesigning source control](https://www.anthropic.com/research/redesigning-source-control) (13 жовтня, оновлено 15 жовтня 2026 року) | Scion, `scn`, Antique, серверні коміти, внутрішні цифри обсягів, позиція щодо черги злиття, «not a suitable replacement for git for general use» |
| [Cloudflare Artifacts](https://blog.cloudflare.com/artifacts-git-for-agents-beta/) (16 квітня 2026 року) | Версіоноване сховище з Git-протоколом для агентів, закрита бета, ціни на час бети |
| [Оголошення Cursor Origin](https://forum.cursor.com/t/origin-code-hosting/168670) (17 серпня 2026 року) | Рання бета, лише платні плани, GitHub як джерело істини для синхронізованих репозиторіїв |

## Рішення щодо кандидатів

| Кандидат | Оцінка | Особливий внесок | Рішення |
|---|---|---|---|
| Форж Entire (Trails, хостинг, пам'ять) | 4/5 | Перший форж, що замінює pull request рев'ю з оцінкою від агентів і Gates для злиття; розширює вже задокументований Entire CLI | Оглядовий розділ плюс виправлене охоплення CLI |
| Anthropic Scion | 3/5 | Першоджерельні дані про обсяг злиттів у масштабі агентів і про те, чому класична черга злиття ламається; це не продукт | Один абзац, поданий як урок, а не інструмент |
| Cursor Origin | 3/5 | Хостинг усередині агентного IDE, де GitHub лишається джерелом істини | Один рядок |
| Cloudflare Artifacts | 3/5 | Програмоване Git-сховище, один репозиторій на сесію агента | Один рядок; пізніший статус бети не перевіряли повторно |

## Виправлення наявного вмісту посібника

Охоплення Entire CLI за лютий 2026 року ([оцінка](./entire-cli.uk.md)) містило твердження, яких поточна документація не підтверджує:

| Попереднє твердження | Що каже поточне джерело | Виправлення |
|---|---|---|
| «SOC2 Type II certified» | Атестації для Entire не знайдено; DPA згадує SOC 2 і ISO 27001 лише щодо постачальників інфраструктури | Прибрано; зазначено, що не знайдено |
| Команди `entire init`, `capture`, `checkpoint --name`, `log`, `rewind`, `handoff`, `approve --approver`, `review --checkpoint`, `audit-export`, `--compliance-mode` | Відсутні в [довіднику CLI](https://docs.entire.com/cli-reference) | Замінено на `enable`, `checkpoint list/explain`, `session resume`, `search`, `why`, `trail approve/merge` |
| Шифрування AES-256 у стані спокою, стовпець FedRAMP | Не задокументовано | Прибрано |
| Чекпоінти в orphan-гілці `entire/checkpoints/v1` | Зберігання в refs під `refs/entire/checkpoints/` є типовим з CLI 0.10.0; гілка лишається для старіших репозиторіїв | Оновлено з обома бекендами |
| Написано на TypeScript; лише macOS/Linux, Windows через WSL | CLI на Go; інсталятор для Windows PowerShell | Оновлено |
| Gates затвердження як локальна функція CLI | Gates належать до Trails на хмарному форжі | Оновлено |
| «Path-agnostic» чекпоінти з відносними шляхами | Не задокументовано; чекпоінти переносяться, бо це Git refs | Переформульовано, відновлення з іншої теки позначено як неперевірене |
| Накладні витрати на зберігання «~5-10% розміру проєкту» | Не задокументовано | Замінено процедурою вимірювання |

## Що не перевірено

- Результати ForgeMark від Entire (418 пушів на секунду для Entire проти 4,7 для GitHub) і економія токенів «до 71%» у entire-graph: вимірювання постачальника, незалежного відтворення не знайдено
- Статус Cloudflare Artifacts після квітня 2026 року
- Яка частина відновленої сесії Claude Code переживає зміну шляху проєкту
- Конкуренти, які трапилися лише у вторинних джерелах (Pierre, GitHub Agent HQ, GitLab Duo Agent Platform, Bitbucket Agentic Pipelines, GitButler, Jujutsu, Graphite, Agent Trace та інші), повторно не перечитувалися й не цитуються в посібнику на підставі цієї оцінки

## Відстеження

Entire публікує індекс на [entire.com/llms.txt](https://entire.com/llms.txt) і нумерований журнал змін «dispatch». Перечитування цього індексу й довідника CLI — найдешевший спосіб тримати посібник актуальним. Повернутися до цієї оцінки, коли Entire CLI досягне 1.0, коли Entire опублікує атестацію відповідності або коли з'явиться незалежне відтворення ForgeMark.
