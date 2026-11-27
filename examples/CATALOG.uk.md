# Каталог шаблонів

Автогенерований індекс шаблонів із фільтрами за складністю, часом і предметною областю.

**Останнє оновлення**: [генерується автоматично]

---

**Усього шаблонів**: 242

- **Агенти**: 23
- **Команди**: 52
- **Skills**: 121
- **Hooks**: 39
- **Воркфлоу**: 5
- **Скрипти**: 2

## Фільтр за складністю

- **Beginner**: 0 шаблонів
- **Intermediate**: 242 шаблони
- **Advanced**: 0 шаблонів

## Фільтр за часом

- **15 min**: 1 шаблон
- **30 min**: 240 шаблонів
- **varies**: 1 шаблон

---

## За категоріями

### Агенти (23)

- **[adr-writer](agents/adr-writer.uk.md)** *intermediate* • 30 min
  Агент-генератор Architecture Decision Record, лише для читання. Виявляє архітектурні рішення у змінах коду, класифікує їхню критичність і генерує ADR у патерн-орієнтованому форматі Майкла Найгарда (контекст-рішення-наслідки). Ніколи не змінює код. Використовуй після значних змін або коли рішення треба задокументувати.

- **[analytics-agent](agents/analytics-with-eval/analytics-agent.uk.md)** *intermediate* • 30 min
  Генератор SQL-запитів із вбудованим оцінюванням і перевірками безпеки

- **[anomaly-detector](agents/cyber-defense/anomaly-detector.uk.md)** *intermediate* • 30 min
  Виявляє статистичні аномалії та патерни атак у структурованих подіях безпеки. Другий етап конвеєра кіберзахисту: читає cyber-defense-events.json і формує перелік аномалій.

- **[architecture-reviewer](agents/architecture-reviewer.uk.md)** *intermediate* • 30 min
  Агент для рев'ю архітектури та дизайну, лише для читання. Оцінює структурні рішення, виявляє запахи дизайну й позначає ризики до початку реалізації. Ніколи не змінює код. Використовуй перед злиттям архітектурних змін або після того, як planner склав план.

- **[code-reviewer](agents/code-reviewer.uk.md)** *intermediate* • 30 min
  Використовуй для ретельного рев'ю коду з перевірками якості, безпеки та продуктивності

- **[devops-sre](agents/devops-sre.uk.md)** *intermediate* • 30 min
  Діагностика інфраструктури за фреймворком FIRE (First Response, Investigate, Remediate, Evaluate)

- **[implementer](agents/implementer.uk.md)** *intermediate* • 30 min
  Агент механічного виконання для обмежених, чітко визначених завдань. Обсяг і підхід мають бути явно вказані в промпті завдання. Використовуй після того, як planner склав план. Для складної логіки чи проєктних рішень використовуй Sonnet.

- **[integration-reviewer](agents/integration-reviewer.uk.md)** *intermediate* • 30 min
  Валідатор інтеграцій під час виконання, лише для читання. Перевіряє параметри підключення до сервісів, узгодженість async/sync, повноту змінних середовища, коректність API бібліотек і повноту конвеєра OTEL. Запускається під час /plan-validate, коли до обсягу входять нові сервіси, бібліотеки чи конфігурація спостережуваності.

- **[log-ingestor](agents/cyber-defense/log-ingestor.uk.md)** *intermediate* • 30 min
  Розбирає сирі логи на структуровані події безпеки. Перший етап конвеєра кіберзахисту: читає файли логів і витягує типізовані події (помилки, попередження, збої автентифікації, аномалії).

- **[loop-monitor](agents/loop-monitor.uk.md)** *intermediate* • 30 min
  Монітор автономних циклів: виявляє зависання, некероване витрачання токенів і нескінченні цикли в довготривалих сесіях Claude без нагляду. Використовуй разом із процесом-watchdog під час запуску автономних конвеєрів.

- **[output-evaluator](agents/output-evaluator.uk.md)** *intermediate* • 30 min
  Оцінює результати Claude Code на якість перед комітом чи дією (патерн LLM-as-a-Judge)

- **[plan-challenger](agents/plan-challenger.uk.md)** *intermediate* • 30 min
  Агент змагального рев'ю планів, лише для читання. Систематично атакує плани реалізації за 5 вимірами, а потім застосовує спростувальні міркування, щоб відсіяти хибнопозитивні результати. Ніколи не змінює код. Використовуй, перш ніж братися за будь-який значний план реалізації.

- **[planner](agents/planner.uk.md)** *intermediate* • 30 min
  Агент стратегічного планування: дослідження лише для читання перед реалізацією. Використовуй, щоб розкласти завдання на кроки, проаналізувати кодову базу й скласти детальний план. Ніколи не змінює файли.

- **[planning-coordinator](agents/planning-coordinator.uk.md)** *intermediate* • 30 min
  Агент синтезу для динамічних дослідницьких команд, лише для читання. Отримує звіти від усіх спеціалізованих дослідницьких агентів і складає цілісний план реалізації без повторів. Запускається автоматично, коли у фазі 4 /plan-start обрано 2+ агентів.

- **[README](agents/cyber-defense/README.uk.md)** *intermediate* • 30 min
  Конвеєр із 4 агентів, що виявляє загрози безпеці у файлах логів. Побудований нативно на Claude Code Agent

- **[README](agents/analytics-with-eval/README.uk.md)** *intermediate* • 30 min
  Готовий до продакшену аналітичний агент з автоматичним збором метрик і перевіркою безпеки

- **[refactoring-specialist](agents/refactoring-specialist.uk.md)** *intermediate* • 30 min
  Використовуй для рефакторингу в дусі чистого коду за принципами SOLID і найкращими практиками

- **[report-template](agents/analytics-with-eval/eval/report-template.uk.md)** *intermediate* • 30 min
  Щомісячний шаблон оцінювання продуктивності й точності аналітичного агента

- **[risk-classifier](agents/cyber-defense/risk-classifier.uk.md)** *intermediate* • 30 min
  Класифікує загальний рівень ризику на основі виявлених аномалій. Третій етап конвеєра кіберзахисту: читає cyber-defense-anomalies.json і призначає CRITICAL/HIGH/MEDIUM/LOW з обґрунтуванням.

- **[security-auditor](agents/security-auditor.uk.md)** *intermediate* • 30 min
  Використовуй для виявлення вразливостей безпеки та перевірок відповідності OWASP

- **[security-patcher](agents/security-patcher.uk.md)** *intermediate* • 30 min
  Застосовує патчі безпеки на основі знахідок security-auditor. Як вхідні дані потребує звіту аудиту. Завжди пропонує патчі на рев'ю людині, ніколи не застосовує без схвалення.

- **[test-writer](agents/test-writer.uk.md)** *intermediate* • 30 min
  Використовуй для генерації вичерпних тестів за принципами TDD/BDD

- **[threat-reporter](agents/cyber-defense/threat-reporter.uk.md)** *intermediate* • 30 min
  Генерує зрозумілий людині звіт про інцидент безпеки. Фінальний етап конвеєра кіберзахисту: читає всі три JSON-файли й формує Markdown-звіт для команд безпеки.


### Skills (52)

