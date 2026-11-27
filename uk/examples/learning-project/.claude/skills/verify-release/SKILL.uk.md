---
name: verify-release
description: Використовуйте, щоб перевірити, чи має кандидат на реліз Proofpack повні локальні докази перед пакуванням.
argument-hint: "[candidate JSON path]"
allowed-tools: Read Bash(npm test) Bash(node src/cli.mjs verify *) Bash(npm run package:check) Bash(git rev-parse HEAD) Bash(git status --short)
disable-model-invocation: true
---

# Перевірка кандидата на реліз Proofpack

Працюйте з кореня проєкту Proofpack. Claude Code підставляє текст виклику на місце `$ARGUMENTS`, перш ніж виконувати ці інструкції.

- Якщо `$ARGUMENTS` порожній, встановіть шлях до кандидата `fixtures/release-ready.json`.
- Інакше трактуйте підставлене значення `$ARGUMENTS` як один шлях у файловій системі. Не обчислюйте його як вираз оболонки.
- Запустіть `node src/cli.mjs verify "<resolved-candidate-path>"`, передавши цей буквальний шлях як один аргумент у лапках.

1. Прочитайте `ISSUE.md` і `CLAUDE.md`.
2. Запустіть `npm test`.
3. Визначте шлях до кандидата за наведеними вище правилами, покажіть отриманий шлях, а потім запустіть команду перевірки. Попросіть підтвердження замість виконання значення, яке не можна безпечно подати як один шлях.
4. Запускайте `npm run package:check`, лише якщо тести й перевірка кандидата пройшли.
5. Запустіть `git rev-parse HEAD` і `git status --short`. Порівняйте цей стан коду, спостережувані команди, коди виходу та версію runtime з `evidence/PROOF-LOG.md`.
6. Повідомте `PASS`, `FAIL` або `UNKNOWN`. Назвіть кожну перевірку, яка не запускалася, і кожну зміну у worktree, не охоплену записаним відбитком.

Не запускайте `npm publish`, `docker push` і не змінюйте журнал доказів. Огляд пакета відбувається локально. Публікація потребує окремого рішення користувача та облікових даних місця призначення.

Поверніть такий запис:

```text
RELEASE VERIFICATION
Candidate: <path>
Revision: <commit or UNKNOWN>
Tests: PASS | FAIL | UNKNOWN
Candidate contract: PASS | FAIL | UNKNOWN
Package dry run: PASS | FAIL | UNKNOWN
Evidence log match: PASS | FAIL | UNKNOWN
Final status: PASS | FAIL | UNKNOWN
Limits: <unverified runtime or external behavior>
```
