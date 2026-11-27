---
title: "Аналітичний агент із вбудованим оцінюванням"
description: "Готовий до продакшену аналітичний агент з автоматичним збором метрик і перевіркою безпеки"
tags: [agents, template, testing, performance]
---

# Аналітичний агент із вбудованим оцінюванням

**Шаблон**: готовий до продакшену аналітичний агент з автоматичним збором метрик

**Сценарій використання**: генерація SQL-запитів з відстеженням якості, моніторингом продуктивності та перевіркою безпеки

**Пов'язаний посібник**: [Agent Evaluation](../../../guide/roles/agent-evaluation.uk.md)

---

## Що входить

| Файл | Призначення |
|------|---------|
| `analytics-agent.md` | Визначення агента з критеріями оцінювання |
| `hooks/post-response-metrics.sh` | Автоматичне логування метрик після кожної відповіді |
| `eval/metrics.sh` | Скрипт аналізу для агрегування зібраних метрик |
| `eval/report-template.md` | Шаблон щомісячних звітів з оцінювання |

---

## Налаштування

### 1. Скопіюй агента в проєкт

```bash
# Copy agent definition
cp analytics-agent.md ~/.claude/agents/

# Or for project-specific:
cp analytics-agent.md /path/to/project/.claude/agents/
```

### 2. Встанови hook

```bash
# Copy hook to project
cp hooks/post-response-metrics.sh /path/to/project/.claude/hooks/

# Make executable
chmod +x /path/to/project/.claude/hooks/post-response-metrics.sh
```

### 3. Налаштуй тригер hook

Додай у `.claude/settings.json`:

```json
{
  "hooks": {
    "postToolUse": [
      {
        "command": ".claude/hooks/post-response-metrics.sh",
        "enabled": true,
        "description": "Log analytics agent metrics"
      }
    ]
  }
}
```

### 4. Створи каталог для логів

```bash
mkdir -p /path/to/project/.claude/logs
```

---

## Використання

### Виклик агента

```bash
# In Claude Code session
"Use analytics-agent to generate a SQL query for [task description]"
```

### Перевірка метрик

```bash
# View raw metrics log
cat .claude/logs/analytics-metrics.jsonl

# Run analysis
./examples/agents/analytics-with-eval/eval/metrics.sh
```

### Генерація щомісячного звіту

```bash
# Copy template
cp eval/report-template.md reports/analytics-2026-02.md

# Fill in metrics from metrics.sh output
```

---

## Метрики, що збираються

Hook автоматично логує:

| Метрика | Опис | Джерело |
|--------|-------------|--------|
| `timestamp` | Позначка часу ISO 8601 | Система |
| `query` | Згенерований SQL-запит | Відповідь агента |
| `exec_time` | Час виконання запиту | База даних |
| `safety` | PASS/FAIL для деструктивних операцій | Аналіз запиту |
| `row_count` | Кількість повернутих рядків | База даних |
| `error` | Повідомлення про помилку, якщо запит не вдався | База даних |

**Формат логу**: JSONL (JSON Lines) у `.claude/logs/analytics-metrics.jsonl`

---

## Приклад виводу метрик

```bash
$ ./eval/metrics.sh

=== Analytics Agent Metrics Report ===
Period: 2026-02-01 to 2026-02-10

Total queries: 45
Safety checks:
  - PASS: 42 (93%)
  - FAIL: 3 (7%)

Execution time:
  - Mean: 2.3s
  - Median: 1.8s
  - P95: 5.2s
  - P99: 8.1s

Common failures:
  1. DELETE without WHERE clause (2 occurrences)
  2. DROP TABLE in query (1 occurrence)

Recommendations:
  - Review agent instructions to emphasize WHERE clause requirement
  - Add explicit prohibition on DROP operations
```

---

## Налаштування під себе

### Зміна перевірок безпеки

Відредагуй рядки 12-16 у `hooks/post-response-metrics.sh`:

```bash
# Add more patterns
if echo "$QUERY" | grep -iE 'DELETE|DROP|TRUNCATE|ALTER'; then
  SAFETY="FAIL"
fi
```

### Додавання власних метрик

Розшир структуру JSON-логу:

```bash
echo "{
  \"timestamp\":\"$(date -Iseconds)\",
  \"query\":\"$QUERY\",
  \"your_metric\":\"$VALUE\"
}" >> .claude/logs/analytics-metrics.jsonl
```

### Зміна розташування логу

Онови змінну `POST_RESPONSE_LOG` у скрипті hook.

---

## Усунення несправностей

### Hook не спрацьовує

**Перевір**:
1. Hook є виконуваним: `ls -l .claude/hooks/*.sh`
2. Hook увімкнено в settings.json
3. Назва агента збігається: `analytics-agent` (через дефіс)

**Налагодження**:
```bash
# Test hook manually
export CLAUDE_RESPONSE='{"content":"SELECT * FROM users;"}'
./.claude/hooks/post-response-metrics.sh
```

### У лозі немає метрик

**Перевір**:
1. Каталог логів існує: `mkdir -p .claude/logs`
2. Права на запис: `touch .claude/logs/test.log`
3. Патерн витягування запиту відповідає твоєму формату SQL

### Аналіз метрик не вдається

**Перевір**:
1. `jq` встановлено: `which jq`
2. Файл логу є коректним JSONL: `jq . .claude/logs/analytics-metrics.jsonl`

---

## Міркування для продакшену

### Продуктивність

- Hook додає ~50 мс накладних витрат на відповідь
- Файл логу зростає на ~200 байтів на запит
- Ротуй логи щомісяця, щоб уникнути розростання

### Приватність

- Логи містять реальні SQL-запити (можуть включати чутливі дані)
- Додай у `.gitignore`: `.claude/logs/`
- Розглянь можливість маскування чутливих значень у скрипті hook

### Підключення до бази даних

- Hook потребує доступу до бази даних для вимірювання `exec_time`
- Налаштуй підключення в скрипті hook або використовуй змінні середовища
- Для безпеки використовуй облікові дані лише для читання

---

## Пов'язані ресурси

- **[Agent Evaluation Guide](../../../guide/roles/agent-evaluation.uk.md)**: повна методологія оцінювання
- **[Hooks Documentation](../../../guide/ultimate-guide.uk.md#7-hooks)**: довідник із системи hooks
- **[nao Framework](https://github.com/getnao/nao/)**: фреймворк аналітичних агентів для продакшену (джерело натхнення)

---

## Ліцензія

Така сама, як у батьківського репозиторію (MIT)

**Є питання?** Відкрий issue або обговорення в основному репозиторії.
