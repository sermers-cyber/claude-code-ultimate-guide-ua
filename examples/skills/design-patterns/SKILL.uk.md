---
name: design-patterns
description: "Виявляє, пропонує й оцінює патерни проєктування GoF у кодових базах на TypeScript/JavaScript. Використовуйте під час рефакторингу коду, застосування патернів singleton/factory/observer/strategy, перевірки якості патернів або пошуку нативних для стеку альтернатив у React, Angular, NestJS і Vue."
allowed-tools: Read Grep Glob mcp__grepai__grepai_search
context: fork
agent: specialist
effort: high
---

# Skill-аналізатор патернів проєктування

**Призначення**: виявляти, пропонувати й оцінювати патерни проєктування Gang of Four (GoF) у кодових базах на TypeScript/JavaScript з адаптацією під стек.

## Основні можливості

1. **Визначення стеку**: розпізнавання основного фреймворку чи бібліотеки (React, Angular, NestJS, Vue, Express, RxJS, Redux, ORM)
2. **Виявлення патернів**: пошук наявних реалізацій 23 патернів GoF
3. **Розумні пропозиції**: рекомендації патернів для усунення code smells з використанням нативних для стеку ідіом, коли вони є
4. **Оцінювання якості**: перевірка якості реалізації патернів на відповідність найкращим практикам

## Режими роботи

### Режим 1: виявлення

**Тригер**: користувач просить виявити патерни або проаналізувати код
**Результат**: JSON-звіт про знайдені патерни з оцінками впевненості та контекстом стеку

**Робочий процес**:
```
1. Stack Detection (package.json, tsconfig.json, framework files)
2. Pattern Search (Glob for candidates -> Grep for signatures -> Read for validation)
3. Classification (native to stack vs custom implementations)
4. Confidence Scoring (0.0-1.0 based on detection rules)
5. JSON Report Generation
```

**Приклад виклику**:
```
/design-patterns detect src/
/design-patterns analyze --format=json
```

### Режим 2: пропозиції

**Тригер**: користувач просить запропонувати патерни або поради щодо рефакторингу
**Результат**: Markdown-звіт із пріоритизованими пропозиціями та прикладами, адаптованими під стек

**Робочий процес**:
```
1. Code Smell Detection (switch statements, long parameter lists, global state, etc.)
2. Pattern Matching (map smell -> applicable patterns)
3. Stack Adaptation (prefer native framework patterns over custom implementations)
4. Priority Ranking (impact x feasibility)
5. Markdown Report with Code Examples
```

**Приклад виклику**:
```
/design-patterns suggest src/payment/
/design-patterns refactor --focus=creational
```

### Режим 3: оцінювання

**Тригер**: користувач просить оцінити якість патернів
**Результат**: JSON-звіт з оцінками за кожним критерієм

**Робочий процес**:
```
1. Pattern Identification (which pattern is implemented)
2. Criteria Assessment (correctness, testability, SOLID compliance, documentation)
3. Issue Detection (common mistakes, anti-patterns)
4. Scoring (0-10 per criterion)
5. JSON Report with Recommendations
```

**Приклад виклику**:
```
/design-patterns evaluate src/services/singleton.ts
/design-patterns quality --pattern=observer
```

## Методологія

### Фаза 1: визначення стеку

**Джерела** (за пріоритетом):
1. `package.json` -> перевірити dependencies і devDependencies
2. Файли, специфічні для фреймворків -> `angular.json`, `next.config.*`, `nest-cli.json`, `vite.config.*`
3. `tsconfig.json` -> перевірити compilerOptions, paths, lib
4. Розширення файлів -> наявність `*.jsx`, `*.tsx`, `*.vue`

**Правила виявлення** (з `signatures/stack-patterns.yaml`):
- React: `react` у залежностях + файли `*.jsx/*.tsx`
- Angular: `@angular/core` + `angular.json`
- NestJS: `@nestjs/core` + `nest-cli.json`
- Vue: `vue` v3+ + файли `*.vue`
- Express: `express` у залежностях + шаблони `app.use`
- RxJS: `rxjs` у залежностях + використання Observable
- Redux/Zustand: `redux`/`zustand` у залежностях + шаблони store
- Prisma/TypeORM: `prisma`/`typeorm` у залежностях + файли схем

