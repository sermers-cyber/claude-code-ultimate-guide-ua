---
title: "Поведінкові патерни проєктування"
description: "Довідник з Observer, Strategy, Command, Chain of Responsibility та інших поведінкових патернів"
tags: [reference, design-patterns, architecture]
---

# Поведінкові патерни проєктування

Патерни, що стосуються алгоритмів і розподілу обов'язків між об'єктами та зосереджені на способах взаємодії.

## Chain of responsibility

### Визначення
Передає запити вздовж ланцюжка обробників, де кожен обробник вирішує: опрацювати запит чи передати його наступному.

### Коли використовувати
- [x] Запит може обробити більше ніж один об'єкт, а потрібний обробник заздалегідь невідомий
- [x] Хочете надіслати запит, не вказуючи одержувача явно
- [x] Набір обробників можна задавати динамічно
- [x] Порядок обробки має значення

### Сигнатура TypeScript
```typescript
interface Handler {
  setNext(handler: Handler): Handler;
  handle(request: string): string | null;
}

abstract class AbstractHandler implements Handler {
  private nextHandler: Handler | null = null;

  setNext(handler: Handler): Handler {
    this.nextHandler = handler;
    return handler; // Allows chaining: h1.setNext(h2).setNext(h3)
  }

  handle(request: string): string | null {
    if (this.nextHandler) {
      return this.nextHandler.handle(request);
    }
    return null;
  }
}

class ConcreteHandlerA extends AbstractHandler {
  handle(request: string): string | null {
    if (request === 'A') {
      return `HandlerA processed ${request}`;
    }
    return super.handle(request);
  }
}

class ConcreteHandlerB extends AbstractHandler {
  handle(request: string): string | null {
    if (request === 'B') {
      return `HandlerB processed ${request}`;
    }
    return super.handle(request);
  }
}

// Usage
const handlerA = new ConcreteHandlerA();
const handlerB = new ConcreteHandlerB();
handlerA.setNext(handlerB);

console.log(handlerA.handle('B')); // HandlerB processed B
```

### Нативні альтернативи стеку

**Express Middleware**:
```typescript
app.use(authMiddleware);
app.use(loggingMiddleware);
app.use(errorMiddleware);
```

**NestJS Guards/Interceptors**:
```typescript
@UseGuards(AuthGuard, RolesGuard)
@UseInterceptors(LoggingInterceptor)
```

### Code smells, які він усуває
- **Тісний зв'язок з обробником запиту**: клієнт не знає, який обробник опрацьовує запит
- **Складна умовна логіка**: кожен обробник має просту логіку

---

## Command

### Визначення
Інкапсулює запит як об'єкт, що дає змогу параметризувати клієнтів різними запитами, ставити запити в чергу чи логувати їх і підтримувати операції з можливістю скасування.

### Коли використовувати
- [x] Параметризувати об'єкти операціями
- [x] Ставити запити в чергу, задавати та виконувати їх у різний час
- [x] Підтримувати операції undo/redo
- [x] Логувати зміни для відновлення системи після збою

### Сигнатура TypeScript
```typescript
// Command interface
interface Command {
  execute(): void;
  undo?(): void;
}

// Receiver
class Light {
  turnOn(): void {
    console.log('Light is on');
  }
  turnOff(): void {
    console.log('Light is off');
  }
}

// Concrete commands
class TurnOnCommand implements Command {
  constructor(private light: Light) {}

  execute(): void {
    this.light.turnOn();
  }

  undo(): void {
    this.light.turnOff();
  }
}

class TurnOffCommand implements Command {
  constructor(private light: Light) {}

  execute(): void {
    this.light.turnOff();
  }

  undo(): void {
    this.light.turnOn();
  }
}

// Invoker
class RemoteControl {
  private history: Command[] = [];

  execute(command: Command): void {
    command.execute();
    this.history.push(command);
  }

  undo(): void {
    const command = this.history.pop();
    if (command?.undo) {
      command.undo();
    }
  }
}

// Usage
const light = new Light();
const remote = new RemoteControl();

remote.execute(new TurnOnCommand(light));  // Light is on
remote.execute(new TurnOffCommand(light)); // Light is off
remote.undo();                             // Light is on
```

