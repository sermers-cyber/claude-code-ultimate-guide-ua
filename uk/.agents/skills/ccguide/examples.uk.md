---
description: Перелічити всі шаблони за категоріями (agents/commands/hooks/skills/scripts)
---

Використай MCP-інструмент `list_examples`.

<% if (typeof $ARGUMENTS !== 'undefined' && $ARGUMENTS.trim()) { %>
Категорія: $ARGUMENTS
<% } else { %>
Покажи всі категорії.
<% } %>
