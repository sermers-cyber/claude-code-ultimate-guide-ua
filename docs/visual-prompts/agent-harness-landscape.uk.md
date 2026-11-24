# Візуальні промпти для ландшафту agent harness

Ці промпти згенерували три растрові ілюстрації, що використовуються в Agent Harness Map. Кожне зображення згенеровано як окремий ресурс, переглянуто візуально, змінено до 1600 x 900 і конвертовано у WebP.

Вибрані вихідні файли Gemini:

| Опублікований ресурс | Вибране джерело |
|---|---|
| `agent-harness-160-not-runtimes.webp` | `Gemini_Generated_Image_21edgl21edgl21ed.jpeg` |
| `agent-harness-four-layers.webp` | `Gemini_Generated_Image_u0ieeju0ieeju0ie.jpeg` |
| `agent-harness-selection-funnel.webp` | `Gemini_Generated_Image_7rttz17rttz17rtt.jpeg`, із виправленою перед конвертацією кількістю пілотних завдань: замість 5-10 стало 8-12 реальних тікетів |

## Спільний художній напрям

Використовуйте теплий кремовий фон у стилі міліметрівки (`#f5f1e8`), ледь помітну сітку (`#d4cfb8`), точні темні олівцеві або чорнильні лінії (`#1a1a1a`) та стримані акценти жовтого (`#fbbf24`), зеленого (`#16a34a`) і помаранчевого (`#d97706`). Червоний залишайте для бар'єрів ризику. Тримайте макет редакційним і технічним. Не використовуйте фото, 3D, маскотів, декоративні дудли, зірки, номери сторінок чи логотипи. Увесь видимий текст англійською. Цільовий розмір 1600 x 900 пікселів.

## 1. Широкий каталог проти суворої мапи рантаймів

Результат: `guide/images/agent-harness-160-not-runtimes.webp`

Альтернативний текст: Триетапна воронка відокремлює широкий каталог із 160 проєктів у 12 категоріях від тесту на володіння циклом і меншої суворої мапи рантаймів, де суміжні та невідомі проєкти тримаються окремо.

```text
Create a clean editorial infographic for a technical documentation guide, landscape 16:9 at 1600x900. Visual language: warm cream graph-paper background (#f5f1e8), very subtle grid (#d4cfb8), precise dark pencil/ink lines (#1a1a1a), restrained yellow (#fbbf24), green (#16a34a), and orange (#d97706) accents. No photos, no 3D, no mascots, no decorative doodles, no stars, no page numbers, no logos. High information density but ample whitespace. All visible text must be exactly in English and spelled correctly.

Headline, large: “160 PROJECTS ≠ 160 RUNTIMES”
Under it, create a left-to-right evidence funnel made of three clearly separated cards connected by thin arrows:
1. Card title “Broad catalog” with large number “160”, small line “projects”, and a compact badge “12 categories”. Show a mixed stack of small abstract tool cards to signal heterogeneous entries.
2. Card title “Loop ownership test” with a simple circular agent loop diagram labeled “plan”, “act”, “observe”, “repeat”. Add a filter gate with the question “Who owns the loop?”
3. Card title “Strict runtime map” with a compact set of selected runtime blocks, plus two side bins labeled “Adjacent control planes” and “Unknown”.
At the bottom, add one concise note: “Catalog size is not runtime count.”
Make hierarchy crystal clear. Avoid tiny text. The image must remain readable embedded in a documentation page.
```

## 2. Чотири шари та відповідальності

Результат: `guide/images/agent-harness-four-layers.webp`

Альтернативний текст: Чотиришаровий стек розділяє модель, repository harness, runtime harness та оркестратор: керування тече вниз, а докази піднімаються вгору.