### Нативний для стеку варіант: Redux actions
```typescript
const incrementAction = { type: 'INCREMENT', payload: 1 };
dispatch(incrementAction); // Command pattern
```

---

## Iterator

### Визначення
Надає спосіб послідовно отримувати доступ до елементів колекції, не розкриваючи її внутрішнього представлення.

### Коли використовувати
- [x] Потрібен доступ до вмісту колекції без розкриття її внутрішньої структури
- [x] Підтримувати кілька способів обходу колекцій
- [x] Надати єдиний інтерфейс для обходу різних структур

### Сигнатура TypeScript
```typescript
// Iterator interface
interface Iterator<T> {
  next(): { value: T; done: boolean };
  hasNext(): boolean;
}

// Iterable collection
interface Iterable<T> {
  createIterator(): Iterator<T>;
}

// Concrete iterator
class ArrayIterator<T> implements Iterator<T> {
  private position = 0;

  constructor(private collection: T[]) {}

  next(): { value: T; done: boolean } {
    if (this.position < this.collection.length) {
      return { value: this.collection[this.position++], done: false };
    }
    return { value: null as any, done: true };
  }

  hasNext(): boolean {
    return this.position < this.collection.length;
  }
}

// Collection
class NumberCollection implements Iterable<number> {
  constructor(private items: number[]) {}

  createIterator(): Iterator<number> {
    return new ArrayIterator(this.items);
  }
}
```

### Нативна підтримка в JavaScript
```typescript
// Symbol.iterator
const collection = {
  items: [1, 2, 3],
  [Symbol.iterator]() {
    let index = 0;
    const items = this.items;
    return {
      next() {
        return index < items.length
          ? { value: items[index++], done: false }
          : { done: true, value: undefined };
      }
    };
  }
};

for (const item of collection) {
  console.log(item); // 1, 2, 3
}

// Generator (simpler)
function* numberGenerator() {
  yield 1;
  yield 2;
  yield 3;
}

for (const num of numberGenerator()) {
  console.log(num);
}
```

---

## Mediator

### Визначення
Визначає об'єкт, що інкапсулює взаємодію набору об'єктів, і забезпечує слабкий зв'язок, не даючи об'єктам явно посилатися один на одного.

### Коли використовувати
- [x] Набір об'єктів взаємодіє складними способами
- [x] Повторно використати об'єкт складно, бо він посилається на багато інших
- [x] Поведінку, розподілену між класами, треба налаштовувати без створення підкласів

### Сигнатура TypeScript
```typescript
// Mediator interface
interface Mediator {
  notify(sender: object, event: string): void;
}

// Concrete mediator
class ConcreteMediator implements Mediator {
  private component1: Component1;
  private component2: Component2;

  constructor(c1: Component1, c2: Component2) {
    this.component1 = c1;
    this.component1.setMediator(this);
    this.component2 = c2;
    this.component2.setMediator(this);
  }

  notify(sender: object, event: string): void {
    if (event === 'A') {
      console.log('Mediator reacts to A and triggers:');
      this.component2.doC();
    }
    if (event === 'D') {
      console.log('Mediator reacts to D and triggers:');
      this.component1.doB();
    }
  }
}

// Base component
class BaseComponent {
  protected mediator: Mediator | null = null;

  setMediator(mediator: Mediator): void {
    this.mediator = mediator;
  }
}

// Concrete components
class Component1 extends BaseComponent {
  doA(): void {
    console.log('Component 1 does A');
    this.mediator?.notify(this, 'A');
  }

  doB(): void {
    console.log('Component 1 does B');
  }
}

class Component2 extends BaseComponent {
  doC(): void {
    console.log('Component 2 does C');
  }

  doD(): void {
    console.log('Component 2 does D');
    this.mediator?.notify(this, 'D');
  }
}

// Usage
const c1 = new Component1();
const c2 = new Component2();
const mediator = new ConcreteMediator(c1, c2);

c1.doA();
// Output:
// Component 1 does A
// Mediator reacts to A and triggers:
// Component 2 does C
```

### Нативний для стеку варіант: React context
```typescript
const ChatContext = createContext<ChatMediator>(null!);

// Mediator as context
function ChatRoom({ children }: Props) {
  const sendMessage = (from: string, to: string, msg: string) => {
    // Mediator logic
  };

  return (
    <ChatContext.Provider value={{ sendMessage }}>
      {children}
    </ChatContext.Provider>
  );
}
```

