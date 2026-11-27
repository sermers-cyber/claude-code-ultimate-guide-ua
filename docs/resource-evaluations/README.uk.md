# Оцінки ресурсів

Ця тека містить оцінки зовнішніх ресурсів (статей, відео, обговорень), щоб визначити їхню релевантність для Claude Code Ultimate Guide.

## Методологія

Кожен ресурс оцінюється за стандартизованою системою балів, а технічний агент перевіряє оцінку запереченнями, щоб гарантувати об'єктивність.

### Шкала оцінок (з 5)

| Оцінка | Значення | Дія |
|-------|---------------|--------|
| 5 | **Critical**: прорив, інтегрувати негайно | Інтегрувати протягом 24 год |
| 4 | **High Value**: нова можливість або суттєве покращення | Інтегрувати протягом 1 тижня |
| 3 | **Moderate**: корисне доповнення, але не термінове | Інтегрувати, якщо є час |
| 2 | **Marginal**: другорядна інформація або нішевий сценарій | Не інтегрувати (або мінімальна згадка) |
| 1 | **Low**: надлишкове, некоректне або поза темою | Відхилити |

### Процес

1. **Початковий аналіз**: вилучення фактів, перевірка джерел
2. **Оцінювання**: присвоєння оцінки з обґрунтуванням
3. **Заперечення**: агент technical-writer ставить оцінку під сумнів
4. **Остаточне рішення**: інтеграція або відхилення з простежуваністю

### Іменування файлів

Формат: `[topic-slug].md` (дату прибрано для стабільності посилань)

Приклад: `remotion-claude-code-video.md`

## Робочі документи

Сирі робочі документи (промпти Perplexity, клієнтські аудити) лишаються в `claudedocs/resource-evaluations/` (у gitignore).

## Індекс оцінок

