---
name: talk-stage6-revision
description: "Створює аркуші повторення зі швидкою навігацією за діями, головною таблицею «концепція-URL», шпаргалкою Q&A із 6-10 очікуваних запитань, глосарієм і переліком зовнішніх ресурсів. Використовуйте, коли готуєтеся до доповіді з Q&A, створюєте довідковий матеріал для слухачів або будуєте глосарій-страховку для живого виступу."
allowed-tools: Write Read
effort: medium
---

# Етап 6 доповіді: Revision

Створює аркуші повторення, придатні для використання під час доповіді й після неї. Швидка навігація за діями, головна таблиця концепцій з URL для поширення, шпаргалка Q&A і глосарій.

## Коли використовувати цей skill

- Після етапу 5 (Script), що надає pitch + slides
- Перед доповіддю, де очікується Q&A
- Щоб створити ресурс, яким можна поділитися зі слухачами

## Що робить цей skill

1. **Читає всі вхідні дані**: pitch + slides + concepts (+ timeline, якщо є)
2. **Витягує навігацію**: зміст із якорями за діями
3. **Перебудовує за діями**: ключові концепції + метрики + історії + ймовірне Q&A
4. **Будує головну таблицю**: усі концепції + визначення + URL
5. **Будує шпаргалку Q&A**: 6-10 запитань + короткі відповіді + посилання
6. **Будує глосарій**: технічні терміни з доповіді
7. **Перелічує зовнішні ресурси**
8. **Збирає й зберігає**

## Вхідні дані

- `talks/{YYYY}-{slug}-pitch.md` (обов'язково)
- `talks/{YYYY}-{slug}-slides.md` (обов'язково)
- `talks/{YYYY}-{slug}-concepts.md` (обов'язково)
- `talks/{YYYY}-{slug}-timeline.md` (необов'язково, для точності метрик)

## Вивід

`talks/{YYYY}-{slug}-revision-sheets.md`

## Формат виводу

```markdown
# Revision Sheets: {title}

**Date**: {date} · **Talk duration**: {n} min + {n} min Q&A
**Purpose**: Someone asks a question -> find the section -> share the URL in 5 seconds

---

## Quick navigation

| Section | Content |
|---------|---------|
| [Act 1](#act-1) | {1-line summary} |
| [Act 2](#act-2) | {1-line summary} |
| [Act 3](#act-3) | {1-line summary} |
| [Act 4](#act-4) | {1-line summary} |
| [Act 5](#act-5) | {1-line summary} |
| [Conclusion](#conclusion) | {1-line summary} |
| [Master Table](#master-table) | All concepts + URLs |
| [Q&A Cheat-sheet](#qa-cheat-sheet) | {n} anticipated questions + answers |
| [Resources](#external-resources) | Links mentioned in the talk |

---

## ACT 1: {Title} (Slides 1-{n})

**~{n} min · {period or context}**

### Key concepts

| Concept | Short definition | URL to share |
|---------|-----------------|--------------|
| **{Concept}** | {1-2 concrete sentences} | {URL or "no direct link"} |
...

### Metrics to know

```
{Metrics as code block, one per line, format: value -> context}
```

### Storytelling / Anecdotes

- **{Anecdote name}**: "{Quote or summary}"

### Probable Q&A for Act {n}

| Question | Short answer |
|----------|-------------|
| "{probable question}" | {direct answer, 2-3 sentences max} |

---

[Repeat for each act]

---

## Conclusion (Slides {n}-{n})

**~{n} min**

### Summary metrics (the big numbers)

```
{All summary metrics, one per line}
```

### {N} actions for Monday (if applicable)

1. **{Action 1}**: {description + why}
2. **{Action 2}**: {description + why}
3. **{Action 3}**: {description + why}

---

## Master Table: Concept -> Definition -> URL to share

**The core deliverable. Every technical concept from the talk.**

| Concept | Definition (1-2 sentences) | Slide | URL to share | Notes |
|---------|--------------------------|-------|--------------|-------|
| **{Concept}** | {precise, concise definition} | {n} | {URL or "pure storytelling"} | {guide section if applicable} |
...

---

## Q&A Cheat-sheet

**The {n} most probable questions + short answers + URL to send**

---

### Q1: "{Question}"

**Short answer**:
{Answer in 3-5 bullets}

**To go further**:
- {Link 1 with context}
- {Link 2 with context}

---

[Q2 through Q{n}: same structure]

---

## External Resources Mentioned in the Talk

### Priority URLs to share

| Resource | URL | Context |
|----------|-----|---------|
| **{Resource}** | `{url}` | {why it's important} |
...

### Studies and external sources (if applicable)

| Source | URL | How used in the talk |
|--------|-----|---------------------|
| **{Source}** | `{url}` | {how it's cited} |

---

## Quick Glossary (memory aid if you blank)

| Term | Ultra-short definition |
|------|----------------------|
| {term} | {10 words max} |
...

---

*Generated {date}. Source: slides, concepts, pitch.*
```

## Правила побудови

### Головна таблиця
- Включіть УСІ технічні концепції, згадані в pitch і slides
- URL = посилання на публічний ресурс (GitHub, документація, посібник), жодних мертвих посилань
- Якщо посилання немає: зазначте «pure storytelling, no guide section» або «concept specific to the project»
- Визначення = те, що ви сказали б, якби хтось у залі запитав «що це?»

### Шпаргалка Q&A
- Мінімум 6 запитань, максимум 10
- Оберіть найімовірніші запитання для аудиторії
- Коротка відповідь = те, що ви сказали б усно максимум за 20 секунд
- «To go further» = посилання, за якими можна діяти, а не розмиті відсилання

### Метрики
- Формат блоку коду для метрик (швидше проглядати)
- Одна метрика на рядок: `{value}` ({context})
- Завжди з одиницями (%, мс, K, дні...)

### Історії
- Витягайте дослівно з pitch, де можливо (для запам'ятовування)
- Формат цитати для фраз, які слід сказати точно

## Антипатерни

- Неповна головна таблиця (брак концепцій = непридатність під час Q&A)
- Надто довгі відповіді в Q&A (якщо більше 5 пунктів, скоротіть)
- Вигадані або приблизні URL (перевірте, що кожне посилання справжнє)
- Копіювання описів із pitch без адаптації до формату шпаргалки
- Забутий глосарій (критично, коли в голові порожньо)

## Контрольний список валідації

- [ ] Швидка навігація з робочими якорними посиланнями
- [ ] Кожна дія має свій розділ (концепції + метрики + Q&A)
- [ ] Головна таблиця охоплює всі концепції pitch (перехресна перевірка)
- [ ] Мінімум 6 запитань у шпаргалці Q&A
- [ ] Зовнішні ресурси перелічено з перевіреними URL
- [ ] Глосарій присутній
- [ ] Файл збережено: `talks/{YYYY}-{slug}-revision-sheets.md`

## Поради

- Аркуші повторення є найчастіше повторно використовуваним результатом: слухачі просять посилання, а ви відкриваєте головну таблицю за 5 секунд
- Будуйте Q&A з профілю аудиторії (які 3 найскептичніші запитання поставив би в цій залі старший розробник?)
- Глосарій є вашою страховкою: забули термін посеред доповіді, глянули в глосарій, оговталися за 2 секунди

## Пов'язане

- [Етап 5: Script](../stage-5-script/SKILL.uk.md): передумова
- [Оркестратор](../orchestrator/SKILL.uk.md)
