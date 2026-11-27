---
title: "Шаблон плагіна claude-mem"
description: "Плагін автоматичної постійної пам'яті, що фіксує виклики інструментів і рішення між сесіями"
tags: [plugin, memory, integration]
---

# Шаблон плагіна claude-mem

**Призначення**: автоматична постійна пам'ять між сесіями Claude Code
**Репозиторій**: https://github.com/thedotmack/claude-mem
**Тип**: офіційний плагін (понад 26.5k зірок)
**Версія**: v10.6.3
**Ліцензія**: AGPL-3.0 + PolyForm Noncommercial

---

## Що він робить

claude-mem автоматично фіксує **все, що Claude робить** під час ваших сесій програмування:
- Виклики інструментів (Read, Edit, Bash, Grep тощо)
- Спостереження та знахідки
- Архітектурні рішення
- Зміни файлів

А потім **розумно впроваджує** релевантний контекст, коли ви повертаєтеся до проєкту.

**Результат**: більше ніяких «що ми робили минулого разу?» → Claude пам'ятає.

---

## Встановлення

### Через plugin marketplace (рекомендовано)

```bash
# Add marketplace
/plugin marketplace add thedotmack/claude-mem

# Install plugin
/plugin install claude-mem

# Restart Claude Code
exit
claude
```

### Ручне встановлення

```bash
# Requires Bun runtime (not Node) — install first if needed:
# curl -fsSL https://bun.sh/install | bash

# Clone repository
git clone https://github.com/thedotmack/claude-mem.git ~/.claude/plugins/claude-mem

# Install dependencies
cd ~/.claude/plugins/claude-mem
bun install

# Restart Claude Code
```

