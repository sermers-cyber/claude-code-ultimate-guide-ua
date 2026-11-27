---
name: learn-teach
description: Покрокове пояснення концепції з поступовим поглибленням
argument-hint: <concept>
effort: low
---

# Навчи мене

Покрокове пояснення концепції з поступовим поглибленням.

## Використання

```
/learn:teach React hooks         # Learn about React hooks
/learn:teach async/await         # Understand async patterns
/learn:teach SOLID principles    # Learn design principles
/learn:teach --deep SQL joins    # In-depth explanation
```

## Інструкції

1. Почніть із **визначення одним реченням**
2. Поясніть, **чому це важливо** (яку реальну проблему це розв'язує)
3. Покажіть **мінімальний приклад** (найпростіший можливий код)
4. Розберіть **кожну частину** прикладу з коментарями
5. Покажіть **практичний приклад** (реальний випадок використання)
6. Виділіть **типові помилки** початківців
7. Запропонуйте **наступні концепції** для вивчення

## Формат відповіді

```markdown
## [Назва концепції]

**Одним реченням**: [Чітке, просте визначення]

### Чому це важливо

[1-2 речення про проблему, яку це розв'язує]

### Мінімальний приклад

\`\`\`[language]
// Simplest possible demonstration
[code]
\`\`\`

**Рядок за рядком**:
- Рядок 1: [пояснення]
- Рядок 2: [пояснення]
...

### Практичний приклад

\`\`\`[language]
// Real-world scenario
[code]
\`\`\`

### Типові помилки

1. **[Помилка]**: [Чому це неправильно і що робити натомість]
2. **[Помилка]**: [Чому це неправильно і що робити натомість]

### Ключові висновки

- [Пункт 1]
- [Пункт 2]
- [Пункт 3]

### Що вивчати далі

- [Пов'язана концепція 1]: [чому вона пов'язана]
- [Пов'язана концепція 2]: [чому вона пов'язана]

---

**Практичне завдання**: [Невелика вправа для закріплення концепції]
```

## Режими глибини

### За замовчуванням
- Визначення одним реченням
- Один мінімальний приклад
- Один практичний приклад
- 2-3 типові помилки

### `--deep`
- Розширене пояснення з історією/контекстом
- Кілька прикладів зростаючої складності
- Граничні випадки й підводні камені
- Міркування щодо продуктивності
- Порівняння з альтернативами
- Деталі, важливі для співбесід

### `--quick`
- Лише визначення
- Один приклад
- Без додатків

## Правила адаптації

### Для початківців
- Використовуйте аналогії з повсякденного життя
- Уникайте жаргону (або одразу його пояснюйте)
- Більше коментарів у коді
- Менші приклади коду

### Для середнього рівня
- Припускайте знання базового синтаксису
- Зосереджуйтеся на «чому», а не на «що»
- Включайте компроміси
- Показуйте ідіоматичні патерни

### Для складних тем
- Посилайтеся на офіційну документацію
- Обговорюйте внутрішню реалізацію, коли доречно
- Включайте наслідки для продуктивності
- Згадуйте пов'язані патерни

## Приклад сесії

```
User: /learn:teach useEffect

Claude: ## useEffect

**In one sentence**: useEffect lets you run side effects (data fetching, subscriptions, DOM changes) after React renders a component.

### Why It Matters

React components are pure functions that render UI. But real apps need to interact with the outside world: APIs, browser events, timers. useEffect is the bridge between React's declarative world and imperative side effects.

### Minimal Example

\`\`\`jsx
import { useEffect, useState } from 'react';

function Timer() {
  const [seconds, setSeconds] = useState(0);

  useEffect(() => {
    const id = setInterval(() => {
      setSeconds(s => s + 1);
    }, 1000);

    return () => clearInterval(id);  // Cleanup
  }, []);  // Empty array = run once

  return <div>{seconds}s</div>;
}
\`\`\`

**Line by line**:
- `useEffect(() => {...}, [])`: Run this function after first render
- `setInterval(...)`: Start a timer (side effect)
- `return () => clearInterval(id)`: Cleanup when component unmounts
- `[]`: Empty dependency array = only run on mount

### Common Mistakes

1. **Missing dependency array**: Without `[]`, effect runs on EVERY render
2. **Forgetting cleanup**: Intervals/subscriptions leak without return function
3. **Stale closures**: Using old state values instead of functional updates

---

**Practice challenge**: Add a pause button that stops and resumes the timer.
```

## Теми, добре придатні для /learn:teach

| Категорія | Приклади |
|----------|----------|
| **React** | hooks, context, suspense, server components |
| **JavaScript** | closures, promises, event loop, prototypes |
| **TypeScript** | generics, mapped types, utility types |
| **Патерни** | SOLID, DI, композиція, фабрики |
| **Бекенд** | REST, GraphQL, автентифікація, кешування |
| **Бази даних** | індекси, joins, транзакції, нормалізація |
| **DevOps** | контейнери, CI/CD, інфраструктура як код |

$ARGUMENTS
