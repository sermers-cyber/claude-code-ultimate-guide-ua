---
name: ccboard
description: "Запуск і навігація TUI/Web-дашбордом ccboard для Claude Code. Використовуйте, щоб моніторити використання токенів, відстежувати витрати, переглядати сесії або перевіряти стан MCP-серверів у різних проєктах."
allowed-tools: Bash(ccboard*)
effort: low
metadata:
  version: 0.1.0
---

# ccboard - дашборд для Claude Code

Повноцінний TUI/Web-дашборд для моніторингу та керування вашим використанням Claude Code.

## Огляд

ccboard надає єдиний інтерфейс для візуалізації та дослідження всіх ваших даних Claude Code:

- **Сесії**: перегляд усіх розмов у ваших проєктах
- **Статистика**: використання токенів у реальному часі, частка влучань у кеш, тренди активності
- **MCP-сервери**: моніторинг і керування серверами Model Context Protocol
- **Витрати**: відстеження витрат із детальною розбивкою токенів і цін
- **Конфігурація**: перегляд каскадних налаштувань (Global > Project > Local)
- **Hooks**: дослідження hooks до/після виконання та автоматизації
- **Агенти**: керування власними агентами, командами та skills
- **Історія**: повнотекстовий пошук по всіх повідомленнях

## Встановлення

### Через cargo (рекомендовано)

```bash
# Using Claude Code command
/ccboard-install

# Or manually
cargo install ccboard
```

### Вимоги

- Rust 1.70+ і Cargo
- Встановлений Claude Code (читає з `~/.claude/`)

## Команди

| Команда | Опис | Швидкий доступ |
|---------|-------------|----------|
| `/dashboard` | Запустити TUI-дашборд | `ccboard` |
| `/mcp-status` | Відкрити вкладку MCP-серверів | Натисніть `8` |
| `/costs` | Відкрити аналіз витрат | Натисніть `6` |
| `/sessions` | Переглянути сесії | Натисніть `2` |
| `/ccboard-web` | Запустити веб-UI | `ccboard web` |
| `/ccboard-install` | Встановити/оновити ccboard | - |

## Можливості

### 8 інтерактивних вкладок

#### 1. Dashboard (натисніть `1`)
- Статистика використання токенів
- Кількість сесій
- Надіслані повідомлення
- Частка влучань у кеш
- Кількість MCP-серверів
- Sparkline активності за 7 днів
- Індикатори використання топ-5 моделей

#### 2. Sessions (натисніть `2`)
- Дві панелі: дерево проєктів + список сесій
- Метадані: часові мітки, тривалість, токени, моделі
- Пошук: фільтр за проєктом, повідомленням чи моделлю (натисніть `/`)
- Операції з файлами: `e` редагувати JSONL, `o` показати у Finder

#### 3. Config (натисніть `3`)
- Каскадний вигляд у 4 стовпці: Global | Project | Local | Merged
- Візуалізація успадкування налаштувань
- Конфігурація MCP-серверів
- Попередній перегляд правил (CLAUDE.md)
- Дозволи, hooks, змінні середовища
- Редагування конфігурації клавішею `e`

#### 4. Hooks (натисніть `4`)
- Перегляд hooks за подіями (PreToolUse, UserPromptSubmit)
- Попередній перегляд bash-скриптів hooks
- Патерни відповідності та умови
- Відстеження шляхів до файлів для зручного редагування

#### 5. Agents (натисніть `5`)
- 3 підвкладки: Agents (12) | / Commands (5) | ★ Skills (0)
- Видобування метаданих із frontmatter
- Попередній перегляд і редагування файлів
- Рекурсивне сканування директорій

#### 6. Costs (натисніть `6`)
- 3 види: Overview | By Model | Daily Trend
- Розбивка токенів: вхідні, вихідні, читання/запис кешу
- Ціни: загальна оцінка витрат
- Розподіл за моделями

#### 7. History (натисніть `7`)
- Повнотекстовий пошук по всіх сесіях
- Гістограма активності за годинами (24 год)
- Sparkline за 7 днів
- Пошук по всіх повідомленнях

