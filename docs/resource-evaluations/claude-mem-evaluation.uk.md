# Оцінка ресурсу: claude-mem

**Ресурс**: thedotmack/claude-mem - Persistent Memory for Claude Code
**URL**: https://github.com/thedotmack/claude-mem
**Тип**: Plugin / MCP-сервер
**Оцінено**: 2026-02-10
**Оцінювач**: Florian BRUNIAUX + Claude (Anthropic)

---

## Короткий підсумок

**Оцінка**: **4/5** (висока цінність, інтегрувати протягом 1 тижня)

Claude-mem це plugin для Claude Code, що дає **автоматичну пам'ять сесій** через стиснене ШІ фіксування використання інструментів, спостережень і рішень. Він закриває прогалину в посібнику: Serena (пам'ять символів) і grepai (семантичний пошук) задокументовані, а **автоматичне фіксування сесій** ні.

**Ключові показники** (оновлено 2026-03-30):
- 26.5k зірок на GitHub (станом на 2026-07-28 уже 88 747), 1.8k форків
- 46 контриб'юторів
- Остання версія: v10.6.3 (на момент першої оцінки була v9.1.1)
- Ліцензія: AGPL-3.0 + PolyForm Noncommercial

---

## Підсумок змісту

**Що робить claude-mem**:

1. **Автоматичне фіксування**: підключається до життєвого циклу Claude Code (SessionStart, PostToolUse, Stop, SessionEnd) і записує всі операції інструментів
2. **Стиснення ШІ**: використовує Claude для генерування семантичних підсумків спостережень (~10x менше token)
3. **Гібридний пошук**: повнотекстовий + векторний пошук (Chroma) + запити природною мовою
4. **Поступове розкриття**: 3-рівневе отримання (search → timeline → get_observations) заощаджує 95% token
5. **Вебпанель**: інтерфейс у реальному часі на `http://localhost:37777` для перегляду історії сесій
6. **Автоматична ін'єкція**: релевантний контекст автоматично підставляється на початку сесії

**Архітектура**:
```
Lifecycle Hooks → Observation capture → AI compression (Claude)
                                             ↓
                                    SQLite storage
                                             ↓
                              Chroma vector indexation
                                             ↓
                              Session start injection
```

**Заявлена продуктивність** (зі статей, незалежно не перевірено):
- Поступове розкриття: у 10x менше token
- Endless Mode (бета): скорочення контексту на 95% → у 20x більше викликів інструментів до лімітів
- Вартість: ~$0.15 за 100 оброблених спостережень

---

## Оцінка релевантності: 4/5

### Чому 4/5 (висока цінність)?

**✅ Сильні сторони**:

