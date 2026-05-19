---
title: "Claude Code — Візуальні діаграми"
description: "48 інтерактивних Mermaid-діаграм, які охоплюють усі основні концепції Claude Code"
tags: [reference, architecture, diagrams, mermaid]
---

# Claude Code — Візуальні діаграми

48 інтерактивних Mermaid-діаграм, упорядкованих в 10 тематичних файлах. Кожна діаграма містить Mermaid-версію (яка рендериться нативно на GitHub) та ASCII-альтернативу.

> Для діаграм лише в ASCII та друкованого візуального довідника → [visual-reference.md](../core/visual-reference.uk.md)

---

## Візуальна палітра

Усі діаграми використовують послідовну палітру Bold Guy:

| Колір | Hex | Використання |
|-------|-----|--------------|
| Теплий бежевий | `#F5E6D3` | Дії користувача, вузли введення |
| Палений помаранчевий | `#E87E2F` | Ключові рішення, дії Claude |
| М'який зелений | `#7BC47F` | Шляхи успіху, рекомендації |
| Попереджувальний червоний | `#E85D5D` | Небезпека, антипатерни, ризики |
| Нейтральний сірий | `#B8B8B8` | Інфраструктура, пасивні елементи |
| Світло-синій | `#6DB3F2` | Інформація, посилання на документацію |

## Угоди Mermaid

| Форма | Синтаксис | Значення |
|-------|-----------|----------|
| Заокруглений прямокутник | `(text)` | Крок процесу, дія |
| Ромб | `{text}` | Точка рішення |
| Стадіон | `([text])` | Початок / Кінець (термінал) |
| Шестикутник | `{{text}}` | Зовнішня система або API |
| Підпрограма | `[[text]]` | Внутрішній компонент Claude Code |
| Циліндр | `[(text)]` | Сховище даних, персистентний стан |

---

## Навігація

| Файл | Діаграми | Теми |
|------|----------|------|
| [01-foundations.md](./01-foundations.uk.md) | 4 | 4-рівнева модель, конвеєр робочого процесу, дерево рішень, режими дозволів |
| [02-context-and-sessions.md](./02-context-and-sessions.uk.md) | 4 | Зони контексту, ієрархія пам'яті, телепортація сесії, свіжий контекст |
| [03-configuration-system.md](./03-configuration-system.uk.md) | 4 | Пріоритет конфігурації, навички проти команд та агентів, життєвий цикл агента, hooks |
| [04-architecture-internals.md](./04-architecture-internals.uk.md) | 4 | Головний цикл (master loop), категорії інструментів, збірка системного промпту, ізоляція sub-agents |
| [05-mcp-ecosystem.md](./05-mcp-ecosystem.uk.md) | 4 | Карта екосистеми MCP, архітектура MCP, атака rug pull, ієрархія конфігурації |
| [06-development-workflows.md](./06-development-workflows.uk.md) | 5 | Цикл TDD, конвеєр спочатку-специфікація, керований планом робочий процес, ітераційне вдосконалення, шляхи адаптації до AI (AI fluency) |
| [07-multi-agent-patterns.md](./07-multi-agent-patterns.uk.md) | 5 | Топології агентів, worktrees, дублювання інстансів (dual-instance), горизонтальне масштабування, матриця рішень |
| [08-security-and-production.md](./08-security-and-production.uk.md) | 4 | 3-рівневий захист, рішення про sandbox, парадокс верифікації, конвеєр CI/CD |
| [09-cost-and-optimization.md](./09-cost-and-optimization.uk.md) | 4 | Вибір моделі, оптимізація витрат, рівні підписки, зменшення кількості токенів |
| [10-adoption-and-learning.md](./10-adoption-and-learning.uk.md) | 3 | Шляхи онбордингу, протокол UVAL, калібрування довіри |
| [11-context-engineering.md](./11-context-engineering.uk.md) | 4 | 3-рівнева система контексту, деградація дотримання правил, модульна архітектура, розміщення правил |
| [12-enterprise-governance.md](./12-enterprise-governance.uk.md) | 3 | Рівні ризику управління, робочий процес затвердження MCP, класифікація даних |
| **Всього** | **48** | |

---

## Навігація за сценаріями використання

