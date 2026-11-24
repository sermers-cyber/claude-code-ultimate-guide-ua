---
title: "Module 07: Advanced Patterns"
description: "Модуль 07 навчального шляху: оркестрація multi-agent workflows у Claude Code, відновлення після помилок і шаблони автоматизації рівня production для командних процесів. 2-3 години, рівень advanced."
---

# Module 07: Advanced Patterns

**Час**: 2-3 години | **Складність**: ⭐⭐⭐ Advanced

## Мета

Оркеструвати multi-agent workflows. Будувати складні процеси автоматизації, які координують роботу кількох спеціалізованих agents.

---

## Що ви дізнаєтеся

- Шаблони архітектури систем з кількома agents (multi-agent systems)
- Стратегії оркестрації (orchestration strategies)
- Обробка помилок (error handling) та відновлення
- Процеси автоматизації рівня production
- Командні workflows
- Практичні сценарії використання

---

## Multi-Agent Systems

**Multi-agent system** — це архітектура, у якій кілька спеціалізованих agents спільно працюють над досягненням однієї мети.

Перш ніж обирати командний шаблон, розділіть рівні: модель видає токени, runtime harness керує циклом «модель — інструменти» в межах сесії, harness репозиторію надає інструкції та верифікацію, а оркестратор координує сесії. Цю модель пояснює [Agent Harness Engineering](../core/agent-harness.uk.md); [Карта agent harness](../ecosystem/agent-harness-landscape.uk.md) порівнює рантайми, що керують циклом, і окремо тримає ширший каталог. Для фреймворків і площин керування використовуйте [Інструменти агентів: поза межами Claude Code](../ecosystem/agentic-tools.uk.md), для термінів — [глосарій](../core/glossary.uk.md), щоб оцінити результат — [Agent Evaluation](../roles/agent-evaluation.uk.md), щоб перевірити виконання — [Спостережуваність сесій](../ops/observability.uk.md), а перед запуском роботи без нагляду — [Зміцнення безпеки](../security/security-hardening.uk.md).

### Приклад: Workflow випуску коду (Code Release Workflow)

Замість того, щоб один Claude відповідав за все:

```
Ви: "Release version 3.5.0"
    ↓
    ├─→ [Version Agent] Оновлює файл VERSION
    │
    ├─→ [Changelog Agent] Створює нотатки до релізу (release notes)
    │
    ├─→ [Test Agent] Запускає повний набір тестів
    │
    ├─→ [Security Agent] Проводить security audit
    │
    ├─→ [Docs Agent] Оновлює документацію
    │
    └─→ [Release Agent] Створює теги, білдить, публікує

Результат: Повний, протестований, задокументований реліз
```

Кожен з agents виконує своє спеціалізоване завдання максимально швидко та якісно.

---

## Шаблони оркестрації (Orchestration Patterns)

### Шаблон 1: Послідовний (Sequential / Pipeline)

Agents запускаються один за одним. Результат роботи (output) agent N стає вхідними даними (input) для agent N+1.

```
Вхід (Input)
  ↓
[Agent 1: Parse Requirements] → Output: структуровані вимоги
  ↓
[Agent 2: Design Schema] → Output: database schema
  ↓
[Agent 3: Generate Code] → Output: каркас коду
  ↓
[Agent 4: Write Tests] → Output: набір тестів
  ↓
Кінцевий результат
```

**Коли використовувати**: Для workflows, де кожен наступний крок критично залежить від результатів попереднього.

**Приклад**:
```bash
/agent requirements-parser
Parse the feature request into specifications

# Пізніше, коли специфікації готові:
/agent database-designer
Design the schema based on these specs

# Після затвердження схеми:
/agent code-generator
Generate models based on the schema
```

### Шаблон 2: Паралельний (Parallel / Fork-Join)

Кілька agents працюють одночасно, після чого результати їхньої роботи об'єднуються.

```
         Вхід (Input)
            ↓
    ┌───────┼───────┐
    ↓       ↓       ↓
 [Unit    [Int.   [Sec.
  Tests]  Tests]  Audit]
    ↓       ↓       ↓
    └───────┼───────┘
            ↓
   Об'єднання результатів
            ↓
      Фінальний звіт
```