### Code smells, які він усуває
- **Заплутана мережа взаємодій**: централізується в посереднику
- **God object із багатьма обов'язками**: посередник відповідає лише за координацію

---

## Memento

### Визначення
Фіксує та виносить назовні внутрішній стан об'єкта, не порушуючи інкапсуляції, щоб згодом об'єкт можна було повернути в цей стан.

### Коли використовувати
- [x] Потрібно зберігати й відновлювати знімки об'єкта (undo/redo)
- [x] Прямий інтерфейс до стану розкрив би деталі реалізації
- [x] Потрібно зберегти межі інкапсуляції

### Сигнатура TypeScript
```typescript
// Memento
class Memento {
  constructor(private state: string, private date: Date) {}

  getState(): string {
    return this.state;
  }

  getDate(): Date {
    return this.date;
  }
}

// Originator
class Editor {
  private content: string = '';

  type(text: string): void {
    this.content += text;
  }

  getContent(): string {
    return this.content;
  }

  save(): Memento {
    return new Memento(this.content, new Date());
  }

  restore(memento: Memento): void {
    this.content = memento.getState();
  }
}

// Caretaker
class History {
  private mementos: Memento[] = [];

  push(memento: Memento): void {
    this.mementos.push(memento);
  }

  pop(): Memento | undefined {
    return this.mementos.pop();
  }
}

// Usage
const editor = new Editor();
const history = new History();

editor.type('Hello ');
history.push(editor.save());

editor.type('World');
history.push(editor.save());

editor.type('!!!');
console.log(editor.getContent()); // Hello World!!!

editor.restore(history.pop()!);
console.log(editor.getContent()); // Hello World
```

### Code smells, які він усуває
- **Розкриття внутрішнього стану заради undo**: Memento інкапсулює стан
- **Складна логіка undo**: History керує знімками

---

## Observer

### Визначення
Визначає залежність «один до багатьох» між об'єктами: коли один об'єкт змінює стан, усі залежні від нього автоматично отримують сповіщення.

### Коли використовувати
- [x] Зміна одного об'єкта вимагає змін в інших (їхня кількість невідома)
- [x] Об'єкт має сповіщати інших, не знаючи, хто вони
- [x] Подієво-орієнтована архітектура
- [x] Реактивне програмування

### Сигнатура TypeScript
```typescript
// Observer interface
interface Observer {
  update(subject: Subject): void;
}

// Subject
interface Subject {
  attach(observer: Observer): void;
  detach(observer: Observer): void;
  notify(): void;
}

// Concrete subject
class ConcreteSubject implements Subject {
  private observers: Observer[] = [];
  private state: number = 0;

  attach(observer: Observer): void {
    if (!this.observers.includes(observer)) {
      this.observers.push(observer);
    }
  }

  detach(observer: Observer): void {
    const index = this.observers.indexOf(observer);
    if (index !== -1) {
      this.observers.splice(index, 1);
    }
  }

  notify(): void {
    for (const observer of this.observers) {
      observer.update(this);
    }
  }

  setState(state: number): void {
    this.state = state;
    this.notify();
  }

  getState(): number {
    return this.state;
  }
}

// Concrete observers
class ConcreteObserverA implements Observer {
  update(subject: ConcreteSubject): void {
    console.log(`ObserverA: State is now ${subject.getState()}`);
  }
}

class ConcreteObserverB implements Observer {
  update(subject: ConcreteSubject): void {
    console.log(`ObserverB: State is now ${subject.getState()}`);
  }
}

// Usage
const subject = new ConcreteSubject();
const observerA = new ConcreteObserverA();
const observerB = new ConcreteObserverB();

subject.attach(observerA);
subject.attach(observerB);

subject.setState(5);
// Output:
// ObserverA: State is now 5
// ObserverB: State is now 5
```

### Нативні альтернативи стеку

**React**:
```typescript
const [value, setValue] = useState(0);
useEffect(() => {
  // Auto-notified on value change
}, [value]);
```

**RxJS**:
```typescript
const subject = new BehaviorSubject(0);
subject.subscribe(value => console.log(value));
subject.next(5); // Notifies subscribers
```

