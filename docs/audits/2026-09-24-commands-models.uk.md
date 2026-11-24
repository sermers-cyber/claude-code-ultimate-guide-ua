# Аудит команд і моделей, 24 вересня 2026 року

Операційні довідники перевірено за офіційною документацією, отриманою 24 вересня, та журналом змін Claude Code до v2.1.281. Це аудит документації та прикладів коду, а не живе тестування кожного тарифу, провайдера чи API моделі.

## Джерела

- [Конфігурація моделей Claude Code](https://code.claude.com/docs/en/model-config): аліаси, відмінності між провайдерами, типові значення облікового запису, effort, збереження налаштувань і керування thinking.
- [Довідник команд](https://code.claude.com/docs/en/commands), [довідник CLI](https://code.claude.com/docs/en/cli-reference) та [інтерактивне керування](https://code.claude.com/docs/en/interactive-mode): команди, прапорці та скорочення.
- [Специфікації моделей](https://platform.claude.com/docs/en/models/overview) і [ціни API](https://platform.claude.com/docs/en/about-claude/pricing): ідентифікатори моделей, контекст, ліміти виводу та стандартні тарифи.
- [Fast mode](https://code.claude.com/docs/en/fast-mode), [Remote Control](https://code.claude.com/docs/en/remote-control), [Agent Teams](https://code.claude.com/docs/en/agent-teams) і [налаштування](https://code.claude.com/docs/en/settings-reference): поведінка окремих функцій.
- [Структурований вивід](https://platform.claude.com/docs/en/build-with-claude/structured-outputs): актуальний синтаксис JSON-схем і strict-інструментів.
- [Журнал змін upstream](https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md): межі версій, зокрема видалення TaskOutput у v2.1.278. Сторінка довідника інструментів досі описує його як застарілий; пізніше явне видалення має тут пріоритет.

## Поточний довідник

Стандартні ціни прямого API в USD за мільйон вхідних/вихідних токенів:

| Модель | ID | Вхід / вихід | Контекст | Типовий effort у Claude Code |
|-------|----|----------------|---------|----------------------------|
| Opus 5.5 | `claude-opus-5-5` | $4 / $20 | 1M | medium |
| Sonnet 5 | `claude-sonnet-5` | $2 / $10 | 1M | high |
| Haiku 4.5 | `claude-haiku-4-5-20251001` | $1 / $5 | 200K | Не підтримується |
| Fable 5.1 | `claude-fable-5-1` | $10 / $50 | 1M | high |

Fast mode для Opus 5.5 коштує $8/$40. Нативні моделі з 1M не успадковують стару націнку понад 200K і вимогу beta-заголовка. Аліаси провайдерів можуть вказувати на старіші моделі, тож хмарний аліас не є універсальним ідентифікатором версії.

## Охоплення та рішення

| Поверхня | Дія |
|---------|--------|
| Основний англомовний посібник і щоденна шпаргалка | Оновити вибір моделі, ціни, thinking, налаштування, перелік команд, скорочення, Remote Control та настанови щодо інструментів завдань |
| Французький повний посібник | Виправити відповідні розділи про моделі, ціни, thinking і команди; зберегти заявлений статус застарілого перекладу, бо це не повний переклад заново |
| Сторінки про архітектуру, контекст, операції, екосистему та Agent Teams | Виправити чинні приклади й твердження; прив'язати вимірювання до моделі, яку справді вимірювали |
| Англомовні/французькі шпаргалки та друковані джерела | Оновити розділи про моделі й команди в WP02, WP04, WP07, WP08 та відповідних рекап-картках; збільшити номери ревізій документів |
| Вікторина | Виправити питання про успадкування моделі, перемикання thinking, вимоги до команд, налагодження MCP і fast mode у канонічному вебзбірнику та згенерованому CLI-збірнику |
| Приклади | Виправити ціни резервної моделі, налаштовані тарифи логера, структурований вивід і читання виводу фонових агентів |
| Машинозчитувані та MCP-індекси | Синхронізувати описи, додані команди, посилання та позиційні посилання |
| Історичні релізи, поради з безпеки, оцінювання ресурсів і бенчмарки | Зберегти початкові назви моделей, дати, уражені версії та виміряні витрати |
| Прив'язки до сторонніх моделей і зразки історичних транскриптів | Зберегти задокументований вибір upstream або зразок; не стверджувати непротестовану сумісність із новішою моделлю |
| Встановлені персональні skills і глобальна конфігурація моделей | Поза межами цього аудиту; розповсюджувані приклади редагуються без їх установлення |

Усі 114 назв команд, представлених рядками в отриманому офіційному довіднику, присутні в основному англомовному посібнику. Це число включає видалені команди та записи за feature-прапорцями; воно не означає, що одна інсталяція надає 114 команд.

Приклади розповсюджуваного skill `plan-pipeline` змінюють лише інструкції зі читання виводу. Їхній frontmatter, імена для виявлення та описи маршрутизації залишаються без змін. Це портативні шаблони, а не встановлені проєкції на хості; активацію в живому маршрутизаторі не заявлено.

## Межі перевірки

Регресійний тест резервних цін перевіряє десять ідентифікаторів моделей, зокрема Haiku із датою. Сім випадків не проходили до виправлення, і всі проходять після нього. Оцінки використовують стандартні тарифи токенів; вони не є рахунками провайдерів і не враховують надбавки fast mode.

Перевірки синтаксису, індексу, дзеркал, вікторини та рендерингу зафіксовано разом зі змінами. Жодних платних запитів до моделей, організаційних налаштувань чи глобальних skills не змінювано для валідації документації. Успішна статична збірка не доводить живої доступності в кожного провайдера.

Походження перекладів слід оновити з закоміченого англомовного джерела. Оновлення вибраних французьких розділів не робить увесь французький переклад актуальним.

## Перевірки, виконані перед публікацією

- Позиційний індекс: перевірено 906 посилань, жодного зламаного; усі 793 прив'язані якорі та 61 оголошений позиційний якір розв'язуються. Усі 106 відстежуваних сторінок посібника проіндексовано.
- CLI-вікторина: усі 17 категорій збігаються з канонічним вебзбірником; три CLI-тести проходять.
- Лендинг: проходить 258 тестів, зокрема HTTP-фікстури на localhost. Статична збірка дає 462 сторінки; інвентар посилань перевіряє 583 HTML-документи й валідує 1 782 локальні цілі. Зовнішні URL лишаються поза цим офлайн-результатом. Сорок шість діаграм рендеряться як SVG; три зберігають текстовий запасний варіант.
- Резервні ціни: проходять десять модельних випадків; обидва змінені shell-скрипти проходять перевірку синтаксису. Підсумок сесії тепер повідомляє пікові вхідні токени, не припускаючи вікно 200K для кожної моделі.
- Друкований експорт: перегенеровано 22 PDF. Дванадцять рекап-карток залишаються по одній сторінці; дві щоденні шпаргалки мають по п'ять сторінок. Для вісьмох уражених whitepapers також перебудовано EPUB. Чотири архіви серій зберігають по 22 картки.
- Пакет MCP: усі 37 тестів і повна перевірка релізу проходять, зокрема перегенерований маніфест продукту, документація, метадані реєстру та вміст пакета.
- Сканування публічного вмісту: нуль порушень щодо шляхів робочої станції у 1 438 вихідних і відрендерених файлах. Вихідні та вбудовані в пакет MCP довідкові файли побайтово ідентичні.

## Змінені файли посібника

Супутній лендинг містить відповідні вебвікторину, шпаргалку, дані рідера/пошуку та завантаження. Портфоліо містить версіоновані PDF/ZIP-активи та їхній список дозволених завантажень.

- `CHANGELOG.md`
- `README.md`
- `docs/audits/2026-09-24-commands-models.md`
- `examples/config/settings-personalization.json`
- `examples/hooks/bash/session-summary.sh`
- `examples/modes/README.md`
- `examples/scripts/session-stats.sh`
- `examples/skills/plan-pipeline/execute/SKILL.md`
- `examples/skills/plan-pipeline/start/SKILL.md`
- `examples/skills/plan-pipeline/validate/SKILL.md`
- `examples/styles/custom-style-template.md`
- `guide/cheatsheet.md`
- `guide/core/architecture.md`
- `guide/core/community-patterns.md`
- `guide/core/context-engineering.md`
- `guide/core/known-issues.md`
- `guide/core/settings-reference.md`
- `guide/core/tools-reference.md`
- `guide/diagrams/09-cost-and-optimization.md`
- `guide/ecosystem/agentic-tools.md`
- `guide/ecosystem/ai-ecosystem.md`
- `guide/ecosystem/local-vs-cloud-inference.md`
- `guide/learning-path/03-memory.md`
- `guide/ops/ai-unit-economics.md`
- `guide/ops/api-gateway.md`
- `guide/ops/devops-sre.md`
- `guide/ops/observability.md`
- `guide/ops/subscription-strategy.md`
- `guide/roles/agent-evaluation.md`
- `guide/ultimate-guide.fr.md`
- `guide/ultimate-guide.md`
- `guide/workflows/agent-teams-quick-start.md`
- `guide/workflows/agent-teams.md`
- `guide/workflows/dual-instance-planning.md`
- `guide/workflows/iterative-refinement.md`
- `guide/workflows/plan-pipeline.md`
- `llms.txt`
- `machine-readable/llms.txt`
- `machine-readable/mcp-product.json`
- `machine-readable/reference.yaml`
- `machine-readable/translations.json`
- `mcp-server/content/llms.txt`
- `mcp-server/content/reference.yaml`
- `mcp-server/content/translations.json`
- `quiz/questions/01-quick-start.yaml`
- `quiz/questions/02-core-concepts.yaml`
- `quiz/questions/03-memory-settings.yaml`
- `quiz/questions/04-agents.yaml`
- `quiz/questions/05-skills.yaml`
- `quiz/questions/06-commands.yaml`
- `quiz/questions/07-hooks.yaml`
- `quiz/questions/08-mcp-servers.yaml`
- `quiz/questions/09-advanced-patterns.yaml`
- `quiz/questions/10-reference.yaml`
- `quiz/questions/11-learning-with-ai.yaml`
- `quiz/questions/12-architecture.yaml`
- `quiz/questions/13-security.yaml`
- `quiz/questions/14-privacy-observability.yaml`
- `quiz/questions/15-ai-ecosystem.yaml`
- `quiz/questions/16-agent-harness-context.yaml`
- `quiz/questions/17-team-metrics.yaml`
- `scripts/test-session-summary-pricing.py`
- `whitepapers/CHANGELOG.md`
- `whitepapers/en/02-customization.qmd`
- `whitepapers/en/04-architecture.qmd`
- `whitepapers/en/07-reference-guide.qmd`
- `whitepapers/en/08-agent-teams.qmd`
- `whitepapers/en/cheatsheet.pdf`
- `whitepapers/en/cheatsheet.qmd`
- `whitepapers/fr/02-personnalisation.qmd`
- `whitepapers/fr/04-architecture.qmd`
- `whitepapers/fr/07-guide-reference.qmd`
- `whitepapers/fr/08-agent-teams.qmd`
- `whitepapers/fr/cheatsheet.pdf`
- `whitepapers/fr/cheatsheet.qmd`
- `whitepapers/recap-cards/en/01-commandes-essentielles.qmd`
- `whitepapers/recap-cards/en/m08-agents-custom.qmd`
- `whitepapers/recap-cards/en/m16-multi-agent-topologie.qmd`
- `whitepapers/recap-cards/en/t18-modeles-thinking-modes.qmd`
- `whitepapers/recap-cards/en/t19-context-window-200k-1m.qmd`
- `whitepapers/recap-cards/en/t21-fast-mode-api.qmd`
- `whitepapers/recap-cards/fr/01-commandes-essentielles.qmd`
- `whitepapers/recap-cards/fr/m08-agents-custom.qmd`
- `whitepapers/recap-cards/fr/m16-multi-agent-topologie.qmd`
- `whitepapers/recap-cards/fr/t18-modeles-thinking-modes.qmd`
- `whitepapers/recap-cards/fr/t19-context-window-200k-1m.qmd`
- `whitepapers/recap-cards/fr/t21-fast-mode-api.qmd`
