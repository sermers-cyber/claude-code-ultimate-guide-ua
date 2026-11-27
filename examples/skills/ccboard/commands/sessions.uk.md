---
name: sessions
description: Переглянути історію сесій Claude Code
category: exploration
---

# Команда перегляду сесій

Запускає ccboard і переходить одразу до вкладки дослідження сесій.

## Можливості

- **Дерево проєктів**: навігація 33+ проєктами з вкладеною структурою
- **Список сесій**: 1.2K+ сесій із метаданими
- **Пошук**: фільтр сесій за проєктом, повідомленням чи моделлю (натисніть `/`)
- **Деталі сесії**:
  - Часові мітки (початок, кінець, тривалість)
  - Розбивка використання токенів
  - Використані моделі
  - Попередній перегляд першого повідомлення
- **Операції з файлами**:
  - `e` : відкрити JSONL сесії в редакторі
  - `o` : показати файл сесії у Finder

## Використання

```bash
# Open sessions tab directly
/sessions

# Alternative: run with tab argument
ccboard --tab sessions
```

## Навігація вкладкою Sessions

- `←/→` : перемикання між деревом проєктів і списком сесій
- `↑/↓` : навігація елементами
- `Enter` : переглянути деталі сесії
- `/` : відкрити поле пошуку
- `e` : редагувати JSONL-файл вибраної сесії
- `o` : показати файл сесії

## Метадані сесії

Для кожної сесії показується:
- **ID**: унікальний ідентифікатор сесії
- **Started**: часова мітка першого повідомлення
- **Duration**: загальний час розмови
- **Messages**: кількість повідомлень
- **Tokens**: загальна кількість використаних токенів
- **Models**: використані AI-моделі (наприклад, opus-4.5, sonnet-4.5)
- **Preview**: перше повідомлення користувача (200 символів)

## Приклади пошуку

```
# Search by project name
/my-project

# Search by model
/opus

# Search by message content
/implement feature
```

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

# Launch ccboard with Sessions tab (tab index 1, accessible with '2' key)
# For now, launch and user presses '2'
exec ccboard
```

**Примітка**: наразі ccboard запускається у вигляді дашборду. Натисніть `2`, щоб перейти до вкладки Sessions.
Майбутня версія підтримуватиме `ccboard --tab sessions` для прямого доступу.
