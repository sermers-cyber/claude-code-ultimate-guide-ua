---
title: "Дослідження перед реалізацією (Exploration Before Implementation)"
description: "Запитуйте у Claude кілька підходів із компромісами перед написанням коду, щоб запобігти ефекту якоря"
tags: [workflow, architecture, design-patterns]
---

# Дослідження перед реалізацією (Exploration Before Implementation)

> **Рівень впевненості**: Рівень 2, підтверджено дослідженнями практиків (+20-30% до якості прийняття рішень, +40% до виявлених альтернатив).
> **Джерело**: [Блог MetalBear Engineering](https://metalbear.com/blog/engineering-ai-use/), arXiv дослідження практиків

Перед написанням коду запитайте у Claude кілька різних підходів із компромісами (trade-offs). Це допомагає уникнути «ефекту якоря» (anchoring bias): тенденції фіксуватися на першому ж запропонованому рішенні.

---

## Зміст

1. [Коротко (TL;DR)](#tldr)
2. [Патерн](#the-pattern)
3. [Промпти проти ефекту якоря](#anti-anchoring-prompts)
4. [Коли використовувати](#when-to-use)
5. [Інтеграція з Claude Code](#integration-with-claude-code)
6. [Антипатерни](#anti-patterns)
7. [Дивіться також](#see-also)

---

## TL;DR

```
1. Describe problem (no code, no preconception)
2. Request 3-5 approaches with trade-offs
3. Ask for quantified comparison
4. Choose approach
5. Then implement
```

Ключовий інсайт: **Як тільки модель пропонує конкретне рішення, це може мимовільно звузити ваше мислення.**

---

## Патерн

### Крок 1: Тільки опис проблеми

Починайте з проблеми, а не з напрямку рішення:

```
I need to handle user sessions in a Node.js API.
Requirements:
- Support 10K concurrent users
- Session data: user ID, permissions, preferences
- Must survive server restarts
```

**Не робіть так** (фіксація на Redis):
```
I'm thinking of using Redis for sessions. How should I implement it?
```

### Крок 2: Запитайте кілька підходів

```
Give me 4 different approaches to solve this.
For each, include:
- Architecture overview
- Pros and cons
- Performance characteristics
- Complexity to implement
```

### Крок 3: Кількісне порівняння

```
Now rank these approaches on a 1-10 scale for:
- Latency (lower is better)
- Scalability (10K → 100K users)
- Operational complexity
- Development time
```

### Крок 4: Оберіть, а потім реалізуйте

```
I'll go with approach B (JWT + Redis hybrid).
Now implement it following our existing patterns in src/auth/.
```

---

## Промпти проти ефекту якоря

Великі мовні моделі (LLM) можуть фіксуватися на своїй першій пропозиції. Ці промпти допомагають боротися з цим:

| Тип промпту | Шаблон | Ефект |
|-------------|----------|--------|
| **Свіжий старт** | "Ignore any prior ideas. Generate 4 novel approaches to [X]" | Змушує до різноманітності |
| **Цикл роздумів** | "Generate 3 options, then critique each, then recommend" | Самокорекція (зниження ефекту якоря на 25%) |
| **Кількісні компроміси** | "Rank by [metric1], [metric2], [metric3] with scores 1-10" | Об'єктивне порівняння |
| **Адвокат диявола** | "What are the strongest arguments against your recommendation?" | Виявлення прихованих компромісів |
| **Зміна обмежень** | "Now solve the same problem with [opposite constraint]" | Розширення простору рішень |

### Приклад: Промпт проти ефекту якоря

```
I need pagination for a REST API with 1M+ records.

IMPORTANT: Don't suggest offset-based pagination first.
Generate 4 different pagination strategies, including at least one
unconventional approach. For each:

1. How it works (2-3 sentences)
2. Best use case
3. Worst use case
4. Performance at 1M records

Then recommend one, explaining why it beats the others for my use case.
```

### Промпт для циклу роздумів

```
For implementing real-time notifications:

Phase 1: Generate 3 approaches (WebSockets, SSE, Long Polling)
Phase 2: For each, list 2 things that could go wrong in production
Phase 3: Based on Phase 2, which approach is most resilient?

Show your reasoning for each phase.
```

---

## Коли використовувати

### Використовуйте дослідження

| Сценарій | Чому |
|----------|-----|
| Нові функції (Greenfield) | Немає існуючого патерну для наслідування |
| Архітектурні рішення | Мають великий вплив, важко змінити |
| Кілька можливих підходів | Потрібен усвідомлений вибір |
| Незнайома предметна область | Ви не знаєте того, чого не знаєте |
| Незгода в команді | Отримайте нейтральний аналіз варіантів |

### Пропускайте дослідження

| Сценарій | Чому |
|----------|-----|
| Виправлення багів | Рішення зазвичай очевидне з симптомів |
| Єдиний можливий підхід | Немає реального вибору |
| Термінові хотфікси | Швидкість > досконалість |
| Наслідування існуючого патерну | Рішення вже прийнято |
| Тривіальні зміни | Витрати на планування не варті того |

---

## Інтеграція з Claude Code

### З Plan Mode

Дослідження відбувається **перед** входом у Plan Mode:

```
# Step 1: Explore (not in Plan Mode yet)
I need to add caching to the API. What are my options?

# Claude responds with 4 approaches

# Step 2: Choose
Let's go with approach C (edge caching with Cloudflare).

# Step 3: Plan (press Shift+Tab twice to enter Plan Mode)
Implement edge caching using Cloudflare Workers.
Follow the patterns in our existing middleware.
```

### З CLAUDE.md

Додайте тригери дослідження до інструкцій вашого проекту:

```markdown
## Workflow Preferences

### Before New Features
When implementing new features, first explore 3-4 approaches
with trade-offs before committing to implementation.
Use quantified comparison (1-10 scale) for:
- Performance
- Maintainability
- Time to implement
```

### З інструментом завдань (Task Tool)

Відстежуйте дослідження як завдання:

```
TaskCreate: "Explore caching approaches"
TaskCreate: "Choose approach based on analysis"
TaskCreate: "Implement cache invalidation"
TaskCreate: "Add cache headers to responses"
# Mark completed as you progress with TaskUpdate
```

---

## Антипатерни

### Передчасне за якорення (Premature Anchoring)

```
# Wrong
"I want to use Redis for caching. How do I set it up?"

# Right
"I need caching for API responses. What are my options?"
```

Ви відкинули 90% рішень ще до початку дослідження.

### Поверхневе порівняння

```
# Wrong
"Which is better: Redis or Memcached?"

# Right
"Compare Redis, Memcached, and in-process caching for:
- 50MB cache size
- Read-heavy workload (95% reads)
- Single server deployment
Include latency, memory overhead, and operational complexity."
```

### Ігнорування компромісів

```
# Wrong
"Just tell me the best approach"

# Right
"What would I give up by choosing approach A over B?
What scenarios would make me regret this choice?"
```

### Аналітичний параліч

```
# Wrong
Exploring 10 options for a simple feature

# Right
Set a limit: "Give me your top 3 approaches, no more"
Make a decision and iterate if needed
```

---

## Приклад сесії

### Первинне дослідження

```
User: I need to implement real-time updates in our React dashboard.
      The dashboard shows ~50 metrics that update every 5 seconds.
      Currently we poll, but users complain about stale data.

Claude: Here are 4 approaches:

**A) WebSockets**
- Full duplex, server can push anytime
- Pros: Lowest latency, true real-time
- Cons: Connection management, scaling complexity
- Best for: Sub-second updates, bidirectional communication

**B) Server-Sent Events (SSE)**
- Unidirectional server → client stream
- Pros: Simple, HTTP-based, auto-reconnect
- Cons: One-way only, limited browser connections
- Best for: Dashboard feeds, notifications

**C) Long Polling**
- Client holds request until data ready
- Pros: Works everywhere, simple fallback
- Cons: Higher latency, more server load
- Best for: Legacy compatibility

**D) GraphQL Subscriptions**
- WebSocket-based with GraphQL schema
- Pros: Type-safe, selective updates
- Cons: Requires GraphQL infrastructure
- Best for: Existing GraphQL APIs

User: Rank these for our use case (React, 50 metrics, 5s refresh,
      team has no WebSocket experience).

Claude: Scores (1-10, higher is better):

| Approach | Latency | Complexity | Team Fit | Scalability |
|----------|---------|------------|----------|-------------|
| WebSockets | 10 | 4 | 3 | 7 |
| SSE | 8 | 8 | 8 | 8 |
| Long Polling | 5 | 9 | 9 | 5 |
| GraphQL Subs | 9 | 3 | 2 | 7 |

**Recommendation: SSE**
Best balance of simplicity and real-time capability.
Your team can implement it in a day, and it handles your
50 metrics × 5s updates easily. Upgrade to WebSockets later
if you need bidirectional or sub-second updates.

User: Let's go with SSE. Now implement it.
```

---

## Дивіться також

- [plan-driven.md](./plan-driven.uk.md): для дослідження кодової бази (режим `/plan`)
- [iterative-refinement.md](./iterative-refinement.uk.md): доопрацювання після вибору підходу
- [../examples/semantic-anchors/anchor-catalog.md](https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/examples/semantic-anchors/anchor-catalog.md): точний словник для промптів
- [spec-first.md](./spec-first.uk.md): визначення вимог перед дослідженням

---
**Локалізація**: [Serhii (MacPlus Software)](https://macplus-software.com)
*Остання синхронізація: Травень 2026*
