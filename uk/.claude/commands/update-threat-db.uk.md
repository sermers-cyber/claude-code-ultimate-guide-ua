# Делегування оновлень бази загроз AgentSec

Нативний skill `update-threat-db` у Claude і Codex читає цей контракт делегування. Його джерело — `.claude/skills/update-threat-db/SKILL.md`; виконай `python3 scripts/sync-threat-skill.py --check`, щоб перевірити проєкцію для Codex.

AgentSec Triage є канонічним технічним джерелом для доказів загроз, датованих fiches, вхідних даних детекторів і публічного security-фіду. Не досліджуй і не редагуй базу посібника першою.

## Знайти AgentSec

Використовуй `AGENTSEC_REPO`, якщо його вже задано. Інакше шукай сусідній checkout `../agentsec-triage` від кореня цього репозиторію. Зупинись, якщо жодного шляху немає або якщо він не містить усіх цих файлів:

- `AGENTS.md`
- `.claude/commands/update-threat-db.md`
- `data/intelligence/sources.yaml`
- `data/intelligence/events.yaml`
- `data/threat-db.yaml`

Не клонуй, не роби pull, не встановлюй, не публікуй і не роби push без явного дозволу.

## Виконати канонічний робочий процес

Прочитай `AGENTS.md` AgentSec, потім виконай його `.claude/commands/update-threat-db.md` з репозиторію AgentSec. AgentSec відповідає за перегляд джерел, невизначеність, покриття детекторів, регресійні тести, згенеровані артефакти та межу публікації.

Після того як AgentSec локально проходить перевірки, синхронізуй його згенерований фід із цим посібником і лендінгом за допомогою `scripts/sync_security_feed.py --write`. Виконай ту саму команду з `--check`, потім виконай:

```bash
python3 scripts/test-check-agentsec-security-feed.py
python3 scripts/check-agentsec-security-feed.py \
  --agentsec-feed "$AGENTSEC_REPO/exports/security-feed.v1.json"
```

Посібник тимчасово зберігає `examples/commands/resources/threat-db.yaml`, бо `/security-check` і `/security-audit` досі його споживають. Це споживач для сумісності, а не місце, з якого починають нове оновлення розвідданих.

Після оновлення цієї бази сумісності онови також пошуковий каталог лендінгу, а не лише його фід. З кореня лендінгу передай фактичний шлях до checkout посібника (особливо під час перевірки ізольованих checkout):

```bash
node scripts/sync-security-catalog.mjs --write --guide-root /path/to/claude-code-ultimate-guide
node scripts/sync-security-catalog.mjs --check --guide-root /path/to/claude-code-ultimate-guide
node --test src/data/agentsec-security-feed.test.ts src/data/agentsec-feed-sync.test.ts
```

Каталог зберігає історичні записи посібника, яких ще може не бути в AgentSec. Повідомляй їхню кількість окремо від кількості канонічного фіду. Не переноси ці історичні записи в AgentSec без перегляду джерел.

## Подальші дії в посібнику

Лише після перегляду запису AgentSec:

- додай контекст для читачів у `guide/security/security-hardening.md`, коли знахідка суттєво змінює рекомендації;
- онови базу сумісності, не заявляючи про покриття детекторів, якого AgentSec не реалізує;
- онови `CHANGELOG.md` у розділі `[Unreleased]`;
- тримай дзеркало фіду AgentSec побайтово ідентичним його канонічному артефакту.

Повідомляй про валідацію AgentSec, посібника й лендінгу окремо. Явно вкажи статус коміту, push, тега та публікації.
