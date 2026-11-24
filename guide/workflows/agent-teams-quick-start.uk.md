---
title: "Швидкий старт для команд агентів (Agent Teams Quick Start Guide)"
description: "Практичний 5-хвилинний посібник із налаштування з шаблонами копіювання-вставки для команд агентів"
tags: [workflow, agents, tutorial]
---

# Швидкий старт для команд агентів (Agent Teams Quick Start Guide)

> **Практичний посібник із використання команд агентів у ваших проектах**
> **Час читання**: 8-10 хв | **Повна документація**: [Agent Teams](./agent-teams.uk.md) (30 хв огляду)

## Що це таке?

Ви знаєте, що команди агентів існують. Ви читали теорію. Але **коли насправді варто використовувати їх у своїх проектах?**

Цей посібник пропонує вам:
- ✅ **5-хвилинне налаштування** (оточення → перший тест)
- ✅ **4 шаблони для копіювання та вставки** для реальних проектів (Guide + RTK)
- ✅ **Матриця рішень** (коли ТАК, коли НІ)
- ✅ **Метрики** для вимірювання окупності інвестицій (ROI)
- ✅ **«Червоні прапорці»** для уникнення марних витрат

**Пропустіть, якщо**: вам потрібна теорія → Замість цього читайте [повну документацію по Agent Teams](./agent-teams.uk.md).

---

## Зміст

