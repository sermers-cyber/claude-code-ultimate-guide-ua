---
name: mcp-status
description: Відкрити вкладку MCP-серверів у ccboard
category: monitoring
---

# Команда стану MCP

Запускає ccboard і переходить одразу до вкладки керування MCP-серверами.

## Можливості

- **Список серверів**: усі MCP-сервери, налаштовані в `claude_desktop_config.json`
- **Визначення стану**: живий стан (● працює, ○ зупинено, ? невідомо)
- **Деталі сервера**: повна команда, аргументи, змінні середовища
- **Швидкі дії**:
  - `e` : редагувати конфігурацію MCP
  - `o` : показати конфігурацію у Finder
  - `r` : оновити стан сервера

## Використання

```bash
# Open MCP tab directly
/mcp-status

# Alternative: run with tab argument
ccboard --tab mcp
```

## Навігація вкладкою MCP

- `h/j/k/l` або `←/→/↑/↓` : навігація
- `Enter` : фокус на панелі деталей
- `e` : редагувати `~/.claude/claude_desktop_config.json`
- `o` : показати файл конфігурації
- `r` : оновити стан сервера

## Стан сервера

- **● Зелений** : процес сервера працює
- **○ Червоний** : процес сервера зупинено
- **? Сірий** : стан невідомий (Windows або визначення не вдалося)

## Вимоги

ccboard має бути встановлено. За потреби запустіть `/ccboard-install`.

## Реалізація

```bash
#!/bin/bash

# Check if ccboard is installed
if ! command -v ccboard &> /dev/null; then
    echo "❌ ccboard is not installed"
    echo "Run: /ccboard-install"
    exit 1
fi

# Launch ccboard with MCP tab (tab index 7, accessible with '8' key)
# For now, launch and user presses '8'
# TODO: Add --tab flag to ccboard CLI in future version
exec ccboard
```

**Примітка**: наразі ccboard запускається у вигляді дашборду. Натисніть `8`, щоб перейти до вкладки MCP.
Майбутня версія підтримуватиме `ccboard --tab mcp` для прямого доступу.
