---
title: "Скрипти"
description: "Допоміжні скрипти для досвідчених користувачів Claude Code: аудити, перевірки стану й керування сесіями"
tags: [template, debugging, security, workflows]
---

# Скрипти

Допоміжні скрипти для досвідчених користувачів Claude Code.

## Огляд

| Скрипт | Опис |
|--------|-------------|
| `pptx-to-pdf.sh` | Пакетне перетворення PPTX у PDF через Keynote на macOS (без залежностей) |
| `audit-scan.sh` | Аудит безпеки та якості налаштування Claude Code |
| `check-claude.sh/.ps1` | Перевірка стану встановлення Claude Code |
| `clean-reinstall-claude.sh/.ps1` | Чисте перевстановлення Claude Code |
| `fresh-context-loop.sh` | Запуск Claude Code у циклах зі свіжим контекстом |
| `session-search.sh` | Пошук в історіях сесій Claude Code |
| `cc-sessions.py` | Розширений пошук сесій з інкрементною індексацією (Python) |
| `session-stats.sh` | Статистика сесій Claude Code |
| `bridge.py` | Міст: Claude Code → doobidoo → LM Studio |
| `bridge-plan-schema.json` | JSON Schema для формату плану bridge v1 |
| `migrate-arguments-syntax.sh` | Міграція синтаксису аргументів slash-команд v1 → v2 (bash) |
| `migrate-arguments-syntax.ps1` | Міграція синтаксису аргументів slash-команд v1 → v2 (PowerShell) |
| `rtk-benchmark.sh` | Бенчмарк економії токенів RTK порівняно з сирими командами |
| `sync-claude-config.sh` | Синхронізація конфігураційних файлів Claude між машинами |
| `sonnetplan.sh` | Запуск Claude із Sonnet замість Opus (аліас для оптимізації витрат) |
| `test-prompt-caching.ts` | Перевірка, чи активне prompt caching в Anthropic (без залежностей, лише fetch) |
| `smart-suggest-roi.py` | Аналіз частки прийнятих пропозицій hook smart-suggest порівняно з активністю в сесіях |
| `supply-chain-triage.py` | Тріаж робочої станції після інциденту в ланцюгу постачання npm (lock-файли, дропери в preinstall, хеші payload, hooks запуску, вартові відкликання, вихідний трафік) |

---

## Скрипт-міст (Claude Code → LM Studio)

**Призначення**: виконувати плани Claude Code локально через LM Studio, щоб заощадити кошти.

### Архітектура

```
┌──────────────┐     store_memory      ┌─────────────────┐
│ Claude Code  │ ─────────────────────►│    doobidoo     │
│   (Opus)     │   tag: "plan"         │   SQLite + Vec  │
│   PLANNER    │   status: "pending"   │ ~/.mcp-memory-  │
└──────────────┘                       │  service/       │
                                       └────────┬────────┘
                                                │
                                                │ Direct SQLite read
                                                ▼
                                       ┌─────────────────┐
                                       │   bridge.py     │
                                       │                 │
                                       │ • PlanReader    │
                                       │ • StepExecutor  │
                                       │ • Validator     │
                                       └────────┬────────┘
                                                │
                                                │ HTTP POST
                                                │ /v1/chat/completions
                                                ▼
                                       ┌─────────────────┐
                                       │    LM Studio    │
                                       │  localhost:1234 │
                                       └─────────────────┘
```

### Вимоги

```bash
pip install httpx
```

- **MCP-сервер doobidoo** із бекендом SQLite (`~/.mcp-memory-service/`)
- **LM Studio**, запущений на `localhost:1234` із завантаженою моделлю

### Використання

```bash
# Check LM Studio is running
python bridge.py --health

# List pending plans
python bridge.py --list

# Execute all pending plans
python bridge.py

# Execute specific plan
python bridge.py --plan plan_auth_refactor

# Verbose mode
python bridge.py -v
```

### Воркфлоу

#### 1. Claude Code створює план

У Claude Code (Opus) збережіть план через doobidoo:

```
store_memory("""
{
  "$schema": "bridge-plan-v1",
  "id": "plan_auth_refactor",
  "status": "pending",
  "context": {
    "project": "/path/to/project",
    "objective": "Refactor authentication to use JWT",
    "files_context": {
      "src/auth.py": "LOAD",
      "src/config.py": "REFERENCE"
    }
  },
  "steps": [
    {
      "id": 1,
      "type": "analysis",
      "description": "Analyze current auth implementation",
      "prompt": "Analyze the authentication code and identify migration points for JWT.",
      "validation": {"type": "non_empty"}
    },
    {
      "id": 2,
      "type": "code_generation",
      "description": "Generate JWT middleware",
      "prompt": "Generate a JWT authentication middleware based on the analysis.",
      "depends_on": [1],
      "validation": {"type": "syntax_check"},
      "file_output": "src/jwt_auth.py"
    }
  ]
}
""", tags=["plan"])
```

#### 2. Виконання через bridge

```bash
python bridge.py
# Reads plan from doobidoo SQLite
# Executes each step via LM Studio
# Stores results back in doobidoo
```

#### 3. Отримання результатів у Claude Code

```
search_by_tag(["result", "plan_auth_refactor"])
# Returns all execution results
```

### Схема плану

Повну JSON Schema дивіться в `bridge-plan-schema.json`.

| Поле | Обов'язкове | Опис |
|-------|----------|-------------|
| `$schema` | Так | Має бути `"bridge-plan-v1"` |
| `id` | Так | Унікальний ID плану (наприклад, `plan_auth_refactor`) |
| `status` | Так | `pending`, `in_progress`, `completed`, `failed` |
| `context.objective` | Так | Опис мети на високому рівні |
| `context.project` | Ні | Абсолютний шлях до кореня проєкту |
| `context.files_context` | Ні | Файли для впровадження (`LOAD`) або для посилання |
| `steps` | Так | Масив кроків виконання |

