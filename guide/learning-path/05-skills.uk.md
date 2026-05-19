# Module 05: Skills & Automation

**Час**: 1.5 години | **Складність**: ⭐⭐ Intermediate

## Мета

Створювати багаторазові skills, які надають Claude специфічні для вашого домену знання. Пакувати готові рішення для повторюваних завдань.

---

## Що ви дізнаєтеся

- Що таке skills та чому вони ефективні
- Створення skills за допомогою файлів SKILL.md
- Блок frontmatter та метадані для skills
- Автоматичний виклик skills (auto-invocation)
- Побудова власної бази знань (knowledge base)
- Додавання skills до ваших проєктів

---

## Що таке Skills?

**Skill** — це багаторазовий модуль знань (knowledge module). Він навчає Claude тому, як саме робити конкретні речі у вашому проєкті.

### Приклад: Skill для тестування

Замість того, щоб кожної session пояснювати ваш підхід до тестування, ви створюєте окремий skill:

```markdown
# Testing Best Practices for Our Project

## Framework: Jest

## Style
- Descriptive names: "should validate email with + symbols"
- Arrange-Act-Assert pattern
- Mock external dependencies
- Test behavior, not implementation

## Coverage Target
Minimum 80%
```

Тепер щоразу, коли Claude допомагатиме вам писати або перевіряти тести, він прочитає цей skill та діятиме відповідно до ваших вимог.

### Skills проти Agents

| Аспект | Skill | Agent |
|--------|-------|-------|
| **Мета** | Надання знань | Виконання завдань |
| **Scope** | Доменні знання | Спеціалізований workflow |
| **Збереження**| Запам'ятовується кожної session| Викликається явно |
| **Автовиклик**| Так (опціонально) | Лише вручну |
| **Приклад** | "Як ми тестуємо код" | "test-writer agent" |

---

## Створення вашого першого Skill

Skills описуються як markdown файли в директорії `.claude/skills/`.

### Базова структура

```markdown
---
name: testing-standards
description: Our project's testing practices and conventions
triggers: [test, testing, jest, spec]
auto_invoke: false
keywords: [jest, unit-test, integration-test, mocking]
version: 1.0.0
---

# Testing Standards

## Framework
Jest with @testing-library/react

## File Organization
- Tests live next to source code
- Naming: `[Component].test.tsx`
- Fixtures in `__fixtures__/`
- Mocks in `__mocks__/`

## Test Structure (AAA)
1. **Arrange**: Set up test data
2. **Act**: Call the function/component
3. **Assert**: Check results

## Example

```typescript
describe('validateEmail', () => {
  it('should accept valid email addresses', () => {
    // Arrange
    const email = 'user@example.com';
    
    // Act
    const result = validateEmail(email);
    
    // Assert
    expect(result).toBe(true);
  });
});
```

## Coverage Requirements
- Target: 80% minimum
- Critical paths: 100%
- Types of coverage: line, branch, function

## Mocking Strategy
- External APIs: use jest.mock()
- Database: use test fixtures
- Timers: use jest.useFakeTimers()

## Running Tests
```bash
npm test                 # Run all tests
npm test -- --coverage   # With coverage report
npm test -- --watch      # Watch mode
```
```

### Розташування файлу

```
my-project/
└── .claude/
    └── skills/
        └── testing-standards.md
```

---

## Можливості та атрибути Skills

### Triggers (Тригери)

Автоматично активують skill, коли Claude бачить певні ключові слова у вашому запиті:

```markdown
---
triggers: [test, jest, spec, coverage, mock]
---
```

Якщо Claude зустрічає фразу "add tests to this function", він автоматично зчитує ваш testing-standards skill.

### Auto-Invoke (Автовиклик)

```markdown
---
auto_invoke: true
---
```

Якщо встановлено значення `true`, Claude завантажує цей skill на самому початку session (навіть якщо ви його не викликали). Використовуйте це для найважливіших правил проєкту.

### Keywords (Ключові слова)

Допомагають пошуковій системі Claude знаходити потрібний skill:

```markdown
---
keywords: [testing, jest, unit-test, mocking, assertions]
---
```

### Version (Версія)

Допомагає відстежувати зміни у skills:

```markdown
---
version: 1.0.0
---
```

Оновлюйте версію при суттєвих змінах у правилах чи підходах.

---

## Популярні шаблони (Patterns) для Skills

### Шаблон 1: Стандарти кодування (Coding Standards)

```markdown
---
name: python-standards
triggers: [python, flask, django]
---

# Python Coding Standards

## Style
- PEP 8 compliance (max 100 chars)
- Type hints on all functions
- Docstrings in Google format

## Testing
- pytest for unit tests
- 80% minimum coverage
- Mock external dependencies

## File Organization
src/
├── models/
├── services/
├── controllers/
└── tests/

## Imports
```python
# ✅ Good: specific imports
from models import User
from services.auth import authenticate

# ❌ Bad: wildcard imports
from models import *
```
```

### Шаблон 2: Доменні знання (Domain Knowledge)

```markdown
---
name: payment-processing
description: Payment system rules and edge cases
auto_invoke: true
---

# Payment Processing Rules

## PCI Compliance
- Never log card numbers
- Use tokenization (Stripe)
- Encrypt sensitive data
- Audit all transactions

## Common Issues
1. Partial charges: Retry with exponential backoff
2. Currency conversion: Always round to 2 decimals
3. Timezone handling: Store all times in UTC

## Edge Cases
- Declined cards: Provide clear error message
- Expired cards: Suggest updating payment method
- 3D Secure: Handle verification flow
```

### Шаблон 3: Документація процесів (Process Documentation)

