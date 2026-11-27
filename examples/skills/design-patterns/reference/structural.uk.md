---
title: "Структурні патерни проєктування"
description: "Довідник з Adapter, Decorator, Facade, Proxy та інших патернів композиції"
tags: [reference, design-patterns, architecture]
---

# Структурні патерни проєктування

Патерни, що стосуються композиції об'єктів і зв'язків між сутностями та пропонують способи збирати об'єкти й класи у більші структури.

## Adapter

### Визначення
Перетворює інтерфейс класу на інший інтерфейс, якого очікують клієнти, дозволяючи несумісним інтерфейсам працювати разом.

### Коли використовувати
- [x] Хочете використати наявний клас із несумісним інтерфейсом
- [x] Треба інтегрувати сторонні бібліотеки з іншими інтерфейсами
- [x] Хочете створити повторно використовуваний клас, що співпрацює з непов'язаними класами
- [x] Legacy-код має працювати з новими системами

### Сигнатура TypeScript
```typescript
// Target interface (what client expects)
interface Target {
  request(): string;
}

// Adaptee (existing incompatible class)
class Adaptee {
  specificRequest(): string {
    return '.eetpadA eht fo roivaheb laicepS';
  }
}

// Adapter (makes Adaptee compatible with Target)
class Adapter implements Target {
  private adaptee: Adaptee;

  constructor(adaptee: Adaptee) {
    this.adaptee = adaptee;
  }

  public request(): string {
    const result = this.adaptee.specificRequest().split('').reverse().join('');
    return `Adapter: ${result}`;
  }
}

// Client code
function clientCode(target: Target) {
  console.log(target.request());
}

// Usage
const adaptee = new Adaptee();
const adapter = new Adapter(adaptee);
clientCode(adapter);
```

### Приклад із практики: інтеграція сторонньої бібліотеки
```typescript
// Third-party library (can't modify)
class XMLDataProvider {
  getXMLData(): string {
    return '<data><item>1</item></data>';
  }
}

// Your application expects JSON
interface JSONDataProvider {
  getJSONData(): object;
}

// Adapter
class XMLToJSONAdapter implements JSONDataProvider {
  constructor(private xmlProvider: XMLDataProvider) {}

  getJSONData(): object {
    const xml = this.xmlProvider.getXMLData();
    // Convert XML to JSON (simplified)
    return { data: { item: '1' } };
  }
}

// Usage
const xmlProvider = new XMLDataProvider();
const adapter = new XMLToJSONAdapter(xmlProvider);
const data = adapter.getJSONData();
```

### Маркери виявлення
- Клас реалізує цільовий інтерфейс
- Тримає посилання на адаптований об'єкт (adaptee)
- Делегує adaptee з перетворенням інтерфейсу
- Назви на кшталт `*Adapter`, `*Wrapper`

### Code smells, які він усуває
- **Несумісні інтерфейси**: робить legacy- або сторонній код сумісним
- **Розростання інтерфейсів**: один адаптер замість зміни багатьох клієнтських викликів

### Поширені помилки
- **Двосторонні адаптери**: двонаправлене перетворення складне; створіть два адаптери
- **Ланцюжки адаптерів**: кілька адаптерів поспіль вказують на проблеми дизайну
- **Надмірне використання в новому коді**: проєктуйте сумісні інтерфейси від початку

---

## Bridge

### Визначення
Відокремлює абстракцію від її реалізації, щоб обидві могли змінюватися незалежно.

### Коли використовувати
- [x] Хочете уникнути постійного зв'язування абстракції та реалізації
- [x] І абстракції, і реалізації мають бути розширюваними через наслідування
- [x] Зміни в реалізації не повинні впливати на клієнтів
- [x] Хочете спільно використовувати реалізацію між кількома об'єктами (на зразок Flyweight)