#### 8. MCP (натисніть `8`) **НОВЕ**
- Дві панелі: список серверів (35%) | деталі (65%)
- Визначення стану наживо: ● працює, ○ зупинено, ? невідомо
- Повні деталі сервера: команда, аргументи, змінні середовища
- Швидкі дії: `e` редагувати конфігурацію, `o` показати файл, `r` оновити стан

### Навігація

**Глобальні клавіші**:
- `1-8` : перейти до вкладки
- `Tab` / `Shift+Tab` : перемикання вкладок
- `q` : вийти
- `F5` : оновити дані

**У стилі Vim**:
- `h/j/k/l` : навігація (ліворуч/вниз/вгору/праворуч)
- `←/→/↑/↓` : альтернатива стрілками

**Загальні дії**:
- `Enter` : переглянути деталі / фокус на панелі
- `e` : редагувати файл у $EDITOR
- `o` : показати файл у Finder
- `/` : пошук (у вкладках Sessions/History)
- `Esc` : закрити спливне вікно / скасувати

### Моніторинг у реальному часі

ccboard має механізм відстеження файлів, що стежить за змінами в `~/.claude/`:

- **Оновлення статистики**: живе оновлення, коли змінюється `stats-cache.json`
- **Оновлення сесій**: нові сесії з'являються автоматично
- **Оновлення конфігурації**: зміни налаштувань відображаються в UI
- **Debounce 500 мс**: запобігає надмірним оновленням

### Редагування файлів

Натисніть `e` на будь-якому елементі, щоб відкрити його в улюбленому редакторі:

- Використовує `$VISUAL` > `$EDITOR` > типовий для платформи (nano/notepad)
- Підтримує: Sessions (JSONL), Config (JSON), Hooks (Shell), Agents (Markdown)
- Стан термінала зберігається (режим альтернативного екрана)
- Кросплатформно (macOS, Linux, Windows)

### Керування MCP-серверами

Вкладка MCP забезпечує всебічний моніторинг серверів:

**Визначення стану** (Unix):
- Перевіряє запущені процеси через `ps aux`
- Видобуває назву пакета з команди
- Показує PID, коли сервер працює
- Windows показує стан "Unknown"

**Деталі сервера**:
- Повна команда й аргументи
- Змінні середовища зі значеннями
- Шлях до файлу конфігурації (`~/.claude/claude_desktop_config.json`)
- Швидкі дії редагування/показу

**Навігація**:
- `h/l` або `←/→` : перемикання між списком і деталями
- `j/k` або `↑/↓` : вибір сервера
- `Enter` : фокус на панелі деталей
- `e` : редагувати конфігурацію MCP
- `o` : показати конфігурацію у Finder
- `r` : оновити стан сервера

## Приклади використання

### Щоденний моніторинг

```bash
# Launch dashboard
/dashboard

# Check activity and costs
# Press '1' for overview
# Press '6' for costs breakdown
# Press '7' for recent history
```

### Усунення проблем із MCP

```bash
# Open MCP tab
/mcp-status

# Or: ccboard then press '8'

# Check server status (● green = running)
# Press 'e' to edit config if needed
# Press 'r' to refresh status after changes
```

### Аналіз сесій

```bash
# Browse sessions
/sessions

# Press '/' to search
# Filter by project: /my-project
# Filter by model: /opus
# Press 'e' on session to view full JSONL
```

### Відстеження витрат

```bash
# View costs
/costs

# Press '1' for overview
# Press '2' for breakdown by model
# Press '3' for daily trend

# Identify expensive sessions
# Track cache efficiency (99.9% hit rate)
```

## Веб-інтерфейс

Запустіть інтерфейс у браузері для віддаленого моніторингу:

```bash
# Launch web UI
/ccboard-web

# Or with custom port
ccboard web --port 8080

# Access at http://localhost:3333
```

**Можливості**:
- Ті самі дані, що й у TUI (спільний бекенд)
- Server-Sent Events (SSE) для живих оновлень
- Адаптивний дизайн (десктоп/планшет/мобільний)
- Одночасний доступ кількох користувачів

**Запуск обох одночасно**:
```bash
ccboard both --port 3333
```

## Архітектура

ccboard є одним бінарником Rust із двома фронтендами:

