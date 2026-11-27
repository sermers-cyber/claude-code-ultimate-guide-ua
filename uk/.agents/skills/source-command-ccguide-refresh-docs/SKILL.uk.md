---
name: "source-command-ccguide-refresh-docs"
description: "Повторно завантажити офіційну документацію Anthropic Codex і оновити поточний знімок (базовий не змінюється)"
---

# source-command-ccguide-refresh-docs

Використовуй цей skill, коли користувач просить виконати мігровану вихідну команду `ccguide-refresh-docs`.

## Command Template

Використай MCP-інструмент `refresh_official_docs`.

Він завантажує ~1.2MB з Anthropic (приблизно 5 с) і оновлює лише "поточний" знімок.
Базовий знімок (встановлений через init_official_docs) ніколи не змінюється.

Після успіху покажи швидкий попередній diff щодо базового знімка, який повертає інструмент.
Нагадай користувачеві виконати /ccguide:diff-docs, щоб отримати повний детальний diff.
