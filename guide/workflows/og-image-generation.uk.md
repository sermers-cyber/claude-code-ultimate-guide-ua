---
title: "Динамічна генерація OG-зображень з Astro"
description: "Генеруйте зображення для прев'ю в соцмережах під час збірки з Astro, щоб поширені посилання показували актуальну статистику замість застарілого статичного PNG."
---

# Динамічна генерація OG-зображень з Astro

Генеруйте зображення для прев'ю в соцмережах автоматично під час збірки (build time) замість підтримки застарілих статичних PNG-файлів. Кожне поширення у Twitter/X, LinkedIn або Slack показуватиме точну та актуальну статистику.

## Навіщо це потрібно

Статичні OG-зображення стають неактуальними. У день, коли ви додаєте 200-й шаблон або отримуєте 1000 зірок на GitHub, ваше прев'ю в соцмережах досі показує старі цифри. Динамічна генерація вирішує цю проблему раз і назавжди, підтримуючи точність даних.

Цей патерн використовує Satori (від Vercel) для рендерингу React-подібного дерева в SVG, а потім resvg для конвертації в PNG. Він працює під час збірки в Astro, з нульовими витратами у runtime та без використання зовнішніх сервісів.

Див. також: [Генерація PDF](pdf-generation.uk.md) — ще один робочий процес генерації під час збірки (Quarto/Typst).

## Стек

| Package | Role |
|---------|------|
| `satori` | Рендерить JSX-подібне дерево об'єктів у SVG |
| `@resvg/resvg-js` | Конвертує SVG у PNG (Rust, швидко) |
| `@fontsource/inter` | Локальні файли шрифтів (вимагається формат woff1) |

## Налаштування

```bash
pnpm add satori @resvg/resvg-js @fontsource/inter
```

Створіть файл за шляхом `src/pages/og-image.png.ts`. Astro автоматично опублікує його за адресою `/og-image.png`.

Додайте посилання на нього у вашому макеті (layout):

```html
<meta property="og:image" content="/og-image.png" />
<meta name="twitter:image" content="/og-image.png" />
```

Дивіться готовий до використання шаблон: [`examples/scripts/og-image-astro.ts`](../../examples/scripts/og-image-astro.ts)

## Патерн

```typescript
import type { APIRoute } from 'astro'
import satori from 'satori'
import { Resvg } from '@resvg/resvg-js'
import { readFileSync } from 'fs'
import { resolve, dirname } from 'path'
import { fileURLToPath } from 'url'

const __dirname = dirname(fileURLToPath(import.meta.url))

export const GET: APIRoute = () => {
  const fontData = readFileSync(
    resolve(__dirname, '../../node_modules/@fontsource/inter/files/inter-latin-400-normal.woff')
  ).buffer as ArrayBuffer

  const svg = satori(
    { type: 'div', props: { style: { /* ... */ }, children: [ /* ... */ ] } },
    { width: 1200, height: 630, fonts: [{ name: 'Inter', data: fontData }] }
  )

  const png = new Resvg(svg, { fitTo: { mode: 'width', value: 1200 } }).render().asPng()

  return new Response(png.buffer as ArrayBuffer, {
    headers: { 'Content-Type': 'image/png' },
  })
}
```

## Динамічна статистика з контенту

Підраховуйте ваші файли контенту під час збірки замість жорсткого кодування (hardcoding):

```typescript
function countQuestions(): number {
  const dir = resolve(__dirname, '../content/questions')
  let total = 0
  for (const cat of readdirSync(dir, { withFileTypes: true })) {
    if (cat.isDirectory()) {
      total += readdirSync(resolve(dir, cat.name))
        .filter(f => f.endsWith('.md')).length
    }
  }
  return total
}
```

Показники, які можна підраховувати автоматично:
- Файли Markdown у каталозі контенту (питання, статті, документація)
- Записи YAML у файлі даних
- Кількість рядків у великому документі

Показники, які варто залишати жорстко закодованими (оновлювати вручну):
- Зірки на GitHub (динамічні дані, використовуйте консервативне значення на кшталт `1.1k+`)
- Шаблони з іншого репозиторію
- Бенчмарки продуктивності

## Підводні камені

### Формат шрифту має значення

Satori вимагає формат **woff1** або **TTF**. Він мовчки завершиться помилкою або видасть помилку при використанні woff2 чи зовнішніх посилань CDN, які перенаправляють на HTML.

