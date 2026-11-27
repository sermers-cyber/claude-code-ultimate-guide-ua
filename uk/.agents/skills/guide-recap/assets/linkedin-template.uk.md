# Шаблон LinkedIn

Ціль: ~1300 символів. Структура: гачок + контекст + пункти + CTA + хештеги.

## Шаблон FR

```
{hook_line_fr}

{context_line_fr}

{bullet_1_fr}
{bullet_2_fr}
{bullet_3_fr}

{cta_fr}

#ClaudeCode #CodingWithAI #DeveloperTools
```

## Шаблон EN

```
{hook_line_en}

{context_line_en}

{bullet_1_en}
{bullet_2_en}
{bullet_3_en}

{cta_en}

#ClaudeCode #CodingWithAI #DeveloperTools
```

## Правила полів

### hook_line (1 рядок, макс. 150 символів)

Найвище оцінена головна подія, перетворена на цінність для користувача. Може містити 0-1 емодзі.

| Шаблон | Приклад FR | Приклад EN |
|--------|------------|------------|
| З числа | `30 nouvelles questions quiz pour tester vos connaissances Claude Code` | `30 new quiz questions to test your Claude Code knowledge` |
| Запитання | `Vous apprenez mieux en visuel ? 4 nouveaux diagrammes ASCII` | `Visual learner? 4 new ASCII diagrams just added` |
| З джерела | `Pat Cullen partage son workflow de code review multi-agent` | `Pat Cullen shares his multi-agent code review workflow` |

### context_line (1-2 рядки, макс. 200 символів)

Посилання на версію + що змінилося в загальних рисах.

```
FR: "Guide v3.20.5 - mise a jour de la reference visuelle."
EN: "Guide v3.20.5 - visual reference update."
```

Для режиму тижня:
```
FR: "N releases cette semaine dans le Claude Code Ultimate Guide."
EN: "N releases this week in the Claude Code Ultimate Guide."
```

### bullets (3 пункти, кожен макс. 200 символів)

Топ-3 головні події за оцінкою. Кожен починається з відповідного емодзі (макс. 1 на пункт).

```
FR:
- [emoji] [Transformed highlight in vous-form]
- [emoji] [Transformed highlight in vous-form]
- [emoji] [Transformed highlight in vous-form]

EN:
- [emoji] [Transformed highlight, direct "you" address]
- [emoji] [Transformed highlight, direct "you" address]
- [emoji] [Transformed highlight, direct "you" address]
```

### cta (1 рядок, макс. 150 символів)

М'яке твердження про цінність або щире запитання. Містить посилання на сайт лендингу.

```
FR: "Guide complet disponible en open source : {landing_url}"
EN: "Full guide available open source: {landing_url}"
```

### hashtags (1 рядок, рівно 3)

Фіксовані: `#ClaudeCode #CodingWithAI #DeveloperTools`

Додай 1 тематичний тег, якщо він явно доречний: `#CodeReview`, `#Security`, `#TDD`

## Обмеження

- Весь пост: 1100-1500 символів
- Бюджет емодзі: 3-4 загалом (0-1 у гачку, 1 на пункт, 0-1 у CTA)
- Без гучних слів (дивись tone-guidelines.md)
- FR: звертання на "vous"
- EN: американська англійська
