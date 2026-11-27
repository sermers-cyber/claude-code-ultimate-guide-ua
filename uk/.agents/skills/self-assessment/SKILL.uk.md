---
name: self-assessment
version: 1.0.0
description: Інтерактивне оцінювання навичок із генерацією персоналізованого шляху навчання
trigger: /self-assessment
invocation: manual

profiles:
  - name: junior
    label: "Beginner"
    min_score: 0
    max_score: 6
  - name: intermediate
    label: "Intermediate"
    min_score: 7
    max_score: 13
  - name: advanced
    label: "Advanced"
    min_score: 14
    max_score: 20

topics:
  - id: 01
    name: "Quick Start"
    guide_section: "guide/ultimate-guide.md#1-quick-start-day-1"
    importance: "critical"
    depends_on: []
    
  - id: 02
    name: "Core Concepts"
    guide_section: "guide/ultimate-guide.md#2-core-concepts"
    importance: "critical"
    depends_on: [01]
    
  - id: 03
    name: "Memory & Settings"
    guide_section: "guide/ultimate-guide.md#3-memory--settings"
    importance: "high"
    depends_on: [02]
    
  - id: 04
    name: "Agents"
    guide_section: "guide/ultimate-guide.md#4-agents"
    importance: "high"
    depends_on: [02, 03]
    
  - id: 05
    name: "Skills"
    guide_section: "guide/ultimate-guide.md#5-skills"
    importance: "high"
    depends_on: [02, 03]
    
  - id: 06
    name: "Commands"
    guide_section: "guide/ultimate-guide.md#6-commands-user-invocable-skills"
    importance: "medium"
    depends_on: [02]
    
  - id: 07
    name: "Hooks"
    guide_section: "guide/ultimate-guide.md#7-hooks"
    importance: "medium"
    depends_on: [02, 03]
    
  - id: 08
    name: "MCP Servers"
    guide_section: "guide/ultimate-guide.md#8-mcp-servers"
    importance: "medium"
    depends_on: [02]
    
  - id: 09
    name: "Advanced Patterns"
    guide_section: "guide/ultimate-guide.md#9-advanced-patterns"
    importance: "low"
    depends_on: [04, 05, 06, 07, 08]
    
  - id: 10
    name: "Security & Production"
    guide_section: "guide/security/"
    importance: "critical"
    depends_on: [02, 03]

modes:
  - id: quick
    name: "Quick Assessment"
    duration: "5 minutes"
    questions_per_topic: 1
    total_questions: 10
    description: "Rapid assessment across core topics. Get a skill level + identify 2-3 immediate gaps."
    
  - id: comprehensive
    name: "Comprehensive Assessment"
    duration: "20 minutes"
    questions_per_topic: 2
    total_questions: 20
    description: "Deep dive into each topic. Get per-topic scores + detailed learning path + practice projects."
---

# Codex Self-Assessment

**Опануйте навички Codex завдяки персоналізованому навчальному шляху.**

Це інтерактивне оцінювання визначає ваш поточний рівень експертизи та створює власний шлях навчання, підлаштований під ваші прогалини та цілі.

---

## Як це працює

### Крок 1: Оберіть режим

**Режим Quick** (5 хв)
- 10 питань за 10 темами
- Найкраще для: швидкої перевірки навичок, розуміння свого загального рівня
- Результат: загальний профіль (Beginner/Intermediate/Advanced) + 2-3 головні прогалини

**Режим Comprehensive** (20 хв)
- 20 питань (по 2 на тему)
- Найкраще для: детального оцінювання рівня володіння, планування навчання команди
- Результат: бали за темами + детальний шлях навчання + 3 практичні проєкти

### Крок 2: Відповідайте на питання

Питання охоплюють:
- Практичне використання (як щось робити)
- Прийняття рішень (коли що використовувати)
- Архітектурні шаблони (чому речі працюють)
- Найкращі практики продакшену (безпека, продуктивність, масштабування)

Кожне питання має:
- 4 варіанти (A-D)
- Негайний відгук щодо правильної відповіді
- Посилання на відповідний розділ посібника

### Крок 3: Отримайте профіль

**Результат режиму Quick:**
```
╔═══════════════════════════════════════════════╗
║ Your Profile: Intermediate Developer          ║
╠═══════════════════════════════════════════════╣
║ Overall Score: 14/20                          ║
║ Level: Intermediate (strong)                  ║
╠═══════════════════════════════════════════════╣
║ Immediate Gaps:                               ║
║  • MCP Servers (5/5 topics weak)              ║
║  • Advanced Patterns (4/5 weak)               ║
║  • Hooks (3/5 partially weak)                 ║
║                                               ║
║ → Recommended learning time: 4-6 hours        ║
╚═══════════════════════════════════════════════╝
```

**Результат режиму Comprehensive:**
```
╔═══════════════════════════════════════════════════════════════╗
║ Detailed Mastery Profile                                      ║
╠═══════════════════════════════════════════════════════════════╣
║                                                               ║
║ 01 Quick Start          ████░░░░░░  8/10  Proficient         ║
║ 02 Core Concepts        ██████░░░░  6/10  Proficient         ║
║ 03 Memory & Settings    ██████░░░░  6/10  Proficient         ║
║ 04 Agents              ████░░░░░░  4/10  Basic               ║
║ 05 Skills              ████░░░░░░  4/10  Basic               ║
║ 06 Commands            ██████░░░░  6/10  Proficient          ║
║ 07 Hooks               ██░░░░░░░░  2/10  None                ║
║ 08 MCP Servers         ██░░░░░░░░  2/10  None                ║
║ 09 Advanced Patterns   ░░░░░░░░░░  0/10  None                ║
║ 10 Security            ███░░░░░░░  3/10  Basic               ║
║                                                               ║
║ OVERALL: Intermediate (14/100 points)                         ║
╚═══════════════════════════════════════════════════════════════╝
```

