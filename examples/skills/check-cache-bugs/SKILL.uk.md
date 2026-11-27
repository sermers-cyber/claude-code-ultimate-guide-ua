---
name: check-cache-bugs
description: "Аудит налаштувань Claude Code на баги кешу (CC#40524): sentinel, --resume/--continue, заголовок атрибуції + ArkNill B3/B4/B5"
effort: low
disable-model-invocation: true
---

# Перевірка багів кешу (CC#40524)

Перевірте свої налаштування Claude Code на баги кешу й витрат, виявлені в березні-квітні 2026 року.

**Час**: ~30 секунд | **Охоплення**: версія, файли конфігурації, CLAUDE.md, skills, hooks, профілі shell, усі бінарники claude

> **Примітка щодо забруднення кешу**: цей skill завантажує вміст із рядками `cch=` у масив повідомлень поточної сесії. Для найчистіших результатів запускайте цю команду на самому початку нової сесії або через `claude -p "$(cat .claude/commands/check-cache-bugs.md)"` як одноразовий виклик у режимі print.

**Довідка**: `anthropics/claude-code#40524` | **Виявили**: `@jmarianski` + `@whiletrue0x` | **Розширив**: `@ArkNill` (ArkNill/claude-code-cache-analysis, квітень 2026)

---

## Передісторія

### Стан виправлень (актуально на v2.1.92)

| Баг | Уражені версії | Стан |
|-----|------------------|--------|
| Bug 1: cch sentinel (standalone-бінарник) | v2.1.36-v2.1.90 | **ВИПРАВЛЕНО у v2.1.91** |
| Bug 2: deferred_tools_delta під час --resume | v2.1.69-v2.1.89 | **ВИПРАВЛЕНО у v2.1.90** |
| Bug 3: хеш заголовка атрибуції для кожної сесії | v2.1.69+ | **Активний** (обхід через змінну середовища) |
| B4: Microcompact / тихе вирізання контексту | усі версії до v2.1.92 включно | **Активний** (керується GrowthBook) |
| B5: ліміт бюджету результатів інструментів 200K | усі версії до v2.1.92 включно | **Активний** (MCP-інструменти звільнено) |

### Три початкові баги (CC#40524)

- **Bug 1** (ВИПРАВЛЕНО v2.1.91): нативний HTTP-шар Bun виконував заміну байтів тієї самої довжини
  в заповнювачі атестації `cch=00000` після `JSON.stringify`, але до TLS. Спрацьовував лише тоді, коли
  `cch=00000` буквально траплявся у вмісті `messages[]`. Закриття підтверджено; npm і standalone-
  бінарник тепер рівнозначні у v2.1.91+.

- **Bug 2** (ВИПРАВЛЕНО v2.1.90): механізм запису JSONL сесії вирізав записи вкладень `deferred_tools_delta`
  перед записом на диск. Під час `--resume` цих записів не було; шар відкладених інструментів не мав
  попередньої історії й оголошував усі інструменти заново, зсуваючи позицію кожного повідомлення
  і повністю ламаючи префікс кешу на рівні повідомлень. Кожне відновлення перебудовувало 87-118K
  токенів як `cache_creation`. Anthropic відстежувала це внутрішньо як inc-4747.

- **Bug 3** (АКТИВНИЙ, v2.1.69+): Claude Code вставляє білінговий заголовок першим блоком
  системного промпту. Заголовок містить 3-символьний хеш SHA-256, отриманий із символів [4, 7, 20]
  першого повідомлення користувача + версії CC, унікальний для кожної сесії, кожного subagent і кожного побічного запиту. Оскільки
  кеш працює за префіксом, це спричиняє холодний промах на ~12K токенів системного промпту під час кожного
  виклику. Сесія з 5 subagents = 6 холодних промахів. Емпірично: 48% -> 99,98% влучань у кеш з
  обходом через змінну середовища.

### Додаткові баги (ArkNill, квітень 2026)

- **B4: Microcompact** (усі версії): три механізми тихо замінюють результати інструментів на
  `[Old tool result content cleared]` перед надсиланням в API. Керується серверними
  прапорцями GrowthBook, обходить `DISABLE_AUTO_COMPACT`. Команда `/export` показує початковий
  контекст, а НЕ те, що отримала модель. В одній сесії виміряно 327 подій очищення.

