---
title: "Шаблон CLAUDE.md для продуктового дизайнера"
description: "Конфігурація CLAUDE.md для воркфлоу «дизайн у код» з Figma MCP"
tags: [claude-md, template, design-patterns, mcp]
---

# Шаблон CLAUDE.md для продуктового дизайнера

Конфігурація CLAUDE.md, оптимізована для воркфлоу «дизайн у код» з Figma MCP.

## Використання

Скопіюйте цей вміст у файл `CLAUDE.md` свого проєкту й налаштуйте розділи, позначені `[квадратними дужками]`.

---

## Шаблон

```markdown
# Конфігурація проєкту продуктового дизайнера

## Джерело дизайн-системи

### Файли Figma
- Бібліотека дизайн-системи: [URL файлу Figma]
- Бібліотека компонентів: [URL файлу Figma]
- Поточний проєкт: [URL файлу Figma]

### Доступ
- Figma MCP налаштовано: Так/Ні
- Personal Access Token: [налаштовано в параметрах MCP - ніколи не розголошуй значення]
- Доступ до Dev Mode: [потрібен для повного перегляду змінних]

## Ієрархія токенів

Наші design tokens мають 3-рівневу структуру:

### Базові токени (примітиви)
Figma Variables → CSS Custom Properties
- Кольори: `--blue-600`, `--gray-100` тощо
- Відступи: `--spacing-1` (4px), `--spacing-2` (8px) тощо
- Типографіка: `--font-size-sm`, `--font-weight-medium` тощо
- Радіуси: `--radius-sm`, `--radius-md` тощо

### Складені токени
Комбінації примітивів, що використовуються в компонентах
- Padding кнопки: `var(--spacing-2) var(--spacing-4)`
- Тінь картки: `var(--shadow-md)`
- Рамка поля вводу: `var(--border-width-1) solid var(--border-default)`

### Семантичні токени
Значення, залежне від контексту
- `--interactive-primary`: колір основної дії
- `--surface-elevated`: тло карток/модальних вікон
- `--text-secondary`: описовий текст
- `--border-error`: валідація форм

## Правила дизайну

### Кольори
- Primary: [#HEX] → `var(--interactive-primary)`
- Secondary: [#HEX] → `var(--interactive-secondary)`
- Ніколи не використовуй: жорстко прописані hex-значення в компонентах
- Завжди використовуй: змінні design tokens

### Відступи
- Базова одиниця: [4px/8px]
- Шкала: [4, 8, 12, 16, 24, 32, 48, 64, 96]
- Ніколи не використовуй: магічні числа (наприклад, `padding: 13px`)
- Завжди використовуй: кратні токенам значення (наприклад, `var(--spacing-3)`)

### Типографіка
- Сімейство шрифтів: [Inter/Roboto/System/Custom]
- Шкала: [12, 14, 16, 18, 20, 24, 32, 48, 64]
- Висота рядка: [1.2, 1.5, 1.6] залежно від розміру тексту
- Міжлітерний інтервал: точно дотримуйся текстових стилів Figma

### Адаптивні breakpoints
Відповідно до розмірів фреймів Figma:
- Мобільний: [320-767px]
- Планшет: [768-1023px]
- Десктоп: [1024px+]
- Максимальна ширина: [1440px]

## Команди Figma MCP

Коли я ділюся URL Figma, ти можеш використовувати ці команди MCP:

### Читання файлів дизайну
```
figma_get_file(file_key: string)
→ Повертає: структуру файлу, сторінки, фрейми
```

### Витягування стилів
```
figma_get_styles(file_key: string)
→ Повертає: стилі кольорів, текстові стилі, стилі ефектів
```

### Отримання компонентів
```
figma_get_component(file_key: string, node_id: string)
→ Повертає: властивості компонента, варіанти, design tokens
```

### Змінні (design tokens)
```
figma_get_variables(file_key: string)
→ Повертає: усі змінні Figma (примітиви)
```

## Відповідності Code Connect

Ми використовуємо Figma Code Connect, щоб пов'язувати дизайн із кодом. Під час реалізації компонентів спирайся на ці відповідності:

| Компонент Figma | Шлях у коді | Примітки |
|-----------------|-----------|-------|
| Button/Primary | `components/Button/Primary.tsx` | Використовує компонент `PrimaryButton` |
| Input/Text | `components/Input/Text.tsx` | Підтримує стани помилок |
| Card/Default | `components/Card/index.tsx` | Auto Layout → Flexbox |
| Modal/Standard | `components/Modal/Standard.tsx` | Focus trap + A11y |

[Додайте сюди свої відповідності]

## Обмеження реалізації

### Технологічний стек
- Фреймворк: [React/Vue/Svelte/Angular]
- Стилізація: [Tailwind/CSS Modules/Styled Components/CSS-in-JS]
- TypeScript: [обов'язково/необов'язково]
- Бібліотека компонентів: [власна / MUI/Chakra тощо]

### Патерни
- Структура компонентів: [Atomic Design / за функціями / пласка]
- Керування станом: [useState / Context / Redux / Zustand]
- Іменування props: [точно відповідає варіантам Figma]

### Вимоги до якості
- Типи TypeScript для всіх props
- Доступність за замовчуванням (мінімум WCAG AA)
- Адаптивна поведінка відповідно до фреймів Figma
- Стани hover/focus/disabled з Figma

## Чекліст передавання дизайну

Коли реалізуєш компонент із Figma, перевір:

### Відповідність дизайну
- [ ] Кольори точно відповідають Figma (використовуй піпетку кольорів у DevTools браузера)
- [ ] Відступи відповідають вимірам у Figma
- [ ] Типографіка (розмір, насиченість, висота рядка) відповідає
- [ ] Радіус заокруглення відповідає
- [ ] Тіні/ефекти відповідають

### Токени
- [ ] Жодних жорстко прописаних кольорів (усі через `var(--token-name)`)
- [ ] Жодних відступів-магічних чисел
- [ ] Розміри шрифтів використовують design tokens
- [ ] Усі значення простежуються до дизайн-системи

### Адаптивність
- [ ] Реалізовано мобільний breakpoint
- [ ] Реалізовано планшетний breakpoint
- [ ] Десктопний макет відповідає
- [ ] Немає горизонтальної прокрутки на мобільних

### Доступність
- [ ] Навігація з клавіатури працює
- [ ] Стани фокуса видимі
- [ ] ARIA-мітки є там, де потрібно
- [ ] Контрастність кольорів проходить WCAG AA
- [ ] Протестовано зі скрінрідером (якщо елемент інтерактивний)

### Стани
- [ ] Реалізовано стан default
- [ ] Стан hover відповідає Figma
- [ ] Стан focus відповідає Figma
- [ ] Стан disabled відповідає Figma
- [ ] Стан помилки (якщо застосовно)
- [ ] Стан завантаження (якщо застосовно)

## Вподобання щодо відповідей

### Для реалізації компонентів
1. Прочитай компонент Figma через MCP
2. Витягни всі варіанти й властивості
3. Зістав design tokens із токенами в коді
4. Згенеруй компонент TypeScript з повними типами
5. Додай story для Storybook (якщо ми використовуємо Storybook)
6. Перевір за чеклістом вище

### Для аудитів дизайн-системи
1. Порівняй кодову базу з Figma як джерелом істини
2. Повідом про жорстко прописані значення (кольори, відступи тощо)
3. Познач невідповідності (відсутні варіанти, неправильні токени)
4. Запропонуй автоматизовані виправлення

### Для оновлень токенів
1. Коли design tokens змінюються у Figma, повідом про зачеплені компоненти
2. Згенеруй скрипт міграції, якщо зміни ламають сумісність
3. Перевір, що жодні жорстко прописані значення не зламаються

## Командні домовленості

### Повідомлення комітів
- Формат: `feat(ui): add Button component from Figma`
- Посилання на фрейм Figma: `feat(ui): implement Modal (Figma frame: abc123)`

### Вимоги до PR
- [ ] Порівняння скриншотів (код і Figma)
- [ ] Усі пункти чекліста перевірено
- [ ] Адаптивну поведінку протестовано
- [ ] Доступність перевірено

### Документація компонентів
Кожен компонент має документувати:
- Джерело у Figma (URL + ID фрейму)
- Коли востаннє синхронізовано з дизайном
- Будь-які відхилення від дизайну (з обґрунтуванням)
```

