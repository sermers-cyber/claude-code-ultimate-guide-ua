---
title: "AI Executive Agents: віртуальні C-suite та симулятори рад директорів"
description: "Як далеко заходить патерн persona/agent, коли його застосовують до іменованих керівних ролей (CFO, CMO, CHRO, General Counsel, рада директорів): детальний розбір OpenExecutive, відкриті альтернативи, таблиця вибору за роллю та питання «доповнення чи заміна»"
tags: [ecosystem, multi-agent, orchestration, personas]
---

# AI executive agents: віртуальні C-suite та симулятори рад директорів

> **Рівень достовірності**: змішаний. OpenExecutive, Gstack і crewAI належать до Tier 1/2 (перевірено за вихідними репозиторіями, активна розробка). Більшість інших open-source проєктів у цьому списку належать до Tier 3 (від однозначної кількості до кількох сотень зірок на GitHub, рання стадія, перевіряйте перед впровадженням). Комерційні продукти наведено за твердженнями вендорів, незалежного аудиту не було.

**Час читання**: ~12 хв
**Передумови**: [Multi-agent orchestration](../workflows/README.uk.md), [Cognitive Mode Switching (Gstack)](../workflows/gstack-workflow.uk.md)
**Пов'язане**: [AI Ecosystem](./ai-ecosystem.uk.md), [Third-Party Tools](./third-party-tools.uk.md), [AI Roles](../roles/ai-roles.uk.md)

---

## TL;DR

