---
name: "source-command-ccguide-init-docs"
description: "Завантажити офіційну документацію Anthropic Codex і зберегти як локальний базовий знімок"
---

# source-command-ccguide-init-docs

Використовуй цей skill, коли користувач просить виконати мігровану вихідну команду `ccguide-init-docs`.

## Command Template

Використай MCP-інструмент `init_official_docs`.

Він завантажує ~1.2MB з Anthropic (приблизно 5 с) і зберігає 4 локальні кеш-файли в ~/.cache/Codex-guide/.
Обидва знімки, базовий і поточний, встановлюються на цю версію.

Після успіху повідом користувачеві:
- Скільки розділів знайдено
- Шлях до знімка
- Що тепер можна виконати /ccguide:diff-docs після /ccguide:refresh-docs, щоб побачити зміни
