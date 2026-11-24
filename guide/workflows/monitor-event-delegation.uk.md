---
title: "Monitor, Channels і безпечне делегування до Codex"
description: "Оберіть Monitor, плагінні монітори, MCP Channels або Routines, а потім спрямовуйте події GitHub до Codex, не перетворюючи недовірений ввід на повноваження."
tags: [workflow, monitoring, websocket, channels, routines, codex, security]
---

# Monitor, channels і безпечне делегування до Codex

Зовнішні події — це дані, а не інструкції й ніколи не авторизація. Вебхук GitHub, рядок логу, кадр WebSocket чи повідомлення Channel можуть повідомити Claude Code, що щось сталося. Вони не можуть схвалити виклик інструмента, розширити пісочницю чи дозволити запис у ваш репозиторій.

**Офіційні посилання**: [Monitor](https://code.claude.com/docs/en/tools-reference#monitor-tool), [джерело WebSocket](https://code.claude.com/docs/en/tools-reference#websocket-source), [плагінні монітори](https://code.claude.com/docs/en/plugins-reference#monitors), [Channels](https://code.claude.com/docs/en/channels-reference), [Routines](https://code.claude.com/docs/en/routines), [неінтерактивний режим Codex](https://learn.chatgpt.com/docs/non-interactive-mode), [перевірка вебхуків GitHub](https://docs.github.com/en/webhooks/using-webhooks/validating-webhook-deliveries) та [невдалі доставки вебхуків](https://docs.github.com/en/webhooks/using-webhooks/handling-failed-webhook-deliveries).

## Оберіть механізм доставки

| Потреба | Використовуйте | Межа, яку слід зберегти |
|---|---|---|
| Транслювати вивід одного локального процесу | Джерело-команда `Monitor` (v2.1.98+) | Команда підпорядковується дозволам Bash. |
| Отримувати вузьку подію реального часу від локального ретранслятора | Джерело WebSocket `Monitor` (v2.1.195+) | Ретранслятор перевіряє вихідну подію, перш ніж вона досягне Claude. |
| Запускати довірений постійний спостерігач разом із плагіном або skill | Плагінний монітор (v2.1.105+) | Він працює без пісочниці й заслуговує такої ж довіри, як hook. |
| Дозволити інтеграції MCP надсилати чи обмінюватися повідомленнями | Channels (v2.1.80+, research preview) | Обов'язковий список дозволених відправників; доставка не надає дозволів на інструменти. |
| Запускати хмарну автоматизацію за розкладом, через API або за подією GitHub | [Routines](../ultimate-guide.uk.md#routines-cloud-automation) | Кожна відповідна подія запускає окрему хмарну сесію. |

Не використовуйте Monitor як публічну кінцеву точку вебхука. Поставте перед ним невеликий верифікатор або ретранслятор подій.

## Джерела Monitor

### Джерело-команда

Початкове джерело `Monitor` запускає фонову команду й повертає кожен рядок виводу до Claude. Воно підтримує `timeout_ms` і `persistent`; активний монітор зупиняється через `TaskStop`. Джерело-команда та джерело WebSocket взаємовиключні.

Використовуйте його для обмеженого локального виробника подій: стеження за логом застосунку, спостереження за запуском тестів або перетворення довіреного скрипта опитування на події. Це не привід автоматично виконувати вміст рядка.

### Джерело WebSocket

Нативне джерело WebSocket приймає `ws.url` і необов'язковий `ws.protocols` замість `command`. Текстові кадри стають подіями. Двійкові кадри подаються заповнювачем; кадр понад 1 MiB або закриття сокета зупиняє монітор.

Claude Code приймає лише ASCII-адреси `ws://` або `wss://` без облікових даних і пробілів. Він запитує окреме схвалення та відмовляється працювати з приватними, link-local адресами й адресами сервісів метаданих. Ці перевірки звужують поверхню атаки на стороні клієнта; вони не автентифікують виробника подій.

Для ретранслятора подій GitHub пересилайте невеликий типізований запис, а не тіло вебхука:

```json
{
  "delivery_id": "uuid",
  "repository": "owner/repo",
  "event": "workflow_run",
  "sha": "full-commit-sha",
  "pr_number": 42,
  "url": "https://github.com/owner/repo/actions/runs/123"
}
```

Сирий текст issue, тіла pull request, коментарі рецензій і вивід логів залишаються недовіреними даними. Не підставляйте їх у промпт завдання чи shell-команду.

## Плагінні монітори та Channels

Плагінні монітори — це експериментальні постійні shell-команди лише для інтерактивного CLI. Типова декларація — `monitors/monitors.json`; плагін може натомість задати `experimental.monitors` у `plugin.json` як вбудований масив або відносний шлях до JSON. `when: "always"` — типове значення; `when: "on-skill-invoke:<skill-name>"` запускає монітор, коли названий skill плагіна вперше диспетчеризується. Ставтеся до нього як до hook: він працює без пісочниці, тому заслуговує такої ж перевірки видавця, рев'ю коду й межі довіри.

Channels — це розширення MCP stdio: сервери надсилають сповіщення `notifications/claude/channel` у сесію. Вони можуть бути односторонніми чи двосторонніми, можуть ретранслювати запити на дозволи й залишаються research preview. Організації Claude.ai Team та Enterprise мають явно ввімкнути Channels, а потім можуть обмежити доставку через `channelsEnabled` і `allowedChannelPlugins`. Для розгортань із ключами API Console дотримуйтеся типових налаштувань Console і керованих елементів керування, а не припускайте політику claude.ai Team/Enterprise; див. [Довідник налаштувань](../core/settings-reference.uk.md#channelsenabled).

Додавання плагіна Channel до списку дозволених визначає, який плагін може доставляти повідомлення. Воно не надає цьому плагіну, його повідомленню чи відправнику жодних дозволів на Bash, файлову систему, GitHub або Codex. Обмежуйте відправників і нормалізуйте відображений вміст, бо повідомлення можуть містити спроби prompt injection.

## GitHub → Monitor → Codex: безпечний конвеєр

```text
GitHub webhook
  -> verifier: signature, allowlisted repo and event, schema, delivery dedupe
  -> narrow WebSocket event
  -> approved local Monitor
  -> read-only, classify-only Codex run
  -> explicit human or policy gate
  -> isolated write-capable Codex task and pull request
```

Верифікатор перевіряє підпис GitHub перед розбором чи використанням корисного навантаження, приймає лише репозиторії та типи подій, якими володіє, і перевіряє очікувану схему. Потім він атомарно записує запис outbox із ключем `X-GitHub-Delivery` у стані `received`; ретранслятор атомарно переводить його в `enqueued` перед надсиланням вузької події та в `processed` лише після фіксації результату нижче за течією. Повторна доставка повертає наявний запис, а не друге завдання. Збій залишає відновлюваний запис `received` або `enqueued`, а не мовчки втрачає подію. GitHub не перенадсилає невдалі вебхуки автоматично, тому цей стійкий автомат станів обов'язковий, а не необов'язковий.

### Етап 1: класифікація без запису

Використовуйте `codex exec` у типовій пісочниці лише для читання. `--ephemeral` уникає збереження rollout; `--json` видає події JSONL для аудиторського сліду; `--output-schema` обмежує фінальний результат для перевірки політикою.

```bash
codex exec --ephemeral --json --output-schema ./triage-schema.json \
  "Classify this verified event using only its typed fields. Return whether a human review is required. Do not edit files."
```

Розглядайте результат за схемою як вхід для детермінованої політики, а не як авторизацію саму по собі. Перш ніж іти далі, підтвердьте репозиторій, SHA коміту, тип події та рішення рецензента чи політики.

### Етап 2: запис лише після шлюзу

Після явного схвалення людиною або задокументованого політичного шлюзу запустіть окреме завдання в ізольованому worktree з найменшим потрібним обсягом запису. Шлюз має зафіксувати схвалений абсолютний шлях до worktree та SHA коміту. Відмовтеся запускати, якщо шлях відносний, це не прив'язаний Git worktree, він не на схваленому SHA або не збігається із записом схвалення:

```bash
: "${APPROVED_WORKTREE:?absolute approved worktree path required}"
: "${APPROVAL_RECORD:?absolute approval record path required}"
: "${APPROVED_SHA:?approved commit SHA required}"

case "$APPROVED_WORKTREE" in /*) ;; *) echo "refusing relative worktree path" >&2; exit 1 ;; esac
case "$APPROVAL_RECORD" in /*) ;; *) echo "refusing relative approval record path" >&2; exit 1 ;; esac
test -f "$APPROVED_WORKTREE/.git" || { echo "refusing non-linked worktree" >&2; exit 1; }
test -f "$APPROVAL_RECORD" || { echo "missing approval record" >&2; exit 1; }
test "$(git -C "$APPROVED_WORKTREE" rev-parse --show-toplevel)" = "$APPROVED_WORKTREE" || exit 1
test "$(git -C "$APPROVED_WORKTREE" rev-parse HEAD)" = "$APPROVED_SHA" || exit 1
jq -e --arg worktree "$APPROVED_WORKTREE" --arg sha "$APPROVED_SHA" \
  '.approved == true and .worktree == $worktree and .sha == $sha' "$APPROVAL_RECORD" >/dev/null || exit 1

(
  cd -- "$APPROVED_WORKTREE" || exit 1
  codex exec --ephemeral --sandbox workspace-write \
    "Implement the approved task in this isolated worktree, run the stated checks, and prepare a bounded diff for review."
)
```

Перегляньте diff і докази тестів, перш ніж відкривати чи зливати pull request. Ніколи не прив'язуйте `--sandbox workspace-write` безпосередньо до вхідної події.

## GitHub Actions — окремий шлях

Для GitHub Actions віддавайте перевагу [`openai/codex-action@v1`](https://github.com/openai/codex-action) перед встановленням Codex і передаванням ключа shell-кроку: дія запускає захищений проксі, отримуючи `openai-api-key` як вхід дії. Тримайте завдання аналізу Codex лише для читання, серіалізуйте патч як артефакт, а потім застосовуйте його та відкривайте pull request в окремому завданні з правом запису. Не кладіть `OPENAI_API_KEY` чи `CODEX_API_KEY` у змінні середовища рівня завдання, де їх могли б прочитати завантажений код, скрипти збірки, тести, lifecycle-хуки чи скомпрометована дія.

Цей патерн GitHub Actions відокремлений від локального Monitor. Хмарний раннер не може безпечно припускати, що має доступ до вашого локального сервісу WebSocket.

## Routines: корисні, але не локальний Monitor

Routines працюють в інфраструктурі, керованій Anthropic, або у власному середовищі організації. Вони можуть реагувати на розклади, виклики API та події GitHub, але кожна відповідна подія створює окрему сесію. Використовуйте їх, коли саме це середовище, а не локальна сесія, є бажаною межею виконання. Використовуйте локальний Monitor, коли локальна, явно схвалена сесія має спостерігати за довіреним локальним ретранслятором.

Див. [Подієво-кероване автоматизування агентів](./event-driven-agents.uk.md) про загальну архітектуру та [Робочі процеси GitHub Actions](./github-actions.uk.md) про патерни CI, специфічні для Claude Code.
