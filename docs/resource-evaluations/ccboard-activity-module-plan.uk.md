# Модуль активності ccboard: план реалізації

**Дата**: 2026-02-21
**Статус**: Чернетка
**Цільовий репозиторій**: [ccboard](https://github.com/FlorianBruniaux/ccboard)
**Приводом стало**: запитання користувача про моніторинг файлової, командної та мережевої активності Claude Code

---

## Контекст

Зараз ccboard охоплює керування сесіями, відстеження витрат і базову статистику. Бракує шару *аудиту активності*: які файли Claude Code читав, які команди виконував, які URL завантажував?

Ці дані вже є в JSONL-файлах сесій: кожен блок `tool_use` у повідомленнях `type: "assistant"` є повним записом дій Claude Code. Модуль Activity розбирає їх і показує в окремій вкладці Tab 10.

---

## Архітектура

### Нові файли

```
ccboard-core/
├── src/
│   ├── parsers/
│   │   └── activity.rs          # Parse tool_use blocks from JSONL
│   └── models/
│       └── activity.rs          # Structs: ToolCall, FileAccess, BashCommand, NetworkCall, Alert

ccboard-tui/
└── src/
    └── tabs/
        └── activity.rs          # Tab 10 — TUI rendering

ccboard-web/
└── src/
    └── pages/
        └── activity.rs          # /activity route — Web UI rendering
```

### Змінені файли

```
ccboard-core/src/db/schema.rs    # Add activity_events table
ccboard-core/src/db/queries.rs   # Add activity query functions
ccboard-tui/src/app.rs           # Register Tab 10
ccboard-web/src/router.rs        # Register /activity route
```

---

## Моделі даних

```rust
// ccboard-core/src/models/activity.rs

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ToolCall {
    pub id: String,
    pub session_id: String,
    pub timestamp: DateTime<Utc>,
    pub tool_name: String,
    pub input: serde_json::Value,
    pub duration_ms: Option<u64>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct FileAccess {
    pub session_id: String,
    pub timestamp: DateTime<Utc>,
    pub path: String,
    pub operation: FileOperation,   // Read | Write | Edit | Glob | Grep
    pub line_range: Option<(usize, usize)>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub enum FileOperation {
    Read,
    Write,
    Edit,
    Glob,
    Grep,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct BashCommand {
    pub session_id: String,
    pub timestamp: DateTime<Utc>,
    pub command: String,
    pub is_destructive: bool,       // Heuristic: rm -rf, git push --force, etc.
    pub output_preview: String,     // First 200 chars of output
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct NetworkCall {
    pub session_id: String,
    pub timestamp: DateTime<Utc>,
    pub url: String,
    pub tool: NetworkTool,          // WebFetch | WebSearch | McpCall
    pub domain: String,             // Extracted from URL
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub enum NetworkTool {
    WebFetch,
    WebSearch,
    McpCall { server: String },
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Alert {
    pub session_id: String,
    pub timestamp: DateTime<Utc>,
    pub severity: AlertSeverity,
    pub category: AlertCategory,
    pub detail: String,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub enum AlertSeverity {
    Info,
    Warning,
    Critical,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub enum AlertCategory {
    CredentialAccess,    // .env, *.pem, id_rsa
    DestructiveCommand,  // rm -rf, git push --force, DROP TABLE
    ExternalExfil,       // WebFetch to unknown domain
    ScopeViolation,      // Write outside project root
    ForcePush,           // git push --force
}
```

---

## Парсер

```rust
// ccboard-core/src/parsers/activity.rs

pub fn parse_tool_calls(session_jsonl: &Path) -> Result<Vec<ToolCall>> {
    // 1. Stream-read JSONL (don't load entire file)
    // 2. Filter lines where .type == "assistant"
    // 3. Extract .message.content[].type == "tool_use" blocks
    // 4. Map to ToolCall structs
    // 5. Return Vec<ToolCall>
}

pub fn classify_tool_calls(calls: Vec<ToolCall>) -> ActivitySummary {
    // Fan out into typed collections
    ActivitySummary {
        file_accesses: extract_file_accesses(&calls),
        bash_commands: extract_bash_commands(&calls),
        network_calls: extract_network_calls(&calls),
        alerts: generate_alerts(&calls),
    }
}

fn is_destructive_command(cmd: &str) -> bool {
    let patterns = [
        "rm -rf", "rm -r ", "git push --force", "git push -f",
        "DROP TABLE", "DROP DATABASE", "truncate ", "git reset --hard",
        "git clean -f", "pkill", "kill -9",
    ];
    patterns.iter().any(|p| cmd.to_lowercase().contains(p))
}

fn is_sensitive_file(path: &str) -> bool {
    let patterns = [".env", ".pem", "id_rsa", "id_ed25519", ".p12",
                    "secrets.json", "credentials.json", ".npmrc", ".netrc"];
    patterns.iter().any(|p| path.contains(p))
}
```

---

## Схема SQLite

```sql
-- Add to ccboard-core/src/db/schema.rs migrations

CREATE TABLE IF NOT EXISTS activity_events (
    id          TEXT PRIMARY KEY,
    session_id  TEXT NOT NULL,
    timestamp   TEXT NOT NULL,
    tool_name   TEXT NOT NULL,
    input_json  TEXT NOT NULL,      -- Full tool input as JSON
    duration_ms INTEGER,
    FOREIGN KEY (session_id) REFERENCES sessions(id)
);

CREATE INDEX IF NOT EXISTS idx_activity_session ON activity_events(session_id);
CREATE INDEX IF NOT EXISTS idx_activity_tool    ON activity_events(tool_name);
CREATE INDEX IF NOT EXISTS idx_activity_ts      ON activity_events(timestamp);

CREATE TABLE IF NOT EXISTS activity_alerts (
    id          TEXT PRIMARY KEY,
    session_id  TEXT NOT NULL,
    timestamp   TEXT NOT NULL,
    severity    TEXT NOT NULL,      -- 'info' | 'warning' | 'critical'
    category    TEXT NOT NULL,
    detail      TEXT NOT NULL,
    FOREIGN KEY (session_id) REFERENCES sessions(id)
);
```

---

## Вкладка TUI (вкладка 10)

### Макет

```
┌─ Activity ─────────────────────────────────────────────────────────┐
│ Session: my-project / 2026-02-21 14:32  [←][→] navigate sessions  │
├─────────────────────────────────────────────────────────────────────┤
│ [Files 47] [Commands 12] [Network 3] [Alerts ⚠ 2] [Timeline]      │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  FILES                                                               │
│  14:32:01  READ   src/main.rs                                       │
│  14:32:04  READ   src/lib.rs                                        │
│  14:32:09  EDIT   src/main.rs          ← lines 45-67               │
│  14:32:15  WRITE  src/new_module.rs                                 │
│  14:32:20  READ   ⚠ .env              ← credential access          │
│                                                                      │
│  [j/k scroll] [Enter: expand] [f: filter] [a: alerts only]         │
└─────────────────────────────────────────────────────────────────────┘
```

### Підвкладки в Activity

| Підвкладка | Клавіша | Вміст |
|---------|-----|---------|
| Files | `1` | Читання/запис/редагування файлів зі шляхом, часовою міткою, діапазоном рядків |
| Commands | `2` | Команди Bash, позначка деструктивності, попередній перегляд виводу |
| Network | `3` | URL у WebFetch, виклики MCP, список доменів |
| Alerts | `4` | Автоматично позначені події за рівнем серйозності |
| Timeline | `5` | Хронологічний перегляд усіх дій (об'єднано) |

### Сполучення клавіш

| Клавіша | Дія |
|-----|--------|
| `Tab` / `Shift+Tab` | Перемкнути підвкладки |
| `j` / `k` | Прокрутити список |
| `Enter` | Розгорнути елемент (повна команда / повний шлях / попередній перегляд відповіді) |
| `f` | Фільтр за шаблоном |
| `a` | Перейти до підвкладки Alerts |
| `s` | Перейти до вибору сесії |
| `/` | Пошук у поточному поданні |
| `y` | Скопіювати вибраний елемент у буфер обміну |
| `e` | Експортувати поточне подання в JSON |

---

## Сторінка вебінтерфейсу (/activity)

```
GET /activity                    → Session picker → redirect to /activity?session=ID
GET /activity?session=ID         → Full activity view for session
GET /activity?session=ID&tab=files
GET /activity?session=ID&tab=commands
GET /activity?session=ID&tab=network
GET /activity?session=ID&tab=alerts
GET /activity?session=ID&tab=timeline

GET /api/activity/:session_id              → Full ActivitySummary JSON
GET /api/activity/:session_id/files        → Vec<FileAccess>
GET /api/activity/:session_id/commands     → Vec<BashCommand>
GET /api/activity/:session_id/network      → Vec<NetworkCall>
GET /api/activity/:session_id/alerts       → Vec<Alert>
GET /api/activity/:session_id/timeline     → Vec<ToolCall> sorted by timestamp
```

---

## Правила виявлення сповіщень

| Правило | Умова | Серйозність |
|------|-----------|----------|
| Доступ до файлів з обліковими даними | Шлях у `Read` відповідає `*.env`, `*.pem`, `id_rsa`, `id_ed25519`, `secrets.json` | Warning |
| Деструктивна команда bash | Вхід `Bash` відповідає `rm -rf`, `git push --force`, `DROP TABLE`, `git reset --hard` | Critical |
| Force push | Вхід `Bash` містить `git push` із прапорцем `--force` або `-f` | Critical |
| Завантаження зовнішнього URL | Домен URL у `WebFetch` не входить до відомих доменів проєкту | Info |
| Запис поза коренем проєкту | Шлях у `Write`/`Edit` поза `$PWD` на початку сесії | Warning |
| Запис великого файлу | Розмір вмісту `Write` > 100KB | Info |
| Секрети у виводі bash | Попередній перегляд виводу `Bash` відповідає `sk-`, `ghp_`, `AKIA` (префікс ключа AWS) | Critical |

Сповіщення генеруються під час розбору й зберігаються в `activity_alerts`. Вони **не** блокують Claude Code: ccboard працює лише на читання.

---

## Обмеження продуктивності

### Вимоги

- Час запуску: < 2s для 1000+ сесій (та сама гарантія, що й у поточному ccboard)
- Розбір JSONL: лінивий, лише коли сесію вибрано, а не під час запуску
- Кеш SQLite: розбирати один раз, кешувати `activity_events` за session_id + mtime. Інвалідувати при зміні файлу.
- Пам'ять: читати JSONL потоково рядок за рядком, ніколи не завантажувати файл повністю

### Стратегія кешування

```
Session selected
    → Check SQLite: activity_events WHERE session_id = ? AND mtime = file_mtime
    → Cache hit: return from DB (< 10ms)
    → Cache miss: parse JSONL → insert to DB → return (< 500ms for typical session)
```

### Стратегія індексу

Індекс активності (кількість інструментів, кількість сповіщень) розбирати під час запуску разом із метаданими сесії: той самий шаблон лінивого індексу, що й для списку сесій. Повні подробиці лише на вимогу.

```
Startup:
    For each session: read first/last line only → session metadata
    Do NOT parse tool_use blocks

On session select:
    Check SQLite cache → parse if stale → display
```

---

## Фази реалізації

### Фаза 1: парсер + моделі (1-2 дні)

- [ ] Моделі `activity.rs`
- [ ] Парсер `activity.rs` (потокове читання JSONL, вилучення tool_use)
- [ ] Правила виявлення сповіщень
- [ ] Юніт-тести парсера на JSONL-фікстурах

### Фаза 2: інтеграція з SQLite (1 день)

- [ ] Міграція схеми
- [ ] Запити кешу (insert / select / invalidate)
- [ ] Бенчмарк: холодний старт на 1000 сесіях

### Фаза 3: вкладка TUI (2-3 дні)

- [ ] Реєстрація Tab 10 в `app.rs`
- [ ] Рендеринг підвкладки Files
- [ ] Рендеринг підвкладки Commands
- [ ] Рендеринг підвкладки Network
- [ ] Рендеринг підвкладки Alerts
- [ ] Рендеринг підвкладки Timeline
- [ ] Сполучення клавіш

### Фаза 4: вебінтерфейс (1-2 дні)

- [ ] Ендпоінти API
- [ ] Маршрутизація сторінки /activity
- [ ] HTML-рендеринг (у тому ж стилі, що й наявні сторінки)

### Фаза 5: доопрацювання (1 день)

- [ ] Експорт у JSON (клавіша `e` у TUI)
- [ ] Копіювання в буфер обміну (клавіша `y`)
- [ ] Фільтр (клавіша `f`)
- [ ] Оновлення документації в README ccboard

---

## Поза межами

- **Моніторинг у реальному часі** (стеження за живою сесією під час її роботи): майбутня фаза
- **Агрегація між сесіями** (наприклад, «усі файли, прочитані цього тижня»): майбутня фаза
- **Сповіщення про алерти** (сповіщення на робочому столі/у Slack): майбутня фаза
- **Блокувальні правила** (ccboard лишається лише для читання, жодної взаємодії з процесом Claude Code)

---

## Пов'язане

- `guide/ops/observability.md`: розділи "Activity Monitoring" і "External Monitoring Tools"
- `guide/security/data-privacy.md`: що залишає вашу машину і чому
- README ccboard: архітектура і посібник для контриб'юторів
