# Перевірка багів кешу (CC#40524)

Проаудитуй свою конфігурацію Claude Code на три баги кешу, виявлені в березні 2026 року, які можуть непомітно роздувати витрати на API у 10-20 разів.

**Час**: ~20 секунд | **Обсяг**: версія, конфігураційні файли, CLAUDE.md, skills, hooks, профілі оболонки, усі бінарні файли claude

**Джерело**: `anthropics/claude-code#40524` | **Виявили**: `u/skibidi-toaleta-2137` (r/ClaudeAI) + `@whiletrue0x` (GitHub)

---

## Передісторія

Три незалежні баги тихо ламають кеш промптів Claude Code:

- **Баг 1** (автономний бінарний файл, v2.1.36+, граничний випадок): нативна заміна рядка в кастомному форку Bun/Zig від Anthropic вшита в Zig-конструктор HTTP-заголовків на нативному рівні: невидима з JavaScript, спрацьовує після `JSON.stringify`, але до TLS. У кожному запиті `/v1/messages` вона шукає в тілі JSON перше входження `cch=00000` і замінює його 5-символьним хешем тіла. У звичайному використанні це зачіпає лише `system[0]` (із `cache_control: null`), тож на кеш це не впливає. Кеш ламається, тільки якщо `cch=00000` потрапляє в `messages[]`: з CLAUDE.md, що обговорює цей механізм, з інструмента, який читає вихідний код бандла CC, або якщо користувач вводить це буквально. Перевірено 62 транскрипти реальних проєктів: жодного випадкового витоку в звичайному використанні.
- **Баг 2** (v2.1.69+): вкладення `deferred_tools_delta`, запроваджене у v2.1.69, призводить до того, що `messages[0]` відрізняється між новою та відновленою сесіями, незалежно ламаючи зіставлення префікса кешу при кожному `--resume` або `--continue`. Підтверджено, що воно все ще є у v2.1.88.
- **Баг 3** (v2.1.69+, найширший вплив): `cli.js` додає `x-anthropic-billing-header` як перший блок системного промпту; він містить хеш для кожної розмови (3 символи SHA-256 від першого повідомлення користувача + версії), що змінюється з кожною новою сесією та кожним викликом субагента. Через це при кожному старті сесії та кожному виклику Agent відбувається повне `cache_creation` системного промпту (~12K токенів) замість `cache_read`. A/B-тест: коефіцієнт попадання в кеш зростає з 48% до 99.98% після виправлення через змінну середовища.

Статус: часткове виправлення випущено у v2.1.88 (байти схеми інструментів). Баги 2 і 3 залишаються активними станом на v2.1.88.

---

## Інструкції

Ти аудитор. Виконай усі фази по порядку, збери кожен результат і підготуй фінальний звіт. Не пропускай фаз і не зупиняйся раніше.

---

### Фаза 1 — Версія Claude Code і спосіб встановлення

```bash
# Version check
claude --version

# All installed claude binaries
which -a claude 2>/dev/null

# Check if active binary is standalone or npm
file $(which claude) 2>/dev/null
ls -la $(which claude) 2>/dev/null
```

- Версія >= 2.1.36 І автономний бінарний файл → познач **BUG 1 MECHANISM PRESENT** (граничний випадок, спрацьовує лише якщо сентинел є в messages)
- Версія >= 2.1.69 → познач **BUG 2 RISK** і **BUG 3 RISK**
- Бінарний файл є виконуваним Mach-O / ELF → автономний → **механізм Багу 1 присутній**
- Бінарний файл є символічним посиланням на `node_modules` або містить `cli.js` → npm/npx → **Баг 1 не застосовується**

---

### Фаза 2 — Сканування сентинела (Баг 1)

Шукай буквальний рядок `cch=` в усіх статичних конфігураційних файлах. Виключи файли `.jsonl` (ефемерна історія розмов) і сам цей файл команди.

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

Познач **BUG 1 RISK**, якщо знайдено будь-який збіг поза файлами `.jsonl`.

---

### Фаза 3 — Використання resume/continue (Баг 2)

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

- Будь-який збіг у hooks/settings → познач **BUG 2 AUTOMATED** (постійний вплив)
- Будь-який збіг у commands/skills/scripts → познач **BUG 2 MANUAL** (вплив під час виклику)

---

### Фаза 4 — Перевірка заголовка атрибуції (Баг 3)

Перевір, чи змінну середовища для billing header уже вимкнено.

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