- **[all](commands/ci/all.uk.md)** *intermediate* • 30 min
  Цю команду перенесено в skill у Claude Code 2.1.3. Див.: [`examples/skills/ci-all/SKILL.md`](

- **[alternatives](commands/learn/alternatives.uk.md)** *intermediate* • 30 min
  Цю команду перенесено в skill у Claude Code 2.1.3. Див.: [`examples/skills/learn-alternatives

- **[audit-agents-skills](commands/audit-agents-skills.uk.md)** *intermediate* • 30 min
  Цю команду перенесено в skill у Claude Code 2.1.3. Див.: [`examples/skills/audit-agents-skill

- **[audit-codebase](commands/audit-codebase.uk.md)** *intermediate* • 30 min
  Цю команду перенесено в skill у Claude Code 2.1.3. Див.: [`examples/skills/audit-codebase/SKI

- **[autoresearch](commands/autoresearch.uk.md)** *intermediate* • 30 min
  Цю команду перенесено в skill у Claude Code 2.1.3. Див.: [`examples/skills/autoresearch/SKILL

- **[canary](commands/canary.uk.md)** *intermediate* • 30 min
  Цю команду перенесено в skill у Claude Code 2.1.3. Див.: [`examples/skills/canary/SKILL.md`](

- **[catchup](commands/catchup.uk.md)** *intermediate* • 30 min
  Цю команду перенесено в skill у Claude Code 2.1.3. Див.: [`examples/skills/catchup/SKILL.md`]

- **[check-cache-bugs](commands/check-cache-bugs.uk.md)** *intermediate* • 30 min
  Цю команду перенесено в skill у Claude Code 2.1.3. Див.: [`examples/skills/check-cache-bugs/S

- **[commit](commands/commit.uk.md)** *intermediate* • 30 min
  Цю команду перенесено в skill у Claude Code 2.1.3. Див.: [`examples/skills/commit/SKILL.md`](

- **[create-handoff](commands/handoff/create-handoff.uk.md)** *intermediate* • 30 min
  Цю команду перенесено в skill у Claude Code 2.1.3. Див.: [`examples/skills/handoff-create/SKI

- **[diagnose](commands/diagnose.uk.md)** *intermediate* • 30 min
  Цю команду перенесено в skill у Claude Code 2.1.3. Див.: [`examples/skills/diagnose/SKILL.md`

- **[explain](commands/explain.uk.md)** *intermediate* • 30 min
  Цю команду перенесено в skill у Claude Code 2.1.3. Див.: [`examples/skills/explain/SKILL.md`]

- **[generate-tests](commands/generate-tests.uk.md)** *intermediate* • 30 min
  Цю команду перенесено в skill у Claude Code 2.1.3. Див.: [`examples/skills/generate-tests/SKI

- **[git-worktree](commands/git-worktree.uk.md)** *intermediate* • 30 min
  Цю команду перенесено в skill у Claude Code 2.1.3. Див.: [`examples/skills/git-worktree/SKILL

- **[git-worktree-clean](commands/git-worktree-clean.uk.md)** *intermediate* • 30 min
  Цю команду перенесено в skill у Claude Code 2.1.3. Див.: [`examples/skills/git-worktree-clean

- **[git-worktree-remove](commands/git-worktree-remove.uk.md)** *intermediate* • 30 min
  Цю команду перенесено в skill у Claude Code 2.1.3. Див.: [`examples/skills/git-worktree-remov

- **[git-worktree-status](commands/git-worktree-status.uk.md)** *intermediate* • 30 min
  Цю команду перенесено в skill у Claude Code 2.1.3. Див.: [`examples/skills/git-worktree-statu

- **[investigate](commands/investigate.uk.md)** *intermediate* • 30 min
  Цю команду перенесено в skill у Claude Code 2.1.3. Див.: [`examples/skills/investigate/SKILL.

- **[land-and-deploy](commands/land-and-deploy.uk.md)** *intermediate* • 30 min
  Цю команду перенесено в skill у Claude Code 2.1.3. Див.: [`examples/skills/land-and-deploy/SK

- **[methodology-advisor](commands/methodology-advisor.uk.md)** *intermediate* • 30 min
  Цю команду перенесено в skill у Claude Code 2.1.3. Див.: [`examples/skills/methodology-adviso

- **[optimize](commands/optimize.uk.md)** *intermediate* • 30 min
  Цю команду перенесено в skill у Claude Code 2.1.3. Див.: [`examples/skills/optimize/SKILL.md`

- **[pipeline](commands/ci/pipeline.uk.md)** *intermediate* • 30 min
  Цю команду перенесено в skill у Claude Code 2.1.3. Див.: [`examples/skills/ci-pipeline/SKILL.

- **[plan-ceo-review](commands/plan-ceo-review.uk.md)** *intermediate* • 30 min
  Цю команду перенесено в skill у Claude Code 2.1.3. Див.: [`examples/skills/plan-pipeline/ceo-

- **[plan-eng-review](commands/plan-eng-review.uk.md)** *intermediate* • 30 min
  Цю команду перенесено в skill у Claude Code 2.1.3. Див.: [`examples/skills/plan-pipeline/eng-

- **[plan-execute](commands/plan-execute.uk.md)** *intermediate* • 30 min
  Цю команду перенесено в skill у Claude Code 2.1.3. Див.: [`examples/skills/plan-pipeline/exec

- **[plan-start](commands/plan-start.uk.md)** *intermediate* • 30 min
  Цю команду перенесено в skill у Claude Code 2.1.3. Див.: [`examples/skills/plan-pipeline/star

- **[plan-validate](commands/plan-validate.uk.md)** *intermediate* • 30 min
  Цю команду перенесено в skill у Claude Code 2.1.3. Див.: [`examples/skills/plan-pipeline/vali

- **[pr](commands/pr.uk.md)** *intermediate* • 30 min
  Цю команду перенесено в skill у Claude Code 2.1.3. Див.: [`examples/skills/pr/SKILL.md`](../s

- **[qa](commands/qa.uk.md)** *intermediate* • 30 min
  Цю команду перенесено в skill у Claude Code 2.1.3. Див.: [`examples/skills/qa/SKILL.md`](../s

- **[quiz](commands/learn/quiz.uk.md)** *intermediate* • 30 min
  Цю команду перенесено в skill у Claude Code 2.1.3. Див.: [`examples/skills/learn-quiz/SKILL.m

- **[README](commands/ci/README.uk.md)** *intermediate* • 30 min
  Slash-команди для воркфлоу CI/CD. Автоматично визначають стек (Python/Node/Rust) і підтримують як GitLab CI 

- **[recipe-template](commands/recipe-template.uk.md)** *intermediate* • 30 min
  Цю команду перенесено в skill у Claude Code 2.1.3. Див.: [`examples/skills/recipe-template/SK

- **[refactor](commands/refactor.uk.md)** *intermediate* • 30 min
  Цю команду перенесено в skill у Claude Code 2.1.3. Див.: [`examples/skills/refactor/SKILL.md`

- **[release-notes](commands/release-notes.uk.md)** *intermediate* • 30 min
  Цю команду перенесено в skill у Claude Code 2.1.3. Див.: [`examples/skills/release-notes/SKIL

- **[resume-handoff](commands/handoff/resume-handoff.uk.md)** *intermediate* • 30 min
  Цю команду перенесено в skill у Claude Code 2.1.3. Див.: [`examples/skills/handoff-resume/SKI

- **[review-plan](commands/review-plan.uk.md)** *intermediate* • 30 min
  Цю команду перенесено в skill у Claude Code 2.1.3. Див.: [`examples/skills/review-plan/SKILL.

- **[review-pr](commands/review-pr.uk.md)** *intermediate* • 30 min
  Цю команду перенесено в skill у Claude Code 2.1.3. Див.: [`examples/skills/review-pr/SKILL.md

- **[routines-discover](commands/routines-discover.uk.md)** *intermediate* • 30 min
  Цю команду перенесено в skill у Claude Code 2.1.3. Див.: [`examples/skills/routines-discover/

- **[sandbox-status](commands/sandbox-status.uk.md)** *intermediate* • 30 min
  Цю команду перенесено в skill у Claude Code 2.1.3. Див.: [`examples/skills/sandbox-status/SKI

- **[scaffold](commands/scaffold.uk.md)** *intermediate* • 30 min
  Цю команду перенесено в skill у Claude Code 2.1.3. Див.: [`examples/skills/scaffold/SKILL.md`

- **[security](commands/security.uk.md)** *intermediate* • 30 min
  Цю команду перенесено в skill у Claude Code 2.1.3. Див.: [`examples/skills/security/SKILL.md`

- **[security-audit](commands/security-audit.uk.md)** *intermediate* • 30 min
  Цю команду перенесено в skill у Claude Code 2.1.3. Див.: [`examples/skills/security-audit/SKI

- **[security-check](commands/security-check.uk.md)** *intermediate* • 30 min
  Цю команду перенесено в skill у Claude Code 2.1.3. Див.: [`examples/skills/security-check/SKI

- **[session-save](commands/session-save.uk.md)** *intermediate* • 30 min
  Цю команду перенесено в skill у Claude Code 2.1.3. Див.: [`examples/skills/session-save/SKILL

- **[ship](commands/ship.uk.md)** *intermediate* • 30 min
  Цю команду перенесено в skill у Claude Code 2.1.3. Див.: [`examples/skills/ship/SKILL.md`](..

- **[sonarqube](commands/sonarqube.uk.md)** *intermediate* • 30 min
  Цю команду перенесено в skill у Claude Code 2.1.3. Див.: [`examples/skills/sonarqube/SKILL.md

- **[status](commands/ci/status.uk.md)** *intermediate* • 30 min
  Цю команду перенесено в skill у Claude Code 2.1.3. Див.: [`examples/skills/ci-status/SKILL.md

- **[teach](commands/learn/teach.uk.md)** *intermediate* • 30 min
  Цю команду перенесено в skill у Claude Code 2.1.3. Див.: [`examples/skills/learn-teach/SKILL.

- **[tests](commands/ci/tests.uk.md)** *intermediate* • 30 min
  Цю команду перенесено в skill у Claude Code 2.1.3. Див.: [`examples/skills/ci-tests/SKILL.md`

- **[update-handoff](commands/handoff/update-handoff.uk.md)** *intermediate* • 30 min
  Цю команду перенесено в skill у Claude Code 2.1.3. Див.: [`examples/skills/handoff-update/SKI

- **[update-threat-db](commands/update-threat-db.uk.md)** *intermediate* • 30 min
  Цю команду перенесено в skill у Claude Code 2.1.3. Див.: [`examples/skills/update-threat-db/S

- **[validate-changes](commands/validate-changes.uk.md)** *intermediate* • 30 min
  Цю команду перенесено в skill у Claude Code 2.1.3. Див.: [`examples/skills/validate-changes/S


### Skills (121)

- **[ast-grep-patterns](skills/ast-grep-patterns.uk.md)** *intermediate* • 30 min
  Skill, що вчить Claude, коли і як використовувати ast-grep для структурного пошуку в коді

- **[audit-agents-skills](skills/audit-agents-skills/SKILL.uk.md)** *intermediate* • 30 min
  Аудит агентів, skills і команд Claude Code на якість і готовність до продакшену. Використовуй, щоб оцінити якість skills, перевірити бали готовності до продакшену або порівняти агентів зі зразковими шаблонами.

- **[audit-codebase](skills/audit-codebase/SKILL.uk.md)** *intermediate* • 30 min
  Аудит стану кодової бази з оцінкою за 7 категоріями та планом розвитку

- **[autoresearch](skills/autoresearch/SKILL.uk.md)** *intermediate* • 30 min
  Автономний цикл покращення: сканує метрики кодової бази, створює каркас файлів експерименту, запускає ітерації під керуванням агента, доки метрика не покращиться

- **[before-after](skills/voice-refine/examples/before-after.uk.md)** *intermediate* • 30 min
  Реальні приклади багатослівного голосового введення, перетвореного на структуровані промпти

- **[behavioral](skills/design-patterns/reference/behavioral.uk.md)** *intermediate* • 30 min
  Довідник з Observer, Strategy, Command, Chain of Responsibility та інших поведінкових патернів

- **[best-of-n](skills/best-of-n/SKILL.uk.md)** *intermediate* • 30 min
  Генерує обмежену кількість незалежних кандидатів, оцінює їх за зафіксованою рубрикою й перевіряє обраний результат із журналом доказів.

- **[canary](skills/canary/SKILL.uk.md)** *intermediate* • 30 min
  Моніторинг після розгортання: стежить за продакшеном після деплою й сповіщає про регресії

- **[catchup](skills/catchup/SKILL.uk.md)** *intermediate* • 30 min
  Відновлює контекст після /clear, підсумовуючи нещодавню роботу та стан проєкту

- **[ccboard](skills/ccboard/SKILL.uk.md)** *intermediate* • 30 min
  Запуск і навігація панеллю ccboard TUI/Web для Claude Code. Використовуй для моніторингу використання токенів, відстеження витрат, перегляду сесій або перевірки стану MCP-серверів у різних проєктах.

- **[ccboard-install](skills/ccboard/commands/install.uk.md)** *intermediate* • 30 min
  Встановити або оновити ccboard

- **[ccboard-web](skills/ccboard/commands/web.uk.md)** *intermediate* • 30 min
  Запустити веб-інтерфейс ccboard

- **[changelog-parsing-rules](skills/guide-recap/references/changelog-parsing-rules.uk.md)** *intermediate* • 30 min
  Як витягувати й категоризувати записи з `CHANGELOG.md` для генерації контенту для соцмереж.

- **[changelog-template](skills/release-notes-generator/assets/changelog-template.uk.md)** *intermediate* • 30 min
  Використовуй цей шаблон для генерації записів CHANGELOG.md.

- **[check-cache-bugs](skills/check-cache-bugs/SKILL.uk.md)** *intermediate* • 30 min
  Аудит налаштувань Claude Code на баги кешу (CC#40524): sentinel, --resume/--continue, заголовок атрибуції + ArkNill B3/B4/B5

- **[ci-all](skills/ci-all/SKILL.uk.md)** *intermediate* • 30 min
  Повний конвеєр CI: запускає локальні тести, перевірку типів, пушить гілку й повертає URL конвеєра. Єдина команда, потрібна перед відкриттям PR.

- **[ci-pipeline](skills/ci-pipeline/SKILL.uk.md)** *intermediate* • 30 min
  Пушить поточну гілку й повертає URL для відстеження конвеєра (GitLab або GitHub Actions)

- **[ci-status](skills/ci-status/SKILL.uk.md)** *intermediate* • 30 min
  Показує поточний стан конвеєра для активної гілки (GitLab CI або GitHub Actions)

- **[ci-tests](skills/ci-tests/SKILL.uk.md)** *intermediate* • 30 min
  Запускає набір тестів поточного репозиторію, автоматично визначаючи Python (pytest/uv), Node (vitest/pnpm) або Rust (cargo test)

- **[commit](skills/commit/SKILL.uk.md)** *intermediate* • 30 min
  Генерує повідомлення коміту за Conventional Commits для проіндексованих змін

- **[commit-categories](skills/release-notes-generator/references/commit-categories.uk.md)** *intermediate* • 30 min
  Цей документ визначає, як категоризувати коміти на основі формату Conventional Commits.

- **[content-transformation](skills/guide-recap/references/content-transformation.uk.md)** *intermediate* • 30 min
  Перекладає технічну мову CHANGELOG на цінність для користувачів у соцмережах. Застосовуй правила з tone-guidelines.md до всіх

- **[costs](skills/ccboard/commands/costs.uk.md)** *intermediate* • 30 min
  Відкрити вкладку аналізу витрат ccboard

- **[creational](skills/design-patterns/reference/creational.uk.md)** *intermediate* • 30 min
  Довідник із Singleton, Factory, Builder, Prototype та інших породжувальних патернів

- **[cyber-defense-team](skills/cyber-defense-team/SKILL.uk.md)** *intermediate* • 30 min
  Оркеструє конвеєр кіберзахисту з 4 агентів для аналізу файлів логів на загрози. Використовуй для розслідування логів безпеки, виявлення аномалій у патернах доступу, класифікації серйозності зламу або генерації звітів про інциденти з файлів nginx/auth/syslog.

- **[dashboard](skills/ccboard/commands/dashboard.uk.md)** *intermediate* • 30 min
  Запустити TUI-панель ccboard

- **[design-patterns](skills/design-patterns/SKILL.uk.md)** *intermediate* • 30 min
  Виявляє, пропонує й оцінює патерни проєктування GoF у кодових базах TypeScript/JavaScript. Використовуй під час рефакторингу, застосування патернів singleton/factory/observer/strategy, рев'ю якості патернів або пошуку нативних для стеку альтернатив у React, Angular, NestJS і Vue.

- **[diagnose](skills/diagnose/SKILL.uk.md)** *intermediate* • 30 min
  Інтерактивний помічник з усунення несправностей Claude Code

- **[eval-agents](skills/eval-agents/SKILL.uk.md)** *intermediate* • 30 min
  Аудит власних визначень subagents для Claude Code (.claude/agents/*.md) і Codex (.codex/agents/*.toml): можливість завантаження за нативною схемою, перетин описів, рівень моделі, обсяг інструментів та інструкції, безпечні для headless-режиму. Використовуй під час онбордингу в проєкт з агентами, після додавання чи імпорту агентів або коли батьківський агент делегує не тому агентові.

- **[eval-hooks](skills/eval-hooks/SKILL.uk.md)** *intermediate* • 30 min
  Аудит hooks Claude Code і Codex на валідність, безпеку й коректність у settings.json, hooks.json, config.toml, плагінах і hooks у frontmatter skills чи агентів. Розв'язує кожну команду, перевіряє назви подій, типи обробників, matchers, стратегію кодів виходу та JSON-рішень і тайм-аути за задокументованими правилами кожного хоста, а потім переглядає hooks по одному. Використовуй під час налаштування hooks, налагодження hook, який ніколи не спрацьовує, ніколи не блокує або підвішує агента, чи для періодичної ревізії hooks. Не для написання нового hook з нуля.

- **[eval-rules](skills/eval-rules/SKILL.uk.md)** *intermediate* • 30 min
  Аудит правил-інструкцій Claude Code у .claude/rules/ і ~/.claude/rules/: frontmatter, валідність glob-шаблонів paths проти реальних файлів, статус завантаження symlink і щоденна корисність, а потім оновлення правил разом із користувачем. Використовуй для першого налаштування правил, для правил, що застосовуються надто часто чи ніколи, або для періодичної ревізії правил. Не для файлів схвалення команд Codex .rules.

- **[eval-skills](skills/eval-skills/SKILL.uk.md)** *intermediate* • 30 min
  Аудит проєкту чи бібліотеки skills: метадані, межі спрацьовування, критерії завершення воркфлоу, замкненість локальних ресурсів, економність інструкцій, обсяг інструментів, зусилля та докази маршрутизації. Використовуй перед випуском skills, після імпорту колекції skills або коли skill спрацьовує надто часто чи взагалі не спрацьовує.

- **[explain](skills/explain/SKILL.uk.md)** *intermediate* • 30 min
  Пояснює код, концепції чи поведінку системи з налаштовуваними рівнями глибини

- **[feedback-draft](skills/talk-pipeline/stage-4-position/templates/feedback-draft.uk.md)** *intermediate* • 30 min
  Використання: надішли 1-2 довіреним колегам ДО подання CFP чи завершення сценарію.

- **[generate-tests](skills/generate-tests/SKILL.uk.md)** *intermediate* • 30 min
  Генерує вичерпні тести для вказаного коду

- **[git-ai-archaeology](skills/git-ai-archaeology/SKILL.uk.md)** *intermediate* • 30 min
  Аналізує еволюцію AI-конфігурацій у git-репозиторії. Використовуй, щоб відтворити історію впровадження AI, знайти, коли конфігурації вперше з'явилися, побудувати графік швидкості комітів за місяцями або визначити фази зрілості AI-інструментів проєкту.

- **[git-worktree](skills/git-worktree/SKILL.uk.md)** *intermediate* • 30 min
  Створює ізольовані git worktrees для розробки функцій без перемикання гілок

- **[git-worktree-clean](skills/git-worktree-clean/SKILL.uk.md)** *intermediate* • 30 min
  Очищає застарілі git worktrees з виявленням злитих гілок і звітом про використання диска

- **[git-worktree-remove](skills/git-worktree-remove/SKILL.uk.md)** *intermediate* • 30 min
  Безпечно видаляє git worktree з очищенням гілки та перевірками безпеки

- **[git-worktree-status](skills/git-worktree-status/SKILL.uk.md)** *intermediate* • 30 min
  Перевіряє стан фонових завдань верифікації, що виконуються в git worktree

- **[guide-recap](skills/guide-recap/SKILL.uk.md)** *intermediate* • 30 min
  Перетворює записи CHANGELOG на контент для соцмереж (LinkedIn, Twitter/X, Newsletter, Slack) французькою та англійською. Використовуй після релізів або щотижня, щоб генерувати release notes, анонси, дописи в соцмережах чи підсумки оновлень посібника.

- **[handoff-create](skills/handoff-create/SKILL.uk.md)** *intermediate* • 30 min
  Генерує структурований документ передачі з поточної сесії. Фіксує обсяг, релевантні файли з номерами рядків, ключові відкриття, виконану роботу, поточний стан, наступні кроки й фрагменти коду. Використовуй перед завершенням сесії або передачею роботи іншому агентові.

- **[handoff-resume](skills/handoff-resume/SKILL.uk.md)** *intermediate* • 30 min
  Завантажує документ передачі й відновлює роботу з місця, де зупинилася попередня сесія. Розбирає обсяг, посилання на файли, виконану роботу й наступні кроки, а потім підтверджує розуміння, перш ніж продовжити.

- **[handoff-update](skills/handoff-update/SKILL.uk.md)** *intermediate* • 30 min
  Оновлює наявний документ передачі прогресом поточної сесії. Застосовує правила злиття для окремих розділів: лише дописування для Work Done (історія ніколи не видаляється), заміна для Status і Next Steps, злиття для Files і Discoveries. Якщо вихідний файл не знайдено, створює новий документ передачі.

- **[investigate](skills/investigate/SKILL.uk.md)** *intermediate* • 30 min
  Систематичне налагодження з пошуком першопричини: знайди причину, перш ніж писати будь-яке виправлення

- **[issue-comment](skills/issue-triage/templates/issue-comment.uk.md)** *intermediate* • 30 min
  Використовуй ці шаблони для генерації коментарів до GitHub issues під час фази 3 `/issue-triage`. Коментарі p

- **[issue-triage](skills/issue-triage/SKILL.uk.md)** *intermediate* • 30 min
  Керування беклогом issues у 3 фази з аудитом, глибоким аналізом і перевіреними діями сортування. Використовуй для сортування GitHub issues, впорядкування баг-репортів, очищення застарілих тікетів або виявлення дублікатів. Аргументи: 'all' для аналізу всіх, номери issues для фокусу (наприклад, '42 57'), 'en'/'fr' для мови, без аргументу = лише аудит.

- **[kimi-prompt-template](skills/talk-pipeline/stage-5-script/templates/kimi-prompt-template.uk.md)** *intermediate* • 30 min
  > Скопіюй увесь цей промпт у Kimi.com, щоб згенерувати презентацію.

- **[land-and-deploy](skills/land-and-deploy/SKILL.uk.md)** *intermediate* • 30 min
  Зливає PR, чекає на CI, перевіряє деплой, запускає canary. Повний конвеєр приземлення змін.

- **[landing-page-generator](skills/landing-page-generator/SKILL.uk.md)** *intermediate* • 30 min
  Генерує повні, готові до розгортання лендинги з будь-якого репозиторію. Використовуй, щоб створити домашню сторінку для open-source проєкту, зробити сайт проєкту, перетворити README на маркетингову сторінку або уніфікувати лендинги кількох репозиторіїв.

- **[landing-pattern](skills/landing-page-generator/references/landing-pattern.uk.md)** *intermediate* • 30 min
  Документація усталеного патерну лендингу, що використовується в `claude-code-ultimate-guide-landing` a

- **[learn-alternatives](skills/learn-alternatives/SKILL.uk.md)** *intermediate* • 30 min
  Порівнює різні підходи до розв'язання тієї самої задачі

- **[learn-quiz](skills/learn-quiz/SKILL.uk.md)** *intermediate* • 30 min
  Перевіряє розуміння нещодавно написаного чи прийнятого коду

- **[learn-teach](skills/learn-teach/SKILL.uk.md)** *intermediate* • 30 min
  Покрокове пояснення концепції з поступовим поглибленням

- **[learning-path](skills/learning-path/SKILL.uk.md)** *intermediate* • 30 min
  Проходить локальний навчальний маршрут Claude Code, записує докази й планує повторення на основі доказів.

- **[linkedin-template](skills/guide-recap/assets/linkedin-template.uk.md)** *intermediate* • 30 min
  Ціль: ~1300 символів. Структура: гачок + контекст + пункти + CTA + хештеги.

- **[mcp-integration-reference](skills/mcp-integration-reference/SKILL.uk.md)** *intermediate* • 30 min
  Шаблон для skills, що інтегруються з MCP-сервером. Демонструє патерн довідкового файлу: Claude читає шпаргалку MCP для конкретної предметної області перед будь-якими викликами інструментів, зменшуючи кількість невдалих запитів через особливості конкретного сервера. Зроби форк цього skill і заміни приклад Sentry на свій цільовий MCP.

- **[mcp-status](skills/ccboard/commands/mcp-status.uk.md)** *intermediate* • 30 min
  Відкрити вкладку MCP-серверів ccboard

- **[methodology-advisor](skills/methodology-advisor/SKILL.uk.md)** *intermediate* • 30 min
  Аналізує твою кодову базу й ставить 3 цільові питання, щоб порекомендувати правильний стек методологій розробки з допомогою AI

- **[newsletter-template](skills/guide-recap/assets/newsletter-template.uk.md)** *intermediate* • 30 min
  Ціль: ~500 слів. Структуровані розділи з глибиною.

- **[optimize](skills/optimize/SKILL.uk.md)** *intermediate* • 30 min
  Аналізує й пропонує покращення продуктивності для коду, запитів чи систем

- **[pattern-evaluation](skills/design-patterns/checklists/pattern-evaluation.uk.md)** *intermediate* • 30 min
  Систематичні критерії оцінювання якості реалізації патернів проєктування

- **[pdf-generator](skills/pdf-generator.uk.md)** *intermediate* • 30 min
  Генерує професійні PDF на стеку Quarto/Typst із сучасним шаблоном дизайну

- **[plan-pipeline](skills/plan-pipeline/SKILL.uk.md)** *intermediate* • 30 min
  Оркеструє повний конвеєр планування: продуктовий напрям (ceo-review) -> архітектура (eng-review) -> план реалізації (start) -> перевірка (validate) -> виконання (execute). Запускай етапи окремо або дозволь оркестратору координувати весь потік.

- **[plan-pipeline-ceo-review](skills/plan-pipeline/ceo-review/SKILL.uk.md)** *intermediate* • 30 min
  Стратегічний продуктовий рубіж: оскарж бриф, знайди 10-зірковий продукт, захований у запиті, перш ніж писати будь-який код

- **[plan-pipeline-eng-review](skills/plan-pipeline/eng-review/SKILL.uk.md)** *intermediate* • 30 min
  Інженерний архітектурний рубіж: зафіксуй архітектуру, діаграми, граничні випадки й тестову матрицю, перш ніж писати код реалізації

- **[plan-pipeline-execute](skills/plan-pipeline/execute/SKILL.uk.md)** *intermediate* • 30 min
  Виконує затверджений план: ізоляція в worktree, каркас TDD, паралельні агенти за рівнями, контроль якості зі smoke-тестом, створення й злиття PR. Доводить усе до злитого PR.

- **[plan-pipeline-start](skills/plan-pipeline/start/SKILL.uk.md)** *intermediate* • 30 min
  Планування в 5 фаз: аналіз PRD, рев'ю дизайну, технічні рішення, динамічна дослідницька команда, метрики. Створює повний план реалізації + ADR до написання будь-якого коду.

- **[plan-pipeline-validate](skills/plan-pipeline/validate/SKILL.uk.md)** *intermediate* • 30 min
  Перевірка плану у 2 рівні: миттєві структурні перевірки + спеціалізовані агенти, що запускаються за тригерами. Автоматично виправляє проблеми з опорою на ADR і першопринципи. Кожну проблему треба розв'язати до виконання.

- **[pr](skills/pr/SKILL.uk.md)** *intermediate* • 30 min
  Аналізує зміни, виявляє проблеми з обсягом і створює добре структурований PR

- **[pr-triage](skills/pr-triage/SKILL.uk.md)** *intermediate* • 30 min
  Керування беклогом PR у 4 фази з аудитом, глибоким рев'ю коду, перевіреними коментарями й необов'язковим налаштуванням worktree. Використовуй для сортування pull requests, надолуження відкладених рев'ю коду або керування беклогом відкритих PR. Аргументи: 'all' для рев'ю всіх, номери PR для фокусу (наприклад, '42 57'), 'en'/'fr' для мови, без аргументу = лише аудит.

- **[qa](skills/qa/SKILL.uk.md)** *intermediate* • 30 min
  Систематичне QA-тестування вебзастосунку: з урахуванням diff, за рівнями, із циклом «виправити й перевірити»

- **[README](skills/learning-path/README.uk.md)** *intermediate* • 30 min
  Цей прототип без залежностей перетворює наявний [навчальний маршрут із семи модулів](../../../guide/learni

- **[README](skills/ccboard/README.uk.md)** *intermediate* • 30 min
  > Всеосяжна TUI/Web-панель для моніторингу й керування Claude Code

- **[README](skills/talk-pipeline/README.uk.md)** *intermediate* • 30 min
  Конвеєр skills із 6 етапів, що перетворює сирий матеріал (статтю, транскрипт, нотатки) на повний con

- **[README](skills/release-notes-generator/references/README.uk.md)** *intermediate* • 30 min
  Цей каталог містить документацію, яка завантажуватиметься контекстно під час виконання skill.

- **[README](skills/release-notes-generator/scripts/README.uk.md)** *intermediate* • 30 min
  Цей каталог містить виконувані скрипти для детермінованих, повторюваних завдань.

- **[README](skills/release-notes-generator/assets/README.uk.md)** *intermediate* • 30 min
  Цей каталог містить шаблони, зображення та шаблонний код.

- **[recipe-template](skills/recipe-template/SKILL.uk.md)** *intermediate* • 30 min
  Шаблон для команд, що реалізують структурований рецепт: перевір передумови, потім виконай пронумеровані кроки. Зроби форк і заміни вміст-заповнювач. Ключовий патерн тут розділ 'Context Validation Checkpoints', що змушує Claude перевіряти передумови перед початком.

- **[refactor](skills/refactor/SKILL.uk.md)** *intermediate* • 30 min
  Аналізує код на порушення SOLID і пропонує цільові покращення

- **[release-notes](skills/release-notes/SKILL.uk.md)** *intermediate* • 30 min
  Генерує release notes у кількох форматах із git-комітів

- **[release-notes-generator](skills/release-notes-generator/SKILL.uk.md)** *intermediate* • 30 min
  Генерує release notes у 3 форматах (CHANGELOG.md, опис PR, анонс у Slack) із git-комітів. Автоматично категоризує зміни й перетворює технічну мову на зрозумілі користувачам повідомлення. Використовуй для релізів, changelog, нотаток до версій, підсумків «що нового» чи анонсів випуску.

- **[review-comment](skills/pr-triage/templates/review-comment.uk.md)** *intermediate* • 30 min
  Використовуй цей шаблон для генерації коментарів рев'ю до GitHub PR. Заповни кожен розділ на основі code-revi

- **[review-plan](skills/review-plan/SKILL.uk.md)** *intermediate* • 30 min
  Структуроване рев'ю плану за 4 осями перед написанням будь-якого коду (натхненне воркфлоу Гаррі Тана)

- **[review-pr](skills/review-pr/SKILL.uk.md)** *intermediate* • 30 min
  Проводить всебічне рев'ю коду pull request

- **[routines-discover](skills/routines-discover/SKILL.uk.md)** *intermediate* • 30 min
  Аналізує поточний проєкт, щоб виявити найцінніші сценарії використання Routines для трьох типів тригерів (розклад, API, події GitHub). Використання: /routines-discover

- **[rtk-optimizer](skills/rtk-optimizer/SKILL.uk.md)** *intermediate* • 30 min
  Обгортає багатослівні shell-команди в RTK, щоб зменшити споживання токенів. Використовуй під час запуску git log, git diff, cargo test, pytest чи інших CLI-команд із багатослівним виводом, що марнують токени контекстного вікна.

- **[sandbox-status](skills/sandbox-status/SKILL.uk.md)** *intermediate* • 30 min
  Показує стан нативного sandbox, конфігурацію й нещодавні порушення

- **[sandbox-unblock](skills/sandbox-unblock/SKILL.uk.md)** *intermediate* • 30 min
  Діагностичний протокол, який слід виконати, перш ніж повідомляти про блокер sandbox або просити змінити конфігурацію. Вісім перевірок, що відсіюють хибнопозитивні результати, а потім шаблон звіту, за яким може діяти людина, що керує налаштуваннями. За один виміряний день шість із восьми повідомлених блокерів виявилися хибними, і всі через ту саму жменьку методологічних помилок.


- **[scaffold](skills/scaffold/SKILL.uk.md)** *intermediate* • 30 min
  Інтерактивний коуч, що ставить 4-5 питань, щоб визначити, чи потрібен тобі агент, команда, skill, hook чи правило, а потім генерує готовий до використання шаблон. Використання: /scaffold (аргументи не потрібні, запускає сесію коучингу)

- **[security](skills/security/SKILL.uk.md)** *intermediate* • 30 min
  Швидка оцінка безпеки з фокусом на вразливостях OWASP Top 10

- **[security-audit](skills/security-audit/SKILL.uk.md)** *intermediate* • 30 min
  Всебічний аудит безпеки з оцінкою стану захищеності в балах

- **[security-check](skills/security-check/SKILL.uk.md)** *intermediate* • 30 min
  Швидка перевірка безпеки конфігурації за базою відомих загроз

- **[security-checklist](skills/security-checklist.uk.md)** *intermediate* • 30 min
  Всебічний чекліст безпеки для вебзастосунків

- **[sentry-mcp](skills/mcp-integration-reference/references/sentry-mcp.uk.md)** *intermediate* • 30 min
  Довідковий файл для MCP-сервера Sentry. Прочитай його перед будь-якими викликами Sentry MCP. Він містить 

- **[session-save](skills/session-save/SKILL.uk.md)** *intermediate* • 30 min
  Зберігає стан поточної сесії (рішення, змінені файли, поточний стан і наступні кроки) у файл передачі для подальшого відновлення.

- **[sessions](skills/ccboard/commands/sessions.uk.md)** *intermediate* • 30 min
  Перегляд історії сесій Claude Code

- **[ship](skills/ship/SKILL.uk.md)** *intermediate* • 30 min
  Всебічна перевірка перед розгортанням, що гарантує готовність до релізу

- **[skill-creator](skills/skill-creator/SKILL.uk.md)** *intermediate* • 30 min
  Створює каркас нового skill Claude Code із SKILL.md, frontmatter і вкладеними ресурсами. Використовуй, щоб створити власний skill, уніфікувати структуру skills у команді або запакувати skill для поширення.

- **[slack-template](skills/guide-recap/assets/slack-template.uk.md)** *intermediate* • 30 min
  Компактно, легко проглядається, багато емодзі. Готово до вставлення.

- **[slack-template](skills/release-notes-generator/assets/slack-template.uk.md)** *intermediate* • 30 min
  Використовуй цей шаблон для генерації повідомлень у Slack з фокусом на продукті.

- **[smart-explore](skills/smart-explore.uk.md)** *intermediate* • 30 min
  Поступове дослідження коду через AST tree-sitter: спершу структура, потім деталі. Зменшує читання коду з 10-15k токенів на файл до 200-500 токенів.

- **[sonarqube](skills/sonarqube/SKILL.uk.md)** *intermediate* • 30 min
  Аналізує проблеми якості SonarCloud для конкретного PR

- **[structural](skills/design-patterns/reference/structural.uk.md)** *intermediate* • 30 min
  Довідник з Adapter, Decorator, Facade, Proxy та інших структурних патернів

- **[talk-pipeline](skills/talk-pipeline/orchestrator/SKILL.uk.md)** *intermediate* • 30 min
  Оркеструє повний конвеєр підготовки виступу від сирого матеріалу до шпаргалок для повторення, послідовно виконуючи 6 етапів із контрольними точками за участі людини для виступів у режимі REX або Concept. Використовуй, щоб розпочати новий конвеєр виступу, відновити конвеєр з певного етапу або пройти повний наскрізний воркфлоу підготовки.

- **[talk-stage1-extract](skills/talk-pipeline/stage-1-extract/SKILL.uk.md)** *intermediate* • 30 min
  Витягує й структурує вихідний матеріал (статті, транскрипти, нотатки) у підсумок виступу з наративною аркою, темами, метриками й прогалинами. Автоматично визначає тип REX чи Concept. Використовуй, щоб розпочати новий виступ із будь-якого вихідного матеріалу або перевірити наявний матеріал, перш ніж братися за виступ.

- **[talk-stage2-research](skills/talk-pipeline/stage-2-research/SKILL.uk.md)** *intermediate* • 30 min
  Проводить git-археологію, аналіз changelog і будує перевірену фактичну хронологію, зіставляючи git-історію з вихідним матеріалом. Лише режим REX (у режимі Concept пропускається автоматично). Використовуй, коли готуєш REX-виступ і потрібні перевірені метрики комітів, хронологія релізів і дані про контриб'юторів із git-репозиторію.

- **[talk-stage3-concepts](skills/talk-pipeline/stage-3-concepts/SKILL.uk.md)** *intermediate* • 30 min
  Будує пронумерований, категоризований каталог концепцій на основі підсумку виступу та хронології, оцінюючи потенціал кожної концепції для виступу як HIGH / MEDIUM / LOW, з необов'язковим збагаченням даними з репозиторію. Використовуй, коли потрібен структурований перелік концепцій перед вибором ракурсу виступу або коли треба оцінити, які ідеї мають найсильніший потенціал для презентації.

- **[talk-stage4-position](skills/talk-pipeline/stage-4-position/SKILL.uk.md)** *intermediate* • 30 min
  Генерує 3-4 стратегічні ракурси виступу з аналізом сильних і слабких сторін, варіантами назв, описами для CFP і чернеткою запиту на відгук колег, а потім вимагає обов'язкової CHECKPOINT для підтвердження користувачем перед написанням сценарію. Використовуй, коли вирішуєш, як подати виступ, готуєш заявку на CFP або обираєш між кількома наративними ракурсами.

- **[talk-stage5-script](skills/talk-pipeline/stage-5-script/SKILL.uk.md)** *intermediate* • 30 min
  Створює повний пітч у 5 актах із нотатками доповідача, специфікацією кожного слайда й готовим до вставлення промптом для Kimi для генерації слайдів за допомогою AI. Потребує затверджених ракурсу й назви з етапу 4. Використовуй, коли маєш підтверджений ракурс виступу й потрібні повний сценарій, специфікація слайдів і промпт для генерації презентації за допомогою AI.

- **[talk-stage6-revision](skills/talk-pipeline/stage-6-revision/SKILL.uk.md)** *intermediate* • 30 min
  Створює шпаргалки для повторення зі швидкою навігацією за актами, головною таблицею «концепція-URL», шпаргалкою Q&A із 6-10 очікуваними питаннями, глосарієм і переліком зовнішніх ресурсів. Використовуй, коли готуєшся до виступу з Q&A, створюєш довідкові матеріали для учасників або складаєш страхувальний глосарій для живого виступу.

- **[tdd-workflow](skills/tdd-workflow.uk.md)** *intermediate* • 30 min
  Воркфлоу та найкращі практики Test-Driven Development

- **[tech-to-product-mappings](skills/release-notes-generator/references/tech-to-product-mappings.uk.md)** *intermediate* • 30 min
  Цей документ визначає, як перетворювати технічні повідомлення комітів на зрозумілу користувачам продуктову мову

- **[token-audit](skills/token-audit/skill.uk.md)** *intermediate* • 30 min
  Аудит конфігурації Claude Code для вимірювання накладних витрат токенів фіксованого контексту та складання пріоритезованого плану дій. Використовуй, коли впираєшся в ліміти частоти, стикаєшся з раннім стисненням контексту або після додавання значних конфігураційних файлів.

- **[tone-guidelines](skills/guide-recap/references/tone-guidelines.uk.md)** *intermediate* • 30 min
  Правила для контенту в соцмережах, згенерованого із записів CHANGELOG. Центральний принцип: **залучення через v

- **[twitter-template](skills/guide-recap/assets/twitter-template.uk.md)** *intermediate* • 30 min
  Два режими: один твіт (280 символів) або тред (2-3 твіти).

- **[update-threat-db](skills/update-threat-db/SKILL.uk.md)** *intermediate* • 30 min
  Делегує дослідження й оновлення розвідданих про загрози AgentSec, а потім перевіряє посібник і дзеркала лендингу.

- **[validate-changes](skills/validate-changes/SKILL.uk.md)** *intermediate* • 30 min
  Оцінює проіндексовані зміни за патерном LLM-as-a-Judge перед комітом

- **[version-output](skills/guide-recap/examples/version-output.uk.md)** *intermediate* • 30 min
  Вхід: `/guide-recap v3.20.5`

- **[voice-refine](skills/voice-refine/SKILL.uk.md)** *intermediate* • 30 min
  Перетворює багатослівне голосове введення на структуровані, економні щодо токенів промпти для Claude. Використовуй для очищення голосових нотаток, результатів диктування чи транскрипцій speech-to-text, що містять слова-паразити, повтори й неструктуровані думки.

- **[week-output](skills/guide-recap/examples/week-output.uk.md)** *intermediate* • 30 min
  Вхід: `/guide-recap week 2026-01-27`


### Hooks (39)

- **[auto-checkpoint](hooks/bash/auto-checkpoint.sh)** *intermediate* • 30 min
  set -euo pipefail

- **[auto-format](hooks/bash/auto-format.sh)** *intermediate* • 30 min
  INPUT=$(cat)

- **[auto-format](hooks/powershell/auto-format.ps1)** *intermediate* • 30 min
  $inputJson = [Console]::In.ReadToEnd() | ConvertFrom-Json

- **[auto-rename-session](hooks/bash/auto-rename-session.sh)** *intermediate* • 30 min
  set -uo pipefail

- **[claudemd-scanner](hooks/bash/claudemd-scanner.sh)** *intermediate* • 30 min
  set -euo pipefail

- **[dangerous-actions-blocker](hooks/bash/dangerous-actions-blocker.sh)** *intermediate* • 30 min
  set -euo pipefail

- **[file-guard](hooks/bash/file-guard.sh)** *intermediate* • 30 min
  set -euo pipefail

- **[governance-enforcement-hook](hooks/bash/governance-enforcement-hook.sh)** *intermediate* • 30 min
  set -euo pipefail

- **[identity-reinjection](hooks/bash/identity-reinjection.sh)** *intermediate* • 30 min
  set -uo pipefail

- **[learning-capture](hooks/bash/learning-capture.sh)** *intermediate* • 30 min
  set -e

- **[mcp-config-integrity](hooks/bash/mcp-config-integrity.sh)** *intermediate* • 30 min
  set -euo pipefail

- **[notification](hooks/bash/notification.sh)** *intermediate* • 30 min
  set -e

- **[output-secrets-scanner](hooks/bash/output-secrets-scanner.sh)** *intermediate* • 30 min
  set -euo pipefail

- **[output-validator](hooks/bash/output-validator.sh)** *intermediate* • 30 min
  set -e

- **[permission-request](hooks/bash/permission-request.sh)** *intermediate* • 30 min
  INPUT=$(cat)

- **[pre-commit-evaluator](hooks/bash/pre-commit-evaluator.sh)** *intermediate* • 30 min
  set -e

- **[pre-commit-secrets](hooks/bash/pre-commit-secrets.sh)** *intermediate* • 30 min
  set -euo pipefail

- **[privacy-warning](hooks/bash/privacy-warning.sh)** *intermediate* • 30 min
  if [[ -n "$PRIVACY_WARNING_SHOWN" ]]; then

- **[prompt-injection-detector](hooks/bash/prompt-injection-detector.sh)** *intermediate* • 30 min
  set -e

- **[repo-integrity-scanner](hooks/bash/repo-integrity-scanner.sh)** *intermediate* • 30 min
  set -euo pipefail

- **[rtk-auto-wrapper](hooks/bash/rtk-auto-wrapper.sh)** *intermediate* • 30 min
  if ! command -v rtk &> /dev/null; then

- **[rtk-baseline](hooks/bash/rtk-baseline.sh)** *intermediate* • 30 min
  set -euo pipefail

- **[sandbox-validation](hooks/bash/sandbox-validation.sh)** *intermediate* • 30 min
  set -euo pipefail

- **[security-check](hooks/bash/security-check.sh)** *intermediate* • 30 min
  INPUT=$(cat)

- **[security-check](hooks/powershell/security-check.ps1)** *intermediate* • 30 min
  $inputJson = [Console]::In.ReadToEnd() | ConvertFrom-Json

- **[security-gate](hooks/bash/security-gate.sh)** *intermediate* • 30 min
  set -e

- **[session-logger](hooks/bash/session-logger.sh)** *intermediate* • 30 min
  set -e

- **[session-summary](hooks/bash/session-summary.sh)** *intermediate* • 30 min
  set -euo pipefail

- **[session-summary-config](hooks/bash/session-summary-config.sh)** *intermediate* • 30 min
  set -euo pipefail

- **[setup-init](hooks/bash/setup-init.sh)** *intermediate* • 30 min
  INPUT=$(cat)

- **[smart-suggest](hooks/bash/smart-suggest.sh)** *intermediate* • 30 min
  set -euo pipefail

- **[subagent-stop](hooks/bash/subagent-stop.sh)** *intermediate* • 30 min
  INPUT=$(cat)

- **[test-hooks](hooks/bash/test-hooks.sh)** *intermediate* • 30 min
  set -euo pipefail

- **[test-on-change](hooks/bash/test-on-change.sh)** *intermediate* • 30 min
  set -euo pipefail

- **[tts-selective](hooks/bash/tts-selective.sh)** *intermediate* • 30 min
  set -e

- **[typecheck-on-save](hooks/bash/typecheck-on-save.sh)** *intermediate* • 30 min
  set -euo pipefail

- **[unicode-injection-scanner](hooks/bash/unicode-injection-scanner.sh)** *intermediate* • 30 min
  set -euo pipefail

- **[velocity-governor](hooks/bash/velocity-governor.sh)** *intermediate* • 30 min
  set -euo pipefail

- **[verification-gate](hooks/bash/verification-gate.sh)** *intermediate* • 30 min
  set -euo pipefail


### Воркфлоу (5)

- **[bounded-loop-contract](workflows/bounded-loop-contract.uk.md)** *intermediate* • 15 min • architecture
  Довідковий контракт для обмеженого циклу агента з окремим інтерфейсом верифікатора, доказами й ескалацією
  *Prerequisites*: Python 3.10+

- **[database-branch-setup](workflows/database-branch-setup.uk.md)** *intermediate* • 30 min
  Посібник з ізольованої розробки функцій із використанням гілок бази даних у Neon або PlanetScale

- **[memory-stack-integration](workflows/memory-stack-integration.uk.md)** *intermediate* • 30 min
  Приклад 5-денного спринту, що поєднує claude-mem, Serena, grepai і rg для рефакторингу автентифікації

- **[remotion-quickstart](workflows/remotion-quickstart.uk.md)** *intermediate* • 30 min
  15-хвилинний швидкий старт зі створення програмних відео за допомогою Remotion і Claude Code

- **[review-admission](workflows/review-admission.uk.md)** *intermediate* • varies • testing • ⚠️ experimental
  Визначає спільну пропускну здатність рев'ю, правила призупинення й відновлення та настільну вправу


### Скрипти (2)

- **[ai-usage-charter-template](scripts/ai-usage-charter-template.uk.md)** *intermediate* • 30 min
  > **Шаблон**: скопіюй у `docs/ai-usage-charter.md` у репозиторії документації своєї організації.

- **[README](scripts/README.uk.md)** *intermediate* • 30 min
  Допоміжні скрипти для досвідчених користувачів Claude Code: аудити, перевірки стану й керування сесіями


---

## За предметною областю

### Архітектура (1)

- **bounded-loop-contract** (intermediate, 15 min)

### Загальне (240)

- **README** (intermediate, 30 min)
- **README** (intermediate, 30 min)
- **README** (intermediate, 30 min)
- **README** (intermediate, 30 min)
- **README** (intermediate, 30 min)
- **README** (intermediate, 30 min)
- **README** (intermediate, 30 min)
- **README** (intermediate, 30 min)
- **README** (intermediate, 30 min)
- **README** (intermediate, 30 min)
- **adr-writer** (intermediate, 30 min)
- **ai-usage-charter-template** (intermediate, 30 min)
- **all** (intermediate, 30 min)
- **alternatives** (intermediate, 30 min)
- **analytics-agent** (intermediate, 30 min)
- **anomaly-detector** (intermediate, 30 min)
- **architecture-reviewer** (intermediate, 30 min)
- **ast-grep-patterns** (intermediate, 30 min)
- **audit-agents-skills** (intermediate, 30 min)
- **audit-agents-skills** (intermediate, 30 min)
- **audit-codebase** (intermediate, 30 min)
- **audit-codebase** (intermediate, 30 min)
- **auto-checkpoint** (intermediate, 30 min)
- **auto-format** (intermediate, 30 min)
- **auto-format** (intermediate, 30 min)
- **auto-rename-session** (intermediate, 30 min)
- **autoresearch** (intermediate, 30 min)
- **autoresearch** (intermediate, 30 min)
- **before-after** (intermediate, 30 min)
- **behavioral** (intermediate, 30 min)
- **best-of-n** (intermediate, 30 min)
- **canary** (intermediate, 30 min)
- **canary** (intermediate, 30 min)
- **catchup** (intermediate, 30 min)
- **catchup** (intermediate, 30 min)
- **ccboard** (intermediate, 30 min)
- **ccboard-install** (intermediate, 30 min)
- **ccboard-web** (intermediate, 30 min)
- **changelog-parsing-rules** (intermediate, 30 min)
- **changelog-template** (intermediate, 30 min)
- **check-cache-bugs** (intermediate, 30 min)
- **check-cache-bugs** (intermediate, 30 min)
- **ci-all** (intermediate, 30 min)
- **ci-pipeline** (intermediate, 30 min)
- **ci-status** (intermediate, 30 min)
- **ci-tests** (intermediate, 30 min)
- **claudemd-scanner** (intermediate, 30 min)
- **code-reviewer** (intermediate, 30 min)
- **commit** (intermediate, 30 min)
- **commit** (intermediate, 30 min)
- **commit-categories** (intermediate, 30 min)
- **content-transformation** (intermediate, 30 min)
- **costs** (intermediate, 30 min)
- **create-handoff** (intermediate, 30 min)
- **creational** (intermediate, 30 min)
- **cyber-defense-team** (intermediate, 30 min)
- **dangerous-actions-blocker** (intermediate, 30 min)
- **dashboard** (intermediate, 30 min)
- **database-branch-setup** (intermediate, 30 min)
- **design-patterns** (intermediate, 30 min)
- **devops-sre** (intermediate, 30 min)
- **diagnose** (intermediate, 30 min)
- **diagnose** (intermediate, 30 min)
- **eval-agents** (intermediate, 30 min)
- **eval-hooks** (intermediate, 30 min)
- **eval-rules** (intermediate, 30 min)
- **eval-skills** (intermediate, 30 min)
- **explain** (intermediate, 30 min)
- **explain** (intermediate, 30 min)
- **feedback-draft** (intermediate, 30 min)
- **file-guard** (intermediate, 30 min)
- **generate-tests** (intermediate, 30 min)
- **generate-tests** (intermediate, 30 min)
- **git-ai-archaeology** (intermediate, 30 min)
- **git-worktree** (intermediate, 30 min)
- **git-worktree** (intermediate, 30 min)
- **git-worktree-clean** (intermediate, 30 min)
- **git-worktree-clean** (intermediate, 30 min)
- **git-worktree-remove** (intermediate, 30 min)
- **git-worktree-remove** (intermediate, 30 min)
- **git-worktree-status** (intermediate, 30 min)
- **git-worktree-status** (intermediate, 30 min)
- **governance-enforcement-hook** (intermediate, 30 min)
- **guide-recap** (intermediate, 30 min)
- **handoff-create** (intermediate, 30 min)
- **handoff-resume** (intermediate, 30 min)
- **handoff-update** (intermediate, 30 min)
- **identity-reinjection** (intermediate, 30 min)
- **implementer** (intermediate, 30 min)
- **integration-reviewer** (intermediate, 30 min)
- **investigate** (intermediate, 30 min)
- **investigate** (intermediate, 30 min)
- **issue-comment** (intermediate, 30 min)
- **issue-triage** (intermediate, 30 min)
- **kimi-prompt-template** (intermediate, 30 min)
- **land-and-deploy** (intermediate, 30 min)
- **land-and-deploy** (intermediate, 30 min)
- **landing-page-generator** (intermediate, 30 min)
- **landing-pattern** (intermediate, 30 min)
- **learn-alternatives** (intermediate, 30 min)
- **learn-quiz** (intermediate, 30 min)
- **learn-teach** (intermediate, 30 min)
- **learning-capture** (intermediate, 30 min)
- **learning-path** (intermediate, 30 min)
- **linkedin-template** (intermediate, 30 min)
- **log-ingestor** (intermediate, 30 min)
- **loop-monitor** (intermediate, 30 min)
- **mcp-config-integrity** (intermediate, 30 min)
- **mcp-integration-reference** (intermediate, 30 min)
- **mcp-status** (intermediate, 30 min)
- **memory-stack-integration** (intermediate, 30 min)
- **methodology-advisor** (intermediate, 30 min)
- **methodology-advisor** (intermediate, 30 min)
- **newsletter-template** (intermediate, 30 min)
- **notification** (intermediate, 30 min)
- **optimize** (intermediate, 30 min)
- **optimize** (intermediate, 30 min)
- **output-evaluator** (intermediate, 30 min)
- **output-secrets-scanner** (intermediate, 30 min)
- **output-validator** (intermediate, 30 min)
- **pattern-evaluation** (intermediate, 30 min)
- **pdf-generator** (intermediate, 30 min)
- **permission-request** (intermediate, 30 min)
- **pipeline** (intermediate, 30 min)
- **plan-ceo-review** (intermediate, 30 min)
- **plan-challenger** (intermediate, 30 min)
- **plan-eng-review** (intermediate, 30 min)
- **plan-execute** (intermediate, 30 min)
- **plan-pipeline** (intermediate, 30 min)
- **plan-pipeline-ceo-review** (intermediate, 30 min)
- **plan-pipeline-eng-review** (intermediate, 30 min)
- **plan-pipeline-execute** (intermediate, 30 min)
- **plan-pipeline-start** (intermediate, 30 min)
- **plan-pipeline-validate** (intermediate, 30 min)
- **plan-start** (intermediate, 30 min)
- **plan-validate** (intermediate, 30 min)
- **planner** (intermediate, 30 min)
- **planning-coordinator** (intermediate, 30 min)
- **pr** (intermediate, 30 min)
- **pr** (intermediate, 30 min)
- **pr-triage** (intermediate, 30 min)
- **pre-commit-evaluator** (intermediate, 30 min)
- **pre-commit-secrets** (intermediate, 30 min)
- **privacy-warning** (intermediate, 30 min)
- **prompt-injection-detector** (intermediate, 30 min)
- **qa** (intermediate, 30 min)
- **qa** (intermediate, 30 min)
- **quiz** (intermediate, 30 min)
- **recipe-template** (intermediate, 30 min)
- **recipe-template** (intermediate, 30 min)
- **refactor** (intermediate, 30 min)
- **refactor** (intermediate, 30 min)
- **refactoring-specialist** (intermediate, 30 min)
- **release-notes** (intermediate, 30 min)
- **release-notes** (intermediate, 30 min)
- **release-notes-generator** (intermediate, 30 min)
- **remotion-quickstart** (intermediate, 30 min)
- **repo-integrity-scanner** (intermediate, 30 min)
- **report-template** (intermediate, 30 min)
- **resume-handoff** (intermediate, 30 min)
- **review-comment** (intermediate, 30 min)
- **review-plan** (intermediate, 30 min)
- **review-plan** (intermediate, 30 min)
- **review-pr** (intermediate, 30 min)
- **review-pr** (intermediate, 30 min)
- **risk-classifier** (intermediate, 30 min)
- **routines-discover** (intermediate, 30 min)
- **routines-discover** (intermediate, 30 min)
- **rtk-auto-wrapper** (intermediate, 30 min)
- **rtk-baseline** (intermediate, 30 min)
- **rtk-optimizer** (intermediate, 30 min)
- **sandbox-status** (intermediate, 30 min)
- **sandbox-status** (intermediate, 30 min)
- **sandbox-unblock** (intermediate, 30 min)
- **sandbox-validation** (intermediate, 30 min)
- **scaffold** (intermediate, 30 min)
- **scaffold** (intermediate, 30 min)
- **security** (intermediate, 30 min)
- **security** (intermediate, 30 min)
- **security-audit** (intermediate, 30 min)
- **security-audit** (intermediate, 30 min)
- **security-auditor** (intermediate, 30 min)
- **security-check** (intermediate, 30 min)
- **security-check** (intermediate, 30 min)
- **security-check** (intermediate, 30 min)
- **security-check** (intermediate, 30 min)
- **security-checklist** (intermediate, 30 min)
- **security-gate** (intermediate, 30 min)
- **security-patcher** (intermediate, 30 min)
- **sentry-mcp** (intermediate, 30 min)
- **session-logger** (intermediate, 30 min)
- **session-save** (intermediate, 30 min)
- **session-save** (intermediate, 30 min)
- **session-summary** (intermediate, 30 min)
- **session-summary-config** (intermediate, 30 min)
- **sessions** (intermediate, 30 min)
- **setup-init** (intermediate, 30 min)
- **ship** (intermediate, 30 min)
- **ship** (intermediate, 30 min)
- **skill-creator** (intermediate, 30 min)
- **slack-template** (intermediate, 30 min)
- **slack-template** (intermediate, 30 min)
- **smart-explore** (intermediate, 30 min)
- **smart-suggest** (intermediate, 30 min)
- **sonarqube** (intermediate, 30 min)
- **sonarqube** (intermediate, 30 min)
- **status** (intermediate, 30 min)
- **structural** (intermediate, 30 min)
- **subagent-stop** (intermediate, 30 min)
- **talk-pipeline** (intermediate, 30 min)
- **talk-stage1-extract** (intermediate, 30 min)
- **talk-stage2-research** (intermediate, 30 min)
- **talk-stage3-concepts** (intermediate, 30 min)
- **talk-stage4-position** (intermediate, 30 min)
- **talk-stage5-script** (intermediate, 30 min)
- **talk-stage6-revision** (intermediate, 30 min)
- **tdd-workflow** (intermediate, 30 min)
- **teach** (intermediate, 30 min)
- **tech-to-product-mappings** (intermediate, 30 min)
- **test-hooks** (intermediate, 30 min)
- **test-on-change** (intermediate, 30 min)
- **test-writer** (intermediate, 30 min)
- **tests** (intermediate, 30 min)
- **threat-reporter** (intermediate, 30 min)
- **token-audit** (intermediate, 30 min)
- **tone-guidelines** (intermediate, 30 min)
- **tts-selective** (intermediate, 30 min)
- **twitter-template** (intermediate, 30 min)
- **typecheck-on-save** (intermediate, 30 min)
- **unicode-injection-scanner** (intermediate, 30 min)
- **update-handoff** (intermediate, 30 min)
- **update-threat-db** (intermediate, 30 min)
- **update-threat-db** (intermediate, 30 min)
- **validate-changes** (intermediate, 30 min)
- **validate-changes** (intermediate, 30 min)
- **velocity-governor** (intermediate, 30 min)
- **verification-gate** (intermediate, 30 min)
- **version-output** (intermediate, 30 min)
- **voice-refine** (intermediate, 30 min)
- **week-output** (intermediate, 30 min)

### Тестування (1)

- **review-admission** (intermediate, varies)

---

## Для початківців

Шаблони, рекомендовані тим, хто користується вперше:

Поки що немає шаблонів, явно позначених як придатні для початківців.

---

## Довідник з метаданих

Шаблони можуть містити такі метадані в YAML-frontmatter:

```yaml

name: template-name

description: What this template does

complexity: beginner|intermediate|advanced

time: 5 min|15 min|30 min|1 hour|2 hours|4+ hours|varies

domain: security|testing|deployment|general|...

prerequisites: [skill1, skill2]

status: stable|experimental|deprecated

keywords: [tag1, tag2]

```