**Коли використовувати**: Для незалежних перевірок або паралельних завдань.

**Приклад**:
```
Запит: "Review my code changes"

Паралельні завдання:
- Code quality agent перевіряє код
- Security agent проводить сканування
- Test coverage agent перевіряє покриття
- Performance agent аналізує швидкодію

(Усі запускаються одночасно)

Результати об'єднуються в один спільний звіт
```

### Шаблон 3: Умовний (Conditional / If-Then)

Запит перенаправляється до різних agents на основі певних умов.

```
Вхід (Input): "Fix the bug"
  ↓
[Analyzer: Is it security?]
  ├─ YES → [Security Agent]
  ├─ PERFORMANCE → [Performance Agent]
  └─ LOGIC → [Logic Agent]
  ↓
Результат
```

**Приклад**:
```bash
/agent bug-classifier
Categorize this bug: security, performance, or logic

# Залежно від відповіді:
# Якщо security:
/agent security-patcher
Fix the security vulnerability

# Якщо performance:
/agent perf-optimizer
Optimize this code
```

---

## Побудова випускного процесу (Release Workflow)

### Сценарій

Ви хочете автоматизувати свій процес релізу. Наразі ви вручну:
1. Оновлюєте файл VERSION
2. Оновлюєте CHANGELOG
3. Запускаєте тести
4. Запускаєте сканування безпеки (security scan)
5. Створюєте git tag
6. Робите push до origin
7. Робите deploy на staging

### Рішення: Multi-Agent Workflow

**Крок 1: Створіть конфігурації для agents** (кожен спеціалізується на своєму завданні)

`.claude/agents/version-manager.md`:
```markdown
---
name: version-manager
description: Manages version files and tags
capabilities:
  - read_files
  - write_files
  - NO: push
---

# Version Manager

## Purpose
Update VERSION files and create git tags

## Tasks
- Bump version (patch, minor, major)
- Update VERSION file
- Update version in package.json, pyproject.toml, etc
- Create annotated git tags
```

`.claude/agents/changelog-generator.md`:
```markdown
---
name: changelog-generator
description: Generates release notes
---

# Changelog Generator

## Purpose
Create readable release notes from commits

## Output Format
- Version header
- Breaking changes (if any)
- New features
- Bug fixes
- Deprecations
```

`.claude/agents/test-validator.md`:
```markdown
---
name: test-validator
description: Runs full test suite
---

# Test Validator

## Purpose
Execute all tests and verify coverage

## Minimum Requirements
- All tests pass
- Coverage >80%
- No flaky tests
```

`.claude/agents/release-publisher.md`:
```markdown
---
name: release-publisher
description: Publishes and deploys
---

# Release Publisher

## Purpose
Tag and push to origin

## Steps
1. Create git tag
2. Push to origin
3. Trigger CI/CD pipeline
4. Monitor deployment
```

**Крок 2: Створіть команду для запуску workflow**

`.claude/commands/release-workflow.md`:
```markdown
# /release-workflow

Orchestrate a complete release process.

Usage:
```
/release-workflow patch|minor|major
```

## Process

1. Validate release readiness
2. Update version (version-manager agent)
3. Generate changelog (changelog-generator agent)
4. Run tests (test-validator agent)
5. Security scan (security-auditor agent)
6. Publish and deploy (release-publisher agent)

## Requirements
- All tests passing
- No outstanding security issues
- Changelog updated
```

**Крок 3: Запустіть workflow**

```bash
/release-workflow patch
```

Далі Claude послідовно:
1. Викликає version-manager → оновлює VERSION
2. Викликає changelog-generator → генерує release notes
3. Викликає test-validator → запускає та перевіряє тести
4. Викликає security-auditor → сканує на вразливості
5. Викликає release-publisher → створює tag та робить push
6. Ви переглядаєте та схвалюєте кожен крок

---

## Обробка помилок в системах з кількома agents (Error Handling)

### Шаблон: Граціозний спад (Graceful Degradation)

Якщо один з agents завершується з помилкою, інші продовжують роботу:

```
[Test Agent] ❌ FAILED: 3 test failures
  ↓
[Security Agent] ✅ PASSED: No vulnerabilities
  ↓
[Docs Agent] ✅ PASSED: Docs updated
  ↓
[Aggregate Results]
  ⚠️  Release blocked (tests failed)
  ✅ Security passed
  ✅ Docs ready
  [Instructions to fix tests first]
```

### Шаблон: Повторна спроба при помилці (Retry on Failure)

Для тимчасових збоїв (проблеми з мережею, таймаути):

```bash
#!/bin/bash
# Використовується в hook або skill

max_retries=3
retry=0

while [ $retry -lt $max_retries ]; do
  if /agent test-validator run-tests; then
    echo "✅ Tests passed"
    exit 0
  fi
  
  retry=$((retry + 1))
  if [ $retry -lt $max_retries ]; do
    echo "⚠️  Retry $retry/$max_retries"
    sleep 5
  fi
done

echo "❌ Tests failed after $max_retries attempts"
exit 1
```

### Шаблон: Відкат змін при помилці (Rollback on Error)

Якщо щось пішло не так, повернути систему до початкового стану:

```bash
#!/bin/bash
# Скрипт для відкату змін (rollback)

ORIGINAL_VERSION=$(git rev-parse HEAD:VERSION)
ORIGINAL_TAG=$(git describe --tags --abbrev=0)

cleanup_and_exit() {
  echo "Rolling back..."
  git reset --hard HEAD~1
  git tag -d "$NEW_TAG"
  echo "VERSION restored to: $ORIGINAL_VERSION"
  exit 1
}

# Виконуємо кроки релізу
if ! /agent version-manager bump-version patch; then
  cleanup_and_exit
fi

if ! /agent test-validator validate-all; then
  cleanup_and_exit
fi

# Якщо дійшли сюди, реліз успішний
exit 0
```

---

## Паттерни для Production (Production Patterns)

### Шаблон 1: Поетапне розгортання (Staged Rollout)

Послідовне розгортання по різних оточеннях (environments):

```
/release major
  ↓
[Dev] Deploy and test
  ✅ Verified
  ↓
[Staging] Deploy and test
  ✅ Verified
  ↓
[Prod] Deploy with monitoring
  ✅ Monitoring green
  ↓
Release Complete
```

### Шаблон 2: Шлюзи схвалення (Approval Gates)

Блокування подальшого прогресу до ручного підтвердження:

```bash
# В .claude/hooks/pre-prod-deploy.sh

echo "🚨 PRODUCTION DEPLOY"
echo "Changes: $CHANGES"
echo "Tests: PASSING"
echo "Security: PASSING"
echo ""
read -p "Type 'I approve' to deploy to production: " approval

if [ "$approval" != "I approve" ]; then
  echo "❌ Deploy cancelled"
  exit 1
fi

exit 0
```

### Шаблон 3: Моніторинг та відкат (Monitoring & Rollback)

Перевірка працездатності після завершення deployment:

```bash
#!/bin/bash
# Post-deploy hook

sleep 10  # Дати час сервісам запуститися

# Перевірка здоров'я системи (health checks)
if ! curl -f https://api.example.com/health; then
  echo "❌ Health check failed"
  echo "Rolling back..."
  git revert -n HEAD
  git commit -m "Rollback: deployment health check failed"
  exit 1
fi

echo "✅ Deployment successful and healthy"
exit 0
```

---

## Вправа: Побудова вашого першого Multi-Agent Workflow

### Сценарій

У вас є проєкт з аналізу даних (data science). Checklist для випуску моделі:
1. Оновити версію моделі
2. Запустити тести валідації (validation tests)
3. Згенерувати звіт про продуктивність (performance report)
4. Оновити документацію
5. Створити git tag для релізу

### Крок 1: Створіть конфігурації для Agents

Створіть у директорії `.claude/agents/` такі файли:
- `model-versioner.md` — Оновлює VERSION, метадані моделі
- `validator.md` — Запускає тести валідації
- `report-generator.md` — Створює метрики продуктивності
- `doc-updater.md` — Оновлює README, API-документацію
- `release-tagger.md` — Створює git tag

