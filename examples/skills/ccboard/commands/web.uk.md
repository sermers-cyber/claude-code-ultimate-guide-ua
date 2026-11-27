---
name: ccboard-web
description: Запустити веб-інтерфейс ccboard
category: monitoring
---

# Команда веб-інтерфейсу

Запускає веб-UI ccboard для моніторингу та візуалізації в браузері.

## Можливості

- **Веб-дашборд**: доступ до ccboard із будь-якого браузера
- **Живі оновлення**: Server-Sent Events (SSE) для даних у реальному часі
- **Адаптивний дизайн**: працює на десктопі, планшеті, мобільному
- **Ті самі дані**: спільний шар даних із TUI (один бінарник)
- **Одночасний доступ**: кілька користувачів можуть переглядати водночас

## Використання

```bash
# Launch web UI on default port 3333
/ccboard-web

# Or specify custom port
ccboard web --port 8080
```

## Доступ

Після запуску відкрийте в браузері:
```
http://localhost:3333
```

## Режими

ccboard підтримує 3 режими виконання:

1. **Лише TUI** (за замовчуванням):
   ```bash
   ccboard
   ```

2. **Лише веб**:
   ```bash
   ccboard web --port 3333
   ```

3. **Обидва одночасно**:
   ```bash
   ccboard both --port 3333
   ```
   Запускає TUI у терміналі + вебсервер на порту 3333

## Можливості веб-UI

- Дашборд зі статистикою в реальному часі
- Перегляд сесій із пагінацією
- Перегляд конфігурації (лише читання)
- Візуалізація hooks, агентів, витрат
- Стан MCP-серверів
- Історія і пошук

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

# Default port
PORT="${1:-3333}"

echo "🌐 Launching ccboard web interface..."
echo "Access at: http://localhost:$PORT"
echo ""
echo "Press Ctrl+C to stop"
echo ""

# Launch web UI
exec ccboard web --port "$PORT"
```

**Примітка**: веб-UI наразі в розробці. Основним інтерфейсом із повним набором функцій є TUI.
