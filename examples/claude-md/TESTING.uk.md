# Журнал доказів перевірки

Скопіюйте цей файл у робочий елемент перед тестуванням зміни, агентного воркфлоу або вибору Best-of-N. Заповнюйте поля доказами. Використовуйте `UNKNOWN`, якщо перевірку не запускали, її неможливо запустити або вона має неповне покриття. Не замінюйте це значення висновком про успішне проходження.

Довідка щодо методу: [Best-of-N: Generate, Select, and Verify](../../guide/workflows/best-of-n.uk.md). Багаторазову процедуру генерації та вибору див. у [skill Best-of-N](../skills/best-of-n/SKILL.uk.md).

## 1. Обсяг і контракт приймання

| Поле | Запис |
| --- | --- |
| Робочий елемент | `<issue, task, or request>` |
| Дата й відповідальний | `<ISO date, person or agent>` |
| Репозиторій і ревізія | `<remote or path, commit SHA>` |
| В обсязі | `<behavior, files, and environments>` |
| Поза обсягом | `<explicit exclusions>` |
| Критерії приймання | `<observable requirements>` |
| Обов'язкові підстави для відхилення | `<conditions that disqualify delivery>` |
| Межа повноважень | `<permissions, external actions, and approvals>` |

## 2. Середовище та вхідні дані

| Поле | Запис |
| --- | --- |
| ОС і середовище виконання | `<OS, language/runtime versions>` |
| Стан залежностей або lockfile | `<lockfile revision and install state>` |
| Конфігурація та секрети | `<redacted names only; never paste secrets>` |
| Версія даних або фікстур | `<source, hash, retention boundary>` |
| Версії інструментів і моделей | `<tool, model, harness, and prompt version>` |
| Бюджет часу й вартості | `<limit and actual if available>` |

## 3. Запис кандидатів і вибору

Використовуйте цей розділ лише тоді, коли згенеровано більше ніж одного кандидата. Під час оцінювання ідентифікатори кандидатів, де це практично можливо, мають бути непрозорими. Додайте по одному рядку таблиці для кожного згенерованого кандидата. Не пропускайте відхилених кандидатів або кандидатів, згенерованих у пізнішій партії.

| Поле | Запис |
| --- | --- |
| Версія зафіксованої рубрики | `<path, hash, or dated identifier>` |
| Кількість кандидатів, розклад партій і правило зупинки | `<N, every declared batch, and between-batch trigger>` |
| Засоби ізоляції | `<separate prompts, worktrees, models, or fresh contexts>` |
| Відома кореляція | `<shared model, prompt, tools, state, or none known>` |
| Обраний кандидат | `<ID and artifact link>` |
| Запис про розв'язання нічиєї або синтез | `<rule used, or new synthesized ID>` |

| Кандидат | Обов'язкові критерії | Оцінка за рубрикою та докази | Посилання на артефакт | Статус |
| --- | --- | --- | --- | --- |
| `<generated candidate ID>` | `<pass/fail>` | `<score, criterion evidence>` | `<path, diff, or URL>` | `<selected/rejected>` |

## 4. Виконувані перевірки

Записуйте кожну команду, яку справді запускали. Команду, якої тут немає, цей журнал не перевіряв.

| Перевірка | Команда | Середовище | Код завершення | Результат | Посилання на артефакт |
| --- | --- | --- | ---: | --- | --- |
| Модульні тести | `<exact command>` | `<environment ID>` | `<0/nonzero>` | `<pass/fail>` | `<output path>` |
| Перевірка типів або схеми | `<exact command>` | `<environment ID>` | `<0/nonzero>` | `<pass/fail>` | `<output path>` |
| Lint або статичний аналіз | `<exact command>` | `<environment ID>` | `<0/nonzero>` | `<pass/fail>` | `<output path>` |
| Збирання або пакування | `<exact command>` | `<environment ID>` | `<0/nonzero>` | `<pass/fail>` | `<artifact path/hash>` |
| Інтеграційні або наскрізні тести | `<exact command>` | `<environment ID>` | `<0/nonzero>` | `<pass/fail/UNKNOWN>` | `<output path>` |

## 5. Незалежне рев'ю

| Поле | Запис |
| --- | --- |
| Рецензент | `<person, agent, or service>` |
| Роль рецензента | `<human, fresh-context agent, different model, deterministic system>` |
| Відокремленість від генерації | `<what the reviewer did not receive>` |
| Спільний контекст і стимули | `<model, repository, tools, prompt, or access overlap>` |
| Обсяг рев'ю | `<requirements and artifacts examined>` |
| Вердикт і знахідки | `<accept/reject/needs changes; links>` |

## 6. Збої, невідомі та остаточне твердження

| Категорія | Запис |
| --- | --- |
| Виявлені збої | `<failed command, symptom, and disposition>` |
| Незапущені перевірки | `<reason and impact>` |
| Невідомі | `<uncovered behavior, environment, or external state>` |
| Зберігання артефактів | `<paths, hashes, access boundary, and expiry if applicable>` |
| Остаточний статус | `PASS`, `FAIL` або `UNKNOWN` |
| Твердження, яке обґрунтовує цей журнал | `<bounded statement only>` |

`PASS` означає, що перелічені критерії приймання пройшли в зазначеному середовищі. Це не доводить поведінку поза цим обсягом. `FAIL` означає, що обов'язковий критерій або заявлена перевірка не пройшли. `UNKNOWN` означає, що наявні докази не можуть підтвердити заявлене твердження.