- **B5: Ліміт бюджету результатів інструментів** (усі версії): `applyToolResultBudget()` обрізає результати інструментів,
  коли сумарна кількість символів перевищує 200K. Це стосується вбудованих інструментів (Read, Bash, Grep, Glob, Edit).
  MCP-інструменти можуть перевизначити ліміт через `_meta["anthropic/maxResultSizeChars"]` (v2.1.91+).

Підсумок впливу на витрати: 2-5x на кожен старт сесії/subagent для Bug 3 окремо; 10-20x на хід для
Bug 2 з 10+ skills і 3-4 відновленнями (обидві оцінки правильні у своєму контексті).

---

## Інструкції

Ви аудитор. Виконайте всі фази по порядку, зберіть кожен результат і підготуйте фінальний звіт. Не пропускайте фази й не зупиняйтеся раніше.

---

### Фаза 1: Версія Claude Code і спосіб встановлення

```bash
# Version check
claude --version

# All installed claude binaries
which -a claude 2>/dev/null

# Check if active binary is standalone or npm
file $(which claude) 2>/dev/null
ls -la $(which claude) 2>/dev/null
```

- Версія < 2.1.90 -> позначте **BUG 2 RISK** (resume/DTD; виправлено у v2.1.90)
- Версія < 2.1.91 І standalone-бінарник -> позначте **BUG 1 MECHANISM** (sentinel; виправлено у v2.1.91)
- Версія >= 2.1.69 -> позначте **BUG 3 RISK** (заголовок атрибуції; виправлення ще немає, перевірте Фазу 4)
- Бінарник є виконуваним файлом Mach-O / ELF -> standalone (актуально для Bug 1 у v2.1.36-v2.1.90)
- Бінарник є символьним посиланням на `node_modules` або містить `cli.js` -> npm/npx

---

### Фаза 2: Пошук sentinel (Bug 1)

Шукайте буквальний рядок `cch=` у всіх статичних файлах конфігурації. Виключіть файли `.jsonl` (тимчасова історія розмов) і сам цей файл команди.

```bash
# Global config files
grep -r "cch=" \
  ~/.claude/CLAUDE.md \
  ~/.claude/MEMORY.md \
  ~/.claude/TONE.md \
  ~/.claude/FLAGS.md \
  ~/.claude/RULES.md \
  ~/.claude/RTK.md \
  ~/.claude/ANTI_AI.md \
  2>/dev/null

# Global skills, commands, agents, hooks (excluding this command file)
grep -rl "cch=" ~/.claude/skills/ 2>/dev/null
grep -rl "cch=" ~/.claude/commands/ --exclude="check-cache-bugs.md" 2>/dev/null
grep -rl "cch=" ~/.claude/agents/ 2>/dev/null
grep -rl "cch=" ~/.claude/hooks/ 2>/dev/null

# Project-level config
grep -r "cch=" CLAUDE.md .claude/CLAUDE.md .claude/MEMORY.md 2>/dev/null
grep -rl "cch=" .claude/skills/ 2>/dev/null
grep -rl "cch=" .claude/commands/ --exclude="check-cache-bugs.md" 2>/dev/null
grep -rl "cch=" .claude/agents/ 2>/dev/null
grep -rl "cch=" .claude/hooks/ 2>/dev/null

# Broader scan: all CLAUDE.md files across projects
find ~ -name "CLAUDE.md" \
  -not -path "*/node_modules/*" \
  -not -path "*/.git/*" \
  2>/dev/null | xargs grep -l "cch=" 2>/dev/null
```

Позначте як **BUG 1 RISK**, якщо знайдено будь-який збіг поза файлами `.jsonl` І версія < v2.1.91.
У v2.1.91+: механізм sentinel виправлено, ризику немає незалежно від вмісту конфігурації.

---

### Фаза 3: Використання resume/continue (Bug 2)

