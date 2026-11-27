# Стартер сесії ICM
> Вставте це на початку будь-якої сесії Claude Code, щоб активувати контекст ICM.
> Потрібен встановлений і налаштований ICM: `brew tap rtk-ai/tap && brew install icm`,
> потім `icm init --mode mcp && icm init --mode hook && icm init --mode skill`

---

# Контекст: у цій сесії активний ICM (Infinite Context Memory)

ICM встановлено й налаштовано на цій машині. Використовуй його, щоб зберігати й отримувати постійну
пам'ять між сесіями в обхід обмежень context window.

## Доступні MCP-інструменти

MCP-сервер `icm` запущено. Тобі доступні 22 інструменти `icm_*` для збереження,
пригадування та керування постійною пам'яттю.

**Прямий CLI** (через Bash, якщо потрібно):

```bash
# Store a memory
icm store --topic "<project-slug>" --content "<fact>" --importance high|medium|low|critical

# Recall by semantic query
icm recall "<natural language query>"

# Inspect
icm stats          # count, topics, avg weight
icm topics         # list all topics
icm list           # list recent memories

# Manage
icm forget <id>    # delete by ID
icm decay          # apply temporal decay
icm prune          # remove low-weight entries
```

**Важливо (синтаксис v0.5.0)**:
- `--importance` є переліченням: `critical / high / medium / low`, а не дробовим числом
- Підкоманди `memory` немає: використовуй безпосередньо `icm store`, `icm recall`
- Постійний граф знань: `icm memoir` (окремий шар, без згасання)

## Slash-команди

- `/recall <query>` — пошук у пам'яті ICM
- `/remember <content>` — зберегти спогад в ICM

## Як працюють спогади

Два шари:
- **Memories** (епізодичні): записи з часовими мітками, що згасають з часом залежно від важливості.
  Записи з важливістю `critical` ніколи не згасають. `low` поступово тьмяніють.
- **Memoir** (семантичний): постійний граф знань із типізованими зв'язками
  (`depends_on`, `contradicts`, `superseded_by`, `part_of` та ще 5).

Пошук гібридний: повнотекстовий BM25 (30%) + векторна схожість (70%).

Hook `PostToolUse` працює автоматично: кожні N викликів інструментів ICM виділяє контекст
і зберігає його без жодних явних дій з твого боку.

## Рекомендоване використання в цій сесії

```bash
# At session start — recall relevant context
icm recall "<current feature or topic>"

# When making a key decision
icm store --topic "<project>" --content "<decision and rationale>" --importance high

# For permanent architectural facts
icm memoir add-concept -m "<project>" -n "<concept>"
```

## Розташування БД

`~/Library/Application Support/dev.icm.icm/memories.db`
