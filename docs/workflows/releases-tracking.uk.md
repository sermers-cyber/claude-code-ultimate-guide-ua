# Відстеження релізів Claude Code

Цей репозиторій підтримує стислу історію офіційних релізів Claude Code.

## Файли

| Файл | Роль |
|------|------|
| `machine-readable/claude-code-releases.yaml` | Локальне джерело істини для стислої історії релізів і значення `latest` |
| `guide/core/claude-code-releases.md` | Версія для читання людьми (Markdown) |
| `mcp-server/content/claude-code-releases.yaml` | Побайтово ідентичний реєстр релізів, що постачається разом із MCP-пакетом |
| `llms.txt`, `machine-readable/llms.txt`, `mcp-server/content/llms.txt` | Побайтово ідентичні індекси для навігації, що оголошують відстежувану версію `latest` |
| `scripts/update-cc-releases.sh` | Скрипт для перевірки нових версій |

Офіційний changelog Claude Code від Anthropic є апстрімним джерелом. Локальний YAML — це переглянутий стислий виклад, тож локальна узгодженість не доводить, що відстеження апстріму актуальне чи повне.

## Перевірка нових версій

```bash
./scripts/update-cc-releases.sh
```

Скрипт:
1. Отримує офіційний CHANGELOG з GitHub
2. Порівнює його з відстежуваною нами версією
3. Показує нові релізи, які треба стисло описати

## Воркфлоу оновлення

1. **Перевірка**: `./scripts/update-cc-releases.sh`
2. **Оновлення YAML**: додайте новий запис у `claude-code-releases.yaml`
   - Оновіть `latest` і `updated`
   - Додайте запис у `releases` (стисло: максимум 2-4 головні пункти)
   - Додайте до `breaking_summary`, якщо це доречно
   - Додайте до `milestones`, якщо це велика функція
3. **Оновлення Markdown**: узгоджено оновіть `claude-code-releases.md`
4. **Оновлення дзеркал**: скопіюйте переглянутий YAML у `mcp-server/content/claude-code-releases.yaml`
5. **Оновлення версії для навігації**: змініть речення з версією в усіх трьох дзеркалах `llms.txt` на значення `latest` з YAML
6. **Перевірка локального зв'язку**:

   ```bash
   python3 scripts/validate-reference-yaml.py --ci
   (cd mcp-server && node --test --test-name-pattern='canonical MCP guide is complete' test/render-product-docs.test.mjs)
   ```

7. **Синхронізація лендингу**: `./scripts/check-landing-sync.sh`
8. **Коміт**: `docs: update Claude Code releases (vX.Y.Z)`

Тест MCP спершу вимагає, щоб три файли `llms.txt` були побайтово ідентичними, потім розбирає `machine-readable/claude-code-releases.yaml` і порівнює його значення `latest` з версією, оголошеною в `llms.txt`. `npm run release:check` виконує цей тест у CI-воркфлоу `index-integrity`. Перевірка доводить узгодженість репозиторію й пакета. Вона не отримує changelog від Anthropic і не доводить повноти стислого опису релізів.

## Формат запису YAML

```yaml
- version: "2.1.13"
  date: "2026-01-20"
  highlights:
    - "Main feature"
    - "Other notable feature"
  breaking:
    - "Description of breaking change (if applicable)"
```
