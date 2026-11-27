---
title: "Приклади Claude Code"
description: "Анотовані шаблони, що пояснюють, чому патерни працюють, з компромісами та альтернативами"
tags: [template, reference, workflows, architecture]
---

# Приклади Claude Code

Анотовані шаблони, які пояснюють, **чому** патерни працюють, а не лише як їх налаштувати. Кожен шаблон містить коментарі про компроміси, альтернативи й випадки, коли варто відступити від шаблону.

> **[📚 Переглянути автогенерований каталог](./CATALOG.uk.md)**: проіндексований за складністю, часом і предметною областю (238 шаблонів у шести категоріях каталогу; загалом 271 шаблон для продакшену)
> **[🔍 Переглянути інтерактивний каталог](./index.html)**: переглядай, копіюй і завантажуй шаблони з підсвічуванням синтаксису

## Нове: автогенерований каталог

**[`CATALOG.md`](./CATALOG.uk.md)** тепер генерується автоматично з метаданих шаблонів і впорядкований за:
- **Складністю**: Beginner, Intermediate, Advanced
- **Часом**: від 5 хв до 4+ годин
- **Предметною областю**: Security, Testing, Deployment, Performance, Architecture, Automation
- **Ключовими словами**: теги для пошуку

Кожен шаблон містить метадані:
```yaml
---
name: template-name
description: One-line description
complexity: beginner|intermediate|advanced
time: 5 min|15 min|30 min|1 hour|2 hours|4+ hours|varies
domain: security|testing|deployment|etc
prerequisites: []
status: stable|experimental|deprecated
keywords: [tag1, tag2]
---
```

**Повну специфікацію див. у [`docs/template-metadata-schema.md`](../docs/template-metadata-schema.uk.md)**.

## Структура

