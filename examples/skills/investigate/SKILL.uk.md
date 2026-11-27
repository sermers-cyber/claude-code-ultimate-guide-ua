---
name: investigate
description: "Систематичне налагодження за першопричиною: знайти причину, перш ніж писати будь-яке виправлення"
argument-hint: <issue_description>
effort: medium
disable-model-invocation: true
---

# Investigate: налагодження за першопричиною

Систематичне налагодження з обов'язковим дослідженням першопричини перед будь-якими змінами коду.

**Залізне правило: ЖОДНИХ ВИПРАВЛЕНЬ БЕЗ ПОПЕРЕДНЬОГО ДОСЛІДЖЕННЯ ПЕРШОПРИЧИНИ.**

Виправлення симптомів перетворює налагодження на гру «вдар крота». Кожне виправлення, що не усуває першопричину, ускладнює пошук наступного бага.

## Інструкції

### Фаза 1: Зібрати симптоми

Зберіть увесь доступний контекст, перш ніж формувати будь-яку гіпотезу.

1. Прочитайте повідомлення про помилки, стек-трейси та кроки відтворення повністю
2. Поставте ОДНЕ цілеспрямоване запитання, якщо користувач не надав достатньо контексту:
   - «Яке саме повідомлення про помилку ви бачите?»
   - «Чи можете ви стабільно це відтворити?»
   - «Коли це почало траплятися?»
3. Визначте уражений компонент і його межі

**Результат**: точне формулювання симптому: що ламається, коли, з якою помилкою.

---

### Фаза 2: Прочитати код

Простежте шлях виконання коду від симптому до потенційних причин. Не вгадуйте.

```bash
# Find all references to the failing component
grep -rn "ComponentName\|function_name\|error_string" src/ --include="*.{ts,js,py,rb,go}" | head -30

# Check recent changes to affected files
git log --oneline -15 -- <affected-file>

# Read the actual diff for each recent commit
git show <commit-hash> -- <affected-file>
```

Використовуйте Grep, щоб знайти всі посилання, і Read, щоб зрозуміти логіку. Ніколи не пропускайте читання коду.

---

### Фаза 3: Перевірити недавні зміни

```bash
# What changed recently across the whole repo
git log --oneline -20

# Changes to files related to the symptom
git log --oneline -20 -- <affected-files>

# Full diff of the last N commits
git diff HEAD~3..HEAD -- <affected-directory>
```

**Ключове запитання**: чи це працювало раніше? Якщо так, першопричина в недавньому diff.

- Регресія = першопричина в змінах, а не в початковому коді
- Зламано завжди = архітектурна проблема або хибне припущення

---

### Фаза 4: Відтворити

Перш ніж щось виправляти, переконайтеся, що можете детерміновано викликати баг.

```bash
# Run the test suite targeting the affected area
npm test -- --testPathPattern="affected-module" 2>/dev/null || \
pnpm test -- --testPathPattern="affected-module" 2>/dev/null || \
pytest tests/test_affected.py -v 2>/dev/null

# Check logs if available
tail -50 logs/error.log 2>/dev/null || \
journalctl -u app-service --lines=50 2>/dev/null
```

Якщо не вдається відтворити: зберіть більше доказів. Не виправляйте те, що не можете підтвердити як зламане.

---

### Фаза 5: Аналіз патернів

Зіставте симптом із відомими патернами багів:

| Патерн | Ознака | Де шукати |
|---------|-----------|---------------|
| Race condition | Періодичні збої, залежні від часу | Одночасний доступ до спільного стану, порядок async/await |
| Null propagation | TypeError, undefined is not a function | Відсутні перевірки необов'язкових значень, неперевірені відповіді API |
| Пошкодження стану | Неузгоджені дані, часткові оновлення | Транзакції, колбеки, мутація спільних об'єктів |
| Збій інтеграції | Тайм-аут, неочікувана форма відповіді | Виклики зовнішніх API, межі сервісів, зміни схем |
| Дрейф конфігурації | Локально працює, у staging/prod ні | Змінні середовища, feature flags, стан бази даних, відсутні секрети |
| Застарілий кеш | Показує старі дані, виправляється після перезапуску/очищення | Redis, CDN, кеш браузера, мемоїзація |
| Помилка імпорту/модуля | "Cannot find module", "is not a function" | Версії пакетів, циклічні імпорти, артефакти збірки |

Також перевірте:
- `TODOS.md` або трекер задач на відомі проблеми в тій самій ділянці
- `git log` на попередні виправлення в тих самих файлах; повторювані баги в одному місці є архітектурним запахом

**Зовнішній пошук:** якщо патерн не збігається, шукайте:
`{framework} {sanitized-error-type}` (прибирайте імена хостів, шляхи до файлів, внутрішні дані). Шукайте категорію помилки, а не сире повідомлення.

