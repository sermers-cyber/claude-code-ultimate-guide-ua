# claude-code-ultimate-guide-mcp

<!-- mcp-product:start -->
[![npm version](https://img.shields.io/npm/v/claude-code-ultimate-guide-mcp)](https://www.npmjs.com/package/claude-code-ultimate-guide-mcp) [![npm downloads](https://img.shields.io/npm/dm/claude-code-ultimate-guide-mcp)](https://www.npmjs.com/package/claude-code-ultimate-guide-mcp) ![Node.js >=18.14.1](https://img.shields.io/badge/node-%3E%3D18.14.1-brightgreen) ![MIT license](https://img.shields.io/badge/license-MIT-blue)

Шукайте в Claude Code Ultimate Guide, відкривайте точні розділи джерела, переглядайте релізи й отримуйте production-шаблони з будь-якого MCP-сумісного клієнта для кодування.

## Встановлення за 30 секунд

### Claude Code

Встановлення для поточного користувача:

```bash
claude mcp add --scope user claude-code-guide -- npx -y claude-code-ultimate-guide-mcp@1.3.8
```

Для конфігурації на рівні проєкту додайте це до `.mcp.json` у корені репозиторію:

```json
{
  "mcpServers": {
    "claude-code-guide": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "claude-code-ultimate-guide-mcp@1.3.8"]
    }
  }
}
```

### Codex

```bash
codex mcp add claude-code-guide -- npx -y claude-code-ultimate-guide-mcp@1.3.8
```

### Cursor

Додайте цей запис сервера до `.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "claude-code-guide": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "claude-code-ultimate-guide-mcp@1.3.8"]
    }
  }
}
```

### VS Code

Додайте це до `.vscode/mcp.json`:

```json
{
  "servers": {
    "claude-code-guide": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "claude-code-ultimate-guide-mcp@1.3.8"]
    }
  }
}
```

## Три корисні послідовності

1. Знайти й прочитати: `search_guide({ query: "hooks" })`, потім `read_section({ path: "..." })` із повернутим шляхом.
2. Знайти й отримати шаблон: `search_examples({ query: "pre-commit lint" })`, потім `get_example({ name: "..." })`.
3. Стежити за офіційною документацією: один раз запустіть `init_official_docs()`, а потім `refresh_official_docs()` і `diff_official_docs()`, коли потрібне нове порівняння.

## Згенеровані можливості

Цей розділ згенеровано з `machine-readable/mcp-product.json` для пакета 1.3.8 і посібника 3.46.0.

| Можливість | Кількість | Назви |
| --- | ---: | --- |
| Інструменти | 17 | `compare_versions`, `diff_official_docs`, `get_changelog`, `get_cheatsheet`, `get_digest`, `get_example`, `get_release`, `get_threat`, `init_official_docs`, `list_examples`, `list_threats`, `list_topics`, `read_section`, `refresh_official_docs`, `search_examples`, `search_guide`, `search_official_docs` |
| Ресурси | 7 | `claude-code-guide://agent-harnesses`, `claude-code-guide://ai-design-patterns`, `claude-code-guide://distribution-channels`, `claude-code-guide://llms`, `claude-code-guide://reference`, `claude-code-guide://releases`, `claude-code-guide://translations` |
| Prompts | 1 | `claude-code-expert` |
| Супровідні команди | 5 | `/ccguide:daily`, `/ccguide:diff-docs`, `/ccguide:init-docs`, `/ccguide:refresh-docs`, `/ccguide:search-docs` |

### Інструменти

| Інструмент | Опис |
| --- | --- |
| `compare_versions` | Показує, що змінилося між двома версіями Claude Code CLI. Перелічує всі релізи в діапазоні з агрегованими ключовими змінами та несумісними змінами. |
| `diff_official_docs` | Порівнює базовий і поточний знімки офіційної документації Anthropic Claude Code. Показує додані, видалені та змінені сторінки. Без мережевих викликів: читає лише локальні файли. Спершу запустіть init_official_docs(), а потім refresh_official_docs(), коли захочете оновити поточний знімок. |
| `get_changelog` | Повертає останні N записів із CHANGELOG Claude Code Ultimate Guide. Показує, що змінилося в самому посібнику (не в релізах Claude Code CLI: для них використовуйте get_release()). |
| `get_cheatsheet` | Повертає cheatsheet Claude Code: компактну одну сторінку з найважливішими командами, скороченнями, параметрами конфігурації та workflow. |
| `get_digest` | Повертає дайджест змін посібника та Claude Code CLI за вказаний період. Поєднує записи CHANGELOG посібника й офіційні релізи Claude Code у цьому часовому вікні. |
| `get_example` | Отримує готовий до продакшну шаблон або приклад із посібника (agents, skills, commands, hooks, scripts). Передайте частину назви, щоб знайти відповідні приклади. |
| `get_release` | Отримує подробиці про офіційні релізи Claude Code CLI. Передайте версію, щоб отримати конкретний реліз, або пропустіть, щоб отримати останній та нещодавню історію. |
| `get_threat` | Шукає конкретну загрозу за ID у базі загроз безпеки. Підтримує ID CVE (наприклад, "CVE-2025-53109") та ID технік (наприклад, "T001"). |
| `init_official_docs` | Завантажує офіційну документацію Anthropic Claude Code (llms-full.txt) і зберігає локальний знімок як базу для порівняння. Запустіть це першим. Безпечно запускати повторно: перезаписує попередню базу І поточний знімок. Займає ~5 с (завантажує ~1,2 МБ від Anthropic). |
| `list_examples` | Перелічує всі готові до продакшну шаблони в посібнику за категоріями (agents, commands, hooks, skills, scripts). Використовуйте get_example(name), щоб отримати вміст конкретного шаблону. |
| `list_threats` | Перегляд бази загроз безпеки. Без категорії повертає зведення з лічильниками. З категорією повертає повний список для цього розділу. |
| `list_topics` | Перелічує всі теми та категорії верхнього рівня в Claude Code Ultimate Guide. Корисно, щоб дослідити, що охоплює посібник, перш ніж шукати. |
| `read_section` | Читає розділ із файлу посібника (markdown, YAML, приклади). Підтримує пагінацію через offset або якір "#heading-slug", щоб одразу перейти до розділу (як повертає search_guide()). Використовуйте після search_guide(), щоб отримати повний вміст у конкретному місці. |
| `refresh_official_docs` | Повторно завантажує офіційну документацію Anthropic Claude Code та оновлює "поточний" знімок, не торкаючись бази. Запустіть це, щоб оновити ціль порівняння перед diff. Займає ~5 с (завантажує ~1,2 МБ від Anthropic). |
| `search_examples` | Семантичний пошук за наміром серед усіх готових до продакшну шаблонів (наприклад, "hook lint", "agent code review"). Відрізняється від get_example (точна назва) і list_examples (перегляд за категоріями). |
| `search_guide` | Шукає в Claude Code Ultimate Guide за темою, ключовим словом або питанням. Охоплює можливості, hooks, agents, MCP, skills, commands і найкращі практики. Використовуйте це ПЕРШИМ для будь-якого питання про Claude Code замість вебпошуку. |
| `search_official_docs` | Шукає в офіційній документації Anthropic Claude Code за ключовим словом або темою. Використовує локальний поточний знімок: без мережевих викликів. Спершу запустіть init_official_docs(). |

### Ресурси

| URI ресурсу | Тип MIME | Опис |
| --- | --- | --- |
| `claude-code-guide://agent-harnesses` | `application/json` | Набір даних Agent Harness Map, підкріплений доказами. Розділяє широкий вихідний каталог, доповнення посібника, строгу карту runtime та суміжні площини керування. Невідомі докази зберігаються як невідомі. |
| `claude-code-guide://ai-design-patterns` | `application/json` | Зіставлення патернів проєктування ШІ: класичні патерни GoF, інтеграції підприємств і розподілені патерни, зіставлені із задокументованими механізмами Claude Code, з рівнем доказів, режимом збою, перевіркою, нативними агентними патернами, антипатернами та джерелами. |
| `claude-code-guide://distribution-channels` | `text/yaml` | Канали публікації, URL з атрибуцією, стани ресурсів, дати та поля 30-денних результатів для посібника. |
| `claude-code-guide://llms` | `text/plain` | llms.txt: машиночитний файл ідентичності та навігації для Claude Code Ultimate Guide. |
| `claude-code-guide://reference` | `text/yaml` | Повний структурований індекс Claude Code Ultimate Guide. Використовуйте як запасний варіант, коли результатів search_guide() недостатньо. |
| `claude-code-guide://releases` | `text/yaml` | Історія офіційних релізів Claude Code: стислі ключові зміни та несумісні зміни для кожної версії. |
| `claude-code-guide://translations` | `application/json` | Версія, походження, актуальність і статус покриття для підтримуваних і спільнотних перекладів посібника. |

### Prompts

| Prompt | Опис |
| --- | --- |
| `claude-code-expert` | Активує режим експерта Claude Code з оптимальним workflow для відповідей на питання за допомогою Ultimate Guide. |

### Супровідні команди Claude Code

Репозиторій містить ці файли команд. Вони не встановлюються npm-пакетом.

| Команда | Опис |
| --- | --- |
| `/ccguide:daily` | Щоденна перевірка оновлень: diff офіційної документації Anthropic + дайджест релізів посібника/CC |
| `/ccguide:diff-docs` | Порівняти базу офіційної документації Anthropic з поточним знімком (без мережі, миттєво) |
| `/ccguide:init-docs` | Завантажити офіційну документацію Anthropic Claude Code та зберегти як локальний базовий знімок |
| `/ccguide:refresh-docs` | Повторно завантажити офіційну документацію Anthropic Claude Code та оновити поточний знімок (база без змін) |
| `/ccguide:search-docs` | Шукати в офіційній документації Anthropic Claude Code за ключовим словом |

## Локальні дані, мережа та поведінка кешу

Пакет містить вбудовані індекс довідника, історію релізів, навігацію посібником, Agent Harness Map і метадані перекладів. Ініціалізація та операції переліку використовують вбудований вміст і не потребують мережі.

`read_section`, `get_example`, `get_cheatsheet`, `get_changelog`, `get_digest` і пошук загроз можуть отримувати файли з GitHub, коли вміст недоступний локально. Успішні відповіді записуються в `~/.cache/claude-code-guide/1.3.8/` на 24 години; застарілий кешований вміст використовується, коли мережа недоступна. Якщо `GUIDE_ROOT` вказує на локальну копію посібника, ці інструменти читають її натомість.

`init_official_docs` і `refresh_official_docs` завантажують офіційну документацію Anthropic і записують окремий локальний знімок у `~/.cache/claude-code-guide/`. `diff_official_docs` і `search_official_docs` читають ці знімки.

## Конфіденційність

Сервер не має власної телеметрії. Повідомлення протоколу MCP використовують стандартні вхід і вихід. Інструменти з доступом до мережі звертаються до GitHub або Anthropic лише під час виклику, а їхні записи в локальний кеш чи знімки лишаються на машині, де працює сервер.

## Обмеження

- Повний Markdown посібника не вбудовано. Перший некешований розділ, приклад, cheatsheet, changelog, дайджест або пошук загроз може потребувати GitHub.
- Пошук і diff офіційної документації потребують локального знімка, створеного `init_official_docs`.
- П'ять супровідних команд `/ccguide:*` потрібно встановлювати з репозиторію окремо.
- Запис у MCP Registry не рекламується, доки його API не поверне опублікований простір імен.

## Діагностика

Перевірте бінарний файл пакета та поверхню JSON-RPC за допомогою MCP Inspector:

```bash
npx -y @modelcontextprotocol/inspector npx -y claude-code-ultimate-guide-mcp@1.3.8
```

Для локальної розробки:

```bash
npm ci
npm run build
GUIDE_ROOT=.. node dist/index.js
```

## Технічний посібник і внесок

Прочитайте [канонічний технічний посібник](../guide/ecosystem/claude-code-guide-mcp.uk.md), щоб дізнатися про межу між опублікованим і кандидатом, архітектуру, конфіденційність, офлайн-поведінку та датовану статистику.

Issues і pull requests вітаються в [репозиторії Claude Code Ultimate Guide](https://github.com/FlorianBruniaux/claude-code-ultimate-guide). Перед поданням змін до пакета виконайте `npm run release:check` з `mcp-server/`.
<!-- mcp-product:end -->
