# ccboard - плагін-дашборд для Claude Code

> Повноцінний TUI/Web-дашборд для моніторингу та керування Claude Code

[![License](https://img.shields.io/badge/license-MIT%20OR%20Apache--2.0-blue.svg)](../../../LICENSE)
[![Rust](https://img.shields.io/badge/rust-1.70%2B-orange.svg)](https://www.rust-lang.org)

## Швидкий старт

### Встановлення

```bash
# Using Claude Code command
/ccboard-install

# Or manually via cargo
cargo install ccboard
```

### Запуск дашборду

```bash
# Launch TUI
/dashboard

# Or run directly
ccboard
```

## Команди

| Команда | Опис |
|---------|-------------|
| `/dashboard` | Запустити інтерактивний TUI-дашборд |
| `/mcp-status` | Моніторинг MCP-серверів (натисніть `8`) |
| `/costs` | Аналітика витрат (натисніть `6`) |
| `/sessions` | Перегляд історії розмов (натисніть `2`) |
| `/ccboard-web` | Запустити веб-інтерфейс |
| `/ccboard-install` | Встановити або оновити ccboard |

## Можливості

- **8 інтерактивних вкладок**: Dashboard, Sessions, Config, Hooks, Agents, Costs, History, MCP
- **Моніторинг у реальному часі**: відстеження файлів для живих оновлень
- **Керування MCP**: стан і конфігурація серверів
- **Відстеження витрат**: аналітика використання токенів і цін (наприклад, $9,145 загалом)
- **Оглядач сесій**: перегляд 1.2K+ розмов у 33+ проєктах
- **Редагування файлів**: натисніть `e`, щоб редагувати файли в $EDITOR
- **Подвійний інтерфейс**: термінал (TUI) і веб-UI з одного бінарника

## Навігація

**Перехід до вкладки**:
- `1` Dashboard
- `2` Sessions
- `3` Config
- `4` Hooks
- `5` Agents
- `6` Costs
- `7` History
- `8` MCP

**Загальні клавіші**:
- `Tab` / `Shift+Tab` : перемикання вкладок
- `e` : редагувати файл у редакторі
- `o` : показати файл у Finder
- `q` : вийти
- `F5` : оновити

## Моніторинг MCP-серверів

Вкладка MCP (натисніть `8`) надає:

- **Живий стан**: ● працює, ○ зупинено, ? невідомо
- **Деталі сервера**: повна команда, аргументи, змінні середовища
- **Швидкі дії**:
  - `e` : редагувати `claude_desktop_config.json`
  - `o` : показати конфігурацію у Finder
  - `r` : оновити стан сервера

## Аналітика витрат

Відстежуйте свої витрати на Claude Code:

- Усього токенів: 17.32M
- Загальна вартість: $9,145.20
- Розподіл за моделями: Opus 4.5 (76%), Sonnet 4.5 (14%)
- Частка влучань у кеш: 99,9%

## Оглядач сесій

Переглядайте розмови й шукайте в них:

- 1.2K+ сесій у 33+ проєктах
- Повнотекстовий пошук (натисніть `/`)
- Метадані: часові мітки, токени, моделі
- Редагування файлів JSONL напряму

## Веб-інтерфейс

```bash
# Launch web UI
/ccboard-web

# Or with custom port
ccboard web --port 8080

# Run both TUI and Web
ccboard both --port 3333
```

## Вимоги

- **Rust 1.70+** і Cargo
- Встановлений **Claude Code** (читає з `~/.claude/`)

## Архітектура

Один бінарник Rust (2.4MB), що містить:
- **TUI**: термінальний інтерфейс на основі Ratatui
- **Web**: веб-інтерфейс на Axum + Leptos
- **Core**: спільний шар даних із відстеженням файлів

## Джерела даних

ccboard читає з:
- `~/.claude/stats-cache.json` - статистика
- `~/.claude/claude_desktop_config.json` - конфігурація MCP
- `~/.claude/projects/*/` - файли сесій JSONL
- `.claude/settings.json` - конфігурація

**Лише читання**: неінвазивний моніторинг, безпечно запускати разом із Claude Code.

## Продуктивність

- Початкове завантаження: <2 с для 1 000+ сесій
- Пам'ять: ~50MB у типовому використанні
- Ліниве завантаження: вміст сесій завантажується на вимогу

## Обмеження

Поточна версія (0.1.0):

- **Лише читання**: жодних операцій запису
- **Стан MCP**: лише Unix (macOS/Linux)
- **Веб-UI**: у розробці

## Усунення несправностей

### ccboard не знайдено
```bash
which ccboard          # Check if installed
/ccboard-install       # Install if needed
```

### Дані не відображаються
```bash
ls ~/.claude/          # Verify Claude Code directory
cat ~/.claude/stats-cache.json  # Check stats file
```

### Стан MCP "Unknown"
- Потребує Unix (macOS/Linux)
- Windows за замовчуванням показує "Unknown"
- Перевірте, що сервер запущено: `ps aux | grep <server-name>`

## Документація

- **Повний посібник**: повну документацію див. у [SKILL.md](SKILL.uk.md)
- **Команди**: див. директорію [commands/](commands/)
- **Скрипти**: див. директорію [scripts/](scripts/)

## Посилання

- **Репозиторій**: https://github.com/{OWNER}/ccboard
- **Issues**: https://github.com/{OWNER}/ccboard/issues
- **Claude Code**: https://claude.ai/code

## Ліцензія

MIT OR Apache-2.0

---

**Зроблено з ❤️ для спільноти Claude Code**