```bash
# settings.json
grep -i -- "--resume\|--continue" ~/.claude/settings.json 2>/dev/null
grep -i -- "--resume\|--continue" .claude/settings.json 2>/dev/null

# Hooks
grep -rn -- "--resume\|--continue" ~/.claude/hooks/ 2>/dev/null
grep -rn -- "--resume\|--continue" .claude/hooks/ 2>/dev/null

# Commands and skills
grep -rn -- "--resume\|--continue" ~/.claude/commands/ 2>/dev/null
grep -rn -- "--resume\|--continue" .claude/commands/ 2>/dev/null

# Shell profiles (aliases, functions)
grep -n -- "--resume\|--continue" ~/.zshrc ~/.bashrc ~/.bash_profile ~/.zprofile 2>/dev/null

# Project scripts
find . -name "*.sh" -o -name "Makefile" 2>/dev/null | \
  xargs grep -l -- "--resume\|--continue" 2>/dev/null
```

- Версія >= v2.1.90: Bug 2 **ВИПРАВЛЕНО**, позначайте збіги лише як інформаційні (активного ризику витрат немає)
- Версія < v2.1.90 І будь-який збіг у hooks/settings -> позначте **BUG 2 AUTOMATED** (постійна вразливість)
- Версія < v2.1.90 І будь-який збіг у commands/skills/scripts -> позначте **BUG 2 MANUAL** (вразливість під час виклику)

---

### Фаза 4: Перевірка заголовка атрибуції (Bug 3)

Перевірте, чи вже вимкнено змінну середовища білінгового заголовка.

```bash
# Global settings
grep -i "CLAUDE_CODE_ATTRIBUTION_HEADER\|ENABLE_TOOL_SEARCH" \
  ~/.claude/settings.json 2>/dev/null

# Project settings
grep -i "CLAUDE_CODE_ATTRIBUTION_HEADER\|ENABLE_TOOL_SEARCH" \
  .claude/settings.json 2>/dev/null

# Shell profiles
grep -i "CLAUDE_CODE_ATTRIBUTION_HEADER" \
  ~/.zshrc ~/.bashrc ~/.bash_profile ~/.zprofile 2>/dev/null
```

- `CLAUDE_CODE_ATTRIBUTION_HEADER` не встановлено у `false` І версія >= 2.1.69 -> позначте **BUG 3 ACTIVE**
- Уже встановлено у `false` -> **BUG 3 MITIGATED**

---

### Фаза 5: Перевірка кількох бінарників

```bash
for b in $(which -a claude 2>/dev/null | sort -u); do
  echo "=== $b ==="
  $b --version 2>/dev/null || echo "unavailable"
  file $b 2>/dev/null
  ls -la $b 2>/dev/null
done
```

Позначайте будь-який standalone-бінарник < v2.1.91 як ризиковий щодо Bug 1.
Позначайте будь-який бінарник < v2.1.90 як ризиковий щодо Bug 2.
Позначайте будь-який бінарник >= v2.1.69 як ризиковий щодо Bug 3 (якщо змінну середовища заголовка атрибуції ще не встановлено).
Зазначте застарілі бінарники, які можуть бути помилково викликані.

---

## Формат виводу

