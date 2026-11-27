---
name: ast-grep-patterns
description: "Skill, що вчить Claude, коли і як використовувати ast-grep для структурного пошуку в коді"
effort: low
---

# Шаблони ast-grep для Claude Code

> **Skill**: навчіть Claude, коли і як використовувати ast-grep для структурного пошуку в коді

## Установлення

```bash
# Install ast-grep skill
npx skills add ast-grep/agent-skill

# Or via plugin marketplace
/plugin marketplace add
```

## Коли пропонувати ast-grep

Пропонуйте ast-grep користувачеві, коли:

| Сценарій | Ключові слова | Чому ast-grep? |
|----------|--------------|---------------|
| **Масштабний рефакторинг** | «перейменувати всі виклики...», «змінити сигнатуру API», «>50k рядків» | Потрібна структурна точність |
| **Міграція фреймворку** | «React 17→18», «Vue 2→3», «оновити залежності» | Перетворення з урахуванням AST |
| **Виявлення патернів** | «знайти функції без...», «знайти невикористані...», «виявити антипатерни» | Структурні правила |
| **Аналіз кодової бази** | «які компоненти залежать від...», «знайти сильнозчеплені...» | Графи залежностей |

**Не пропонуйте для**:
- Простого пошуку рядків (назви функцій, імпорти) → використовуйте Grep
- Малих проєктів (<10k рядків) → достатньо Grep
- Одноразового пошуку → Grep швидший
- Семантичного пошуку → використовуйте Serena MCP або grepai

## Дерево рішень

```
User request analysis:
├─ "Find string/text" → Grep (native)
├─ "Find by meaning" → Serena MCP or grepai
├─ "Find by structure" → ast-grep (plugin)
└─ Mixed requirements → Start with Grep, escalate if needed
```

## Поширені шаблони

### 1. Async-функції без обробки помилок

**Випадок використання**: знайти async-функції без блоків try/catch

```yaml
# ast-grep rule
rule:
  pattern: |
    async function $FUNC($$$PARAMS) {
      $$$BODY
    }
  not:
    has:
      pattern: try { $$$TRY } catch
```

**Коли використовувати**: аудити безпеки, перевірки готовності до production

### 2. Компоненти React зі специфічними hooks

**Випадок використання**: знайти всі компоненти, що використовують `useEffect` без cleanup

```yaml
rule:
  pattern: |
    useEffect(() => {
      $$$BODY
    })
  not:
    has:
      pattern: return () => { $$$CLEANUP }
```

**Коли використовувати**: виявлення витоків пам'яті, аудит дотримання кращих практик React

### 3. Функції, що перевищують поріг кількості параметрів

**Випадок використання**: знайти функції з >5 параметрами (ознака складності)

```yaml
rule:
  pattern: function $NAME($P1, $P2, $P3, $P4, $P5, $P6, $$$REST) { $$$BODY }
```

**Коли використовувати**: покращення якості коду, кандидати на рефакторинг

### 4. Console.log у production-коді

**Випадок використання**: прибрати debug-логування з production-файлів

```yaml
rule:
  pattern: console.log($$$ARGS)
  inside:
    pattern: |
      class $CLASS {
        $$$METHODS
      }
```

**Коли використовувати**: очищення перед production, аудити перед релізом

### 5. Невикористані props у React

**Випадок використання**: виявити props, які передаються, але ніколи не використовуються

```yaml
rule:
  pattern: |
    function $COMP({ $PROP, $$$OTHER }) {
      $$$BODY
    }
  not:
    has:
      pattern: $PROP
      inside: $$$BODY
```

**Коли використовувати**: видалення мертвого коду, оптимізація продуктивності

### 6. Використання застарілого API

**Випадок використання**: знайти використання старих методів API

```yaml
rule:
  any:
    - pattern: React.Component
    - pattern: componentWillMount
    - pattern: componentWillReceiveProps
```

**Коли використовувати**: міграції фреймворків, очищення від застарілого коду

### 7. Шаблони ризику SQL-ін'єкцій

**Випадок використання**: знайти потенційні вразливості до SQL-ін'єкцій

```yaml
rule:
  pattern: |
    db.query($TEMPLATE_LITERAL)
  where:
    $TEMPLATE_LITERAL:
      kind: template_string
```

**Коли використовувати**: аудити безпеки, сканування вразливостей

### 8. Відсутні типи повернення в TypeScript

**Випадок використання**: примусово вимагати явні типи повернення

```yaml
rule:
  pattern: |
    function $NAME($$$PARAMS) {
      $$$BODY
    }
  not:
    has:
      pattern: ': $TYPE'
```

**Коли використовувати**: кращі практики TypeScript, покращення типобезпеки

### 9. Великі оператори switch (кандидати на рефакторинг)

**Випадок використання**: знайти оператори switch із >10 гілками

```yaml
rule:
  pattern: |
    switch ($EXPR) {
      $C1: $$$B1
      $C2: $$$B2
      $C3: $$$B3
      $C4: $$$B4
      $C5: $$$B5
      $C6: $$$B6
      $C7: $$$B7
      $C8: $$$B8
      $C9: $$$B9
      $C10: $$$B10
      $C11: $$$B11
    }
```

**Коли використовувати**: зниження складності, рефакторинг на поліморфізм

### 10. Порожні блоки catch (проковтнуті помилки)

**Випадок використання**: знайти обробку помилок, яка мовчки зазнає невдачі

```yaml
rule:
  pattern: |
    try {
      $$$TRY
    } catch ($ERR) {
      // empty or only comment
    }
```

**Коли використовувати**: налагодження загадкових збоїв, аудит обробки помилок

## Складність налаштування проти користі