### "Я новачок у Claude Code — з чого почати?"
1. [Швидке дерево рішень](./01-foundations.uk.md#quick-decision-tree) — Чи варто мені використовувати Claude Code?
2. [9-кроковий конвеєр робочого процесу](./01-foundations.uk.md#9-step-workflow-pipeline) — Як це працює?
3. [Режими дозволів](./01-foundations.uk.md#permission-modes-comparison) — Які існують режими безпеки?
4. [Шляхи онбордингу](./10-adoption-and-learning.uk.md#onboarding-adaptive-learning-paths) — Який шлях мені підходить?

### "Я хочу зрозуміти архітектуру"
1. [Головний цикл (master loop)](./04-architecture-internals.uk.md#the-master-loop) — Основний механізм виконання
2. [Збірка системного промпту](./04-architecture-internals.uk.md#system-prompt-assembly) — Як будується контекст
3. [4-рівнева система контексту](./01-foundations.uk.md#chatbot-to-context-system-4-layer-model) — Модель трансформації
4. [Категорії інструментів](./04-architecture-internals.uk.md#tool-categories) — Які інструменти доступні

### "Мене турбує безпека"
1. [Атака MCP rug pull](./05-mcp-ecosystem.uk.md#mcp-rug-pull-attack-chain) — Основний вектор загроз
2. [3-рівневий захист](./08-security-and-production.uk.md#security-3-layer-defense) — Як захистити себе
3. [Дерево рішень щодо sandbox](./08-security-and-production.uk.md#sandbox-decision-tree) — Коли використовувати sandbox
4. [Парадокс верифікації](./08-security-and-production.uk.md#the-verification-paradox) — Не довіряйте Claude верифікувати самого себе

### "Я хочу зменшити свої витрати на токени"
1. [Схема прийняття рішень щодо вибору моделі](./09-cost-and-optimization.uk.md#model-selection-decision-flow) — Виберіть правильну модель
2. [Дерево оптимізації витрат](./09-cost-and-optimization.uk.md#cost-optimization-decision-tree) — Систематичне зниження витрат
3. [Конвеєр зменшення кількості токенів](./09-cost-and-optimization.uk.md#token-reduction-strategies-pipeline) — RTK + гігієна сесій
4. [Зони керування контекстом](./02-context-and-sessions.uk.md#context-management-zones) — Керуйте розміром контексту

### "Я хочу використовувати кілька агентів"
1. [Топологія команд агентів](./07-multi-agent-patterns.uk.md#agent-teams-topology-3-patterns) — 3 патерни оркестрації
2. [Матриця рішень для кількох інстансів](./07-multi-agent-patterns.uk.md#multi-instance-decision-matrix) — Який патерн використовувати?
3. [Багатоінстансність через git worktree](./07-multi-agent-patterns.uk.md#git-worktree-multi-instance-pattern) — Паралельна ізоляція
4. [Ізоляція контексту sub-agents](./04-architecture-internals.uk.md#sub-agent-context-isolation) — Як ізолюються агенти

### "Я хочу налаштувати MCP-сервери"
1. [Карта екосистеми MCP](./05-mcp-ecosystem.uk.md#mcp-server-ecosystem-map) — Які сервери існують
2. [Архітектура MCP](./05-mcp-ecosystem.uk.md#mcp-architecture-client-server) — Як це працює
3. [Ізоляція конфігурації MCP](./05-mcp-ecosystem.uk.md#mcp-config-hierarchy) — Де живуть конфігурації

### "Я хочу керувати використанням Claude Code у своїй команді"
1. [Рівні ризику управління](./12-enterprise-governance.uk.md#governance-risk-tiers) — Який рівень контролю підходить для вашого контексту?
2. [Робочий процес управління MCP](./12-enterprise-governance.uk.md#mcp-governance-workflow) — Конвеєр затвердження для MCP-серверів
3. [Правила класифікації даних](./12-enterprise-governance.uk.md#data-classification--claude-code-access-rules) — До чого Claude має і не має доступу

### "Я хочу покращити дотримання контексту з боку Claude"
1. [Дерево рішень щодо розміщення правил](./11-context-engineering.uk.md#rule-placement-decision-tree) — Куди помістити це правило?
2. [3-рівнева система контексту](./11-context-engineering.uk.md#the-3-layer-context-system) — Глобальний / Проект / Сесія
3. [Бюджет контексту та відповідність](./11-context-engineering.uk.md#context-budget--adherence-degradation) — Чому правила перестають виконуватися
4. [Модульна архітектура](./11-context-engineering.uk.md#monolithic-vs-modular-architecture) — Обмеження шляхів як рішення

---

*Назад до [guide/README.md](../README.uk.md) | ASCII-діаграми → [visual-reference.md](../core/visual-reference.uk.md)*

---
**Локалізація**: [Serhii (MacPlus Software)](https://macplus-software.com)
*Остання синхронізація: Травень 2026*
