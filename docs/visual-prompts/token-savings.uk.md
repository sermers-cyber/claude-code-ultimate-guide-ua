# Візуальні промпти про заощадження токенів

Ці промпти ілюструють порівняння заявленого та виміряного заощадження в інструментах економії токенів і розподіл токенів інструментів за типами викликів. Кожен видимий рядок узято з первинних джерел, прочитаних 2026-09-30 (блог JetBrains AI, Stet.sh, Dasein Code-Compression Bench, README вендорів, Marmelab Atomic CRM Builder). Генеруйте по одному зображенню на промпт за допомогою Gemini 3 Pro Image, перед публікацією звіряйте кожен відрендерений напис і число з рядками джерел і конвертуйте обране джерело у WebP у рідному розмірі (Gemini повернув 1376 x 768; зображення не масштабували вгору).

## Запис вибору

| Опублікований ресурс | Спроба | Статус |
|---|---|---|
| `token-savings-claimed-vs-measured.webp` | 2 | Спробу 1 відхилено: кожен рядок тегу відрендерився двічі в кожному ряду (по одному під кожним значенням). Спробу 2 обрано після виправлення промпту (один рядок тегу на ряд): усі чотири ряди, вісім значень, чотири теги, чотири маркери одиниць, футер і рядок джерела збігаються з рядками джерела; зайвого тексту немає. Рядок джерела переноситься на два рядки на "Code-" і "Compression", але сам рядок цілий |
| `token-savings-tool-token-share.webp` | 1 | Обрано з першої спроби: заголовок, три підписи сегментів, два виноски, примітка та рядок джерела збігаються; ширини сегментів виміряно приблизно як 90%, 6.7% і 3.4% смуги, помітно пропорційно до 90.6, 6.4 і 3.0 |

## Спільне художнє рішення

Використовуйте теплий кремовий фон у стилі міліметрівки (`#f5f1e8`), ледь помітну сітку (`#d4cfb8`), точні темні лінії чорнила (`#1a1a1a`) і стримані акценти: помаранчевий (`#d97706`), зелений (`#16a34a`) і жовтий (`#fbbf24`). Червоний залишайте для попереджень. Жодних фото, 3D, маскотів, декоративних дудлів, логотипів компаній, номерів сторінок чи додаткового надзаголовка. Увесь видимий текст англійською. Не використовуйте довгих тире. Запитуване співвідношення сторін 16:9.

## 1. Заявлене проти виміряного

Вивід: `guide/images/token-savings-claimed-vs-measured.webp`

Альтернативний текст: Чотири інструменти економії токенів, порівняні за заявою вендора та незалежним вимірюванням: Caveman заявляє на 65% менше вихідних токенів, виміряно 8.5%; RTK заявляє на 60-90% менше токенів у виводі shell, виміряно +7.6% вартості завдання; Ponytail заявляє приблизно на 20% дешевше, виміряно +20%, потім -2%; Headroom заявляє на 73-92% менше токенів на певному вмісті, виміряно +44% загальної вартості.