**Angular**:
```typescript
private data$ = new BehaviorSubject<Data>(initial);
getData() { return this.data$.asObservable(); }
```

### Code smells, які він усуває
- **Розкидана логіка сповіщень**: централізується в суб'єкті
- **Тісний зв'язок**: спостерігачі не знають один про одного

### Поширені помилки
- **Витоки пам'яті**: забули відписатися або від'єднатися
- **Лавини сповіщень**: забагато оновлень запускають каскади
- **Залежність від порядку**: спостерігачі мають бути незалежними

---

## State

### Визначення
Дозволяє об'єкту змінювати поведінку, коли змінюється його внутрішній стан, так що здається, ніби змінився його клас.

### Коли використовувати
- [x] Поведінка об'єкта залежить від його стану
- [x] Операції містять великі умовні конструкції, що залежать від стану
- [x] Переходи між станами чітко визначені

### Сигнатура TypeScript
```typescript
// State interface
interface State {
  handle(context: Context): void;
}

// Context
class Context {
  private state: State;

  constructor(initialState: State) {
    this.state = initialState;
  }

  setState(state: State): void {
    console.log(`Context: Transitioning to ${state.constructor.name}`);
    this.state = state;
  }

  request(): void {
    this.state.handle(this);
  }
}

// Concrete states
class ConcreteStateA implements State {
  handle(context: Context): void {
    console.log('StateA handles request');
    context.setState(new ConcreteStateB());
  }
}

class ConcreteStateB implements State {
  handle(context: Context): void {
    console.log('StateB handles request');
    context.setState(new ConcreteStateA());
  }
}

// Usage
const context = new Context(new ConcreteStateA());
context.request(); // StateA handles request, transitions to StateB
context.request(); // StateB handles request, transitions to StateA
```

### Приклад із практики: стани документа
```typescript
interface DocumentState {
  publish(doc: Document): void;
  review(doc: Document): void;
}

class Draft implements DocumentState {
  publish(doc: Document): void {
    console.log('Cannot publish draft directly');
  }
  review(doc: Document): void {
    console.log('Sending for review');
    doc.setState(new InReview());
  }
}

class InReview implements DocumentState {
  publish(doc: Document): void {
    console.log('Publishing document');
    doc.setState(new Published());
  }
  review(doc: Document): void {
    console.log('Already in review');
  }
}

class Published implements DocumentState {
  publish(doc: Document): void {
    console.log('Already published');
  }
  review(doc: Document): void {
    console.log('Cannot review published document');
  }
}

class Document {
  private state: DocumentState = new Draft();

  setState(state: DocumentState): void {
    this.state = state;
  }

  publish(): void {
    this.state.publish(this);
  }

  review(): void {
    this.state.review(this);
  }
}
```

### Нативний для стеку варіант: React useReducer
```typescript
const reducer = (state: State, action: Action) => {
  switch (action.type) {
    case 'DRAFT': return { status: 'draft' };
    case 'REVIEW': return { status: 'review' };
    case 'PUBLISHED': return { status: 'published' };
  }
};

const [state, dispatch] = useReducer(reducer, { status: 'draft' });
```

### Code smells, які він усуває
- **Складні умови за станом**: кожен стан є окремим класом
- **Розкидана поведінка, що залежить від стану**: локалізується в класах станів

---

## Strategy

### Визначення
Визначає сімейство алгоритмів, інкапсулює кожен із них і робить їх взаємозамінними, тож алгоритм можна змінювати незалежно від клієнтів.

### Коли використовувати
- [x] Багато споріднених класів відрізняються лише поведінкою
- [x] Потрібні різні варіанти алгоритму
- [x] Алгоритм використовує дані, про які клієнти не повинні знати
- [x] У класі кілька умовних конструкцій для вибору поведінки

### Сигнатура TypeScript
```typescript
// Strategy interface
interface Strategy {
  execute(a: number, b: number): number;
}

// Concrete strategies
class AddStrategy implements Strategy {
  execute(a: number, b: number): number {
    return a + b;
  }
}

class MultiplyStrategy implements Strategy {
  execute(a: number, b: number): number {
    return a * b;
  }
}

// Context
class Calculator {
  constructor(private strategy: Strategy) {}

  setStrategy(strategy: Strategy): void {
    this.strategy = strategy;
  }

  calculate(a: number, b: number): number {
    return this.strategy.execute(a, b);
  }
}

// Usage
const calculator = new Calculator(new AddStrategy());
console.log(calculator.calculate(5, 3)); // 8

calculator.setStrategy(new MultiplyStrategy());
console.log(calculator.calculate(5, 3)); // 15
```