### Сигнатура TypeScript
```typescript
// Implementation interface
interface Implementation {
  operationImpl(): string;
}

// Concrete implementations
class ConcreteImplementationA implements Implementation {
  operationImpl(): string {
    return 'ConcreteImplementationA';
  }
}

class ConcreteImplementationB implements Implementation {
  operationImpl(): string {
    return 'ConcreteImplementationB';
  }
}

// Abstraction
class Abstraction {
  constructor(protected implementation: Implementation) {}

  public operation(): string {
    return `Abstraction: ${this.implementation.operationImpl()}`;
  }
}

// Refined abstraction
class ExtendedAbstraction extends Abstraction {
  public operation(): string {
    return `ExtendedAbstraction: ${this.implementation.operationImpl()}`;
  }
}

// Usage
const implA = new ConcreteImplementationA();
const abstraction1 = new Abstraction(implA);
console.log(abstraction1.operation());

const implB = new ConcreteImplementationB();
const abstraction2 = new ExtendedAbstraction(implB);
console.log(abstraction2.operation());
```

### Приклад із практики: UI-компоненти з кількома рендерерами
```typescript
// Implementation: Renderers
interface Renderer {
  renderCircle(radius: number): string;
  renderSquare(side: number): string;
}

class VectorRenderer implements Renderer {
  renderCircle(radius: number): string {
    return `Drawing circle (vector) with radius ${radius}`;
  }
  renderSquare(side: number): string {
    return `Drawing square (vector) with side ${side}`;
  }
}

class RasterRenderer implements Renderer {
  renderCircle(radius: number): string {
    return `Drawing circle (pixels) with radius ${radius}`;
  }
  renderSquare(side: number): string {
    return `Drawing square (pixels) with side ${side}`;
  }
}

// Abstraction: Shapes
abstract class Shape {
  constructor(protected renderer: Renderer) {}
  abstract draw(): string;
}

class Circle extends Shape {
  constructor(renderer: Renderer, private radius: number) {
    super(renderer);
  }
  draw(): string {
    return this.renderer.renderCircle(this.radius);
  }
}

class Square extends Shape {
  constructor(renderer: Renderer, private side: number) {
    super(renderer);
  }
  draw(): string {
    return this.renderer.renderSquare(this.side);
  }
}

// Usage: Can mix any shape with any renderer
const vectorCircle = new Circle(new VectorRenderer(), 5);
const rasterSquare = new Square(new RasterRenderer(), 10);
```

### Маркери виявлення
- Абстракція тримає посилання на інтерфейс реалізації
- Конструктор впроваджує реалізацію
- Дві паралельні ієрархії (абстракції та реалізації)

### Поширені помилки
- **Плутанина з Adapter**: Bridge закладається на етапі проєктування; Adapter є виправленням під час виконання
- **Надмірне ускладнення простих сценаріїв**: використовуйте лише тоді, коли обидві ієрархії мають змінюватися

---

## Composite

### Визначення
Компонує об'єкти в деревоподібні структури для подання ієрархій «частина-ціле», дозволяючи клієнтам однаково працювати з окремими об'єктами та їхніми композиціями.

### Коли використовувати
- [x] Хочете подати ієрархії об'єктів «частина-ціле»
- [x] Хочете, щоб клієнти не розрізняли композиції та окремі об'єкти
- [x] Деревоподібні структури природні для предметної області (файлові системи, UI-компоненти, оргструктури)

### Сигнатура TypeScript
```typescript
// Component interface
interface Component {
  operation(): string;
  add?(component: Component): void;
  remove?(component: Component): void;
  getChild?(index: number): Component;
}

// Leaf (no children)
class Leaf implements Component {
  constructor(private name: string) {}

  operation(): string {
    return this.name;
  }
}

// Composite (has children)
class Composite implements Component {
  private children: Component[] = [];

  constructor(private name: string) {}

  add(component: Component): void {
    this.children.push(component);
  }

  remove(component: Component): void {
    const index = this.children.indexOf(component);
    if (index !== -1) {
      this.children.splice(index, 1);
    }
  }

  getChild(index: number): Component {
    return this.children[index];
  }

  operation(): string {
    const results = this.children.map(child => child.operation());
    return `${this.name}(${results.join(', ')})`;
  }
}

// Usage
const tree = new Composite('root');
const branch1 = new Composite('branch1');
branch1.add(new Leaf('leaf1'));
branch1.add(new Leaf('leaf2'));

const branch2 = new Composite('branch2');
branch2.add(new Leaf('leaf3'));

tree.add(branch1);
tree.add(branch2);
tree.add(new Leaf('leaf4'));

console.log(tree.operation());
// Output: root(branch1(leaf1, leaf2), branch2(leaf3), leaf4)
```

