---
name: learn-alternatives
description: Порівняти різні підходи до розв'язання однієї й тієї самої задачі
argument-hint: "[topic]"
effort: low
---

# Показати альтернативи

Порівняйте різні підходи до розв'язання однієї й тієї самої задачі.

## Використання

```
/learn:alternatives              # Compare approaches for current code
/learn:alternatives auth         # Compare authentication methods
/learn:alternatives state        # Compare state management options
/learn:alternatives --detailed   # Include code examples for each
```

## Інструкції

1. Визначте **задачу, що розв'язується** (з контексту або аргументу)
2. Наведіть **3-5 альтернативних підходів**
3. Для кожного підходу поясніть:
   - Що це (одне речення)
   - Коли його використовувати
   - Компроміси (плюси/мінуси)
4. Дайте **рекомендацію** з урахуванням контексту
5. За бажанням покажіть приклади коду для найкращих варіантів

## Формат відповіді

```markdown
## Задача: [Що ми намагаємося розв'язати]

### Підхід 1: [Назва]

**Що це**: [Опис одним реченням]

**Коли використовувати**:
- [Сценарій 1]
- [Сценарій 2]

**Плюси**: [Список]
**Мінуси**: [Список]

---

### Підхід 2: [Назва]
...

---

## Порівняльна таблиця

| Критерій | Підхід 1 | Підхід 2 | Підхід 3 |
|----------|------------|------------|------------|
| Складність | Низька | Середня | Висока |
| Продуктивність | ★★☆ | ★★★ | ★★☆ |
| Розмір бандла | Малий | Середній | Великий |
| Крива навчання | Легка | Середня | Крута |

## Рекомендація

**Для вашого випадку**: [Рекомендований підхід], тому що [причина, що ґрунтується на контексті]

**Натомість розгляньте, якщо**: [Альтернативні сценарії]
```

## Критерії порівняння

Стандартні критерії для оцінювання (коригуйте залежно від задачі):

| Критерій | Опис |
|----------|-------------|
| **Складність** | Наскільки важко реалізувати й підтримувати |
| **Продуктивність** | Швидкість виконання, використання пам'яті |
| **Розмір бандла** | Вплив на фронтенд-бандл |
| **Крива навчання** | Час, потрібний, щоб зрозуміти й правильно використовувати |
| **Гнучкість** | Легкість розширення чи зміни |
| **Спільнота** | Документація, екосистема, підтримка |
| **Тестування** | Наскільки легко тестувати |
| **Типобезпека** | Якість підтримки TypeScript |

## Режими глибини

### За замовчуванням
- 3-4 альтернативи
- Короткий опис кожної
- Порівняльна таблиця
- Рекомендація

### `--detailed`
- 4-5 альтернатив
- Приклад коду для кожної
- Докладні компроміси
- Міркування щодо міграції
- Реальні кейси

### `--quick`
- 2-3 альтернативи
- По одному рядку на кожну
- Швидка рекомендація

## Приклад сесії

```
User: I'm using useState for form state. /learn:alternatives

Claude: ## Problem: Managing Form State in React

### Approach 1: Multiple useState

**What**: Separate useState for each field

**When to use**:
- Simple forms (< 5 fields)
- No complex validation
- No cross-field dependencies

**Pros**: Simple, no dependencies, easy to understand
**Cons**: Verbose with many fields, scattered state

---

### Approach 2: Single useState with Object

**What**: One useState holding all fields as object

**When to use**:
- Medium forms (5-10 fields)
- Need to reset entire form
- Want cleaner code

**Pros**: Grouped state, easy reset, cleaner
**Cons**: Need spread operator, can cause unnecessary re-renders

---

### Approach 3: useReducer

**What**: Reducer pattern for complex state transitions

**When to use**:
- Complex validation logic
- Multi-step forms
- Undo/redo functionality

**Pros**: Predictable updates, handles complex logic, testable
**Cons**: More boilerplate, learning curve

---

### Approach 4: Form Library (React Hook Form, Formik)

**What**: Dedicated form state management library

**When to use**:
- Large forms (10+ fields)
- Complex validation (async, cross-field)
- Performance critical (many fields)

**Pros**: Optimized re-renders, validation built-in, less code
**Cons**: Dependency, learning curve, bundle size

---

## Comparison Table

| Criteria | useState | useReducer | React Hook Form |
|----------|----------|------------|-----------------|
| Complexity | Low | Medium | Medium |
| Performance | ★★☆ | ★★☆ | ★★★ |
| Bundle size | 0kb | 0kb | ~8kb |
| Validation | Manual | Manual | Built-in |
| Best for | Simple | Complex logic | Large forms |

## Recommendation

**For your case**: If this is a simple login/contact form, stick with **useState**. If you're building a multi-step checkout or admin form, consider **React Hook Form** for the validation and performance benefits.

**Consider useReducer if**: You need undo/redo, complex state machines, or want reducer-style testing.
```

## Типові порівняння альтернатив

| Тема | Типові альтернативи |
|-------|---------------------|
| **Стан** | useState, useReducer, Zustand, Redux, Jotai |
| **Стилізація** | CSS Modules, Tailwind, styled-components, CSS-in-JS |
| **Отримання даних** | fetch, axios, React Query, SWR |
| **Форми** | useState, React Hook Form, Formik |
| **Автентифікація** | JWT, сесії, OAuth, magic links |
| **Дизайн API** | REST, GraphQL, tRPC, gRPC |
| **Тестування** | Jest, Vitest, Testing Library, Cypress |
| **Бази даних** | PostgreSQL, MySQL, MongoDB, SQLite |

$ARGUMENTS
