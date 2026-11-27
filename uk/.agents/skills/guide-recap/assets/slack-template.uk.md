# Шаблон Slack

Компактно, зручно для перегляду, багато емодзі. Готово до вставлення.

## Шаблон FR

```
:newspaper: *{title_fr}*

{highlights_fr}

:link: {link}
```

## Шаблон EN

```
:newspaper: *{title_en}*

{highlights_en}

:link: {link}
```

## Правила полів

### title (макс. 60 символів)

```
FR: "Guide v3.20.5 - Reference visuelle"
EN: "Guide v3.20.5 - Visual reference"

FR: "Recap semaine : 4 releases"
EN: "Week recap: 4 releases"
```

### highlights (3-5 рядків)

Кожен рядок: емодзі Slack + короткий опис. Без жирного шрифту в тексті пункту.

```
FR:
:art: 4 nouveaux diagrammes ASCII (TDD, UVAL, securite, incidents)
:brain: 30 nouvelles questions quiz (257 total)
:shield: Guide sandbox isolation Docker
:mag: 9 patterns avances identifies via claudelog.com

EN:
:art: 4 new ASCII diagrams (TDD, UVAL, security, incidents)
:brain: 30 new quiz questions (257 total)
:shield: Docker sandbox isolation guide
:mag: 9 advanced patterns identified via claudelog.com
```

### link

URL репозиторію GitHub.

## Довідник емодзі Slack

Використовуй стандартні емодзі Slack, які відображаються в усіх робочих просторах:

| Емодзі | Код | Для чого |
|--------|-----|----------|
| :newspaper: | `:newspaper:` | Маркер заголовка |
| :art: | `:art:` | Візуальний контент, діаграми, UI |
| :brain: | `:brain:` | Квіз, навчання, знання |
| :shield: | `:shield:` | Контент про безпеку |
| :mag: | `:mag:` | Дослідження, аналіз, конкурентна розвідка |
| :wrench: | `:wrench:` | Інструменти, воркфлоу, конфігурація |
| :books: | `:books:` | Нові посібники, документація |
| :chart_with_upwards_trend: | `:chart_with_upwards_trend:` | Показники зростання |
| :white_check_mark: | `:white_check_mark:` | Виправлення, корекції |
| :link: | `:link:` | Маркер посилання |
| :arrow_right: | `:arrow_right:` | Індикатор зростання (X -> Y) |

## Обмеження

- Макс. 500 символів загалом
- Бюджет емодзі: 4-6 (1 у заголовку + 1 на кожну головну подію + 1 для посилання)
- Без гучних слів
- FR: звертання на "tu"
- EN: американська англійська
- Одне посилання (GitHub)
- Без хештегів (це не конвенція Slack)
- Використовуй форматування Slack: `*bold*`, `_italic_`, коди `:emoji:`