**Сформулюйте гіпотезу**: «Гіпотеза першопричини: [конкретне, перевірюване твердження про те, що не так і чому]»

---

### Фаза 6: Перевірка гіпотези

Перш ніж писати будь-яке виправлення, перевірте свою гіпотезу.

1. **Підтвердьте гіпотезу**: додайте тимчасовий лог, assertion або налагоджувальний вивід у передбачуваній першопричині. Запустіть відтворення. Чи збігаються докази?

```javascript
// Example: temporary diagnostic
console.log('[DEBUG investigate]', { value, expected, type: typeof value });
```

```python
# Example: temporary diagnostic
import sys; print(f'[DEBUG investigate] value={value!r} type={type(value)}', file=sys.stderr)
```

2. **Якщо гіпотеза хибна**: зберіть більше доказів. Поверніться до Фази 2. Не вгадуйте.

3. **Правило трьох спроб**: якщо 3 гіпотези не підтвердилися, ЗУПИНІТЬСЯ. Це може бути архітектурна проблема.

   Покажіть користувачеві таке:
   ```
   3 hypotheses tested, none confirmed. This likely requires deeper investigation.

   Options:
   A) I have a new hypothesis: [describe], continue investigating
   B) Add instrumentation and wait: capture the bug in the act next time
   C) Escalate: this needs someone with deeper system knowledge
   ```

**Червоні прапорці, негайно сповільніться:**
- «Швидке виправлення поки що»: ніякого «поки що» не існує
- Пропозиція виправлення до трасування потоку даних: це вгадування
- Кожне виправлення виявляє нову проблему деінде: хибний шар, а не хибний код

---

### Фаза 7: Реалізація

Коли першопричину підтверджено:

1. **Виправляйте першопричину, а не симптом.** Найменша зміна, що усуває справжню проблему.

2. **Мінімальний diff**: найменше зачеплених файлів, найменше змінених рядків. Опирайтеся рефакторингу сусіднього коду.

3. **Напишіть регресійний тест**, який:
   - **Падає** без виправлення (доводить, що тест змістовний)
   - **Проходить** з виправленням (доводить, що виправлення працює)

4. **Запустіть повний набір тестів** і вставте вивід. Регресії неприпустимі.

5. **Перевірка радіуса ураження**: якщо виправлення зачіпає понад 5 файлів, зупиніться й підтвердьте:

   ```
   This fix touches N files. That's a large blast radius for a bug fix.

   A) Proceed: the root cause genuinely spans these files
   B) Split: fix the critical path now, defer the broader cleanup
   C) Rethink: there may be a more targeted approach
   ```

---

## Формат результату

```
DEBUG REPORT
════════════════════════════════════════════════════
Symptom:          [what the user observed]
Root cause:       [what was actually wrong, specific not vague]
Fix:              [what was changed, with file:line references]
Evidence:         [test output or reproduction showing fix works]
Regression test:  [file:line of the new test]
Related:          [known issues, prior bugs in same area, architectural notes]
Status:           DONE | DONE_WITH_CONCERNS | BLOCKED
════════════════════════════════════════════════════
```

**Визначення статусів:**
- **DONE**: першопричину знайдено, виправлення застосовано, регресійний тест написано, усі тести проходять
- **DONE_WITH_CONCERNS**: виправлено, але повністю перевірити неможливо (періодичний баг, потрібен staging)
- **BLOCKED**: першопричина лишається неясною після повного розслідування

**Формат ескалації (коли BLOCKED):**
```
STATUS: BLOCKED
REASON: [1-2 sentences explaining what was tried and why it failed]
ATTEMPTED: [list of hypotheses tested]
RECOMMENDATION: [what the user should do next: add logging, escalate, or request an architectural review]
```

## Важливі правила

- **Ніколи не застосовуйте виправлення, яке не можете перевірити.** Якщо не можете відтворити й підтвердити, не випускайте його.
- **Ніколи не кажіть «це має виправити».** Перевірте й доведіть. Запустіть тести.
- **Ніколи не виправляйте >3 непов'язаних речей в одному розслідуванні.** Якщо знайдете інші баги, занотуйте їх, але лишайтеся сфокусованими.
- **Видаліть усі налагоджувальні логи** перед комітом виправлення.
- **3+ невдалих гіпотез → ставте під сумнів архітектуру**, а не власні навички формулювання гіпотез.

## Використання

```
/investigate TypeError: Cannot read properties of undefined (reading 'map')
/investigate the payment flow is silently dropping some transactions
/investigate
```

## Пов'язані команди

- `/review-pr`: переглянути виправлення перед злиттям
- `/qa`: запустити браузерне QA для зачепленої функції після виправлення
- `/ship`: чекліст перед деплоєм після завершення розслідування

$ARGUMENTS