| Розмір кодової бази | Чи виправдане налаштування? | Альтернатива |
|---------------|-----------------|-------------|
| <10k рядків | ❌ Ні | Використовуйте Grep |
| 10k-50k рядків | ⚠️ Можливо | Почніть із Grep, переходьте далі за потреби |
| 50k-200k рядків | ✅ Так | ast-grep для структури, Grep для тексту |
| >200k рядків | ✅ Однозначно | Комбінація ast-grep + Serena MCP |

## Усунення несправностей

### ast-grep не знайдено

```bash
# Verify installation
npx ast-grep --version

# Reinstall skill
npx skills add ast-grep/agent-skill --force
```

### Claude не використовує ast-grep

**Проблема**: Claude використовує Grep замість ast-grep

**Рішення**: формулюйте запит явно
- ❌ "Find async functions"
- ✅ "Use ast-grep to find async functions"

### Проблеми з продуктивністю

**Проблема**: ast-grep повільно працює на великій кодовій базі

**Рішення**:
1. Звузьте область пошуку: `ast-grep --path src/components/`
2. Використовуйте фільтри файлів: `ast-grep --lang tsx`
3. Кешуйте результати для ітеративного уточнення

### Шаблон не збігається

**Проблема**: шаблон ast-grep не збігається з очікуваним кодом

**Кроки налагодження**:
1. Перевірте шаблон ізольовано: `ast-grep -p 'your-pattern' file.js`
2. Перевірте структуру AST: `ast-grep --debug-query`
3. Поступово спрощуйте шаблон
4. Перевірте синтаксис мови (JS проти TS проти JSX)

## Приклади інтеграції

### Робочий процес: pre-commit hook з ast-grep

```bash
#!/bin/bash
# .git/hooks/pre-commit

# Check for console.log in staged files
if ast-grep -p 'console.log($$$)' $(git diff --cached --name-only); then
  echo "❌ Found console.log statements"
  exit 1
fi
```

### Робочий процес: скрипт міграції

```bash
#!/bin/bash
# Migrate React class components to hooks

# Find all class components
ast-grep -p 'class $C extends React.Component' --json > components.json

# Process each component
jq -r '.[] | .file' components.json | while read file; do
  echo "Migrating: $file"
  # ... transformation logic
done
```

### Робочий процес: аудит безпеки

```bash
#!/bin/bash
# security-audit.sh

echo "=== Security Audit ==="

# SQL injection risks
ast-grep -p 'db.query(`${$VAR}`)' --lang ts

# XSS risks
ast-grep -p 'innerHTML = $VAR' --lang js

# Hardcoded secrets
ast-grep -p 'password: "$PASSWORD"' --lang ts
```

## Шаблони prompt для Claude

### Шаблон 1: масштабний рефакторинг

```
Мені потрібно зробити рефакторинг [ФУНКЦІОНАЛЬНОСТІ] у всій нашій кодовій базі (~[РОЗМІР] рядків).

Використай ast-grep, щоб:
1. Знайти всі входження [СТАРОГО_ШАБЛОНУ]
2. Визначити, які файли буде зачеплено
3. Запропонувати стратегію перетворення
4. Скласти поетапний план міграції

Почни лише з аналізу, а перед внесенням змін дочекайся мого схвалення.
```

### Шаблон 2: міграція фреймворку

```
Ми мігруємо з [СТАРИЙ_ФРЕЙМВОРК v1] на [НОВИЙ_ФРЕЙМВОРК v2].

Використай ast-grep, щоб:
1. Знайти всі використання застарілого API
2. Зіставити їх з еквівалентами нового API
3. Оцінити обсяг міграції (кількість зачеплених файлів)
4. Виявити зміни з високим ризиком

Надай граф залежностей, що показує порядок міграції.
```

### Шаблон 3: аудит якості коду

```
Проведи аудит якості коду в [КАТАЛОЗІ] за допомогою ast-grep.

Зосередься на:
- Функціях із >5 параметрами
- Async-функціях без обробки помилок
- Порожніх блоках catch
- Невикористаних параметрах функцій

Розстав проблеми за серйозністю та запропонуй варіанти рефакторингу.
```

## Просунуте: поєднання ast-grep з іншими інструментами

### ast-grep + Serena MCP

```bash
# 1. ast-grep finds structural patterns
ast-grep -p 'async function $F' --json > async-funcs.json

# 2. Serena finds symbols and dependencies
claude mcp call serena find_symbol --name "authenticate"

# 3. Combine insights for full context
# ast-grep: "This is an async function"
# Serena: "Called by 12 other functions"
```

### ast-grep + grepai

```bash
# 1. grepai for semantic search
# "Find authentication-related code"

# 2. ast-grep for structural refinement
# "Among those results, which are async without error handling?"
```

## Кращі практики

1. **Починайте з простого**: починайте з Grep, переходьте до ast-grep за потреби
2. **Тестуйте шаблони**: перевіряйте на малих файлах, перш ніж запускати на всій кодовій базі
3. **Документуйте шаблони**: зберігайте вдалі шаблони як правила для повторного використання
4. **Явні запити**: завжди прямо кажіть Claude, коли використовувати ast-grep
5. **Поєднуйте інструменти**: ast-grep для структури, Grep для тексту, Serena для символів

## Ресурси

- [ast-grep Documentation](https://ast-grep.github.io/)
- [Pattern Playground](https://ast-grep.github.io/playground.html)
- [ast-grep GitHub](https://github.com/ast-grep/ast-grep)
- [Claude Skill](https://github.com/ast-grep/claude-skill)

---

**Останнє оновлення**: січень 2026
**Сумісно з**: Claude Code 2.1.7+