### Типи кроків

| Тип | Сценарій використання |
|------|----------|
| `analysis` | Аналіз коду, виявлення патернів, планування змін |
| `code_generation` | Генерація нового коду з нуля |
| `code_modification` | Зміна наявного коду |
| `decision` | Ухвалення архітектурних чи дизайнерських рішень |

### Типи валідації

| Тип | Опис |
|------|-------------|
| `non_empty` | Вивід не порожній (за замовчуванням) |
| `json` | Коректний JSON на виході |
| `syntax_check` | Коректний синтаксис Python |
| `contains_keys` | JSON містить певні ключі |

### Обробка збоїв

| on_failure | Поведінка |
|------------|----------|
| `retry_with_context` | Повторна спроба з відгуком про помилку (за замовчуванням) |
| `skip` | Пропустити крок, продовжити виконання |
| `halt` | Зупинити весь план |

### Економія коштів

- **Планування** (Opus): ~$0.50-2.00 за складний план
- **Виконання** (LM Studio): безкоштовно (локально)
- **ROI**: скорочення витрат на 80-90% для завдань реалізації

### Обмеження

| Обмеження | Пом'якшення |
|------------|------------|
| Якість локальних моделей різниться | Сувора валідація + повторні спроби |
| У LM Studio немає MCP-інструментів | Впроваджуйте вміст файлів у контекст |
| Обмежене context window | Обрізайте старі результати |
| Немає стримінгу | Тайм-аут 120s на крок |

---

## Аудит-сканування

Аудит безпеки та якості вашої конфігурації Claude Code.

```bash
./audit-scan.sh
```

Перевіряє:
- Чутливі дані у файлах CLAUDE.md
- Конфігурації дозволів
- Безпеку MCP-серверів
- Безпечність скриптів hooks

---

## Перевірка стану

Швидка перевірка встановлення Claude Code.

```bash
# macOS/Linux
./check-claude.sh

# Windows
./check-claude.ps1
```

---

## Чисте перевстановлення

Повне перевстановлення зі збереженням конфігурацій.

```bash
# macOS/Linux
./clean-reinstall-claude.sh

# Windows
./clean-reinstall-claude.ps1
```

---

## Цикл зі свіжим контекстом

Запуск Claude Code зі свіжим контекстом для довготривалих завдань.

```bash
./fresh-context-loop.sh --iterations 5 --project /path/to/project
```

---

## Пошук сесій

Пошук в усіх історіях сесій Claude Code.

```bash
./session-search.sh "authentication"
```

---

## Менеджер сесій (розширений)

Розширений CLI для пошуку, перегляду, відновлення сесій і виявлення патернів з інкрементною індексацією.

**Порівняно з session-search.sh**: швидший пошук (~200ms проти ~400ms), відновлення за частковим ID, фільтр за гілкою, підтримка worktree, інкрементний JSONL-індекс і підкоманда `discover` для автоматизованої оптимізації конфігурації.

**GitHub**: [FlorianBruniaux/cc-sessions](https://github.com/FlorianBruniaux/cc-sessions)

```bash
# Search in current project
cc-sessions search "notion"

# Search all projects
cc-sessions --all search "stripe"

# Filter by date and branch
cc-sessions search "auth" --since 7d --branch develop

# Recent sessions
cc-sessions recent 10

# Resume with partial ID
cc-sessions resume 8d472d

# JSON output for scripting
cc-sessions --json search "prisma" | jq -r '.[].id'

# Discover recurring patterns (n-gram, local, free)
cc-sessions --all discover

# Discover with semantic analysis via claude --print
cc-sessions --all discover --llm

# JSON output for scripting
cc-sessions --all discover --json | jq '.[] | select(.category == "skill")'
```

**Встановлення з GitHub**:
```bash
curl -sL https://raw.githubusercontent.com/FlorianBruniaux/cc-sessions/main/cc-sessions \
  -o ~/.local/bin/cc-sessions && chmod +x ~/.local/bin/cc-sessions
```

**Або скопіюйте локально**: `cp cc-sessions.py ~/bin/cc-sessions && chmod +x ~/bin/cc-sessions`

> [Репозиторій GitHub](https://github.com/FlorianBruniaux/cc-sessions) · [Gist](https://gist.github.com/FlorianBruniaux/992d4d1107592d9e98ca9d89838871c6)

---

## Статистика сесій

Отримайте статистику використання Claude Code.

```bash
./session-stats.sh
```

---

## PPTX у PDF (macOS)

Пакетне перетворення презентацій PPTX у PDF за допомогою Keynote. Без LibreOffice, без Python — лише macOS + Keynote.

```bash
# Convert all PPTX in a folder (recursive)
./pptx-to-pdf.sh ~/Downloads/Prose

# Convert current directory
./pptx-to-pdf.sh
```

**Вимоги**: macOS + встановлений Keynote.

**Поведінка**:
- Рекурсивно: знаходить усі файли `.pptx` у підкаталогах
- Ідемпотентно: пропускає файли, для яких `.pdf` уже існує
- Результат: PDF створюється поруч із кожним PPTX, у тій самій папці, з тією самою назвою
- Наприкінці друкується підсумок

**Головна пастка**: скрипт відкриває файли через `open -a "Keynote"` з оболонки, а не власною командою `open` в AppleScript. Коли Keynote відкриває PPTX через AppleScript, він іноді не реєструє документ у своєму внутрішньому списку, що спричиняє помилку -1719 на `document 1`. Патерн «open з оболонки + пауза 8 секунд» надійно це виправляє.