### Приклад із практики: файлова система
```typescript
interface FileSystemComponent {
  getName(): string;
  getSize(): number;
  print(indent: string): void;
}

class File implements FileSystemComponent {
  constructor(private name: string, private size: number) {}

  getName(): string {
    return this.name;
  }

  getSize(): number {
    return this.size;
  }

  print(indent: string): void {
    console.log(`${indent}📄 ${this.name} (${this.size} bytes)`);
  }
}

class Directory implements FileSystemComponent {
  private children: FileSystemComponent[] = [];

  constructor(private name: string) {}

  add(component: FileSystemComponent): void {
    this.children.push(component);
  }

  getName(): string {
    return this.name;
  }

  getSize(): number {
    return this.children.reduce((sum, child) => sum + child.getSize(), 0);
  }

  print(indent: string): void {
    console.log(`${indent}📁 ${this.name} (${this.getSize()} bytes)`);
    this.children.forEach(child => child.print(indent + '  '));
  }
}

// Usage
const root = new Directory('root');
const home = new Directory('home');
home.add(new File('photo.jpg', 2048));
home.add(new File('document.pdf', 4096));

const work = new Directory('work');
work.add(new File('report.docx', 8192));

root.add(home);
root.add(work);
root.print('');
```

### Маркери виявлення
- Деревоподібна структура з однаковим інтерфейсом
- Колекція дочірніх компонентів
- Методи `add()`, `remove()`, `getChild()`
- Рекурсивні виклики операцій

### Code smells, які він усуває
- **Перевірка типу «композиція чи лист»**: однаковий інтерфейс усуває перевірки `instanceof`
- **Різна обробка частин і цілого**: клієнти працюють з обома однаково

### Поширені помилки
- **Порушення однаковості**: Leaf і Composite повинні мати той самий інтерфейс
- **Неправильне керування дочірніми елементами**: некоректна обробка видалення
- **Глибока рекурсія**: може спричинити переповнення стеку на дуже глибоких деревах

---

## Decorator

### Визначення
Динамічно додає об'єкту додаткові обов'язки, пропонуючи гнучку альтернативу наслідуванню для розширення функціональності.

### Коли використовувати
- [x] Треба додавати обов'язки об'єктам динамічно й прозоро
- [x] Обов'язки можна знімати
- [x] Розширення через наслідування непрактичне (багато можливих комбінацій)
- [x] Хочете додавати можливості поступово

### Сигнатура TypeScript
```typescript
// Component interface
interface Component {
  operation(): string;
}

// Concrete component
class ConcreteComponent implements Component {
  operation(): string {
    return 'ConcreteComponent';
  }
}

// Base decorator
abstract class Decorator implements Component {
  constructor(protected component: Component) {}

  operation(): string {
    return this.component.operation();
  }
}

// Concrete decorators
class DecoratorA extends Decorator {
  operation(): string {
    return `DecoratorA(${super.operation()})`;
  }
}

class DecoratorB extends Decorator {
  operation(): string {
    return `DecoratorB(${super.operation()})`;
  }
}

// Usage: Stack decorators
const simple = new ConcreteComponent();
const decorated1 = new DecoratorA(simple);
const decorated2 = new DecoratorB(decorated1);
console.log(decorated2.operation());
// Output: DecoratorB(DecoratorA(ConcreteComponent))
```

### Нативні альтернативи стеку

**React - компоненти вищого порядку (HOC)**:
```typescript
// HOC decorator
function withAuth<P extends object>(
  Component: React.ComponentType<P>
): React.ComponentType<P> {
  return (props: P) => {
    const { user } = useAuth();
    if (!user) return <Redirect to="/login" />;
    return <Component {...props} />;
  };
}

// Usage: Stack decorators
const AuthenticatedProfile = withAuth(Profile);
const AuthenticatedAdminProfile = withLogging(withAuth(Profile));
```

