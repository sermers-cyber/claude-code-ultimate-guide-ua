---
title: "PDF Generation with Claude Code"
description: "Generate professional PDFs using Claude Code with Quarto and Typst stack"
tags: [workflow, guide, integration]
---

# PDF Generation з Claude Code

> **Confidence**: Tier 2 — На основі перевіреного на практиці воркфлоу зі стеком Quarto/Typst.

Генеруйте професійні PDF-файли (документацію, технічні звіти, аналітику) за допомогою Claude Code з використанням сучасної типографіки та дизайну.

---

## Table of Contents

1. [TL;DR](#tldr)
2. [When to Use](#when-to-use)
3. [Stack Overview](#stack-overview)
4. [Setup](#setup)
5. [Workflow](#workflow)
6. [Integration with Claude Code](#integration-with-claude-code)
7. [Customization](#customization)
8. [Troubleshooting](#troubleshooting)
9. [See Also](#see-also)

---

## TL;DR

```bash
# Install
brew install quarto  # macOS

# Generate
quarto render document.qmd  # → document.pdf

# Preview
quarto preview document.qmd  # Hot-reload
```

**Стек**: Quarto (оркестрація) + Typst (типографіка) + Pandoc (markdown)

---

## When to Use

| Use Case | Good Fit | Alternative |
|----------|----------|-------------|
| Технічна документація | ✅ | — |
| Звіти / Аналітика | ✅ | — |
| API-документація | ⚠️ | OpenAPI + Redoc |
| Слайди / Презентації | ⚠️ | Quarto Revealjs |
| Швидкі нотатки | ❌ | Plain Markdown |
| Спільне редагування | ❌ | Google Docs, Notion |

**Найкраще підходить для**: Великих технічних документів, які потребують професійної розмітки, версіонування (version control) та відтворюваності.

---

## Stack Overview

```
┌─────────────────────────────────────────────────┐
│                  Your .qmd File                 │
│         (Markdown + YAML frontmatter)           │
└─────────────────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────┐
│                    Quarto                       │
│           (Document rendering engine)           │
│         • Processes YAML metadata               │
│         • Handles extensions                    │
│         • Manages output formats                │
└─────────────────────────────────────────────────┘
                        │
          ┌─────────────┴─────────────┐
          ▼                           ▼
┌─────────────────────┐    ┌─────────────────────┐
│       Pandoc        │    │       Typst         │
│   (MD → AST → ?)    │    │  (Typography/PDF)   │
│  • Markdown parser  │    │  • Modern engine    │
│  • Fast compilation │    │  • No LaTeX needed  │
│  • Format bridges   │    │                     │
└─────────────────────┘    └─────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────┐
│                  document.pdf                   │
│        (Professional typography output)         │
└─────────────────────────────────────────────────┘
```

### Output Formats & Commands

```
  FORMAT                COMMANDE                      SORTIE
  ──────                ────────                      ──────

  PDF standard    →  quarto render doc.qmd            doc.pdf
                      --to typst                       (sans template custom)

  PDF stylé ✅    →  quarto render doc.qmd            doc.pdf
                      --to whitepaper-typst            (~270K–1.7M, Bold Guy)
                      (format custom via _extensions/)

  EPUB            →  quarto render doc.qmd            doc.epub
                      --to epub

  Preview         →  quarto preview doc.qmd           hot-reload navigateur
```

### Extension Structure

```
  _extensions/
  └── whitepaper/
      ├── _extension.yml       ← déclare le format "whitepaper-typst"
      ├── typst-template.typ   ← design system (couleurs, typo, callouts)
      └── typst-show.typ       ← bridge Quarto → Typst

  ⚠️  Si tu maintiens des copies dans fr/ en/ et racine :
      garder les 3 fichiers typst-template.typ synchronisés
```

### Troubleshooting Rapide

```
  SYMPTÔME                        CAUSE                    FIX
  ────────                        ─────                    ───
  PDF petit (~80-190K), non stylé  --to pdf au lieu de      Utiliser --to whitepaper-typst
                                   --to whitepaper-typst

  Erreur "bibliography"            @ref dans titre callout   Supprimer le @ du titre
                                   → interprété comme cit.

  Table rendue comme code          Backtick ``` non fermé    Compter les ``` (doit être pair)

  "Extension not found"            Mauvais répertoire        Vérifier _extensions/ path
```

| Component | Version | Role |
|-----------|---------|------|
| **Quarto** | ≥1.4.0 | Оркестрація, розширення, підтримка кількох форматів |
| **Typst** | 0.13.0 | Сучасна типографіка (замінює LaTeX) |
| **Pandoc** | 3.x | Парсинг Markdown (входить до складу Quarto) |

---

## Setup

### Installation

**macOS**:
```bash
brew install quarto
```

**Linux (Debian/Ubuntu)**:
```bash
wget https://github.com/quarto-dev/quarto-cli/releases/download/v1.4.555/quarto-1.4.555-linux-amd64.deb
sudo dpkg -i quarto-1.4.555-linux-amd64.deb
```

**Windows**:
```powershell
winget install Posit.Quarto
```

**Verify**:
```bash
quarto --version  # Має бути ≥1.4.0
```

### Project Structure

```
project/
├── _extensions/           # Розширення Quarto (шаблони)
│   └── custom-template/
│       ├── _extension.yml
│       ├── typst-template.typ
│       └── typst-show.typ
├── documents/
│   ├── guide.qmd          # Вихідний файл
│   └── guide.pdf          # Згенерований результат
└── assets/
    └── logo.png           # Спільні ресурси
```

### Minimal Document

Створіть `document.qmd`:

```yaml
---
title: "My Document"
author: "Author Name"
date: 2026-01-17
format:
  typst:
    toc: true
lang: en
---

# Introduction

Your content here...

## Section 1

More content with **bold** and `code`.

```bash
echo "Code blocks work!"
```

## Section 2

| Column A | Column B |
|----------|----------|
| Data 1   | Data 2   |
```

Згенеруйте PDF:
```bash
quarto render document.qmd  # Створює document.pdf
```

---

## Workflow

### 1. Content-First Approach

```
1. Write content in Markdown (.qmd)
2. Add YAML frontmatter for metadata
3. Preview with hot-reload
4. Generate final PDF
5. Version control both source and PDF
```

### 2. Available YAML Parameters

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `title` | string | Головний заголовок | `"Technical Guide"` |
| `subtitle` | string | Підзаголовок | `"v2.0 Edition"` |
| `author` | string/array | Автор(и) | `"John Doe"` |
| `date` | date | Дата документа | `2026-01-17` |
| `date-format` | string | Формат показу дати | `"MMMM YYYY"` |
| `toc` | boolean | Зміст (Table of contents) | `true` |
| `toc-depth` | number | Глибина змісту (1-3) | `2` |
| `lang` | string | Мова документа | `fr` або `en` |
| `section-numbering` | string | Формат нумерації розділів | `"1.1"` |

### 3. Markdown Features

**Page Breaks (Розриви сторінок)**:
```markdown
{{< pagebreak >}}
```

**Code Blocks (Кодові блоки)** (із підсвічуванням синтаксису):
````markdown
```typescript
function hello(): string {
  return "world";
}
```
````

**Tables (Таблиці)**:
```markdown
| Feature | Supported |
|---------|-----------|
| Tables  | ✅        |
| Images  | ✅        |
| Links   | ✅        |
```

**Images (Зображення)**:
```markdown
![Alt text](path/to/image.png){width=50%}
```

---

## Integration with Claude Code

### Using the pdf-generator Skill

Викличте навичку (skill) для покрокової генерації PDF:

```
/pdf-generator
```

Навичка надає:
- Шаблон із метаданими YAML frontmatter
- Налаштування системи дизайну (design system)
- Поради щодо вирішення поширених проблем
- Команди генерації

### Prompt Examples

**Згенерувати документацію**:
```
Create a technical guide for our API as a Quarto document.
Use the Typst format with a table of contents.
Include sections for: Authentication, Endpoints, Error Codes.
```

**Конвертувати існуючий Markdown**:
```
Convert README.md to a professional PDF.
Add a cover page with title and date.
Use Quarto/Typst format.
```

**Створити шаблон**:
```
Create a Quarto extension for our company's document style:
- Logo in header
- Custom colors: primary #0f172a, accent #6366f1
- Inter font for body, JetBrains Mono for code
```

### With Plan Mode

Для складних документів:
```
[Press Shift+Tab to enter Plan Mode]

I need to create a series of 5 technical whitepapers.
Plan the structure:
1. Common template/extension
2. Shared assets
3. Build automation
4. Version management
```

### With Hooks

Автоматично генеруйте PDF після редагувань за допомогою hook'а `PostToolUse`:

```json
// In .claude/settings.json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "command": "if echo \"$TOOL_INPUT\" | grep -q '.qmd'; then quarto render \"$FILE\"; fi"
      }
    ]
  }
}
```

---

## Customization

### Custom Template Extension

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

### Typst Template Variables

У файлі `typst-template.typ`:

```typst
// Colors
#let primary = rgb("#0f172a")      // Dark text
#let secondary = rgb("#334155")    // Lighter text
#let accent = rgb("#6366f1")       // Highlights

// Typography
#set text(
  font: ("Inter", "Helvetica Neue", "Arial"),
  size: 11pt,
)

#set par(
  leading: 0.75em,  // Line height
  justify: true,
)

// Code blocks
#show raw.where(block: true): it => {
  block(
    fill: rgb("#f8fafc"),
    stroke: (left: 3pt + accent),
    inset: 10pt,
    radius: 4pt,
    it,
  )
}
```

### Callout Boxes

Визначте в шаблоні:

```typst
#let info(title: "Note", body) = {
  block(
    fill: rgb("#E0F2FE"),
    stroke: (left: 3pt + rgb("#0284C7")),
    inset: 12pt,
    radius: 4pt,
    [*#title*: #body]
  )
}

#let warning(title: "Warning", body) = { ... }
#let success(title: "Success", body) = { ... }
#let danger(title: "Danger", body) = { ... }
```

Використовуйте у документі:
```typst
#info[This is an informational note.]
#warning(title: "Attention")[Check your configuration.]
```

---

## Troubleshooting

### Quick Checks

```bash
# Verify Quarto
quarto --version

# Check extension exists
ls _extensions/*/

# Validate code block pairs (must be even)
grep -c '^```' document.qmd

# Check encoding
file -i document.qmd  # Should show utf-8
```

### Common Issues

| Issue | Symptom | Fix |
|-------|---------|-----|
| Вкладені кодові блоки | Вміст виривається з блоку | Використовуйте 4+ бектреки для зовнішнього блоку |
| Таблиці як код | Сірий фон | Перевірте непарний символ ` ``` ` вище |
| Відсутнє розширення | "Extension not found" | Перевірте правильність шляху `_extensions/` |
| Попередження про шрифти | "unknown font family" | Це нормально; використовуються альтернативи |
| Зламані спецсимволи | `?` або спотворення тексту | Конвертуйте файл у UTF-8 |

### Nested Code Blocks

**Проблема**: Внутрішній кодовий блок передчасно закриває зовнішній блок.

**Рішення**: Використовуйте більше бектреків (backticks) для зовнішнього блоку:

`````markdown
````markdown
# Outer block with 4 backticks

```bash
echo "Inner block with 3 backticks"
```

Outer block continues...
````
`````

### Validation Script

```bash
#!/bin/bash
# validate-qmd.sh

for f in *.qmd; do
  count=$(grep -c '^```' "$f")
  if [ $((count % 2)) -ne 0 ]; then
    echo "ERROR: $f has odd code block count ($count)"
  fi
done
```

---

## See Also

- [Quarto Documentation](https://quarto.org/docs/guide/)
- [Typst Documentation](https://typst.app/docs/)
- [Quarto + Typst Guide](https://quarto.org/docs/output-formats/typst.html)
- [examples/skills/pdf-generator.md](../../examples/skills/pdf-generator.md) — Шаблон навички
- [whitepapers/README.md](../../whitepapers/README.md) — Реальний приклад використання

---
**Локалізація**: [Serhii (MacPlus Software)](https://macplus-software.com)
*Остання синхронізація: Травень 2026*
