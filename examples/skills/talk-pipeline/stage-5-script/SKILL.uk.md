---
name: talk-stage5-script
description: "Створює повний пітч у 5 діях із нотатками доповідача, специфікацію слайд за слайдом і готовий до вставлення промпт для Kimi для генерації слайдів ШІ. Потребує підтверджених ракурсу й назви з етапу 4. Використовуйте, коли маєте підтверджений ракурс доповіді й потрібні повний сценарій, специфікація слайдів і промпт для презентації, згенерованої ШІ."
allowed-tools: Write Read
effort: high
---

# Етап 5 доповіді: Script

Створює повну доповідь у 3 результатах: наратив у 5 діях із нотатками доповідача, специфікацію слайдів і промпт для Kimi, готовий до копіювання.

**Передумова**: користувач підтвердив ракурс і назву на CHECKPOINT етапу 4. Не запускайте цей етап без цього підтвердження.

## Коли використовувати цей skill

- Після підтвердження CHECKPOINT етапу 4
- Коли маєте підтверджені ракурс і назву
- Щоб створити повний сценарій і специфікацію слайдів

## Що робить цей skill

1. **Перевіряє вхідні дані**: усі файли попередніх етапів + підтвердження ракурсу/назви
2. **Завантажує шаблон Kimi**: з `templates/kimi-prompt-template.md`
3. **Будує пітч**: структура з 5 дій, нотатки доповідача й таймінг
4. **Будує специфікацію слайдів**: слайд за слайдом із візуалом, текстом, нотатками
5. **Генерує промпт для Kimi**: заповнює шаблон вмістом доповіді
6. **Зберігає 3 файли**

## Вхідні дані