**NestJS - інтерсептори**:
```typescript
@Injectable()
export class LoggingInterceptor implements NestInterceptor {
  intercept(context: ExecutionContext, next: CallHandler): Observable<any> {
    console.log('Before...');
    return next.handle().pipe(
      tap(() => console.log('After...'))
    );
  }
}

// Apply decorator
@UseInterceptors(LoggingInterceptor)
@Controller('users')
export class UsersController {}
```

### Маркери виявлення
- Реалізує той самий інтерфейс, що й обгорнутий об'єкт
- Тримає посилання на обгорнутий об'єкт
- Делегує обгорнутому об'єкту, додаючи поведінку
- Можна накладати шарами

### Code smells, які він усуває
- **Вибух кількості класів**: не потрібно створювати підклас для кожної комбінації можливостей
- **Жорстке додавання можливостей**: можливості додаються й прибираються динамічно

### Поширені помилки
- **Залежність від порядку**: DecoratorA(DecoratorB(x)) ≠ DecoratorB(DecoratorA(x))
- **Вибух кількості декораторів**: забагато дрібних декораторів важко контролювати
- **Порушення інтерфейсу**: декоратор має зберігати контракт інтерфейсу

---

## Facade

### Визначення
Надає єдиний інтерфейс до набору інтерфейсів підсистеми, спрощуючи її використання.

### Коли використовувати
- [x] Хочете надати простий інтерфейс до складної підсистеми
- [x] Між клієнтами та класами реалізації багато залежностей
- [x] Хочете розбити підсистеми на шари
- [x] Треба відокремити підсистему від клієнтів

### Сигнатура TypeScript
```typescript
// Complex subsystem classes
class SubsystemA {
  operationA(): string {
    return 'SubsystemA';
  }
}

class SubsystemB {
  operationB(): string {
    return 'SubsystemB';
  }
}

class SubsystemC {
  operationC(): string {
    return 'SubsystemC';
  }
}

// Facade
class Facade {
  private subsystemA: SubsystemA;
  private subsystemB: SubsystemB;
  private subsystemC: SubsystemC;

  constructor() {
    this.subsystemA = new SubsystemA();
    this.subsystemB = new SubsystemB();
    this.subsystemC = new SubsystemC();
  }

  // Simplified interface
  public simpleOperation(): string {
    const resultA = this.subsystemA.operationA();
    const resultB = this.subsystemB.operationB();
    const resultC = this.subsystemC.operationC();
    return `Facade coordinates: ${resultA}, ${resultB}, ${resultC}`;
  }
}

// Client code
const facade = new Facade();
console.log(facade.simpleOperation());
// Instead of:
// const a = new SubsystemA(); const b = new SubsystemB(); const c = new SubsystemC();
// a.operationA(); b.operationB(); c.operationC();
```

### Приклад із практики: обробка платежів
```typescript
// Complex subsystems
class PaymentValidator {
  validate(amount: number, card: string): boolean {
    // Complex validation logic
    return amount > 0 && card.length === 16;
  }
}

class PaymentGateway {
  charge(amount: number, card: string): string {
    return `Charged $${amount} to ${card}`;
  }
}

class NotificationService {
  sendReceipt(email: string, transactionId: string): void {
    console.log(`Receipt sent to ${email}: ${transactionId}`);
  }
}

class TransactionLogger {
  log(transaction: string): void {
    console.log(`Logged: ${transaction}`);
  }
}

// Facade
class PaymentFacade {
  private validator = new PaymentValidator();
  private gateway = new PaymentGateway();
  private notifications = new NotificationService();
  private logger = new TransactionLogger();

  processPayment(amount: number, card: string, email: string): boolean {
    // Simplified interface for complex process
    if (!this.validator.validate(amount, card)) {
      return false;
    }

    const result = this.gateway.charge(amount, card);
    this.logger.log(result);
    this.notifications.sendReceipt(email, result);
    return true;
  }
}

// Client code (simple!)
const payment = new PaymentFacade();
payment.processPayment(100, '1234567890123456', 'user@example.com');
```

### Маркери виявлення
- Клас із кількома залежностями від підсистем
- Прості публічні методи, що координують підсистеми
- Назви `*Facade`, `*API`, `*Service`