### Крок 2: Створіть команду оркестрації

`.claude/commands/ml-release.md`:
```markdown
# /ml-release

Release a new model version.

Usage:
```
/ml-release [major|minor|patch]
```

## Workflow
1. Version agent bumps version
2. Validator runs test suite
3. Report agent generates metrics
4. Doc agent updates documentation
5. Tagger creates release tag
```

### Крок 3: Протестуйте його роботу

```bash
/ml-release patch
```

Спостерігайте за тим, як agents скоординовано проводять повний цикл релізу.

---

## Найкращі практики для складних систем

### РЕКОМЕНДУЄТЬСЯ

✅ Проектувати agents за принципом **композиції** (composability — коли вивід одного легко передається на вхід наступному)

✅ **Детально логувати все** (це значно полегшує налагодження збоїв)

✅ Тестувати готові workflows спочатку на **невеликих точкових змінах**

✅ **Документувати весь процес оркестрації** (щоб інші члени команди розуміли логіку роботи)

✅ Будувати **approval gates** для будь-яких ризикованих операцій

✅ **Моніторити стан системи** після завершення автоматичних дій

### НЕ РЕКОМЕНДУЄТЬСЯ

❌ Об'єднувати в ланцюжок занадто багато agents (якщо >7, налагодження стає вкрай складним)

❌ Робити agents **взаємозалежними** (намагайтеся дотримуватися слабкого зв'язку / loose coupling)

❌ Ігнорувати **error handling** (збої обов'язково траплятимуться)

❌ Запускати автоматичні релізи в production **без попереднього тестування** workflow

❌ Припускати, що agents **завжди прийматимуть однакові рішення** (будуйте логіку вирішення конфліктів)

---

## Валідація: Ви готові, якщо...

✓ Ви можете детально пояснити шаблони оркестрації кількох agents

✓ Ви самостійно створили щонайменше 2-3 взаємодіючих agents

✓ Ви розумієте стратегії обробки помилок (error handling)

✓ Ви вмієте проектувати процеси автоматизації з використанням approval gates

✓ Ви готові самостійно побудувати автоматизацію випуску релізів для власного проєкту

---

## Вітаємо! Що далі?

Ви повністю пройшли 7-модульний шлях навчання! Тепер ви володієте знаннями про:

- ✅ Встановлення та налаштування (Installation and setup)
- ✅ Цикл взаємодії та context (Core loop and context)
- ✅ Пам'ять та конфігурування (Memory and configuration)
- ✅ Спеціалізацію agents (Agent specialization)
- ✅ Навички та бази знань (Skills and knowledge)
- ✅ Hooks та автоматизацію (Hooks and automation)
- ✅ Складну оркестрацію кількох agents (Advanced orchestration)

### Наступні кроки

**Варіант A: Глибоке занурення у конкретний напрямок**
- Детальніше про безпеку: `guide/security/`
- Детальніше про DevOps та інфраструктуру: `guide/ops/`
- Детальніше про архітектуру: `guide/core/architecture.md`

**Варіант B: Створення власної автоматизації**
- Створіть індивідуальний multi-agent workflow для вашого поточного проєкту
- Виконайте одну з практичних вправ цього навчального шляху
- Створіть набір плагінів та поділіться ним із командою

**Варіант C: Вивчення готових прикладів**
- Перегляньте готові конфігурації agents у `examples/agents/`
- Дослідіть набори плагінів у `examples/plugins/`
- Вивчіть шаблони проектування skills у `guide/core/skill-design-patterns.md`

**Варіант D: Самооцінка та аудит знань**
- Запустіть `/self-assessment comprehensive`, щоб виявити можливі прогалини в знаннях
- Отримайте персоналізовані рекомендації
- Створіть план навчання для підтягування слабких зон

---

**Завершили Module 07?** → Ви — досвідчений користувач Claude Code.

Для глибшого занурення відкрийте повний посібник `guide/ultimate-guide.md` або навчіть інших тому, що ви вивчили.

---
**Локалізація**: [Serhii (MacPlus Software)](https://macplus-software.com)
*Остання синхронізація: Травень 2026*
