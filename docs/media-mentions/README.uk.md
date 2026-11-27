# Трекер згадок у медіа

Відстежує всі зовнішні джерела, що згадують Claude Code Ultimate Guide (GitHub або cc.bruniaux.com).

Цей файл залишається специфічним для посібника. Публічний міжпроєктний каталог, до якого входять Cowork, StarMapper,
CCBoard, CC-Copilot Bridge, ctxharness, Dep Scope, flow-lean, GSC MCP і Claude Code Plugins, міститься в
`src/data/mentions.json` у репозиторії портфоліо та опублікований на
`https://www.florian.bruniaux.com/mentions/`. RTK навмисно не входить до цього каталогу.

## Джерело істини

- `mentions.yaml`: один запис на кожну підтверджену згадку.
- `review-queue.yaml`: недоступні кандидати та відхилені хибні спрацювання, що зберігаються для майбутньої дедуплікації.

## Схема

```yaml
- id: "001"                  # Sequential, zero-padded
  platform: article          # article | reddit | linkedin-own | linkedin-other | twitter | directory | instagram | podcast | forum | video | translation
  url: "https://..."
  title: "..."
  author: "..."              # Handle, name, or publication name. Use "unknown" if not found.
  date: "YYYY-MM-DD"         # Publication date, or null if unknown
  angle: "..."               # One sentence: how they framed the guide
  reach: unknown             # low (<1K) | medium (1K-10K) | high (10K-100K) | viral (100K+) | unknown | null (own property)
  status: active             # active | dead | paywall
  notes: "..."               # Optional. Anything worth remembering (quote, context, SEO value).
  first_seen: "YYYY-MM-DD"   # Date we logged it
```

## Додавання нової згадки

1. Додайте запис до `mentions.yaml` з наступним послідовним id.
2. Оновіть `meta.total_mentions` і `meta.last_updated`.
3. Закомітьте: `docs: add media mention: [platform] [author/publication]`

## Slash command

`/track-mention <url>` ще не реалізовано. Поки що додавайте вручну.

## Статистика (станом на 2026-08-31)

| Платформа | Кількість |
|---|---|
| Статті / блоги | 12 |
| Відео (YouTube) | 2 |
| Подкасти | 1 |
| Reddit | 4 |
| LinkedIn (власні) | 2 |
| LinkedIn (сторонні) | 7 |
| Twitter / X | 3 |
| Instagram | 1 |
| Каталоги / реєстри | 14 |
| Форуми (HN) | 1 |
| Переклади / адаптації | 2 |
| **Разом** | **49** |

Серед 49 відстежуваних посилань 2 дописи належать Florian Bruniaux. Отже, каталог посібника містить
47 сторонніх посилань: 32 редакційні або спільнотні згадки, 2 переклади та 13 записів
у каталогах. Автоматизовані індекси є сигналами для виявлення, а не незалежними схваленнями. Каталог
портфоліо синхронізується окремо й може тимчасово відставати від цього джерела під час паралельної роботи.

### Виявлені мови

| Мова | Згадки |
|---|---|
| Англійська | 39 |
| Французька | 3 |
| Іспанська | 2 |
| Корейська | 1 |
| Китайська | 2 |
| Українська | 1 |
| Невідома | 1 |

## Slash command

Запустіть `/track-mentions`, щоб шукати нові згадки через Perplexity і автоматично оновлювати цей файл.

Для запусків без нагляду використовуйте `/track-mentions --scheduled`. Цей режим створює лише звіт про кандидатів:
він не має змінювати жоден із каталогів чи створювати коміт. Точний промпт для Perplexity та процедура рев'ю
описані в `perplexity-scheduled-search.md`.

Перевіряйте каталог і чергу рев'ю після кожного прийнятого оновлення:

```bash
python3 scripts/check-media-mentions.py
```
