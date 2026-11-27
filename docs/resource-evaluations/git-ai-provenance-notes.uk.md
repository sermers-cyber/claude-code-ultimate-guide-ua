# git-ai: построкова атрибуція AI у git notes, перевірена на переписуванні історії

**Переглянуто**: 2026-11-08. **Оцінка**: 4/5, інтегровано в [AI Traceability §3.4 і §3.5](../../guide/ops/ai-traceability.uk.md#35-походження-provenance-у-git-notes) та як діаграму в [Enterprise Governance](../../guide/diagrams/12-enterprise-governance.uk.md#атрибуція-ai-через-переписування-історії). Пов'язане: [трасування походження агентів](agent-provenance-traces.uk.md), [Entire CLI](entire-cli.uk.md).

[git-ai](https://github.com/git-ai-project/git-ai/tree/5420ab9081d2cd57ffdafced09a8028d6dabf4bd) фіксує, які рядки написав агент, зберігає цю атрибуцію в git notes під `refs/notes/ai` і переносить її, коли історію переписують. Для цієї оцінки версію 1.7.7 зібрано з вихідного коду на `5420ab9` (2026-11-05) і проведено тест переписування. Серед інструментів відстеження походження, оцінених у цьому циклі, лише його було запущено.

## Джерела

| Джерело | Внесок | Обмеження |
|---|---|---|
| [Репозиторій на `5420ab9`](https://github.com/git-ai-project/git-ai/tree/5420ab9081d2cd57ffdafced09a8028d6dabf4bd), README і `src/` прочитано 2026-11-08 | Набір команд, використання `checkpoint`, дизайн демона, захист у sandbox, таблиця підтримки переписувань | Документація проєкту; виконано лише шляхи, наведені нижче |
| Тест переписування, запущений 2026-11-08, і тест звичайних git notes з git 2.56.0 (скрипти й логи збережено в робочих нотатках цієї оцінки) | Вміст нотатки та `git-ai blame` до і після amend, rebase і `git merge --squash` | Один файл, тестовий пресет `mock_ai`, локальний репозиторій, git 2.56.0, macOS |
| [Aidan Cunniffe, "Tracking AI generated code with Git"](https://www.youtube.com/watch?v=irK4G2SzhpA), DevCon Fall 2025, 2025-11-27 | Демо й твердження автора | Доповідач є автором інструмента |

## Як це працює, за кодом і README

- Агенти викликають `git-ai checkpoint <preset> [--hook-input <json|stdin>] [files...]`, коли записують файли; серед пресетів є `claude`, `codex`, `cursor` і тестовий пресет `mock_ai` (`src/commands/git_ai_handlers.rs`). Прапорців `--tool` чи `--session` немає.
- Під час коміту построкова атрибуція потрапляє в нотатку на `refs/notes/ai` (схема `authorship/3.0.0`): для кожного файлу діапазони рядків зіставлено із сесією, а для кожної сесії вказано інструмент, ідентифікатор і модель.
- За переписуваннями стежить фоновий демон, який читає події trace2 від git через `trace2.eventTarget`, а не git hooks чи обгортка над git. З README: "Git AI analyzes the final state of the code after the operation completes and copies/merges the attributions into a Git Note for any updated commits. The entire system is eventually consistent".
- `git-ai install-hooks` встановлює hooks агентів і задає глобальну ціль trace2; також може встановлювати розширення редакторів (`code --install-extension` у `src/mdm/utils.rs`). `git-ai stats [commit]` показує статистику для одного коміту.
- Демон відмовляється запускатися всередині sandbox агентів (`src/sandbox.rs`: `CURSOR_SANDBOX`, `SANDBOX_RUNTIME`, `CODEX_SANDBOX`).

## Тест переписування

Налаштування: ізольовані `HOME` і глобальна конфігурація git, `trace2.eventTarget` вручну спрямовано на сокет демона (`install-hooks` не запускався, бо зачепив би й справжні редактори), демон запущено через `git-ai bg start`, два рядки AI записано й зафіксовано через checkpoint з `mock_ai`, потім третій.

| Крок | HEAD після кроку | Нотатка на HEAD | `git-ai blame ai.txt` |
|---|---|---|---|
| 1. Коміт AI (2 рядки) | `cf0f5d1` | сесія `s_0527…` рядки 1-2 | рядки 1-2 `mock_ai` |
| 2. `git commit --amend`, третій рядок AI зафіксовано через checkpoint | `c234f08` | сесія `s_0527…` рядки 1-2, сесія `s_74c7…` рядок 3 | рядки 1-3 `mock_ai` |
| 3. `git rebase main` на новий коміт у main | `7b8655a` | ті самі дві сесії й діапазони | рядки 1-3 `mock_ai` |
| 4. `git merge --squash feature`, потім коміт у main | `3dbe89d` | ті самі дві сесії й діапазони | рядки 1-3 `mock_ai` |

Кожне переписування давало новий SHA, і нотатка переходила за ним, зберігаючи попередні діапазони (крок 2 додав зафіксований рядок 3). Інтеграційні тести автора для amend, rebase і squash (`cargo test --test integration -- amend:: rebase:: squash_merge:: ci_squash_rebase::`) не змогли запустити свій демон у sandbox Claude Code; кожна помилка вказувала на той самий захист, тож про атрибуцію вони нічого не кажуть.

**Тест не охоплює**: cherry-pick, stash, reset; кілька файлів і часткове додавання до індексу; справжні пресети агентів; push і fetch нотаток; squash чи rebase, виконаний платформою (кнопка злиття в GitLab чи GitHub), коли жоден локальний демон не бачить переписування. Для цього випадку README посилається на [CI workflows](https://usegitai.com/docs/guides/ci-workflows); не прочитано.

## Твердження з доповіді автора

- [201 с](https://www.youtube.com/watch?v=irK4G2SzhpA&t=201): "it'll go through merges rebases cherrypicks all the nasty evil stuff that you can do to commits and diffs. Um, Git AI will preserve the authorship through all those real world workflows." Тест вище локально підтверджує rebase і squash merge, але не cherry-pick.
- [295 с](https://www.youtube.com/watch?v=irK4G2SzhpA&t=295): "it's doing this by attaching git notes um to every single commit."
- [520 с](https://www.youtube.com/watch?v=irK4G2SzhpA&t=520): користувачі "review code differently based on whether an AI wrote it or whether a human wrote it", а запуск blame показував "what the prompt was and what the intent was behind this block of code". Зі слів автора; без кількісних даних.

## Виправлення в посібнику, зроблені разом із цією оцінкою

- «AI Code Halflife of 3.33 years», указаний в `ai-traceability.md`, не мав джерела. Станом на 2026-11-08 у репозиторії git-ai не було жодного входження «half-life», а вебпошук повернув лише цей посібник і його копії. Показник вилучено, як це вже зробили підсумкові картки.
- «Survive rebase, squash, and cherry-pick» замінено на те, що було перевірено, а cherry-pick лишено як твердження автора.
- `git-ai stats [commit]`, згідно з довідкою, показує "AI authorship statistics for a commit"; `git-ai stats HEAD` на тестовому репозиторії показав squash-коміт як 100% AI. Це не команда для «метрик усього проєкту».
- [Оцінка Entire CLI](entire-cli.uk.md) у лютому 2026 року зафіксувала git-ai як 404; репозиторій `git-ai-project/git-ai` був доступний 2026-11-08.

## Оцінка: 4/5

Основний механізм працює, як задокументовано, на перевірених шляхах, зберігає атрибуцію в репозиторії, а не в сервісі постачальника, і специфікація Agent Trace називає його серед партнерів, які допомогли сформувати формат. Він фіксує, хто написав які рядки, але не чому: нотатка містить сесії й діапазони рядків; її поле `prompts` у тесті було порожнім, а збирання промптів зі справжніми агентами не перевірялося.

## Рішення

Переписати §3.4 з перевіреними фактами, додати §3.5 «Provenance in git notes» з порівнянням git-ai з іншими прочитаними засобами запису та додати діаграму шляху атрибуції через amend, rebase, squash і злиття на платформі. Вилучити показник halflife.
