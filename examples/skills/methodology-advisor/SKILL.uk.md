---
name: methodology-advisor
description: Аналізує вашу кодову базу й ставить 3 цілеспрямовані запитання, щоб порекомендувати відповідний стек методологій розробки за допомогою ШІ
effort: medium
allowed-tools: Read Grep Glob
---

# Методологічний радник

Проаналізуйте цей проєкт і порекомендуйте найкращий стек методологій розробки за допомогою ШІ. Спершу прочитайте все, що можна, з кодової бази, а потім запитайте лише те, чого не можна вивести.

**Час**: 2-4 хвилини | **Результат**: один рекомендований стек + контекстний швидкий старт

---

## Фаза 1: Тихий аналіз кодової бази

Виконайте ці читання мовчки. Поки що не виводьте результатів, лише формуйте внутрішню картину.

### 1.1 Ідентичність проєкту

```bash
# Config files
cat CLAUDE.md 2>/dev/null || cat claude.md 2>/dev/null
cat package.json 2>/dev/null | grep -E '"name"|"description"|"scripts"' | head -10
cat Cargo.toml 2>/dev/null | grep -E '^name|^description' | head -5
cat pyproject.toml 2>/dev/null | grep -E '^name|^description' | head -5
cat go.mod 2>/dev/null | head -3
```

### 1.2 Розмір команди

```bash
# Unique contributors in last 90 days
git log --since="90 days ago" --format="%ae" 2>/dev/null | sort -u | wc -l
# Total commits
git log --oneline 2>/dev/null | wc -l
```

### 1.3 Зрілість тестування

```bash
# Test files exist?
find . -name "*.test.*" -o -name "*.spec.*" -o -name "*_test.*" -o -name "test_*.py" \
  2>/dev/null | grep -v node_modules | grep -v ".git" | wc -l
# Test framework hints
grep -rn --include="*.json" --include="*.toml" --include="*.yaml" \
  -l "jest\|vitest\|pytest\|rspec\|mocha\|cypress\|playwright" \
  2>/dev/null | grep -v node_modules | head -5
# CI config
ls .github/workflows/*.yml 2>/dev/null | wc -l
ls .gitlab-ci.yml .circleci/config.yml 2>/dev/null | wc -l
```

### 1.4 Сигнали специфікацій і документації

```bash
# Spec files
find . -name "*.spec.md" -o -name "SPEC*.md" -o -name "spec.md" -o -name "DESIGN*.md" \
  -o -name "ADR*.md" -o -name "RFC*.md" \
  2>/dev/null | grep -v node_modules | grep -v ".git" | head -10
# OpenAPI / contract files
find . -name "openapi*.yaml" -o -name "openapi*.json" -o -name "swagger*.yaml" \
  -o -name "*.proto" \
  2>/dev/null | grep -v node_modules | head -5
# BDD feature files
find . -name "*.feature" 2>/dev/null | grep -v node_modules | wc -l
```

### 1.5 Розмір і структура кодової бази

```bash
# File count (rough)
find . -type f \( -name "*.ts" -o -name "*.tsx" -o -name "*.js" -o -name "*.py" \
  -o -name "*.rs" -o -name "*.go" -o -name "*.java" -o -name "*.rb" \) \
  2>/dev/null | grep -v node_modules | grep -v ".git" | wc -l
# Services / packages (monorepo signal)
ls packages/ apps/ services/ 2>/dev/null | head -10
```

### 1.6 Сигнали ШІ та LLM

```bash
# LLM API usage in code
grep -rn --include="*.ts" --include="*.py" --include="*.js" \
  -l "anthropic\|openai\|groq\|mistral\|langchain\|llm\|ChatCompletion\|claude" \
  2>/dev/null | grep -v node_modules | grep -v ".git" | head -5
# Eval framework hints
find . -name "evals*" -o -name "*eval*" -type d 2>/dev/null | grep -v node_modules | head -5
```

---

## Фаза 2: Оцінити 8 стеків

На основі знайденого оцініть кожен стек від 0 до 10 за сигналами відповідності:

| Стек | Ключові сигнали, що підвищують оцінку |
|-------|----------------------------------|
| **solo-mvp** | 1 контриб'ютор, мало файлів, ще немає CI, greenfield |
| **team-greenfield** | 2-10 контриб'юторів, новий проєкт, немає legacy-файлів |
| **microservices** | `packages/`, `services/`, файли OpenAPI, `.proto` |
| **brownfield-saas** | Велика кількість комітів, велика кількість файлів, мало тестових файлів |
| **enterprise-gov** | 10+ контриб'юторів, CI, файли ADR, `AGENTS.md` |
| **llm-native** | Імпорти LLM, директорії eval, сигнали ШІ-продукту |
| **power-solo** | 1 контриб'ютор, висока частота комітів, ітеративні коміти |
| **plan-moderate** | Змішані сигнали, наявний CLAUDE.md, помірний розмір |