**Результат**:
```json
{
  "stack_detected": {
    "primary": "react",
    "version": "18.2.0",
    "secondary": ["typescript", "zustand", "prisma"],
    "detection_sources": ["package.json", "tsconfig.json", "37 *.tsx files"],
    "confidence": 0.95
  }
}
```

### Фаза 2: виявлення патернів

**Стратегія пошуку**:
1. **Фаза Glob**: знайти файли-кандидати за угодою про іменування
   - `*Singleton*.ts`, `*Factory*.ts`, `*Strategy*.ts`, `*Observer*.ts` тощо
   - `*Manager*.ts`, `*Builder*.ts`, `*Adapter*.ts`, `*Proxy*.ts` тощо

2. **Фаза Grep**: шукати сигнатури патернів (з `signatures/detection-rules.yaml`)
   - Основні сигнали: `private constructor`, `static getInstance()`, `subscribe()`, `createXxx()` тощо
   - Другорядні сигнали: іменування інтерфейсів, шаблони делегування, сигнатури методів

3. **Фаза Read**: перевірити структуру патерну
   - Розібрати визначення класів і інтерфейсів
   - Перевірити зв'язки (наслідування, композиція, делегування)
   - З'ясувати, чи патерн реалізовано повністю, чи використано лише частково

**Оцінка впевненості**:
- 0.9-1.0: наявні всі основні та другорядні сигнали, структура збігається точно
- 0.7-0.89: наявні всі основні сигнали та частина другорядних, незначні відхилення
- 0.5-0.69: основні сигнали є, другорядного підтвердження бракує
- 0.3-0.49: збігається іменування, структурні докази слабкі
- 0.0-0.29: доказів недостатньо, імовірно хибнопозитивний результат

**Класифікація**:
- `native`: патерн реалізовано нативними засобами стеку (React Context, Angular Services, NestJS Guards тощо)
- `custom`: ручна реалізація на TypeScript
- `library`: патерн надає стороння бібліотека (RxJS Subject, Redux Store тощо)

### Фаза 3: виявлення code smells

**Цільові smells** (з `signatures/code-smells.yaml`):
1. **Switch за типом** -> патерн Strategy/Factory
2. **Довгий список параметрів (>4)** -> патерн Builder
3. **Доступ до глобального стану** -> Singleton (а краще DI)
4. **Дубльовані умови за станом** -> патерн State
5. **Розкидана логіка сповіщень** -> патерн Observer
6. **Складне створення об'єктів** -> Factory/Abstract Factory
7. **Тісний зв'язок із конкретними класами** -> Adapter/Bridge
8. **Повторювані перетворення інтерфейсів** -> патерн Adapter
9. **Глибоке вкладення для додавання функціональності** -> патерн Decorator
10. **Великий клас із багатьма обов'язками** -> патерн Facade

**Евристики виявлення**:
- Grep за `switch (.*type)`, `switch (.*kind)`, `switch (.*mode)`
- Підрахунок параметрів функції: `function \w+\([^)]{60,}\)` (наближення для >4 параметрів)
- Пошук глобального доступу: `window\.`, `global\.`, `process\.env\.\w+` (поза файлами конфігурації)
- Пошук умов за станом: `if.*state.*===.*&&.*if.*state.*===`
- Пошук шаблонів сповіщень: `forEach.*notify`, `map.*\.emit\(`

### Фаза 4: пропозиції з урахуванням стеку

**Логіка адаптації** (з `signatures/stack-patterns.yaml`):

```
IF pattern_detected == "custom" AND stack_has_native_equivalent:
  SUGGEST: "Use stack-native pattern instead"
  PROVIDE: Side-by-side comparison (current vs recommended)

ELSE IF code_smell_detected AND pattern_missing:
  IF stack_provides_pattern:
    SUGGEST: Stack-native implementation with examples
  ELSE:
    SUGGEST: Custom TypeScript implementation with best practices

ELSE IF pattern_implemented_incorrectly:
  PROVIDE: Refactoring steps to fix anti-patterns
```

