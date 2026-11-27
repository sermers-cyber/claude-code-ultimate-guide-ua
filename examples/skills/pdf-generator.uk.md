---
name: pdf-generator
description: Створення професійних PDF на стеку Quarto/Typst із сучасним дизайн-шаблоном
effort: low
version: 1.0.0
---

# Skill «Генератор PDF»

Створюйте професійні PDF із сучасною типографікою за допомогою Quarto + Typst.

## Призначення skill

Цей skill допомагає з:
- Налаштуванням проєктів Quarto/Typst
- Створенням шаблонів документів
- Генерацією PDF із Markdown
- Усуненням проблем із рендерингом
- Налаштуванням дизайн-систем

## Стек

| Інструмент | Версія | Роль |
|------|---------|------|
| **Quarto** | ≥1.4.0 | Рушій рендерингу документів |
| **Typst** | 0.13.0 | Сучасна типографіка (інтегрований) |
| **Pandoc** | 3.x | Конвертація Markdown (інтегрований) |

### Конвеєр генерації

```
  SOURCE              OUTIL           TEMPLATE              OUTPUT
  ──────              ─────           ────────              ──────

  .qmd  ──────────► Quarto ────► --to whitepaper-typst ──► Typst 0.13 ──► .pdf ✅
  (Markdown           │           (_extensions/               (~270K–1.7M,
  + YAML)             │            typst-template.typ)         stylé)
                      │
                      └──────► --to epub ──► Pandoc ──────────────────► .epub
                                             + epub-styles.css

  ⚠️  --to pdf (sans template) → PDF petit, non stylé → Toujours préférer --to whitepaper-typst
```

### Доступні формати

```
  ┌──────────────────────┬────────────────────────┬──────────────────┐
  │ Format               │ Commande               │ Sortie           │
  ├──────────────────────┼────────────────────────┼──────────────────┤
  │ PDF stylé ✅         │ --to whitepaper-typst  │ ~270K–1.7M       │
  │ PDF standard ❌      │ --to pdf               │ ~80-190K, brut   │
  │ EPUB                 │ --to epub              │ epub-output/     │
  └──────────────────────┴────────────────────────┴──────────────────┘
```

## Швидкий старт

### Встановлення

```bash
# macOS
brew install quarto

# Linux
wget https://github.com/quarto-dev/quarto-cli/releases/download/v1.4.555/quarto-1.4.555-linux-amd64.deb
sudo dpkg -i quarto-1.4.555-linux-amd64.deb

# Windows
winget install Posit.Quarto
```

### Генерація PDF

```bash
# Single file
quarto render document.qmd

# All files
quarto render *.qmd

# Preview with hot-reload
quarto preview document.qmd
```

## Шаблон YAML frontmatter

```yaml
---
title: "Document Title"
subtitle: "Optional subtitle"
author: "Author Name"
date: 2026-01-17
date-format: "MMMM YYYY"
format:
  typst:
    toc: true
    toc-depth: 2
    section-numbering: "1.1"
lang: en
---
```

### Доступні параметри

| Параметр | Тип | Опис |
|-----------|------|-------------|
| `title` | string | Головний заголовок (титульна сторінка) |
| `subtitle` | string | Необов'язковий підзаголовок |
| `author` | string | Автор(и) |
| `date` | date | Формат ISO (YYYY-MM-DD) |
| `date-format` | string | Формат відображення (`MMMM YYYY`) |
| `toc` | boolean | Показати зміст |
| `toc-depth` | number | Глибина змісту (1-3) |
| `section-numbering` | string | Формат (`1.1`, `1.a`) |
| `lang` | string | Мова (`fr`, `en`) |

## Структура проєкту

```
project/
├── _extensions/
│   └── custom-template/
│       ├── _extension.yml      # Extension metadata
│       ├── typst-template.typ  # Main template
│       └── typst-show.typ      # Quarto → Typst bridge
├── document.qmd                # Source file
└── document.pdf                # Generated output
```

## Синтаксис Markdown

### Розриви сторінок

```markdown
{{< pagebreak >}}
```

### Блоки коду

Стандартні fenced-блоки з підсвічуванням синтаксису:

````markdown
```bash
npm install
```
````

### Таблиці

```markdown
| Column A | Column B |
|----------|----------|
| Value 1  | Value 2  |
```

### Зображення

```markdown
![Caption](path/to/image.png){width=50%}
```

## Власний шаблон

### Конфігурація extension

Створіть `_extensions/mytemplate/_extension.yml`:

```yaml
title: My Template
author: Your Name
version: 1.0.0
contributes:
  formats:
    typst:
      template: typst-template.typ
      template-partials:
        - typst-show.typ
```

### Дизайн-система (Typst)

