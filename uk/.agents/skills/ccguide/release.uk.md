---
description: Показати нотатки до релізів Claude Code CLI
---

Використай MCP-інструмент `get_release`.

<% if (typeof $ARGUMENTS !== 'undefined' && $ARGUMENTS.trim()) { %>
Версія: $ARGUMENTS
<% } else { %>
Покажи останній реліз і попередні 5.
<% } %>