- `CLAUDE_CODE_ATTRIBUTION_HEADER` не встановлено в `false` І версія >= 2.1.69 → познач **BUG 3 ACTIVE**
- Уже встановлено в `false` → **BUG 3 MITIGATED**

---

### Фаза 5 — Перевірка кількох бінарних файлів

```bash
for b in $(which -a claude 2>/dev/null | sort -u); do
  echo "=== $b ==="
  $b --version 2>/dev/null || echo "unavailable"
  file $b 2>/dev/null
  ls -la $b 2>/dev/null
done
```

Познач будь-який автономний бінарний файл >= 2.1.69 як вразливий до всіх трьох багів.
Зазнач застарілі npm-бінарні файли, які можуть бути викликані помилково.

---

## Формат виводу

```
## Claude Code Cache Bug Audit — CC#40524

**Date**: [today]
**Active claude version**: [version]
**Install method**: [standalone binary | npm/npx | mixed]

---

### Bug 1 — Sentinel replacement (standalone binary v2.1.36+, edge case)
**Status**: [SAFE / AT RISK / NOT APPLICABLE]

**Mechanism active (standalone binary >= v2.1.36)**: [YES / NO]
**Trigger sentinel found in static config**: [YES — locations | NO]

[If AT RISK] `cch=00000` found in static config files:
- [file path]: [matching line]
→ Fix: remove the `cch=00000` string from those files.
→ Temporary workaround: `npx @anthropic-ai/claude-code` (npm package uses standard Bun, no replacement).
→ Note: sentinel in `.jsonl` conversation history is normal and harmless — only static config matters.

[If SAFE] Mechanism present in binary but no trigger in static config. Normal usage unaffected.
[If NOT APPLICABLE] npm/npx install — Bug 1 mechanism absent at the binary level.

---

### Bug 2 — Cache prefix mismatch on --resume / --continue (v2.1.69+)
**Status**: [SAFE / AT RISK (automated) / AT RISK (manual) / NOT APPLICABLE]

**Version in affected range (>= 2.1.69)**: [YES / NO]
**Automated usage (hooks/settings)**: [YES — locations | NO]
**Manual usage (commands/skills/scripts)**: [YES — locations | NO]

**Root cause**: `deferred_tools_delta` attachment introduced in v2.1.69 causes `messages[0]` to differ between fresh and resumed sessions, breaking cache prefix matching independently of Bug 1.

[If AT RISK]
→ Avoid `--resume` and `--continue` until fix ships.
→ Downgrade workaround: `npm install -g @anthropic-ai/claude-code@2.1.68` (last version before regression)

[If NOT APPLICABLE] Version < 2.1.69 — not affected.

---

### Bug 3 — Attribution header per-session hash (widest impact)
**Status**: [ACTIVE / MITIGATED / NOT APPLICABLE]

**Version in affected range (>= 2.1.69)**: [YES / NO]
**CLAUDE_CODE_ATTRIBUTION_HEADER=false already set**: [YES / NO]

[If ACTIVE] Every session start and every subagent call misses the system prompt cache (~12K tokens rebuilt at cache_creation rate).
→ Fix: add to ~/.claude/settings.json:
  {
    "env": {
      "CLAUDE_CODE_ATTRIBUTION_HEADER": "false",
      "ENABLE_TOOL_SEARCH": "false"
    }
  }
→ Expected impact: cache hit ratio 48% → ~99.98% (measured, source: @whiletrue0x CC#40524)

[If MITIGATED] Header already disabled. No action needed.
[If NOT APPLICABLE] Version < 2.1.69 — not affected.

---

### Multiple binaries
[List each binary found, version, type (standalone/npm), and per-bug status]

---

### Summary

| Bug | Impact | Status | Action |
|-----|--------|--------|--------|
| Bug 1 — sentinel in config | Edge case | [SAFE / AT RISK / N/A] | [action or "none"] |
| Bug 2 — --resume/--continue | Per-resume cache miss | [SAFE / AT RISK / N/A] | [action or "none"] |
| Bug 3 — attribution header | Every session + subagent | [ACTIVE / MITIGATED / N/A] | [action or "none"] |
| Stale binaries | — | [CLEAN / PRESENT] | [remove or none] |

[If Bug 3 ACTIVE — always show this]
⚡ Quick win: add CLAUDE_CODE_ATTRIBUTION_HEADER=false to settings.json — immediate effect, no restart needed.

[If all SAFE/MITIGATED/N/A]
✅ No active exposure. Re-run after updating Claude Code.

⚠️ Track fixes: github.com/anthropics/claude-code/issues/40524
```