```typst
// Colors (Slate + Indigo palette)
#let primary = rgb("#0f172a")      // Slate 900 - titles
#let secondary = rgb("#334155")    // Slate 700 - subtitles
#let accent = rgb("#6366f1")       // Indigo 500 - accents
#let muted = rgb("#64748b")        // Slate 500 - metadata
#let light-bg = rgb("#f8fafc")     // Slate 50 - code bg
#let border-light = rgb("#e2e8f0") // Slate 200 - borders
```

### Типографіка

```typst
#set text(
  font: ("Inter", "Helvetica Neue", "Arial"),
  size: 11pt,
)

#set par(
  leading: 0.75em,
  justify: true,
)

// Code blocks
#show raw.where(block: true): it => {
  block(
    fill: light-bg,
    stroke: (left: 3pt + accent),
    inset: 10pt,
    radius: 4pt,
    it,
  )
}
```

### Callout-блоки

```typst
#let info(title: "Note", body) = {
  block(
    fill: rgb("#E0F2FE"),
    stroke: (left: 3pt + rgb("#0284C7")),
    inset: 12pt,
    [*#title*: #body]
  )
}

#let warning(title: "Warning", body) = {
  block(
    fill: rgb("#FEF3C7"),
    stroke: (left: 3pt + rgb("#D97706")),
    inset: 12pt,
    [*#title*: #body]
  )
}

#let success(title: "Success", body) = {
  block(
    fill: rgb("#DCFCE7"),
    stroke: (left: 3pt + rgb("#16A34A")),
    inset: 12pt,
    [*#title*: #body]
  )
}

#let danger(title: "Danger", body) = {
  block(
    fill: rgb("#FEE2E2"),
    stroke: (left: 3pt + rgb("#DC2626")),
    inset: 12pt,
    [*#title*: #body]
  )
}
```

## Усунення несправностей

### Швидка валідація

```bash
# Check Quarto version
quarto --version  # >= 1.4.0

# Verify extension exists
ls _extensions/*/

# Validate code block pairs (must be even)
grep -c '^```' document.qmd

# Check encoding
file -i document.qmd  # Must show utf-8
```

### Поширені проблеми

| Проблема | Причина | Рішення |
|-------|-------|-----|
| Вкладені блоки коду ламаються | Внутрішній ` ``` ` закриває зовнішній | Використовуйте 4+ зворотні лапки для зовнішнього |
| Таблиці відображаються як код | Вище є непарний ` ``` ` | Перевірте кількість роздільників |
| Extension не знайдено | Неправильний каталог | Перевірте шлях `_extensions/` |
| Попередження про шрифти | Шрифти не встановлено | Це нормально; використовуються запасні |
| Спотворені символи | Неправильне кодування | Конвертуйте в UTF-8 |

### Вкладені блоки коду

Використовуйте більше зворотних лапок для зовнішнього блоку:

`````markdown
````markdown
# This is the outer block

```bash
echo "This is nested"
```

Outer continues...
````
`````

### Скрипт валідації

```bash
#!/bin/bash
for f in *.qmd; do
  count=$(grep -c '^```' "$f")
  if [ $((count % 2)) -ne 0 ]; then
    echo "ERROR: $f has odd count ($count)"
  fi
done
```

### Повний конвеєр валідації

```bash
#!/bin/bash
# validate-qmd.sh

echo "=== Validating QMD files ==="
errors=0

for f in *.qmd; do
  # Check code block pairs
  count=$(grep -c '^```' "$f")
  if [ $((count % 2)) -ne 0 ]; then
    echo "ERROR: $f - odd code block count ($count)"
    ((errors++))
  fi

  # Check UTF-8
  encoding=$(file -i "$f" | grep -o 'charset=[^;]*')
  if [[ "$encoding" != *"utf-8"* ]]; then
    echo "WARNING: $f - encoding is $encoding"
  fi
done

echo "=== Validation complete: $errors errors ==="
exit $errors
```

## Приклади використання

### Технічна документація

```yaml
---
title: "API Reference"
subtitle: "v2.0"
author: "Engineering Team"
date: 2026-01-17
format:
  typst:
    toc: true
    toc-depth: 3
---

# Authentication

All requests require an API key...
```

### Серія whitepaper

```yaml
---
title: "Security Best Practices"
series: "Engineering Whitepapers"
wp-number: "03"
author: "Security Team"
date: 2026-01-17
format:
  whitepaper-typst:
    toc: true
---
```

### Внутрішній звіт

```yaml
---
title: "Q1 Performance Report"
author: "Analytics Team"
date: 2026-01-17
date-format: "Q1 YYYY"
format:
  typst:
    toc: false
---
```

## Ресурси

- [Quarto Documentation](https://quarto.org/docs/guide/)
- [Typst Documentation](https://typst.app/docs/)
- [Quarto + Typst Guide](https://quarto.org/docs/output-formats/typst.html)
- [Робочий процес](../../guide/workflows/pdf-generation.uk.md)