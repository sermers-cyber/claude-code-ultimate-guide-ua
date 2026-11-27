# Шаблон Twitter/X

Два режими: один твіт (280 символів) або тред (2-3 твіти).

## Один твіт

Використовуй, коли: 1-2 головні події, просте оновлення версії.

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

- Макс. 280 символів загалом (разом із посиланням)
- Макс. 2 емодзі
- Посилання на репозиторій GitHub
- FR: звертання на "tu"
- EN: пряме звертання

## Тред (2-3 твіти)

Використовуй, коли: 3+ головні події, багата версія/тиждень.

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

## Правила полів

### hook_line (макс. 100 символів)

Найкоротша форма головної події. Має поміститися в перший твіт разом із контекстом.

| Шаблон | FR | EN |
|--------|-----|-----|
| З числа | `30 nouvelles questions quiz Claude Code` | `30 new Claude Code quiz questions` |
| Прямо | `Nouveau guide : sandbox isolation Docker` | `New guide: Docker sandbox isolation` |

### context (макс. 80 символів)

```
FR: "Guide v3.20.5 vient de sortir"
EN: "Guide v3.20.5 just dropped"
```

### highlights (макс. 120 символів кожна)

Перетворені записи, по одному в рядок. Без маркерів (використовуй розриви рядків).

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
|-------|--------|
| 1-2 головні події, усе вміщується в 280 символів | Один твіт |
| 3+ головні події або багатий вміст | Тред (2-3 твіти) |
| Тиждень з кількома версіями | Тред |
| Лише зміни щодо супроводу | Один твіт (або пропустити) |

## Обмеження

- Кожен твіт: макс. 280 символів
- Бюджет емодзі: 2 на весь тред
- Без гучних слів
- FR: звертання на "tu"
- EN: американська англійська
- Тред максимум: 3 твіти (не 5+)