### Нативний для стеку варіант: React hooks
```typescript
// Strategies as hooks
const useCreditPayment = () => ({ process: async (amount) => { /* ... */ } });
const usePaypalPayment = () => ({ process: async (amount) => { /* ... */ } });

const usePaymentStrategy = (type: PaymentType) => {
  const strategies = {
    credit: useCreditPayment(),
    paypal: usePaypalPayment(),
  };
  return strategies[type];
};

// Usage in component
const PaymentForm = ({ type }: Props) => {
  const strategy = usePaymentStrategy(type);
  const handlePay = () => strategy.process(amount);
};
```

### Code smells, які він усуває
- **Switch за типом**: `switch (type) { case 'A': ... case 'B': ... }`
  → Замініть вибором стратегії
- **Жорстко зашиті алгоритми**: стратегії взаємозамінні

### Поширені помилки
- **Вибух стратегій**: забагато дрібних стратегій
- **Обізнаність клієнта**: клієнт не повинен знати деталей стратегії

---

## Template method

### Визначення
Визначає скелет алгоритму в методі, перекладаючи деякі кроки на підкласи, які можуть перевизначати окремі кроки, не змінюючи структури.

### Коли використовувати
- [x] Реалізувати незмінні частини алгоритму один раз, а змінні залишити підкласам
- [x] Спільну поведінку підкласів потрібно виокремити й локалізувати
- [x] Контролювати розширення в підкласах (hook-операції)

### Сигнатура TypeScript
```typescript
abstract class AbstractClass {
  // Template method
  templateMethod(): void {
    this.baseOperation1();
    this.requiredOperation1();
    this.baseOperation2();
    this.hook();
    this.requiredOperation2();
  }

  // Implemented operations
  baseOperation1(): void {
    console.log('AbstractClass: base operation 1');
  }

  baseOperation2(): void {
    console.log('AbstractClass: base operation 2');
  }

  // Must be implemented by subclasses
  abstract requiredOperation1(): void;
  abstract requiredOperation2(): void;

  // Hook (optional override)
  hook(): void {
    // Default empty implementation
  }
}

class ConcreteClassA extends AbstractClass {
  requiredOperation1(): void {
    console.log('ConcreteClassA: operation 1');
  }

  requiredOperation2(): void {
    console.log('ConcreteClassA: operation 2');
  }

  hook(): void {
    console.log('ConcreteClassA: hook override');
  }
}

class ConcreteClassB extends AbstractClass {
  requiredOperation1(): void {
    console.log('ConcreteClassB: operation 1');
  }

  requiredOperation2(): void {
    console.log('ConcreteClassB: operation 2');
  }
}

// Usage
const classA = new ConcreteClassA();
classA.templateMethod();
```

### Code smells, які він усуває
- **Дублювання структури алгоритму**: шаблон визначає спільні кроки
- **Непослідовний порядок кроків**: шаблон примусово задає порядок

---

## Visitor

### Визначення
Подає операцію, яку треба виконати над елементами структури об'єктів, і дає змогу визначати нові операції, не змінюючи класів цих елементів.

### Коли використовувати
- [x] Структура об'єктів містить багато класів із різними інтерфейсами
- [x] Над об'єктами потрібно виконувати багато різних операцій
- [x] Структура об'єктів змінюється рідко, а операції над нею часто

### Сигнатура TypeScript
```typescript
// Element interface
interface Element {
  accept(visitor: Visitor): void;
}

// Concrete elements
class ConcreteElementA implements Element {
  accept(visitor: Visitor): void {
    visitor.visitConcreteElementA(this);
  }

  operationA(): string {
    return 'A';
  }
}

class ConcreteElementB implements Element {
  accept(visitor: Visitor): void {
    visitor.visitConcreteElementB(this);
  }

  operationB(): string {
    return 'B';
  }
}

// Visitor interface
interface Visitor {
  visitConcreteElementA(element: ConcreteElementA): void;
  visitConcreteElementB(element: ConcreteElementB): void;
}

// Concrete visitor
class ConcreteVisitor implements Visitor {
  visitConcreteElementA(element: ConcreteElementA): void {
    console.log(`Visiting A: ${element.operationA()}`);
  }

  visitConcreteElementB(element: ConcreteElementB): void {
    console.log(`Visiting B: ${element.operationB()}`);
  }
}

// Usage
const elements: Element[] = [
  new ConcreteElementA(),
  new ConcreteElementB(),
];

const visitor = new ConcreteVisitor();
for (const element of elements) {
  element.accept(visitor);
}
```