```
ccboard/
├── ccboard-core/      # Parsers, models, data store, watcher
├── ccboard-tui/       # Ratatui frontend (8 tabs)
└── ccboard-web/       # Axum + Leptos frontend
```

**Джерела даних**:
- `~/.claude/stats-cache.json` - статистика
- `~/.claude/claude_desktop_config.json` - конфігурація MCP
- `~/.claude/projects/*/` - файли сесій JSONL
- `~/.claude/settings.json` - глобальні налаштування
- `.claude/settings.json` - налаштування проєкту
- `.claude/settings.local.json` - локальні перевизначення
- `.claude/CLAUDE.md` - правила й поведінка

## Усунення несправностей

### ccboard не знайдено

```bash
# Check installation
which ccboard

# Install if needed
/ccboard-install
```

### Дані не відображаються

```bash
# Verify Claude Code is installed
ls ~/.claude/

# Check stats file exists
cat ~/.claude/stats-cache.json

# Run with specific project
ccboard --project ~/path/to/project
```

### Стан MCP показує "Unknown"

- Визначення стану потребує Unix (macOS/Linux)
- Windows за замовчуванням показує "Unknown"
- Перевірте, чи справді запущено процес сервера: `ps aux | grep <server-name>`

### Відстеження файлів не працює

- Переконайтеся, що crate `notify` підтримує вашу платформу
- Перевірте дозволи на файли в `~/.claude/`
- Перезапустіть ccboard, якщо події файлової системи було пропущено

## Розширене використання

### Параметри командного рядка

```bash
ccboard --help              # Show all options
ccboard --claude-home PATH  # Custom Claude directory
ccboard --project PATH      # Specific project
ccboard stats               # Print stats and exit
ccboard web --port 8080     # Web UI on port 8080
ccboard both                # TUI + Web simultaneously
```

### Змінні середовища

```bash
# Editor preference
export EDITOR=vim
export VISUAL=code

# Custom Claude home
export CLAUDE_HOME=~/custom/.claude
```

### Інтеграція з Claude Code

ccboard читає директорії Claude Code **лише для читання**:

- Неінвазивний моніторинг
- Жодних змін у даних Claude
- Безпечно запускати одночасно з Claude Code
- Механізм відстеження файлів бачить зміни в реальному часі

## Продуктивність

- **Розмір бінарника**: 2.4MB (release-збірка)
- **Початкове завантаження**: <2 с для 1 000+ сесій
- **Пам'ять**: ~50MB у типовому використанні
- **CPU**: <5% під час моніторингу
- **Ліниве завантаження**: вміст сесій завантажується на вимогу

## Обмеження

Поточна версія (0.1.0):

- **Лише читання**: жодних операцій запису в дані Claude
- **Стан MCP**: лише Unix (Windows показує "Unknown")
- **Веб-UI**: у розробці (основний інтерфейс TUI)
- **Пошук**: базовий пошук підрядка (нечіткого пошуку поки немає)

Плани на майбутнє:

- Розширене керування MCP-серверами (запуск/зупинка)
- Перевірки здоров'я протоколу MCP
- Експорт звітів (PDF, JSON, CSV)
- Редагування конфігурації (запис settings.json)
- Інтеграція з відновленням сесій
- Покращений пошук із нечітким збігом

## Внесок

ccboard має відкритий код (MIT OR Apache-2.0).

Репозиторій: https://github.com/{OWNER}/ccboard

Внески вітаються:
- Звіти про баги й запити функцій
- Pull requests із новими функціями
- Покращення документації
- Тестування на конкретних платформах (Windows, Linux)

## Подяки

Створено з використанням:
- [Ratatui](https://ratatui.rs/) - фреймворк для термінального UI
- [Axum](https://github.com/tokio-rs/axum) - вебфреймворк
- [Leptos](https://leptos.dev/) - реактивний фронтенд
- [Notify](https://github.com/notify-rs/notify) - відстеження файлів
- [Serde](https://serde.rs/) - серіалізація

## Ліцензія

MIT OR Apache-2.0

---

**Є питання?**

- GitHub Issues: https://github.com/{OWNER}/ccboard/issues
- Документація: https://github.com/{OWNER}/ccboard
- Claude Code: https://claude.ai/code