### Крок 4: Отримайте шлях навчання

На основі ваших балів ви отримуєте:

**Пріоритезовану послідовність навчання** (з урахуванням залежностей):
1. Теми впорядковані за слабкістю + важливістю
2. Показані передумови (основи пропустити не можна)
3. Оцінки часу для кожної теми (сумуються лише потрібні вам)
4. Шаблони та приклади, прив'язані до кожної теми

**Приклад шляху для розробника середнього рівня:**
```
Phase 1: Hooks Fundamentals (2 hours)
  → Read: guide/ultimate-guide.md#7-hooks
  → Try: examples/hooks/event-driven-formatting.sh
  → Quiz: /lesson-quiz 07-hooks

Phase 2: MCP Integration (3 hours)
  → Read: guide/ultimate-guide.md#8-mcp-servers
  → Try: examples/mcp-configs/github-integration.json
  → Quiz: /lesson-quiz 08-mcp-servers

Phase 3: Advanced Patterns (4 hours)
  → Read: guide/ultimate-guide.md#9-advanced-patterns
  → Practice: 3 real-world projects (see below)
  → Quiz: /lesson-quiz 09-advanced-patterns
```

**3 практичні проєкти**
На основі вашого профілю ви отримуєте цільові вправи:
- Проєкт 1: Поєднайте 2-3 теми, у яких ви слабкі
- Проєкт 2: Інтеграція реального воркфлоу
- Проєкт 3: Сценарій для команди/продакшену

---

## Початок роботи

### Швидке оцінювання
```
/self-assessment quick
```

### Повне оцінювання
```
/self-assessment comprehensive
```

### Опції
```
/self-assessment quick --verbose      # Show explanations
/self-assessment comprehensive --save  # Save results to file
```

---

## Чого ви навчитеся

Це оцінювання призначене для виявлення:

### Фундаментальні прогалини
- Основні цикли взаємодії, які ви не пробували
- Важливі можливості, які ви пропустили
- Хибні уявлення в ментальній моделі

### Сліпі зони у прийнятті рішень
- Коли використовувати agents, а коли skills чи commands
- Яку подію hook обрати для якої проблеми
- Вибір MCP-сервера під ваші потреби

### Готовність до продакшену
- Найкращі практики безпеки
- Шаблони оптимізації продуктивності
- Масштабування мультиагентних систем
- Конфігурація команди та управління

---

## Після оцінювання

### Негайні дії
1. **Перегляньте свій профіль** — зрозумійте свій поточний рівень володіння
2. **Визначте прогалини** — точно знайте, що вивчати далі
3. **Отримайте шлях навчання** — персоналізована послідовність з урахуванням залежностей
4. **Практикуйтеся** — 3 цільові проєкти, що відповідають вашому рівню

### Рекомендовані подальші skills
- `/lesson-quiz [topic]` — перевірте себе з окремих тем
- `/audit-agents-skills` — проаудитуйте якість власної конфігурації
- `/Codex-md` — керуйте конфігурацією AGENTS.md

### Інтеграція зі шляхом навчання

Після оцінювання skill `/lesson-quiz` забезпечує перевірку за модулями:
- Відповідайте на 5 питань за модуль
- Отримуйте миттєвий відгук щодо слабких місць
- Розблоковуйте наступний модуль, коли будете готові

---

## Бали та профілі

### Junior Developer (0-6 балів)
- Щойно встановили Codex
- Знають базові команди та воркфлоу
- Ще не торкалися пам'яті/agents/hooks
- **Наступний крок:** Core Concepts + модуль Memory

### Intermediate Developer (7-13 балів)
- Користуються Codex щодня
- Комфортно почуваються з AGENTS.md і базовими agents
- Досліджують skills і commands
- Трохи використовують hooks, без MCP-серверів
- **Наступний крок:** Поглиблено MCP + Advanced Patterns

### Advanced Developer (14-20 балів)
- Опанували оркестрацію кількох агентів
- Безпека та масштабування продакшен-рівня
- Власні skills і складні hooks
- Експертиза з MCP-серверів
- **Наступний крок:** Навчання команди, корпоративні шаблони

---

## Поради для кращих результатів

1. **Відповідайте чесно** — не вгадуйте, пропускайте невідомі питання
2. **Переглядайте пояснення** — кожне питання має посилання на посібник
3. **Повертайтеся перед підвищенням рівня** — проходьте оцінювання повторно після вивчення нових тем
4. **Діліться результатами** — використовуйте свій профіль для координації з командою

---

## Потрібна допомога?

- **Питання щодо оцінювання?** → Дивіться `/help self-assessment`
- **Хочете обговорити результати?** → Дивіться `guide/roles/learning-with-ai.md`
- **Знайшли помилку?** → Повідомте про неї в GitHub Issues

---

**Готові опанувати Codex?** Почніть із `/self-assessment quick` просто зараз.