Патерн persona/agent, який набори skills для Claude Code застосовують до інженерних ролей (див. [Gstack](../workflows/gstack-workflow.uk.md)), тепер переносять на іменовані бізнес-ролі керівників: CFO, CMO, CHRO, General Counsel, COO, рада директорів. [OpenExecutive](https://github.com/SenteLabsAI/OpenExecutive) — найповніший відкритий приклад: 8 спеціалізованих агентів Claude за єдиною цілісною персоною «Executive». Є й аналоги, але здебільшого невеликі й на ранній стадії. Майже жоден із цих проєктів не претендує на юридичні чи фідуціарні повноваження: уся категорія позиціонує себе як доповнення, а не заміну, хоч би яким агресивним був маркетинговий текст.

```
Persona          →  a role definition layered on a general model (tone, scope, priorities)
Agent            →  a persona + tools + state + goal-directed multi-step behavior
AI executive     →  an agent explicitly named after a C-suite/board role, with enough
                     autonomy and persistence to be treated as a virtual team member
```

---

## Gstack — це не ця категорія

Перш ніж іти далі: [Gstack](../workflows/gstack-workflow.uk.md) (Гаррі Тан, 124,8K+ зірок) — це набір із 6 skills для **розробки програмного забезпечення** (`/plan-ceo-review`, `/plan-eng-review`, `/review`, `/ship`, `/browse`, `/retro`). Назва команди `/plan-ceo-review` може збивати з пантелику, але це етап перевірки продукту перед реалізацією всередині coding-сесії, а не персона, що імітує Chief Executive Officer для бізнес-рішень. Якщо ви потрапили сюди, шукаючи Gstack через назву цієї команди, дивіться [Cognitive Mode Switching](../workflows/gstack-workflow.uk.md). Спільне між Gstack і проєктами нижче — базова архітектура: визначення ролей + спільний контекст + робочі процеси зі slash-командами в одному репозиторії. Цей патерн — наскрізна нитка цієї сторінки, застосована до іншої сфери.

---

## OpenExecutive: еталонна архітектура

[OpenExecutive](https://github.com/SenteLabsAI/OpenExecutive) (SenteLabsAI, Apache 2.0, 838 зірок станом на 2026-08-27) — найвиразніше відображення патерну persona/agent на стандартний виконавчий комітет. Вісім спеціалізованих агентів Claude стоять за однією цілісною персоною «Executive» і ніколи не відкриваються користувачеві окремо:

```
User message
    ↓
Executive Orchestrator (claude-sonnet-4-6)
    ↓ tool use → parallel specialist calls
CSO / CFO / CHRO / GC / COO / CMO / CPO / Board Communications
    ↓ each specialist retrieves relevant context from ChromaDB
Built-in MBA knowledge + company documents
    ↓
Synthesized executive response
```

Стек: бекенд на Python 3.11 + FastAPI, UI на Next.js 15, ChromaDB для RAG (вбудована база знань + завантажені документи компанії, дві окремі колекції), SQLite для епізодичної пам'яті (фоновий прохід `claude-haiku-4-5` витягує рішення після кожної відповіді), одноекземплярний планувальник для проактивних повторних звернень та інтеграції зі Slack, email, Telegram, Google Chat і Discord. `claude-opus-4-7` відповідає за глибокі міркування для CSO/CFO/GC/Board; решта за замовчуванням працює на `claude-sonnet-4-6`. Замість Anthropic API проєкт також може працювати через OpenRouter або локальні OpenAI-сумісні сервери (Ollama, LM Studio, vLLM).

Два моменти варто позначити, а не приймати на віру. По-перше, гасло «Harvard MBA-level knowledge» — це маркетинговий текст, а не перевірене твердження: база знань — це Markdown-корпус під git, завантажений у ChromaDB, а її реальна глибина тут не аудитувалася. По-друге, у README не задокументовано жодного явного запобіжника, що відрізняв би «це рекомендація» від «це рішення», хоча агенти General Counsel і Board Communications зачіпають юридичну та управлінську сфери, де ця різниця найважливіша. Що справді добре: кешування промптів побудовано правильно (persona, профіль компанії та індекс знань кешуються окремо, динамічний RAG-контент вставляється в повідомлення користувача, а ніколи не в кешований системний промпт), і проєкт постачається зі справжнім eval-бар'єром: 29 сценаріїв у всіх 8 доменах, які оцінює `claude-opus-4-7` як LLM-as-judge за 5 вимірами; CI-бар'єр вимагає середнього балу ≥3,5/5 і блокує будь-який вимір, що просів більш ніж на 10% порівняно з `main`.

---

## Open-source альтернативи OpenExecutive

Перевірено безпосередньо через GitHub API 2026-08-27, а не за вторинними переказами (попередній дослідницький прохід для цієї сторінки цитував завищені або хибні цифри з блогів; так само ставтеся до будь-яких тверджень про AI-executive-agent, які читаєте деінде, доки не перевірите репозиторій самостійно).

| Проєкт | Автор | Зірки | Ліцензія | Останній push | Ролі | Відмінність |
|---|---|---|---|---|---|---|
| [OpenExecutive](https://github.com/SenteLabsAI/OpenExecutive) | SenteLabsAI | 838 | Apache 2.0 | 2026-08-26 | CSO, CFO, CHRO, GC, COO, CMO, CPO, Board Comms | Найповніше відображення на стандартний C-suite; eval-набір production-рівня |
| [Become CEO](https://github.com/wanikua/become-ceo) | wanikua | 60 | MIT | 2026-03-13 | Engineering, Finance, Marketing, DevOps, Legal, Management, Chief of Staff | Нативний для Discord: 7 ботів, по одному на роль, побудовані на фреймворку Clawdbot |
| [OneManCompany](https://github.com/1mancompany/OneManCompany) | 1mancompany | 398 | Apache 2.0 | 2026-08-26 | Визначаються користувачем (не наперед задані) | Не набір персон. «Агентна операційна система», що оркеструє ієрархічні команди агентів на рівень вище за інструменти на кшталт Claude Code / Codex |
| [AI CFO Agent](https://github.com/daniel-st3/ai-cfo-agent) | daniel-st3 | 7 | не виявлено | 2026-03-08 | Лише CFO | Вузький і дешевий: FastAPI + LangGraph + Next.js + Claude Haiku, від завантаження CSV до дашборда для ради директорів, заявлені $0,003 за запуск |
| [Quorum Virtual Board](https://github.com/granman3/quorum-virtual-board) | granman3 | 0 | не виявлено | 2026-02-22 | Рада з 4 членів | Формат дебатів замість консенсусу: агентів спонукають заперечувати одне одному, а не сходитися. Фактично нікому не відомий (0 зірок, немає файлу ліцензії, тобто за замовчуванням права на повторне використання не надаються) |
| [crewAI](https://github.com/crewaiinc/crewai) | crewAI Inc | 57 664 | MIT | 2026-08-27 | Немає (фреймворк) | Не executive-продукт. Універсальна основа для multi-agent оркестрації, на якій, імовірно, побудовано кілька вендорських інструментів у цій галузі |

Сприймайте кількість зірок як ознаку зрілості, а не якості: проєкт із 7 чи 0 зірок може бути технічно якісним, це лише означає, що майже ніхто ще не дивився на його код. Відсутність файлу ліцензії в Quorum Virtual Board — реальна перешкода для впровадження, а не формальність: без неї діє типове авторське право, і ви не маєте юридичного права повторно використовувати, змінювати чи самостійно розгортати цей код.

---

## Таблиця вибору: який проєкт для якої ролі

| Що шукаєте | Open source | Комерційні | Примітка |
|---|---|---|---|
| Повну віртуальну керівну команду | OpenExecutive · Become CEO · OneManCompany (збери сам) | BattleTested (62 агенти / 10 відділів) · Ghost CEO (AI Boardroom) | OpenExecutive має найповніше відображення стандартного C-suite; Become CEO міняє широту охоплення на інтерфейс, нативний для Discord |
| CFO | [AI CFO Agent](https://github.com/daniel-st3/ai-cfo-agent) | [Nume](https://www.nume.ai/) · [Zeni AI CFO Agent](https://www.zeni.ai/ai-agents/ai-cfo-agent) | AI CFO Agent розгортається самостійно й вузький (лише фінансові дашборди для стартапів) |
| CMO | не знайдено | [Okara](https://okara.ai/) · [Improvado](https://improvado.io/blog/ai-cmo) (концепція, а не окремий продукт) | У цьому дослідженні не знайшлося жодного достовірного open-source AI CMO |
| COO | не знайдено | [Tericsoft](https://www.tericsoft.com/blogs/ai-coo-fleet-operations-agent) | Вузькогалузевий (управління автопарком), не універсальний |
| CHRO / People | не знайдено | жоден не позиціонується як «AI CHRO» | Підтверджена прогалина. HR-обов'язки розподілені між Phenom, Greenhouse, HireVue, Pymetrics, Culture Amp, BetterUp, Workday Adaptive Planning, Oracle Cloud HCM, і жоден не просувається як керівна персона |
| General Counsel / Legal | GC-агент OpenExecutive · Legal-бот Become CEO (обидва вбудовані, не окремі) | [GC AI](https://gc.ai/) | Окремого open-source «AI General Counsel» не знайдено |
| Chief of Staff | Chief of Staff-бот Become CEO (вбудований) | [alfred_](https://get-alfred.ai/ai-chief-of-staff) · Lindy AI Chief of Staff · [Viktor](https://viktor.com/ai-chief-of-staff) | Найзріліша комерційна категорія в усьому цьому ландшафті: сортування пошти/календаря (alfred_), виконання SaaS-процесів (Lindy), операції в Slack/Teams (Viktor) |
| Продажі / CRO | CSO-агент OpenExecutive (вбудований) | [Salesforce Agentforce](https://www.salesforce.com/sales/ai-sales-agent/guide/) · [Veetee AI Chief Sales Officer](https://veeteetechnologies.com/artificial-intelligence-leadership) | Перевага Salesforce — прямий доступ до даних CRM, а не якість моделі |
| Рада директорів / радники | [Quorum Virtual Board](https://github.com/granman3/quorum-virtual-board) (0 зірок, без ліцензії) | [Diligent AI Board Member](https://ai.boardroom.diligentoneplatform.com/) · Personal Board AI (споживчий) | Diligent заявляє про сотні активних користувачів-директорів; Quorum — єдина знайдена open-source реалізація дебатів ради, але фактично не має користувачів |
| Зібрати власне з нуля | [crewAI](https://github.com/crewaiinc/crewai) | - | Універсальний фреймворк, а не продукт із персонами |

---

## Доповнення, а не заміна (поки що)

У всіх оглянутих проєктах маркетингова мова коливається від обережної до агресивної («не потрібен штатний CFO»), але жоден не заявляє про юридичну суб'єктність, фідуціарний обов'язок чи право остаточного рішення. Найближчий до теоретичного винятку — концепція **Synthetic Director**, яку 2023 року запропонувала юридична фірма Stirling & Rose: ШІ-система, зареєстрована в регулятора, з унікальним ідентифікатором, що проходить «тест функціональної компетентності» щодо реальних обов'язків директора (запобігання торгівлі в стані неплатоспроможності, дотримання зобов'язань за статутом), з повноваженням призупинити чи припинити її роботу за аномальної поведінки. Такої рамки сьогодні не існує в законодавстві жодної юрисдикції. Знати про неї варто, бо це єдина серйозна спроба визначити, якою взагалі була б підзвітність, якби комусь із цих агентів колись надали реальну владу, а не тому, що якийсь продукт тут близький до відповідності.

Два бар'єри впровадження діють незалежно від того, наскільки б не вдосконалювалася базова модель. По-перше, інтеграція даних: AI CFO чи AI CMO настільки хороший, наскільки хороші бухгалтерські, CRM- та рекламні дані, до яких він реально має доступ, а в більшості організацій дані брудніші, ніж у демо. По-друге, терміни відповідності EU AI Act і відсутність судової практики щодо рішень керівників, на які вплинув ШІ, означають, що будь-який агент, який торкається найму, звільнення чи фінансового розкриття, опиняється в справді невизначеній правовій зоні, а не лише в зоні обережних формулювань вендорів.

Про загальне бачення Claude Code щодо доповнення проти заміни (інший контекст — інструменти розробки, а не бізнес-ролі, але та сама філософія) дивіться [AI Ecosystem: Augmentation, Not Replacement](./ai-ecosystem.uk.md#philosophy-augmentation-not-replacement).

---

## Коли справді варто використовувати щось із цього

- **Хочете побачити патерн, реалізований наскрізно**: прочитайте вихідний код [OpenExecutive](https://github.com/SenteLabsAI/OpenExecutive). Це найповніша еталонна архітектура в цьому списку, а Apache 2.0 дозволяє форкнути її під власну предметну область.
- **Хочете вузького, дешевого агента з однією роллю**: AI CFO Agent (CFO) або схожий вузький комерційний інструмент — менша ставка, ніж упровадження цілої віртуальної керівної команди.
- **Хочете операційного сортування в стилі chief-of-staff уже сьогодні**: це єдина категорія зі зрілими комерційними продуктами, що мають фінансування (alfred_, Lindy, Viktor). Не будуйте це самі першим ділом.
- **Шукаєте AI CHRO**: як брендований продукт його ще не існує. Складіть натомість інструменти для рекрутингу (Phenom, Greenhouse), оцінювання (Culture Amp, BetterUp) і планування персоналу (Workday Adaptive Planning) або побудуйте шар оркестрації самі на crewAI.
- **Оцінюєте це для реального рішення ради чи юридичного питання**: ніщо в цьому списку не має фідуціарних чи юридичних повноважень. Вважайте кожен вивід рекомендацією, яку людина має перевірити, а не рішенням.

---

## Джерела

- [OpenExecutive](https://github.com/SenteLabsAI/OpenExecutive), [Become CEO](https://github.com/wanikua/become-ceo), [Quorum Virtual Board](https://github.com/granman3/quorum-virtual-board), [OneManCompany](https://github.com/1mancompany/OneManCompany), [AI CFO Agent](https://github.com/daniel-st3/ai-cfo-agent), [crewAI](https://github.com/crewaiinc/crewai): кількість зірок, ліцензії та дати останнього push отримано безпосередньо з GitHub API 2026-08-27.
- [Nume](https://www.nume.ai/), [Zeni AI CFO Agent](https://www.zeni.ai/ai-agents/ai-cfo-agent), [Okara](https://okara.ai/), [Improvado](https://improvado.io/blog/ai-cmo), [Tericsoft](https://www.tericsoft.com/blogs/ai-coo-fleet-operations-agent), [Diligent AI Board Member](https://ai.boardroom.diligentoneplatform.com/), [GC AI](https://gc.ai/), [Veetee Technologies](https://veeteetechnologies.com/artificial-intelligence-leadership), [Salesforce AI Sales Agents](https://www.salesforce.com/sales/ai-sales-agent/guide/), [alfred_](https://get-alfred.ai/ai-chief-of-staff), [Viktor](https://viktor.com/ai-chief-of-staff): сторінки продуктів, опубліковані вендорами; заяви про популярність і точність незалежно не аудитувалися.
- [Synthetic Directors: The Hybrid Boardroom](https://stirlingandrose.com/insights/posts/synthetic-directors-the-hybrid-boardroom-of-ai-and-human-collaboration/) (Stirling & Rose, 2023).
- [AI and the CHRO](https://www.imd.org/ibyimd/human-resources/ai-and-the-chro-redefining-human-capital-leadership/) (IMD) щодо прогалини AI-CHRO та суміжних HR-інструментів.