### Code smells, які він усуває
- **Складне використання підсистеми**: клієнтам не потрібно знати деталі підсистеми
- **Тісне зчеплення**: клієнти залежать від фасаду, а не від багатьох класів

### Поширені помилки
- **God Facade**: фасад робить забагато; він має координувати, а не містити логіку
- **Протікаюча абстракція**: розкриття деталей підсистеми зводить нанівець сенс патерна

---

## Flyweight

### Визначення
Використовує спільне використання, щоб ефективно підтримувати велику кількість дрібних об'єктів, зберігаючи спільний стан зовні.

### Коли використовувати
- [x] Застосунок використовує велику кількість об'єктів
- [x] Витрати на зберігання високі через кількість об'єктів
- [x] Більшу частину стану об'єкта можна зробити зовнішнім (винести назовні)
- [x] Багато груп об'єктів можна замінити відносно невеликою кількістю спільних об'єктів

### Сигнатура TypeScript
```typescript
// Flyweight
class Flyweight {
  constructor(private sharedState: string) {}

  operation(uniqueState: string): void {
    console.log(`Flyweight: Shared (${this.sharedState}) and unique (${uniqueState}) state.`);
  }
}

// Flyweight factory
class FlyweightFactory {
  private flyweights: Map<string, Flyweight> = new Map();

  constructor(initialFlyweights: string[][]) {
    for (const state of initialFlyweights) {
      this.flyweights.set(this.getKey(state), new Flyweight(state.join('_')));
    }
  }

  private getKey(state: string[]): string {
    return state.join('_');
  }

  getFlyweight(sharedState: string[]): Flyweight {
    const key = this.getKey(sharedState);

    if (!this.flyweights.has(key)) {
      console.log('Creating new flyweight');
      this.flyweights.set(key, new Flyweight(key));
    } else {
      console.log('Reusing existing flyweight');
    }

    return this.flyweights.get(key)!;
  }

  listFlyweights(): void {
    console.log(`FlyweightFactory: ${this.flyweights.size} flyweights:`);
    for (const key of this.flyweights.keys()) {
      console.log(key);
    }
  }
}

// Usage
const factory = new FlyweightFactory([
  ['Chevrolet', 'Camaro2018', 'pink'],
  ['Mercedes Benz', 'C300', 'black'],
]);

const flyweight1 = factory.getFlyweight(['Chevrolet', 'Camaro2018', 'pink']);
flyweight1.operation('license-123');

const flyweight2 = factory.getFlyweight(['Chevrolet', 'Camaro2018', 'pink']);
flyweight2.operation('license-456'); // Reuses same flyweight
```

### Приклад із практики: символи в текстовому редакторі
```typescript
// Flyweight: Character formatting (shared)
class CharacterFormat {
  constructor(
    public font: string,
    public size: number,
    public color: string
  ) {}
}

// Flyweight factory
class FormatFactory {
  private formats = new Map<string, CharacterFormat>();

  getFormat(font: string, size: number, color: string): CharacterFormat {
    const key = `${font}_${size}_${color}`;
    if (!this.formats.has(key)) {
      this.formats.set(key, new CharacterFormat(font, size, color));
    }
    return this.formats.get(key)!;
  }
}

// Character with extrinsic state
class Character {
  constructor(
    private char: string,
    private format: CharacterFormat // Shared flyweight
  ) {}

  render(position: number): string {
    return `'${this.char}' at ${position} (${this.format.font}, ${this.format.size}px, ${this.format.color})`;
  }
}

// Document
const formatFactory = new FormatFactory();
const arial12Black = formatFactory.getFormat('Arial', 12, 'black');
const arial12Red = formatFactory.getFormat('Arial', 12, 'red');

// 10,000 characters, but only 2 format objects
const characters: Character[] = [];
for (let i = 0; i < 10000; i++) {
  const format = i % 2 === 0 ? arial12Black : arial12Red;
  characters.push(new Character('A', format));
}
```

### Маркери виявлення
- Фабрика, що керує пулом спільних об'єктів
- Розділення внутрішнього (спільного) і зовнішнього (унікального) стану
- Map/кеш об'єктів-flyweight

