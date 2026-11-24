# Візуальні промпти для Reviewable agent changes

Ці промпти ілюструють [Reviewable agent changes](../../guide/workflows/reviewable-agent-changes.uk.md): п'ять полів, які нотатка агента фіксує для кожного hunk, і де нотатка може жити та що переживає переписування. Кожен видимий рядок походить із тієї сторінки та тестів за нею (git 2.56.0 і git-ai 1.7.7, 8 листопада 2026). Згенеруйте одне зображення на промпт за допомогою Gemini 3 Pro Image, перед публікацією звірте кожну відтворений підпис із наведеними нижче рядками й конвертуйте вибраний результат у WebP у рідному розмірі.

## Запис вибору

| Опублікований ресурс | Спроба | Статус |
|---|---|---|
| `agent-note-storage.webp` | 1 | Вибрано з першої спроби, пілот: заголовок, підзаголовок, три заголовки стовпців, чотири підписи рядків, дванадцять комірок, нижня смуга та футер збігаються з рядками; зелені та сірі краї на очікуваних комірках; зайвого тексту немає. Gemini повернув дані JPEG розміром 1376 x 768 під іменем `.png`; конвертовано у WebP у рідному розмірі, без збільшення |
| `agent-note-fields.webp` | 2 | Спробу 1 відхилено: значок картки 2 містив зайве слово «Why?», а дві картки мали зелені верхні лінійки замість чорнильних. Спроба 2 (той самий промпт, дефект визнано стохастичним) має всі рядки правильними й без зайвого тексту, але картки 2–5 мали помаранчеві, зелені та жовті верхні лінійки замість чорнильних. Це виправлено локально, а не третім платним викликом: лише насичені пікселі рядків лінійки (рядки 227–238, праворуч від першої картки) змішано в бік чорнильного; у цих рядках немає пікселів тексту. Рідні дані JPEG 1376 x 768, конвертовано у WebP, без збільшення |

## Спільний арт-напрям

Використовуйте теплий кремовий фон у стилі міліметрівки (`#f5f1e8`), ледь помітну сітку (`#d4cfb8`), точні темні лінії чорнила (`#1a1a1a`) і стримані акценти: помаранчевий (`#d97706`), зелений (`#16a34a`) та жовтий (`#fbbf24`), а сірий (`#9ca3af`) — для частин, що були прочитані, але не запущені. Не використовуйте фото, 3D, маскотів, декоративні дудли, логотипи компаній, номери сторінок чи зайвий надзаголовок. Весь видимий текст англійською. Не використовуйте довгі тире. Запитуване співвідношення сторін 16:9.

## 1. Де живе нотатка агента

Вивід: `guide/images/agent-note-storage.webp`

Alt-текст: Три місця, де може жити нотатка агента, порівняно за чотирма рядками. Git notes у refs/notes/rationale не видно в merge request, якщо інструмент їх не публікує, вони переживають amend і rebase з notes.rewriteRef (перевірено) і втрачаються при squash-merge для простих нотаток (перевірено). Файл, закомічений разом із кодом, відображається як змінений файл, переміщується разом із вмістом і зберігається при squash з діапазонами рядків, що можуть дрейфувати. Коментар у forge видно в merge request, його позначають застарілим на новому head, а його доля при squash залежить від forge й не перевірялася.

