---
title: "Щотижневий огляд Anthropic (17-23 лютого 2026)"
type: "weekly-watch"
date: "2026-02-22"
score: 3
action: "partial-integration"
sources:
  - "Скопійований текст (дайджест-агрегатор, без URL)"
---

# Щотижневий огляд Anthropic (17-23 лютого 2026)

## Підсумок

Дайджест-агрегатор, що охоплює Sonnet 4.6, Claude Code Security, CC v2.1.49-v2.1.50, Automatic Prompt Caching API, виведення моделей з експлуатації та активність у Twitter.

## Оцінка: 3/5

**Обґрунтування**: дайджест первинних джерел (блог Anthropic, CHANGELOG на GitHub, Twitter). 50% уже задокументовано в посібнику. Справжня цінність — сигнал про 2-3 прогалини: prompt caching API (нульове покриття), виведення моделей з експлуатації (нульове покриття), відсутні змінні середовища. Оцінка 3 (знижено з 4 до 3 після виклику): це тригер для пошуку, а не джерело, на яке можна послатися — немає URL, твердження про API не можна перевірити безпосередньо.

## Виявлені прогалини

| Прогалина | Розташування | Пріоритет |
|-----|-------------|----------|
| Prompt caching API (`cache_control`) | guide/ultimate-guide.md (Cost Optimization) | **P1** |
| Змінна середовища `CLAUDE_CODE_DISABLE_1M_CONTEXT` | guide/ultimate-guide.md (таблиця змінних середовища) | **P1** |
| Уточнення щодо змінної середовища `CLAUDE_CODE_SIMPLE` | guide/ultimate-guide.md (таблиця змінних середовища) | **P1** |
| Виведення моделей з експлуатації (Haiku 3 → 20 квітня 2026) | guide/ultimate-guide.md або architecture.md | P2 |
| Поле агента `background: true` | guide/ultimate-guide.md (розділ про агентів) | P2 |
| Команда CLI `claude agents` | guide/ultimate-guide.md (розділ про агентів) | P2 |
| Hooks worktree `WorktreeCreate`/`WorktreeRemove` | guide/ultimate-guide.md (розділ про worktree) | P3 |

## Перевірка фактів

| Твердження | Статус | Джерело |
|-------------|--------|--------|
| Sonnet 4.6 = модель за замовчуванням | ✅ Перевірено | ultimate-guide.md:1765 |
| Дати CC v2.1.49/v2.1.50: 19-20 лютого | ✅ Перевірено | claude-code-releases.md:27-51 |
| Claude Code Security research preview | ✅ Перевірено | security-hardening.md:780-832 |
| Haiku 3 визнано застарілою 19 лютого 2026, виведення 20 квітня | ✅ Перевірено | Perplexity → platform.claude.com/docs/model-deprecations |
| «Автоматичне» Prompt Caching (нуль конфігурації) | ⚠️ Некоректно | Anthropic використовує **явні** точки розриву (`cache_control`), а не автоматичні. Perplexity підтверджує: «developer-controlled through explicit cache breakpoints, not automatic» |
| Sonnet 3.7 / Haiku 3.5 виведено з експлуатації | ⚠️ Не перевірено | Не знайдено в джерелах Perplexity. Перевірити на docs.anthropic.com/release-notes |
| Ціна prompt caching: знижка 90% | ✅ Перевірено | Читання з кешу = 0.1x базової ціни (Perplexity + документація Anthropic) |

## Дії P1 (виконано)

1. **Prompt caching** → Strategy 6 додано до Cost Optimization Strategies (ultimate-guide.md ~1912)
2. **Змінні середовища** → `CLAUDE_CODE_DISABLE_1M_CONTEXT` і `CLAUDE_CODE_SIMPLE` додано до основної таблиці (ultimate-guide.md ~19862)

## Виклик (technical-writer)

- **Скоригована оцінка**: 3/5 (знижено з 4 до 3)
- **Причина**: дайджест без URL = джерело, на яке не можна послатися. 50% уже охоплено. Цінність — у тому, що це тригер первинного пошуку.
- **Головний ризик**: твердження про «automatic prompt caching» некоректне — Anthropic вимагає явного `cache_control`. Не інтегрувати цього формулювання.
- **Наступні кроки**: перевірити Sonnet 3.7/Haiku 3.5 в офіційній документації до інтеграції P2.