1. **Виявлено прогалину**: посібник документує Serena (пам'ять символів, вручну) і grepai (семантичний пошук), але **не автоматичне фіксування сесій**
2. **Масове поширення**: 26.5k зірок, 181 реліз, 46 активних контриб'юторів
3. **Готовий до продакшену**: ліцензія AGPL-3.0, стабільний API, активна підтримка
4. **Доповнює**: не замінює наявні інструменти, а підсилює їх
5. **Економія token**: шаблон поступового розкриття цінний для керування контекстом

**⚠️ Чому не 5/5?**:

1. **Шаблон частково охоплено**: Serena `write_memory()` існує для ручної пам'яті, тож прогалина стосується «автоматичності», а не «пам'яті»
2. **Обмеження AGPL-3.0**: обмеження комерційного використання, вимоги розкривати вихідний код
3. **Приховані витрати**: $0.15/100 спостережень не задокументовано в офіційному README
4. **Лише CLI**: немає вебінтерфейсу, хмарної синхронізації, підтримки кількох машин
5. **Нішевий сценарій**: корисний користувачам із >10 сесіями на тиждень, менш цінний для епізодичних користувачів

### Порівняння з наявним охопленням

| Аспект | Цей ресурс (claude-mem) | Наш посібник (v3.23.4) |
|--------|----------------------------|---------------------|
| **Автоматичне фіксування сесій** | ✅ Ключова функція | ❌ **Відсутнє** |
| **Відстеження використання інструментів** | ✅ На основі hooks | ➕ Задокументовано (архітектура hooks), але без конкретного інструмента |
| **Поступове розкриття** | ✅ 3-рівневий воркфлоу | ❌ Шаблон не задокументовано |
| **Пам'ять між сесіями** | ✅ Автоматична ін'єкція | ➕ Частково (Serena вручну, не автоматично) |
| **Вебпанель** | ✅ Інтерфейс у реальному часі | ❌ Відсутня |
| **Шаблони економії token** | ✅ Скорочення на 95% | ➕ Задокументовано (керування контекстом), але не такого масштабу |
| **Наслідки ліцензії AGPL** | ⚠️ Обмеження | ❌ **Відсутнє** (ліцензійні міркування) |
| **Вартість**: стиснення через API | ⚠️ $0.15/100 спостережень | ❌ **Відсутнє** (приховані витрати) |
| **Обмеження платформи** | ⚠️ Лише CLI | ❌ **Відсутнє** |

**Підсумок**: Посібник охоплює будівельні блоки (hooks, MCP, Serena), але **бракує інтегрованого рішення**, яке дає claude-mem. Прогалина помірна (не критична), бо шаблони існують, але автоматичне фіксування додає суттєвої цінності.

---

## Рекомендації щодо інтеграції

### Де документувати

**Рекомендовано**: **Розділ 8.2.5** (після grepai) у `guide/ultimate-guide.md`, ~рядок 8463

**Структура**:

```markdown
## 8.2.5 claude-mem (Automatic Session Capture)

### Architecture & Features
- Lifecycle hooks integration
- AI compression workflow
- Progressive disclosure pattern
- Web dashboard overview

### Installation & Setup
- Plugin marketplace installation
- Configuration options
- Privacy controls (<private> tags)

### Usage Patterns
- Automatic injection workflow
- Natural language queries
- Web UI navigation

### Cost & Privacy Considerations
- API compression costs ($0.15/100 obs)
- AGPL-3.0 licensing implications
- Data locality (SQLite + Chroma)
- Privacy tags for sensitive content

### Decision Matrix: vs Serena vs grepai
| Need | Tool | Rationale |
|------|------|-----------|
| Auto capture tool usage | claude-mem | Zero manual effort |
| Symbol-aware navigation | Serena | Precise editing |
| Semantic discovery | grepai | Intent-based search |
| Manual decision storage | Serena | Explicit control |

### Hybrid Workflows
- claude-mem + Serena (auto capture + manual decisions)
- claude-mem + grepai (session history + semantic search)
- Complete stack: rg → grepai → Serena → claude-mem
```

**Обсяг**: 300-400 рядків (а не 800, як пропонувалося спочатку)

### Файли для створення/зміни

1. **guide/ultimate-guide.md**
   - Додати розділ 8.2.5 (~300 рядків)
   - Оновити розділ 2.2 (Session vs Persistent Memory) посиланням на claude-mem

2. **machine-readable/reference.yaml**
   ```yaml
   claude_mem: "guide/ultimate-guide.md:8463"
   claude_mem_architecture: "guide/ultimate-guide.md:8470"
   claude_mem_progressive_disclosure: "guide/ultimate-guide.md:8520"
   claude_mem_dashboard: "guide/ultimate-guide.md:8550"
   claude_mem_vs_serena: "guide/ultimate-guide.md:8600"
   claude_mem_installation: "/plugin marketplace add thedotmack/claude-mem"
   claude_mem_repo: "https://github.com/thedotmack/claude-mem"
   claude_mem_stars: "26.5k"
   claude_mem_license: "AGPL-3.0"
   claude_mem_score: "4/5"
   ```

3. **examples/plugins/claude-mem.md** (шаблон встановлення)

4. **CHANGELOG.md**
   ```markdown
   ## [3.24.0] - 2026-02-XX

   ### Added
   - **Section 8.2.5**: claude-mem plugin documentation
   - Memory Stack Patterns (claude-mem + Serena + grepai integration)
   - Decision matrix for memory tools
   ```

### Пріоритет

**Висока цінність**: інтегрувати протягом **1 тижня**

**Обґрунтування**:
- Закриває справжню прогалину (автоматичне фіксування не задокументовано)
- Масове поширення в спільноті (26.5k зірок)
- Доповнює наявні інструменти
- АЛЕ не «Критично» (5/5), бо шаблони частково існують

---

## Технічний аналіз: claude-mem vs Serena vs grepai

### Порівняння архітектури

| Аспект | claude-mem | Serena | grepai |
|--------|-----------|---------|--------|
| **Призначення** | Фіксування сесій | Пам'ять символів | Семантичний пошук |
| **Тригер** | Автоматично (hooks) | Ручний API | Ручний CLI |
| **Сховище** | SQLite + Chroma | `.serena/memories/` | Вектори Ollama |
| **Технологія** | Стиснення ШІ | Сховище ключ-значення | Ембединги |
| **Індексація** | Події сесій | Символи проєкту | Файли коду |
| **Запит** | Природна мова | Пошук за ключем | Семантичний пошук |
| **Панель** | ✅ Вебінтерфейс | ❌ Ні | ❌ Ні |
| **Вартість** | $0.15/100 спостережень | Безкоштовно (локально) | Безкоштовно (локально) |
| **Приватність** | ✅ Локально | ✅ Локально | ✅ Локально |

### Матриця сценаріїв

| Потреба | Інструмент | Приклад |
|------|------|---------|
| «Що ми робили вчора?» | claude-mem | Автоматична ін'єкція попереднього контексту |
| «Знайти функцію login» | Serena | `find_symbol --name "login"` |
| «Хто викликає цю функцію?» | grepai | `grepai trace callers "login"` |
| «Записати архітектурне рішення» | Serena | `write_memory("auth", "JWT")` |
| «Знайти код, що робить X» | grepai | `grepai search "payment validation"` |
| «Підсумок усіх сесій» | claude-mem | Вебпанель + пошук |
| «Точний шаблон 'authenticate'» | rg (нативно) | `rg "authenticate" --type ts` |

### Шаблон стека пам'яті (запропонований)

```
┌─────────────────────────────────────────────────────────┐
│           Memory Stack (4 layers)                       │
├─────────────────────────────────────────────────────────┤
│ Layer 4: Session Capture   → claude-mem (automatic)    │
│ Layer 3: Symbol Memory     → Serena (manual decisions) │
│ Layer 2: Semantic Search   → grepai (discovery)        │
│ Layer 1: Exact Search      → rg (native, fast)         │
└─────────────────────────────────────────────────────────┘
```

**Приклад інтегрованого воркфлоу**:

```bash
# Scenario: Refactoring auth module after 3 days

# 1. AUTO CONTEXT (claude-mem)
# At session start, Claude injects:
# "3 previous sessions explored auth module.
#  Decision: Migrate to JWT.
#  Files modified: auth.service.ts, session.middleware.ts"

# 2. ARCH DECISIONS (Serena)
serena list_memories
# → "auth_decision: Use JWT for stateless API (2026-02-07)"

serena read_memory("auth_decision")

# 3. SEMANTIC DISCOVERY (grepai)
grepai search "JWT token validation"
# → Finds validateJWT() in auth.service.ts

# 4. DEPENDENCIES (grepai trace)
grepai trace callers "validateJWT"
# → Called by: ApiGateway, AdminPanel, UserController

# 5. EXACT SEARCH (rg)
rg "validateJWT" --type ts -A 5
```

**Результат**: повний контекст без повторного читання всіх файлів, безпечний рефакторинг.

---

## Результати фактчекінгу

| Твердження | Джерело | Перевірено | Примітки |
|-------|--------|----------|-------|
| **26.5k зірок** | GitHub (WebFetch 2026-02-10) | ✅ | У Perplexity було 15.6k (застаріло) |
| **1.8k форків** | GitHub | ✅ | Підтверджено |
| **181 реліз** | GitHub | ✅ | У Perplexity було 174 (застаріло) |
| **46 контриб'юторів** | GitHub | ✅ | У Perplexity було 22 (застаріло) |
| **Ліцензія AGPL-3.0** | README на GitHub | ✅ | + PolyForm Noncommercial для ragtime/ |
| **Остання версія: v9.1.1 (7 лютого 2026)** | Релізи на GitHub | ✅ | Активно |
| **Ціль: Claude Code** | README на GitHub | ✅ | Основна (+ вторинна підтримка Desktop) |
| **Посібник не документує Serena** | grep по ultimate-guide.md | ❌ **ХИБНО** | Знайдено 10 входжень |
| **Посібник не документує grepai** | grep по ultimate-guide.md | ❌ **ХИБНО** | Знайдено 22 входження |
| **Поступове розкриття 10x** | Perplexity + статті | ⚠️ | Твердження підтверджено, але метрика приблизна |
| **$0.15/100 спостережень** | Зовнішні статті | ⚠️ | В офіційному README не знайдено |
| **95% у Endless Mode** | Статті | ⚠️ | Бета-твердження, незалежно не перевірено |

**Застосовані виправлення**:

1. **Виправлено аналіз прогалин**: посібник ТАКИ документує Serena (рядки 686, 762, 765, 770, 775, 779, 968, 1521, 1532) і grepai (22 згадки). Прогалина **не «немає документації про пам'ять»**, а **«немає рішення для автоматичного фіксування»**.

2. **Показники перевірено**: 26.5k зірок (дані Perplexity застарілі), 181 реліз, 46 контриб'юторів.

3. **Цільовий продукт**: Claude Code (основний), не плутати з Desktop.

4. **Надійність Perplexity**: виявлено застарілі дані → критичні показники завжди перевіряйте безпосередньо на GitHub.

---

## Обмеження та міркування

### Обмеження claude-mem

1. **Ліцензія AGPL-3.0**
   - Зміни вимагають розкриття вихідного коду
   - Мережеве розгортання вимагає AGPL
   - Обмеження комерційного використання

2. **Приховані витрати**
   - $0.15 за 100 спостережень (стиснення через API)
   - Не задокументовано в офіційному README
   - Можуть накопичуватися на великих проєктах

3. **Лише CLI**
   - Немає підтримки вебінтерфейсу
   - Немає хмарної синхронізації між машинами
   - Немає інтеграції з VS Code

4. **Ручні теги приватності**
   - Для чутливого вмісту потрібні теги `<private>`
   - Забули тег → чутливі дані в БД
   - Немає автоматичного виявлення секретів

### Перетини з наявними інструментами

Посібник уже документує:
- Пошук сесій (`guide/ops/observability.md:29`)
- Міграцію сесій (`guide/ops/observability.md:175`)
- Керування контекстом (`/compact`, `/clear`)

**Питання**: Чи дає claude-mem достатньо **додаткової цінності**, щоб виправдати 300-400 рядків?

**Відповідь**: Так, бо:
- ✅ **Автоматичне** фіксування (проти ручної Serena)
- ✅ Стиснення ШІ (проти сирих сесій)
- ✅ Вебпанель (проти лише CLI)
- ✅ Поступове розкриття (економія token)

---

## Результати виклику технічного письменника

**ID агента**: ac8e0c6

**Підсумок виклику**:

Агент technical-writer оскаржив початкову оцінку 5/5 і виявив:

1. **Хибна передумова**: «Посібник не документує Serena/grepai» → **ХИБНО** (обидва задокументовано)
2. **Суперечності в показниках**: 15.6k проти 26.5k зірок → знадобилася перевірка
3. **Плутанина з продуктом**: уточнено орієнтацію на Claude Code проти Claude Desktop
4. **Проблеми з обсягом**: 800 рядків завелико → скорочено до 300-400 рядків
5. **Терміновість під сумнівом**: <24h нереалістично → змінено на 1 тиждень

**Результат**: оцінку змінено з 5/5 → 4/5 на підставі:
- Прогалина реальна, але **помірна** (Serena/grepai існують, автоматичного фіксування бракує)
- AGPL-3.0 + приховані витрати + лише CLI = обмеження
- Допоміжний інструмент, а не критична інфраструктура

---

## Зовнішні ресурси

**Статті**:
- [Corti.com: Claude-Mem Deep Dive](https://corti.com/claude-mem-persistent-memory-for-ai-coding-assistants/) (2026-02-03)
- [yuv.ai: Persistent Memory Guide](https://yuv.ai/blog/claude-mem) (2026-02-05)
- [byteiota: Progressive Disclosure Analysis](https://byteiota.com/claude-mem-persistent-memory-for-claude-code/) (2026-02-04)

**Відео**:
- [YouTube: 5-Minute Setup Guide](https://www.youtube.com/watch?v=ryqpGVWRQxA) (2026-02-06)
- [YouTube: Unlimited Memory Demo](https://www.youtube.com/watch?v=qhuS__jC4n8) (2026-02-05)

**GitHub**:
- [thedotmack/claude-mem](https://github.com/thedotmack/claude-mem)
- [Release Notes v9.1.1](https://github.com/thedotmack/claude-mem/releases/tag/v9.1.1)

**Бенчмарки**:
- Станом на 2026-02-10 незалежних бенчмарків не знайдено
- Твердження зі статей: "95% context reduction, 20x tool calls" (не перевірено)
- Поступове розкриття: "10x token reduction" (правдоподібно з огляду на архітектуру)

---

## Рішення

**Оцінка**: **4/5** (висока цінність, інтегрувати протягом 1 тижня)

**Дія**:
1. Інтегрувати розділ 8.2.5 у `guide/ultimate-guide.md` (300-400 рядків)
2. Оновити `machine-readable/reference.yaml` записами про claude-mem
3. Створити шаблон plugin в `examples/plugins/claude-mem.md`
4. Додати до CHANGELOG.md v3.24.0

**Впевненість**: висока (показники перевірено, архітектуру зрозуміло, план інтеграції чіткий)

---

**Оцінено**: 2026-02-10
**Наступний перегляд**: перед інтеграцією v3.24.0
**Статус**: схвалено для інтеграції
