---
name: learn-quiz
description: Перевірити розуміння нещодавно написаного або прийнятого коду
argument-hint: "[topic] [--hard]"
effort: low
---

# Перевір мене

Перевірте розуміння нещодавно написаного або прийнятого коду.

## Використання

```
/learn:quiz                     # Quiz on last code worked with
/learn:quiz error handling      # Focus on specific aspect
/learn:quiz --hard              # More challenging questions
```

## Інструкції

1. Визначте останній код, з яким я працював (написав, відредагував або прийняв від ШІ)
2. Згенеруйте 3-5 запитань, що перевіряють розуміння на різних рівнях:
   - **Відтворення**: що робить цей код?
   - **Розуміння**: чому обрано саме цей підхід?
   - **Застосування**: що станеться, якщо X зміниться?
   - **Аналіз**: які компроміси цього підходу?
   - **Синтез**: як би ви це розширили?
3. Ставте запитання по одному
4. Зачекайте на мою відповідь, перш ніж розкривати правильну
5. До кожної відповіді давайте пояснення, а не просто «правильно/неправильно»

## Типи запитань

### Рівень 1: Відтворення
- "What does the function X return?"
- "What parameters does Y accept?"
- "What happens when Z is called?"

### Рівень 2: Розуміння
- "Why do we use X instead of Y here?"
- "What problem does this pattern solve?"
- "Why is this line necessary?"

### Рівень 3: Застосування
- "What would happen if we removed line X?"
- "How would you add feature Y to this code?"
- "What would break if input Z was provided?"

### Рівень 4: Аналіз
- "What are the performance implications of this approach?"
- "What edge cases might cause issues?"
- "How does this compare to alternative X?"

### Рівень 5: Синтез
- "How would you refactor this for better testability?"
- "What would need to change to support X?"
- "Design an extension that adds Y"

## Напрями фокусу

Коли вказано фокус (наприклад, `/learn:quiz error handling`), надавайте пріоритет запитанням про:

| Фокус | Теми запитань |
|-------|-----------------|
| `error handling` | Try/catch, типи помилок, стратегії відновлення |
| `performance` | Big-O, оптимізація, вузькі місця |
| `security` | Валідація вводу, XSS, ін'єкції |
| `testing` | Тест-кейси, граничні випадки, мокінг |
| `architecture` | Патерни, розділення відповідальності, SOLID |
| `types` | Типи TypeScript, виведення, generics |

## Режими складності

### За замовчуванням
- 3 запитання
- Суміш рівнів 1-3
- Фокус на розумінні поточного коду

### `--hard`
- 5 запитань
- Рівні 3-5
- Включайте гіпотетичні модифікації
- Питайте про компроміси й альтернативи

## Формат відповіді

Для кожного запитання:

```
## Запитання 1 з 3

[Текст запитання]

Яка ваша відповідь?

---
(Після відповіді користувача)

### Зворотний зв'язок

[Чи правильно і чому]

**Ключова думка**: [Концепція, яку це перевіряє]

**Пов'язана концепція**: [Те, що варто дослідити далі]

Готові до наступного запитання?
```

## Після завершення вікторини

Підсумуйте:
- Результат: X/Y правильно
- Сильні сторони: [Теми, зрозумілі добре]
- Потребує повторення: [Теми, до яких варто повернутися]
- Рекомендована практика: [Конкретна вправа]

## Приклад сесії

```
User: /learn:quiz

Claude: Looking at your last code - the useEffect hook for data fetching.

## Question 1 of 3

In your useEffect, you have an empty dependency array [].
What does this mean for when the effect runs?

User: It runs only once when the component mounts

Claude: ### Feedback
Correct! An empty dependency array means the effect runs only on mount
(and cleanup on unmount).

**Key insight**: The dependency array controls WHEN effects re-run.

**Related concept**: What happens with no array vs. [someValue]?

Ready for Question 2?
```

## Поради для користувачів

1. **Будьте чесними**: неправильні відповіді дають можливість навчитися
2. **Пояснюйте свої міркування**: це допомагає виявити прогалини навіть у правильних відповідях
3. **Ставте уточнювальні запитання**: якщо зворотний зв'язок незрозумілий, копайте глибше
4. **Відстежуйте слабкі місця**: занотовуйте теми, що потребують більше практики

$ARGUMENTS
