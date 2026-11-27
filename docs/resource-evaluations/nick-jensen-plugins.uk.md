# Оцінка ресурсу: plugins Claude Code і продуктивність розробників

**URL**: https://www.nickjensen.co/posts/claude-code-plugins-developer-productivity
**Автор**: Nick Jensen (Product Engineering)
**Дата статті**: © 2026 NickJensen.co (явної дати публікації немає)
**Дата оцінки**: 2026-01-24
**Оцінювач**: Claude (через skill /eval-resource)

---

## Короткий підсумок

| Критерій | Значення |
|-----------|-------|
| **Початкова оцінка** | 3/5 |
| **Оцінка після перевірки** | 4/5 |
| **Оцінка після перевірки через Perplexity** | **2/5** (маргінально) |
| **Остаточне рішення** | НЕ інтегрувати напряму |
| **Причина** | Застаріла статистика, неперевірені твердження, існують кращі первинні джерела |

---

## Зміст

Стаття про plugins у Claude Code:
- Архітектура plugin (структура `.claude-plugin/` з manifest.json)
- Маркетплейси (наведено `wshobson/agents` зі статистикою)
- Встановлення й керування у воркфлоу
- Конкретні приклади: /test-report, /deploy, /review
- Бізнес-сценарії: командні стандарти, прискорення онбордингу

---

## Результати фактчекінгу

### Твердження, перевірені за текстом статті

| Твердження | У статті | Статус |
|-------|-----------|--------|
| Nick Jensen, Product Engineering | ✅ | Перевірено |
| © 2026 | ✅ | Перевірено |
| wshobson/agents: 63 plugins, 85 агентів, 47 skills | ✅ | **ЗАСТАРІЛО** |
| Онбординг 4-6 тиж → 1-2 тиж | ✅ | **НЕ ПЕРЕВІРЕНО незалежно** |
| 47 skills із поступовим розкриттям | ✅ | Перевірено |
| 44 інструменти у 23 категоріях | ✅ | Перевірено |

### Поглиблена перевірка через Perplexity

| Твердження | Реальність (січень 2026) | Джерело |
|-------|-------------------|--------|
| Статистика wshobson/agents | **67 plugins, 99 агентів, 107 skills** | README на GitHub |
| Покращення онбордингу | **Трапляється лише в цій статті** — жодної незалежної цитати | Кілька пошуків |
| Існування маркетплейсу | ✅ Підтверджено, активно підтримується (коміти за грудень 2025) | Активність на GitHub |

---

## Чому оцінка впала з 4/5 до 2/5

1. **Статистика застаріла**: 63/85/47 — це попередня версія, тепер 67/99/107
2. **Твердження про онбординг анекдотичне**: «4-6 тижнів → 1-2 тижні» більше ніде не трапляється
3. **Існують кращі первинні джерела**:
   - Офіційна документація Anthropic: code.claude.com/docs/en/plugins
   - README wshobson/agents (актуальна статистика)
   - Реєстр claude-plugins.dev (11 989 plugins, 63 065 skills)
   - Аналіз від Firecrawl із реальною кількістю встановлень

---

## Знайдені первинні джерела (кращі альтернативи)

| Джерело | Цінність | URL |
|--------|-------|-----|
| **Офіційна документація Anthropic** | Авторитетна структура plugin, схема маніфесту | code.claude.com/docs/en/plugins |
| **wshobson/agents** | 67 plugins, 99 агентів, 107 skills (станом на 2026-01-24), 38 296 зірок на GitHub станом на 2026-07-28 | github.com/wshobson/agents |
| **claude-plugins.dev** | Проіндексовано 11 989 plugins, 63 065 skills | claude-plugins.dev |
| **claudemarketplaces.com** | Автоматично сканує GitHub у пошуках маркетплейсів | claudemarketplaces.com |
| **Аналіз Firecrawl** | Реальна кількість встановлень (Context7: 72k, Ralph: 57k) | firecrawl.dev/blog/best-claude-code-plugins |
| **awesome-claude-code** | 20k+ зірок, курований список | github.com/hesreallyhim/awesome-claude-code |

---

## Виконані дії з інтеграції

Замість інтеграції статті Nick Jensen ми інтегрували **первинні джерела**:

### 1. Виправлено розділ 8.5 «Creating Custom Plugins» (guide/ultimate-guide.md)

**До** (некоректно):
```
my-plugin/
├── plugin.json           # Plugin manifest
```

**Після** (коректно згідно з документацією Anthropic):
```
my-plugin/
├── .claude-plugin/
│   └── plugin.json       # Plugin manifest (ONLY file in this dir)
├── agents/
├── skills/
├── commands/
├── hooks/
│   └── hooks.json
├── .mcp.json
├── .lsp.json
└── README.md
```

### 2. Додано підрозділ «Community Marketplaces» (~рядок 7245)

- wshobson/agents (67 plugins, 99 агентів, 107 skills)
- claude-plugins.dev (11 989 plugins, 63 065 skills)
- claudemarketplaces.com
- Популярні plugins із кількістю встановлень
- Посилання на awesome-claude-code

### 3. Оновлено reference.yaml

- Додано посилання на офіційну документацію Anthropic
- Додано ресурси маркетплейсів спільноти
- Додано популярні plugins із кількістю встановлень
- Додано посилання на awesome-список

---

## Отримані уроки

1. **Завжди перевіряйте статистику за первинними джерелами** — дописи в блогах часто наводять застарілі дані
2. **Твердження про продуктивність потребують зовнішнього підтвердження** — анекдотичні покращення не узагальнюються
3. **Дослідження через Perplexity виявило кращі джерела** — дані реєстрів > коментарі в блогах
4. **Спершу слід перевіряти офіційну документацію** — Anthropic має вичерпну документацію з plugins

---

## Пов'язані оцінки

- [se-cove-plugin.md](./se-cove-plugin.uk.md) — перший інтегрований приклад plugin

---

## Метадані

```yaml
evaluated_by: Claude (Opus 4.5)
skill_used: /eval-resource
time_spent: ~30 minutes
perplexity_used: Yes (user-provided research)
changes_made:
  - guide/ultimate-guide.md (Section 8.5)
  - machine-readable/reference.yaml
integration_decision: Rejected article, integrated primary sources instead
```
