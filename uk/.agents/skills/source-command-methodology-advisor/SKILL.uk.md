---
name: "source-command-methodology-advisor"
description: "Аналізує вашу кодову базу та ставить 3 цільові запитання, щоб рекомендувати відповідний стек методологій розробки з підтримкою ШІ"
---

# source-command-methodology-advisor

Використовуй цей skill, коли користувач просить виконати мігровану вихідну команду `methodology-advisor`.

## Command Template

# Methodology Advisor

Проаналізуй цей проєкт і порекомендуй найкращий стек методологій розробки з підтримкою ШІ. Спершу прочитай із кодової бази все, що можеш, а потім запитай лише те, що не можна вивести.

**Час**: 2-4 хвилини | **Результат**: один рекомендований стек + контекстний швидкий старт

---

## Фаза 1 — Тихий аналіз кодової бази

Виконай ці читання мовчки. Поки не виводь результати: лише будуй внутрішню картину.

### 1.1 Ідентичність проєкту

```bash
# Config files
cat AGENTS.md 2>/dev/null || cat AGENTS.md 2>/dev/null
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

### 1.4 Ознаки специфікацій і документації

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

### 1.6 Ознаки ШІ та LLM

```bash
# LLM API usage in code
grep -rn --include="*.ts" --include="*.py" --include="*.js" \
  -l "anthropic\|openai\|groq\|mistral\|langchain\|llm\|ChatCompletion\|Codex" \
  2>/dev/null | grep -v node_modules | grep -v ".git" | head -5
# Eval framework hints
find . -name "evals*" -o -name "*eval*" -type d 2>/dev/null | grep -v node_modules | head -5
```

---

## Фаза 2 — Оцінка 8 стеків

На основі знайденого оціни кожен стек від 0 до 10 за ознаками відповідності:

| Стек | Ключові ознаки, що підвищують оцінку |
|------|---------------------------------------|
| **solo-mvp** | 1 контриб'ютор, мало файлів, CI ще немає, greenfield |
| **team-greenfield** | 2-10 контриб'юторів, новий проєкт, немає legacy-файлів |
| **microservices** | `packages/`, `services/`, файли OpenAPI, `.proto` |
| **brownfield-saas** | Багато комітів, багато файлів, мало тестових файлів |
| **enterprise-gov** | 10+ контриб'юторів, CI, файли ADR, `AGENTS.md` |
| **llm-native** | Імпорти LLM, теки eval, ознаки AI-продукту |
| **power-solo** | 1 контриб'ютор, висока частота комітів, ітеративні коміти |
| **plan-moderate** | Змішані сигнали, є AGENTS.md, помірний розмір |

---

## Фаза 3 — Питай лише те, що не можна вивести

Після тихого аналізу представ користувачеві попередню картину у 2-3 рядках, потім став рівно 3 запитання. Не більше.

Формат:

```
From your codebase I can see: [2-3 concrete observations].
Before recommending, 3 quick questions:

1. [Pain point question — pick the most relevant from below]
2. [Deploy frequency — if not inferable from CI/CD signals]
3. [Setup appetite — how much ceremony are you willing to invest?]
```

**Банк запитань: обери 3 найрелевантніші з огляду на знайдене:**

- Pain: "What slows you down most right now — regressions, unclear requirements, context rot between sessions, or no traceability?"
- Pain: "When Codex generates a large chunk of code, what is your biggest worry — quality, drift from spec, or losing track of what was built?"
- Deploy: "How often do you ship to production — multiple times a day, weekly, or on longer release cycles?"
- Deploy: "Is this a product with real users today, a prototype, or an internal tool?"
- Governance: "How much initial setup are you willing to invest — none (just start), 30 minutes, or half a day?"
- Governance: "Does anyone outside your dev team (PM, QA, compliance) need to validate what gets built?"
- AI product: "Does your product expose AI-generated outputs directly to end users?"
- Scale: "Do multiple services or teams need to agree on API contracts before implementing?"

---

## Фаза 4 — Рекомендація

Виведи рекомендацію в такій структурі:

---

### Your Stack: [Stack Name] [icon]

**Why this fits your project:**
- [Finding from Phase 1] → [explains this stack choice]
- [Finding from Phase 1] → [explains this stack choice]
- [Answer to question N] → [explains this stack choice]

**Methodologies included:** `[Method A]` + `[Method B]` (+ `[Method C]` if applicable)

**What this looks like in practice:**
[2-3 sentences describing the concrete workflow for THIS project, using actual file names or paths found.]

**Quick start for your project:**
1. [Concrete first step using actual project context]
2. [Second step]
3. [Third step]

**Before you start, note:**
- [One honest trade-off or limitation of this stack]
- [One thing to watch out for given what you found]

**Go deeper:** https://cc.bruniaux.com/methodologies/ — interactive quiz and full stack comparison
**Full methodology guide:** https://cc.bruniaux.com/guide/methodologies/

---

## Довідник стеків (внутрішній)

Використовуй це, щоб зіставити свою оцінку з формулюваннями швидкого старту:

**solo-mvp** (SDD + TDD): Write feature spec in AGENTS.md → `"Write failing tests for this spec, then implement until green."`

**team-greenfield** (Spec Kit + TDD + BDD): `/speckit.constitution` → Given/When/Then scenarios with PM → TDD each scenario.

**microservices** (CDD + Specmatic + TDD): Write OpenAPI spec first → Specmatic for contract tests → TDD implementation.

**brownfield-saas** (OpenSpec + BDD + JiTTesting): OpenSpec captures current state → BDD for changed behavior → pre-merge: `"Generate tests that catch regressions in this diff."`

**enterprise-gov** (BMAD + Spec Kit + Specmatic): `constitution.md` → agent role definitions → Spec Kit requirements → Specmatic contract enforcement.

**llm-native** (Eval-Driven + Multi-Agent): Define eval criteria (accuracy, safety, format) → build eval harness → iterate until evals pass.

**power-solo** (TDD + Ralph Loop + Iterative): Tight test loop → fresh context per task via git stash + progress files → `"Keep iterating until all tests pass and lint is clean."`

**plan-moderate** (Plan-First + SDD + Context Engineering): Every complex task starts in Plan Mode (Shift+Tab) → validate → write spec in AGENTS.md → execute with progressive context loading.