```typescript
// Correct — local woff1 from @fontsource
readFileSync('node_modules/@fontsource/inter/files/inter-latin-400-normal.woff')

// Fails — woff2 not supported by resvg
readFileSync('node_modules/@fontsource/inter/files/inter-latin-400-normal.woff2')

// Fails — CDN may return HTML (redirects, auth walls)
await fetch('https://fonts.gstatic.com/s/inter/...')
```

### Статичні файли перекривають API-роути

Сервер розробки Astro віддає статичні файли з каталогу `public/` **перед** API-роутами. Якщо у вас є файл `public/og-image.png`, завжди буде віддаватися саме він замість вашої динамічної кінцевої точки (endpoint).

**Видаліть його:**
```bash
rm public/og-image.png
```

Також перевірте корінь проєкту та каталог `dist/`: файли там також можуть перекривати роут. Перевірити це можна командою `curl -I http://localhost:4321/og-image.png`: якщо відповідь містить заголовок `Last-Modified`, ви потрапляєте на статичний файл, а не на API-роут.

### Кеш браузера

Після видалення статичного файлу виконайте повне очищення кешу (`Cmd+Shift+R`) або протестуйте у новому вікні інкогніто. Браузер міг агресивно закешувати старий PNG-файл.

### `satori` є синхронним у новіших версіях

Деякі версії satori повертають `Promise<string>`, інші — просто `string`. Якщо ви отримуєте PNG із написом `[object Promise]`, додайте `await`:

```typescript
const svg = await satori(tree, options)
```

## Тестування

**Локальний перегляд**: відкрийте безпосередньо в браузері:
```
http://localhost:4321/og-image.png
```

**Симуляція прев'ю в соцмережах**: вставте ваш production-URL у:
- [opengraph.xyz](https://www.opengraph.xyz): універсальний відлагоджувач OG
- LinkedIn Post Inspector (`linkedin.com/post-inspector/`): змушує оновити кеш для LinkedIn
- Twitter Card Validator (`cards-dev.twitter.com/validator`)

**CI-перевірка**: якщо ви хочете відловлювати регресії, ви можете додати крок збірки, який перевіряє, чи розмір згенерованого PNG-файлу перевищує встановлений поріг:

```bash
# In CI after pnpm build
SIZE=$(wc -c < dist/og-image.png)
if [ "$SIZE" -lt 10000 ]; then
  echo "og-image.png looks too small ($SIZE bytes) — generation may have failed"
  exit 1
fi
```

## Варіанти

### Персональний брендинг (без сітки статистики)

```typescript
children: [
  { type: 'span', props: { style: { fontSize: '48px', color: '#c0522a' }, children: 'FB.' } },
  { type: 'span', props: { style: { fontSize: '80px', fontWeight: 800, color: '#f5f5f5' }, children: 'Your Name' } },
  { type: 'span', props: { style: { fontSize: '24px', color: '#8b949e' }, children: 'Your tagline here' } },
]
```

### Плашки списку проєктів (Project list badges)

```typescript
['project-a.com', 'project-b.com', 'project-c.com'].map(label => ({
  type: 'div',
  props: {
    style: { background: '#161b22', border: '1px solid #30363d', borderRadius: '8px', padding: '8px 16px' },
    children: [{ type: 'span', props: { style: { color: '#c0522a' }, children: label } }],
  },
}))
```

### Плашка у стилі терміналу (для CLI-інструментів)

```typescript
{
  type: 'div',
  props: {
    style: { background: '#21262d', border: '1px solid #30363d', borderRadius: '20px', padding: '6px 16px', color: '#3fb950', fontFamily: 'monospace' },
    children: '>_ your-cli-tool',
  },
}
```

## Синхронізація статистики

Підтримуйте єдине джерело істини (single source of truth). Коли ви оновлюєте статистику на OG-зображенні, оновлюйте її всюди (плашки на цільовій сторінці, README тощо) в одному комміті.

Для проєктів із декількома цільовими сторінками (landings) створіть слеш-команду `/update-stats-image-landings`, яка обходить кожен репозиторій і пропонує вам підтвердити кожен показник. Це запобігає розходженню даних між сайтами.

---
**Локалізація**: [Serhii (MacPlus Software)](https://macplus-software.com)
*Остання синхронізація: Травень 2026*