### Поширені помилки
- **Передчасна оптимізація**: використовуйте лише тоді, коли пам'ять справді є проблемою
- **Неправильне розділення стану**: змішування внутрішнього й зовнішнього стану

---

## Proxy

### Визначення
Надає замінник або заглушку для іншого об'єкта, щоб контролювати доступ до нього.

### Коли використовувати
- [x] Лінива ініціалізація (віртуальний проксі): створювати дорогий об'єкт лише за потреби
- [x] Контроль доступу (захисний проксі): контролювати доступ до оригінального об'єкта
- [x] Локальний представник віддаленого об'єкта (віддалений проксі)
- [x] Логування, кешування або моніторинг доступу

### Сигнатура TypeScript
```typescript
// Subject interface
interface Subject {
  request(): void;
}

// Real subject
class RealSubject implements Subject {
  request(): void {
    console.log('RealSubject: Handling request');
  }
}

// Proxy
class Proxy implements Subject {
  private realSubject: RealSubject | null = null;

  request(): void {
    // Access control
    if (this.checkAccess()) {
      // Lazy initialization
      if (!this.realSubject) {
        this.realSubject = new RealSubject();
      }

      // Logging
      this.logAccess();

      // Delegate to real subject
      this.realSubject.request();
    }
  }

  private checkAccess(): boolean {
    console.log('Proxy: Checking access');
    return true;
  }

  private logAccess(): void {
    console.log('Proxy: Logging access time');
  }
}

// Usage
const proxy = new Proxy();
proxy.request();
// Output:
// Proxy: Checking access
// Proxy: Logging access time
// RealSubject: Handling request
```

### Сучасний Proxy у JavaScript
```typescript
const target = {
  message: 'Hello',
  getValue() {
    return this.message;
  }
};

const handler = {
  get(target: any, prop: string) {
    console.log(`Accessing property: ${prop}`);
    return target[prop];
  },
  set(target: any, prop: string, value: any) {
    console.log(`Setting property: ${prop} = ${value}`);
    target[prop] = value;
    return true;
  }
};

const proxy = new Proxy(target, handler);
console.log(proxy.message); // Logs: Accessing property: message
proxy.message = 'World';     // Logs: Setting property: message = World
```

### Маркери виявлення
- Реалізує той самий інтерфейс, що й реальний об'єкт
- Тримає посилання на реальний об'єкт
- Контролює доступ (перевірки, логування, кешування)
- Лінива ініціалізація реального об'єкта

### Поширені помилки
- **Ланцюжки проксі**: кілька проксі, що обгортають один одного
- **Накладні витрати на продуктивність**: кожен доступ проходить через проксі
- **Плутанина з Decorator**: Proxy контролює доступ; Decorator додає поведінку

---

## Зведена таблиця

| Патерн | Складність | Частота використання | Головна перевага |
|---------|------------|---------------|--------------|
| Adapter | Низька | Висока | Сумісність інтерфейсів |
| Bridge | Висока | Низька | Відокремлення абстракції від реалізації |
| Composite | Середня | Висока | Однакова робота з деревоподібними структурами |
| Decorator | Середня | Висока | Динамічне додавання обов'язків |
| Facade | Низька | Дуже висока | Спрощений інтерфейс підсистеми |
| Flyweight | Висока | Низька | Оптимізація пам'яті |
| Proxy | Середня | Середня | Контрольований доступ |

## Найкращі практики

1. **Adapter чи Bridge**: Adapter виправляє несумісність; Bridge закладає гнучкість у дизайн
2. **Decorator чи Proxy**: Decorator додає можливості; Proxy контролює доступ
3. **Простота Facade**: має координувати, а не містити бізнес-логіку
4. **Однаковість Composite**: Leaf і Composite мають спільно використовувати інтерфейс
5. **Використовуйте нативний Proxy**: об'єкт JavaScript `Proxy` для динамічного доступу до властивостей

## Джерела

- *Design Patterns: Elements of Reusable Object-Oriented Software* (Gang of Four)
- [MDN: Proxy](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Proxy)
- [Refactoring Guru: Structural Patterns](https://refactoring.guru/design-patterns/structural-patterns)