| Каталог | Опис | Кількість |
|--------|-------------|-------|
| [`agents/`](./agents/) | Власні AI-персони для спеціалізованих завдань | 21 + 2 колекції |
| [`commands/`](./commands/) | Slash-команди (автоматизація воркфлоу) | 52 |
| [`hooks/`](./hooks/) | Скрипти безпеки й автоматизації, керовані подіями | 39 записів у каталозі |
| [`skills/`](./skills/) | Багаторазові модулі знань, зокрема [9 на SkillHub](https://skills.palebluedot.live/owner/FlorianBruniaux) | 118 записів у каталозі |
| [`claude-md/`](./claude-md/) | Профілі конфігурації CLAUDE.md | 7 |
| [`config/`](./config/) | Налаштування, MCP, шаблони git | 6 |
| [`memory/`](./memory/) | Шаблони файлів пам'яті CLAUDE.md | 1 |
| [`rules/`](./rules/) | Поведінкові правила для типових патернів рев'ю | 5 |
| [`scripts/`](./scripts/) | Діагностичні та допоміжні скрипти | 17 |
| [`team-config/`](./team-config/) | Шаблони онбордингу команди | 3 |
| [`templates/`](./templates/) | Шаблони сесій і воркфлоу | 2 |
| [`github-actions/`](./github-actions/) | Воркфлоу CI/CD | 6 |
| [`workflows/`](./workflows/) | Просунуті воркфлоу розробки, зокрема обмежені цикли, експерименти з harness і допуск до рев'ю | 6 |
| [`plugins/`](./plugins/) | Плагіни спільноти (SE-CoVe, claude-mem) | 2 |
| [`integrations/`](./integrations/) | Інтеграції із зовнішніми інструментами (Agent Vibes TTS) | 3 |
| [`context-engineering/`](./context-engineering/) | Патерни та профілі контекстної інженерії | 10 |
| [`mcp-configs/`](./mcp-configs/) | Конфігурації MCP-серверів | 1 |
| [`modes/`](./modes/) | Поведінкові режими (SuperClaude) | 1 |
| [`semantic-anchors/`](./semantic-anchors/) | Точна лексика для кращих результатів LLM | 1 |
| [`multi-provider/`](https://github.com/FlorianBruniaux/cc-copilot-bridge) | Міст між кількома провайдерами → окремий репозиторій | - |

## Внесок, пропускна здатність рев'ю та розуміння

- [Пакет для внеску з допомогою AI](templates/ai-assisted-contribution.uk.md): докази й пояснення автора перед поданням
- [Робочий аркуш допуску до рев'ю](workflows/review-admission.uk.md): спільна пропускна здатність, правила призупинення/відновлення і настільна вправа
- [Робочий аркуш контрзаходів для harness](workflows/lean-harness-experiment.uk.md): протестуй один повторюваний збій, дозволений випадок, альтернативні шляхи й вартість контролю
- [Вправа на розуміння під час рев'ю](learning-project/review-comprehension-exercise.uk.md): пояснити, змінити, діагностувати й ескалювати

Ці робочі аркуші є запропонованими процедурами. Їхні приклади не доводять примусового виконання під час роботи чи виміряних приростів у навчанні та пропускній здатності.

## Швидкий старт

1. Скопіюй потрібний шаблон
2. Адаптуй його під свій проєкт
3. Поклади в правильне місце (див. шляхи нижче)

## Розташування файлів

| Тип | Розташування в проєкті | Глобальне розташування |
|------|------------------|-----------------|
| Агенти | `.claude/agents/` | `~/.claude/agents/` |
| Skills | `.claude/skills/` | `~/.claude/skills/` |
| Команди | `.claude/commands/` | `~/.claude/commands/` |
| Hooks | `.claude/hooks/` | `~/.claude/hooks/` |
| Конфігурація | `.claude/` | `~/.claude/` |
| Пам'ять | `./CLAUDE.md` або `.claude/CLAUDE.md` | `~/.claude/CLAUDE.md` |
| Режими | - | `~/.claude/MODE_*.md` |

> **Windows**: заміни `~/.claude/` на `%USERPROFILE%\.claude\`

## Індекс шаблонів

### Агенти (23)

| Файл | Призначення | Модель |
|------|---------|-------|
| [code-reviewer.md](./agents/code-reviewer.uk.md) | Ретельне рев'ю коду | Sonnet |
| [test-writer.md](./agents/test-writer.uk.md) | Генерація тестів за TDD/BDD | Sonnet |
| [security-auditor.md](./agents/security-auditor.uk.md) | Виявлення вразливостей безпеки | Sonnet |
| [refactoring-specialist.md](./agents/refactoring-specialist.uk.md) | Рефакторинг у дусі чистого коду | Sonnet |
| [output-evaluator.md](./agents/output-evaluator.uk.md) | Контроль якості за патерном LLM-as-a-Judge | Haiku |
| [devops-sre.md](./agents/devops-sre.uk.md) | Діагностика інфраструктури за фреймворком FIRE | Sonnet |
| [planner.md](./agents/planner.uk.md) | Стратегічне планування лише для читання перед реалізацією | Opus |
| [implementer.md](./agents/implementer.uk.md) | Механічне виконання в обмеженому обсязі | Haiku |
| [architecture-reviewer.md](./agents/architecture-reviewer.uk.md) | Рев'ю архітектури та дизайну, лише для читання | Opus |
| [adr-writer.md](./agents/adr-writer.uk.md) | Генератор Architecture Decision Record, лише для читання | Opus |
| [integration-reviewer.md](./agents/integration-reviewer.uk.md) | Валідатор інтеграцій під час виконання, лише для читання | Sonnet |
| [plan-challenger.md](./agents/plan-challenger.uk.md) | Змагальне рев'ю плану за 5 вимірами, лише для читання | Sonnet |
| [planning-coordinator.md](./agents/planning-coordinator.uk.md) | Агент синтезу для динамічних дослідницьких команд, лише для читання | Sonnet |
| [security-patcher.md](./agents/security-patcher.uk.md) | Застосування патчів безпеки за знахідками аудиту, пропонує на рев'ю | Sonnet |
| [analytics-with-eval/](./agents/analytics-with-eval/) | Колекція: аналітичний агент + hooks оцінювання | - |
| [cyber-defense/](./agents/cyber-defense/) | Колекція: детектор аномалій, приймач логів, класифікатор ризиків, звітувач про загрози | - |

### Skills (68) · [9 на SkillHub](https://skills.palebluedot.live/owner/FlorianBruniaux)

| Файл | Призначення |
|------|---------|
| [agent-rationale/](./skills/agent-rationale/) | Записує намір, відхилену альтернативу, ризик, докази та відкрите питання для кожного hunk у git notes, з прив'язкою за хешем hunk, виявленням застарілих нотаток і тестами |
| [git-ai-archaeology/](./skills/git-ai-archaeology/) | Археологія git-історії AI coding harness: створення, змінність, копії та покинутість кожного конфігураційного файлу, використання AI-трейлерів за місяцями, фази зрілості |
| [token-audit/](./skills/token-audit/) | Вимірює накладні витрати токенів фіксованого контексту, класифікує правила за частотою використання, аудитує вартість hooks, складає пріоритезований план дій |
| [design-patterns/](./skills/design-patterns/) | Виявляє й аналізує патерни проєктування GoF з пропозиціями з урахуванням стеку |
| [tdd-workflow.md](./skills/tdd-workflow.uk.md) | Процес Test-Driven Development |
| [security-checklist.md](./skills/security-checklist.uk.md) | Перевірки безпеки OWASP Top 10 |
| [pdf-generator.md](./skills/pdf-generator.uk.md) | Професійна генерація PDF (Quarto/Typst) |
| [voice-refine/](./skills/voice-refine/) | Шліфування авторського голосу з прикладами до/після |
| [ast-grep-patterns.md](./skills/ast-grep-patterns.uk.md) | Патерни пошуку коду на основі AST |
| [rtk-optimizer/](./skills/rtk-optimizer/) | Аналіз оптимізації токенів RTK |
| [audit-agents-skills/](./skills/audit-agents-skills/) | Аудит якості агентів, skills і команд |
| [skill-creator/](./skills/skill-creator/) | Створення нових skills із правильною структурою та найкращими практиками |
| [landing-page-generator/](./skills/landing-page-generator/) | Генерація готових до розгортання лендингів із будь-якого репозиторію |
| [ccboard/](./skills/ccboard/) | Всеосяжна TUI/Web-панель для моніторингу Claude Code |
| [guide-recap/](./skills/guide-recap/) | Перетворення записів CHANGELOG на контент для соцмереж (LinkedIn, Twitter/X, Slack) |
| [release-notes-generator/](./skills/release-notes-generator/) | Генерація release notes у 3 форматах із git-комітів |
| [pr-triage/](./skills/pr-triage/) | Керування беклогом PR у 4 фази (аудит, глибоке рев'ю, перевірені коментарі, налаштування worktree) |
| [issue-triage/](./skills/issue-triage/) | Керування беклогом issues у 3 фази (аудит, глибокий аналіз, перевірені дії) |
| [cyber-defense-team/](./skills/cyber-defense-team/) | Оркестрація багатоагентної команди кіберзахисту |
| [talk-pipeline/](./skills/talk-pipeline/) | Конвеєр із 6 етапів: від сирого матеріалу до слайдів через Kimi |
| [eval-rules/](./skills/eval-rules/) | Аудит `.claude/rules/` і `~/.claude/rules/`: frontmatter, glob-шаблони `paths` проти реальних файлів, статус завантаження symlink, перегляд корисності, потім правки на місці |

### Команди (52)

| Файл | Тригер | Призначення |
|------|---------|---------|
| [commit.md](./commands/commit.uk.md) | `/commit` | Повідомлення комітів за Conventional Commits |
| [pr.md](./commands/pr.uk.md) | `/pr` | Створення добре структурованих PR з аналізом обсягу |
| [review-pr.md](./commands/review-pr.uk.md) | `/review-pr` | Воркфлоу рев'ю PR |
| [release-notes.md](./commands/release-notes.uk.md) | `/release-notes` | Генерація release notes у 3 форматах |
| [sonarqube.md](./commands/sonarqube.uk.md) | `/sonarqube` | Аналіз проблем якості SonarCloud для PR |
| [generate-tests.md](./commands/generate-tests.uk.md) | `/generate-tests` | Генерація тестів |
| [git-worktree.md](./commands/git-worktree.uk.md) | `/git-worktree` | Налаштування ізольованого git worktree |
| [git-worktree-status.md](./commands/git-worktree-status.uk.md) | `/git-worktree-status` | Перевірка фонових завдань верифікації worktree |
| [git-worktree-remove.md](./commands/git-worktree-remove.uk.md) | `/git-worktree-remove` | Безпечне видалення worktree з перевірками злиття |
| [git-worktree-clean.md](./commands/git-worktree-clean.uk.md) | `/git-worktree-clean` | Пакетне очищення застарілих worktrees |
| [diagnose.md](./commands/diagnose.uk.md) | `/diagnose` | Інтерактивний помічник з усунення несправностей (FR/EN) |
| [validate-changes.md](./commands/validate-changes.uk.md) | `/validate-changes` | Перевірка перед комітом за патерном LLM-as-a-Judge |
| [catchup.md](./commands/catchup.uk.md) | `/catchup` | Відновлення контексту після /clear |
| [security.md](./commands/security.uk.md) | `/security` | Швидкий аудит безпеки за OWASP |
| [security-check.md](./commands/security-check.uk.md) | `/security-check` | Сканування конфігурації на відомі загрози (~30s) |
| [security-audit.md](./commands/security-audit.uk.md) | `/security-audit` | Повний аудит у 6 фаз з оцінкою /100 |
| [update-threat-db.md](./commands/update-threat-db.uk.md) | `/update-threat-db` | Дослідження й оновлення розвідданих про загрози |
| [audit-agents-skills.md](./commands/audit-agents-skills.uk.md) | `/audit-agents-skills` | Аудит якості конфігурації .claude/ |
| [sandbox-status.md](./commands/sandbox-status.uk.md) | `/sandbox-status` | Перевірка стану ізоляції sandbox |
| [refactor.md](./commands/refactor.uk.md) | `/refactor` | Покращення коду на основі SOLID |
| [explain.md](./commands/explain.uk.md) | `/explain` | Пояснення коду (3 рівні глибини) |
| [optimize.md](./commands/optimize.uk.md) | `/optimize` | Аналіз продуктивності та дорожня карта |
| [ship.md](./commands/ship.uk.md) | `/ship` | Чекліст перед розгортанням |
| [learn/quiz.md](./commands/learn/quiz.uk.md) | `/learn:quiz` | Самоперевірка засвоєння концепцій |
| [learn/teach.md](./commands/learn/teach.uk.md) | `/learn:teach` | Покрокові пояснення концепцій |
| [learn/alternatives.md](./commands/learn/alternatives.uk.md) | `/learn:alternatives` | Порівняння різних підходів |
| [audit-codebase.md](./commands/audit-codebase.uk.md) | `/audit-codebase` | Аудит стану кодової бази з оцінкою за 7 категоріями |
| [plan-start.md](./commands/plan-start.uk.md) | `/plan-start` | Планування в 5 фаз: аналіз PRD, рев'ю дизайну, технічні рішення, дослідницька команда, метрики |
| [plan-execute.md](./commands/plan-execute.uk.md) | `/plan-execute` | Виконання затвердженого плану: ізоляція в worktree, каркас TDD, паралельні агенти, створення PR |
| [plan-validate.md](./commands/plan-validate.uk.md) | `/plan-validate` | Перевірка плану у 2 рівні: структурні перевірки + спеціалізовані агенти, автовиправлення проблем |
| [review-plan.md](./commands/review-plan.uk.md) | `/review-plan` | Структуроване рев'ю плану за 4 осями перед написанням коду |
| [check-cache-bugs.md](./commands/check-cache-bugs.uk.md) | `/check-cache-bugs` | Аудит на баги кешу CC#40524, які можуть непомітно збільшити витрати на API в 10-20 разів |

### Hooks (37)

Безпека насамперед: 12 hooks безпеки, 8 hooks продуктивності, 5 hooks автоматизації, 5 hooks моніторингу.

**Hooks безпеки** (13 bash):

| Файл | Подія | Призначення |
|------|-------|---------|
| [dangerous-actions-blocker.sh](./hooks/bash/dangerous-actions-blocker.sh) | PreToolUse | Блокує `rm -rf`, force-push, операції на продакшені |
| [prompt-injection-detector.sh](./hooks/bash/prompt-injection-detector.sh) | PreToolUse | Виявляє патерни ін'єкцій у промптах |
| [unicode-injection-scanner.sh](./hooks/bash/unicode-injection-scanner.sh) | PreToolUse | Виявляє символи нульової ширини, RTL override, ANSI escape |
| [repo-integrity-scanner.sh](./hooks/bash/repo-integrity-scanner.sh) | PreToolUse | Сканує README/package.json на приховані ін'єкції |
| [security-check.sh](./hooks/bash/security-check.sh) | PreToolUse | Блокує секрети в командах |
| [sandbox-validation.sh](./hooks/bash/sandbox-validation.sh) | PreToolUse | Перевіряє ізоляцію sandbox |
| [file-guard.sh](./hooks/bash/file-guard.sh) | PreToolUse | Захищає чутливі файли від змін |
| [permission-request.sh](./hooks/bash/permission-request.sh) | PreToolUse | Явний потік дозволів для ризикованих операцій |
| [mcp-config-integrity.sh](./hooks/bash/mcp-config-integrity.sh) | SessionStart | Перевіряє хеш конфігурації MCP (захист від CVE) |
| [claudemd-scanner.sh](./hooks/bash/claudemd-scanner.sh) | SessionStart | Виявляє атаки ін'єкцій через CLAUDE.md |
| [output-secrets-scanner.sh](./hooks/bash/output-secrets-scanner.sh) | PostToolUse | Запобігає появі API-ключів/токенів у відповідях Claude |
| [pre-commit-secrets.sh](./hooks/bash/pre-commit-secrets.sh) | Git hook | Не допускає секрети в коміти |
| [security-gate.sh](./hooks/bash/security-gate.sh) | PreToolUse | Виявляє вразливі патерни коду перед записом у файли з кодом |

**Hooks продуктивності** (10):

| Файл | Подія | Призначення |
|------|-------|---------|
| [auto-format.sh](./hooks/bash/auto-format.sh) | PostToolUse | Автоформатування після правок (Prettier, Black, go fmt) |
| [auto-checkpoint.sh](./hooks/bash/auto-checkpoint.sh) | PostToolUse | Автоматичні контрольні точки роботи через інтервали |
| [typecheck-on-save.sh](./hooks/bash/typecheck-on-save.sh) | PostToolUse | Запуск перевірок TypeScript під час збереження |
| [test-on-change.sh](./hooks/bash/test-on-change.sh) | PostToolUse | Запуск тестів у разі зміни файлів |
| [rtk-auto-wrapper.sh](./hooks/bash/rtk-auto-wrapper.sh) | PreToolUse | Автоматично обгортає команди в RTK для економії токенів |
| [rtk-baseline.sh](./hooks/bash/rtk-baseline.sh) | SessionStart | Зберігає базову лінію RTK для відстеження економії за сесію |
| [setup-init.sh](./hooks/bash/setup-init.sh) | SessionStart | Ініціалізує середовище сесії |
| [subagent-stop.sh](./hooks/bash/subagent-stop.sh) | Stop | Звільняє ресурси subagent |
| [auto-rename-session.sh](./hooks/bash/auto-rename-session.sh) | SessionEnd | Генерація назви сесії за допомогою AI (Haiku) |
| [velocity-governor.sh](./hooks/bash/velocity-governor.sh) | PreToolUse | Обмежує частоту викликів інструментів, щоб уникнути тротлінгу API |

**Hooks моніторингу** (6):

| Файл | Подія | Призначення |
|------|-------|---------|
| [output-validator.sh](./hooks/bash/output-validator.sh) | PostToolUse | Евристична перевірка виводу |
| [session-logger.sh](./hooks/bash/session-logger.sh) | PostToolUse | Логує операції для моніторингу |
| [session-summary.sh](./hooks/bash/session-summary.sh) | SessionEnd | Показує статистику сесії (тривалість, інструменти, вартість, економія RTK) |
| [session-summary-config.sh](./hooks/bash/session-summary-config.sh) | CLI-інструмент | Налаштовує розділи й відображення session-summary |
| [learning-capture.sh](./hooks/bash/learning-capture.sh) | Stop | Пропонує щоденно фіксувати отримані знання |
| [privacy-warning.sh](./hooks/bash/privacy-warning.sh) | PostToolUse | Попереджає про можливі витоки приватних даних |

**Сповіщення та TTS** (3):

| Файл | Подія | Призначення |
|------|-------|---------|
| [notification.sh](./hooks/bash/notification.sh) | Notification | Контекстні звукові сповіщення macOS |
| [tts-selective.sh](./hooks/bash/tts-selective.sh) | PostToolUse | Озвучення вибраних результатів (text-to-speech) |
| [pre-commit-evaluator.sh](./hooks/bash/pre-commit-evaluator.sh) | Git hook | LLM-as-a-Judge перед комітом |

**PowerShell** (2):

| Файл | Подія | Призначення |
|------|-------|---------|
| [security-check.ps1](./hooks/powershell/security-check.ps1) | PreToolUse | Блокує секрети в командах |
| [auto-format.ps1](./hooks/powershell/auto-format.ps1) | PostToolUse | Автоформатування після правок |

> **Повну документацію, приклади конфігурації та патерни посилення безпеки див. у [hooks/README.md](./hooks/README.uk.md)**

### Конфігурація (6)

| Файл | Призначення |
|------|---------|
| [settings.json](./config/settings.json) | Конфігурація hooks |
| [mcp.json](./config/mcp.json) | Налаштування MCP-серверів |
| [.gitignore-claude](./config/.gitignore-claude) | Патерни для git ignore |
| [CONTRIBUTING-ai-disclosure.md](./config/CONTRIBUTING-ai-disclosure.uk.md) | Шаблон розкриття використання AI для CONTRIBUTING.md |
| [PULL_REQUEST_TEMPLATE-ai.md](./config/PULL_REQUEST_TEMPLATE-ai.uk.md) | Шаблон PR із зазначенням участі AI |
| [sandbox-native.json](./config/sandbox-native.json) | Конфігурація нативного sandbox Claude Code |
| [settings-personalization.json](./config/settings-personalization.json) | Персоналізація UI: дієслова спінера, власна карусель порад |
| [settings.local.json.example](./config/settings.local.json.example) | Приклад локальних перевизначень (у gitignore) |

### Пам'ять (1)

| Файл | Призначення |
|------|---------|
| [CLAUDE.md.project-template](./memory/CLAUDE.md.project-template) | Пам'ять командного проєкту |
| [CLAUDE.md.personal-template](./memory/CLAUDE.md.personal-template) | Особиста глобальна пам'ять |

### Конфігурації CLAUDE.md (7)

| Файл | Призначення |
|------|---------|
| [learning-mode.md](./claude-md/learning-mode.uk.md) | Конфігурація розробки, орієнтована на навчання |
| [devops-sre.md](./claude-md/devops-sre.uk.md) | Конфігурація проєкту DevOps/SRE |
| [product-designer.md](./claude-md/product-designer.uk.md) | Конфігурація воркфлоу продуктового дизайнера |
| [tts-enabled.md](./claude-md/tts-enabled.uk.md) | Конфігурація з увімкненим озвученням (text-to-speech) |
| [rtk-optimized.md](./claude-md/rtk-optimized.uk.md) | Конфігурація з оптимізацією токенів через RTK |
| [session-naming.md](./claude-md/session-naming.uk.md) | Автоматичне перейменування сесій описовими назвами для паралельної роботи |
| [design-reference-file.md](./claude-md/design-reference-file.uk.md) | Контекст брендбука й UI-кіту для узгодженої генерації UI |

> **Документацію режиму навчання див. у [guide/roles/learning-with-ai.md](../guide/roles/learning-with-ai.uk.md)**
> **Посібник DevOps/SRE див. у [guide/ops/devops-sre.md](../guide/ops/devops-sre.uk.md)**

### Скрипти (17)

| Файл | Призначення | Вивід |
|------|---------|--------|
| [audit-scan.sh](./scripts/audit-scan.sh) | Швидкий сканер для аудиту налаштувань | JSON / Human |
| [check-claude.sh](./scripts/check-claude.sh) | Діагностика стану (macOS/Linux) | Human |
| [check-claude.ps1](./scripts/check-claude.ps1) | Діагностика стану (Windows) | Human |
| [clean-reinstall-claude.sh](./scripts/clean-reinstall-claude.sh) | Процедура чистого перевстановлення (macOS/Linux) | Human |
| [clean-reinstall-claude.ps1](./scripts/clean-reinstall-claude.ps1) | Процедура чистого перевстановлення (Windows) | Human |
| [session-stats.sh](./scripts/session-stats.sh) | Аналіз логів сесій і витрат | JSON / Human |
| [session-search.sh](./scripts/session-search.sh) | Швидкий пошук і відновлення сесій | Human |
| [cc-sessions.py](./scripts/cc-sessions.py) | Розширений пошук сесій з інкрементною індексацією | Human |
| [fresh-context-loop.sh](./scripts/fresh-context-loop.sh) | Автоматичний перезапуск сесій на межі контексту | Human |
| [bridge.py](./scripts/bridge.py) | Перенесення планів між сесіями | JSON |
| [bridge-plan-schema.json](./scripts/bridge-plan-schema.json) | JSON Schema для формату bridge plan v1 | - |
| [migrate-arguments-syntax.sh](./scripts/migrate-arguments-syntax.sh) | Міграція синтаксису аргументів v1 → v2 (bash) | Human |
| [migrate-arguments-syntax.ps1](./scripts/migrate-arguments-syntax.ps1) | Міграція синтаксису аргументів v1 → v2 (PowerShell) | Human |
| [rtk-benchmark.sh](./scripts/rtk-benchmark.sh) | Бенчмарк економії токенів RTK | Human |
| [sync-claude-config.sh](./scripts/sync-claude-config.sh) | Синхронізація конфігурації Claude між машинами | Human |
| [sonnetplan.sh](./scripts/sonnetplan.sh) | Аліас для запуску Claude із Sonnet замість Opus (оптимізація витрат) | Human |

> **Докладне використання див. у [scripts/README.md](./scripts/README.uk.md)**

### Правила (5)

| Файл | Призначення |
|------|---------|
| [architecture-review.md](./rules/architecture-review.uk.md) | Правила для сесій рев'ю архітектури |
| [code-quality-review.md](./rules/code-quality-review.uk.md) | Правила для сесій рев'ю якості коду |
| [first-principles.md](./rules/first-principles.uk.md) | Правила міркувань від першопринципів |
| [performance-review.md](./rules/performance-review.uk.md) | Правила для сесій рев'ю продуктивності |
| [test-review.md](./rules/test-review.uk.md) | Правила для сесій рев'ю тестів |

### Командна конфігурація (3)

| Файл | Призначення |
|------|---------|
| [claude-skeleton.md](./team-config/claude-skeleton.uk.md) | Мінімальний каркас CLAUDE.md для нових учасників команди |
| [profile-template.yaml](./team-config/profile-template.yaml) | Шаблон збирання профілю для команд із кількома інструментами |
| [sync-script.ts](./team-config/sync-script.ts) | Синхронізація конфігурації Claude між машинами команди |

### Шаблони (1)

| Файл | Призначення |
|------|---------|
| [session-handoff-lorenz.md](./templates/session-handoff-lorenz.uk.md) | Шаблон передачі сесії для безперервності контексту |

### GitHub Actions (6)

| Файл | Тригер | Призначення |
|------|---------|---------|
| [claude-code-review.yml](./github-actions/claude-code-review.yml) ⭐ | Відкриття/синхронізація PR + коментар `/claude-review` | Рев'ю на основі промпту (винесений промпт + протокол проти галюцинацій) |
| [claude-pr-auto-review.yml](./github-actions/claude-pr-auto-review.yml) | Відкриття/оновлення PR | Автоматичне рев'ю коду з інлайн-коментарями |
| [claude-security-review.yml](./github-actions/claude-security-review.yml) | Відкриття/оновлення PR | Сканування з фокусом на безпеці (OWASP) |
| [claude-issue-triage.yml](./github-actions/claude-issue-triage.yml) | Відкриття issue | Автосортування з мітками й рівнем серйозності |

> **Інструкції з налаштування та адаптації див. у [github-actions/README.md](./github-actions/README.uk.md)**

### Воркфлоу (3)

| Файл | Призначення |
|------|---------|
| [database-branch-setup.md](./workflows/database-branch-setup.uk.md) | Ізольована розробка функцій із гілками бази даних (Neon/PlanetScale) |
| [memory-stack-integration.md](./workflows/memory-stack-integration.uk.md) | Багатоденний воркфлоу з інструментами пам'яті (claude-mem + Serena + grepai) |
| [remotion-quickstart.md](./workflows/remotion-quickstart.uk.md) | Воркфлоу генерації відео з Remotion |

### Плагіни (2)

| Файл | Призначення |
|------|---------|
| [se-cove.md](./plugins/se-cove.uk.md) | Chain-of-Verification для незалежного рев'ю коду (Meta AI, ACL 2024) |
| [claude-mem.md](./plugins/claude-mem.uk.md) | Плагін для керування постійною пам'яттю |

### Інтеграції (3)

| Інструмент | Призначення |
|------|---------|
| [Agent Vibes TTS](./integrations/agent-vibes/) | Озвучення відповідей Claude Code (text-to-speech) |

> **Встановлення та каталог голосів див. у [agent-vibes/README.md](./integrations/agent-vibes/README.uk.md)**

### Конфігурації MCP (1)

| Файл | Призначення |
|------|---------|
| [figma.json](./mcp-configs/figma.json) | Конфігурація MCP-сервера Figma |

### Режими (1)

| Файл | Призначення | Активація |
|------|---------|------------|
| [MODE_Learning.md](./modes/MODE_Learning.uk.md) | Пояснення саме тоді, коли вони потрібні | прапорець `--learn` |

> **Встановлення та довідку з фреймворку SuperClaude див. у [modes/README.md](./modes/README.uk.md)**

### Семантичні якорі (1)

| Файл | Призначення |
|------|---------|
| [anchor-catalog.md](./semantic-anchors/anchor-catalog.uk.md) | Дібрані терміни, джерела й межі використання для промптів |

> **Як використовувати семантичні якорі, див. у [Розділі 2.9](../guide/ultimate-guide.uk.md#29-semantic-anchors) посібника**

### Міст між кількома провайдерами

| Інструмент | Призначення |
|------|---------|
| [cc-copilot-bridge](https://github.com/FlorianBruniaux/cc-copilot-bridge) | Міст між GitHub Copilot і Claude Code CLI для доступу за фіксованим тарифом |

> Перенесено в окремий репозиторій: [github.com/FlorianBruniaux/cc-copilot-bridge](https://github.com/FlorianBruniaux/cc-copilot-bridge)

---

*Докладні пояснення див. в [основному посібнику](../guide/ultimate-guide.uk.md), а те, як Claude Code влаштований усередині, в [посібнику з архітектури](../guide/core/architecture.uk.md).*