**Приклади адаптацій**:

| Патерн | Стек | Нативна альтернатива | Рекомендація |
|---------|-------|-------------------|----------------|
| Singleton | React | Context API + Provider | Використовуйте `createContext()` замість `getInstance()` |
| Observer | Angular | RxJS Subject/BehaviorSubject | Використовуйте вбудовані Observable, а не власну реалізацію |
| Decorator | NestJS | @Injectable() decorators + Interceptors | Використовуйте interceptors фреймворку |
| Strategy | Vue 3 | Composition API composables | Використовуйте `ref()` + composables замість класів |
| Chain of Responsibility | Express | Middleware (`app.use()`) | Використовуйте ланцюжок middleware в Express |
| Command | Redux | Action creators + reducers | Використовуйте Redux actions, а не власні об'єкти-команди |

### Фаза 5: оцінювання якості

**Критерії** (з `checklists/pattern-evaluation.md`):
1. **Коректність (0-10)**: чи відповідає вона канонічній структурі патерну?
2. **Тестованість (0-10)**: чи легко замінити залежності на mock/stub?
3. **Єдина відповідальність (0-10)**: чи робить вона лише одну річ?
4. **Принцип відкритості/закритості (0-10)**: чи розширюється вона без змін наявного коду?
5. **Документація (0-10)**: чи зрозумілий задум і промовисті назви?

**Настанови з оцінювання**:
- 9-10: зразкова, еталонна реалізація
- 7-8: добре, можливі незначні покращення
- 5-6: прийнятно, є помітні проблеми, які варто виправити
- 3-4: проблемно, потрібен значний рефакторинг
- 0-2: некоректно або має серйозні вади

