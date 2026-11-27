---
description: Щоденна перевірка оновлень — diff офіційної документації Anthropic + дайджест релізів посібника і CC
---

Виконай цю послідовність по порядку. Подай результати одним зведеним звітом.

## Крок 1 — Оновити офіційну документацію

Виклич MCP-інструмент `refresh_official_docs`, щоб отримати найновішу документацію Anthropic і оновити поточний знімок.

Якщо він завершується помилкою (немає базового знімка), скажи користувачеві спочатку один раз виконати /ccguide:init-docs, і зупинись.

## Крок 2 — Diff офіційної документації

Виклич MCP-інструмент `diff_official_docs`, щоб порівняти базовий знімок із оновленим поточним.

## Крок 3 — Дайджест посібника та релізів CC

Виклич MCP-інструмент `get_digest` із period: "day"

---

## Формат виводу

Подай усе як єдиний щоденний брифінг:

```
# Daily Claude Code Update — {today's date}

## Official Anthropic Docs
{diff results — added/removed/modified sections, or "No changes"}

## Guide + CC CLI
{digest results — guide CHANGELOG entries + CC releases from last 24h, or "No changes"}

---
Docs snapshot: {baseline date} → {current date}
```

Правила:
- Якщо ніде немає змін: скажи про це чітко одним рядком, без води
- Відтворюй УСІ URL дослівно (URL джерел, посилання на GitHub)
- Якщо офіційна документація не змінилась І немає оновлень посібника/CC: "Nothing changed in the last 24h."
- Пиши щільно: це щоденний брифінг, а не звіт