---

## Фаза 3: Питайте лише те, чого не можна вивести

Після тихого аналізу представте користувачеві попередню картину в 2-3 рядках, а потім поставте рівно 3 запитання. Не більше.

Формат:

```
From your codebase I can see: [2-3 concrete observations].
Before recommending, 3 quick questions:

1. [Pain point question, pick the most relevant from below]
2. [Deploy frequency, if not inferable from CI/CD signals]
3. [Setup appetite: how much ceremony are you willing to invest?]
```

**Банк запитань: оберіть 3 найрелевантніші з огляду на знайдене:**

- Біль: "What slows you down most right now: regressions, unclear requirements, context rot between sessions, or no traceability?"
- Біль: "When Claude generates a large chunk of code, what is your biggest worry: quality, drift from spec, or losing track of what was built?"
- Деплой: "How often do you ship to production: multiple times a day, weekly, or on longer release cycles?"
- Деплой: "Is this a product with real users today, a prototype, or an internal tool?"
- Управління: "How much initial setup are you willing to invest: none (just start), 30 minutes, or half a day?"
- Управління: "Does anyone outside your dev team (PM, QA, compliance) need to validate what gets built?"
- ШІ-продукт: "Does your product expose AI-generated outputs directly to end users?"
- Масштаб: "Do multiple services or teams need to agree on API contracts before implementing?"

---

## Фаза 4: Рекомендація

Виведіть рекомендацію в такій структурі:

---

### Ваш стек: [Назва стеку] [іконка]

**Чому це підходить вашому проєкту:**
- [Знахідка з Фази 1] -> [пояснює вибір цього стеку]
- [Знахідка з Фази 1] -> [пояснює вибір цього стеку]
- [Відповідь на запитання N] -> [пояснює вибір цього стеку]

**Включені методології:** `[Метод A]` + `[Метод B]` (+ `[Метод C]`, якщо застосовно)

**Як це виглядає на практиці:**
[2-3 речення з описом конкретного воркфлоу для ЦЬОГО проєкту із застосуванням справжніх імен файлів чи шляхів, що знайдено.]

**Швидкий старт для вашого проєкту:**
1. [Конкретний перший крок із використанням справжнього контексту проєкту]
2. [Другий крок]
3. [Третій крок]

**Перед початком зверніть увагу:**
- [Один чесний компроміс чи обмеження цього стеку]
- [Одна річ, на яку слід звернути увагу з огляду на знайдене]

**Заглибитися:** https://cc.bruniaux.com/methodologies/ (інтерактивна вікторина та повне порівняння стеків)
**Повний посібник із методологій:** https://cc.bruniaux.com/guide/methodologies/

---

## Довідник стеків (внутрішній)

Використовуйте його, щоб зіставити оцінювання з мовою швидкого старту:

**solo-mvp** (SDD + TDD): напишіть специфікацію функції в CLAUDE.md -> `"Напиши тести, що падають, для цієї специфікації, а потім реалізуй, доки вони не пройдуть."`

**team-greenfield** (Spec Kit + TDD + BDD): `/speckit.constitution` -> сценарії Given/When/Then разом із PM -> TDD для кожного сценарію.

**microservices** (CDD + Specmatic + TDD): спершу напишіть специфікацію OpenAPI -> Specmatic для контрактних тестів -> реалізація за TDD.

**brownfield-saas** (OpenSpec + BDD + JiTTesting): OpenSpec фіксує поточний стан -> BDD для зміненої поведінки -> перед злиттям: `"Згенеруй тести, що ловлять регресії в цьому diff."`

**enterprise-gov** (BMAD + Spec Kit + Specmatic): `constitution.md` -> визначення ролей агентів -> вимоги Spec Kit -> примусове дотримання контрактів через Specmatic.

**llm-native** (Eval-Driven + Multi-Agent): визначте критерії eval (точність, безпека, формат) -> побудуйте eval harness -> ітеруйте, доки eval не пройдуть.

**power-solo** (TDD + Ralph Loop + Iterative): щільний цикл тестів -> свіжий контекст для кожного завдання через git stash + файли прогресу -> `"Продовжуй ітерації, доки всі тести не пройдуть, а lint не буде чистим."`

**plan-moderate** (Plan-First + SDD + Context Engineering): кожне складне завдання починається в Plan Mode (Shift+Tab) -> валідація -> напишіть специфікацію в CLAUDE.md -> виконання з поступовим завантаженням контексту.