```
## Claude Code Cache Bug Audit: CC#40524

**Date**: [today]
**Active claude version**: [version]
**Install method**: [standalone binary | npm/npx | mixed]

---

### Bug 1: Sentinel replacement (standalone binary v2.1.36-v2.1.90)
**Status**: [FIXED (v2.1.91+) / SAFE / AT RISK / NOT APPLICABLE]

**Version >= v2.1.91**: [YES -> FIXED | NO -> check below]
**Mechanism active (standalone binary, v2.1.36-v2.1.90)**: [YES / NO]
**Trigger sentinel found in static config**: [YES (locations) | NO]

[If FIXED] Running v2.1.91+. Sentinel mechanism patched; npm and standalone are equivalent. No action needed.
[If AT RISK (v < 2.1.91 AND standalone AND sentinel found)]
-> Update to v2.1.91+: `npm install -g @anthropic-ai/claude-code@latest`
-> Temporary: remove `cch=00000` string from the flagged files, or use npm instead.
[If SAFE] Mechanism present in binary but no trigger in static config. Update to v2.1.91 still recommended.
[If NOT APPLICABLE] npm/npx install: Bug 1 mechanism absent.

---

### Bug 2: Cache prefix mismatch on --resume / --continue (v2.1.69-v2.1.89)
**Status**: [FIXED (v2.1.90+) / AT RISK (automated) / AT RISK (manual) / NOT APPLICABLE]

**Version >= v2.1.90**: [YES -> FIXED | NO -> check below]
**Automated usage found (hooks/settings)**: [YES (locations) | NO]
**Manual usage found (commands/skills/scripts)**: [YES (locations) | NO]

**Root cause**: JSONL writer stripped `deferred_tools_delta` records before writing to disk. On `--resume`,
the deferred tools layer had no announcement history and re-announced all tools from scratch, shifting every
message position and breaking messages-level cache prefix. Each resume rebuilt 87-118K tokens as cache_creation.
Anthropic tracked as inc-4747. Fixed in v2.1.90.

[If FIXED] Running v2.1.90+. Bug resolved. `--resume` usage found in config is now safe at the cache level.
[If AT RISK]
-> Update to v2.1.90+: `npm install -g @anthropic-ai/claude-code@latest`
-> Immediate: avoid `--resume` and `--continue` until updated.
[If NOT APPLICABLE] Version < 2.1.69: not affected.

---

### Bug 3: Attribution header per-session hash (v2.1.69+, no fix yet)
**Status**: [ACTIVE / MITIGATED / NOT APPLICABLE]

**Version in affected range (>= v2.1.69)**: [YES / NO]
**CLAUDE_CODE_ATTRIBUTION_HEADER set to false/0/no/off**: [YES -> MITIGATED | NO -> ACTIVE]

[If ACTIVE] Every session start and every subagent call misses the system prompt cache (~12K tokens
rebuilt at cache_creation rate). A session with 5 subagents = 6 cold misses.
-> Fix (immediate, no restart needed): add to ~/.claude/settings.json:
  {
    "env": {
      "CLAUDE_CODE_ATTRIBUTION_HEADER": "false"
    }
  }
-> Expected impact: cache hit ratio 48% -> ~99.98% (measured, source: @whiletrue0x CC#40524)

[If MITIGATED] Header already disabled. No action needed.
[If NOT APPLICABLE] Version < 2.1.69: not affected.

---

### B4/B5: Context mutation (informational, all versions)

These bugs are controlled by server-side GrowthBook flags and cannot be mitigated client-side.
No config check is possible; report as informational.

**B4: Microcompact**: Three mechanisms silently replace tool results with `[Old tool result content cleared]`
before sending to the API. The `/export` command shows original context, NOT what the model received.
Workaround: start fresh sessions periodically to reset the tool result pool.

**B5: Tool result budget cap (200K chars aggregate)**: Built-in tools (Read, Bash, Grep, Glob, Edit)
hit a 200K character cap on aggregate tool results per session. Results are truncated beyond this threshold.
MCP tools can partially override via `_meta["anthropic/maxResultSizeChars"]` (v2.1.91+, up to 500K).

---

### Multiple binaries
[List each binary found, version, type (standalone/npm), and per-bug status]

---

### Summary

| Bug | Versions | Status | Action |
|-----|----------|--------|--------|
| Bug 1: sentinel (standalone) | v2.1.36-v2.1.90 | [FIXED / SAFE / AT RISK / N/A] | [update to v2.1.91+ or "none"] |
| Bug 2: --resume/--continue | v2.1.69-v2.1.89 | [FIXED / AT RISK / N/A] | [update to v2.1.90+ or "none"] |
| Bug 3: attribution header | v2.1.69+ | [ACTIVE / MITIGATED / N/A] | [add env var or "none"] |
| B4: microcompact | all versions | INFORMATIONAL | start fresh sessions |
| B5: tool result budget 200K | all versions | INFORMATIONAL | use MCP tools for large reads |
| Stale binaries | -- | [CLEAN / PRESENT] | [remove or none] |

[If Bug 3 ACTIVE (always show this)]
Quick win: add CLAUDE_CODE_ATTRIBUTION_HEADER=false to settings.json, immediate effect, no restart needed.

[If all SAFE/MITIGATED/FIXED/N/A on Bugs 1-3]
No active cache exposure on the original CC#40524 bugs. B4/B5 are informational, monitor session length.

Track: github.com/anthropics/claude-code/issues/40524 | github.com/ArkNill/claude-code-cache-analysis
```
