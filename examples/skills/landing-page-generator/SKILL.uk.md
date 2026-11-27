---
name: landing-page-generator
description: "Генерація повних, готових до деплою лендингів із будь-якого репозиторію. Використовуйте, коли створюєте домашню сторінку для open-source проєкту, будуєте вебсайт проєкту, перетворюєте README на маркетингову сторінку або уніфікуєте лендинги кількох репозиторіїв."
allowed-tools: Read Bash Write
effort: medium
---

# Генератор лендингів

Згенеруйте повний, готовий до деплою лендинг із будь-якого репозиторію, проаналізувавши його документацію та структуру.

## Коли використовувати цей skill

- Створення лендингу для репозиторію GitHub
- Генерація статичних сайтів із наявної документації
- Уніфікація лендингів кількох проєктів
- Перетворення вмісту README на маркетингові/демонстраційні сторінки

## Що робить цей skill

1. **Аналіз репозиторію**: читає README.md, CHANGELOG.md, package.json/VERSION, docs/, assets/
2. **Витяг вмісту**: визначає заголовок, слоган, функції, встановлення, скріншоти
3. **Відображення на розділи**: Hero, Features, Install, FAQ, Footer (+ опційно: Risk Banner, Pricing)
4. **Генерація лендингу**: створює повний статичний сайт (HTML + CSS + JS)
5. **Результат, готовий до деплою**: включає workflow GitHub Actions для GitHub Pages

## Як використовувати

### Базове використання

```
/landing-page-generator from ~/path/to/repo
```

### З опціями

```
/landing-page-generator from ~/path/to/repo --risk-banner --pricing-table
```

### Доступні опції

| Опція | Опис | За замовчуванням |
|--------|-------------|---------|
| `--risk-banner` | Додати помітний банер із попередженням/відмовою від відповідальності над згином | false |
| `--pricing-table` | Включити розділ порівняння цін | false |
| `--screenshots <path>` | Шлях до теки зі скріншотами | ./assets/ |
| `--theme [dark\|light]` | Варіант кольорової теми | dark |
| `--search` | Увімкнути пошук Cmd+K | true |
| `--output <path>` | Директорія виводу | ./[repo-name]-landing/ |

## Робочий процес

### Крок 1: Аналіз репозиторію

Прочитайте й проаналізуйте ці файли з вихідного репозиторію:

```
README.md        → Primary content source (title, tagline, features, install)
CHANGELOG.md     → Version info, recent changes
package.json     → Version number, dependencies, metadata
VERSION          → Alternative version source
docs/            → Additional documentation pages
assets/          → Screenshots, images
LICENSE          → License type for badge
```

### Крок 2: Мапа витягу вмісту