```text
Create a clean editorial data infographic for a technical documentation guide, landscape 16:9 at 1600x900. Warm cream graph-paper background (#f5f1e8) with a subtle grid (#d4cfb8), precise dark ink lines (#1a1a1a), restrained orange (#d97706), green (#16a34a) and yellow (#fbbf24) accents, red only for the warning marker. No photos, no 3D, no mascots, no decorative doodles, no company logos, no page number, and no pretitle. All visible text must be exactly the English strings listed below, spelled correctly, each appearing exactly once. Do not use em dashes. Do not add any other words, numbers, or labels.

Headline at top left, large bold sans-serif: "CLAIMED VS MEASURED"

Below the headline, a table of four horizontal rows, each row a flat card with a thin ink border. Each row has three zones from left to right: a narrow tool name zone, a "claimed" zone with an orange left edge, and a "measured" zone with a dark ink left edge. Above the two value zones, shown once only as column captions in small monospace capitals: "CLAIMED" over the left value zone and "MEASURED" over the right value zone. Each row carries exactly ONE small monospace tag line, placed once at the bottom of the row card, spanning the row under the two value zones; it is never repeated inside both zones. At the far right of each row, a small rounded pill marker.

Row 1. Tool name in bold: "Caveman". Claimed value: "65% fewer output tokens". Measured value: "8.5% fewer output tokens". Tag line: "JetBrains, 82 paired tasks, forced activation". Pill marker: "same unit".
Row 2. Tool name in bold: "RTK". Claimed value: "60-90% fewer tokens in shell output". Measured value: "+7.6% cost per task (low effort)". Tag line: "JetBrains, 86 SkillsBench tasks". Pill marker: "different unit".
Row 3. Tool name in bold: "Ponytail". Claimed value: "~20% cheaper". Measured value: "+20% then -2% cost over two runs". Tag line: "Stet, 10 tasks, 2 runs". Pill marker: "same unit".
Row 4. Tool name in bold: "Headroom". Claimed value: "73-92% fewer tokens on specific content". Measured value: "+44% total cost". Tag line: "Dasein, 100 SWE-bench tasks, sponsor-run". Pill marker: "different unit".

Pill markers reading "same unit" are green outlined; pill markers reading "different unit" are yellow filled.

Bottom strip across the full width with a small red warning marker and the text in regular weight: "A shell-output or content-type saving is not a total-cost saving."

Footer at bottom right in small monospace, with a clear margin so no character touches the canvas edge: "Sources: JetBrains AI blog, Stet.sh, Dasein Code-Compression Bench, vendor READMEs. Read 2026-09-30."
```

## 2. Звідки беруться токени інструментів

Вивід: `guide/images/token-savings-tool-token-share.webp`

Альтернативний текст: Одна складена смуга токенів інструментів у базовому прогоні Atomic CRM Builder: Read 90.6% при 958 токенах на виклик, Bash 6.4% при 77 токенах на виклик, Edit, Write та інше 3.0%, тож фільтр виводу shell зачіпає лише частку Bash.

```text
Create a clean editorial data infographic for a technical documentation guide, landscape 16:9 at 1600x900. Warm cream graph-paper background (#f5f1e8) with a subtle grid (#d4cfb8), precise dark ink lines (#1a1a1a), restrained orange (#d97706), green (#16a34a) and yellow (#fbbf24) accents, red only for the warning marker. No photos, no 3D, no mascots, no decorative doodles, no company logos, no page number, and no pretitle. All visible text must be exactly the English strings listed below, spelled correctly, each appearing exactly once. Do not use em dashes. Do not add any other words, numbers, axis ticks, or labels.

Headline at top left, large bold sans-serif: "WHERE TOOL TOKENS COME FROM"

Center of the canvas: a single very wide horizontal 100% stacked bar, spanning almost the full canvas width, with a thin ink outline, tall enough to hold labels inside or directly above. Three segments, widths strictly proportional to their values: the first segment takes 90.6% of the bar width (orange), the second takes 6.4% (green), the third takes 3.0% (yellow). The first segment is therefore much wider than the other two combined. Each segment is labeled with exactly one label: the orange segment "Read 90.6%", the green segment "Bash 6.4%", the yellow segment "Edit, Write, other 3.0%". Because the green and yellow segments are narrow, place their labels just above or below them with a thin leader line.

Under the bar, two callout cards side by side, flat with thin ink borders. Left card, under the orange part: "Read: 958 tokens per call". Right card, under the green part: "Bash: 77 tokens per call".

Below the callouts, a wide strip with a small red warning marker and the text in regular weight: "A shell-output filter only touches the Bash slice."

Footer at bottom right in small monospace: "Marmelab, Atomic CRM Builder, 9 baseline instances, August 2026."
```