**Виявлення проблем**:
- Жорстко зашиті залежності (Singleton з `new` усередині getInstance)
- God classes (забагато обов'язків)
- Дірясті абстракції (розкриття внутрішньої структури)
- Відсутня обробка помилок
- Погані назви (Strategy1, Strategy2 замість описових імен)

## Формати виводу

### Режим виявлення (JSON)

```json
{
  "metadata": {
    "scan_date": "2026-01-21T10:30:00Z",
    "scope": "src/",
    "files_scanned": 147,
    "execution_time_ms": 2341
  },
  "stack_detected": {
    "primary": "react",
    "version": "18.2.0",
    "secondary": ["typescript", "zustand", "prisma"],
    "detection_sources": ["package.json", "tsconfig.json", "37 *.tsx files"],
    "confidence": 0.95
  },
  "patterns_found": {
    "singleton": [
      {
        "file": "src/lib/api-client.ts",
        "lines": "5-28",
        "confidence": 0.85,
        "type": "custom",
        "signals": ["private constructor", "static getInstance", "private static instance"],
        "note": "Consider using React Context instead for better testability"
      }
    ],
    "observer": [
      {
        "file": "src/hooks/useAuth.ts",
        "lines": "12-45",
        "confidence": 0.92,
        "type": "native",
        "implementation": "React useState + useEffect",
        "note": "Correctly using React's built-in observer pattern"
      }
    ],
    "factory": [
      {
        "file": "src/services/notification-factory.ts",
        "lines": "8-67",
        "confidence": 0.78,
        "type": "custom",
        "signals": ["createNotification method", "type discrimination", "returns interface"]
      }
    ]
  },
  "summary": {
    "total_patterns": 7,
    "native_to_stack": 4,
    "custom_implementations": 3,
    "by_category": {
      "creational": 2,
      "structural": 3,
      "behavioral": 2
    },
    "by_confidence": {
      "high": 5,
      "medium": 2,
      "low": 0
    }
  },
  "recommendations": [
    "Consider replacing custom Singleton (api-client.ts) with React Context for better DI",
    "Review Factory pattern (notification-factory.ts) - could be simplified with strategy pattern"
  ]
}
```

### Режим пропозицій (markdown)

```markdown
# Design Pattern Suggestions

**Scope**: `src/payment/`
**Stack**: React 18 + TypeScript + Stripe
**Date**: 2026-01-21

---

## High Priority

### 1. Strategy Pattern: `src/payment/processor.ts:45-89`

**Code Smell**: Switch statement on payment type (4 cases, 78 lines)

**Current Implementation** (lines 52-87):
```typescript
switch (paymentType) {
  case 'credit':
    // 20 lines of credit card logic
    break;
  case 'paypal':
    // 15 lines of PayPal logic
    break;
  case 'crypto':
    // 18 lines of crypto logic
    break;
  case 'bank':
    // 12 lines of bank transfer logic
    break;
}
```

**Recommended (React-adapted Strategy)**:
```typescript
// Define strategy interface
interface PaymentStrategy {
  process: (amount: number) => Promise<PaymentResult>;
}

// Custom hooks as strategies
const useCreditPayment = (): PaymentStrategy => ({
  process: async (amount) => { /* credit logic */ }
});

const usePaypalPayment = (): PaymentStrategy => ({
  process: async (amount) => { /* PayPal logic */ }
});

// Strategy selection hook
const usePaymentStrategy = (type: PaymentType): PaymentStrategy => {
  const strategies = {
    credit: useCreditPayment(),
    paypal: usePaypalPayment(),
    crypto: useCryptoPayment(),
    bank: useBankPayment(),
  };
  return strategies[type];
};

// Usage in component
const PaymentForm = ({ type }: Props) => {
  const strategy = usePaymentStrategy(type);
  const handlePay = () => strategy.process(amount);
  // ...
};
```

**Impact**:
- **Complexity**: Reduces cyclomatic complexity from 12 to 2
- **Extensibility**: New payment methods = new hook, no modification to existing code
- **Testability**: Each strategy hook can be tested in isolation
- **Effort**: ~2 hours (extract logic into hooks, add tests)

---

## Medium Priority

### 2. Observer Pattern: `src/cart/CartManager.ts:23-156`

**Code Smell**: Manual notification logic scattered across 8 methods

**Current**: Manual loops calling update functions
**Recommended**: Use Zustand store (already in dependencies)

```typescript
// Instead of custom observer:
import create from 'zustand';

interface CartStore {
  items: CartItem[];
  addItem: (item: CartItem) => void;
  removeItem: (id: string) => void;
  // Zustand automatically notifies subscribers
}

export const useCartStore = create<CartStore>((set) => ({
  items: [],
  addItem: (item) => set((state) => ({ items: [...state.items, item] })),
  removeItem: (id) => set((state) => ({ items: state.items.filter(i => i.id !== id) })),
}));

// Components auto-subscribe:
const CartDisplay = () => {
  const items = useCartStore((state) => state.items);
  // Re-renders automatically on cart changes
};
```

**Impact**:
- **LOC**: Reduces from 156 to ~25 lines
- **Stack-native**: Uses existing Zustand dependency
- **Testability**: Zustand stores are easily tested
- **Effort**: ~1.5 hours

---

## Summary

- **Total suggestions**: 4
- **High priority**: 2 (Strategy, Observer)
- **Medium priority**: 2 (Builder, Facade)
- **Estimated total effort**: ~6 hours
- **Primary benefits**: Reduced complexity, improved testability, stack-native idioms
```

### Режим оцінювання (JSON)

```json
{
  "file": "src/services/config-singleton.ts",
  "pattern": "singleton",
  "lines": "5-34",
  "scores": {
    "correctness": 8,
    "testability": 4,
    "single_responsibility": 9,
    "open_closed": 7,
    "documentation": 6,
    "overall": 6.8
  },
  "details": {
    "correctness": {
      "score": 8,
      "rationale": "Implements singleton structure correctly with private constructor and static getInstance",
      "issues": ["Missing thread-safety consideration (not critical in JS single-threaded context)"]
    },
    "testability": {
      "score": 4,
      "rationale": "Hard to mock or reset instance in tests",
      "issues": [
        "No reset method for test isolation",
        "Static instance makes dependency injection impossible",
        "Tests must run in specific order or share state"
      ],
      "suggestions": [
        "Add resetInstance() method for tests (with appropriate guards)",
        "Consider using dependency injection instead"
      ]
    },
    "single_responsibility": {
      "score": 9,
      "rationale": "Focuses solely on configuration management",
      "issues": []
    },
    "open_closed": {
      "score": 7,
      "rationale": "Configuration can be extended but requires modification for new sources",
      "suggestions": ["Consider strategy pattern for configuration sources"]
    },
    "documentation": {
      "score": 6,
      "rationale": "Has JSDoc but missing rationale for singleton choice",
      "suggestions": ["Document why singleton is chosen over DI", "Add usage examples"]
    }
  },
  "recommendations": [
    {
      "priority": "high",
      "suggestion": "Add test-friendly reset mechanism or refactor to use DI",
      "rationale": "Current implementation makes testing difficult"
    },
    {
      "priority": "medium",
      "suggestion": "Document singleton rationale in JSDoc",
      "rationale": "Team members should understand why global state is necessary here"
    }
  ]
}
```

## Обмеження та настанови

### Аналіз лише для читання
- **Жодних змін**: цей skill лише аналізує та пропонує, код він ніколи не змінює
- **Жодного створення файлів**: він не генерує файли з відрефакторенним кодом
- **Рішення за користувачем**: кожна пропозиція потребує явного схвалення користувача перед втіленням

### Мовний фокус
- **Основна**: TypeScript (`.ts`, `.tsx`)
- **Другорядна**: JavaScript (`.js`, `.jsx`)
- **Винятки**: інші мови (Python, Java, C#) не підтримуються

### Охоплення патернів
- **Породжувальні (5)**: Singleton, Factory Method, Abstract Factory, Builder, Prototype
- **Структурні (7)**: Adapter, Bridge, Composite, Decorator, Facade, Flyweight, Proxy
- **Поведінкові (11)**: Chain of Responsibility, Command, Iterator, Mediator, Memento, Observer, State, Strategy, Template Method, Visitor, Interpreter

### Міркування щодо продуктивності
- **Великі кодові бази (>500 файлів)**: використовуйте `--scope`, щоб обмежити сканування окремими каталогами
- **Паралельний пошук**: Grep-пошуки виконуються незалежно для кожного патерну
- **Кешування**: результати визначення стеку кешуються на сесію, щоб не читати package.json повторно

## Приклади використання

### Базове виявлення
```bash
# Detect all patterns in src/
/design-patterns detect src/

# Detect only creational patterns
/design-patterns detect src/ --category=creational

# Focus on specific pattern
/design-patterns detect src/ --pattern=singleton
```

### Цільові пропозиції
```bash
# Get suggestions for payment module
/design-patterns suggest src/payment/

# Focus on specific smell
/design-patterns suggest src/ --smell=switch-on-type

# High priority only
/design-patterns suggest src/ --priority=high
```

### Оцінювання якості
```bash
# Evaluate specific file
/design-patterns evaluate src/services/api-client.ts

# Evaluate all singletons
/design-patterns evaluate src/ --pattern=singleton

# Full quality report
/design-patterns evaluate src/ --detailed
```

## Інтеграція з іншими skills

Цей skill можуть успадковувати:
- `refactoring-specialist.md`: надає знання про патерни для рефакторингу
- `code-reviewer.md`: додає виявлення патернів до процесу рев'ю
- `architecture-advisor.md`: підказує архітектурні рішення на основі використання патернів

## Довідкові файли

- `reference/patterns-index.yaml`: машинозчитуваний індекс із 23 патернів з метаданими
- `reference/creational.uk.md`: документація з породжувальних патернів
- `reference/structural.uk.md`: документація зі структурних патернів
- `reference/behavioral.uk.md`: документація з поведінкових патернів
- `signatures/detection-rules.yaml`: регулярні вирази та евристики для виявлення
- `signatures/code-smells.yaml`: відповідність code smells застосовним патернам
- `signatures/stack-patterns.yaml`: правила визначення стеку та нативні еквіваленти патернів
- `checklists/pattern-evaluation.md`: критерії оцінювання якості та настанови з оцінок

## Версія

**Версія skill**: 1.0.0
**Охоплення патернів**: 23 патерни GoF
**Підтримувані стеки**: 8 (React, Angular, NestJS, Vue, Express, RxJS, Redux/Zustand, ORM)
**Останнє оновлення**: 2026-01-21
