---
title: "Module 06: Hooks and events"
description: "Модуль 06 навчального шляху: додайте hook для Claude Code, який ухвалює рішення зі структурованого вводу, відмовляє за замовчуванням (fails closed) на некоректному вводі та тестується без сесії."
---

# Module 06: Hooks and events

**Час:** 1 година | **Складність:** Intermediate

**Попередній:** [Module 05: Skills and Automation](05-skills.uk.md)

## Мета

Додати один hook для Claude Code, який ухвалює рішення щодо інструмента зі структурованого вводу, відмовляє за замовчуванням (fails closed) на некоректному вводі та може бути протестований без запуску інтерактивної сесії.

Hooks Claude Code не є Git hooks. Git hooks реагують на дії з репозиторієм, як-от `pre-commit`. Hooks Claude Code реагують на події життєвого циклу та інструментів Claude Code, як-от `PreToolUse`, `PostToolUse` і `SessionStart`.

## Що ви дізнаєтеся

- де Claude Code читає конфігурацію hooks;
- як matchers вибирають виклики інструментів;
- що command hook отримує на стандартний ввід;
- як hook `PreToolUse` дозволяє або забороняє виклик;
- що коди виходу доводять, а що ні;
- як протестувати скрипт рішення на фіксованих фікстурах.

Повну матрицю подій дивіться в [довіднику подій hooks](../core/hooks-events-reference.uk.md). Авторитетну [документацію hooks](https://code.claude.com/docs/en/hooks) підтримує Anthropic.

## Межа hook

Command hook — це локальна програма, яку запускає Claude Code. Вона отримує один JSON-об'єкт на стандартний ввід. Поля залежать від події. Для `PreToolUse` корисні поля містять `tool_name`, `tool_input` і `tool_use_id`.

Matcher для події інструмента фільтрує за `tool_name`:

```text
Claude proposes Write or Edit
             |
             v
PreToolUse matcher selects the hook
             |
             v
Hook reads JSON and returns deny or no decision
             |
             v
Claude Code applies the decision
```

Тримайте рішення вузьким. Політика шляхів може вирішити, чи спрямований запропонований запис файлу в захищене розташування. Вона не може довести, що отримана програма безпечна або коректна.

## Зареєструйте hook `PreToolUse`

Hooks проєкту розміщуються в `.claude/settings.json`. Наведений запис запускає одну команду Python для викликів `Write` і `Edit`:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "python3",
            "args": ["${CLAUDE_PROJECT_DIR}/.claude/hooks/protect-paths.py"],
            "timeout": 10
          }
        ]
      }
    ]
  }
}
```

У цьому прикладі підтримуваним файлом конфігурації є `settings.json`. Варіант `settings.yaml` не входить до цього контракту.

## Побудуйте скрипт рішення

Збережіть цей файл як `.claude/hooks/protect-paths.py`:

```python
#!/usr/bin/env python3
import json
import sys
from pathlib import PurePosixPath


def decide(value: str, reason: str) -> None:
    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": value,
            "permissionDecisionReason": reason,
        }
    }))


try:
    payload = json.load(sys.stdin)
except (json.JSONDecodeError, UnicodeDecodeError):
    decide("deny", "Hook input was not valid JSON.")
    raise SystemExit(0)

if payload.get("tool_name") not in {"Write", "Edit"}:
    decide("deny", "Unexpected tool for this matcher.")
    raise SystemExit(0)

file_path = payload.get("tool_input", {}).get("file_path")
if not isinstance(file_path, str) or not file_path.strip():
    decide("deny", "Write or Edit input did not contain a file_path.")
    raise SystemExit(0)

path = PurePosixPath(file_path.replace("\\", "/"))
protected = (
    ".git" in path.parts
    or path.name == ".env"
    or path.name.startswith(".env.")
    or path.suffix in {".key", ".pem"}
)

if protected:
    decide("deny", f"Protected path: {file_path}")
else:
    raise SystemExit(0)
```

Цей приклад повертає структуроване рішення лише тоді, коли забороняє виклик. Код виходу `0` без виводу залишає в силі звичайний потік дозволів Claude Code; він не надає дозволу. Некоректний або неповний ввід забороняється, бо скрипт не може встановити безпечний шлях.

## Протестуйте три фікстури

Запустіть скрипт рішення безпосередньо:

```bash
printf '%s\n' '{"tool_name":"Write","tool_input":{"file_path":"src/app.py"}}' \
  | python3 .claude/hooks/protect-paths.py