```markdown
---
name: code-review-checklist
triggers: [review, pull request, pr]
---

# Code Review Checklist

## Before Requesting Review
- [ ] Tests pass locally
- [ ] No console.log statements
- [ ] No secrets in code
- [ ] Commit messages are clear

## Security Checks
- [ ] No SQL injection vulnerabilities
- [ ] No XSS vulnerabilities
- [ ] No exposed API keys
- [ ] Input is validated

## Performance
- [ ] No N+1 queries
- [ ] No infinite loops
- [ ] Load times acceptable

## Testing
- [ ] Unit tests added
- [ ] Integration tests updated
- [ ] Coverage >80%
```

---

## Об'єднання Skills (Bundling Skills)

Ви можете об'єднувати кілька пов'язаних skills в один пакет.

### Набір skills проєкту (Project Skill Bundle)

```
my-project/
└── .claude/
    └── skills/
        ├── testing-standards.md
        ├── api-design.md
        ├── database-patterns.md
        └── security-checklist.md
```

Зробіть посилання на них у вашому файлі CLAUDE.md:

```markdown
## Available Skills
Our custom skills are loaded automatically:
- **testing-standards**: How we write tests
- **api-design**: REST API conventions
- **database-patterns**: Common queries and migrations
- **security-checklist**: Security review process
```

### Поширення Skills

Щоб поділитися skills з вашою командою, додайте їх до системи контролю версій git:

```bash
git add .claude/skills/
git commit -m "Add testing and API design skills"
git push
```

Колеги по команді отримають ці оновлені skills автоматично під час checkout проєкту.

---

## Вправа: Створення Domain Skill

### Сценарій

Ви будуєте e-commerce платформу. Вам потрібно, щоб Claude добре розумів модель даних ваших товарів.

### Крок 1: Створіть Skill

```bash
cat > .claude/skills/product-data-model.md << 'EOF'
---
name: product-data-model
description: E-commerce product data structure and rules
triggers: [product, catalog, sku, price, inventory]
auto_invoke: false
version: 1.0.0
---

# Product Data Model

## Core Entities

### Product
```
{
  id: UUID,
  name: string,
  slug: string,  // URL-friendly
  description: string,
  category_id: UUID,
  created_at: timestamp,
  updated_at: timestamp
}
```

### SKU (Stock Keeping Unit)
```
{
  id: UUID,
  product_id: UUID,
  sku: string,  // e.g., "BLUE-XL-001"
  price: decimal,  // Always 2 decimals
  cost: decimal,
  inventory: integer,
  weight: float,  // In kg
}
```

### Inventory Rules
- Decrement on order placement
- Increment on return
- Low stock alert: <5 units
- Reorder level: Set per product

## Common Queries

### Get product with all SKUs
```sql
SELECT p.*, s.* 
FROM products p 
JOIN skus s ON p.id = s.product_id 
WHERE p.slug = ?
```

### Check inventory
```sql
SELECT sum(inventory) FROM skus WHERE product_id = ?
```

## Edge Cases
1. Out of stock: Return 404 or "unavailable"
2. Variant selection: Show price per SKU
3. Price changes: Update in SKU, not Product
EOF
```

### Крок 2: Додайте посилання у CLAUDE.md

```markdown
## Skills
- **product-data-model**: Understanding our product structure
```

### Крок 3: Перевірте його роботу

Під час session надішліть запит:

```
Add a query to find all products with low inventory (< 5 units)
```

Claude зробить наступне:
1. Прочитає `product-data-model` skill
2. Зрозуміє вашу схему даних
3. Напише правильний SQL-запит

---

## Найкращі практики

### РЕКОМЕНДУЄТЬСЯ

✅ Створювати skills для повторюваних завдань або концепцій

✅ Робити skills вузькоспрямованими (один домен — один skill)

✅ Зберігати skills під контролем версій git

✅ Додавати практичні приклади всередину skills

✅ Оновлювати вміст skills при зміні вимог

✅ Ділитися корисними skills зі своєю командою

### НЕ РЕКОМЕНДУЄТЬСЯ

❌ Створювати skill для разових завдань та знань (краще скористатися CLAUDE.md)

❌ Робити skills занадто великими (якщо >500 рядків, розбийте на декілька дрібних)

❌ Використовувати skills для тимчасових інструкцій (для цього призначені CLAUDE.md або AGENT.md)

❌ Вважати, що skills повністю замінюють вичерпну технічну документацію

---

## Життєвий цикл Skill

1. **Визначення**: Виявити повторюваний шаблон роботи чи область знань
2. **Документування**: Описати skill, додавши практичні приклади
3. **Тестування**: Запустити в session і переконатися, що Claude дотримується правил
4. **Вдосконалення**: Оновити на основі досвіду використання
5. **Поширення**: Зробити commit у git для вашої команди
6. **Підтримка**: Актуалізувати знання у міру еволюції вашого проєкту

---

## Валідація: Ви готові, якщо...

✓ Ви створили принаймні один користувацький skill

✓ Ви розумієте різницю між triggers та auto-invoke

✓ Ви знаєте, чим відрізняються skills від agents

✓ Ви можете пояснити, коли варто створити skill, а коли використати CLAUDE.md

✓ Ваш новий skill успішно пройшов тестування в реальній session

---

## Що далі?

**Module 06: Hooks & Events** охоплює:
- Автоматизацію реакцій на системні події
- Валідацію перед створенням commit (pre-commit validation)
- Сповіщення після виконання дій (post-action notifications)
- Побудову безпечних ланцюгів автоматизації

Це навчить вас автоматизувати повторювані рутинні кроки без ручного втручання.

---
**Локалізація**: [Serhii (MacPlus Software)](https://macplus-software.com)
*Остання синхронізація: Травень 2026*
