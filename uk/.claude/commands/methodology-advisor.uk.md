---
name: methodology-advisor
description: "Аналізує вашу кодову базу та ставить 3 цільові запитання, щоб порекомендувати відповідний стек методологій розробки з підтримкою AI"
---

# Консультант із методологій

Проаналізуй цей проєкт і порекомендуй найкращий стек методологій розробки з підтримкою AI. Спершу прочитай із кодової бази все, що можна, а запитуй лише про те, чого не можеш вивести.

**Час**: 2-4 хвилини | **Результат**: Один рекомендований стек + контекстний швидкий старт

---

## Фаза 1 — Тихий аналіз кодової бази

Виконуй ці читання мовчки. Поки не виводь результатів — лише будуй внутрішню картину.

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

### 1.6 Сигнали AI та LLM

```bash
# LLM API usage in code
grep -rn --include="*.ts" --include="*.py" --include="*.js" \
  -l "anthropic\|openai\|groq\|mistral\|langchain\|llm\|ChatCompletion\|claude" \
  2>/dev/null | grep -v node_modules | grep -v ".git" | head -5
# Eval framework hints
find . -name "evals*" -o -name "*eval*" -type d 2>/dev/null | grep -v node_modules | head -5
```

---

## Фаза 2 — Оцінити 8 стеків

На основі знайденого оціни кожен стек від 0 до 10 за сигналами відповідності:

| Стек | Ключові сигнали, що підвищують оцінку |
|-------|----------------------------------|
| **solo-mvp** | 1 контриб'ютор, мало файлів, ще немає CI, greenfield |
| **team-greenfield** | 2-10 контриб'юторів, новий проєкт, без застарілих файлів |
| **microservices** | `packages/`, `services/`, файли OpenAPI, `.proto` |
| **brownfield-saas** | Велика кількість комітів, багато файлів, мало тестових файлів |
| **enterprise-gov** | 10+ контриб'юторів, CI, файли ADR, `AGENTS.md` |
| **llm-native** | Імпорти LLM, директорії eval, ознаки AI-продукту |
| **power-solo** | 1 контриб'ютор, висока частота комітів, ітеративні коміти |
| **plan-moderate** | Змішані сигнали, наявний CLAUDE.md, помірний розмір |

---

## Фаза 3 — Запитуй лише те, чого не можеш вивести

Після тихого аналізу представ користувачеві попередню картину у 2-3 рядках, потім став рівно 3 запитання. Не більше.

Формат:

```
З вашої кодової бази я бачу: [2-3 конкретні спостереження].
Перш ніж рекомендувати, 3 короткі запитання:

1. [Запитання про больову точку — обери найрелевантніше з наведених нижче]
2. [Частота деплоїв — якщо не виводиться із сигналів CI/CD]
3. [Готовність до налаштування — скільки церемоній ви готові витратити?]
```

**Банк запитань — обери 3 найрелевантніші з огляду на знайдене:**

- Біль: "Що найбільше вас гальмує зараз — регресії, нечіткі вимоги, context rot між сесіями чи відсутність простежуваності?"
- Біль: "Коли Claude генерує великий шматок коду, що вас турбує найбільше — якість, відхилення від специфікації чи втрата розуміння того, що збудовано?"
- Деплой: "Як часто ви викочуєте в продакшен — кілька разів на день, щотижня чи за довшими релізними циклами?"
- Деплой: "Це продукт із реальними користувачами вже сьогодні, прототип чи внутрішній інструмент?"
- Керування: "Скільки початкового налаштування ви готові витратити — жодного (просто почати), 30 хвилин чи півдня?"
- Керування: "Чи потрібно комусь поза вашою командою розробників (PM, QA, комплаєнс) валідувати те, що створюється?"
- AI-продукт: "Чи показує ваш продукт згенеровані AI результати безпосередньо кінцевим користувачам?"
- Масштаб: "Чи потрібно кільком сервісам або командам погоджувати контракти API до реалізації?"

---

## Фаза 4 — Рекомендація

Виведи рекомендацію в такій структурі:

---

### Ваш стек: [Назва стеку] [іконка]

**Чому це підходить вашому проєкту:**
- [Знахідка з Фази 1] → [пояснює вибір цього стеку]
- [Знахідка з Фази 1] → [пояснює вибір цього стеку]
- [Відповідь на запитання N] → [пояснює вибір цього стеку]

**Включені методології:** `[Метод A]` + `[Метод B]` (+ `[Метод C]`, якщо застосовно)

**Як це виглядає на практиці:**
[2-3 речення, що описують конкретний робочий процес для ЦЬОГО проєкту з використанням реальних знайдених назв файлів чи шляхів.]

**Швидкий старт для вашого проєкту:**
1. [Конкретний перший крок з використанням реального контексту проєкту]
2. [Другий крок]
3. [Третій крок]

**Перш ніж почати, зверніть увагу:**
- [Один чесний компроміс чи обмеження цього стеку]
- [Одна річ, на яку варто звернути увагу з огляду на знайдене]

**Заглибитися:** https://cc.bruniaux.com/methodologies/ — інтерактивна вікторина та повне порівняння стеків
**Повний посібник із методологій:** https://cc.bruniaux.com/guide/methodologies/

---

## Довідник стеків (внутрішній)

Використовуй це, щоб зіставити свої оцінки з формулюваннями швидкого старту:

**solo-mvp** (SDD + TDD): Напиши специфікацію фічі в CLAUDE.md → `"Write failing tests for this spec, then implement until green."`

**team-greenfield** (Spec Kit + TDD + BDD): `/speckit.constitution` → сценарії Given/When/Then з PM → TDD для кожного сценарію.

**microservices** (CDD + Specmatic + TDD): Спершу напиши специфікацію OpenAPI → Specmatic для контрактних тестів → реалізація через TDD.

**brownfield-saas** (OpenSpec + BDD + JiTTesting): OpenSpec фіксує поточний стан → BDD для зміненої поведінки → перед злиттям: `"Generate tests that catch regressions in this diff."`

**enterprise-gov** (BMAD + Spec Kit + Specmatic): `constitution.md` → визначення ролей агентів → вимоги Spec Kit → забезпечення контрактів через Specmatic.

**llm-native** (Eval-Driven + Multi-Agent): Визнач критерії eval (точність, безпека, формат) → збудуй eval harness → ітеруй, доки eval не пройдуть.

**power-solo** (TDD + Ralph Loop + Iterative): Тісний тестовий цикл → свіжий контекст на кожне завдання через git stash + файли прогресу → `"Keep iterating until all tests pass and lint is clean."`

**plan-moderate** (Plan-First + SDD + Context Engineering): Кожне складне завдання починається в Plan Mode (Shift+Tab) → валідація → напиши специфікацію в CLAUDE.md → виконання з прогресивним завантаженням контексту.
