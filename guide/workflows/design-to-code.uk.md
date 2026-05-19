---
title: "Робочий процес перенесення дизайну в код за допомогою Figma MCP"
description: "Автоматизована реалізація дизайн-системи за допомогою Figma MCP Server для досягнення паритету дизайну та коду 1:1"
tags: [workflow, mcp, integration]
---

# Робочий процес перенесення дизайну в код за допомогою Figma MCP

> **Рівень впевненості**: Рівень 2 — на основі задокументованих практичних кейсів із реального виробництва (Parallel HQ, builder.io), специфікацій серверів MCP та робочих процесів спільноти.

Автоматизована реалізація дизайн-системи за допомогою Figma MCP Server дозволяє продуктовим дизайнерам передавати готові до продакшену специфікації у Claude Code, який реалізує компоненти із збереженням паритету між дизайном та кодом 1:1.

---

## Зміст

1. [Коротко (TL;DR)](#tldr)
2. [Задокументований ефект](#documented-impact)
3. [Огляд архітектури](#architecture-overview)
4. [3-рівнева ієрархія токенів](#3-tier-token-hierarchy)
5. [Передумови](#prerequisites)
6. [Основні робочі процеси](#core-workflows)
7. [Налаштування Code Connect](#code-connect-setup)
8. [Приклади промптів](#example-prompts)
9. [Шаблони впровадження в команду](#team-adoption-patterns)
10. [Антипатерни](#anti-patterns)
11. [План впровадження (Roadmap)](#implementation-roadmap)
12. [Джерела](#resources)

---

## TL;DR

```
Designer (Figma Make) → Export (Figma Design) → Claude (Figma MCP) → Production Code

Key insight: Design system = source of truth
Claude consumes tokens/components directly from Figma
Implementation maintains design parity automatically
```

---

## Задокументований ефект

На основі виробничих практичних кейсів станом на січень 2026 року:

| Метрика | Покращення | Джерело |
|---------|-------------|--------|
| Невідповідності дизайну | Зниження на 62% | Дослідження Parallel HQ |
| Ефективність робочого процесу | Покращення на 78% | Кейс-стаді builder.io |
| Збережений інженерний час | 75 днів (за 6 місяців) | Виробничі дані Parallel HQ |
| Час виходу на ринок (Time-to-market) | Зниження на 56% | Композитні дані кількох організацій |
| Технічний борг у дизайні | Зниження на 82% | Аудит після впровадження |

**Типовий час виконання робочих процесів**:
- Один frame → Готовий до продакшену компонент: 2-3 хвилини
- Аудит відхилень від дизайн-системи: 3 тижні → 3 хвилини
- Поширення оновлень токенів: години ручної роботи → секунди в автоматичному режимі

*Джерела: builder.io/blog/claude-code-figma-mcp-server, parallelhq.com/blog/automating-design-systems-with-ai, composio.dev/blog/how-to-use-figma-mcp-with-claude-code*

---

## Огляд архітектури

### Повний стек

```
[Figma Design File]
    ↓ (Variables & Styles)
[Плагін Tokens Studio] (необов'язково, але рекомендовано)
    ↓ (експорт у JSON)
[Репозиторій GitHub]
    ↓ (CI/CD)
[Style Dictionary]
    ↓ (Перетворення)
[CSS Custom Properties / Конфігурація Tailwind]
    ↓ (Використовується)
[Бібліотека компонентів]
    ↑ (Читає через)
[Claude Code + Figma MCP]
```

### Точка інтеграції MCP

Claude Code отримує доступ до Figma через Figma MCP Server:

```
Claude Code
    ↓ (використовує)
Figma MCP Server (mcp-server-figma)
    ↓ (автентифікується через)
Figma Personal Access Token
    ↓ (читає)
Figma File (дані Dev Mode)
```

**До чого Claude має доступ**:
- Структура файлу та frames
- Стилі кольорів, тексту та ефектів
- Властивості компонентів
- Змінні (токени)
- Анотації Dev Mode
- Фрагменти Code Connect (якщо налаштовано)

**До чого Claude НЕ має доступу**:
- Приватні файли без дозволів токена
- Можливості редагування (лише для читання)
- Дані про спільну роботу в реальному часі
- Історія версій (лише поточний стан)

---

## 3-рівнева ієрархія токенів

Сучасні дизайн-системи використовують ієрархічну структуру токенів. Claude Code розуміє цю ієрархію при читанні даних із Figma.

| Рівень | Визначення | Реалізація у Figma | Результат у коді |
|------|------------|----------------------|-------------|
| **Базовий (Base)** | Примітивні значення | Figma Variables (наприклад, `blue-600: #0066CC`, `spacing-2: 8px`) | CSS-властивості (`--blue-600`, `--spacing-2`) |
| **Композитний (Composite)** | Комбіновані примітиви | Заливки компонентів, що посилаються на змінні | Конфігурація Tailwind або CSS-класи |
| **Семантичний (Semantic)** | Контекстуальне значення | Контекстуальні аліаси змінних (наприклад, `color-interactive-primary` → `blue-600`) | Props компонентів або токени теми |

### Приклад ієрархії

```
Base:
  --color-blue-600: #0066CC
  --spacing-2: 8px
  --radius-md: 4px

Composite:
  --button-padding: var(--spacing-2) var(--spacing-4)
  --button-border-radius: var(--radius-md)

Semantic:
  --interactive-primary: var(--color-blue-600)
  --interactive-primary-hover: var(--color-blue-700)
```

**Поведінка Claude Code**: Отримавши компонент Figma, Claude:
1. Витягує змінні, на які є посилання (базовий рівень)
2. Визначає композитні патерни (відступи, розміри)
3. Застосовує семантичні назви відповідно до ваших правил іменування токенів
4. Генерує код, що відповідає цій ієрархії

---

## Передумови

### Для дизайнерів

| Вимога | Деталі |
|-------------|---------|
| **Ліцензія Figma** | Місце з доступом до Dev Mode (дозволяє інспектувати змінні, фрагменти коду) |
| **Впорядковані змінні** | Використання Figma Variables або плагіна Tokens Studio для керування токенами |
| **Структура компонентів** | Auto Layout, іменовані шари, узгоджені правила іменування |
| **Іменування Frame** | Описові назви frame (Claude використовує їх для назв компонентів) |

### Для розробників

| Вимога | Деталі |
|-------------|---------|
| **Claude Code** | Версія 1.5.0+ (підтримка MCP) |
| **Figma MCP Server** | `npm install -g @modelcontextprotocol/server-figma` |
| **Персональний токен доступу** | Генерується в налаштуваннях облікового запису Figma → Tokens |
| **Конфігурація MCP** | Токен налаштований у конфігурації Claude Code |

### Конфігурація MCP

Додайте у ваші налаштування Claude Code MCP (`.claude/mcp.json` або через UI налаштувань):

```json
{
  "mcpServers": {
    "figma": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-figma"],
      "env": {
        "FIGMA_PERSONAL_ACCESS_TOKEN": "your-token-here"
      }
    }
  }
}
```

**Примітка щодо безпеки**: Використовуйте змінні оточення для продакшену:
```json
{
  "env": {
    "FIGMA_PERSONAL_ACCESS_TOKEN": "${FIGMA_TOKEN}"
  }
}
```

Потім експортуйте у вашому шеллі: `export FIGMA_TOKEN="figd_..."`

---

## Основні робочі процеси

### Робочий процес A: Один Frame → Готовий до продакшену компонент

**Час виконання**: 2-3 хвилини на компонент

**Кроки**:

1. **Дизайнер**: Створює компонент у Figma з відповідними змінними/стилями.
2. **Дизайнер**: Ділитися URL-адресою файлу Figma з розробником/Claude.
3. **Розробник**: Надає промпт для Claude Code:

```
Read the "Button/Primary" component from Figma file:
https://www.figma.com/design/FILE_KEY

Implement as a React component with TypeScript.
Use Tailwind for styling, mapping Figma variables to our design tokens.
Ensure responsive behavior matches Figma's Auto Layout constraints.
```

4. **Claude**:
   - Отримує компонент через Figma MCP.
   - Витягує стилі, розміри, відступи.
   - Мапить змінні на токени в коді.
   - Генерує компонент із props, що відповідають варіантам Figma.

5. **Верифікація**: `npm run dev` → Візуальне порівняння з Figma.

**Приклад результату**:
```tsx
// components/Button/Primary.tsx
interface ButtonProps {
  size?: 'sm' | 'md' | 'lg';
  disabled?: boolean;
  children: React.ReactNode;
}

export function PrimaryButton({ size = 'md', disabled, children }: ButtonProps) {
  return (
    <button
      className={cn(
        'rounded-md font-medium transition-colors',
        'bg-interactive-primary text-white',
        'hover:bg-interactive-primary-hover',
        'disabled:opacity-50 disabled:cursor-not-allowed',
        {
          'px-3 py-1.5 text-sm': size === 'sm',
          'px-4 py-2 text-base': size === 'md',
          'px-6 py-3 text-lg': size === 'lg',
        }
      )}
      disabled={disabled}
    >
      {children}
    </button>
  );
}
```

---

### Робочий процес B: Аудит відхилень від дизайн-системи

**Час виконання**: 3 тижні ручного перегляду → 3 хвилини в автоматичному режимі

**Проблема**: З часом код відхиляється від дизайн-системи (з'являються «магічні числа», зашиті кольори, неузгоджені відступи).

**Рішення**: Claude проводить аудит кодової бази на відповідність єдиному джерелу правди у Figma.

**Промпт**:
```
Audit src/components for design system compliance.
Compare against our Figma design system:
https://www.figma.com/design/FILE_KEY

Report:
1. Hardcoded colors not using design tokens
2. Magic number spacing values
3. Components not matching Figma structure
4. Missing responsive patterns

Then propose fixes with token replacements.
```

**Вивід Claude**:
```markdown
## Design System Audit Results

### Issues Found (23 total)

#### Hardcoded Colors (8 instances)
- `src/components/Card.tsx:45` → `#0066CC` should be `var(--interactive-primary)`
- `src/components/Header.tsx:12` → `#F3F4F6` should be `var(--surface-secondary)`
...

#### Magic Numbers (11 instances)
- `src/components/Modal.tsx:23` → `padding: 16px 24px` should be `var(--spacing-4) var(--spacing-6)`
...

#### Structural Mismatches (4 instances)
- `src/components/Button.tsx` → Missing `icon-left` variant present in Figma
...
```

---

### Робочий процес C: Конвеєр автоматизації токенів

**Мета**: Зміни змінних Figma автоматично поширюються на код.

**Архітектура**:

```
Figma Variables
    ↓ (Tokens Studio export or Figma API)
GitHub Repository (tokens.json)
    ↓ (GitHub Actions CI/CD)
Style Dictionary Transform
    ↓ (generates)
CSS / Tailwind / Platform-specific tokens
    ↓ (commit & deploy)
Production
```

**Налаштування** (одноразове):

1. **Плагін Tokens Studio**: Підключіть до репозиторію GitHub.
2. **Конфігурація Style Dictionary**: Визначте правила перетворення.
3. **GitHub Actions**: Автоматичний запуск при оновленні токенів.
4. **Роль Claude**: Перегляд та валідація згенерованих токенів.

**Промпт розробника** (після запуску CI):
```
Review the token update from commit abc1234.
Check if any components need updates to consume new tokens.
Generate migration guide if breaking changes exist.
```

**Вивід Claude**:
```markdown
## Token Update Review (v2.3.0 → v2.4.0)

### Changes
- Added: `--spacing-7`, `--spacing-8` (requested by design)
- Changed: `--interactive-secondary` hue shift 5° (brand refresh)
- Deprecated: `--legacy-blue` (remove by Q3)

### Impact Analysis
- 12 components reference `--interactive-secondary` → Auto-updated via token reference
- 3 components use deprecated `--legacy-blue` → Migration needed

### Migration Required
1. `src/components/LegacyButton.tsx:34` → Replace `--legacy-blue` with `--interactive-primary`
2. `src/components/OldCard.tsx:67` → Replace with new token
3. `src/utils/theme.ts:12` → Update theme export

### Migration Script
[Claude generates codemod or find/replace script]
```

---

### Робочий процес D: Візуальний цикл ітерацій (Figma + Playwright)

**Мета**: Автоматизоване тестування візуальної регресії на відповідність макетам Figma.

**Стек MCP**: Figma MCP + Playwright MCP

**Налаштування**:
```
Claude Code accesses:
- Figma (design source of truth)
- Playwright (automated browser testing)
```

**Промпт**:
```
Take a screenshot of our Button component in all variants.
Compare against Figma frames from:
https://www.figma.com/design/FILE_KEY → "Button Tests" page

Report any visual differences (color, spacing, typography).
```

**Процес**:
1. Claude зчитує frames Figma (очікуваний стан).
2. Claude використовує Playwright для створення скріншотів реальних компонентів (фактичний стан).
3. Claude порівнює їх (попіксельний diff або візуальний аналіз).
4. Звітує про невідповідності з пропозиціями щодо виправлення.

**Вивід Claude**:
```markdown
## Visual Regression Report

### ✅ Matching (5/7)
- Button/Primary/Default
- Button/Primary/Hover
- Button/Secondary/Default
...

### ❌ Mismatches (2/7)

#### Button/Primary/Disabled
- **Issue**: Text opacity 0.4 in code, 0.5 in Figma
- **Fix**: Update `disabled:opacity-50` → `disabled:opacity-40`
- **File**: `src/components/Button.tsx:23`

#### Button/Large
- **Issue**: Padding 12px in code, 16px in Figma
- **Fix**: Update `py-3` → `py-4` (16px)
- **File**: `src/components/Button.tsx:18`
```

---

## Налаштування Code Connect

**Code Connect** — це інструмент Figma без написання коду для пов'язування компонентів дизайну з фрагментами коду. Це покращує здатність Claude генерувати правильний код.

### Що це робить

- Дизайнери анотують компоненти Figma прикладами коду.
- Claude зчитує ці анотації через MCP.
- Згенерований код автоматично відповідає стандартам вашої команди.

### Налаштування (для дизайнерів)

1. У Figma Dev Mode → Виберіть компонент → Панель Code Connect.
2. Додайте фрагмент коду, що показує, як використовується компонент:

```tsx
// Example Code Connect annotation in Figma
<Button variant="primary" size="lg">
  Click me
</Button>
```

3. Claude бачить це, коли отримує завдання реалізувати компонент, і використовує точні патерни вашої команди.

### Переваги

| Без Code Connect | З Code Connect |
|---------------------|-------------------|
| Claude генерує узагальнений код | Claude використовує стандарти команди |
| Неузгоджені назви props | Props точно відповідають варіантам Figma |
| Вимагає ручного виправлення | Готовий до продакшену код із першої спроби |

**Посилання**: Детальніше читайте на [parallelhq.com/blog](https://parallelhq.com/) (стаття про інтерфейс Code Connect).

---

## Альтернатива: Pencil (IDE-вбудоване полотно)

**Огляд**: [Pencil](https://pencil.dev) приносить нескінченне дизайнерське полотно безпосередньо в Claude Code/Cursor/VSCode, усуваючи необхідність перемикатися на зовнішні інструменти та забезпечуючи робочі процеси в парадигмі «дизайн як код».

### Архітектура

**Ключова інновація**: На відміну від Figma (хмарний сервіс) або Excalidraw (окремий додаток), Pencil вбудовує полотно дизайну безпосередньо у вашу IDE, де працює Claude і зберігається ваш код.

```
Traditional Workflow:
Figma (design) → Export → Claude Code → Implementation → Manual sync

Pencil Workflow:
IDE Canvas (design + AI agents + code) → Git commit → Continuous alignment
```

**Ключові особливості**:
- **Полотно WebGL**: нескінченне, продуктивне, повністю редаговане.
- **Мультиплеєрні AI-агенти**: паралельні агенти спільно опрацьовують дизайн.
- **Нативна підтримка Git**: `.pen` файли (формат JSON) з версіонуванням пліч-о-пліч із кодом.
- **Двонаправлений MCP**: повний доступ на читання та запис (а не лише для читання, як у Figma MCP).
- **Імпорт із Figma**: пряме копіювання-вставка з Figma із збереженням векторів та стилів.

### Pencil проти Figma MCP

| Аспект | Pencil | Figma MCP |
|--------|--------|-----------|
| **Розташування** | Вбудовано в IDE (Cursor/VSCode/Claude Code) | Зовнішня хмара |
| **Формат** | `.pen` JSON (відкритий) | Власний бінарний |
| **Версіонування** | Нативне в Git (гілки/злиття/історія) | Хмарні версії Figma |
| **AI-агенти** | Мультиплеєрні паралельні | Однопотокові через MCP |
| **Спільна робота** | Код-орієнтована (розробники + дизайнери) | Дизайн-орієнтована (дизайнери + розробники) |
| **Доступ через MCP** | Двонаправлений (читання + запис) | Лише для читання |
| **Робочий процес** | Дизайн → Комміт → Код в одному середовищі | Дизайн → Експорт → Передача → Код |
| **Найкраще для** | Інженери-дизайнери, код-орієнтовані команди | Традиційний поділ на дизайнерів та розробників |
| **Зрілість** | Новий продукт (запущено в січні 2026) | Зрілий продукт (2024+) |
| **Ціноутворення** | Наразі безкоштовно, буде визначено в майбутньому | Freemium (доступний безкоштовний тариф) |

### Коли використовувати Pencil

✅ **Добре підходить**:
- Команда використовує Cursor або VSCode + Claude Code як основне середовище.
- Інженери-дизайнери почуваються комфортно з робочими процесами в терміналі/IDE.
- Проекти, що вимагають тісної синхронізації дизайну та коду (парадигма «дизайн як код»).
- Бажання мати нативне версіонування дизайну в git (захист гілок, відкати змін тощо).
- Бажання використовувати паралельних AI-агентів для автоматизації дизайну.

⚠️ **Слід ретельно зважити**:
- Традиційна команда дизайнерів (нетехнічна) → Figma може бути кращим вибором.
- Потрібен корпоративний рівень SLA/підтримки → Pencil ще розвивається.
- Складна дизайн-система з понад 50 компонентами → екосистема Figma є більш зрілою.
- Команда не використовує Cursor/VSCode → обмежена сумісність.

### Налаштування

1. **Встановіть розширення Pencil**:
   - Відвідайте [pencil.dev](https://pencil.dev).
   - Дотримуйтесь інструкцій для встановлення у Cursor/VSCode/Claude Code.
   - Створіть обліковий запис (наразі безкоштовно).

2. **Створіть перше полотно**:
   ```bash
   # Відкрийте IDE, запустіть розширення Pencil
   # Створіть новий файл .pen у вашому репозиторії
   # Створюйте дизайн на нескінченному полотні
   ```

3. **Робочий процес Git**:
   ```bash
   git add design/homepage.pen
   git commit -m "feat(design): add homepage hero section"
   git push
   ```

4. **Інтеграція з Claude**:
   - Claude може читати `.pen` файли через MCP.
   - Промпт: "Implement the Button component from design/components.pen"
   - Claude витягує специфікації дизайну та генерує код.

### Приклад промпту

```
Read the "Hero Section" from design/homepage.pen.

Implement as React component with:
- Responsive behavior matching canvas breakpoints
- Animations from design (fade-in, slide-up)
- Copy exactly as specified in canvas
- Use Tailwind for styling

Ensure pixel-perfect match with design specs.
```

### Засновник та фінансування

**Tom Krcha** (CEO, Pencil):
- Співзасновник Adobe XD (2014-2018), 10 років роботи в Adobe.
- Попередні успішні виходи (exits): Alter Avatars (придбано Google), Around (придбано Miro).
- Понад 14 років досвіду розробки.

**Фінансування**: a16z Speedrun (~$1M) + KAYA VC

**Популярність**: 1M+ переглядів під час запуску, тисячі реєстрацій, включно з топ-менеджерами Microsoft, Shopify, Uber.

### Примітка щодо зрілості

**⚠️ Статус**: Запущено в січні 2026 року (зовсім нещодавно). Сильні ранні сигнали, але документація та екосистема ще формуються.

**Рекомендації**:
- **Проекти у продакшені**: Спочатку проведіть пілотний проект із 1-2 некритичними функціями.
- **Нові проекти**: Безпечно для впровадження командами, що використовують Cursor/Claude Code.
- **Традиційні робочі процеси**: Залишайтеся на Figma MCP, поки Pencil не стане більш зрілим (3-6 місяців).
- **Моніторинг**: Анонс ціноутворення, публічний репозиторій GitHub, зріла документація очікуються у другому кварталі 2026 року.

---

## Приклади промптів

### Реалізація компонента
```
Implement the "Card/Product" component from our Figma design system:
[Figma URL]

Requirements:
- Use our existing design tokens from tailwind.config.ts
- Include hover states matching Figma interactions
- Implement all variants (default, featured, compact)
- Add TypeScript types for all props
```

### Розширення дизайн-системи
```
Our design team added a new "Badge" component to Figma:
[Figma URL → Badge frame]

Generate:
1. React component with all variants
2. Storybook stories
3. Unit tests for prop combinations
4. Update design system docs
```

### Валідація токенів
```
Compare the color tokens in our Tailwind config against
Figma variables from: [Figma URL]

Report any mismatches and generate update script.
```

### Адаптивна реалізація
```
Implement the "Hero" section from Figma with exact responsive behavior:
[Figma URL → Hero/Responsive frame]

Figma has 3 breakpoints configured. Match these precisely.
```

### Аудит доступності (Accessibility)
```
Review the "Modal" component implementation against Figma specs:
[Figma URL]

Check:
- Focus management matches Figma's interaction flow
- Color contrast meets WCAG AA (Figma has contrast checker)
- Keyboard navigation (Figma annotations specify tab order)
```

### QA дизайну перед передачею в розробку
```
Review the "Checkout Flow" frames for implementation readiness:
[Figma URL → Checkout Flow page]

Check:
- All interactive states defined (hover, focus, disabled, error)
- Variables used consistently (no magic values)
- Auto Layout constraints are implementable
- Missing anything needed for production code?
```

### Атомарна реалізація кількох компонентів
```
Implement the atomic design system components in order:

1. Atoms: [Figma URL → Atoms page]
   - Button, Input, Label, Badge

2. Molecules: [Figma URL → Molecules page]
   - FormField (Label + Input + Error)
   - SearchBar (Input + Button)

3. Organisms: [Figma URL → Organisms page]
   - LoginForm (using molecules)

Ensure each level only imports from lower levels.
```

---

## Шаблони впровадження в команду

### Для продуктових дизайнерів

**Новий робочий процес**:
1. Створення дизайну у Figma з правильною структурою змінних.
2. Використання Figma Make для швидкого прототипування.
3. Експорт у Figma Design з увімкненим Dev Mode.
4. Спільний доступ до URL файлу + конкретних frames з командою розробки.
5. Claude зчитує дизайн → Генерує реалізацію.
6. Дизайнер візуально перевіряє вихідний код (не читаючи сам код).

**Ключовий інсайт**: Дизайнерам не потрібно вчитися програмувати. Вони перевіряють реалізацію шляхом візуального порівняння з Figma.

### Для розробників

**Новий робочий процес**:
1. Отримання URL-адреси Figma від дизайнера.
2. Промпт для Claude щодо реалізації на основі джерела у Figma.
3. Перегляд згенерованого коду на відповідність архітектурі.
4. Запуск візуального порівняння (Playwright або вручну).
5. Комміт готового до продакшену компонента.

**Збережений час**: Пропустіть ручну реалізацію «піксель-в-піксель». Фокусуйтеся на логіці, а не на верстці макетів.

### Для менеджерів продуктів (PM)

**Нова можливість**: Запит оцінки складності реалізації дизайну на основі frames Figma.

**Промпт для PM**:
```
Review the "Dashboard Redesign" Figma file:
[Figma URL]

Estimate implementation complexity:
- How many new components needed?
- Which existing components can be reused?
- Any technical blockers?

Provide rough timeline for dev implementation.
```

**Вивід Claude**:
```markdown
## Implementation Analysis

### Scope
- 12 frames total
- 4 new components (DataTable, MetricCard, FilterPanel, DateRangePicker)
- 8 existing components reused

### Complexity Assessment
- **Low**: MetricCard (similar to existing Card, 1-2h)
- **Medium**: FilterPanel (multi-select logic, 4-6h)
- **High**: DataTable (sorting, pagination, virtualization, 2-3 days)
- **High**: DateRangePicker (third-party library integration, 1-2 days)

### Technical Considerations
- DataTable needs backend API for server-side pagination
- DateRangePicker: evaluate date-fns vs dayjs vs native
- FilterPanel state management (local vs global)

### Estimated Timeline
- Development: 5-7 days
- Code review + QA: 2 days
- Total: 1.5-2 weeks
```

---

## Антипатерни

| ❌ Антипатерн | Чому це не працює | ✅ Правильний підхід |
|----------------|-------------|-------------------|
| **Ручне переписування дизайну** | Схильне до помилок, забирає багато часу, розбіжності неминучі | Дозвольте Claude читати Figma безпосередньо через MCP |
| **Скріншоти як специфікація** | Немає даних про токени, відсутня інтерактивність, неоднозначно | Діліться URL Figma, надавайте Claude доступ до структурованих даних |
| **Зашиті (hardcoded) значення** | Ламається при оновленні дизайн-системи | Використовуйте дизайн-токени зі змінних Figma |
| **Дизайнер пише код** | Неефективне використання навичок дизайнера | Дизайнер малює дизайн → Claude пише код → Розробник перевіряє |
| **Розробник вгадує відступи** | Не відповідає дизайн-системі | Claude витягує точні значення з Figma |
| **Відсутність анотацій Code Connect** | Узагальнений вивід коду | Анотуйте один раз → Claude використовуватиме стандарти команди |
| **Пропуск візуального порівняння** | Розбіжності в реалізації | Завжди перевіряйте на відповідність першоджерелу у Figma |
| **Невідповідність імен токенів** | Змінні Figma ≠ токени в коді | Встановіть правила іменування, використовуйте Style Dictionary |
| **Відсутність адаптивних специфікацій** | Розробник вгадує точки зупину (breakpoints) | У Figma є адаптивні frames → Claude зчитує точні специфікації |
| **Однорівневі токени** | Негнучкі, важко створювати теми | Використовуйте 3-рівневу ієрархію (base/composite/semantic) |

---

## План впровадження (Roadmap)

### Фаза 1: Фундамент (Тиждень 1-2)

**Мета**: Базовий конвеєр Figma → Claude → Код

- [ ] Встановити Figma MCP Server.
- [ ] Налаштувати персональний токен доступу.
- [ ] Перевірити з'єднання: Claude зчитує публічний файл Figma.
- [ ] Створити проектний CLAUDE.md з конвенціями дизайн-системи.
- [ ] Реалізувати 3-5 простих компонентів (Button, Input, Badge).
- [ ] Встановити процес візуального QA (ручне порівняння).

**Критерії успіху**:
- Claude генерує компонент із URL Figma.
- Результат візуально відповідає дизайну.
- Команда розробників розуміє робочий процес.

---

### Фаза 2: Масштабування (Тиждень 3-4)

**Мета**: Повна реалізація дизайн-системи + автоматизація

- [ ] Реалізувати 20+ компонентів із бібліотеки Figma.
- [ ] Налаштувати автоматизацію токенів (Tokens Studio + Style Dictionary).
- [ ] Створити набір тестів компонентів (Storybook + візуальна регресія).
- [ ] Навчити дизайнерів гігієні роботи зі змінними.
- [ ] Документувати конвенції команди в CLAUDE.md.
- [ ] Запустити перший аудит відхилень від дизайн-системи.

**Критерії успіху**:
- 80%+ компонентів UI генеруються автоматично.
- Оновлення токенів поширюються автоматично.
- Дизайнери впевнені в процесі передачі макетів.

---

### Фаза 3: Оркестрація (Тиждень 5+)

**Мета**: Робочі процеси з кількома MCP + безперервна синхронізація

- [ ] Інтегрувати Playwright MCP для автоматизованого візуального тестування.
- [ ] Налаштувати CI/CD для перевірки паритету дизайну та коду.
- [ ] Створити конвеєр Figma → GitHub → Продакшен.
- [ ] Впровадити управління дизайн-системою (лінтинг, аудити).
- [ ] Дозволити не-розробникам запускати реалізацію через Claude (тікети, Slack).
- [ ] Вимірювати метрики (TTM, коефіцієнт невідповідностей, збережений час розробки).

**Критерії успіху**:
- Оновлення дизайну → Продакшен менш ніж за 1 день.
- Нуль ручного переписування дизайну.
- Вимірюване збільшення швидкості роботи команди.

---

## Джерела

### Офіційна документація

- **Figma MCP Server**: [@modelcontextprotocol/server-figma](https://github.com/modelcontextprotocol/servers/tree/main/src/figma) (GitHub)
- **Figma Developer Docs**: [figma.com/developers](https://www.figma.com/developers)
- **Style Dictionary**: [amzn.github.io/style-dictionary](https://amzn.github.io/style-dictionary/)
- **Tokens Studio Plugin**: [tokens.studio](https://tokens.studio/)

### Кейс-стаді та навчальні посібники

- **builder.io**: "Claude Code + Figma MCP Server: AI Design-to-Code Workflow" (січень 2026)
  - [builder.io/blog/claude-code-figma-mcp-server](https://www.builder.io/blog/claude-code-figma-mcp-server)
  - Виробничі метрики, приклади робочих процесів.
- **Vladimir Siedykh**: "Multi-MCP Orchestration with Claude Code"
  - [vladimirsiedykh.com/blog/claude-code-mcp-workflow](https://vladimirsiedykh.com/)
  - Інтеграція Figma + Playwright + Linear.
- **Parallel HQ**: "Automating Design Systems with AI"
  - [parallelhq.com/blog/automating-design-systems-with-ai](https://parallelhq.com/)
  - 75 збережених днів, посібник з Code Connect UI.
- **Composio**: "How to Use Figma MCP with Claude Code"
  - [composio.dev/blog/how-to-use-figma-mcp-with-claude-code](https://composio.dev/)
  - Патерни ієрархії токенів, посібник із налаштування.

### Ресурси спільноти

- **Figma Community**: Шукайте "Design System Tokens" для стартових шаблонів.
- **MCP Registry**: [mcp.run](https://mcp.run/) → приклади серверів Figma.
- **Discord**: Anthropic Discord → канал #mcp-servers.

### Пов'язані робочі процеси

- [Робота із зображеннями](#working-with-images-and-screenshots) — аналіз зображень у Claude Code.
- [ASCII Art & Wireframing](#wireframing-tools-for-ai-development) — низькодеталізовані ітерації дизайну.
- [Playwright MCP](#playwright-browser-automation) — тестування візуальної регресії.

---

## Дивіться також

- [Розділ Figma MCP](#figma-mcp-integration) — основний розділ посібника Figma MCP.
- [examples/claude-md/product-designer.md](../../examples/claude-md/product-designer.md) — шаблон `CLAUDE.md` для продуктового дизайнера.
- [../cheatsheet.md](../cheatsheet.md) — швидка довідка.

---
**Локалізація**: [Serhii (MacPlus Software)](https://macplus-software.com)
*Остання синхронізація: Травень 2026*