### Code smells, які він усуває
- **Додавання нових операцій вимагає змінювати елементи**: Visitor виносить операції назовні
- **Операції розкидані між класами**: Visitor групує споріднені операції

### Поширені помилки
- **Додавання нових типів елементів**: вимагає змінювати всі visitor (жорсткість)
- **Порушення інкапсуляції**: Visitor може потребувати доступу до внутрішніх деталей

---

## Interpreter

### Визначення
Визначає представлення граматики разом з інтерпретатором, що використовує це представлення для інтерпретації речень мови.

### Коли використовувати
- [x] Граматика проста (для складних граматик використовуйте генератори парсерів)
- [x] Ефективність некритична
- [x] Створюється проста предметно-орієнтована мова (DSL)

### Сигнатура TypeScript
```typescript
// Context
class Context {
  constructor(public input: string) {}
}

// Abstract expression
interface Expression {
  interpret(context: Context): number;
}

// Terminal expression
class NumberExpression implements Expression {
  constructor(private value: number) {}

  interpret(context: Context): number {
    return this.value;
  }
}

// Non-terminal expressions
class AddExpression implements Expression {
  constructor(private left: Expression, private right: Expression) {}

  interpret(context: Context): number {
    return this.left.interpret(context) + this.right.interpret(context);
  }
}

class MultiplyExpression implements Expression {
  constructor(private left: Expression, private right: Expression) {}

  interpret(context: Context): number {
    return this.left.interpret(context) * this.right.interpret(context);
  }
}

// Usage: (5 + 3) * 2
const context = new Context('(5 + 3) * 2');
const expression = new MultiplyExpression(
  new AddExpression(
    new NumberExpression(5),
    new NumberExpression(3)
  ),
  new NumberExpression(2)
);

console.log(expression.interpret(context)); // 16
```

### Code smells, які він усуває
- **Складна логіка парсингу**: правила граматики стають явними класами
- **Жорстко зашита інтерпретація мови**: граматика розширювана

---

## Зведена таблиця

| Патерн | Складність | Частота використання | Головна перевага |
|---------|------------|---------------|--------------|
| Chain of Responsibility | Середня | Середня | Розділення відправника й одержувача |
| Command | Середня | Середня | Параметризація, черга, скасування операцій |
| Iterator | Низька | Висока | Послідовний доступ без розкриття структури |
| Mediator | Середня | Середня | Зменшення зв'язності між об'єктами |
| Memento | Середня | Низька | Збереження й відновлення стану |
| Observer | Низька | Дуже висока | Сповіщення «один до багатьох» |
| State | Середня | Середня | Поведінка, що залежить від стану |
| Strategy | Низька | Висока | Взаємозамінні алгоритми |
| Template Method | Середня | Середня | Скелет алгоритму з варіаціями |
| Visitor | Висока | Низька | Операції над структурою об'єктів |
| Interpreter | Висока | Дуже низька | Інтерпретація простих DSL |

## Найкращі практики

1. **Observer**: завжди відписуйтеся, щоб уникнути витоків пам'яті
2. **Strategy чи State**: Strategy змінює поведінку ззовні; State змінює її зсередини
3. **Використовуйте патерни фреймворків**: React hooks, RxJS і Redux уже надають ці патерни
4. **Command для undo**: зберігайте історію об'єктів-команд
5. **Chain of Responsibility**: тримайте обробники простими й стежте, щоб запит було оброблено

## Джерела

- *Design Patterns: Elements of Reusable Object-Oriented Software* (Gang of Four)
- [Refactoring Guru: Behavioral Patterns](https://refactoring.guru/design-patterns/behavioral-patterns)
- [RxJS Documentation](https://rxjs.dev/)
