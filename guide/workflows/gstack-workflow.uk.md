---
title: "Перемикання когнітивних режимів"
description: "Відібраний шлях через gstack: поставити під сумнів попит, переглянути архітектуру й код, перевірити поведінку, випустити й підбити підсумки"
tags: [workflow, skills, planning, review, shipping, browser-automation]
---

# Перемикання когнітивних режимів

> **Джерело**: [gstack](https://github.com/garrytan/gstack) від Garry Tan. Ця сторінка добирає шість кроків робочого процесу з більшого пакета skills, що розвивається; актуальний список команд дивіться в репозиторії.

**Час читання**: ~10 хв
**Необхідні знання**: Основи Claude Code skills, plan mode
**Пов'язані теми**: [Plan Pipeline](./plan-pipeline.uk.md), [Plan-Driven Development](./plan-driven.uk.md)

---

## TL;DR

Агент для кодингу може змішувати продуктові рішення, реалізацію, рев'ю та реліз. Цей добраний шлях gstack надає кожному кроку окреме питання, а користувач сам вирішує, коли додатковий крок виправдовує свою вартість.

```
/plan-ceo-review  → "Are we building the right thing?"
/plan-eng-review  → "How do we make this buildable?"
/review           → "What can still break?"
/qa               → Test the changed behavior
/ship             → Complete the Git and PR workflow
/retro            → What should change next time?
```

Планування, рев'ю та реліз вимагають фундаментально різних когнітивних підходів. Один асистент, залишений у загальному режимі, поєднує їх вкрай неефективно.

---

## Шість відібраних гейтів

| Команда | Роль | Ключове питання | Коли перемикатися |
|---------|------|---------------|----------------|
| `/plan-ceo-review` | Founder / CEO | "Are we building the right thing?" | When product direction is uncertain |
| `/plan-eng-review` | Eng manager / tech lead | "How do we make this buildable?" | After direction is locked |
| `/review` | Paranoid staff engineer | "What can still break in prod?" | Before merging |
| `/qa` | QA engineer | "Does the changed behavior work?" | Before the release decision, against a safe target |
| `/ship` | Release engineer | "Is the branch ready to publish?" | After review and applicable QA |
| `/retro` | Engineering manager | "How well did we ship?" | Weekly or post-launch |

---

## Прогалина, яку це закриває: стратегічний гейт перед реалізацією

Найважче завдання при роботі з AI-помічником для написання коду — це не сама реалізація. Це питання, яке передує їй: **чи правильну річ ми будуємо?**

Claude Code оптимізований для того, щоб створювати те, що ви просите. Якщо ви скажете "додати завантаження фото", він додасть завантаження фото. Він не запитає, чи є завантаження фото справжнім продуктом. Саме цю проблему вирішує `/plan-ceo-review`.

**Приклад**: Ви розробляєте додаток для оголошень на кшталт Craigslist.

- Запит: "Дозволити продавцям завантажувати фото для свого товару"
- Буквальна реалізація: вибір файлу + збереження зображення
- Яким є справжній продукт: допомога продавцям у створенні оголошень, які дійсно продають

Якщо спочатку запустити `/plan-ceo-review`, асистенту буде прямо доручено поставити під сумнів буквальний запит і знайти справжній продукт, схований всередині нього. Результатом стане зовсім інше технічне завдання: автоматично ідентифікувати продукт за фотографією, підтягнути характеристики та порівняльні ціни з мережі, підготувати чернетку назви та опису, запропонувати найкраще головне зображення, виявити низьку якість фото перед публікацією.

Це інша, більша пропозиція фічі. Перш ніж вона замінить вужчий початковий запит, потрібні докази, що продавці цього хочуть і що додаткова робота того варта.

**Режими всередині `/plan-ceo-review`** охоплюють розширення (expansion), вибіркове розширення (selective expansion), утримання рамок (hold scope) та скорочення (reduction). Це різні способи поставити пропозицію під сумнів, а не правило збільшувати обсяг. Обирайте режим залежно від потреби користувача та вартості вже виконаної роботи.

Користувач обирає режим. Асистент фокусується на ньому та не відхиляється від курсу.

---

## /plan-eng-review: як зробити ідею придатною до реалізації

Як тільки напрямок затверджено, когнітивний режим перемикається з продуктової інтуїції на інженерну суворість. `/plan-eng-review` — це місце, де завершується генерація ідей і починається архітектура.

Що це має згенерувати:
- Архітектурну діаграму (компоненти, межі, потоки даних)
- Скінченний автомат (state machine) для основного флоу
- Рішення щодо синхронних та асинхронних меж
- Сценарії відмов та логіку повторних спроб (retry logic)
- Межі довіри (де приймаються зовнішні дані?)
- Матрицю тестів

Ключовий фактор успіху тут — **примусова генерація діаграм**. Діаграми витягують на поверхню приховані припущення, які текст може маскувати. Діаграма послідовності (sequence diagram) змушує вас детально описати, хто і що викликає. Скінченний автомат змушує перелічити кожен сценарій відмови. Без цього фраза "система сама все обробить" залишається розмитою на невизначений термін.

---

## /review: режим параноїдального staff-інженера

Успішне проходження тестів ще не означає, що гілка безпечна. `/review` створений для пошуку тієї категорії багів, які проходять через CI та все одно потрапляють у production.

Що перевіряється:
- N+1 запити
- Стани гонитви (race conditions) (наприклад, коли дві вкладки перезаписують один і той самий стан)
- Порушення меж довіри (прийняття метаданих від клієнта без валідації)
- Загублені дані (orphaned data) на шляхах помилок
- Відсутні індекси
- Погана логіка повторних спроб (bad retry logic)
- Тести, які проходять успішно, але не перевіряють справжній сценарій відмови
- Prompt injection, коли вивід LLM потрапляє в подальшу обробку

Підхід тут свідомий: уявіть інцидент на продакшені ще до того, як він трапиться.

---

## Браузерний QA: `/qa` і `/browse`

Актуальний gstack розділяє браузерний драйвер і робочий процес QA. [`/browse`](https://github.com/garrytan/gstack/blob/main/docs/skills.md) відкриває сторінки та перевіряє взаємодії; `/qa` обирає глибину тестування, фіксує докази й може відтворити дефект до виправлення. Для браузера він використовує Aside, якщо той доступний, а інакше власний браузер gstack. Ця сторінка не стверджує, що він швидший за інші браузерні інструменти.

Lean-питання: чи виявляє ця перевірка дефекти до того, як вони підуть далі, не створюючи черги неперевірених звітів. Успішна браузерна перевірка охоплює лише ті сценарії, які було виконано, а не всі результати для користувача.

---

## Демо повного циклу

Це ілюстративна послідовність, а не виміряний результат gstack.

```
# 1. Strategic gate — аналіз завдання
[plan mode]
You: I want to add seller photo upload to the listing app.
     Sellers should be able to upload a photo and we create the listing from it.

You: /plan-ceo-review   (select SCOPE EXPANSION mode)

Claude: "Photo upload" is not the feature. The real job is helping sellers
        create listings that actually sell. Here's the 10-star version:
        auto-identify the product, pull specs and pricing comps from the web,
        draft title and description, suggest the best hero image...

# 2. Engineering gate — затвердження архітектури
You: /plan-eng-review

Claude: [Architecture diagram, async job boundaries, state machine for
        upload → classify → enrich → draft pipeline, failure modes,
        trust boundaries, test matrix]

# 3. Реалізація плану
[exit plan mode, write code]

# 4. Paranoid review — пошук того, що пропустили тести
You: /review

Claude: Race condition: two tabs can overwrite cover-photo selection.
        Trust boundary: pulling web data into draft generation creates
        a prompt injection vector.
        Missing: orphan cleanup for failed uploads.

You: [fix the issues]

# 5. QA against a safe local or staging target
You: /qa staging.myapp.com

Claude: [Exercises the listing flow, records the cases tried and any failures]
        The tested listing path passes; other user outcomes remain unmeasured.

# 6. Ship after the release decision
You: /ship

Claude: [Runs release checks, then commits, pushes and opens a PR when authorized]
```

---

## Встановлення

```bash
# Install globally (~/.claude/skills/)
git clone https://github.com/garrytan/gstack.git ~/.claude/skills/gstack
cd ~/.claude/skills/gstack && ./setup
```

Або просто вставте цю команду в Claude Code, і він зробить усе інше:

> Install gstack: run `git clone https://github.com/garrytan/gstack.git ~/.claude/skills/gstack && cd ~/.claude/skills/gstack && ./setup`

Для встановлення у команді (збереження у репозиторії, щоб `git clone` працював для колег), див. [gstack README](https://github.com/garrytan/gstack).

> **Поточний обсяг**: у gstack більше skills, ніж ці шість. Перш ніж додавати skill до робочого процесу проєкту, перегляньте актуальний README та побічні ефекти цього skill.

---

## Коли використовувати це, а коли інші воркфлоу

| Ситуація | Цей воркфлоу | Альтернатива |
|-----------|---------------|-------------|
| Complex feature, direction uncertain | `/plan-ceo-review` спочатку | [Spec-First](./spec-first.uk.md) |
| Direction clear, architecture complex | `/plan-eng-review` | [Plan Pipeline](./plan-pipeline.uk.md) |
| Need independent validation of plan | [Plan Pipeline](./plan-pipeline.uk.md) `/plan-validate` | — |
| One-off browser inspection | `/browse` або доступний браузерний інструмент | Без явної перевірки результату QA немає |
| Changed-flow verification | `/qa` | Зафіксуйте перевірений шлях, збої та неперевірену поведінку |
| Want structured ADR learning loop | [Plan Pipeline](./plan-pipeline.uk.md) | — |

Ця сторінка подає добрану послідовність, яку ви викликаєте свідомо; ширший пакет gstack містить і автоматизовані шляхи. [Plan Pipeline](./plan-pipeline.uk.md): окремий підхід до оркестрації. Порівнюйте будь-який із них із реальним очікуванням і переробками у вашому потоці поставки, а не вважайте, що більше етапів означає краще.

---

## Див. також

- [Plan Pipeline](./plan-pipeline.uk.md) — Автоматизований воркфлоу з 3 команд із навчальним циклом ADR
- [Plan-Driven Development](./plan-driven.uk.md): Основи планування перед написанням коду
- [Iterative Refinement](./iterative-refinement.uk.md): Цикли підвищення якості коду
- [gstack on GitHub](https://github.com/garrytan/gstack): Вихідний код, інструкції з налаштування, повні промпти для навичок

---
**Локалізація**: [Serhii (MacPlus Software)](https://macplus-software.com)
*Остання синхронізація: Травень 2026*