> **Залежність**: воркер claude-mem працює на [Bun](https://bun.sh), а не на Node. Якщо у вас встановлено лише Node, спочатку встановіть Bun. Без нього воркер не запуститься, і сесії не фіксуватимуться (fail-open: Claude Code продовжує працювати, просто без запису пам'яті).

---

## Конфігурація

### Конфігурація за замовчуванням

claude-mem працює **одразу після встановлення** з розумними налаштуваннями за замовчуванням:

```json
{
  "worker": {
    "port": 37777,
    "host": "127.0.0.1"
  },
  "storage": {
    "location": "~/.claude-mem/claude-mem.db",
    "backend": "sqlite"
  },
  "indexation": {
    "provider": "chroma",
    "embeddings": "claude"
  },
  "privacy": {
    "excludeTags": ["<private>", "</private>"]
  }
}
```

> ⚠️ **Безпека**: завжди використовуйте `host: "127.0.0.1"`, ніколи `"0.0.0.0"`. Ендпоінт `GET /api/settings` повертає API-ключі відкритим текстом: будь-який локальний процес (розширення браузера, npm-пакет) може їх прочитати. Прив'язка лише до localhost зменшує поверхню атаки, але не усуває її на спільних машинах.

### Власна конфігурація

Створіть `~/.claude-mem/config.json`:

```json
{
  "worker": {
    "port": 38888,
    "host": "localhost"
  },
  "compression": {
    "enabled": true,
    "summaryLength": "medium"
  },
  "privacy": {
    "excludeTags": ["<private>", "</private>", "<secret>", "</secret>"],
    "autoDetectSecrets": false
  },
  "storage": {
    "maxObservations": 10000,
    "retentionDays": 90
  }
}
```

**Параметри**:

| Параметр | Значення | Опис |
|--------|--------|-------------|
| `compression.enabled` | true/false | Увімкнути AI-стиснення (за замовчуванням: true) |
| `compression.summaryLength` | short/medium/long | Докладність підсумків |
| `privacy.autoDetectSecrets` | true/false | Автовиявлення API-ключів (за замовчуванням: false) |
| `storage.maxObservations` | number | Максимальна кількість збережених спостережень |
| `storage.retentionDays` | number | Автовидалення через N днів |

---

## Використання

### Автоматична фіксація (поведінка за замовчуванням)

**Жодних команд не потрібно**: claude-mem автоматично:

1. **Фіксує** використання інструментів через lifecycle hooks
2. **Стискає** спостереження за допомогою AI-підсумків
3. **Індексує** через векторну базу даних Chroma
4. **Впроваджує** релевантний контекст на початку сесії

**Приклад перебігу сесій**:

```
Session 1 (Day 1):
User: "Explore auth module"
Claude: [Reads auth.service.ts, session.middleware.ts]
claude-mem: [Captures] "Auth exploration: JWT validation, session middleware"

Session 2 (Day 2):
Claude: [Auto-injected]
"Previously: Explored auth module.
 Files: auth.service.ts, session.middleware.ts
 Key finding: JWT validation in validateToken()"
User: "Refactor auth to use jose library"
Claude: [Already has context, no re-reading]
```

---

### Доступні skills

claude-mem постачається з 5 skills, доступними через `/claude-mem:<skill>`:

| Skill | Тригер | Сценарій використання |
|-------|---------|----------|
| `mem-search` | "How did we fix X?" | Пошук в історії сесій природною мовою |
| `smart-explore` | "Explore the auth module" | Навігація кодом на основі AST (економна щодо токенів) |
| `make-plan` | "Plan a refactor of Y" | Поетапний план реалізації з пошуком документації |
| `do` | "Execute the plan" | Виконує результат `make-plan` через субагентів |
| `timeline-report` | "Show my journey" | Наративний звіт про всю історію проєкту |

### Пошук природною мовою (skill `mem-search`)

Шукайте в історії сесій природною мовою:

```bash
# Search for specific topics
"Search my memory for authentication decisions"
"What files did we modify for the payment bug?"
"Remind me why we chose Zod over Yup"
"Show me all sessions where we worked on the API"
```

Skill повертає:
- Відповідні сесії з підсумками
- Релевантні спостереження (типізовані: DISCOVERY / CHANGE / FEATURE / BUGFIX)
- Історію змін файлів
- Архітектурні рішення

---

### Вебпанель

Відкрийте інтерфейс реального часу за адресою `http://localhost:37777`:

```bash
# Open dashboard
open http://localhost:37777

# Features:
# - Timeline view (all sessions chronologically)
# - Natural language search bar
# - Observation details (tool calls + results)
# - Session statistics (duration, tool usage, files modified)
# - Export/import functionality
```

**Розділи панелі**:

| Розділ | Опис |
|---------|-------------|
| **Timeline** | Хронологічний перегляд усіх сесій |
| **Search** | Інтерфейс запитів природною мовою |
| **Sessions** | Перегляд списком із фільтрами |
| **Statistics** | Аналітика використання й тенденції |
| **Settings** | Керування приватністю, керування сховищем |

---

### Керування приватністю

#### Використання тегів `<private>`

```markdown
<!-- In your prompts -->
Modify the database connection to use:
<private>
Host: prod-db-123.aws.com
Username: admin
Password: super-secret-password
API Key: sk-1234567890abcdef
</private>

<!-- claude-mem excludes content between <private> tags -->
```

#### Ручне виключення спостережень

```bash
# Delete specific observation
curl -X DELETE http://localhost:37777/api/observations/obs_123

# Clear all observations for a session
curl -X DELETE http://localhost:37777/api/sessions/session_456/observations
```

#### Розташування даних

```bash
# Database location
~/.claude-mem/claude-mem.db

# Chroma index
~/.claude-mem/chroma/

# View database size
du -sh ~/.claude-mem/
```

---

## Розширені можливості

### Поступове розкриття

claude-mem використовує тришаровий підхід, щоб мінімізувати витрату токенів:

```
Layer 1: Search (50-100 tokens)
├─ Query: "Find authentication work"
├─ Returns: 5 session summaries
│
Layer 2: Timeline (500-1000 tokens)
├─ Query: "Show session abc123 timeline"
├─ Returns: Observation list
│
Layer 3: Details (full context)
└─ Query: "Get observation obs_456 details"
    Returns: Complete tool call + result
```

**Економія токенів**: приблизно в 10 разів менше порівняно із завантаженням повної історії.

---

### Endless mode (бета)

Експериментальна функція для подовжених сесій:

```bash
# Enable in config
{
  "experimental": {
    "endlessMode": true
  }
}
```

**Заявлено** (незалежно не перевірено):
- ~95% скорочення контексту
- У 20 разів більше викликів інструментів до досягнення лімітів
- Агресивне стиснення + розумне підсумовування

⚠️ **Примітка**: бета-функція, у продакшені використовуйте обережно.

---

### Експорт/імпорт

**Експорт історії сесій**:

```bash
# Via dashboard
http://localhost:37777/export

# Via CLI
curl http://localhost:37777/api/export > claude-mem-backup.json
```

**Імпорт на іншій машині**:

```bash
# Via dashboard
http://localhost:37777/import

# Via CLI
curl -X POST http://localhost:37777/api/import \
  -H "Content-Type: application/json" \
  -d @claude-mem-backup.json
```

---

## Міркування щодо вартості

### Вартість API-стиснення

| Рівень використання | Сесій/місяць | Спостережень | Орієнт. вартість (Claude Haiku) | Орієнт. вартість (Gemini Lite) |
|-------------|----------------|--------------|--------------------------|-------------------------|
| **Легкий** | 10-20 | 200-400 | $0.30-0.60 | ~$0.05 |
| **Середній** | 50-80 | 1000-1600 | $1.50-2.40 | ~$0.20 |
| **Інтенсивний** | 100-150 | 2000-3000 | $3.00-4.50 | ~$0.45 |
| **Дуже інтенсивний** | ~400 сесій | ~8000 | ~$102 | ~$14 |

**Формула**: ~$0.15 за 100 спостережень (Claude Haiku) проти ~$0.02 (Gemini 2.5 Flash Lite)

**Перейдіть на Gemini, щоб знизити вартість на 86%**:

```json
// ~/.claude-mem/settings.json
{
  "provider": "gemini",
  "model": "gemini-2.5-flash-lite",
  "auth_method": "cli"
}
```

> **Компроміс Flash і Flash Lite**: Gemini 2.5 Flash Lite коштує менше, але генерує слабші підсумки. Для більшості проєктів це прийнятно. Для складних довготривалих проєктів, де важлива точність впровадженого контексту, розгляньте Gemini 2.5 Flash (не Lite).

**Подальше зниження витрат (пакетна обробка)**:

```json
{
  "compression": {
    "batchSize": 50,
    "interval": "hourly"
  }
}
```

Пакетне стиснення (щогодини) зменшує кількість викликів API порівняно зі стисненням кожного спостереження окремо.

---

### Вартість сховища

**Локальне сховище** (SQLite + Chroma):

| Рівень використання | Сховище |
|-------------|---------|
| **Легкий** (10 сесій/тиждень) | 10-20 MB/місяць |
| **Середній** (50 сесій/тиждень) | 50-100 MB/місяць |
| **Інтенсивний** (100 сесій/тиждень) | 100-200 MB/місяць |

**Стратегії очищення**:

```json
{
  "storage": {
    "retentionDays": 90,
    "autoCleanup": true
  }
}
```

---

## Усунення несправностей

### Панель не завантажується

```bash
# Check if worker is running
curl http://localhost:37777/health
# Expected: {"status":"ok"}

# Restart worker
claude-mem restart

# Check logs
tail -f ~/.claude-mem/logs/worker.log
```

---

### Високі витрати на API

```bash
# Check observation count
curl http://localhost:37777/api/stats
# Returns: {"observations": 5234, "sessions": 123}

# If too many observations:
# 1. Enable batching
# 2. Increase compression interval
# 3. Lower retention days
```

---

### Пам'ять не впроваджується

```bash
# Verify indexation
curl http://localhost:37777/api/index/status
# Expected: {"indexed": true, "observations": 1234}

# Manually trigger re-indexation
curl -X POST http://localhost:37777/api/index/rebuild
```

---

### Пошкодження бази даних

```bash
# Backup first
cp ~/.claude-mem/claude-mem.db ~/.claude-mem/claude-mem.db.backup

# Rebuild index
claude-mem index rebuild

# If still broken, reset (⚠️ loses all data)
rm -rf ~/.claude-mem/
claude-mem init
```

---

## Ліцензійні міркування

### AGPL-3.0

**Що це означає**:

- ✅ Безкоштовно для особистого використання
- ✅ Безкоштовно для open-source проєктів
- ⚠️ Використання через мережу = потрібно розкрити вихідний код
- ⚠️ Модифікації = потрібно розкрити вихідний код
- ❌ Не можна використовувати в закритому SaaS без дотримання вимог

**Комерційне використання**:

Якщо використовуєте в комерційному продукті:
1. Ознайомтеся з вимогами AGPL-3.0
2. Подбайте про юридичну відповідність
3. Альтернатива: зверніться до автора щодо комерційної ліцензії

**PolyForm Noncommercial** (каталог ragtime/):
- Окрема ліцензія для певних компонентів
- Суворіші комерційні обмеження

---

## Коли використовувати claude-mem

### ✅ Використовуйте, коли:

- Проєкти з багатьма сесіями (>1 тижня)
- Потрібно пам'ятати рішення протягом днів/тижнів
- Ви часто повертаєтеся до того самого проєкту
- Автоматична фіксація для вас цінніша за ручні нотатки
- Потрібна вебпанель для дослідження історії

### ❌ Не використовуйте, коли:

- Разові швидкі завдання (<10 хвилин)
- Надзвичайно чутливі дані (розгляньте натомість ручний Serena)
- Комерційні проєкти без перевірки відповідності AGPL
- Потрібна синхронізація між машинами (нативно не підтримується)
- Обмежений бюджет (<$5/місяць на API-стиснення)

---

## Порівняння з альтернативами

| Інструмент | Призначення | Фіксація | Запити |
|------|---------|---------|-------|
| **claude-mem** | Пам'ять сесій | Автоматично (hooks) | Природна мова |
| **Serena** | Пам'ять символів | Вручну (`write_memory`) | Пошук за ключем |
| **grepai** | Семантичний пошук | Н/д (лише пошук) | Семантичні |
| **CLAUDE.md** | Контекст проєкту | Вручну (запис файлу) | Claude читає на старті |

**Найкраще працюють разом**:
- claude-mem: автоматична фіксація сесій
- Serena: ручні архітектурні рішення
- grepai: пошук у коді
- CLAUDE.md: настанови проєкту

---

## Ресурси

**Офіційні**:
- [Репозиторій GitHub](https://github.com/thedotmack/claude-mem)
- [Документація](https://github.com/thedotmack/claude-mem/wiki)
- [Release Notes](https://github.com/thedotmack/claude-mem/releases)

**Посібники**:
- [Corti.com: Deep Dive](https://corti.com/claude-mem-persistent-memory-for-ai-coding-assistants/)
- [yuv.ai: Setup Guide](https://yuv.ai/blog/claude-mem)
- [YouTube: 5-Minute Setup](https://www.youtube.com/watch?v=ryqpGVWRQxA)

**Спільнота**:
- [GitHub Issues](https://github.com/thedotmack/claude-mem/issues)
- [GitHub Discussions](https://github.com/thedotmack/claude-mem/discussions)

---

**Версія шаблону**: 1.1.0
**Останнє оновлення**: 2026-03-30
**Версія посібника**: 3.38.1