1. [5-хвилинне налаштування](#1-5-хвилинне-налаштування)
2. [Шаблони для ваших проектів](#2-шаблони-для-ваших-проектів)
   - 2.1 [Посібник Claude Code - Огляд перед релізом](#21-посібник-claude-code---огляд-перед-релізом)
   - 2.2 [Посібник Claude Code - Синхронізація цільової сторінки (Landing Sync)](#22-посібник-claude-code---синхронізація-цільової-сторінки-landing-sync)
   - 2.3 [Посібник Claude Code - Оновлення документації у кількох файлах](#23-посібник-claude-code---оновлення-документації-у-кількох-файлах)
   - 2.4 [RTK - Огляд PR на безпеку](#24-rtk---огляд-pr-на-безпеку)
3. [Матриця рішень: коли використовувати](#3-матриця-рішень-коли-використовувати)
4. [Мінімальний шаблон робочого процесу](#4-мінімальний-шаблон-робочого-процесу)
5. [Метрики успіху](#5-метрики-успіху)
6. [Обмеження та «червоні прапорці»](#6-обмеження-та-червоні-прапорці)

---

## 1. 5-хвилинне налаштування

### Крок 1: Перевірка передумов

```bash
# Check Claude Code version (v2.1.32+ required)
claude --version

# Check model availability
claude
> /model opus
# Check the resolved model in /model; provider aliases can differ
```

**Мінімальні вимоги**:
- Claude Code v2.1.32+
- Модель, доступна вашому обліковому запису; Opus необов'язковий, а teammates можуть використовувати різні моделі
- Git-репозиторій (команди агентів використовують git для координації)

### Крок 2: Увімкнення функції

```bash
# Set environment variable (add to ~/.bashrc or ~/.zshrc for persistence)
export CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1

# Launch Claude Code
claude
```

### Крок 3: Перевірка

```
> Are agent teams enabled?
```

**Очікувана відповідь**:
```
Yes, agent teams are enabled in this session. I can create teams
of agents to work in parallel on complex tasks using:
- Multi-agent coordination
- Git-based task claiming
- Autonomous team coordination
```

**Якщо вимкнено**: перевірте, чи встановлено змінну оточення (`echo $CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS`).

### Крок 4: Перший тест (2 агенти)

```
> Create a simple test team to analyze this README:
> - Agent 1: Check structure (sections, TOC, badges)
> - Agent 2: Check content quality (clarity, examples, completeness)
```

**Що відбувається**:
1. Claude створює 2 агентів (ви побачите повідомлення "Creating team...")
2. Агенти працюють паралельно (ви можете бачити повідомлення "Idle" — це нормально)
3. Claude представляє зведені результати (збіжність + унікальні висновки)

**Навігація**:
- `Shift+Down`: Перемикання між виводами колег по команді (у процесі роботи)
- Основний екран: Зведений синтез

**Тривалість**: 1-2 хв для простого завдання з 2 агентами.

---

## 2. Шаблони для ваших проектів

### 2.1 Посібник Claude Code - Огляд перед релізом

**Сценарій використання**: Систематичний аудит перед підвищенням версії для виявлення проблем узгодженості (битих посилань, невідповідності підрахунків, неправильних версій)

**Тригер**: Перед кожним виконанням команди `/release`

**Тривалість**: 3-5 хв

**Склад команди**:
```
Team: pre-release-audit (3 agents)
├─ accuracy-auditor → Verify claims, stats, versions, external links
├─ consistency-checker → Check template count, eval count, guide lines match across files
└─ breaking-checker → Identify breaking changes vs last release
```

**Промпт для копіювання та вставки**:
```
> Create a pre-release audit team:
> - Accuracy: Check all claims, stats, version numbers, external links in CHANGELOG.md, README.md, and guide/ultimate-guide.md
> - Consistency: Verify template count (count examples/ files), eval count (count docs/resource-evaluations/ files), guide lines (wc -l guide/ultimate-guide.md) match across README.md, guide/cheatsheet.md, machine-readable/reference.yaml
> - Breaking: Identify breaking changes vs v3.23.0 by analyzing CHANGELOG.md [Unreleased] section
```

**ROI (окупність)**: виловлює такі помилки, як:
- Пошкодження URL LinkedIn (виявлено під час реального аудиту сьогодні)
- Розсинхронізація між guide та landing (підрахунок шаблонів)
- Неправильні номери версій у кількох файлах
- Биті зовнішні посилання

**Коли пропустити**: Прості виправлення друкарських помилок (без змін версій/підрахунків/посилань).

**Реальний приклад** (тест від 2026-02-08):
```
Findings:
- Accuracy: 1 critical (LinkedIn URL malformed), 3 warnings (external links to verify)
- Consistency: 2 criticals (template count mismatch README vs landing, line numbers outdated in reference.yaml)
- Breaking: 0 breaking changes detected vs v3.23.0 (clean release)

Convergence: 2 agents flagged template count issue (high confidence)
Time: 4 min 12 sec
Verdict: ✅ High value, found 3 criticals that would've shipped
```

---

### 2.2 Посібник Claude Code - Синхронізація цільової сторінки (Landing Sync)

**Сценарій використання**: Перевірка синхронізації guide/landing (версія, підрахунки, вміст) без запуску ручного скрипта

**Тригер**: Після значних змін у guide (підвищення версії, додавання шаблонів, зміни у FAQ)

**Тривалість**: 2-3 хв

**Склад команди**:
```
Team: landing-sync (2 agents)
├─ guide-scanner → Extract version, template count, eval count, guide lines, FAQ content
└─ landing-scanner → Compare with index.html, examples.html, check sync status
```

**Промпт для копіювання та вставки**:
```
> Validate guide/landing synchronization:
> - Guide scanner: Extract version from VERSION file, template count (find examples/ -type f | wc -l), eval count (find docs/resource-evaluations/ -name "*.md" | wc -l), guide lines (wc -l guide/ultimate-guide.md), FAQ entries from README.md
> - Landing scanner: Check ../claude-code-ultimate-guide-landing/index.html and examples.html for version in footer+FAQ, template count in badges, eval count, guide lines approximation (~9800+)
>
> Report: Synced ✅ / Mismatches with line numbers
```

**ROI (окупність)**:
- Нульова розсинхронізація потрапляє в продакшен
- Уникає ручного виконання `./scripts/check-landing-sync.sh`
- Швидше, ніж скрипт (2 хв проти 5 хв на запуск скрипта + виправлення)

**Коли пропустити**: Чисті зміни коду (документи/підрахунки не зачіпаються).

**Критерії успіху**:
```
✅ All synced: Version, template count, eval count match
⚠️ Mismatch: Specific line numbers in index.html to fix
```

---

### 2.3 Посібник Claude Code - Оновлення документації у кількох файлах

**Сценарій використання**: Додавання документації для нової функції у кількох файлах (ultimate-guide.md, reference.yaml, README.md) із забезпеченням узгодженості перехресних посилань

**Тригер**: Новий розділ функції (>50 рядків), зворотні несумісні зміни, оновлення архітектури

**Тривалість**: 5-8 хв

**Склад команди**:
```
Team: doc-update (3 agents)
├─ content-writer → Write main section in ultimate-guide.md with examples
├─ index-updater → Update TOC, reference.yaml entries, README navigation
└─ consistency-checker → Verify cross-references, line numbers, anchors work
```

**Промпт для копіювання та вставки**:
```
> Update documentation for new "[FEATURE NAME]" feature:
> - Content Scope: Write section [X.Y] in guide/ultimate-guide.md with:
>   - Overview (what/why/when)
>   - 2-3 concrete examples
>   - Best practices + gotchas
>   - Links to related sections
>   Context: guide/ultimate-guide.md section [X.Y] only
> - Index Scope: Update:
>   - guide/ultimate-guide.md TOC (add section [X.Y])
>   - machine-readable/reference.yaml (add entry with line numbers)
>   - README.md navigation (add link if major feature)
>   Context: Index files only (TOC, reference.yaml, README.md)
> - Consistency Scope: Verify:
>   - All cross-references resolve correctly
>   - Line numbers in reference.yaml match actual content
>   - Anchors in README point to correct sections
>   - No broken internal links
>   Context: All modified files for cross-reference validation
```

**ROI (окупність)**:
- Нуль битих посилань (consistency-checker знаходить усе)
- На 60% швидше, ніж послідовно (написання → індексування → перевірка)
- Паралельна робота скорочує час очікування

**Коли пропустити**: Редагування одного файлу (<50 рядків), перехресні посилання не потрібні.

**Реальний приклад** (додавання розділу Agent Teams):
```
Task: Add "Agent Teams" as section 9.20 (300 lines)
Files touched: 3 (ultimate-guide.md, reference.yaml, README.md)

Sequential estimate: 12-15 min (write → index → verify)
Agent Teams: 7 min 30 sec (3 agents parallel)
Savings: 40% time + zero manual cross-ref checks
```

---

### 2.4 RTK - Огляд PR на безпеку

**Сценарій використання**: Огляд PR від зовнішнього контриб'ютора на наявність проблем із безпекою (ін'єкції, витік токенів), ідіом Rust та продуктивності

**Тригер**: PR відкритий не основним контриб'ютором, PR торкається конфіденційного коду (авторизація, зовнішні команди, регулярні вирази)

**Тривалість**: 5-8 хв

**Склад команди**:
```
Team: security-pr-review (3 agents)
├─ rust-expert → Check ownership patterns, error handling (anyhow/thiserror), idiomatic code
├─ security-auditor → Scan for injection risks, token leaks, input sanitization
└─ perf-analyzer → Review allocations, async patterns, compiled regex
```

**Промпт для копіювання та вставки**:
```
> Review PR #[NUMBER] with scope-focused analysis:
> - Rust Scope: Check:
>   - Ownership patterns (prefer &str over String, minimize clones)
>   - Error handling (anyhow::Result with .context(), no unwrap outside tests)
>   - Idiomatic code (impl after type, #[cfg(test)] mod tests)
>   - Clippy compliance (zero warnings)
>   Context: All modified .rs files
> - Security Scope: Scan for:
>   - Command injection (shell escapes, argument sanitization)
>   - Token/credential leaks (hardcoded secrets, logs, error messages)
>   - Input sanitization (path traversal, regex DoS)
>   - File operations (path validation, permissions)
>   Context: Input handling, auth, file I/O code
> - Performance Scope: Review:
>   - Unnecessary allocations (String::from vs &str)
>   - Async patterns (spawn_blocking for CPU-bound work)
>   - Compiled regex (lazy_static! for hot paths)
>   - Algorithm complexity (O(n) vs O(n²))
>   Context: Hot paths, loops, async functions
```

**ROI (окупність)**:
- Виявлення «сліпих зон»: Безпека + Rust + Продуктивність = сфери, які один рецензент міг би пропустити
- Стабільна якість огляду (не залежить від настрою/зосередженості рецензента)
- Швидше, ніж послідовно (3 агенти паралельно проти огляду в 3 проходи)

**Коли пропустити**: Внутрішні PR від надійних контриб'юторів, тривіальні зміни (тільки документи, коментарі, тести).

**Критерії успіху**:
```
✅ Convergence: 2+ agents flag same critical issue (high confidence)
✅ Unique insights: Each agent finds domain-specific issues (Rust/Security/Perf)
❌ False positives: <20% of findings are invalid
```

**Реальний приклад** (гіпотетичний зовнішній PR):
```
PR: Add new git filter command
Agents findings:
- Rust: 3 issues (unwrap in production code, missing .context(), non-idiomatic error handling)
- Security: 2 criticals (shell injection via user input, token leak in error message)
- Perf: 1 issue (regex compiled on every call, not lazy_static)

Convergence: Security + Rust both flagged missing input sanitization (high confidence)
Time: 6 min 40 sec
Verdict: ✅ Critical security issues caught, PR requires revision
```

---

## 3. Матриця рішень: коли використовувати

| Ваша ситуація | Agent Teams ? | Обґрунтування |
|-----------|---------------|--------|
| **Огляд перед релізом (Guide)** | ✅ ТАК | Багаторівневий аудит (точність + узгодженість + зміни) вимагає паралельних точок зору |
| **Просте виправлення друкарської помилки** | ❌ НІ | Надмірність, 1 агент = 10 сек, 3 агенти = роздування витрат |
| **Зовнішній PR (RTK)** | ✅ ТАК | Безпека + Rust + Продуктивність = виявлення «сліпих зон», огляд з високими ставками |
| **Оновлення документації у кількох файлах (Guide)** | ✅ ТАК | Вміст + Індекс + Узгодженість = нуль битих посилань, паралельна робота |
| **Перевірка синхронізації цільової сторінки** | ⚠️ МОЖЛИВО | Використовуйте команди агентів, якщо є підозра на розсинхронізацію, інакше `./scripts/check-landing-sync.sh` швидше |
| **Оновлення CHANGELOG** | ❌ НІ | Послідовне завдання (лінійний запис), немає переваг від паралелізму |
| **Редагування одного файлу (RTK)** | ❌ НІ | Координація не потрібна, послідовне виконання підходить |
| **Невелике коригування README (<50 рядків)** | ❌ НІ | Без перехресних посилань, без складності, один агент впорається швидше |
| **Проектування архітектури** | ✅ ТАК | Кілька перспектив (фронтенд, бекенд, інфраструктура, безпека) виявляють «сліпі зони» |
| **Дослідження багу** | ⚠️ МОЖЛИВО | Прості баги → НІ, складні збої в кількох компонентах → ТАК |

### Практичне правило

**Використовуйте Agent Teams, коли**:
- ✅ Ви природно думаєте: «Мені варто перевірити X, Y та Z»
- ✅ Високі ставки (реліз у продакшен, зовнішній контриб'ютор, чутливий до безпеки код)
- ✅ Необхідний аналіз у кількох напрямках (напрямок Rust + безпека + продуктивність)
- ✅ Важлива узгодженість між файлами (синхронізація посилань, підрахунків, версій)
- ✅ Можлива паралельна робота (незалежні завдання, без послідовних залежностей)

**Не використовуйте Agent Teams, коли**:
- ❌ Просте завдання (<5 файлів, <100 рядків, 1 область)
- ❌ Послідовний робочий процес (крок Б залежить від результату кроку А)
- ❌ Обмежений бюджет (3x токенів, резервуйте для високовартісних завдань)
- ❌ Багато записів (багато редагувань одних і тих самих файлів = конфлікти злиття)

### Офіційні рекомендації щодо розміру та обмеження (перевірено 2026-11-01)

[Документація Agent Teams](https://code.claude.com/docs/en/agent-teams) рекомендує починати з **3-5 teammates** і **5-6 завдань на teammate**. Два обмеження впливають на планування сесії:

- `/resume` і `/rewind` не відновлюють teammates, що працюють у тому самому процесі (in-process); після відновлення lead створіть заміну.
- Teammates за замовчуванням не ізольовані у worktrees; призначайте їм окремі набори файлів або дайте кожному власний worktree.

Перш ніж братися за команду, прочитайте [Single agent, subagents or a team: the October 2026 evidence](https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#single-agent-subagents-or-a-team-the-october-2026-evidence): на обмежених завданнях один цикл агента зі skills часто відповідав мультиагентним схемам або перевершував їх.

---

## 4. Мінімальний шаблон робочого процесу

### Шаблон Bash (багаторазовий)

```bash
# 1. Setup (once per session)
export CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1

# 2. Launch Claude
claude

# 3. Create team (prompt template)
> Create a team to [TASK]:
> - Agent 1 ([SCOPE/CONTEXT]): [SPECIFIC MISSION]
> - Agent 2 ([SCOPE/CONTEXT]): [SPECIFIC MISSION]
> - Agent 3 ([SCOPE/CONTEXT]): [SPECIFIC MISSION]
>
> [FILES/DIRECTORIES TO ANALYZE]

# 4. Observe (optional)
# Shift+Down to cycle through teammate outputs (in-process mode)

# 5. Synthesis
# Claude presents consolidated findings automatically

# 6. Act
# Fix critical findings, skip minor ones
```

### Приклади промптів (готові до копіювання та вставки)

#### Аудит посібника перед релізом

```
> Create a pre-release audit team:
> - Accuracy: Check all claims, stats, version numbers, external links in CHANGELOG.md, README.md, and guide/ultimate-guide.md
> - Consistency: Verify template count (count examples/ files), eval count (count docs/resource-evaluations/ files), guide lines (wc -l guide/ultimate-guide.md) match across README.md, guide/cheatsheet.md, machine-readable/reference.yaml
> - Breaking: Identify breaking changes vs v3.23.0 by analyzing CHANGELOG.md [Unreleased] section
```

#### Огляд PR на безпеку (RTK)

```
> Review PR #42 with scope-focused analysis:
> - Rust Scope: Check ownership patterns, error handling (anyhow/thiserror), idiomatic code in modified files (context: src/**/*.rs)
> - Security Scope: Scan for injection risks, token leaks, input sanitization (context: auth, input handling code)
> - Performance Scope: Review allocations, async patterns, compiled regex (context: hot paths, loops)
```

#### Оновлення документації у кількох файлах

```
> Update documentation for new "Agent Teams Quick Start" feature:
> - Content Scope: Write guide/workflows/agent-teams-quick-start.md with overview, 4 patterns, decision matrix, metrics
> - Index Scope: Update guide/ultimate-guide.md (add reference section 9.20), machine-readable/reference.yaml (add entry), CHANGELOG.md (add "Added" entry)
> - Consistency Scope: Verify all cross-refs work, line numbers match, no broken links (context: all modified files)
```

#### Перевірка синхронізації цільової сторінки

```
> Validate guide/landing synchronization:
> - Guide scanner: Extract version from VERSION file, template count (find examples/ -type f | wc -l), eval count (find docs/resource-evaluations/ -name "*.md" | wc -l), guide lines (wc -l guide/ultimate-guide.md)
> - Landing scanner: Check ../claude-code-ultimate-guide-landing/index.html and examples.html for version, counts, guide lines approximation
```

---

## 5. Метрики успіху

### Як вимірювати ROI для Agent Teams

| Метрика | Ціль | Як виміряти |
|--------|--------|----------------|
| **Рівень збіжності** | >50% | Кількість зауважень, позначених 2+ агентами / загальна кількість зауважень. Висока збіжність = висока впевненість. |
| **Унікальні висновки** | Кожен агент ≥1 | Кожен агент повинен знайти принаймні 1 унікальну проблему у своїй області. Якщо агент знаходить 0 унікальних = токени витрачено марно. |
| **Рівень хибних спрацьовувань** | <20% | Кількість недійсних висновків / загальна кількість висновків. Занадто багато хибних спрацьовувань = погані промпти. |
| **Економія часу** | 60-70% | Порівняйте час роботи команд агентів із послідовним часом (оцінюйте як 3x часу одного агента для 3 завдань). |
| **Рівень виявлення багів** | >80% | Кількість критичних багів, знайдених агентами / загальна кількість багів, знайдених після релізу. Високий показник = ефективне запобігання. |

### Реальний приклад: тест огляду перед релізом (2026-02-08)

```
Task: Pre-release audit for v3.23.1
Agents: 3 (accuracy-auditor, consistency-checker, breaking-checker)
Duration: 4 min 12 sec

Findings (raw): 45 total
├─ Accuracy: 12 (1 critical: LinkedIn URL malformed, 11 warnings)
├─ Consistency: 18 (2 criticals: template count desync, line numbers outdated)
└─ Breaking: 15 (0 breaking changes, 15 informational notes)

Findings (deduplicated): ~30 unique issues

Convergence analysis:
├─ High confidence (2-3 agents): 4 issues
│   ├─ Template count mismatch (consistency + accuracy)
│   ├─ Line numbers outdated (consistency + accuracy)
│   ├─ External link verification needed (accuracy + breaking)
│   └─ Version sync across files (all 3 agents)
└─ Unique insights:
    ├─ Accuracy: LinkedIn URL corruption (only this agent caught it)
    ├─ Consistency: TOC structure deviation (only this agent)
    └─ Breaking: Changelog format improvement suggestion (only this agent)

Metrics:
├─ Convergence rate: 4/30 = 13% (lower than target, but 4 criticals flagged by multiple agents = high confidence on what matters)
├─ Unique insights: 3/3 agents = 100% (each agent found unique issues in their domain)
├─ False positive rate: 2/30 = 6.6% (below 20% target ✅)
├─ Time saving: 4 min vs estimated 12 min sequential = 66% savings ✅
├─ Bug catch rate: 3 critical bugs caught that would've shipped = prevented production issues ✅

Verdict: ✅ High value for pre-release audits
```

### Як відстежувати ваші метрики

**Після кожного завдання команди агентів**:

1. **Підрахуйте висновки**: запишіть сирі результати для кожного агента, а потім дедуплікуйте їх
2. **Позначте збіжність**: які проблеми були помічені 2+ агентами?
3. **Перевірте унікальні висновки**: чи знайшов кожен агент хоча б 1 специфічну для його області проблему?
4. **Перевірте хибні спрацьовувань**: скільки висновків були недійсними/шумом?
5. **Порівняння часу**: тривалість роботи команди агентів проти розрахункового послідовного часу
6. **Валідація після релізу**: чи виявила команда агентів баги, які могли потрапити у реліз?

**Ведіть журнал** (таблиця Markdown у документах проекту):

```markdown
| Date | Task | Agents | Duration | Findings | Convergence | Unique | False+ | Time Saved | Bugs Caught |
|------|------|--------|----------|----------|-------------|--------|--------|------------|-------------|
| 2026-02-08 | Pre-release v3.23.1 | 3 | 4m12s | 30 | 13% (4 critical) | 3/3 | 6.6% | 66% | 3 |
```

**Налаштуйте промпти**, якщо метрики не відповідають цілям:
- Низька збіжність (<30%) → Занадто вузькі області, більше перекривайте межі контексту
- Немає унікальних висновків → Області занадто схожі, урізноманітніть кути аналізу
- Багато хибних спрацьовувань (>20%) → Занадто розмиті промпти, додайте конкретні критерії

---

## 6. Обмеження та «червоні прапорці»

### Чого НЕ роблять команди агентів

| Обмеження | Що це означає | Як пом'якшити |
|------------|---------------|-----------|
| **3x токенів** | Кожен агент = окремий виклик моделі = потрійна вартість | Резервуйте для завдань із високими ставками (передреліз, PR на безпеку, а не для виправлення друкарських помилок) |
| **Спам про бездіяльність (Idle)** | Агенти показують повідомлення "Idle" під час координації | Нормальна поведінка, не баг, просто ігноруйте цей спам |
| **Експериментальний статус** | Попередній перегляд дослідження = стабільність не гарантована | Очікуйте помилок, не покладайтеся на команди агентів у критичних для продакшену робочих процесах |
| **Накладні витрати на координацію** | Максимум 3-5 агентів, а не 10 (складність координації зростає) | Дотримуйтеся 2-4 агентів, уникайте промптів на кшталт «команда з 10» |
| **Ізоляція контексту** | Агенти не бачать відкриттів один одного (працюють незалежно) | Claude синтезує висновки, але агенти не можуть спиратися на роботу один одного посеред виконання завдання |

### «Червоні прапорці»: коли НЕ використовувати

❌ **Просте завдання** (<5 файлів, <100 рядків, 1 область)
- Приклад: Виправити друкарську помилку в README.md
- Чому уникати: 3x токенів для 10-секундного завдання = марнотратство

❌ **Послідовний робочий процес** (крок Б залежить від результату кроку А)
- Приклад: Реалізувати функцію → Написати тести → Розгорнути
- Чому уникати: Агенти працюють паралельно, не можуть обробляти залежності

❌ **Обмежений бюджет** (3x токенів, оптимізація витрат)
- Приклад: Особистий проект із обмеженими лімітами API
- Чому уникати: Команди агентів = розкіш для завдань з високими ставками, а не щоденний робочий процес

❌ **Багато записів** (багато редагувань одних і тих самих файлів)
- Приклад: Рефакторинг усієї структури кодової бази
- Чому уникати: Конфлікти злиття, накладні витрати на координацію, агенти заважають один одному

❌ **Огляд з низькими ставками** (внутрішній PR, надійний контриб'ютор, прості зміни)
- Приклад: Член команди виправляє невеликий баг
- Чому уникати: Надмірність, огляд одним агентом швидший і дешевший

### Коли ви ПОВИННІ використовувати (незважаючи на витрати)

✅ **Високі ставки** (реліз у продакшен, чутливий до безпеки код, зовнішній контриб'ютор)
✅ **Кілька областей** (Rust + Безпека + Продуктивність = «сліпі зони»)
✅ **Паралельна робота** (незалежні завдання, без послідовних залежностей)
✅ **Критично важлива узгодженість** (синхронізація файлів, підрахунків, версій)
✅ **Можливість навчання** (розуміння «сліпих зон», покращення промптів)

---

## Резюме: коротка довідка

### Налаштування (5 хв один раз)

```bash
export CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1
claude
> Are agent teams enabled?  # Verify
```

### Коли використовувати (правило прийняття рішень)

**ТАК, якщо**:
- Високі ставки + Кілька областей + Паралельна робота

**НІ, якщо**:
- Просте завдання + Послідовне виконання + Обмежений бюджет

### Шаблони (4 готових до використання)

1. **Огляд перед релізом** (Guide) → Точність + Узгодженість + Зміни
2. **Синхронізація цільової сторінки** (Guide) → Сканер посібника + Сканер цільової сторінки
3. **Оновлення документації у кількох файлах** (Guide) → Вміст + Індекс + Узгодженість
4. **Огляд PR на безпеку** (RTK) → Rust + Безпека + Продуктивність

### Метрики (відстеження ROI)

- Збіжність: >50% (висновки 2+ агентів)
- Унікальні висновки: Кожен агент ≥1
- Хибні спрацьовування: <20%
- Економія часу: 60-70%
- Виявлення багів: >80%

### «Червоні прапорці» (уникнення марнотратства)

- ❌ Просте завдання (<5 файлів)
- ❌ Послідовний робочий процес
- ❌ Обмежений бюджет
- ❌ Багато записів (конфлікти злиття)

---

## Наступні кроки

1. **Спробуйте перший тест** (5 хв налаштування + просте завдання з 2 агентами)
2. **Виберіть 1 шаблон** зі свого проекту (Guide або RTK)
3. **Виміряйте метрики** (збіжність, унікальні висновки, збережений час)
4. **Налаштуйте промпти** на основі результатів
5. **Прочитайте повну документацію** про розширені шаблони: [Agent Teams](./agent-teams.uk.md)

**Маєте запитання?** Перевірте [повну документацію](./agent-teams.uk.md) щодо:
- Глибокого занурення в архітектуру (як працює координація через git)
- Розширених випадків використання (15+ сценаріїв для продакшену)
- Усунення несправностей (поширені проблеми + рішення)
- Кращих практик (розмір команди, дизайн промптів, вирішення конфліктів)

---
**Локалізація**: [Serhii (MacPlus Software)](https://macplus-software.com)
*Остання синхронізація: Травень 2026*
