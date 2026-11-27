# Оцінка: Kairn: Knowledge graph memory MCP

**Дата**: 2026-02-25
**Оцінювач**: Claude (skill eval-resource)
**Оцінка**: 4/5 — Інтегровано

---

## Оцінені джерела

1. **Допис у LinkedIn**: Robin Lorenz, «Context Engineering for Claude Code», 24 лют. 2026
   - Оцінка: 2/5 — список спостереження (твердження неможливо перевірити, немає вихідного коду)
2. **Репозиторій GitHub**: [kairn-ai/kairn](https://github.com/kairn-ai/kairn) (MIT, Python 100%)
   - Оцінка: 4/5 — **Інтегровано**

---

## Підсумок щодо Kairn

MCP-сервер на Python, що пропонує пам'ять, організовану як knowledge graph, з 18 інструментами.

**Ключові відмінності порівняно з Serena/doobidoo**:
- Типізовані зв'язки (`depends-on`, `resolves`, `causes`)
- Біологічна модель згасання: розв'язки ~200 днів, обхідні шляхи ~50 днів (автоматичне очищення)
- Повнотекстовий пошук + маршрутизація за рівнем довіри
- Між сесіями та між IDE

---

## Рішення щодо інтеграції

| Змінений елемент | Опис |
|-----------------|-------------|
| `guide/ultimate-guide.md` ~10233 | Новий розділ «Kairn: Knowledge Graph Memory with Biological Decay» |
| `guide/ultimate-guide.md` | Comparison Matrix + таблиця «When to use» — додано стовпець Kairn |
| `guide/ultimate-guide.md` | Обмеження Doobidoo «No expiration» → вказує на Kairn |
| `examples/config/mcp.json` | Додано запис `kairn` |

---

## Список спостереження — LinkedIn Lorenz

**Оцінка: 2/5**: переоцінити, якщо до допису з'явиться репозиторій/технічна стаття.

Причина відхилення: допис у LinkedIn без вихідного коду, статистику неможливо перевірити (зменшення токенів на 93%), Perplexity не знайшов жодних незалежних слідів. Філософія «infrastructure outlives prompts» уже охоплена в `guide/core/methodologies.md`.

**Тригер для повторного оцінювання**: публікація репозиторію GitHub до допису.
