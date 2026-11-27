---
name: dashboard
description: Запустити TUI-дашборд ccboard
category: monitoring
---

# Команда дашборду

Запускає інтерактивний TUI ccboard для візуалізації та моніторингу вашого використання Claude Code.

## Можливості

- **8 інтерактивних вкладок**: Dashboard, Sessions, Config, Hooks, Agents, Costs, History, MCP
- **Моніторинг у реальному часі**: відстеження файлів для живих оновлень
- **Керування MCP**: стан і конфігурація серверів
- **Відстеження витрат**: аналітика використання токенів і цін
- **Оглядач сесій**: перегляд історії розмов і пошук у ній
- **Редагування файлів**: натисніть `e`, щоб редагувати файли в $EDITOR

## Використання

```bash
# Launch TUI dashboard
/dashboard

# Alternative: run directly
ccboard
```

## Навігація

- `1-8` : перейти до конкретної вкладки
- `Tab` / `Shift+Tab` : перемикання вкладок
- `q` : вийти
- `F5` : оновити дані
- `e` : редагувати вибраний файл
- `o` : показати файл у Finder

## Вимоги

ccboard має бути встановлено. Якщо його не встановлено, запустіть:
```bash
/ccboard-install
```

## Реалізація

```bash
#!/bin/bash

# Check if ccboard is installed
if ! command -v ccboard &> /dev/null; then
    echo "❌ ccboard is not installed"
    echo ""
    echo "Install with:"
    echo "  /ccboard-install"
    echo ""
    echo "Or manually:"
    echo "  cargo install ccboard"
    exit 1
fi

# Launch ccboard TUI
exec ccboard
```
