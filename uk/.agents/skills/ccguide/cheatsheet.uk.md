---
description: Показати шпаргалку Claude Code (повну або відфільтровану за розділом)
---

Використай MCP-інструмент `get_cheatsheet`.

<% if (typeof $ARGUMENTS !== 'undefined' && $ARGUMENTS.trim()) { %>
Відфільтруй за розділом: $ARGUMENTS
<% } else { %>
Поверни повну шпаргалку.
<% } %>