```text
Create a clean editorial infographic for a technical documentation guide, landscape 16:9 at 1600x900. Visual language: warm cream graph-paper background (#f5f1e8), very subtle grid (#d4cfb8), precise dark pencil/ink lines (#1a1a1a), restrained yellow (#fbbf24), green (#16a34a), and orange (#d97706) accents. No photos, no 3D, no mascots, no decorative doodles, no stars, no page numbers, no logos. High information density but ample whitespace. All visible text must be exactly in English and spelled correctly.

Headline: “FOUR LAYERS, FOUR JOBS”
Build one clear vertical architecture stack of four wide horizontal layers. Use thin arrows to show control flowing downward and evidence flowing upward.
Layer 4, top, orange accent: “ORCHESTRATOR” and subtitle “coordinates agents or runtimes”. Include three small connected worker nodes.
Layer 3, green accent: “RUNTIME HARNESS” and subtitle “owns plan → act → observe → repeat”. Include a concise circular loop with labels “plan”, “act”, “observe”, “repeat”.
Layer 2, yellow accent: “REPOSITORY HARNESS” and subtitle “instructions, hooks, skills, policy”. Include compact file tabs labeled “AGENTS.md”, “hooks”, “skills”.
Layer 1, bottom, neutral accent: “MODEL” and subtitle “generates and reasons”. Include one abstract neural block, not a brain illustration.
At the right, add a slim responsibility panel titled “ASK FIRST” with four questions aligned to the layers: “Who coordinates?”, “Who owns the loop?”, “What configures the repo?”, “Which model runs?”
At the bottom, add: “Do not compare tools from different layers as substitutes.”
Make the layer boundaries and ownership distinction unmistakable. Avoid tiny text.
```

## 3. Воронка вибору та доказів

Результат: `guide/images/agent-harness-selection-funnel.webp`

Альтернативний текст: П'ятикроковий потік вибору визначає завдання, перевіряє володіння циклом, верифікує докази, проводить пілот на 8-12 реальних завданнях і завершується рішенням: прийняти, суміжний шар або відхилити.

```text
Create a clean editorial decision infographic for a technical documentation guide, landscape 16:9 at 1600x900. Visual language: warm cream graph-paper background (#f5f1e8), very subtle grid (#d4cfb8), precise dark pencil/ink lines (#1a1a1a), restrained yellow (#fbbf24), green (#16a34a), and orange (#d97706) accents. Use red only for a risk gate. No photos, no 3D, no mascots, no decorative doodles, no stars, no page numbers, no logos. All visible text must be exactly in English and spelled correctly.

Headline: “CHOOSE THE LOWEST LAYER THAT SOLVES THE PROBLEM”
Create a left-to-right selection funnel with five large steps connected by arrows:
1. “DEFINE THE JOB” with four selectable labels: “Generate”, “Run”, “Configure”, “Coordinate”.
2. “CHECK LOOP OWNERSHIP” with the question “Does it own plan → act → observe → repeat?” and two paths “Yes” and “No / unknown”.
3. “VERIFY EVIDENCE” with a small checklist: “Official URL”, “README or docs”, “Security boundary”, “Recovery behavior”.
4. “PILOT” with a bold band “8–12 REAL TASKS” and three measured outputs: “success”, “cost”, “recovery”.
5. “DECIDE” with three outcome cards: “Adopt”, “Keep as adjacent layer”, “Reject”.
Below the funnel, add a horizontal red risk gate labeled “Human approval for consequential actions”.
At the bottom, add a concise note: “Features and popularity do not replace task-level evidence.”
Keep each step visually distinct, readable, and practical. Avoid tiny text.
```

## Запис верифікації

| Ресурс | Розміри | Розмір |
|---|---:|---|
| `agent-harness-160-not-runtimes.webp` | 1600 x 900 | Вибраний вихід Gemini, змінений за розміром і конвертований у WebP |
| `agent-harness-four-layers.webp` | 1600 x 900 | Вибраний вихід Gemini, змінений за розміром і конвертований у WebP |
| `agent-harness-selection-funnel.webp` | 1600 x 900 | Вибраний вихід Gemini, виправлений до протоколу з 8-12 тікетів, змінений за розміром і конвертований у WebP |
