# Шаблон для Twitter/X

Два режими: один твіт (280 символів) або тред (2-3 твіти).

## Один твіт

Використовуйте, коли: 1-2 акценти, просте оновлення версії.

### Шаблон FR

```
{hook_line_fr}

{highlight_fr}

{link}
```

### Шаблон EN

```
{hook_line_en}

{highlight_en}

{link}
```

### Правила

- Макс. 280 символів загалом (включно з посиланням)
- Макс. 2 емодзі
- Посилання на репозиторій GitHub
- FR: звертання на «ти» (tutoiement)
- EN: пряме звертання

## Тред (2-3 твіти)

Використовуйте, коли: 3+ акценти, насичена версія/тиждень.

### Шаблон FR

```
Tweet 1/N:
{hook_line_fr}

{context_fr}

Thread [down_arrow]

---

Tweet 2/N:
{highlight_1_fr}
{highlight_2_fr}

---

Tweet 3/N (optional):
{highlight_3_fr}

{cta_fr}
{link}
```

### Шаблон EN

```
Tweet 1/N:
{hook_line_en}

{context_en}

Thread [down_arrow]

---

Tweet 2/N:
{highlight_1_en}
{highlight_2_en}

---

Tweet 3/N (optional):
{highlight_3_en}

{cta_en}
{link}
```

## Правила для полів

### hook_line (макс. 100 символів)

Найкоротша форма найкращого акценту. Має вміщатися в перший твіт разом з контекстом.

| Патерн | FR | EN |
|---------|-----|-----|
| З числа | `30 nouvelles questions quiz Claude Code` | `30 new Claude Code quiz questions` |
| Прямий | `Nouveau guide : sandbox isolation Docker` | `New guide: Docker sandbox isolation` |

### context (макс. 80 символів)

```
FR: "Guide v3.20.5 vient de sortir"
EN: "Guide v3.20.5 just dropped"
```

### highlights (макс. 120 символів кожен)

Перетворені записи, по одному на рядок. Без маркерів (використовуйте розриви рядків).

```
FR: "4 diagrammes ASCII pour TDD, UVAL, securite"
EN: "4 ASCII diagrams for TDD, UVAL, security"
```

### cta (макс. 60 символів)

```
FR: "Tout est open source"
EN: "All open source"
```

### link

URL репозиторію GitHub. Враховується в ліміт 280 символів (23 символи для t.co).

## Рішення: один твіт чи тред

| Умова | Формат |
|-----------|--------|
| 1-2 акценти, усе вміщається в 280 символів | Один твіт |
| 3+ акценти або насичений контент | Тред (2-3 твіти) |
| Тиждень із кількома версіями | Тред |
| Лише зміни щодо супроводу | Один твіт (або пропустити) |

## Обмеження

- Кожен твіт: макс. 280 символів
- Бюджет емодзі: 2 на весь тред
- Без гіпе-слів
- FR: звертання на «ти» (tutoiement)
- EN: американська англійська
- Максимум у треді: 3 твіти (не 5+)