---

## Посібник із налаштування

### Для проєктів React + Tailwind

Додайте до «Технологічного стеку»:
```markdown
### Конфігурація Tailwind
- Файл конфігурації: `tailwind.config.ts`
- Власні утиліти: `src/styles/utilities.css`
- Design tokens зіставлено в: об'єкті `theme.extend`

### Патерн компонента
```tsx
// components/Button/Primary.tsx
import { cn } from '@/lib/utils';

interface ButtonProps {
  size?: 'sm' | 'md' | 'lg';
  disabled?: boolean;
  children: React.ReactNode;
}

export function PrimaryButton({ size = 'md', disabled, children }: ButtonProps) {
  return (
    <button
      className={cn(
        // Base styles
        'rounded-md font-medium transition-colors',
        // Semantic tokens
        'bg-interactive-primary text-white',
        'hover:bg-interactive-primary-hover',
        // States
        'disabled:opacity-50 disabled:cursor-not-allowed',
        // Size variants
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
```

### Для дизайн-системи з Tokens Studio

Додайте розділ:
```markdown
## Автоматизація токенів

### Налаштування Tokens Studio
- Плагін підключено до: [URL репозиторію GitHub]
- Гілка: `design-tokens`
- Частота синхронізації: [під час збереження / вручну / CI/CD]

### Формат експорту токенів
```json
{
  "color": {
    "blue": {
      "600": {
        "value": "#0066CC",
        "type": "color"
      }
    }
  },
  "spacing": {
    "2": {
      "value": "8px",
      "type": "spacing"
    }
  }
}
```

### Перетворення Style Dictionary
- Конфігурація: `style-dictionary.config.js`
- Вихід: каталог `src/tokens/`
- Платформи: CSS, Tailwind, iOS, Android
```

### Для команд, що використовують Storybook

Додайте до «Вподобань щодо відповідей»:
```markdown
### Для stories Storybook
Генеруй stories з усіма варіантами:

```tsx
// Button.stories.tsx
import type { Meta, StoryObj } from '@storybook/react';
import { PrimaryButton } from './Primary';

const meta: Meta<typeof PrimaryButton> = {
  title: 'Components/Button/Primary',
  component: PrimaryButton,
  parameters: {
    design: {
      type: 'figma',
      url: 'https://www.figma.com/file/[FILE_KEY]?node-id=[NODE_ID]',
    },
  },
};

export default meta;
type Story = StoryObj<typeof PrimaryButton>;

export const Default: Story = {
  args: {
    children: 'Click me',
    size: 'md',
  },
};

export const Small: Story = {
  args: {
    children: 'Small button',
    size: 'sm',
  },
};

// ... all variants from Figma
```
```

---

## Інтеграція з воркфлоу

Цей CLAUDE.md поєднується з воркфлоу «дизайн у код»:

- Прочитайте: [Воркфлоу «дизайн у код»](../../guide/workflows/design-to-code.uk.md)
- Зрозумійте: конвеєр Figma Make → Claude MCP → продакшн
- Застосуйте: використовуйте цю конфігурацію, щоб підтримувати відповідність між дизайном і кодом

---

## Приклади prompt

### Реалізувати компонент із Figma
```
Реалізуй компонент "Card/Product" з нашої дизайн-системи у Figma:
[URL Figma]

Дотримуйся чекліста передавання дизайну.
Використовуй наші домовленості щодо токенів із цього CLAUDE.md.
Згенеруй компонент TypeScript з усіма варіантами.
```

### Аудит розбіжностей із дизайн-системою
```
Перевір src/components на відповідність нашій дизайн-системі у Figma:
[URL Figma]

Звіт:
1. Жорстко прописані значення без токенів
2. Відсутні варіанти, які є у Figma
3. Непослідовні відступи/кольори
4. Запропонуй виправлення
```

### Оновити компонент після зміни дизайну
```
Компонент Button оновлено у Figma:
[URL Figma → фрейм Button]

Переглянь зміни, онови код відповідно.
Забезпеч зворотну сумісність, якщо можливо.
Онови stories у Storybook, якщо потрібно.
```

---

## Див. також

- [Воркфлоу «дизайн у код»](../../guide/workflows/design-to-code.uk.md): повний посібник із воркфлоу Figma MCP
- [Розділ про Figma MCP](../../guide/ultimate-guide.uk.md#figma-mcp-integration): технічні подробиці
- [Робота із зображеннями](../../guide/ultimate-guide.uk.md#working-with-images-and-screenshots): основи візуального аналізу
