# Оцінка ресурсу: Context7 CLI (ctx7)

**URL**: https://context7.com/docs/clients/cli
**Дата**: 2026-03-17
**Оцінювач**: Claude Sonnet 4.6
**Оцінка**: 4/5

## Підсумок

CLI-компаньйон для MCP-сервера Context7 (Upstash). Охоплює три функції: отримання документації бібліотек у терміналі, керування skills (встановлення/пошук/рекомендації/генерація), налаштування Context7 для Claude Code.

Ключові команди:
- `npx ctx7 skills suggest`: автоматично визначає залежності проєкту й рекомендує відповідні skills
- `npx ctx7 skills install owner/repo`: встановлює з будь-якого репозиторію GitHub
- `npx ctx7 setup --claude`: майстер налаштування режиму MCP або CLI+Skills
- `npx ctx7 library [name]` / `ctx7 docs [id] [query]`: пошук документації без браузера

## Рішення

**Інтегровано** в `guide/ultimate-guide.md` §5.5 як новий підрозділ «Registry-based Discovery: ctx7 CLI» (~60 рядків) і примітку з перехресним посиланням у розділі Context7 файлу `guide/ecosystem/mcp-servers-ecosystem.md`.

## Ключовий висновок

Наявний робочий процес (curl/unzip з GitHub) замінюється на `ctx7 skills suggest` + `ctx7 skills install`, що додає врахування залежностей і оцінки довіри. Посібник документував ручний процес 2024 року для екосистеми 2025-го.

## Примітка щодо фактчекінгу

Перший виклик WebFetch вигадав, що Context7 «Built by Anthropic»; це хибно. Context7 — продукт Upstash (підтверджено в mcp-servers-ecosystem.md: `@upstash/context7-mcp`). Виправлено до інтеграції.

## Зв'язок між реєстрами

- `agentskills.io` = відкрита специфікація (30+ платформ, визначений формат skill), §5.1 посібника
- `context7.com/skills` = розміщений реєстр сумісних skills з оцінками довіри
- Вони доповнюють, а не конкурують одне з одним. Задокументовано під час інтеграції в посібник.