printf '%s\n' '{"tool_name":"Edit","tool_input":{"file_path":".env"}}' \
  | python3 .claude/hooks/protect-paths.py

printf '%s\n' '{bad json' \
  | python3 .claude/hooks/protect-paths.py
```

Очікувані рішення:

| Фікстура | Очікуваний результат | Причина |
| --- | --- | --- |
| `src/app.py` | Вихід `0`, без виводу | Шлях поза захищеним набором, тож звичайний потік дозволів триває |
| `.env` | `deny` | Політика прямо називає цей шлях |
| некоректний JSON | `deny` | Hook не може перевірити запит |

Ці тести фікстур перевіряють локальний контракт вводу й виводу скрипта. Вони не перевіряють, що Claude Code завантажив налаштування проєкту. Підтвердьте завантаження під час виконання окремо, спробувавши нешкідливий запис і запис у захищений шлях у тимчасовому проєкті-фікстурі.

## Коди виходу

Коди виходу залежать від події:

- код виходу `0` означає, що команда hook завершилася; після цього Claude Code розбирає будь-який підтримуваний JSON-вивід;
- код виходу `2` блокує події, що підтримують блокування, зокрема `PreToolUse`, і повертає стандартний вивід помилок Claude;
- інші ненульові коди виходу зазвичай повідомляють про неблокувальну помилку hook;
- `WorktreeCreate` є винятком, бо будь-який ненульовий вихід зриває створення;
- деякі події ігнорують коди виходу або натомість використовують структуроване JSON-рішення.

Не переносьте конвенції Unix бездумно. Код виходу `1` не блокує виклик `PreToolUse`. [Довідник подій](../core/hooks-events-reference.uk.md#поведінка-коду-виходу-2-для-кожної-події) фіксує поведінку для кожної підтримуваної події.

## Правила безпечного проєктування

- Тримайте matcher таким самим вузьким, як політика.
- Розбирайте ввід явно й відхиляйте невідомі форми, коли від них залежить безпека.
- Уникайте мережевих викликів у блокувальному hook.
- Не допускайте секретів у вивід hook і журнали налагодження.
- Віддавайте перевагу валідації лише для читання, а не прихованій зміні файлів.
- Встановлюйте timeout.
- Тестуйте фікстури дозволу, заборони та некоректного вводу.
- Записуйте, яка поведінка під час виконання лишилася неперевіреною.

Hooks виконують локальний код із правами процесу Claude Code. Перегляньте спільний hook, перш ніж його вмикати. Про моделювання загроз і ризики виконання під час запуску читайте [Посилення безпеки](https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/security/security-hardening.md#16-startup-hooks-code-execution-before-your-first-prompt) і [Безпеку у продакшені](../security/production-safety.uk.md).

## Вправа: створіть hook для валідації

1. Додайте реєстрацію `PreToolUse` до `.claude/settings.json` у тимчасовому проєкті.
2. Збережіть скрипт рішення як `.claude/hooks/protect-paths.py`.
3. Запустіть три фікстури та збережіть їхні JSON-виводи.
4. Запустіть Claude Code в проєкті-фікстурі.
5. Попросіть записати `src/app.py` і переконайтеся, що рішення це дозволяє.
6. Попросіть записати `.env` і переконайтеся, що рішення це забороняє.
7. Запишіть версію Claude Code, шлях до налаштувань, команду, результат і неперевірений обсяг.

Вправу завершено, коли три прямі фікстури збігаються з таблицею, а дві тимчасові перевірки під час виконання збігаються із заявленими рішеннями. Якщо завантаження під час виконання не тестувалося, запишіть його як `UNKNOWN`, а не робіть висновок із прямих тестів скрипта.

## Ви готові, якщо

- ви вмієте відрізнити hooks Claude Code від Git hooks;
- ви можете назвати подію та matcher, які використовує ваш hook;
- ваш hook читає JSON зі стандартного вводу;
- некоректний ввід має явний наслідок;
- ви знаєте, що код виходу `1` не блокує `PreToolUse`;
- ваше підтвердження відокремлює тести скрипта від завантаження в Claude Code під час виконання.

## Що далі

[Module 07: Advanced Patterns](07-advanced.uk.md) поєднує hooks, skills, agents і верифікацію у більші воркфлоу.

---
**Локалізація**: [Serhii (MacPlus Software)](https://macplus-software.com)
*Остання синхронізація: Листопад 2026*