| Джерело | Цільовий розділ | Метод витягу |
|--------|---------------|-------------------|
| Заголовок/бейджі README | Hero | Перший H1 + рядки бейджів shield.io |
| README TL;DR | Слоган Hero | Перший абзац або цитата після заголовка |
| Функції README | Сітка Features | Розділи H2/H3 із маркованими списками |
| Встановлення в README | Quick Start | Блоки коду з shell-командами |
| Використання в README | Examples | Блоки коду з прикладами |
| FAQ у README | FAQ | Патерни details/summary або H3+P |
| CHANGELOG | What's New | Останні 1-3 релізи |
| assets/*.png | Скріншоти | Розділ-галерея |

### Крок 3: Генерація розділів

Згенеруйте ці розділи в такому порядку:

1. **Header** (закріплений)
   - Логотип/назва проєкту
   - Навігаційні посилання: Features, Install, FAQ
   - Дії: пошук (Cmd+K), зірка GitHub, основний CTA

2. **Risk Banner** (якщо `--risk-banner`)
   - Помаранчевий/попереджувальний стиль над згином
   - Чіткий, помітний текст відмови від відповідальності
   - Посилання на розділ із докладним розкриттям

3. **Hero Section**
   - Заголовок із H1 README
   - Слоган із TL;DR/першого абзацу
   - Бейджі зі статистикою (версія, ліцензія, платформа)
   - CTA: «Quick Start» (основний), «View on GitHub» (другорядний)

4. **Architecture/Overview** (якщо в README є діаграма)
   - ASCII-діаграма, перетворена на стилізований блок
   - Або картки огляду

5. **Features Grid**
   - 4-6 карток функцій із функцій README
   - Патерн «іконка + заголовок + опис»

6. **Pricing Table** (якщо `--pricing-table`)
   - Таблиця порівняння планів
   - Таблиця множників/використання, якщо є

7. **Screenshots Gallery** (якщо є assets)
   - Галерея на вкладках або карусель
   - Підписи з alt-тексту

8. **Quick Start Section**
   - Однорядкова команда встановлення (виділений блок коду)
   - Кроки налаштування
   - Перший приклад використання

9. **Risk Disclosure** (якщо `--risk-banner`)
   - Повний розділ із відмовою від відповідальності
   - Міркування щодо ToS
   - Рекомендації

10. **FAQ Section**
    - Генерується з FAQ у README або поширених запитань
    - Патерн згортуваних details

11. **Related Projects** (якщо в README є посилання)
    - Картки з посиланнями на залежності/пов'язані репозиторії

12. **Footer**
    - Швидкі посилання
    - Бейдж ліцензії
    - Інформація про версію
    - Посилання на автора/репозиторій

### Крок 4: Структура виводу

```
[project-name]-landing/
├── index.html              # Main landing page
├── styles.css              # Complete stylesheet
├── search.js               # Cmd+K search functionality
├── search-data.js          # Search index (FAQ, features)
├── favicon.svg             # Generated or copied
├── robots.txt              # SEO
├── CLAUDE.md               # Project instructions
├── README.md               # Landing repo documentation
├── assets/                 # Copied screenshots
│   └── [copied from source]
└── .github/
    └── workflows/
        └── static.yml      # GitHub Pages deployment
```

### Крок 5: Контрольна точка валідації

Перед завершенням перевірте:
- Усі розділи коректно відображаються в браузері
- Посилання ведуть на дійсні цілі (репозиторій GitHub, документація, команди встановлення)
- Адаптивна розмітка працює на ширинах мобільного (375px), планшета (768px) і десктопа (1280px)
- Доступність: наявні skip-посилання, мітки ARIA на інтерактивних елементах, контраст кольорів відповідає WCAG AA

## Технологічний стек

- **Без кроку збірки**: чисті HTML + CSS + JS
- **Пошук**: MiniSearch, що завантажується ліниво з CDN із запасним варіантом
- **Деплой**: GitHub Pages через Actions
- **Стилізація**: CSS custom properties, адаптивність, темна тема за замовчуванням
- **Доступність**: skip-посилання, мітки ARIA, навігація клавіатурою

## Патерни CSS (із усталених лендингів)

### Класи компонентів

```css
/* Buttons */
.btn, .btn-primary, .btn-secondary, .btn-github-star, .btn-outline

/* Cards */
.feature-card, .comparison-card, .path-card

/* Layout */
.container, .features-grid, .hero, .section

/* Utilities */
.visually-hidden, .skip-link
```

### Змінні CSS

```css
:root {
  --color-bg: #0d1117;
  --color-surface: #161b22;
  --color-border: #30363d;
  --color-text: #c9d1d9;
  --color-text-muted: #8b949e;
  --color-primary: #58a6ff;
  --color-success: #3fb950;
  --color-warning: #d29922;
  --color-danger: #f85149;
  --space-xs: 0.25rem;
  --space-sm: 0.5rem;
  --space-md: 1rem;
  --space-lg: 1.5rem;
  --space-xl: 2rem;
  --radius: 6px;
}
```

## Приклад

**Користувач**: `/landing-page-generator from ~/projects/my-project --risk-banner --pricing-table`

**Результат**:

Створює `~/projects/my-project-landing/` із:
- Повним лендингом, що демонструє мультипровайдерний роутер
- Помітним банером ризику ToS (помаранчевий, над згином)
- Картками провайдерів (Anthropic, Copilot, Ollama)
- Таблицями цін із README
- Галереєю скріншотів
- Готовністю до деплою на GitHub Pages

## Поради

- Завжди додавайте `--risk-banner` для проєктів із юридичними/ToS-міркуваннями
- Скріншоти суттєво покращують якість лендингу: переконайтеся, що assets/ заповнена
- Skill зберігає мову README (англійська/французька)
- Перегляньте згенерований FAQ: його може знадобитися адаптувати
- Протестуйте адаптивний дизайн після генерації

## Довідники

Докладну документацію патернів дивіться в `references/landing-pattern.md`.
Багаторазові шаблони та фрагменти дивіться в `assets/`.