| Ресурс | Початкова оцінка | Фінальна оцінка | Рішення | Файл |
|-----------|---------------|-------------|----------|---------|
| **GenAI Days Nantes, звіт Emmanuel Sciara** (19 листопада 2026) | 3/5 | **3/5** | Цільова інтеграція: спеціалізовані оцінювачі й калібрування, чемпіони та навчання за ролями, явні процедури підтримки. Вторинна розповідь, без перевірених записів виступів чи порівняння продуктивності. | [genai-days-nantes-sciara.md](./genai-days-nantes-sciara.uk.md) |
| **git-ai** (атрибуція ШІ на рівні рядків у git notes, зібрано з вихідного коду на `5420ab9` і протестовано) | 4/5 | **4/5** | Інтегровано в ai-traceability.md §3.4 і новий §3.5 «Provenance in git notes» плюс діаграму в 12-enterprise-governance.md: нотатка в `refs/notes/ai` зберігається після amend, rebase і `git merge --squash` у локальному тесті з пресетом `mock_ai`; простий `notes.rewriteRef` охоплює amend і rebase, але не squash; переписування кнопкою злиття на форжі, cherry-pick і пуш нотаток git-ai не тестувалися; необґрунтоване твердження «AI Code Halflife 3.33 years» відкликано | [git-ai-provenance-notes.md](./git-ai-provenance-notes.uk.md) |
| **Локальні поверхні рев'ю для змін, написаних агентами** (diffo, glassbox, hunk, drift, ai-pr-review, guidedreview) | 4/5, 3/5, 3/5, 3/5, 2/5, 2/5 | **4/5, 3/5, 3/5, 3/5, 2/5, 2/5** | Інтегровано як порівняльну таблицю в multi-provider-code-review.md (інтерактивні помічники проти CI) і діаграму в 06-development-workflows.md: жоден із п'яти, чий код прочитано, не показує пояснення агента в колонці поруч із diff, лише diffo типізує відгуки рев'юера, у прочитаних версіях лише drift читає й пише обговорення GitLab; застереження з безпеки щодо ai-pr-review, який запускає Codex з доступом до мережі на коді pull request; прочитано статично, нічого не запускали | [agent-review-surfaces.md](./agent-review-surfaces.uk.md) |
| **Трейси походження агентних змін** (специфікація Agent Trace, `Dillonsmart/docket`, `wasabeef/AgentNote`) | 3/5, 3/5, 2/5 | **3/5, 3/5, 2/5** | Використано в ai-traceability.md §3.5 «Provenance in git notes» (прочитано, не запускали): форма запису Agent Trace і хеш вмісту діапазону як еталонний формат (RFC 0.1.0, канонічний `cursor/agent-trace` 2026-11-08 не знайдено, прочитано копію `superhq-dev`), docket як дизайн, орієнтований на рев'юера (намір і щільність доказів для кожного hunk), AgentNote як застереження (нецензуровані транскрипти пушаться; згідно з кодом і документацією нотатки, прив'язані до SHA, осиротіють після переписування, не тестувалося). Відрізняється від рекордера `agent-trace` від Siddhant | [agent-provenance-traces.md](./agent-provenance-traces.uk.md) |
| **Три доповіді про рев'ю змін, написаних агентами** (Geoffrey Litt, Sachin Gupta, Ryan Lopopolo) | 4/5, 3/5, 3/5 | **4/5, 3/5, 3/5** | Збережено для запланованої сторінки воркфлоу про агентні зміни, придатні до рев'ю, ще не інтегровано: пояснювальний документ Litt і gate з тестом для автора, критерій опису «чому, а не що» від Gupta й межі атрибуції через trailers, дозвіл від Lopopolo агентові відкладати відгуки або заперечувати їм; цифри Faros AI, які цитує Gupta, вторинні й не використовуються | [reviewable-agent-changes-talks.md](./reviewable-agent-changes-talks.uk.md) |
| **Resisting Cognitive Surrender** (есей knlb.dev, листопад 2026) | 3/5 | **3/5** | Інтегровано як короткий фрагмент у learning-with-ai.md (третій режим рев'ю): визначення, тривожна ознака «так, продовжуй», тактики розуміння, зокрема перегляд pull request з поточним коментарем агента; Kaufman et al. (arXiv, n=86) як застереження: пояснення згенерованих тверджень не дали загальної користі; доповіді Kerr і Jain як два підходи до рев'ю; нова діаграма «Approve only what you can explain» | [knlb-cognitive-surrender.md](./knlb-cognitive-surrender.uk.md) |
| **Sparks of Weight-Space Programming** (блог MIT CSAIL, `gpt-6-astra` редагує Qwen3.5-0.8B) | 3/5 | **3/5** | Інтегровано як кейс в ai-ecosystem.md §13 (autoresearch): приріст на MATH-500 збігається з виправленням зациклення (93% відповідей базової моделі обрізані), промпт називав повторення, один запуск на бюджет, негативний контроль на Gemma; повторний запуск стороннього чекпоінта підтверджено, опублікованого порівняння з базовою моделлю за налаштувань із картки моделі немає | [weight-space-programming.md](./weight-space-programming.uk.md) |
| **prismantis** (NahumLitvin, мод термінального рендерингу для Claude Code) | 4/5 | **4/5** | Інтегровано: third-party-tools.md «Terminal rendering (mods)» і рядок персони; вартість `diagramHints` наведено як цифру з README (близько 630 токенів на промпт, не виміряно); перевірка валідатором на v0.38.2; перехресне посилання з основного посібника очікує (hook на довге тире) | [prismantis-terminal-rendering-mod.md](./prismantis-terminal-rendering-mod.uk.md) |
| **Агентно-нативні Git-форжі** (Entire forge, Cursor Origin, Cloudflare Artifacts, Anthropic Scion) | 4/5 | **4/5** | Розділ-огляд у сторонніх інструментах; усі фрагменти про Entire CLI виправлено за довідником CLI (атестації SOC 2 не знайдено, неіснуючі команди прибрано, зберігання в refs) | [agent-native-git-forges.md](./agent-native-git-forges.uk.md) |
| **Зіставлення патернів проєктування ШІ** (kage-ai, agentpatterns.ai, aicodingpatterns, roanbrasil, GO4, чотири статті arXiv) | 3/5 | **3/5** | Цитуються як джерела `guide/core/ai-design-patterns.md`: рядки консенсусу й розбіжностей тримаються окремо, кожне зіставлення з Claude Code, якого не наводить жодне джерело, позначено як зіставлення посібника; статті, відомі лише з уривків, попередні; репозиторії на основі витоків виключено | [ai-design-pattern-crosswalks.md](./ai-design-pattern-crosswalks.uk.md) |
| **Agent Harness Engineering Patterns** (ashishpatel26, 192 патерни) | 3/5 | **3/5** | Натхнення й процитоване джерело для `guide/core/ai-design-patterns.md`; ліцензії немає, тож жодного тексту чи діаграми не використано повторно; його додаток з виправленнями лежить в основі антипатернів | [agent-harness-engineering-patterns-ahep.md](./agent-harness-engineering-patterns-ahep.uk.md) |
| **Bruno Boucard: ощадливі agent harnesses** (2026-10-23) | 3/5 | **3/5** | Вибіркова двомовна інтеграція: приклад вартості кешованого вводу/виводу, робочий стан, безпечний для префікса, і пропорційні артефакти; жодного виміряного виграшу від прибирання засобів контролю | [boucard-frugal-agent-harnesses.md](./boucard-frugal-agent-harnesses.uk.md) |
| **Grill me** (gatekeeper від Cherny, офіційна специфікація з інтерв'ю на початку, `grill-me` від Pocock) | 4/5 | **4/5** | Інтегровано в `guide/workflows/spec-first.md`: порівняно три патерни, режими відмови й вимкнення, жодного контрольованого дослідження; дату треду Cherny виправлено на січень 2026 | [grill-me-interview-patterns.md](./grill-me-interview-patterns.uk.md) |
| **Десктопні робочі простори для агентів** (Conductor, Vibe Kanban, Emdash, Superset, Escouade, Opcode, Orca) | Emdash/Superset/Escouade/Orca: 3; Opcode: 2 | **Emdash/Superset/Escouade/Orca: 3; Opcode: 2** | Оновити наявні профілі; Opcode лишити лише в оцінці; додати огляд документації Orca з безперервністю Codex і обмеженнями дозволів (3/5). Локальне випробування Escouade 1.8.8: перевірено планування залежностей, перезапуск/відновлення і злиття через gate тестів; зафіксовано обмеження парсера, підсумків файлів і встановлення, без рейтингу продуктивності | [agent-workspace-cockpits.md](./agent-workspace-cockpits.uk.md) |
| **Lexigraph** (двомовний словник ШІ та порівняння понять) | 3/5 | **3/5** | Вибіркова адаптація: шість розрізнень понять і оригінальні вправи на розуміння; атрибуція CC BY 4.0, прогалини експорту й упередження позиції відповіді задокументовано | [lexigraph-ai-lexicon.md](./lexigraph-ai-lexicon.uk.md) |
| **Lopopolo: антологія Harness Engineering** | 4/5 | **4/5** | Вибіркова інтеграція: володіння істиною, локальна планка якості, телеметрія MLD, кураторська публікація, епохи воркерів і чотири годинники; жодного виконаного плейбука чи локального виграшу не заявлено | [lopopolo-harness-engineering.md](./lopopolo-harness-engineering.uk.md) |
| **Honkonen: протокол «архітектор-інженер»** | 4/5 | **4/5** | Інтегрувати в наявний воркфлоу з двома екземплярами й шаблони передавання; прибрати необґрунтовані гарантії щодо вартості/якості; власні інженерні інструменти не є функцією Claude Code | [honkonen-architect-engineer.md](./honkonen-architect-engineer.uk.md) |
| **WikiSkill** (постійні знання для еволюції skills) | 4/5 | **4/5** | Вибіркова інтеграція: зберігати відхилені пропозиції, відокремлювати навчання від виконання, оцінювати перенесення між моделями; докази з бенчмарків не встановлюють нативної маршрутизації skills чи виграшу в продакшені | [wikiskill-persistent-skill-evolution.md](./wikiskill-persistent-skill-evolution.uk.md) |
| **Grob** (проксі LLM на Rust, DLP і бюджети) | 3/5 | **3/5** | Лише технічний довідник і обмежений пілот: відтворено дві прогалини санітайзера; обмеження fan-out HIT, судді й обліку; жодного схвалення для безпеки в продакшені | [grob-llm-proxy.md](./grob-llm-proxy.uk.md) |
| **Mistral Large 4** (публічний превʼю 6 жовтня) | 3/5 | **3/5** | Вибіркова інтеграція: ціни API, докази з бенчмарків, закупівлі й обмеження майбутнього розгортання ваг; параметри уточнено, контекст і заплановані дати релізу різняться між джерелами | [mistral-large-4.md](./mistral-large-4.uk.md) |
| **shunt** (spotify/portal-ai-plugins, делегування дешевшій моделі через hook) | 3/5 | **3/5** | Інтегровано як патерн: context-engineering-tools.md §3 і таблиця важелів витрат; цифра 90% стосується контексту Claude у 3 приватних сценаріях; лише для Portal; обхід через шлях `~` і блокування PDF підтверджено наживо | [spotify-portal-shunt.md](./spotify-portal-shunt.uk.md) |
| **logseq-wiki** (ystreibel/logseq-wiki, порт obsidian-wiki як LLM Wiki) | 2/5 | **2/5** | Лише кейс: memory-systems.md §7.1 (отруєння однокористувацької вікі на етапі завантаження: headless `--dangerously-skip-permissions` над сторонніми транскриптами, опційне проміжне розміщення не на цьому шляху); 5 зірок, один автор | [logseq-wiki-llm-wiki-port.md](./logseq-wiki-llm-wiki-port.uk.md) |
| **Brownfield Agentic Engineering** (Addy Osmani, вересень 2026) | 4/5 | **4/5** | Інтегровано: зони, незалежні характеризаційні тести, повнота міграції, паралелізація в останню чергу | [osmani-brownfield-agentic-engineering.md](./osmani-brownfield-agentic-engineering.uk.md) |
| **Rewriting Bun in Rust** (Jarred Sumner, липень 2026) | 4/5 | **4/5** | Інтегровано як кейс міграції з Claude Code у розділі посібника 9.21 | [bun-rust-rewrite-claude-code.md](./bun-rust-rewrite-claude-code.uk.md) |
| **From SDLC to ADLC** (Rakesh Gohel, LinkedIn, вересень 2026) | 2/5 | **2/5** | Не інтегровано: переказує плейбук Anthropic; два виправлення зроблено за першоджерелом | [gohel-sdlc-to-adlc-post.md](./gohel-sdlc-to-adlc-post.uk.md) |
| **Доповнення до корпусу про harness** (3 статті, 3 доповіді) | 3-4/5 | **3-4/5** | Вибіркові доповнення: обмеження рев'ю, міграція пам'яті, пояснення, логи, відновлення інструментів і метрики рев'ю | [harness-corpus-supplement-2026.md](./harness-corpus-supplement-2026.uk.md) |
| **Learn Harness Engineering** | 3/5 | **3/5** | Навчальні кейси з відтвореними контрольними перевірками відмов; жодного схвалення каркаса для продакшену | [learn-harness-engineering-2026.md](./learn-harness-engineering-2026.uk.md) |
| **AutoHarness** | 3/5 | **3/5** | Кейс підтримки skills із цільовими контрприкладами; жодного вимірювання користі наживо | [autoharness-2026.md](./autoharness-2026.uk.md) |
| **AI Agents Push Humans Out of the Loop** | 4/5 | **4/5** | Позиційна стаття лежить в основі вправ із нагляду; жодних локальних результатів щодо людей не заявлено | [human-oversight-agents-2608-23642.md](./human-oversight-agents-2608-23642.uk.md) |
| **Marmelab і докази оцінювання harness** | 4/5 | **4/5** | Вибіркова інтеграція: протестовані засоби контролю, абляції рев'юерів, обмеження оцінювання й виправлення файлів контексту | [harness-evidence-marmelab-2026.md](./harness-evidence-marmelab-2026.uk.md) |
| **Jev / TypeSafe AI** (типізовані рішення) | 3/5 | **3/5** | У роботі: докази щодо API, незалежні звіти й критерії експерименту; жодної рекомендації для продакшену | [jev-typesafe-system-one.md](./jev-typesafe-system-one.uk.md) |
| **DarkMoon і Strix** (агентне тестування на проникнення) | 3/5 | **3/5** | Задокументовано порівняння й вимоги до доказів; жодного рейтингу продуктивності чи схвалення для продакшену | [darkmoon-strix-agentic-pentesting.md](./darkmoon-strix-agentic-pentesting.uk.md) |
| **Databricks: Managing AI Coding Costs at Scale** | 4/5 | **4/5** | ✅ Вибіркова інтеграція: трирівнева маршрутизація, поступові бюджети, кеш і роз'яснення meta-harness; внутрішні цифри не узагальнено | [databricks-managing-ai-coding-costs-scale.md](./databricks-managing-ai-coding-costs-scale.uk.md) |
| **Навчальний корпус MLTUT + Awesome Claude Code** | 4/5 | **4/5** | ✅ Інтегровано цільові прогалини, маршрути й матеріали для поширення | [mltut-learning-resources-comparative-audit.md](./mltut-learning-resources-comparative-audit.uk.md) |
| **Поточна поверхня продукту Claude Code** | - | **5/5** | ✅ Інтегровано з офіційної документації від 31 серпня 2026 | [claude-code-current-surface-2026-08.md](./claude-code-current-surface-2026-08.uk.md) |
| **Best-of-N і докази перевірки** | - | **4/5** | ✅ Інтегровано з протоколом, skill і журналом доказів | [best-of-n-verification-evidence.md](./best-of-n-verification-evidence.uk.md) |
| **Релізи Anthropic** (16-23 січня 2026) | - | - | ✅ Регулярне відстеження | [anthropic-releases-jan16-23-2026.md](./anthropic-releases-jan16-23-2026.uk.md) |
| **Caliber** (rely-ai-org/caliber) | 3/5 | 3/5 | ✅ Інтегровано: Configuration Quality | [caliber-config-quality-tool.md](./caliber-config-quality-tool.uk.md) |
| **AST-grep** (Flavien Métivier) | 3/5 | **4/5** | ✅ Інтегрувати воркфлоу | [astgrep-flavien-metivier.md](./astgrep-flavien-metivier.uk.md) |
| **MCP Apps** (SEP-1865) | 3/5 | **4/5** | ✅ Інтегровано (архітектура + посібник) | [mcp-apps-announcement.md](./mcp-apps-announcement.uk.md) |
| **Boris Cherny** (відео Cowork) | 4/5 | **4/5** | ✅ Інтегровано (ментальні моделі) | [boris-cowork-video-eval.md](./boris-cowork-video-eval.uk.md) |
| **Clawdbot** (аналіз у Twitter) | 2/5 | **2/5** | ⚠️ Лише спостереження | [clawdbot-twitter-analysis.md](./clawdbot-twitter-analysis.uk.md) |
| **GSD** (Getting Shit Done) | 4/5 | **4/5** | ✅ Інтегровано (воркфлоу) | [gsd-evaluation.md](./gsd-evaluation.uk.md) |
| **Плагіни Nick Jensen** | 3/5 | **3/5** | ✅ Згадка | [nick-jensen-plugins.md](./nick-jensen-plugins.uk.md) |
| **Стаття про повторення промпта** | 3/5 | **4/5** | ✅ Інтегрувати в найкращі практики | [prompt-repetition-paper.md](./prompt-repetition-paper.uk.md) |
| **Remotion + Claude Code** (виробництво відео) | 2/5 | **3/5** | ✅ Мінімальна згадка | [remotion-claude-code-video.md](./remotion-claude-code-video.uk.md) |
| **Плагін SE-Cove** | 2/5 | **2/5** | ⚠️ Лише спостереження | [se-cove-plugin.md](./se-cove-plugin.uk.md) |
| **Self-Improve Skill** | 3/5 | **3/5** | ✅ Додано шаблон | [self-improve-skill.md](./self-improve-skill.uk.md) |
| **Steinberger** (швидкість інференсу) | 3/5 | **3/5** | ✅ Інтегровано (мінімально) | [steinberger-inference-speed.md](./steinberger-inference-speed.uk.md) |
| **Діаграми UML і ООП** | 3/5 | **3/5** | ✅ Згадка | [uml-oop-diagrams.md](./uml-oop-diagrams.uk.md) |
| **Vibe Coding Level 2** (Rusitschka) | 4/5 | **4/5** | ✅ Інтегровано (воркфлоу) | [vibe-coding-rusitschka.md](./vibe-coding-rusitschka.uk.md) |
| **Peter Wooldridge** (стек продуктивності) | 2/5 | **3/5** | ✅ Practitioner Insights | [wooldridge-productivity-stack.md](./wooldridge-productivity-stack.uk.md) |
| **Системні промпти** (офіційні проти спільнотних) | 4/5 | **2/5** | ⚠️ Лише спостереження (існують офіційні джерела) | [system-prompts-official-vs-community.md](./system-prompts-official-vs-community.uk.md) |
| **Worktrunk** | 4/5 | **4/5** | ✅ Інтегровано (воркфлоу) | [worktrunk-evaluation.md](./worktrunk-evaluation.uk.md) |
| **Pat Cullen** (мультиагентне рев'ю PR) | 5/5 | **5/5** | ✅ Інтегровано (review-pr, code-reviewer, посібник) | [017-pat-cullen-final-review.md](./017-pat-cullen-final-review.uk.md) |
| **Docker Sandboxes** (огляд ізоляції) | 4/5 | **4/5** | ✅ Інтегровано (посібник + довідка) | [docker-sandboxes-isolation.md](./docker-sandboxes-isolation.uk.md) |
| **dclaude** (Claude Code у Docker) | 2/5 | **2/5** | ⚠️ Виноска (sandbox-isolation.md) | [dclaude-docker-wrapper.md](./dclaude-docker-wrapper.uk.md) |
| **10 Tips from Inside the Claude Code Team** (paddo.dev) | 4/5 | **4/5** | ✅ Інтегровано (4 розділи) | [paddo-team-tips-eval.md](./paddo-team-tips-eval.uk.md) |
| **Досвід Sankalp із Claude Code 2.0** | 2/5 | **2/5** | ⚠️ Лише спостереження (85% перекриття, ймовірні помилки) | [sankalp-claude-code-experience.md](./sankalp-claude-code-experience.uk.md) |
| **Kajan Siva** (команда /insights) | 2/5 | **2/5** | ❌ Не інтегрувати (немає технічного змісту) | [kajan-siva-insights-command.md](./kajan-siva-insights-command.uk.md) |
| **Zolkos** (глибокий розбір /insights) | 4/5 | **4/5** | ✅ Інтегрувати (архітектура + аспекти) | [zolkos-insights-deep-dive.md](./zolkos-insights-deep-dive.uk.md) |
| **Grenier** (якість агентів/skills) | 3/5 | **3/5** | ✅ Інтегрувати частково | [grenier-agent-skill-quality.md](./grenier-agent-skill-quality.uk.md) |
| **Awesome Claude Skills** (BehiSecc) | 3/5 | **3/5** | ✅ Спеціалізована згадка | [awesome-claude-skills-github.md](./awesome-claude-skills-github.uk.md) |
| **Wasp Fullstack Essentials** (Vinny @ Wasp) | 3/5 | **3/5** | ✅ Інтегрувати концепції, незалежні від фреймворку | [wasp-fullstack-essentials-eval.md](./wasp-fullstack-essentials-eval.uk.md) |
| **Інфографіка Master Claude Code** (Rakesh Gohel / Aakash Gupta) | 2/5 | **2/5** | ❌ Не інтегрувати (поверхово, помилка щодо Cursor) | [rakesh-gohel-aakash-gupta-master-claude-code.md](./rakesh-gohel-aakash-gupta-master-claude-code.uk.md) |
| **Snyk ToxicSkills** (аудит ланцюга постачання) | 4/5 | **4/5** | ✅ Інтегровано (security-hardening.md §1.1, §1.2, §1.5) | [snyk-toxicskills-evaluation.md](./snyk-toxicskills-evaluation.uk.md) |
| **Системні промпти Opus 4.6** (офіційне оновлення) | 2/5 | **2/5** | ⚠️ Лише спостереження (друга оцінка, той самий URL, уже охоплено) | [system-prompts-opus-4-6-update.md](./system-prompts-opus-4-6-update.uk.md) |
| **Straude** (соціальний трекер використання) | 3/5 | **3/5** | ✅ Інтегровано (third-party-tools.md, аналіз безпеки) | [straude-evaluation.md](./straude-evaluation.uk.md) |
| **qmd Token Savings** (Simone Ruggiero, Medium) | 2/5 | **2/5** | ❌ Не інтегрувати (дублює grepai, твердження неможливо перевірити) | [2026-02-14-simone-ruggiero-qmd-token-savings-medium.md](./2026-02-14-simone-ruggiero-qmd-token-savings-medium.uk.md) |
| **Rippletide** (платформа надійності ШІ) | 2/5 | **2/5** | ⚠️ Лише спостереження (рівні MCP-сервера, твердження неможливо перевірити, немає популярності) | [072-rippletide-ai-reliability-platform.md](./072-rippletide-ai-reliability-platform.uk.md) |
| **Сигнали спільноти й бенчмарк** (зведення за березень 2026) | 4/5 | **3/5** | ✅ Без інтеграції (усі прогалини вже охоплено; виявлено 2 фактичні помилки) | [community-signals-benchmark-march-2026.md](./community-signals-benchmark-march-2026.uk.md) |
| **context-evaluator** (PackmindHub/context-evaluator) | 4/5 | **4/5** | ✅ Інтегровано: third-party-tools.md + 2 патерни в skill-design-patterns.md | [context-evaluator-evaluation.md](./context-evaluator-evaluation.uk.md) |
| **CLI-інструменти liza-mas** (scip-search, mdtoc, functional-clusters, stacklit-cli) | 1-2/5 | **2-3/5** | Переоцінено 2026-10-13: mdtoc і stacklit-cli 3/5, придатні для прикладів у посібнику, але очікують порівняння; scip-search і functional-clusters 2/5 | [liza-mas-token-saving-cli-tools.md](./liza-mas-token-saving-cli-tools.uk.md) |
| **Semble** (MinishLab/semble) | 3/5 | **3/5** | ✅ Інтегровано: розділ Code Search у mcp-servers-ecosystem.md | [semble-code-search.md](./semble-code-search.uk.md) |
| **MDMA** (MobileReality/mdma) | 3/5 | **3/5** | ✅ Інтегровано: ai-ecosystem.md розділ 7.1 (генеративний UI) | [mdma-evaluation.md](./mdma-evaluation.uk.md) |
| **BMAD-METHOD** (bmad-code-org) | 4/5 | **4/5** | ✅ Інтегровано: spec-first.md (планування з кількома ролями) | [bmad-method-spec-driven-agents.md](./bmad-method-spec-driven-agents.uk.md) |
| **OpenHands** (All Hands AI) | 4/5 | **4/5** | ✅ Інтегровано: agentic-tools.md §2.4 | [openhands-autonomous-agent.md](./openhands-autonomous-agent.uk.md) |
| **Kajan Siva** (туторіал зі створення Mini Claude Code) | 2/5 | **2/5** | ❌ Не інтегрувати (дублює architecture.md, вміст лише французькою; натомість у learning-with-ai.md додано Thorsten Ball) | [kajan-siva-mini-claude-code.md](./kajan-siva-mini-claude-code.uk.md) |
| **Spec-Kitty** (Priivacy-ai) | 3/5 | **3/5** | ✅ Згадка: spec-first.md (ізоляція через worktree) | [spec-kitty-worktree-isolation.md](./spec-kitty-worktree-isolation.uk.md) |
| **Agent Orchestrator** (OrchestratorInc, раніше AgentWrapper/ComposioHQ) | 3/5 | **3/5** | Випробування з Codex, 27 жовтня: відстеження PR і сповіщення CI перевірено; виправлення після рев'ю потребувало ручного пробудження; 5 локальних тестів проходять, віддалений CI заблоковано через білінг | [agent-orchestrator-composio.md](./agent-orchestrator-composio.uk.md) |
| **Liza** (фреймворк MAS, liza-mas/liza) | 3/5 | **3/5** | ✅ Згадка: spec-first.md (еталонна архітектура керування OSS) | [liza-mas-framework.md](./liza-mas-framework.uk.md) |
| **IA-QA CLI** (@ia-qa/cli, Jean-Christophe Jamet) | 3/5 | **2/5** | ⚠️ Лише спостереження (тонкий клієнт, усі вхідні дані йдуть на сторонній сервер; евристики виміряно на рівні -35% на коді) | [ia-qa-cli-llm-testing.md](./ia-qa-cli-llm-testing.uk.md) |
| **Fusion** (Runfusion/Fusion, MIT) | 4/5 | **4/5** | ✅ Лише кейс, не рекомендований інструмент (патерн захисту від шахрайства з подвійним checkout + агентна швидкість без архітектури; bus factor 1, 94% комітів від однієї людини) | [fusion-multi-agent-orchestrator.md](./fusion-multi-agent-orchestrator.uk.md) |
| **ORF** (Open Reasoning Format, Guillaume Laforge) | 3/5 | **2/5** | ✅ Інтегровано в трек файлових плейбуків (memory-systems.md §3.7) після проходу змагальних заперечень; новизну скориговано (поступове розкриття вже охоплено в claude-mem §3.1 і Auto Memory §2.2-2.3), опору на ReasoningBank arXiv 2509.25140 збережено | [orf-open-reasoning-format.md](./orf-open-reasoning-format.uk.md) |
| **DiffMem** (Growth Kinetics, git-нативна пам'ять) | 3/5 | **3/5** | ✅ Лише кейс (memory-systems.md §3.7, LLM-агентний пошук через git-оболонку + навчальний висновок «узгоджуйте пошук із формою запиту»; bus factor 1, немає LICENSE, пошук не тестувався) | [diffmem-git-native-memory.md](./diffmem-git-native-memory.uk.md) |
| **Executor** (UsefulSoftwareCo/executor, шар керування інтеграціями) | 3/5 | **3/5** | ✅ Лише перехресне посилання: enterprise-governance.md §3.5 (продуктова форма патерну ручного реєстру MCP); список спостереження, bus factor 1, активність з квітня впала на 76% | [executor-integration-governance-layer.md](./executor-integration-governance-layer.uk.md) |
| **agentOS** (Rivet, VM агента в процесі) | 4/5 | **4/5** | ✅ Інтегровано: sandbox-isolation.md §5 (контрприклад «у процесі» до чотирьох постачальників хмарних пісочниць); список спостереження, bus factor 1, бенчмарки лише від постачальника | [agentos-in-process-agent-vm.md](./agentos-in-process-agent-vm.uk.md) |
| **Rippletide** («The Harness is the Agent») | 2/5 | **2/5** | ❌ Відхилити, нічого нового порівняно з agent-harness.md, третє подання від Rippletide | [084-rippletide-harness-is-the-agent.md](./084-rippletide-harness-is-the-agent.uk.md) |
| **just-bash** (vercel-labs, симульований bash для агентів) | 4/5 | **4/5** | ✅ Інтегровано: sandbox-isolation.md §5 (протилежність agentOS за принципом «симулювати, а не ізолювати»); bus factor 1 (84,7%), немає файлу LICENSE попри заяву про Apache-2.0 | [just-bash-simulated-shell.md](./just-bash-simulated-shell.uk.md) |
| **Multi-Project Agent Network** (M. Grenier, CTO Easystrat) | 3/5 | **3/5** | ✅ Частково: 2 патерни в agent-teams.md §Advanced (правило скерування, єдиний записувач); заяву про новизну відхилено (суперечить mailbox у agent-teams, Gas Town, Hermes GEPA). ⚠️ Автор НЕ та сама людина, що в `grenier-agent-skill-quality.md` | [grenier-multi-project-agent-network.md](./grenier-multi-project-agent-network.uk.md) |
| **Supermemory** (supermemoryai/supermemory, API пам'яті + рушій контексту) | 3/5 | **3/5** | ✅ Інтегровано: memory-systems.md §3.8/§3.9 (запис), §4.7 (докази командної прогалини), §9 (невідповідність бенчмарків 95%/85,4%); платний плагін для Claude Code (від $19/міс.) проти безкоштовного загального MCP | [supermemory-memory-context-engine.md](./supermemory-memory-context-engine.uk.md) |
| **Корпус Pavan Belagatti 2026** (62 транскрипти YouTube) | 3/5 | **3/5** | ✅ Вибіркова інтеграція: виконання проти керування, операційна модель фабрики ПЗ, межі доказів; туторіали Port не вважаються незалежним підтвердженням | [pavan-belagatti-agentic-engineering-2026.md](./pavan-belagatti-agentic-engineering-2026.uk.md) |
| **Switch** (Flint AI / SandboxAQ, міст чату між агентом і людиною) | 3/5 | **3/5** | ✅ Лише рядок у Known Gaps: third-party-tools.md (кросплатформний міст чату між агентом і людиною з керуванням, порівнянного аналога не знайдено); список спостереження, до 1.0 (0.21.0), 252 зірки за 6 тижнів, bus factor близько 1 (80%) | [switch-agent-human-chat-bridge.md](./switch-agent-human-chat-bridge.uk.md) |
| **Multica** (multica-ai/multica) | 3/5 | **3/5** | ✅ Інтегровано як суміжну керівну площину з межами щодо розгортання, даних, дозволів, Git, ліцензії та доказів роботи середовища виконання | [2026-09-05-multica.md](./2026-09-05-multica.uk.md) |

## Список спостереження

Ресурси, за якими стежимо, але ще не інтегрували: [watch-list.md](./watch-list.uk.md)

---

**Останнє оновлення**: 2026-10-24 (206 файлів Markdown на диску, 83 проіндексовано вище; розрив між диском та індексом лишається окремим завданням з обслуговування)
