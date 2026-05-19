---
title: "Cognitive Mode Switching"
description: "Switch between specialist roles across your ship cycle — strategic gate, architecture, paranoid review, release, browser QA, retrospective"
tags: [workflow, skills, planning, review, shipping, browser-automation]
---

# Cognitive Mode Switching

> **Confidence**: Tier 2 — Референсна імплементація: [gstack](https://github.com/garrytan/gstack) від Garry Tan (CEO Y Combinator), 1,100+ зірок за перші 24 години після запуску (Березень 2026).

**Час читання**: ~10 хв
**Необхідні знання**: Основи Claude Code skills, plan mode
**Пов'язані теми**: [Plan Pipeline](./plan-pipeline.uk.md), [Plan-Driven Development](./plan-driven.uk.md)

---

## TL;DR

Один універсальний асистент змішує всі фази розробки докупи. Цей патерн надає кожній фазі окремий когнітивний режим (cognitive mode): ви викликаєте правильну "півкулю мозку" для конкретного завдання, а потім перемикаєтесь, коли характер роботи змінюється.

```
/plan-ceo-review  → "Are we building the right thing?"
/plan-eng-review  → "How do we make this buildable?"
/review           → "What will blow up in production?"
/ship             → Execute the release, no debate
/browse           → Does it actually work in the browser?
/retro            → How well did we ship this week?
```

Основна ідея полягає в тому, що планування, рев'ю та шипінг вимагають фундаментально різних когнітивних підходів — і один асистент, залишений у загальному режимі, буде поєднувати їх вкрай неефективно.

---

## The 6 Gears

| Command | Role | Core question | When to switch |
|---------|------|---------------|----------------|
| `/plan-ceo-review` | Founder / CEO | "Are we building the right thing?" | Before writing any code |
| `/plan-eng-review` | Eng manager / tech lead | "How do we make this buildable?" | After direction is locked |
| `/review` | Paranoid staff engineer | "What can still break in prod?" | Before merging |
| `/ship` | Release engineer | "Get the plane landed" | Branch is ready, no more debate |
| `/browse` | QA engineer | "Does it actually work?" | After deploy, against staging or prod |
| `/retro` | Engineering manager | "How well did we ship?" | Weekly or post-launch |

---

## The Gap This Fills: Pre-Implementation Strategic Gate

Найважче завдання при роботі з AI-помічником для написання коду — це не сама реалізація. Це питання, яке передує їй: **чи правильну річ ми будуємо?**

Claude Code оптимізований для того, щоб створювати те, що ви просите. Якщо ви скажете "додати завантаження фото", він додасть завантаження фото. Він не запитає, чи є завантаження фото справжнім продуктом. Саме цю проблему вирішує `/plan-ceo-review`.

**Приклад**: Ви розробляєте додаток для оголошень на кшталт Craigslist.

- Запит: "Дозволити продавцям завантажувати фото для свого товару"
- Буквальна реалізація: вибір файлу + збереження зображення
- Яким є справжній продукт: допомога продавцям у створенні оголошень, які дійсно продають

Якщо спочатку запустити `/plan-ceo-review`, асистенту буде прямо доручено поставити під сумнів буквальний запит і знайти справжній продукт, схований всередині нього. Результатом стане зовсім інше технічне завдання: автоматично ідентифікувати продукт за фотографією, підтягнути характеристики та порівняльні ціни з мережі, підготувати чернетку назви та опису, запропонувати найкраще головне зображення, виявити низьку якість фото перед публікацією.

Це зовсім інша фіча. Набагато краща. І ви отримаєте її лише завдяки встановленню чіткого бар'єра перед початком реалізації.

**Три режими всередині `/plan-ceo-review`**:
- **SCOPE EXPANSION** (розширення рамок) — знайдіть версію продукту "на 10 зірок", запитайте "що зробить це в 10 разів кращим за вдвічі більших зусиль?"
- **HOLD SCOPE** (утримання рамок) — прийміть обраний напрямок, зробіть план бездоганним
- **SCOPE REDUCTION** (скорочення рамок) — безжально відсікайте все зайве до мінімально життєздатної версії (MVP)

Користувач обирає режим. Асистент фокусується на ньому та не відхиляється від курсу.

---

## /plan-eng-review: Making the Idea Buildable

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

## /review: Paranoid Staff Engineer Mode

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

## /browse: Non-MCP Native Browser Automation

`/browse` є найбільш технічно унікальною частиною gstack. Це не MCP server. Це скомпільований нативний бінарний файл (TypeScript + Bun), який запускає постійний фоновий процес headless Chromium.

**Чому архітектура має значення**:

| Approach | Cold start | Subsequent calls | State persistence |
|----------|-----------|-----------------|-------------------|
| MCP browser server | Нове з'єднання на кожну сесію | ~500ms+ | Втрачається між сесіями |
| `/browse` native daemon | ~3s (один раз) | ~100-200ms | Зберігаються cookies, вкладки та auth |

Це надзвичайно важливо для воркфлоу QA: ви один раз логінитесь у staging-середовище, а потім швидко виконуєте повну послідовність переходів, оскільки демон ніколи не перезапускається. Жодних накладних витрат на MCP-сокети, жодного скидання сесії.

**Доступні операції**: перехід за посиланням, читання тексту сторінки, створення скріншотів, знімок дерева доступності (accessibility tree) з посиланнями, кліки/заповнення форм за посиланнями, запуск JavaScript, перегляд консольних логів, перехоплення мережевих запитів.

**Коли варто віддати перевагу цьому інструменту замість MCP browser tools**:
- Чутливі до затримки QA-цикли (послідовна перевірка 10+ сторінок)
- Середовища, де підключення до MCP-серверів обмежені
- Коли вам потрібно, щоб стан браузера (авторизація, cookies) зберігався між декількома командами в одній сесії

**Коли краще залишитися з MCP**: перевірка однієї сторінки, простіші середовища або коли інструменти MCP-браузера вже налаштовані.

---

## Full Cycle Demo

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

# 5. Ship
You: /ship

Claude: [Syncs main, runs tests, pushes branch, opens PR — done]

# 6. Browser QA на staging
You: /browse staging.myapp.com — test the listing flow

Claude: [Navigates routes, fills upload form, verifies enrichment renders,
        checks console for errors, screenshots each step]
        All pages load correctly. Listing flow works end to end.
```

---

## Install

```bash
# Install globally (~/.claude/skills/)
git clone https://github.com/garrytan/gstack.git ~/.claude/skills/gstack
cd ~/.claude/skills/gstack && ./setup
```

Або просто вставте цю команду в Claude Code, і він зробить усе інше:

> Install gstack: run `git clone https://github.com/garrytan/gstack.git ~/.claude/skills/gstack && cd ~/.claude/skills/gstack && ./setup`

Для встановлення у команді (збереження у репозиторії, щоб `git clone` працював для колег), див. [gstack README](https://github.com/garrytan/gstack).

> **Примітка (Березень 2026)**: gstack було випущено 11 березня 2026 року. Патерни надійні, але сама реалізація є новою. Переконайтеся, що репозиторій активно підтримується, перш ніж впроваджувати його в production-процеси.

---

## When to Use This vs. Other Workflows

| Situation | This workflow | Alternative |
|-----------|---------------|-------------|
| Complex feature, direction uncertain | `/plan-ceo-review` спочатку | [Spec-First](./spec-first.uk.md) |
| Direction clear, architecture complex | `/plan-eng-review` | [Plan Pipeline](./plan-pipeline.uk.md) |
| Need independent validation of plan | [Plan Pipeline](./plan-pipeline.uk.md) `/plan-validate` | — |
| Browser automation, single page check | Будь-який інструмент MCP browser | `/browse` (надлишково) |
| Browser automation, multi-step QA loop | `/browse` | Інструменти MCP (повільніше) |
| Want structured ADR learning loop | [Plan Pipeline](./plan-pipeline.uk.md) | — |

Головна відмінність від [Plan Pipeline](./plan-pipeline.uk.md): gstack — це лінійна послідовність кроків ("шестерень"), якою ви керуєте вручну. Plan Pipeline — це більш автоматизована оркестрація з пам'яттю ADR та паралельними командами агентів. Для розробників-одинаків, які хочуть мати чіткий контроль над кожною фазою, gstack простіший у впровадженні.

---

## See Also

- [Plan Pipeline](./plan-pipeline.uk.md) — Автоматизований воркфлоу з 3 команд із навчальним циклом ADR
- [Plan-Driven Development](./plan-driven.uk.md) — Основи планування перед написанням коду
- [Iterative Refinement](./iterative-refinement.uk.md) — Цикли підвищення якості коду
- [gstack on GitHub](https://github.com/garrytan/gstack) — Вихідний код, інструкції з налаштування, повні промпти для навичок

---
**Локалізація**: [Serhii (MacPlus Software)](https://macplus-software.com)
*Остання синхронізація: Травень 2026*