```text
Create ONE clean editorial data infographic for a technical documentation guide, landscape 16:9 at 1600x900. Warm cream graph-paper background (#f5f1e8) with a subtle grid (#d4cfb8), precise dark ink lines (#1a1a1a), restrained orange (#d97706), green (#16a34a) and yellow (#fbbf24) accents, grey (#9ca3af) for cells read but not run. No photos, no 3D, no mascots, no decorative doodles, no company logos, no page number, no pretitle. Do not use em dashes.

Layout: a comparison table with three aligned columns and four labelled rows, read left to right then top to bottom.

Title at top left, large bold sans-serif: "Where an agent note lives, and what survives a rewrite"
Subtitle under the title, regular weight: "Green: tested. Grey: read from source, not run."

Three column headers in bold, each in a flat card with a thin ink border:
Column 1: "Git notes"
Column 2: "File committed with the code"
Column 3: "Forge comment"

Four row labels in small monospace capitals in a narrow left column:
Row 1: "STORED IN"
Row 2: "VISIBLE IN THE MERGE REQUEST"
Row 3: "AMEND AND REBASE"
Row 4: "SQUASH MERGE"

Cells, each a flat card with a thin ink border:
Row 1, column 1: "refs/notes/rationale" in monospace. Row 1, column 2: "SARIF or JSON beside the code". Row 1, column 3: "Merge request discussion".
Row 2, column 1: "No, unless a tool posts it". Row 2, column 2: "As a changed file". Row 2, column 3: "Yes".
Row 3, column 1: "Kept with notes.rewriteRef", with a green left edge. Row 3, column 2: "Moves with the content", with a grey left edge. Row 3, column 3: "Marked outdated on a new head", with a grey left edge.
Row 4, column 1: "Lost for plain notes", with a green left edge. Row 4, column 2: "Kept, line ranges may drift", with a grey left edge. Row 4, column 3: "Depends on the forge", with a grey left edge.
Rows 1 and 2 have no coloured edge.

Bottom strip across the full width, with a small yellow marker, regular weight: "A forge merge button rewrites history on the server: not tested."

Footer at bottom right in small monospace, with a clear margin from the canvas edge: "git 2.56.0 and git-ai 1.7.7, November 8, 2026"

Colour names, layout words and the words row, column, cell and edge are instructions, never visible text. Text inventory: exactly the strings in double quotes above, each appearing exactly once, spelled exactly as written; nothing else, no extra labels, numbers, icons with text, or legend.
```

## 2. П'ять речей, які записує нотатка агента

Вивід: `guide/images/agent-note-fields.webp`

Alt-текст: П'ять однакових карток для полів нотатки агента для кожного hunk: intent — для чого зміна; rejected alternative — варіант, який не взято, і чому; risk — що це може зламати і для кого; evidence — що рев'юер може перезапустити; open question — що агент не зміг вирішити. Кожна картка має приклад із шаблону. Unknown є дійсною відповіддю, окрім intent; нотатка — це твердження для перевірки, а не доказ.

```text
Create ONE clean editorial data infographic for a technical documentation guide, landscape 16:9 at 1600x900. Warm cream graph-paper background (#f5f1e8) with a subtle grid (#d4cfb8), precise dark ink lines (#1a1a1a), restrained orange (#d97706), green (#16a34a) and yellow (#fbbf24) accents. No photos, no 3D, no mascots, no decorative doodles, no company logos, no page number, no pretitle. Do not use em dashes.

Layout: five equal cards side by side in one row, read left to right. Each card is flat with a thin ink border and has, from top to bottom: a simple line icon, a bold name, a one-line definition, and at the lower edge a small monospace example chip with a thin ink outline. The first card has an orange top rule; the other four have a thin ink top rule.

Title at top left, large bold sans-serif: "Five things an agent note records for each hunk"
Subtitle under the title, regular weight: "This guide's proposal. Unknown is a valid answer, except for intent."

Card 1: name "Intent", definition "What the change is for", example chip "Sum prices, not item objects".
Card 2: name "Rejected alternative", definition "The option not taken, and why", example chip "Give Item an __add__ method".
Card 3: name "Risk", definition "What this could break, for whom", example chip "Items without a price raise AttributeError".
Card 4: name "Evidence", definition "What the reviewer can rerun", example chip "test_cart.py::test_total_uses_price".
Card 5: name "Open question", definition "What the agent could not decide", example chip "unknown".

Closing sentence centred below the cards, regular weight: "A note is a claim to check, not evidence."

Footer at bottom right in small monospace, with a clear margin from the canvas edge: "Template: examples/skills/agent-rationale"

Colour names and layout words are instructions, never visible text. Icons carry no text. Text inventory: exactly the strings in double quotes above, each appearing exactly once, spelled exactly as written; nothing else.
```