- `talks/{YYYY}-{slug}-summary.md`
- `talks/{YYYY}-{slug}-concepts.md`
- `talks/{YYYY}-{slug}-angles.md`
- `talks/{YYYY}-{slug}-titre.md`
- `talks/{YYYY}-{slug}-timeline.md` (необов'язково, збагачує нотатки доповідача)
- **Обраний ракурс + обрана назва** (явне підтвердження користувача з етапу 4)

## Вивід

- `talks/{YYYY}-{slug}-pitch.md`
- `talks/{YYYY}-{slug}-slides.md`
- `talks/{YYYY}-{slug}-kimi-prompt.md`

## Формат pitch.md

```markdown
# Pitch: {title}

**Event**: {event} | **Duration**: {duration} min | **Slides**: ~{n} slides
**Angle**: {selected angle}

---

## Global structure

| Act | Title | Duration | Slides |
|-----|-------|----------|--------|
| 1 | {act title} | {n} min | {n} slides |
...
| Total | | {duration} min | {n} slides |

---

## ACT 1: {TITLE} (Slides 1-{n}, ~{n} min)

{Narrative description of the act in 2-3 sentences: what happens, the emotion targeted}

---

**Slide {n}: {Slide title}**
- Visual: {visual description, simple and precise}
- Key text: {what appears on screen, max 10 words}
- Speaker notes: "{exact text to say, conversational and natural}"
- Duration: {n} min
- Pause: yes/no | {if yes: why, intended effect}

---

[Repeat for each slide in the act]

---

[Acts 2, 3, 4, 5: same structure]

---

## Key moments (must not be rushed)

| Moment | Slide | What happens | Technique |
|--------|-------|-------------|-----------|
| {moment} | {n} | {description} | Pause / Number / Anecdote |

---

## Timing check

| Act | Planned | Buffer | Total |
|-----|---------|--------|-------|
| ACT 1 | {n} min | 30s | {n} min |
...
| **Total** | **{n} min** | **{n} min** | **{n} min** |

Q&A planned: {n} min
```

## Формат slides.md

Специфікація слайд за слайдом, готова для передачі дизайнеру або Kimi.

```markdown
# Slides Spec: {title}

**Total**: {n} slides | **Event**: {event} | **Date**: {date}

---

### SLIDE 1: Title Slide

- **Main title**: {title}
- **Subtitle**: {subtitle or tagline}
- **Speaker**: {name}
- **Event**: {event} ({date})
- **Visual**: {background description, texture, image, mood}
- **Speaker notes**: "{text}"
- **Duration**: {n} sec

---

### SLIDE {n}: {Slide title}

- **Title**: {title}
- **Visual**: {precise visual description}
  - Type: {bar chart / timeline / diagram / big number / comparison table / screenshot placeholder}
  - Data: {specific values if chart}
- **Key text**: {what appears, max 30 words total}
- **Metrics displayed**: {numbers if metrics slide}
- **Speaker notes**: "{exact text}"
- **Duration**: {n} min
- **Act**: {act number}

---

[Repeat for each slide]

---

## Screenshots to capture

| Slide | Screenshot | Source | Status |
|-------|-----------|--------|--------|
| {n} | {description} | {tool/URL} | To capture / Available |
```

## kimi-prompt.md

Заповніть шаблон `templates/kimi-prompt-template.md` вмістом доповіді.

Обов'язкові розділи для заповнення:
- Повна назва й підзаголовок
- Ім'я доповідача + подія + дата + тривалість + мова + кількість слайдів
- Вимоги до дизайну (змініть кольорову палітру, якщо вона відрізняється від типової)
- Структура вмісту слайдів (розділ за розділом, усі 5 дій)
- Плейсхолдери скриншотів (слайди, що чекають на реальні знімки)
- Орієнтир тону (адаптуйте до стилю доповіді)

**Переконайтеся, що у фінальному файлі не лишилося жодного `{PLACEHOLDER}`**, перш ніж передати його користувачу.

## Правила побудови сценарію

- **1 ідея на слайд**: ні більше, ні менше
- **Нотатки доповідача = те, що ви говорите, а не те, що читаєте**: мінімальні слайди, розмовні нотатки
- **Числа є героями**: метрики з'являються великими й самі на своєму слайді
- **Анекдоти > пояснення**: «одного вівторка вранці 3 баги...» > «git worktrees уможливлюють паралелізм»
- **Явні переходи**: зазначайте у нотатках зв'язок між кожною дією
- **Реалістичний таймінг**: додайте 10% запасу загалом (слайди завжди затягуються)

## Антипатерни

- Слайди, перевантажені списками (ніколи більше 5 слів у рядку)
- Нотатки доповідача технічним жаргоном (прочитайте їх уголос для перевірки)
- Розмитий промпт для Kimi («зроби гарно»): кожен слайд має бути точним
- Пропуск плейсхолдерів скриншотів у промпті для Kimi
- Генерація більшої кількості слайдів, ніж дозволяє тривалість (2-3 хв/слайд для REX)

## Контрольний список валідації

- [ ] Пітч охоплює 5 дій із узгодженим таймінгом (у межах 10% від цільової тривалості)
- [ ] Кожен слайд має візуал + текст + нотатки доповідача
- [ ] Ключові моменти визначено (паузи, пуанти, переходи)
- [ ] Специфікацію слайдів готово передати дизайнеру
- [ ] Промпт для Kimi повний (усі розділи шаблону заповнено)
- [ ] Скриншоти для зйомки перелічено з джерелом
- [ ] У kimi-prompt.md не лишилося `{PLACEHOLDER}`
- [ ] 3 файли збережено

## Використання промпту для Kimi

1. Відкрийте `{slug}-kimi-prompt.md`
2. Переконайтеся, що не лишилося жодного `{PLACEHOLDER}` (пошукайте у файлі)
3. Перейдіть на [kimi.com](https://kimi.com) (безкоштовний обліковий запис, API не потрібен)
4. Почніть нову розмову
5. Скопіюйте й вставте весь промпт
6. Kimi згенерує презентацію

Для ітеративного доопрацювання додавайте подальші повідомлення, націлені на конкретні слайди. «Слайд 7: збільши число, прибери список.»

## Поради

- Нотатки доповідача є серцем цього етапу; саме вони відрізняють добру доповідь від добре зробленої колоди слайдів
- Шаблон Kimi містить темну дизайн-систему з помаранчевими акцентними кольорами. Адаптуйте `Color Palette` у шаблоні, якщо ваш бренд має інші кольори
- У першому проході генеруйте більше слайдів, ніж потрібно, а потім скорочуйте (легше, ніж писати з нуля)

## Шаблони

- Промпт для Kimi: [`templates/kimi-prompt-template.md`](templates/kimi-prompt-template.uk.md)

## Пов'язане

- [Етап 4: Position](../stage-4-position/SKILL.uk.md): передумова (потрібен CHECKPOINT)
- [Етап 6: Revision](../stage-6-revision/SKILL.uk.md): читає pitch + slides
- [Оркестратор](../orchestrator/SKILL.uk.md)
