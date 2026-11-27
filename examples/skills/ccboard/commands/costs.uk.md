---
name: costs
description: Відкрити вкладку аналізу витрат у ccboard
category: analytics
---

# Команда аналізу витрат

Запускає ccboard і переходить одразу до вкладки відстеження та аналітики витрат.

## Можливості

- **3 види**:
  - Overview: загальні витрати й розбивка
  - By Model: витрати за кожною AI-моделлю (Opus, Sonnet, Haiku)
  - Daily Trend: зміна витрат із часом

- **Розбивка токенів**:
  - Вхідні токени (промпт)
  - Вихідні токени (генерація)
  - Токени читання кешу (повторно використані)
  - Токени запису в кеш (збережені)

- **Ціни**: автоматичний розрахунок за тарифами Anthropic 2024 року

## Використання

```bash
# Open costs tab directly
/costs

# Alternative: run with tab argument
ccboard --tab costs
```

## Навігація вкладкою Costs

- `1` : вид Overview
- `2` : вид By Model
- `3` : вид Daily Trend
- `Tab` : перемикання між видами
- `↑/↓` : прокручування даних

## Приклад виводу

```
Total Tokens: 17.32M
Total Cost: $9,145.20

Breakdown by Model:
- Opus 4.5:   76% ($7,828)  ████████████████
- Sonnet 4.5: 14% ($1,314)  ███
- Haiku 3.5:  10% ($3)      █

Token Distribution:
- Input:       10.70M (65%)
- Output:      4.58M  (28%)
- Cache Read:  1.01M  (6%)
- Cache Write: 1.04B  (1%)
```

## Вимоги

ccboard має бути встановлено. За потреби запустіть `/ccboard-install`.

## Реалізація

```bash
#!/bin/bash

# Check if ccboard is installed
if ! command -v ccboard &> /dev/null; then
    echo "❌ ccboard is not installed"
    echo "Run: /ccboard-install"
    exit 1
fi

# Launch ccboard with Costs tab (tab index 5, accessible with '6' key)
# For now, launch and user presses '6'
exec ccboard
```

**Примітка**: наразі ccboard запускається у вигляді дашборду. Натисніть `6`, щоб перейти до вкладки Costs.
Майбутня версія підтримуватиме `ccboard --tab costs` для прямого доступу.
