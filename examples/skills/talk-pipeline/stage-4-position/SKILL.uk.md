---
name: talk-stage4-position
description: "Генерує 3-4 стратегічні ракурси доповіді з аналізом сильних і слабких сторін, варіанти назв, описи для CFP і чернетку відгуку від колег, а потім вимагає обов'язкового CHECKPOINT для підтвердження користувачем перед написанням сценарію. Використовуйте, коли вирішуєте, як подати доповідь, готуєте заявку на CFP або обираєте між кількома наративними ракурсами."
allowed-tools: Write Read AskUserQuestion
effort: high
---

# Етап 4 доповіді: Position + CHECKPOINT

Генерує стратегічні ракурси, назви, описи й чернетку для відгуку від колег. Потім **зупиняється й чекає** на ваш вибір ракурсу й назви, перш ніж етап 5 зможе продовжити.

## Коли використовувати цей skill

- Після етапу 3 (Concepts), що надає каталог концепцій
- Коли вирішуєте, як подати доповідь
- Перед надсиланням CFP (безпосередньо використовує згенеровані описи)

## Що робить цей skill

1. **Читає вхідні дані**: підсумок + концепції + обмеження події
2. **Генерує ракурси**: 3-4 різні ракурси з аналізом сильних і слабких сторін
3. **Рекомендує**: один чіткий вибір зі структурованим обґрунтуванням
4. **Генерує назви**: 3-5 варіантів на кожен ракурс
5. **Генерує описи**: короткий анотація + довгий опис для CFP
6. **Генерує чернетку відгуку**: готове до надсилання повідомлення (3 формати)
7. **CHECKPOINT**: показує запит на вибір і чекає на відповідь користувача
8. **Зберігає 4 файли**

## Вхідні дані

- `talks/{YYYY}-{slug}-summary.md` (обов'язково)
- `talks/{YYYY}-{slug}-concepts.md` (обов'язково)
- Обмеження події: тривалість, аудиторія, формат CFP, якщо застосовно

## Вивід

- `talks/{YYYY}-{slug}-angles.md`
- `talks/{YYYY}-{slug}-titre.md`
- `talks/{YYYY}-{slug}-descriptions.md`
- `talks/{YYYY}-{slug}-feedback-draft.md`

## Формат angles.md

```markdown
# Talk Angles: {provisional title}

**Goal**: Choose the angle that maximizes impact for {audience}.
**Audience**: {audience description}

---

## Angle 1: {Angle name}

**Pitch**: {2-3 sentences describing the talk from this angle}

**Strengths**:
- {strength 1}
- {strength 2}

**Weaknesses**:
- {weakness 1}
- {weakness 2}

**Audience fit**: Strong / Medium / Weak ({short justification})

**Verdict**: (out of 5 stars)

---

[Angle 2, Angle 3, (optional Angle 4): same structure]

---

## Recommendation: Angle {X}, enriched by the others

**Angle {X} is the right choice.** Here's why:

### 1. It's the only angle that integrates the others
[Structure showing how other angles feed into the main one]

### 2. The narrative arc is natural and compelling
[Why the story holds better with this angle]

### 3. The metrics lend credibility throughout
[Which metrics support this angle most]

### 4. The final message emerges naturally
[How the conclusion flows from this angle]

---

## Recommended structure with sub-angles

| Act | Duration | Main angle | Integrated sub-angle |
|-----|----------|-----------|---------------------|
| 1. {name} | {n} min | {main angle} | {sub-angle} |
...
```

## Формат titre.md

```markdown
# Titles: Talk {slug}

**Selected angle**: Angle {X} ({name})
**Constraints**: {duration} min | {audience}

---

## Titles for the recommended angle

### Option 1 (recommended)
**{Main title}**
*Optional subtitle: {subtitle}*

Strengths: {why this title works}
Audience appeal: {who it hooks}

### Option 2
**{Title}**
Strengths: {strengths}

[Options 3-5]

---

## Titles for alternative angles (backup)

### If Angle 2 chosen
- **{title}**
- **{title}**

[If Angle 3 chosen: same structure]

---

## Verdict

**Recommendation**: Option 1 ("{title}")
**Why**: {short justification}
```

## Формат descriptions.md

```markdown
# Descriptions: Talk {slug}

---

## Short description (abstract, ~100 words)

{Full text: direct, engaging, starts with the impact or concrete promise.
Not "In this talk, we will..."}

---

## Long description (CFP, ~250 words)

{Full text: context, what the audience will learn, who it's for.
Includes key metrics if available.
Direct and factual tone.}

---

## Speaker pitch (bio-ready, ~50 words)

{Speaker introduction in 1-2 sentences, their relationship to the topic}

---

## Tags / Keywords

{5-10 relevant tags for CFP or search}
```

## CHECKPOINT (обов'язковий, крок 7)

Після генерації й збереження 4 файлів покажіть:

```
---
CHECKPOINT: Angle + Title choice

I've generated 4 files:
- talks/{YYYY}-{slug}-angles.md    -> {n} angles analyzed
- talks/{YYYY}-{slug}-titre.md     -> {n} title options
- talks/{YYYY}-{slug}-descriptions.md
- talks/{YYYY}-{slug}-feedback-draft.md

Before starting the script (Stage 5), I need your choice:

1. Which angle do you choose? (recommended: Angle {X}, {name})
2. Which title do you prefer? (recommended: "{title}")

You can also modify, combine, or propose something different.
Reply to start the script.
---
```

**Не запускайте етап 5 без явного підтвердження користувача.**

## Правила генерації ракурсів

- Мінімум 3 ракурси, максимум 4 (більше вже шум)
- Кожен ракурс має бути справді відмінним (а не варіаціями одного)
- Рекомендація має бути чіткою й аргументованою, а не «вибір за вами»
- Завжди перевіряйте: «чи витримає цей ракурс усю тривалість без повторів?»

## Антипатерни

- Клікбейтні назви («Що ніхто не розповідає про ШІ»)
- Рекомендація останнього в списку ракурсу за замовчуванням (ефект новизни)
- Описи, що читаються як підсумки слайдів
- Пропуск CHECKPOINT (це найважливіша контрольна точка конвеєра)
- Маркетингова мова в описах (революційний тощо)

## Контрольний список валідації

- [ ] 3-4 ракурси з аналізом сильних/слабких сторін і відповідності аудиторії
- [ ] Чітка рекомендація зі структурованим обґрунтуванням
- [ ] 3-5 назв для рекомендованого ракурсу
- [ ] Короткий опис (~100 слів) і довгий опис (~250 слів)
- [ ] Чернетку відгуку згенеровано за шаблоном
- [ ] CHECKPOINT чітко показано
- [ ] 4 файли збережено

## Поради

- Надішліть `feedback-draft.md` колезі перед checkpoint; 10 хвилин зовнішнього відгуку можуть заощадити години переробки сценарію
- Рекомендація є відправною точкою, а не наказом (ваше знання аудиторії важливіше за будь-яку алгоритмічну пропозицію)
- Слабкі назви зазвичай надто абстрактні: перевіряйте кожну назву питанням «чи зупиниться хтось у коридорі, щоб це прочитати?»

## Шаблони

- Формати відгуку від колег: [`templates/feedback-draft.md`](templates/feedback-draft.uk.md)

## Пов'язане

- [Етап 3: Concepts](../stage-3-concepts/SKILL.uk.md): передумова
- [Етап 5: Script](../stage-5-script/SKILL.uk.md): починається після цього CHECKPOINT
- [Оркестратор](../orchestrator/SKILL.uk.md)
