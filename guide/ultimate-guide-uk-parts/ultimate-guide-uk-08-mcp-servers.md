# 8. MCP Сервери

_Швидкий перехід:_ [What is MCP](#81-what-is-mcp) · [Доступні сервери](#82-available-servers) · [Конфігурація](#83-configuration) · [Посібник з вибору сервера](#84-server-selection-guide) · [Система плагінів](#85-plugin-system) · [MCP Security](#86-mcp-security)

---

**Час читання**: 15 хвилин
**Рівень навичок**: 2-3 тиждень
**Мета**: Розширити Claude Code зовнішніми інструментами

## 8.1 What is MCP

MCP (Model Context Protocol) — це стандарт для підключення AI моделей до зовнішніх інструментів та джерел даних.

### Чому MCP?

| Без MCP | З MCP |
|-------------|----------|
| Обмежено вбудованими інструментами | Розширювана екосистема інструментів |
| Claude здогадується про зовнішні дані | Claude запитує реальні дані |
| Загальне розуміння коду | Глибокий семантичний аналіз |

### Як це працює

```
┌─────────────────────────────────────────────────────────┐
│                    MCP ARCHITECTURE                     │
├─────────────────────────────────────────────────────────┤
│                                                         │
│   ┌─────────────┐                                       │
│   │ Claude Code │                                       │
│   └──────┬──────┘                                       │
│          │                                              │
│          ▼                                              │
│   ┌─────────────────────────────────────────────┐       │
│   │               MCP Protocol                  │       │
│   └──────────────────────┬──────────────────────┘       │
│                          │                              │
│          ┌───────────────┼───────────────┐              │
│          ▼               ▼               ▼              │
│   ┌───────────┐   ┌───────────┐   ┌───────────┐         │
│   │  Serena   │   │ Context7  │   │ Postgres  │         │
│   │(Semantic) │   │  (Docs)   │   │(Database) │         │
│   └───────────┘   └───────────┘   └───────────┘         │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### MCP Evolution: Apps Extension (SEP-1865)

> **🆕 З січня 2026**: MCP може доставляти інтерактивні інтерфейси разом із традиційними текстовими відповідями.

#### Проблема контекстного розриву

Традиційні AI взаємодії вимагають повторних запитів для дослідження даних:

**Без MCP Apps**:
```
Ви: "Покажи дані клієнтів"
Claude: "Ось 500 клієнтів [текстовий список]"
Ви: "Сортуй за доходом"
Claude: "Ось відсортований список [текст]"
Ви: "Фільтруй за останні 30 днів"
Claude: "Ось відфільтрований список [текст]"
Ви: "Покажи топ-10"
... (багато циклів запитів)
```

**З MCP Apps**:
```
Ви: "Покажи дані клієнтів"
Claude: [Відображає інтерактивну панель із сортуванням, фільтрацією, вибором дати]
Ви: [Сортуєте, фільтруєте, заглиблюєтесь в UI — без додаткових запитів]
```

#### Що таке MCP Apps?

MCP Apps дозволяють MCP серверам доставляти **інтерактивні інтерфейси**, які відображаються безпосередньо у вашій розмові:

- **Панелі**: Діаграми з фільтрацією, заглибленням, експортом
- **Майстери налаштувань**: Форми з залежними полями та валідацією
- **Переглядачі документів**: PDF з вбудованими підсвічуваннями та анотаціями
- **Монітори в реальному часі**: Живі метрики без повторного запуску інструментів

#### Доступні інтерактивні інструменти

**На запуску** (26 січня 2026), **9 інтерактивних інструментів** доступні:

| Інструмент | Що робить |
|------|--------------|
| **Asana** | Створення таймлайнів проєктів, керування завданнями, видимими командам |
| **Slack** | Написання форматованих повідомлень з попереднім переглядом перед публікацією |
| **Figma** | Перетворення тексту на блок-схеми, діаграми Ганта у FigJam |
| **Amplitude** | Побудова аналітичних діаграм, дослідження трендів інтерактивно |
| **Box** | Пошук файлів, попередній перегляд документів вбудовано |
| **Canva** | Створення презентацій з налаштуванням дизайну в реальному часі |
| **Clay** | Дослідження компаній, пошук контактів, створення outreach |
| **Hex** | Запити даних з інтерактивними діаграмами та таблицями |
| **monday.com** | Керування роботою, оновлення дощок, візуалізація прогресу |

**Незабаром**: Salesforce (Agentforce 360), інтеграція Claude Cowork

→ **Доступ**: [claude.ai/directory](https://claude.ai/directory) (плани Pro/Max/Team/Enterprise)

#### Підтримка платформ

| Платформа | Підтримка | Як використовувати |
|----------|---------|------------|
| **Claude Desktop** | ✅ Зараз | claude.ai/directory — підключайте інтерактивні інструменти |
| **Claude Cowork** | 🔄 Незабаром | Агентні робочі процеси з доступом до файлів/проєктів |
| **VS Code** | ✅ Insiders | Встановіть Insiders збірку, налаштуйте MCP Apps |
| **ChatGPT** | 🔄 Розгортання | Тиждень 26 січня 2026 |
| **Goose** | ✅ Зараз | Відкрита альтернатива з підтримкою UI |
| **Claude Code CLI** | ❌ Ні | Термінал — лише текст (без UI рендерингу) |

#### Чому це важливо для CLI користувачів

**Прямий вплив**: **Немає** - Claude Code CLI не може рендерити інтерактивні UI в терміналі.

**Непрямі переваги**:

1. **Обізнаність про екосистему**: Розуміння того, куди рухається MCP (інтерактивні агентні робочі процеси)
2. **Гібридні робочі процеси**: Використовуйте Claude Desktop для візуального дослідження → Claude Code CLI для автоматизації
3. **Розробка MCP серверів**: Якщо створюєте власні сервери, Apps тепер є опцією
4. **Контекст для інструментів**: Деякі MCP сервери можуть рекламувати UI можливості (видно в метаданих)

**Приклад гібридного робочого процесу**:
```
1. Claude Desktop: Використовуйте Amplitude MCP App для інтерактивного дослідження аналітики
2. Визначте патерни візуально (наприклад, "Регіон EU показує 30% зростання")
3. Claude Code CLI: Автоматизуйте експорт даних та звіти на основі висновків
```

#### Технічна основа

MCP Apps побудовано на **Model Context Protocol** (відкритий стандарт Anthropic):

- **Відкрита специфікація**: [SEP-1865 на GitHub](https://github.com/modelcontextprotocol/ext-apps)
- **Співавтори**: OpenAI, Anthropic, творці MCP-UI
- **SDK**: `@modelcontextprotocol/ext-apps` (npm)
- **"Створи один раз, розгортай всюди"**: Працює в Claude, VS Code, ChatGPT, Goose

→ **Детальніше**: див. [guide/architecture.md:656](./core/architecture.md#mcp-extensions-apps-sep-1865) для технічної архітектури, моделі безпеки та деталей SDK.

#### Ресурси

- **MCP Apps блог пост**: [Anthropic announcement](https://blog.modelcontextprotocol.io/posts/2026-01-26-mcp-apps/)
- **Interactive tools блог**: [Claude announcement](https://claude.com/blog/interactive-tools-in-claude)
- **Офіційна специфікація**: [SEP-1865 на GitHub](https://github.com/modelcontextprotocol/ext-apps)

---

## 8.2 Доступні сервери

<details>
<summary><b>Каталог MCP серверів (натисніть, щоб розгорнути)</b></summary>

### Serena (Semantic Code Analysis)

**Призначення**: Глибоке розуміння коду через семантичний аналіз, індексацію та постійну пам'ять.

**Чому Serena важлива**: Claude Code не має вбудованої індексації (на відміну від Cursor). Serena заповнює цю прогалину, індексуючи вашу кодову базу для швидшого та розумнішого пошуку. Вона також надає **сесійну пам'ять** — контекст, який зберігається між розмовами.

**Ключові можливості**:

| Можливість | Опис |
|---------|-------------|
| **Індексація** | Попередньо індексує кодову базу для ефективного пошуку символів |
| **Пам'ять проєкту** | Зберігає контекст у `.serena/memories/` між сесіями |
| **Онбординг** | Автоматично аналізує структуру проєкту на першому запуску |

**Інструменти**:

| Інструмент | Опис |
|------|-------------|
| `find_symbol` | Знайти функції, класи, методи за назвою |
| `get_symbols_overview` | Отримати огляд структури файлу |
| `search_for_pattern` | Регулярний пошук по кодовій базі |
| `find_referencing_symbols` | Знайти всі використання символу |
| `replace_symbol_body` | Замінити тіло функції/класу |
| `write_memory` | Зберегти контекст для майбутніх сесій |
| `read_memory` | Отримати збережений контекст |
| `list_memories` | Список усіх збережених спогадів |

**Робочий процес сесійної пам'яті**:

```
# Початок сесії
list_memories() → Подивитися, який контекст існує
read_memory("auth_architecture") → Завантажити відповідний контекст

# Під час роботи
write_memory("api_refactor_plan", "...") → Зберегти рішення для пізнішого використання

# Кінець сесії
write_memory("session_summary", "...") → Зберегти прогрес
```

**Налаштування**:

```bash
# Базова індексація (перший запуск)
uvx --from git+https://github.com/oraios/serena serena project index

# Примусова повна перебудова (якщо індекс пошкоджено або застаріло)
uvx --from git+https://github.com/oraios/serena serena project index --force-full

# Інкрементна індексація (швидше після початкового індексу)
uvx --from git+https://github.com/oraios/serena serena project index --incremental

# Паралельна обробка (рекомендовано: 50-75% ядер CPU)
uvx --from git+https://github.com/oraios/serena serena project index --parallel 4

# Детальний режим (показати деталі прогресу)
uvx --from git+https://github.com/oraios/serena serena project index --verbose --force-full

# Переглянути всі опції
uvx --from git+https://github.com/oraios/serena serena project index --help
```

**Опції індексації**:

| Опція | Опис | Коли використовувати |
|--------|-------------|----------|
| `--force-full` | Повна перебудова індексу | Пошкоджений індекс, значні зміни в кодовій базі |
| `--incremental` | Оновлення лише змінених файлів | Регулярне обслуговування після початкового індексу |
| `--parallel N` | Використовувати N ядер CPU | Великі кодові бази (50-75% ядер) |
| `--verbose` | Показати детальний прогрес | Налагодження проблем індексації |

**Розташування кешу**: Індекс зберігається в `.serena/cache/typescript/` (додати до `.gitignore`)

**Важливі зауваження**:
- **Застаріла команда**: `serena index-project` → Використовуйте `serena project index`
- **Перший запуск**: Використовуйте базову `serena project index` (автовизначення повної перебудови)
- **Регулярні оновлення**: Використовуйте `--incremental` для швидшої повторної індексації
- **Продуктивність**: `--parallel 4` на 8-ядерному = ~60% швидше

> **Джерела**: [Serena Docs](https://oraios.github.io/serena/02-usage/020_running.html) • [GitHub Issues](https://github.com/oraios/serena/issues/372) • [Optimization Guide](https://smartscope.blog/en/ai-development/serena-mcp-project-indexing-optimization/)

**Використовуйте, коли**:
- Навігація великими кодовими базами (>10k рядків)
- Потрібен контекст між сесіями
- Розуміння зв'язків між символами
- Рефакторинг у кількох файлах

> **Джерело**: [Serena GitHub](https://github.com/oraios/serena)

### grepai (Рекомендований семантичний пошук)

**Призначення**: Приватний семантичний пошук коду з аналізом графу викликів.

**Чому grepai рекомендовано**: Повністю відкритий, локальний (Ollama, без хмари) з **аналізом графу викликів**.

**Ключові можливості**:

| Можливість | Опис |
|---------|-------------|
| **Семантичний пошук** | Знайти код за описом природною мовою |
| **Граф викликів** | Відстеження викликаючих, викликаних та повних графів залежностей |
| **Приватність на першому місці** | Використовує Ollama локально (без хмари) |
| **Фонова індексація** | `grepai watch` демон підтримує індекс свіжим |

**Приклад**:

```bash
# Семантичний пошук (знаходить за значенням, не за точним текстом)
grepai search "user authentication flow"

# Хто викликає цю функцію?
grepai trace callers "createSession"
# → Показує всі 23 файли, які викликають createSession з контекстом

# Що викликає ця функція?
grepai trace callees "SessionProvider"

# Повний граф залежностей
grepai trace graph "createSession" --depth 3
```

**Доступні MCP інструменти**:

| Інструмент | Опис |
|------|-------------|
| `grepai_search` | Семантичний пошук природною мовою |
| `grepai_trace_callers` | Знайти всіх викликаючих функцію |
| `grepai_trace_callees` | Знайти всі функції, які викликає функція |
| `grepai_trace_graph` | Згенерувати граф викликів |
| `grepai_index_status` | Перевірити статус індексації |

**Налаштування**:

```bash
# 1. Встановіть Ollama та модель embeddings
brew install ollama
brew services start ollama
ollama pull nomic-embed-text

# 2. Встановіть grepai
curl -sSL https://raw.githubusercontent.com/yoanbernabeu/grepai/main/install.sh | sh

# 3. Ініціалізуйте у проєкті
cd your-project
grepai init

# 4. Запустіть демон індексації
grepai watch &
```

**Комбінований робочий процес з Serena**:

```
1. grepai search "payment validation"     → Знайти файли
2. Serena get_symbols_overview            → Структура файлу
3. grepai trace callers "validatePayment" → Залежності
4. Serena find_symbol + replace_symbol_body → Точне редагування
```

**Використовуйте, коли**:
- Дослідження незнайомих кодових баз за призначенням
- Розуміння залежностей викликів перед рефакторингом
- Потрібна приватність (без хмари, все локально)

**Продуктивність**:

| Тип пошуку | Інструмент | Час | Результати |
|-------------|------|------|---------|
| Точний збіг | `rg` (ripgrep) | ~20ms | Лише точні збіги |
| Точний збіг | `grep` | ~45ms | Лише точні збіги |
| Семантичний | `grepai` | ~500ms | Збіги за призначенням |

> **Джерело**: [grepai GitHub](https://github.com/yoanbernabeu/grepai)

**Патерн Blast-Radius**:

Перед зміною широко використовуваної функції — знайдіть всі місця виклику:

```bash
# Крок 1: Всі викликаючі
grepai trace callers "processPayment"
# → 14 місць виклику у 7 файлах

# Крок 2: Залежності
grepai trace callees "processPayment"
# → 3 залежності нижче

# Крок 3: Оцініть обсяг
# 14 викликів + 3 залежності = значний радіус → сплануйте рефакторинг
```

---

### claude-mem (Автоматична сесійна пам'ять)

**Призначення**: Автоматична постійна пам'ять між сесіями Claude Code через AI-стиснене захоплення.

**Чому claude-mem важливий**: На відміну від ручних інструментів (Serena `write_memory()`), claude-mem **автоматично захоплює все** та впроваджує контекст при повторному підключенні.

**Ключові можливості**:

| Можливість | Опис |
|---------|-------------|
| **Автоматичне захоплення** | Хуки на SessionStart, PostToolUse, Stop, SessionEnd |
| **AI стиснення** | Семантичні підсумки (~10x скорочення токенів) |
| **Прогресивне розкриття** | 3 рівні (пошук → таймлайн → спостереження) ~95% економії |
| **Гібридний пошук** | Повнотекстовий + векторний (Chroma) + природна мова |
| **Веб-панель** | `http://localhost:37777` |
| **Контроль приватності** | Теги `<private>` |

**Архітектура**:

```
Життєвий цикл сесії (хуки → воркер → сховище):

┌─────────────────────┬──────────────────────┬────────────────────────────────┐
│ Момент              │ Хук                  │ Дія                            │
├─────────────────────┼──────────────────────┼────────────────────────────────┤
│ Сесія починається   │ SessionStart         │ Впровадження останніх N сесій │
│ Перший запит        │ UserPromptSubmit     │ Створення/ідентифікація сесії │
│ Після інструмента   │ PostToolUse (*)      │ Захоплення спостереження      │
│ Кінець відповіді    │ Stop                 │ Генерація LLM підсумку        │
│ Сесія завершується  │ SessionEnd           │ Позначення як завершеної      │
└─────────────────────┴──────────────────────┴────────────────────────────────┘
```

**Типи спостережень**:

| Тип | Коли | Приклад |
|------|------|---------|
| `DISCOVERY` | Читання/дослідження | "Досліджено auth модуль, JWT в validateToken()" |
| `CHANGE` | Редагування файлів | "Змінено session.middleware.ts: додано refresh логіку" |
| `FEATURE` | Нова функціональність | "Реалізовано OAuth2 в auth.service.ts" |
| `BUGFIX` | Виправлення помилок | "Виправлено null pointer в UserController.getById()" |

**Встановлення**:

```bash
/plugin marketplace add thedotmack/claude-mem
/plugin install claude-mem
# Перезапустіть Claude Code
```

**Доступні скіли** (`/claude-mem:*`):

| Скіл | Призначення |
|-------|---------|
| `mem-search` | Пошук: "Як ми вирішили проблему з CORS?" |
| `smart-explore` | AST-дослідження кодової бази |
| `make-plan` | Поетапний план реалізації |
| `do` | Виконання плану через суб-агенти |
| `timeline-report` | Наратив "Подорож у [Проєкт]" |

**Прогресивне розкриття** (3 рівні):

```
Рівень 1: Пошук (50-100 токенів) — "Знайди сесії про автентифікацію"
Рівень 2: Таймлайн (500-1000 токенів) — "Покажи таймлайн сесії abc123"
Рівень 3: Деталі (повний контекст) — "Деталі спостереження obs_456"
```

**Результат**: ~10x скорочення токенів.

**Контроль приватності**:

```markdown
<private>
Дані БД: postgres://prod-db-123
API ключ: sk-1234567890abcdef
</private>
```

**Попередження безпеки**:

> ⚠️ `GET /api/settings` повертає API ключі у відкритому тексті. Будь-який локальний процес може читати це без автентифікації.

**Витрати**:

| Аспект | Вартість |
|--------|---------|
| API стиснення | ~$0.15/100 спостережень |
| Зберігання | Безкоштовно (локальний SQLite) |
| Типова місячна вартість | $5-15 (100+ сесій/міс) |

**Оптимізація витрат — Gemini**:

```bash
# ~/.claude-mem/settings.json
{ "provider": "gemini", "model": "gemini-2.5-flash-lite", "auth_method": "cli" }
```

| Модель | Вартість/міс (~400 сесій) | Економія |
|--------|--------------------------|---------|
| Claude Haiku | ~$102 | — |
| Gemini 2.5 Flash | ~$14 | **-86%** |

**Критичний момент — співіснування хунків**:

claude-mem додає хуки на `SessionStart`, `PostToolUse`, `Stop`, `SessionEnd`. Він **перезаписує** існуючі хуки, а не об'єднує.

**Fail-open архітектура (v9.1.0+)**: Якщо воркер не працює, Claude Code продовжує без блокування.

**Обмеження**:

| Обмеження | Вплив |
|-----------|--------|
| CLI тільки | Немає VS Code |
| Немає хмарної синхронізації | Лише локально |
| Ліцензія AGPL-3.0 | Комерційні обмеження |

**Приклад: багатоденний рефакторинг**:

```
День 1: "Досліди auth модуль" → захоплено
День 2: [Автоконтекст] "Раніше: auth.service.ts, session.middleware.ts"
День 3: [Автоконтекст] "Рішення: обрали jose замість jsonwebtoken"
```

> **Джерела**: [GitHub](https://github.com/thedotmack/claude-mem) • [Progressive Disclosure](https://corti.com/claude-mem-persistent-memory-for-ai-coding-assistants/)

---

### Graphify (Графи знань кодової бази)

**GitHub**: [safishamsi/graphify](https://github.com/safishamsi/graphify) | **PyPI**: `graphifyy` | **Зірки**: 42K | **Ліцензія**: MIT

Graphify перетворює директорію проєкту на постійний граф знань. Асистент відповідає на питання про архітектуру з графа замість повторного сканування файлів.

**Три проходи**:

1. **Локальне AST вилучення** — tree-sitter парсить 25+ мов (без API, без мережі)
2. **Локальна транскрипція** — faster-whisper для аудіо/відео
3. **Паралельне семантичне вилучення** — Claude суб-агенти для документів, PDF, зображень

Результати в `graphify-out/`:
- `graph.html` — візуалізація
- `GRAPH_REPORT.md` — звіт (впроваджується в Claude)
- `graph.json` — постійний граф

**Встановлення**:

```bash
uv tool install graphifyy && graphify install
graphify claude install
/graphify .
/graphify . --update
/graphify query "що з'єднує auth з БД?"
/graphify path "UserService" "DatabasePool"
```

**Graphify vs GrepAI**: GrepAI — семантичні пошуки в реальному часі. Graphify — структурні зв'язки по всій кодовій базі. Взаємодоповнюючі.

**Graphify vs claude-mem**: claude-mem зберігає *обговорення*. Graphify відображає *структуру коду*. Без перетину.

**Застереження**: Не-кодові файли надсилаються до API. Без post-commit хука граф розходиться. Заяви про ефективність токенів (71.5x–120x) — самостійні бенчмарки.

---

### Матриця рішень інструментів пам'яті

| Потреба | Інструмент | Приклад |
|---------|------------|---------|
| "Що ми робили вчора?" | claude-mem | Автоконтекст |
| "Знайди login" | Serena | `find_symbol --name "login"` |
| "Хто викликає login?" | grepai | `grepai trace callers "login"` |
| "Запиши арх. рішення" | Serena | `write_memory("decision", "Use JWT")` |
| "Знайди код, що робить X" | grepai | `grepai search "payment"` |
| "Підсумок сесій" | claude-mem | localhost:37777 |
| "Точний збіг" | rg | `rg "authenticate"` |
| "Залежності модуля" | Graphify | `/graphify query "auth deps"` |

**Стек пам'яті (5 рівнів)**:

```
Рівень 5: Захоплення сесій   → claude-mem (авто)
Рівень 4: Пам'ять символів   → Serena (ручні рішення)
Рівень 3: Семантичний пошук  → grepai (виявлення)
Рівень 2: Структурний граф   → Graphify (архітектура)
Рівень 1: Точний пошук       → rg (вбудований, швидкий)
```

**Порівняння: claude-mem vs Serena vs grepai**:

| Аспект | claude-mem | Serena | grepai |
|--------|-----------|---------|--------|
| Запуск | Авто (хуки) | Ручний API | Ручний CLI |
| Зберігання | SQLite + Chroma | `.serena/memories/` | Ollama вектори |
| Призначення | Сесії | Символи | Семантичний пошук |
| Панель | ✅ Web UI | ❌ | ❌ |
| Вартість | ~$0.15/100 | Безкоштовно | Безкоштовно |
| Зусилля | Нуль (авто) | Ручні команди | Ручні команди |
| Ліцензія | AGPL-3.0 | MIT | MIT |

---

### 🔍 Порівняння пошукових інструментів

| Потреба | Інструмент | Приклад |
|---------|-------------|---------|
| Точний текст | `rg` | `rg "authenticate" --type ts` |
| За значенням | `grepai` | `grepai search "user login flow"` |
| Визначення функції | `Serena` | `serena find_symbol --name "login"` |
| Структурний патерн | `ast-grep` | `ast-grep "async function $F"` |
| Хто викликає | `grepai` | `grepai trace callers "login"` |
| Структура файлу | `Serena` | `serena get_symbols_overview` |
| Минулі сесії | `claude-mem` | Автовпровадження |

**Коли що використовувати**:

**rg** — знаєте точний текст, швидкість критична
**grepai** — пошук за призначенням, граф викликів, приватність
**Serena** — рефакторинг, навігація символами, постійний контекст
**ast-grep** — великомасштабний рефакторинг, міграції, структурні патерни
**claude-mem** — багатосесійні проєкти, автоконтекст

**Приклад комбінованого робочого процесу** (рефакторинг auth):

```bash
# 1. Виявлення (grepai)
grepai search "authentication and session management"
# 2. Структура (Serena)
serena get_symbols_overview --file auth.service.ts
# 3. Залежності (grepai)
grepai trace callers "login"
# 4. Патерни (ast-grep)
ast-grep "async function login" --without "try { $$$ } catch"
# 5. Перевірка (rg)
rg "validateSession" --type ts -A 5
```

---

### mgrep (Альтернативний семантичний пошук)

**Призначення**: Семантичний пошук по коду, PDF та зображеннях.

**Ключові можливості**: семантичний пошук, фонова індексація, багатоформатний, веб-інтеграція.

**Використовуйте, коли**: потрібен пошук по змішаному вмісту або хмарні embeddings.

> **Джерело**: [mgrep GitHub](https://github.com/mixedbread-ai/mgrep)

### Context7 (Пошук документації)

**Інструменти**: `resolve-library-id`, `query-docs`

**Використовуйте для**: вивчення бібліотек, пошук API, офіційні патерни.

### ast-grep (Структурний пошук коду)

**Тип**: Опціональний плагін спільноти.

**Встановлення**:
```bash
npx skills add ast-grep/agent-skill
```

ast-grep шукає код на основі **AST**, не тексту. Патерни: "async без try/catch", "React з конкретними хуками".

✅ Для: великомасштабний рефакторинг (>50k рядків), міграції фреймворків, структурні патерни
❌ Не для: прості текстові пошуки, маленькі проєкти, одноразові пошуки

**Важливо**: Claude не використовує ast-grep автоматично — потрібен явний запит.

---

### Sequential Thinking (Структуроване міркування)

**Інструменти**: `sequentialthinking`

**Використовуйте**: складне налагодження, архітектурний аналіз, системний дизайн.

### Postgres (Запити до БД)

**Інструменти**: `query`

**Використовуйте**: дослідження даних, розуміння схеми, налагодження.

### Playwright (Автоматизація браузера)

**Інструменти**: `navigate`, `click`, `fill`, `screenshot`

**Використовуйте**: E2E тестування, візуальна валідація, налагодження браузера.

### agent-browser (Vercel Labs) — AI-нативна автоматизація браузера

> **Статус**: v0.15.0 (лютий 2026). 12,100+ зірок. Rust.

**Призначення**: Headless браузер CLI для AI агентів. Використовує Playwright/CDP, оптимізує вивід для LLM.

**Встановлення**:
```bash
brew install vercel-labs/tap/agent-browser
npm install -g @vercel-labs/agent-browser
```

**Можливості**: навігація, клік, скрол, форми, дерево доступності, візуальні diff, сесії (AES-256-GCM), безпека v0.15.0.

**agent-browser vs Playwright MCP**:
- Токенів: **-82.5%**
- Елементи: `@e1`, `@e2` (стабільні, компактні)
- Rust (суб-мс запуск) vs Node.js
- Сесії: Так vs Ні
- Безпека: сховища, білі списки vs Немає

**Цикл Ralph Wiggum** — самоверифікаційний агент:
```
1. Агент пише код → 2. Розгортає → 3. agent-browser перевіряє
4. Тестує сценарії → 5. При невдачі: виправляє, перерозгортає → 6. Цикл
```

### doobidoo Memory Service (Семантична пам'ять)

> **⚠️ Статус: Тестується**

**Призначення**: Постійна семантична пам'ять з крос-сесійним пошуком.

**Serena vs doobidoo**: Serena — ключ-значення, doobidoo — семантичний пошук.

**Бекенди**: `sqlite_vec` (локальний), `cloudflare` (хмарний), `hybrid` (гібрид)

**12 MCP інструментів**: `store_memory`, `retrieve_memory`, `search_by_tag`, `delete_memory`, `list_memories`, `check_database_health`, `get_cache_stats`, `memory_graph:connected/path/subgraph`

**Встановлення**:
```bash
pip install mcp-memory-service
python -m mcp_memory_service.scripts.installation.install --quick
```

**MCP конфіг**:
```json
{
  "mcpServers": {
    "memory": {
      "command": "memory",
      "args": ["server"]
    }
  }
}
```

**Використання**:
```
store_memory("Рішення: FastAPI для API", tags=["architecture"])
retrieve_memory("який фреймворк?")
search_by_tag(["architecture"])
```

**Панель**: http://localhost:8000

### Kairn: Граф знань з біологічним затуханням

> **⚠️ Статус: Тестується**. MIT, Python 100%.

**Відмінності**: типізовані зв'язки (`depends-on`, `resolves`, `causes`), біологічне затухання (рішення ~200 днів, workarounds ~50 днів), 18 MCP інструментів.

**MCP конфіг**:
```json
"kairn": { "command": "python", "args": ["-m", "kairn", "serve"] }
```

**Встановлення**: `pip install kairn`

### ICM: Двоїста архітектура пам'яті (Rust, нуль залежностей)

> **⚠️ Статус: Тестується**. Source-Available (≤20 безкоштовно).

**Призначення**: Memories (епізодичне затухання) + Memoirs (постійний граф знань) в одному Rust бінарі.

**Встановлення**:
```bash
brew tap rtk-ai/tap && brew install icm
```

**3 режими налаштування**:
```bash
icm init --mode mcp     # MCP сервер
icm init --mode hook    # PostToolUse хук
icm init --mode skill   # /recall та /remember команди
```

**Використання**:
```bash
icm store --topic "my-project" --content "PostgreSQL for main DB" --importance high
icm recall "database choice"
icm memoir create -n "system-architecture"
icm memoir link -m "system-architecture" --from "api-gateway" --to "auth-service" -r depends-on
```

### MCP Стек пам'яті: Патерни взаємодоповнення

```
doobidoo  → Рішення, ADR, бізнес-контекст
Serena    → Символи, структура, ключ-значення
grepai    → Семантичний пошук + граф викликів
Context7  → Офіційна документація
```

**Патерни**:
- Рішення / конвенція / баг / WIP → doobidoo
- Символи → Serena
- Викликаючі / пошук → grepai
- Документація → Context7

---

### Git MCP сервер (Офіційний Anthropic)

**Призначення**: 12 структурованих інструментів для Git: commit, diff, log, branch.

**Інструменти**: `git_status`, `git_diff_unstaged`, `git_diff_staged`, `git_diff`, `git_commit`, `git_add`, `git_reset`, `git_log`, `git_create_branch`, `git_checkout`, `git_show`, `git_branch`

**Налаштування**:
```bash
uvx mcp-server-git --repository /path/to/repo
```

**Конфіг** (`~/.claude.json`):
```json
{
  "mcpServers": {
    "git": {
      "command": "uvx",
      "args": ["mcp-server-git", "--repository", "/absolute/path/to/repo"]
    }
  }
}
```

---

### GitHub MCP сервер (Офіційний)

**Призначення**: Issues, PRs, Projects, Code search, GitHub Enterprise.

**Два режими**: віддалений (Copilot) або саморозміщений (GitHub PAT).

**Віддалений**:
```bash
claude mcp add --transport http github https://api.githubcopilot.com/mcp/
gh auth token  # → gho_xxx
# Додати Authorization header в ~/.claude.json
```

**Саморозміщений**:
```bash
export GITHUB_PERSONAL_ACCESS_TOKEN=ghp_xxx
./github-mcp-server stdio
```

**Можливості**: Issues, PRs, Projects v2, Code search, GitHub Enterprise.

</details>

---

### 📖 Цей гайд як MCP сервер

`claude-code-ultimate-guide-mcp` — 9 інструментів для пошуку в гайді без клонування.

**Встановлення** (`~/.claude.json`):
```json
{
  "mcpServers": {
    "claude-code-guide": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "claude-code-ultimate-guide-mcp"]
    }
  }
}
```

**Інструменти**: `search_guide`, `read_section`, `list_topics`, `get_example`, `list_examples`, `get_changelog`, `get_digest`, `get_release`, `get_cheatsheet`

**Слеш-команди**: `/ccguide:search`, `/ccguide:cheatsheet`, `/ccguide:digest`, `/ccguide:example`, `/ccguide:release`, `/ccguide:changelog`, `/ccguide:topics`, `/ccguide:init-docs`, `/ccguide:refresh-docs`, `/ccguide:diff-docs`, `/ccguide:search-docs`, `/ccguide:daily`

---

### 🌐 Екосистема MCP серверів спільноти

**8 валідованих серверів**: Playwright (Microsoft), Semgrep, Kubernetes (Red Hat), Context7, Linear, Vercel, Browserbase, MCP-Compose

**Приклад** (Playwright):
```bash
npm install @microsoft/playwright-mcp
# Конфіг:
{
  "mcpServers": {
    "playwright": {
      "command": "npx",
      "args": ["--yes", "@microsoft/playwright-mcp"]
    }
  }
}
```

---

## 8.3 Конфігурація

**Розташування**:
```
~/.claude.json          # Користувач (поле "mcpServers")
.mcp.json               # Проєкт (корінь, VCS)
```

Області: `local`, `project`, `user`. Використовуйте `claude mcp add --scope <scope>`.

**Поля**:

| Поле | Опис |
|------|-------|
| `command` | Виконуваний файл |
| `args` | Аргументи |
| `env` | Змінні середовища |
| `cwd` | Робоча директорія |

**Підстановка змінних**: `${VAR}`, `${VAR:-default}`

> ⚠️ `${workspaceFolder}` та `${env:VAR}` — це VS Code, не Claude Code.

**Динамічні заголовки (v2.1.85+)**: Розгалуження на `CLAUDE_CODE_MCP_SERVER_NAME` для різних токенів.

**Керування великими наборами**: мінімальна глобальна конфігурація (2-3 сервери), специфічні — в `.mcp.json`.

**MCP Tool Search** (v4): ліниве завантаження схем інструментів. Скорочення ~85% токенів (~77,000 → ~8,700). Точність: 49% → 74%.

### 8.3.1 MCP Secrets Management

**Проблема**: API ключі в `mcp.json` — ризик безпеки (коміти в Git, логи, крадіжка).

**Рішення**: Відокремити секрети від конфігурації.

**Три підходи**:

| Підхід | Безпека | Складність |
|----------|---------|------------|
| OS Keychain | Висока | Середня |
| .env + .gitignore | Середня | Низька |
| Secret Vaults | Дуже висока | Висока |

#### OS Keychain (рекомендовано)

**macOS**:
```bash
security add-generic-password -a "claude-mcp" -s "github-token" -w "ghp_token"
```

**MCP конфіг**:
```json
{
  "mcpServers": {
    "github": {
      "command": "bash",
      "args": ["-c", "GITHUB_TOKEN=$(security find-generic-password -s 'github-token' -w) npx @github/mcp-server"]
    }
  }
}
```

**Linux** (secret-tool) та **Windows** (Credential Manager) — аналогічно.

#### .env + .gitignore (простий)

```bash
cat > ~/.claude/.env << EOF
GITHUB_TOKEN=ghp_token
DATABASE_URL=postgresql://user:pass@localhost/db
EOF
chmod 600 ~/.claude/.env
```

**MCP конфіг**:
```json
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["@github/mcp-server"],
      "env": { "GITHUB_TOKEN": "${GITHUB_TOKEN}" }
    }
  }
}
```

#### Secret Vaults (Enterprise)

HashiCorp Vault, AWS Secrets Manager, 1Password CLI.

**Ротація секретів**:
```bash
# rotate-secret.sh
sed -i.bak "s|^${SECRET_NAME}=.*|${SECRET_NAME}=${NEW_VALUE}|" ~/.claude/.env
envsubst < ~/.claude/mcp-config.template.json > ~/.claude.json
pkill -f "mcp-server" || true
```

**Pre-commit хук**: блокує коміти з секретами (патерни: `sk-`, `ghp_`, `AKIA`, `api_key`).

**Чеклист перевірки**: .env не в Git, права 600, pre-commit хук встановлено.

---

## 8.4 Посібник з вибору сервера

**Дерево рішень**:

```
Що потрібно?
├─ Точний текст/патерн? → Grep / rg (~20ms)
├─ Глибоке розуміння коду? → Serena
├─ Пошук за призначенням? → grepai (~500ms)
├─ Хто що викликає? → grepai
├─ Документація бібліотеки? → Context7
├─ Складне міркування? → Sequential Thinking
├─ Запити до БД? → Postgres
├─ Тестування браузера? → Playwright
└─ Загальне завдання? → Вбудовані інструменти
```

**Комбінування серверів**:
```
1. Context7 → Офіційний патерн для auth
2. Serena → Знайти існуючий auth код
3. Sequential → Проаналізувати інтеграцію
4. Playwright → Протестувати реалізацію
```

**Case Study: Mergify** — підтримка через 5 систем. Claude Code + 5 MCP серверів.
- Час: ~15 хв → <5 хв (зменшення на ⅔)
- Точність: 75%

---

## 8.5 Система плагінів

Плагіни — пакунки, що об'єднують агенти, скіли та конфігурацію.

**Команди**:

| Команда | Призначення |
|---------|------------|
| `claude plugin` | Список плагінів |
| `claude plugin install <name>` | Встановити |
| `claude plugin install <name>@<mp>` | З конкретного маркетплейсу |
| `claude plugin enable <name>` | Увімкнути |
| `claude plugin disable <name>` | Вимкнути |
| `claude plugin uninstall <name>` | Видалити |
| `claude plugin update [name]` | Оновити |
| `claude plugin validate <path>` | Валідувати маніфест |

**Маркетплейси**:

```bash
claude plugin marketplace add <url-or-path>
claude plugin marketplace list
claude plugin marketplace remove <name>
```

**Тимчасове завантаження**:
```bash
claude --plugin-dir ~/.claude/custom-plugins
```

**Політика на рівні репозиторію** (`--add-dir`):
```bash
claude --add-dir /path/to/shared-config
```

**Створення плагіна**:
```
my-plugin/
├── .claude-plugin/plugin.json   # Маніфест
├── agents/my-agent.md           # Агенти
├── skills/code-review/SKILL.md  # Скіли
├── commands/my-cmd.md           # Команди
├── hooks/hooks.json             # Хуки
├── .mcp.json                    # MCP (опціонально)
└── .lsp.json                    # LSP (опціонально)
```

**Plugin vs MCP Server**:
- **Плагін** = "Як Claude мислить" (нові робочі процеси, спеціалізовані агенти)
- **MCP сервер** = "Що Claude може робити" (нові інструменти, зовнішні системи)

**LSP Native Support (v2.0.74+)**: 11 мов. Активується `ENABLE_LSP_TOOL=1`.

**Спільнота**:
- [wshobson/agents](https://github.com/wshobson/agents) — 67 плагінів
- [claude-plugins.dev](https://claude-plugins.dev) — 11,989 плагінів
- [awesome-claude-code](https://github.com/hesreallyhim/awesome-claude-code)

**Плагіни з цього гайду**: `security-suite`, `devops-pipeline`, `release-automation`, `code-quality`, `pr-workflow`, `session-tools`, `ai-methodology`, `session-summary`

**Встановлення**:
```bash
claude plugin marketplace add FlorianBruniaux/claude-code-plugins
```

**Vitals** — виявлення здоров'я кодової бази (git churn × складність × зв'язність):
```bash
/plugin marketplace add chopratejas/vitals
/plugin install vitals@vitals
/vitals:scan
```

**SE-CoVe** — Chain-of-Verification (Meta):
```bash
/plugin marketplace add vertti/se-cove-claude-plugin
/plugin install chain-of-verification
/chain-of-verification:verify <question>
```

**Cross-Model Review** — генерація однією моделлю, рев'ю іншою:
```bash
# Реалізація з Opus
claude --model opus
# Рев'ю з Sonnet
claude -p "Review last commit..." --model sonnet
# Швидка перевірка з Haiku
claude -p "List bugs in last commit" --model haiku
```

---

## 8.6 MCP Security

**Перед встановленням**:
- Перевірка джерела (зірки, організація, вендор)
- Аудит коду (без opaque бінарі)
- Мінімальні дозволи
- Активна підтримка
- Документація

**Тіньове перекриття інструментів**:

Зловмисний MCP сервер може оголосити інструменти з назвами вбудованих (Read, Write, Bash).

```
Легітимно:  Claude → Native Read → Ваш файл
Тінь:       Claude → MCP "Read" → Атакуючий
```

**Пом'якшення**: `/mcp`, `disallowedTools`, `permissions.deny`.

**Плутаний заступник**:

MCP сервер з підвищеними привілеями може бути використаний через prompt injection.

**Пом'якшення**: read-only за замовчуванням, мінімальні привілеї.

**Динамічне впровадження можливостей**:

MCP сервери можуть динамічно змінювати інструменти після першої перевірки.

**Пом'якшення**: фіксувати версії, періодично перевіряти.

**Мінімальні привілеї**:
```json
{
  "mcpServers": {
    "postgres": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-postgres"],
      "env": {
        "DATABASE_URL": "postgres://readonly_user:pass@host/db"
      }
    }
  }
}
```

**Червоні прапорці**:
- Запит credentials понад необхідне
- Інструменти shell без обґрунтування
- Немає вихідного коду
- Не оновлювалось 6+ місяців
- Мережевий доступ для локальної функціональності

**Аудит**:
```bash
claude
/mcp   # Список активних серверів та інструментів
```

**Найкраща практика**: аудит MCP раз на квартал, видалення невикористовуваних серверів.
