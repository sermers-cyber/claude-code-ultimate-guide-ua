---
title: "Породжувальні патерни проєктування"
description: "Довідник із Singleton, Factory, Builder, Prototype та інших патернів створення об'єктів"
tags: [reference, design-patterns, architecture]
---

# Породжувальні патерни проєктування

Патерни, що стосуються механізмів створення об'єктів і намагаються створювати об'єкти у спосіб, який відповідає ситуації.

## Singleton

### Визначення
Гарантує, що клас має лише один екземпляр, і надає глобальну точку доступу до нього.

### Коли використовувати
- [x] Потрібен рівно один екземпляр класу (конфігурація, логування, з'єднання з базою даних)
- [x] Потрібен контрольований доступ до єдиного об'єкта
- [x] Екземпляр має бути розширюваним через наслідування

**Попередження**: часто використовується надміру. Спершу розгляньте впровадження залежностей (DI) або альтернативи на основі контексту.

### Сигнатура TypeScript
```typescript
class Singleton {
  private static instance: Singleton;
  private constructor() {
    // Private constructor prevents instantiation
  }

  public static getInstance(): Singleton {
    if (!Singleton.instance) {
      Singleton.instance = new Singleton();
    }
    return Singleton.instance;
  }

  public someMethod(): void {
    // Business logic
  }
}

// Usage
const instance = Singleton.getInstance();
```

### Нативні альтернативи стеку

**React**:
```typescript
// Instead of Singleton, use Context
const ConfigContext = createContext<Config>(defaultConfig);

export const ConfigProvider = ({ children }: Props) => {
  const [config] = useState(() => loadConfig());
  return <ConfigContext.Provider value={config}>{children}</ConfigContext.Provider>;
};
```

**Angular**:
```typescript
// Injectable service (singleton by default)
@Injectable({ providedIn: 'root' })
export class ConfigService {
  // Automatically singleton via DI
}
```

**NestJS**:
```typescript
@Injectable() // Default scope is SINGLETON
export class AppService {}
```

### Маркери виявлення
- `private constructor`
- Метод `static getInstance()`
- Поле `private static instance`
- Перевірка лінивої ініціалізації: `if (!instance)`

### Code smells, які він усуває
- **Доступ до глобального стану**: надає контрольований доступ замість розкиданих глобальних змінних
- **Кілька екземплярів спільного ресурсу**: гарантує єдине з'єднання з базою даних, об'єкт конфігурації тощо

### Поширені помилки
- **Важко тестувати**: статичні методи й глобальний стан ускладнюють модульне тестування
  - *Рішення*: використовуйте натомість впровадження залежностей або надайте `resetInstance()` для тестів
- **Проблеми потокобезпеки**: (менш актуально в однопотоковій моделі JavaScript, але важливо для воркерів Node.js)
- **Приховані залежності**: класи, що використовують `getInstance()`, мають приховане зчеплення
- **Порушує принцип єдиної відповідальності**: часто керує і створенням екземпляра, і бізнес-логікою

### Критерії оцінювання
- **Тестованість**: 3/10 (важко мокати, глобальний стан)
- **Потокобезпека**: 7/10 (менш критично в JS)
- **Розширюваність**: 5/10 (наслідування складне)

---

## Factory method

### Визначення
Визначає інтерфейс для створення об'єкта, але дозволяє підкласам вирішувати, екземпляр якого класу створювати.

### Коли використовувати
- [x] Клас не може передбачити тип об'єктів, які йому потрібно створювати
- [x] Клас хоче, щоб його підкласи визначали об'єкти, які він створює
- [x] Треба централізувати логіку створення об'єктів, щоб уникнути дублювання
- [x] Треба відокремити створення об'єкта від його використання

### Сигнатура TypeScript
```typescript
// Product interface
interface Product {
  operation(): string;
}

// Concrete products
class ConcreteProductA implements Product {
  operation(): string {
    return 'Product A';
  }
}

class ConcreteProductB implements Product {
  operation(): string {
    return 'Product B';
  }
}

// Creator (Factory)
abstract class Creator {
  // Factory method
  abstract createProduct(): Product;

  // Business logic using the product
  someOperation(): string {
    const product = this.createProduct();
    return `Creator: ${product.operation()}`;
  }
}

// Concrete creators
class CreatorA extends Creator {
  createProduct(): Product {
    return new ConcreteProductA();
  }
}

class CreatorB extends Creator {
  createProduct(): Product {
    return new ConcreteProductB();
  }
}

// Usage
const creator: Creator = new CreatorA();
console.log(creator.someOperation());
```

### Сучасна альтернатива на TypeScript
```typescript
// Simpler approach without inheritance
type ProductType = 'A' | 'B';

function createProduct(type: ProductType): Product {
  switch (type) {
    case 'A': return new ConcreteProductA();
    case 'B': return new ConcreteProductB();
  }
}
```

### Маркери виявлення
- Метод із назвою `create*()`, що повертає інтерфейс/абстрактний клас
- `abstract createProduct()` у базовому класі
- Підкласи перевизначають фабричний метод
- `switch` або `if-else` за параметром типу/виду

### Code smells, які він усуває
- **Тісне зчеплення з конкретними класами**: клієнтський код залежить від інтерфейсу, а не від реалізації
- **Дублювання логіки створення екземплярів**: централізовано у фабричному методі
- **Розкидані оператори switch**: зібрані в одному місці

### Поширені помилки
- **Плутанина із Simple Factory**: Factory Method використовує наслідування; Simple Factory використовує композицію
- **Забагато параметрів**: фабрика має створювати об'єкти з конфігурацією за замовчуванням
- **Фабричний метод не зроблено абстрактним**: це зводить нанівець спеціалізацію в підкласах

### Критерії оцінювання
- **Тестованість**: 8/10 (продукти легко мокати)
- **Гнучкість**: 9/10 (нові продукти не змінюють наявний код)
- **Складність**: 6/10 (додає ієрархію наслідування)

---

## Abstract factory

### Визначення
Надає інтерфейс для створення сімейств пов'язаних або залежних об'єктів без зазначення їхніх конкретних класів.

### Коли використовувати
- [x] Система має не залежати від того, як створюються її продукти
- [x] Систему треба конфігурувати одним із кількох сімейств продуктів
- [x] Сімейство пов'язаних об'єктів-продуктів має використовуватися разом
- [x] Ви хочете надати бібліотеку продуктів і розкрити лише інтерфейси

### Сигнатура TypeScript
```typescript
// Abstract products
interface AbstractProductA {
  usefulFunctionA(): string;
}

interface AbstractProductB {
  usefulFunctionB(): string;
  anotherFunctionB(collaborator: AbstractProductA): string;
}

// Concrete products - Family 1
class ConcreteProductA1 implements AbstractProductA {
  usefulFunctionA(): string {
    return 'Product A1';
  }
}

class ConcreteProductB1 implements AbstractProductB {
  usefulFunctionB(): string {
    return 'Product B1';
  }

  anotherFunctionB(collaborator: AbstractProductA): string {
    return `B1 collaborating with ${collaborator.usefulFunctionA()}`;
  }
}

// Concrete products - Family 2
class ConcreteProductA2 implements AbstractProductA {
  usefulFunctionA(): string {
    return 'Product A2';
  }
}

class ConcreteProductB2 implements AbstractProductB {
  usefulFunctionB(): string {
    return 'Product B2';
  }

  anotherFunctionB(collaborator: AbstractProductA): string {
    return `B2 collaborating with ${collaborator.usefulFunctionA()}`;
  }
}

// Abstract factory
interface AbstractFactory {
  createProductA(): AbstractProductA;
  createProductB(): AbstractProductB;
}

// Concrete factories
class ConcreteFactory1 implements AbstractFactory {
  createProductA(): AbstractProductA {
    return new ConcreteProductA1();
  }

  createProductB(): AbstractProductB {
    return new ConcreteProductB1();
  }
}

class ConcreteFactory2 implements AbstractFactory {
  createProductA(): AbstractProductA {
    return new ConcreteProductA2();
  }

  createProductB(): AbstractProductB {
    return new ConcreteProductB2();
  }
}

// Client code
function clientCode(factory: AbstractFactory) {
  const productA = factory.createProductA();
  const productB = factory.createProductB();

  console.log(productB.anotherFunctionB(productA));
}

// Usage
clientCode(new ConcreteFactory1());
clientCode(new ConcreteFactory2());
```

### Маркери виявлення
- Кілька методів `create*()` в інтерфейсі фабрики
- Сімейства пов'язаних продуктів (наприклад, Button + Checkbox для Windows/Mac)
- Реалізації фабрики повертають різні сімейства продуктів
- Інтерфейс із 2+ фабричними методами

### Code smells, які він усуває
- **Неузгоджені сімейства продуктів**: гарантує, що сумісні продукти створюються разом (Windows Button + Windows Checkbox, а не впереміш)
- **Розкидана логіка створення**: централізує створення пов'язаних об'єктів

### Поширені помилки
- **Надмірне ускладнення**: часто занадто складно для простих сценаріїв; може вистачити Factory Method
- **Жорсткі сімейства продуктів**: додавання нових типів продуктів вимагає змінювати всі фабрики
- **Плутанина з Factory Method**: Abstract Factory створює сімейства; Factory Method створює один тип продукту

### Критерії оцінювання
- **Тестованість**: 8/10 (фабрики легко мокати)
- **Узгодженість**: 10/10 (гарантує сумісні продукти)
- **Складність**: 4/10 (висока складність, багато класів)

---

## Builder

### Визначення
Відокремлює конструювання складного об'єкта від його подання, дозволяючи будувати його покроково.

### Коли використовувати
- [x] Об'єкт має багато необов'язкових параметрів (>4)
- [x] Процес конструювання має дозволяти різні подання
- [x] Потрібно будувати складні об'єкти покроково
- [x] Хочете уникнути антипатерна «телескопічний конструктор»

### Сигнатура TypeScript
```typescript
// Product
class House {
  public walls: string = '';
  public doors: number = 0;
  public windows: number = 0;
  public roof: string = '';
  public garage: boolean = false;
  public pool: boolean = false;

  public describe(): string {
    return `House with ${this.walls} walls, ${this.doors} doors, ${this.windows} windows, ${this.roof} roof, garage: ${this.garage}, pool: ${this.pool}`;
  }
}

// Builder
class HouseBuilder {
  private house: House;

  constructor() {
    this.house = new House();
  }

  public setWalls(walls: string): this {
    this.house.walls = walls;
    return this;
  }

  public setDoors(doors: number): this {
    this.house.doors = doors;
    return this;
  }

  public setWindows(windows: number): this {
    this.house.windows = windows;
    return this;
  }

  public setRoof(roof: string): this {
    this.house.roof = roof;
    return this;
  }

  public addGarage(): this {
    this.house.garage = true;
    return this;
  }

  public addPool(): this {
    this.house.pool = true;
    return this;
  }

  public build(): House {
    const result = this.house;
    this.house = new House(); // Reset for next build
    return result;
  }
}

// Usage
const house = new HouseBuilder()
  .setWalls('brick')
  .setDoors(2)
  .setWindows(6)
  .setRoof('tile')
  .addGarage()
  .build();
```

### Сучасна альтернатива на TypeScript (типобезпечний builder)
```typescript
// Progressive type safety: each step unlocks the next
type HouseBuilderState<
  TWalls extends boolean = false,
  TRoof extends boolean = false
> = {
  setWalls: TWalls extends true ? never : (walls: string) => HouseBuilderState<true, TRoof>;
  setRoof: TRoof extends true ? never : (roof: string) => HouseBuilderState<TWalls, true>;
  build: TWalls extends true ? (TRoof extends true ? () => House : never) : never;
};
```

### Маркери виявлення
- Ланцюжок викликів методів (повертає `this` або тип builder)
- Метод `build()`, що повертає кінцевий продукт
- Методи `with*()` або `set*()`
- Необов'язкові поля встановлюються поступово

### Code smells, які він усуває
- **Телескопічний конструктор**: конструктор із великою кількістю параметрів
  ```typescript
  // Bad
  new House(walls, doors, windows, roof, garage, pool, garden, basement, ...);

  // Good with Builder
  new HouseBuilder().setWalls('brick').setRoof('tile').build();
  ```
- **Незрозумілий порядок параметрів**: іменовані методи роблять намір очевидним
- **Складність необов'язкових параметрів**: Builder елегантно обробляє необов'язкові можливості

### Поширені помилки
- **Змінюваний builder**: повторне використання builder може призвести до неочікуваного стану
  - *Рішення*: скидайте внутрішній стан після `build()`
- **Неповний builder**: обов'язкові поля не перевіряються в `build()`
  - *Рішення*: використовуйте типи TypeScript, щоб примусово вимагати обов'язкові кроки
- **Занадто просто для патерна**: якщо параметрів <4, конструктор або об'єктний літерал можуть бути простішими

### Критерії оцінювання
- **Тестованість**: 9/10 (легко створювати тестові фікстури)
- **Читабельність**: 10/10 (fluent-інтерфейс документує сам себе)
- **Складність**: 7/10 (додає клас builder)

---

## Prototype

### Визначення
Створює нові об'єкти копіюванням наявного об'єкта (прототипу), а не з нуля.

### Коли використовувати
- [x] Створення об'єкта дороге (складна ініціалізація, запити до бази даних)
- [x] Треба уникнути наслідування лише заради зміни ініціалізації
- [x] Система має не залежати від того, як створюються продукти
- [x] Класи для створення екземплярів визначаються під час виконання

### Сигнатура TypeScript
```typescript
// Prototype interface
interface Prototype {
  clone(): Prototype;
}

// Concrete prototype
class ConcretePrototype implements Prototype {
  public field: number;
  public complexObject: { data: string };

  constructor(field: number, complexObject: { data: string }) {
    this.field = field;
    this.complexObject = complexObject;
  }

  // Shallow clone
  public clone(): ConcretePrototype {
    return Object.create(this);
  }

  // Deep clone
  public deepClone(): ConcretePrototype {
    return new ConcretePrototype(
      this.field,
      { data: this.complexObject.data } // Clone nested objects
    );
  }
}

// Usage
const original = new ConcretePrototype(42, { data: 'important' });
const shallowCopy = original.clone();
const deepCopy = original.deepClone();

// Shallow copy shares nested objects
shallowCopy.complexObject.data = 'modified';
console.log(original.complexObject.data); // 'modified' (!)

// Deep copy is independent
deepCopy.field = 99;
console.log(original.field); // 42 (unchanged)
```

### Сучасні альтернативи на JavaScript
```typescript
// Spread operator (shallow)
const copy1 = { ...original };

// Object.assign (shallow)
const copy2 = Object.assign({}, original);

// structuredClone (deep, modern browsers/Node 17+)
const copy3 = structuredClone(original);

// JSON (deep, but limited: no functions, undefined, etc.)
const copy4 = JSON.parse(JSON.stringify(original));
```

### Маркери виявлення
- Метод `clone()`
- `Object.create()`
- `structuredClone()`
- Патерн `JSON.parse(JSON.stringify())`
- Spread-оператор `{ ...obj }`

### Code smells, які він усуває
- **Дорога ініціалізація**: клонування замість повторної ініціалізації
- **Складні графи об'єктів**: клонування зберігає зв'язки
- **Визначення типу під час виконання**: клонування прототипу замість жорсткого кодування типів

### Поширені помилки
- **Плутанина між поверхневим і глибоким клонуванням**: поверхнева копія спільно використовує вкладені об'єкти
  ```typescript
  // Dangerous if nested objects are modified
  const shallow = { ...original };
  ```
- **Циклічні посилання**: `JSON.stringify` падає на циклічних посиланнях
  - *Рішення*: використовуйте `structuredClone()` або власну логіку клонування
- **Клонування методів/функцій**: деякі підходи втрачають методи
  ```typescript
  JSON.parse(JSON.stringify(obj)); // Loses all methods!
  ```
- **Не клонується приватний стан**: переконайтеся, що весь потрібний стан скопійовано

### Критерії оцінювання
- **Продуктивність**: 9/10 (швидше за повторну ініціалізацію)
- **Простота**: 7/10 (поверхневе й глибоке клонування підступні)
- **Надійність**: 6/10 (легко помилитися з вкладеними об'єктами)

---

## Зведена таблиця

| Патерн | Складність | Частота використання | Головна перевага |
|---------|------------|---------------|--------------|
| Singleton | Низька | Висока | Контроль глобального доступу |
| Factory Method | Середня | Висока | Відокремлює створення від використання |
| Abstract Factory | Висока | Середня | Узгоджені сімейства продуктів |
| Builder | Середня | Висока | Fluent-конструювання складних об'єктів |
| Prototype | Низька | Низька | Ефективне клонування |

## Найкращі практики

1. **Надавайте перевагу композиції над наслідуванням**: Factory і Builder часто кращі за Singleton
2. **Використовуйте нативні альтернативи стеку**: React Context > Singleton, DI > getInstance()
3. **Використовуйте можливості TypeScript**: generics і обмеження типів для типобезпечних builder
4. **Дизайн, зручний для тестування**: уникайте Singleton; використовуйте впровадження залежностей
5. **Спершу простота**: не використовуйте Abstract Factory, коли вистачає Factory Method

## Джерела

- *Design Patterns: Elements of Reusable Object-Oriented Software* (Gang of Four)
- *Effective TypeScript*, Dan Vanderkam
- [Refactoring Guru: Creational Patterns](https://refactoring.guru/design-patterns/creational-patterns)
