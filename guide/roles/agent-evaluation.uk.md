---
title: "Agent Evaluation"
description: "Метрики, патерни та інструменти для вимірювання ефективності кастомних агентів"
tags: [agents, testing, guide]
---

# Agent Evaluation

**Швидка навігація**: [Навіщо оцінювати агентів?](#навіщо-оцінювати-агентів) · [Метрики для відстеження](#метрики-для-відстеження) · [Шаблони впровадження](#шаблони-впровадження) · [Приклад: Агент з оцінкою](#приклад-агент-з-оцінкою) · [Інструменти та корисні посилання](#інструменти-та-корисні-посилання)

---

## Навіщо оцінювати агентів?

Коли ви створюєте кастомних агентів у директорії `.claude/agents/`, ви кодуєте спеціалізовану експертизу в багаторазово використовувані воркфлоу (робочі процеси). Але як дізнатися, чи ваші агенти насправді є ефективними?

**Без оцінки** ви будуєте наосліп:
- ❌ Немає можливості виміряти, чи покращуються чи погіршуються відповіді агента з часом
- ❌ Неможливо об'єктивно порівняти різні конфігурації агентів
- ❌ Складно визначити, які саме аспекти контексту або інструкцій агента потребують вдосконалення
- ❌ Відсутні дані для обґрунтування інвестицій у розробку агентів

**З оцінкою** ви ітеруєте впевнено:
- ✅ Кількісно оцінюєте якість роботи агента за допомогою метрик (час відповіді, точність, використання інструментів)
- ✅ Проводите A/B тестування різних конфігурацій агентів із вимірюваними результатами
- ✅ Виявляєте патерни в успішних взаємодіях порівняно з невдалими
- ✅ Створюєте цикли зворотного зв'язку для безперервного вдосконалення

**Основний принцип**: Агенти — це код. Як і будь-який інший код, вони потребують тестів, метрик та спостережуваності (observability).

---

## Метрики для відстеження

### 1. Метрики якості відповідей (Response Quality Metrics)

**Що вимірювати**:
- **Task completion rate** (показник виконання завдань): Чи досяг агент поставленої мети?
- **Correctness** (правильність): Чи були результати роботи агента фактично точними?
- **Relevance** (відповідність): Чи залишалася відповідь у межах теми і чи вирішувала вона безпосередньо поставлене питання?
- **Hallucination rate** (рівень галюцинацій): Як часто агент вигадував інформацію?

**Як відстежувати**:
```bash
# Post-response hook: .claude/hooks/log-response-quality.sh
# Triggered after each agent response

# Log structure:
{
  "timestamp": "2026-02-10T14:32:00Z",
  "agent_id": "backend-architect",
  "task_completed": true,
  "correctness_score": 4.5,  # User rating 1-5
  "hallucinations": 0,
  "response_tokens": 1250
}
```

**Порада щодо впровадження**: Використовуйте запити для зворотного зв'язку з користувачем (пальці вгору/вниз) або автоматизовані перевірки (успішне проходження тестів після генерації коду агентом).

---

### 2. Метрики використання інструментів (Tool Usage Metrics)

**Що вимірювати**:
- **Tool call success rate** (успішність викликів інструментів): Відсоток викликів інструментів, які були виконані без помилок.
- **Tool selection accuracy** (точність вибору інструментів): Чи вибрав агент правильний інструмент для конкретного завдання?
- **Tool call efficiency** (ефективність викликів інструментів): Мінімальна кількість викликів для досягнення мети (уникнення непотрібних читань/пошуків).
- **Error recovery** (відновлення після помилок): Чи обробив агент збої інструментів належним чином?

**Як відстежувати**:
```bash
# Post-tool-use hook: .claude/hooks/log-tool-usage.sh
# Triggered after each tool call

# Log structure:
{
  "timestamp": "2026-02-10T14:32:05Z",
  "agent_id": "backend-architect",
  "tool_name": "Read",
  "tool_success": true,
  "tool_parameters": {"file_path": "src/auth.ts"},
  "execution_time_ms": 45
}
```

**Порада щодо впровадження**: Використовуйте систему хуків (hooks) Claude Code (див. `examples/hooks/`) для автоматичного логування викликів інструментів.

---

### 3. Метрики продуктивності (Performance Metrics)

**Що вимірювати**:
- **Response time** (час відповіді): Загальний час від промпту користувача до отримання повної відповіді.
- **Token efficiency** (ефективність використання токенів): Кількість вхідних/вихідних токенів, використаних на одне завдання.
- **Context utilization** (використання контексту): Яка частина вікна контексту була використана?
- **Cost per task** (вартість завдання): Вартість API для повної взаємодії.

**Як відстежувати**:
```bash
# Session-end hook: .claude/hooks/log-performance.sh
# Triggered at end of session

# Log structure:
{
  "timestamp": "2026-02-10T14:35:00Z",
  "agent_id": "backend-architect",
  "session_duration_s": 180,
  "input_tokens": 3500,
  "output_tokens": 2800,
  "total_cost_usd": 0.15,
  "context_utilization": 0.42
}
```

**Порада щодо впровадження**: Парсіть логи сесій Claude Code або використовуйте інструменти спостережуваності MCP.

---

### 4. Метрики задоволеності користувачів (User Satisfaction Metrics)

**Що вимірювати**:
- **Explicit feedback** (явний зворотний зв'язок): Оцінки користувачів, коментарі, звіти про баги.
- **Implicit signals** (неявні сигнали): Чи прийняв користувач пропозиції агента? Чи надіслав він промпт повторно?
- **Adoption rate** (рівень впровадження): Як часто використовується цей агент порівняно з альтернативами?
- **Retention** (утримання): Чи повертаються користувачі до цього агента для виконання аналогічних завдань?

**Як відстежувати**:
```bash
# Manual feedback collection
# After agent completes task, prompt user:
"Rate this agent's performance (1-5): _"

# Log:
{
  "timestamp": "2026-02-10T14:35:10Z",
  "agent_id": "backend-architect",
  "user_rating": 5,
  "user_comment": "Perfect analysis of auth flow",
  "would_use_again": true
}
```

**Порада щодо впровадження**: Додавайте запити зворотного зв'язку до шаблонів агентів або використовуйте опитування після завершення сесії.

---

## Шаблони впровадження

### Шаблон 1: Автоматична система хуків логування (Logging Hook System)

**Сценарій використання**: Автоматичне відстеження всіх взаємодій агента без ручного втручання.

**Налаштування**:
```bash
# .claude/hooks/post-tool-use.sh
#!/bin/bash
# Triggered after every tool call

AGENT_ID=$(echo "$CLAUDE_AGENT_ID" | jq -r)
TOOL_NAME=$(echo "$CLAUDE_TOOL_NAME" | jq -r)
TOOL_SUCCESS=$(echo "$CLAUDE_TOOL_SUCCESS" | jq -r)

# Append to metrics log
echo "{\"timestamp\":\"$(date -Iseconds)\",\"agent\":\"$AGENT_ID\",\"tool\":\"$TOOL_NAME\",\"success\":$TOOL_SUCCESS}" \
  >> .claude/logs/agent-metrics.jsonl
```

**Переваги**: Нульові ручні накладні витрати, повне покриття даних, дані у вигляді часових рядів.
**Недоліки**: Вимагає парсингу змінних оточення Claude Code (які можуть змінюватися між версіями).

---

### Шаблон 2: Юніт-тести для агентів (Agent Unit Tests)

**Сценарій використання**: Регресійне тестування для гарантії того, що покращення агента не ламають існуючі можливості.

**Налаштування**:
```bash
# tests/agents/backend-architect.test.sh
#!/bin/bash

# Test 1: Agent correctly identifies hexagonal architecture layers
echo "Test: Hexagonal architecture analysis"
RESULT=$(claude agent backend-architect "Analyze src/auth.ts for layer violations")
if echo "$RESULT" | grep -q "domain layer"; then
  echo "✅ PASS: Identified layers"
else
  echo "❌ FAIL: Did not identify layers"
  exit 1
fi

# Test 2: Agent recommends correct patterns
echo "Test: Pattern recommendations"
RESULT=$(claude agent backend-architect "Improve error handling in src/api.ts")
if echo "$RESULT" | grep -q "Result<T, E>"; then
  echo "✅ PASS: Recommended Result pattern"
else
  echo "❌ FAIL: Incorrect pattern"
  exit 1
fi
```

**Переваги**: Автоматизованість, виявлення регресій, інтеграція з CI/CD.
**Недоліки**: Вимагає підтримки тестів, можливі хибнопозитивні/хибнонегативні результати.

---

### Шаблон 3: A/B тестування конфігурацій (A/B Testing Configurations)

**Сценарій використання**: Порівняння двох версій агента для визначення того, яка з них працює краще.

**Налаштування**:
```yaml
# .claude/agents/backend-architect-v1.md (control)
name: backend-architect
version: 1.0
instructions: |
  You are a backend architect specializing in...
  [original instructions]

# .claude/agents/backend-architect-v2.md (experiment)
name: backend-architect-v2
version: 2.0
instructions: |
  You are a backend architect specializing in...
  [modified instructions with new pattern emphasis]
```

**Оцінка**:
```bash
# Run same task with both agents, compare metrics
# Task: "Analyze src/auth.ts for security issues"

# Version 1 metrics:
# - Response time: 45s
# - Issues found: 3
# - User rating: 4/5

# Version 2 metrics:
# - Response time: 38s
# - Issues found: 5 (2 additional critical issues)
# - User rating: 5/5

# Conclusion: Version 2 is more thorough and faster → promote to production
```

**Переваги**: Рішення на основі даних, кількісно вимірювані покращення.
**Недоліки**: Вимагає дисципліни для проведення контрольованих експериментів.

---

### Шаблон 4: Інтеграція циклу зворотного зв'язку (Feedback Loop Integration)

**Сценарій використання**: Безперервне вдосконалення агента на основі реальних даних використання.

**Налаштування**:
```bash
# After agent completes task
echo "How would you rate this response? (1-5, or 'skip'): "
read RATING

if [ "$RATING" != "skip" ]; then
  echo "Any specific feedback?: "
  read COMMENT

  # Log feedback
  echo "{\"timestamp\":\"$(date -Iseconds)\",\"agent\":\"$AGENT_ID\",\"rating\":$RATING,\"comment\":\"$COMMENT\"}" \
    >> .claude/logs/agent-feedback.jsonl
fi

# Weekly: Review feedback.jsonl, identify patterns
# Monthly: Update agent instructions based on aggregated feedback
```

**Переваги**: Адаптує агента до реальних потреб користувачів, виявляє граничні випадки (edge cases).
**Недоліки**: Вимагає ручного аналізу та реагування на зворотний зв'язок.

---

## Приклад: Агент з оцінкою

**Повний шаблон доступний за посиланням**: [`examples/agents/analytics-with-eval/`](../../examples/agents/analytics-with-eval/), що містить повне визначення агента, хуки, скрипти аналізу та шаблон звіту.

### Налаштування: Analytics Agent із вбудованими метриками

```yaml
# .claude/agents/analytics-agent.md
---
name: analytics-agent
description: SQL query generator with evaluation hooks
version: 1.0
tools:
  - Read
  - Write
  - Bash
hooks:
  post_response: .claude/hooks/log-analytics-metrics.sh
---

# Analytics Agent

You are an expert SQL analyst helping users query databases.

## Evaluation Criteria

After each query:
1. **Correctness**: Does query produce expected results?
2. **Performance**: Query execution time < 5s?
3. **Safety**: No destructive operations (DELETE, DROP, TRUNCATE)?
4. **Best practices**: Uses proper JOINs, indexes, parameterized queries?

## Instructions

[... agent instructions ...]
```

### Хук метрик (Metrics Hook)

```bash
# .claude/hooks/log-analytics-metrics.sh
#!/bin/bash
# Triggered after analytics-agent response

# Extract query from response (naive grep, improve with jq)
QUERY=$(echo "$CLAUDE_RESPONSE" | grep -oP 'SELECT.*?;')

if [ -n "$QUERY" ]; then
  # Test query (requires database connection)
  EXEC_TIME=$( (time psql -U user -d db -c "$QUERY") 2>&1 | grep real | awk '{print $2}')

  # Check for destructive operations
  if echo "$QUERY" | grep -iE 'DELETE|DROP|TRUNCATE'; then
    SAFETY="FAIL"
  else
    SAFETY="PASS"
  fi

  # Log metrics
  echo "{\"timestamp\":\"$(date -Iseconds)\",\"query\":\"$QUERY\",\"exec_time\":\"$EXEC_TIME\",\"safety\":\"$SAFETY\"}" \
    >> .claude/logs/analytics-metrics.jsonl
fi
```

### Аналіз (Analysis)

```bash
# Monthly review: Analyze metrics
jq -s 'group_by(.safety) | map({safety: .[0].safety, count: length})' \
  .claude/logs/analytics-metrics.jsonl

# Output:
# [
#   {"safety": "PASS", "count": 127},
#   {"safety": "FAIL", "count": 3}
# ]

# Action: Review 3 failed queries, update agent instructions to prevent future violations
```

---

## Інструменти та корисні посилання

### Відкриті фреймворки для оцінки (Open-Source Evaluation Frameworks)

#### nao (Analytics Agents)

**URL**: [github.com/getnao/nao](https://github.com/getnao/nao/)

**Що він надає**:
- Вбудований фреймворк оцінки для аналітичних агентів
- Можливості юніт-тестування для відповідей агентів
- Збір метрик (якість відповідей, використання інструментів, продуктивність)
- Інтеграція циклу зворотного зв'язку

**Як адаптувати для Claude Code**:
- **Context builder pattern** (патерн побудови контексту): Застосуйте структурований підхід nao до побудови контексту в конфігурації `.claude/agents/`
- **Evaluation hooks** (хуки оцінки): Перекладіть фреймворк оцінки nao на систему хуків Claude Code
- **Metrics schema** (схема метрик): Використовуйте схему метрик nao як шаблон для ваших власних логів

**Статус**: Готовий до продакшену, активно підтримується розробниками, TypeScript + Python.

---

### Вбудовані патерни Claude Code (Claude Code Native Patterns)

**Система хуків**: Директорія `.claude/hooks/` для автоматизованого логування (див. `examples/hooks/README.md`)

**Директорія агентів**: Директорія `.claude/agents/` для кастомних визначень агентів (див. `guide/ultimate-guide.md` Розділ 4)

**Спостережуваність MCP**: Використання MCP-серверів для розширеного логування та агрегації метрик.

---

## Найкращі практики

### Починайте з простого

- **Тиждень 1**: Додайте базовий хук логування (тільки виклики інструментів)
- **Тиждень 2**: Додайте запит зворотного зв'язку з користувачем (оцінки вручну)
- **Тиждень 3**: Побудуйте простий дашборд для візуалізації метрик
- **Тиждень 4**: Запустіть перший A/B тест конфігурації агента

### Фокусуйтеся на дієвих метриках

Не відстежуйте метрики, на основі яких ви не збираєтеся вживати жодних дій. Надавайте пріоритет:
1. **Task completion rate** (показник виконання завдань) → Вдосконалюйте інструкції агента
2. **Tool call errors** (помилки виклику інструментів) → Покращуйте контекст або додавайте більше прикладів
3. **User ratings** (оцінки користувачів) → Виявляйте незрозумілі або некорисні відповіді

### Автоматизуйте скрізь, де це можливо

Ручна оцінка не масштабується. Використовуйте:
- Хуки для автоматичного логування
- Інтеграцію з CI/CD для юніт-тестів агентів
- Скрипти для періодичної агрегації метрик

### Будуйте цикли зворотного зв'язку

Метрики марні без дій на їхній основі:
- Щотижня: Переглядайте метрики, виявляйте повторювані патерни
- Щомісяця: Оновлюйте інструкції агентів на основі зібраних даних
- Щокварталу: Проводьте масштабний рефакторинг агентів за потреби

---

## Пов'язані розділи

- **[Agents](#agents)**: Створення кастомних агентів
- **[Hooks](#hooks)**: Автоматизація за допомогою хуків подій
- **[Observability](../ops/observability.md)**: Стратегії логування та моніторингу
- **[AI Ecosystem](../ecosystem/ai-ecosystem.md#82-domain-specific-agent-frameworks)**: Зовнішні фреймворки, такі як nao

---

**Наступні кроки**:
1. Додайте хук логування до агента, якого ви використовуєте найчастіше
2. Збирайте метрики протягом 1 тижня
3. Проаналізуйте отримані дані та вдоскональте агента на їхній основі

**Шаблон**: Див. `examples/agents/analytics-with-eval/` для повного впровадження з хуками, скриптами та шаблоном звіту.

---
**Локалізація**: [Serhii (MacPlus Software)](https://macplus-software.com)
*Остання синхронізація: Травень 2026*
