# Аудит вашого налаштування Claude Code

> Самодостатній prompt, що за один прохід перевіряє вашу конфігурацію Claude Code: пам'ять проєкту, гігієну правил, skills, агентів/команди, безпеку, MCP, команди workflow та актуальність.

**Автор**: [Florian BRUNIAUX](https://github.com/FlorianBruniaux) | Fractional Chief AI Officer

**Еталон**: [The Ultimate Claude Code Guide](https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md)

---

## 1. Що це робить

Цей prompt перетворює Claude на **оркестратора аудиту** за 8 зваженими вимірами (разом 100 балів). Він запускає швидку інвентаризацію через bash, а потім делегує кожну область спеціалізованому skill або команді, якщо вони встановлені, і повертається до вбудованих перевірок, коли ні.

| Що перевіряється | Як |
|---|---|
| Memory & Context (CLAUDE.md, правила, бюджет токенів) | Делегує `/token-audit`, якщо встановлено, інакше оцінка через bash |
| Rules Hygiene (`.claude/rules/`, чинність `paths:`) | Делегує `/eval-rules`, якщо встановлено, інакше сканування через bash |
| Skills Quality (frontmatter, effort, allowed-tools) | Делегує `/eval-skills`, якщо встановлено, інакше швидка перевірка |
| Agents/Commands Quality (16 критеріїв, оцінки A-F) | Делегує `/audit-agents-skills`, якщо встановлено, інакше перевірка |
| Security Posture (дозволи, hooks, sandbox) | Делегує `/security-check`, якщо встановлено, інакше перевірка через bash |
| MCP Ecosystem (сервери, ризик БД, безпека версій) | Вбудований bash (окремий skill не потрібен) |
| Workflow Commands (/investigate, /qa, /canary…) | Вбудоване сканування через bash |
| Freshness & Best Practices (застарілі посилання, баги кешу) | Вбудований bash + перевірки патернів |

**Чого це НЕ робить**: не замінює поглиблені інструменти, яким делегує. Використовуйте `/security-audit`, `/token-audit`, `/eval-rules` безпосередньо, коли потрібні повні подробиці щодо конкретного виміру.

**Час**: ~5-8 хв, якщо встановлені всі skills аудиту, ~3-4 хв у запасному режимі.

**Важливо**: Claude НЕ вноситиме жодних змін без вашого явного схвалення.

---

## 2. Для кого це

| Рівень | Що ви отримаєте |
|-------|-----------------|
| **Початківець** | Дізнатися, чого вам бракує, і отримати стартові шаблони |
| **Середній** | Виявити можливості оптимізації та просунуті патерни |
| **Power User** | Перевірити своє налаштування та знайти крайні випадки для доопрацювання |

**Передумови**:
- Встановлений і робочий Claude Code
- Каталог проєкту для аналізу (або лише глобальна конфігурація)
- Оболонка Bash (нативна на macOS/Linux, WSL на Windows)

**Необов'язково** (багатші результати): встановлені `/token-audit`, `/eval-rules`, `/eval-skills`, `/audit-agents-skills`, `/security-check`. Команди встановлення див. у розділі 8.

---

## 3. Як користуватися

### Крок 1: Скопіюйте prompt

Скопіюйте весь вміст блоку коду в [розділі 4](#4-prompt) нижче.

### Крок 2: Запустіть Claude Code

```bash
cd your-project-directory
claude
```

### Крок 3: Вставте та виконайте

Вставте prompt і натисніть Enter. Щоб також перевірити вашу глобальну конфігурацію `~/.claude/`, додайте `--include-global` після вставки.

### Крок 4: Перегляньте результати

Claude представить 8-вимірну картку оцінок і попросить підтвердження перед внесенням будь-яких змін.

### Примітка щодо платформи

| Платформа | Шлях до глобальної конфігурації |
|----------|-------------------|
| **macOS/Linux** | `~/.claude/` |
| **Windows** | `%USERPROFILE%\.claude\` |

---

## 4. Prompt

````markdown
# Audit My Claude Code Setup — v5.0

## Визначення області

Перевір, чи користувач додав `--include-global` до цього prompt.
- **За замовчуванням (лише проєкт)**: перевіряй `.` + `.claude/` у поточному каталозі.
- **З `--include-global`**: також перевіряй `~/.claude/` і `~/.claude.json`.

Встанови SCOPE відповідно. Усі блоки bash нижче вказують, які шляхи застосовуються для кожної області.

## Інструкції

НЕ змінюй жодних файлів. НЕ вноси жодних змін. Лише перевіряй і звітуй.

Використовуй ефективні команди bash для виявлення. Читай вміст файлів лише тоді, коли це потрібно для оцінювання.

---

## Фаза 1 — Інвентаризація (30 секунд, лише bash)

Запусти цей єдиний блок, щоб зібрати всі структурні дані одразу:

```bash
bash -c '
echo "=== SCOPE ==="
SCOPE="project"
[[ "$*" == *"--include-global"* ]] && SCOPE="project+global"
echo "Audit scope: $SCOPE"
CURRENT_DIR=$(pwd)

echo ""
echo "=== CONFIG FILES ==="
# Project
for f in ./CLAUDE.md ./.claude/CLAUDE.md ./.claude/settings.json ./.claude/settings.local.json; do
  [ -f "$f" ] && echo "✅ $f" || echo "❌ $f"
done
# Global (always check for context, even in project-only scope)
[ -f ~/.claude/CLAUDE.md ] && echo "✅ ~/.claude/CLAUDE.md (global)" || echo "❌ ~/.claude/CLAUDE.md (global)"
[ -f ~/.claude.json ] && echo "✅ ~/.claude.json (MCP config)" || echo "❌ ~/.claude.json"

echo ""
echo "=== FOLDER STRUCTURE ==="
for d in agents commands skills hooks rules styles; do
  if [ -d "./.claude/$d" ]; then
    count=$(find "./.claude/$d" -maxdepth 2 -type f | wc -l | tr -d " ")
    echo "✅ .claude/$d/ ($count files)"
  else
    echo "❌ .claude/$d/"
  fi
done

echo ""
echo "=== TECH STACK ==="
[ -f package.json ] && grep -o '"name": *"[^"]*"' package.json | head -1 | sed "s/\"name\": /nodejs: /"
[ -f pyproject.toml ] && grep "^name" pyproject.toml | head -1 | sed "s/name/python:/"
[ -f requirements.txt ] && echo "python: requirements.txt"
[ -f go.mod ] && head -1 go.mod | sed "s/module /go: /"
[ -f Cargo.toml ] && grep "^name" Cargo.toml | head -1 | sed "s/name/rust:/"
[ -f composer.json ] && echo "php: detected"
[ -f Gemfile ] && echo "ruby: detected"

echo ""
echo "=== MCP SERVERS ==="
if command -v jq &>/dev/null && [ -f ~/.claude.json ]; then
  MCP=$(jq -r --arg p "$CURRENT_DIR" '.projects[$p].mcpServers // {} | keys[]' ~/.claude.json 2>/dev/null)
  [ -n "$MCP" ] && echo "$MCP" | sed "s/^/  /" || echo "  (none for this project)"
  DB_MCP=$(echo "$MCP" | grep -iE "postgres|neon|supabase|mysql|database" || true)
  [ -n "$DB_MCP" ] && echo "  ⚠️  DB MCPs detected: $DB_MCP (verify not production)"
else
  echo "  (jq not installed or ~/.claude.json absent)"
fi

echo ""
echo "=== RULES INVENTORY ==="
RULES_DIR="./.claude/rules"
if [ -d "$RULES_DIR" ]; then
  count=$(find "$RULES_DIR" -name "*.md" | wc -l | tr -d " ")
  size=$(find "$RULES_DIR" -name "*.md" | xargs wc -c 2>/dev/null | tail -1 | awk "{print \$1}")
  echo "  $count rules files, ~$size total chars"
  echo "  Top 3 by size:"
  find "$RULES_DIR" -name "*.md" | xargs wc -c 2>/dev/null | sort -rn | head -4 | grep -v "total" | awk "{print \"    \" \$0}"
  with_paths=$(grep -rl "^paths:" "$RULES_DIR"/*.md 2>/dev/null | wc -l | tr -d " ")
  always_on=$(( count - with_paths ))
  echo "  path-scoped: $with_paths | always-on: $always_on"
else
  echo "  No .claude/rules/ directory"
fi

echo ""
echo "=== AUDIT SKILLS AVAILABLE ==="
for skill in token-audit eval-rules eval-skills audit-agents-skills; do
  found=false
  [ -f "$HOME/.claude/skills/$skill/SKILL.md" ] && found=true
  [ -f ".claude/skills/$skill/SKILL.md" ] && found=true
  $found && echo "  ✅ /$skill" || echo "  ❌ /$skill (fallback mode)"
done
for cmd in security-check security-audit; do
  found=false
  [ -f "$HOME/.claude/commands/$cmd.md" ] && found=true
  [ -f ".claude/commands/$cmd.md" ] && found=true
  [ -f "$HOME/.claude/skills/$cmd/SKILL.md" ] && found=true
  [ -f ".claude/skills/$cmd/SKILL.md" ] && found=true
  $found && echo "  ✅ /$cmd" || echo "  ❌ /$cmd (fallback mode)"
done

echo ""
echo "=== CACHE BUG INDICATORS ==="
grep -rl "disableSkillShellExecution\|--resume" .claude/ ~/.claude/ 2>/dev/null | head -3 | sed "s/^/  /" || echo "  No cache bug workarounds found"
' "$@"
```

Збережи весь цей вивід. Використовуй його для оцінювання всіх вимірів нижче.

---

## Фаза 2 — Аудит вимірів

Оціни кожен вимір. Для вимірів із делегованим skill перевір, чи цей skill доступний (за виводом Фази 1). Якщо ✅: виклич skill і використай його вивід для оцінювання. Якщо ❌: запусти вбудований запасний bash і застосуй спрощену евристику.

### Вимір 1 — Memory & Context (20 балів)

**Повний аудит** (якщо доступний `/token-audit`):
Виклич: `/token-audit`
Використай вивід Token Audit:
- Фіксований контекст <20K токенів → 18-20 балів
- 20-40K токенів → 12-17 балів
- 40-60K токенів → 6-11 балів
- >60K токенів → 0-5 балів. Відніми 2 бали, якщо бракує CLAUDE.md, 3 бали, якщо бракує глобального CLAUDE.md.

**Запасний варіант** (якщо `/token-audit` не встановлено):

```bash
GLOBAL=$(cat ~/.claude/CLAUDE.md ~/.claude/*.md 2>/dev/null | wc -c || echo 0)
PROJECT=$(wc -c < CLAUDE.md 2>/dev/null || echo 0)
RULES=$(find .claude/rules -name "*.md" 2>/dev/null | xargs cat 2>/dev/null | wc -c || echo 0)
TOTAL=$(( (GLOBAL + PROJECT + RULES) / 4 + 7500 ))
echo "Estimated fixed context: ~$TOTAL tokens (~$(( TOTAL * 100 / 200000 ))% of 200K window)"
```

Оцінювання запасного варіанта (макс. 14 балів):
- Глобальний CLAUDE.md існує й не порожній: 3 бали
- Проєктний CLAUDE.md існує: 3 бали
- Кількість правил розумна (<15 файлів): 2 бали
- Оцінка токенів <20K: 6 балів | 20-40K: 3 бали | >40K: 0 балів

### Вимір 2 — Rules Hygiene (10 балів)

**Повний аудит** (якщо доступний `/eval-rules`):
Виклич: `/eval-rules`
Візьми середню оцінку за всіма файлами правил (по 12 балів кожен). Пропорційно переведи на 10 балів.

**Запасний варіант** (якщо `/eval-rules` не встановлено):

```bash
RULES_DIR=".claude/rules"
[ -d "$RULES_DIR" ] || { echo "No rules dir"; exit 0; }
total=$(find "$RULES_DIR" -name "*.md" | wc -l | tr -d " ")
with_front=$(grep -rl "^---" "$RULES_DIR"/*.md 2>/dev/null | wc -l | tr -d " ")
with_paths=$(grep -rl "^paths:" "$RULES_DIR"/*.md 2>/dev/null | wc -l | tr -d " ")
valid_patterns=0
for f in "$RULES_DIR"/*.md; do
  pattern=$(grep -A1 "^paths:" "$f" 2>/dev/null | grep "^\s*-" | head -1 | sed "s/.*- //;s/['\"]//g")
  [ -n "$pattern" ] && ls $pattern 2>/dev/null | head -1 | grep -q . && valid_patterns=$(( valid_patterns + 1 ))
done
echo "Total: $total | With frontmatter: $with_front | With paths: $with_paths | Valid patterns: $valid_patterns"
```

Оцінювання запасного варіанта (макс. 8 балів):
- Каталог правил існує: 1 бал
- Усі файли мають YAML frontmatter: 2 бали
- Принаймні половина має поле `paths:`: 3 бали
- Жоден файл не >150 рядків (перевір через `wc -l`): 2 бали

### Вимір 3 — Skills Quality (10 балів)

**Повний аудит** (якщо доступний `/eval-skills`):
Виклич: `/eval-skills`
Візьми середню оцінку за всіма файлами skills (по 14 балів кожен). Пропорційно переведи на 10 балів.

**Запасний варіант** (якщо `/eval-skills` не встановлено):

```bash
SKILLS_DIR=".claude/skills"
[ -d "$SKILLS_DIR" ] || { echo "No skills dir (0 pts)"; exit 0; }
total=$(find "$SKILLS_DIR" -name "SKILL.md" | wc -l | tr -d " ")
with_effort=$(grep -rl "^effort:" "$SKILLS_DIR"/*/SKILL.md 2>/dev/null | wc -l | tr -d " ")
with_tools=$(grep -rl "^allowed-tools:" "$SKILLS_DIR"/*/SKILL.md 2>/dev/null | wc -l | tr -d " ")
with_desc=$(grep -rl "^description:" "$SKILLS_DIR"/*/SKILL.md 2>/dev/null | wc -l | tr -d " ")
echo "Skills: $total | effort field: $with_effort | allowed-tools: $with_tools | description: $with_desc"
```

Оцінювання запасного варіанта (макс. 8 балів):
- Каталог skills існує: 1 бал
- Усі SKILL.md мають поле `description:`: 2 бали
- Усі SKILL.md мають поле `effort:`: 3 бали
- Усі SKILL.md мають поле `allowed-tools:`: 2 бали

### Вимір 4 — Agents/Commands Quality (10 балів)

**Повний аудит** (якщо доступний `/audit-agents-skills`):
Виклич: `/audit-agents-skills`
Візьми загальну оцінку з його звіту (оцінка/100). Помнож на 0.10, щоб отримати бали з 10.

**Запасний варіант** (якщо `/audit-agents-skills` не встановлено):

```bash
agents=$(find .claude/agents -name "*.md" 2>/dev/null | wc -l | tr -d " ")
commands=$(find .claude/commands -name "*.md" 2>/dev/null | wc -l | tr -d " ")
skills=$(find .claude/skills -name "SKILL.md" 2>/dev/null | wc -l | tr -d " ")
with_front=$(find .claude/agents .claude/commands .claude/skills -name "*.md" 2>/dev/null | xargs grep -l "^---" 2>/dev/null | wc -l | tr -d " ")
with_desc=$(find .claude/agents .claude/commands .claude/skills -name "*.md" 2>/dev/null | xargs grep -l "^description:" 2>/dev/null | wc -l | tr -d " ")
# Check argument-hint on legacy commands still using $ARGUMENTS
uses_args=$(find .claude/commands -name "*.md" 2>/dev/null | xargs grep -l '\$ARGUMENTS' 2>/dev/null | wc -l | tr -d " ")
with_hint=$(find .claude/commands -name "*.md" 2>/dev/null | xargs grep -l 'argument-hint' 2>/dev/null | wc -l | tr -d " ")
echo "Agents: $agents | Commands: $commands | Skills: $skills | With frontmatter: $with_front | With description: $with_desc"
echo "Commands using \$ARGUMENTS: $uses_args | With argument-hint: $with_hint"
```

Оцінювання запасного варіанта (макс. 8 балів):
- Є агенти, команди або skills: 2 бали
- Усі мають YAML frontmatter: 2 бали
- Усі мають поле `description:`: 2 бали
- `argument-hint:` присутній у всіх застарілих командах, що використовують `$ARGUMENTS`: 2 бали

### Вимір 5 — Security Posture (20 балів)

**Повний аудит** (якщо доступний `/security-check`):
Виклич: `/security-check`
Зістав його висновки з 20 балами:
- Немає критичних висновків: 18-20 балів
- 1-2 середні висновки: 12-17 балів
- 3+ висновки або будь-який критичний: 0-11 балів

**Запасний варіант** (якщо `/security-check` не встановлено):

```bash
# permissions.deny check
echo "=== Permissions Deny ==="
for setting in ".claude/settings.json" "~/.claude/settings.json"; do
  [ -f "$setting" ] && {
    echo "File: $setting"
    grep -E "\.env|\.pem|credentials|secrets" "$setting" 2>/dev/null && echo "  ✅ Sensitive patterns found" || echo "  ❌ No .env/.pem/credentials blocked"
    grep -i "sandbox\|failIfUnavailable" "$setting" 2>/dev/null | head -3 | sed "s/^/  /"
  }
done

echo ""
echo "=== Hooks ==="
if [ -d ".claude/hooks" ]; then
  hooks=$(ls .claude/hooks/*.sh 2>/dev/null | wc -l | tr -d " ")
  pretool=$(grep -rl "PreToolUse" .claude/hooks/ 2>/dev/null | wc -l | tr -d " ")
  echo "  Hooks: $hooks | PreToolUse: $pretool"
else
  echo "  ❌ No hooks directory"
fi

echo ""
echo "=== Dangerous Patterns ==="
# Check for hardcoded tokens/keys in config
grep -rn "sk-\|ghp_\|xox[baprs]-\|AKIA" .claude/ CLAUDE.md 2>/dev/null | grep -v "example\|sample\|template" | head -5 || echo "  No obvious secrets found"
```

Оцінювання запасного варіанта (макс. 17 балів):
- `.env*` заблоковано в `permissions.deny`: 4 бали
- `*.pem` і `credentials*` також заблоковано: 3 бали
- Існує принаймні один hook `PreToolUse`: 4 бали
- Sandbox налаштовано (`failIfUnavailable`): 3 бали
- Немає захардкоджених секретів у конфігурації: 3 бали

### Вимір 6 — MCP Ecosystem (10 балів)

Лише вбудований bash (окремого skill для цього виміру немає):

```bash
CURRENT_DIR=$(pwd)
echo "=== MCP Servers for this project ==="
if command -v jq &>/dev/null && [ -f ~/.claude.json ]; then
  jq -r --arg p "$CURRENT_DIR" '
    .projects[$p].mcpServers // {} | to_entries[] |
    "\(.key): \(.value.command // .value.url // "configured")"
  ' ~/.claude.json 2>/dev/null || echo "  No project-specific MCPs"

  echo ""
  echo "=== DB MCP Risk ==="
  jq -r --arg p "$CURRENT_DIR" '.projects[$p].mcpServers // {} | keys[]' ~/.claude.json 2>/dev/null \
    | grep -iE "postgres|neon|supabase|mysql|database|mongo" \
    | sed "s/^/  ⚠️  /" || echo "  No DB MCPs found"

  echo ""
  echo "=== Guide MCP ==="
  jq -r --arg p "$CURRENT_DIR" '.projects[$p].mcpServers // {} | keys[]' ~/.claude.json 2>/dev/null \
    | grep -iE "claude-code-ultimate-guide|ccguide" \
    | sed "s/^/  ✅ /" || echo "  ❌ Guide MCP not installed"
else
  echo "  (install jq for MCP analysis)"
fi
```

Оцінювання (макс. 10 балів):
- Налаштовано принаймні 1 MCP: 3 бали
- Є MCP документації (Context7 чи подібний): 2 бали
- Немає MCP бази даних, або MCP бази даних чітко обмежений dev/staging: 3 бали
- Guide MCP встановлено: 2 бали

### Вимір 7 — Workflow Commands (10 балів)

```bash
echo "=== Core Workflow Skills/Commands ==="
for cmd in investigate qa canary land-and-deploy review-pr; do
  found=false
  [ -f ".claude/commands/$cmd.md" ] && found=true
  [ -f "$HOME/.claude/commands/$cmd.md" ] && found=true
  [ -f ".claude/skills/$cmd/SKILL.md" ] && found=true
  [ -f "$HOME/.claude/skills/$cmd/SKILL.md" ] && found=true
  $found && echo "  ✅ /$cmd" || echo "  ❌ /$cmd"
done

echo ""
echo "=== Additional Debug/Deploy Skills/Commands ==="
for cmd in ship commit release-notes diagnose; do
  found=false
  [ -f ".claude/commands/$cmd.md" ] && found=true
  [ -f "$HOME/.claude/commands/$cmd.md" ] && found=true
  [ -f ".claude/skills/$cmd/SKILL.md" ] && found=true
  [ -f "$HOME/.claude/skills/$cmd/SKILL.md" ] && found=true
  $found && echo "  ✅ /$cmd" || echo "  ❌ /$cmd"
done
```

Оцінювання: 2 бали за кожну наявну базову команду (`/investigate`, `/qa`, `/canary`, `/land-and-deploy`, `/review-pr`). Макс. 10 балів.

### Вимір 8 — Freshness & Best Practices (10 балів)

```bash
echo "=== Deprecated Model References ==="
grep -rn "claude-3-haiku\|gpt-3.5\|claude-2\b\|claude-instant\|claude-3-5-sonnet\b" \
  .claude/ CLAUDE.md ~/.claude/CLAUDE.md 2>/dev/null | grep -v ".git" | head -8 \
  || echo "  No deprecated model names found"

echo ""
echo "=== Config Freshness ==="
git log --oneline -1 --format="  Last commit: %ar (%h)" 2>/dev/null || echo "  (not a git repo)"

echo ""
echo "=== Cache Bug Workarounds ==="
# Bug 2 HIGH: --resume causes 87-118K token re-announcement
grep -rn "disableSkillShellExecution" ~/.claude/settings.json .claude/settings.json 2>/dev/null \
  | sed "s/^/  /" || echo "  disableSkillShellExecution: not set"

echo ""
echo "=== argument-hint Coverage (legacy commands) ==="
missing=0
for f in $(find .claude/commands -name "*.md" 2>/dev/null); do
  grep -q '\$ARGUMENTS' "$f" && ! grep -q "argument-hint" "$f" && {
    echo "  ⚠️  Missing argument-hint: $f"
    missing=$(( missing + 1 ))
  }
done
[ $missing -eq 0 ] && echo "  ✅ All commands using \$ARGUMENTS have argument-hint (skills use effort: field instead)"

echo ""
echo "=== Hook Profiles (env vars) ==="
grep -rn "CLAUDE_HOOK_PROFILE\|HOOK_PROFILE" .claude/ CLAUDE.md 2>/dev/null | head -3 | sed "s/^/  /" || echo "  No hook profiles configured"
```

Оцінювання (макс. 10 балів):
- Немає застарілих назв моделей: 3 бали
- Активність git за останні 90 днів (або це не репозиторій git): 2 бали
- `disableSkillShellExecution: false` АБО не використовується патерн `--resume`: 3 бали
- Усі команди, що використовують `$ARGUMENTS`, мають `argument-hint:`: 2 бали

---

## Фаза 3 — Єдиний звіт

Створи звіт точно за такою структурою:

### Executive Summary

Вкажи:
- **Total Score**: X/100
- **Maturity Tier**: Starter (<40) | Growing (40-59) | Established (60-79) | Optimized (80+)
- **Detected Stack**: [із Фази 1]
- **Top 3 Quick Wins**: прогалини з найвищою віддачею, які можна виправити менш ніж за 15 хв кожна
- **Top 3 Critical Gaps**: відсутні елементи з найвищою серйозністю

### Dimension Scorecard

| # | Вимір | Бал | Макс | Статус | Ключовий висновок |
|---|-----------|-------|-----|--------|-------------|
| 1 | Memory & Context | X | 20 | ✅/⚠️/❌ | висновок одним рядком |
| 2 | Rules Hygiene | X | 10 | ✅/⚠️/❌ | висновок одним рядком |
| 3 | Skills Quality | X | 10 | ✅/⚠️/❌ | висновок одним рядком |
| 4 | Agents/Commands Quality | X | 10 | ✅/⚠️/❌ | висновок одним рядком |
| 5 | Security Posture | X | 20 | ✅/⚠️/❌ | висновок одним рядком |
| 6 | MCP Ecosystem | X | 10 | ✅/⚠️/❌ | висновок одним рядком |
| 7 | Workflow Commands | X | 10 | ✅/⚠️/❌ | висновок одним рядком |
| 8 | Freshness & Best Practices | X | 10 | ✅/⚠️/❌ | висновок одним рядком |
| | **TOTAL** | **X** | **100** | | |

Пороги статусів: ✅ ≥80% від максимуму, ⚠️ 50-79%, ❌ <50%.

### Detailed Findings

Згрупуй за виміром. Для кожної прогалини (❌ або ⚠️):

```
**[Dimension N — Name]**
Gap: [що відсутнє або неоптимально]
Impact: [що ламається або погіршується без цього]
Fix: [конкретна дія зі шляхом до файлу]
```

### Stack-Specific Templates

Запропонуй щонайбільше 3 шаблони, обрані за найвпливовішими прогалинами для виявленого стека. Включай лише шлях до файлу + стартовий вміст. Не повторюй наявний вміст.

### Deepen Your Audit

Перелічи, які skills аудиту не встановлено і що вони відкрили б:

```
Skills not installed — install for deeper analysis:

# token-audit (Dimension 1 — adds rule classification, hook overhead analysis)
mkdir -p ~/.claude/skills/token-audit
curl -sL https://raw.githubusercontent.com/FlorianBruniaux/claude-code-ultimate-guide/main/examples/skills/token-audit/SKILL.md \
  > ~/.claude/skills/token-audit/SKILL.md

# eval-rules (Dimension 2 — adds glob validation, interactive review)
mkdir -p ~/.claude/skills/eval-rules
curl -sL https://raw.githubusercontent.com/FlorianBruniaux/claude-code-ultimate-guide/main/examples/skills/eval-rules/SKILL.md \
  > ~/.claude/skills/eval-rules/SKILL.md

# eval-skills (Dimension 3 — adds 14-pt scoring per skill)
mkdir -p ~/.claude/skills/eval-skills
curl -sL https://raw.githubusercontent.com/FlorianBruniaux/claude-code-ultimate-guide/main/examples/skills/eval-skills/SKILL.md \
  > ~/.claude/skills/eval-skills/SKILL.md

# audit-agents-skills (Dimension 4 — adds grades A-F, comparative analysis)
mkdir -p ~/.claude/skills/audit-agents-skills
curl -sL https://raw.githubusercontent.com/FlorianBruniaux/claude-code-ultimate-guide/main/examples/skills/audit-agents-skills/SKILL.md \
  > ~/.claude/skills/audit-agents-skills/SKILL.md

# security-check (Dimension 5 — scans against threat-db, 55 CVEs, 24 techniques)
mkdir -p ~/.claude/skills/security-check
curl -sL https://raw.githubusercontent.com/FlorianBruniaux/claude-code-ultimate-guide/main/examples/skills/security-check/SKILL.md \
  > ~/.claude/skills/security-check/SKILL.md

# Alternative for dimension 1 — context-evaluator.ai
# Zero-install LLM-native audit: 17 AI evaluators for CLAUDE.md/AGENTS.md,
# automated .patch remediation. Complements /token-audit with deeper rule analysis.
# Visit: https://context-evaluator.ai
```

---

## Фаза 4 — Запит на підтвердження

Після подання звіту запитай:

"Implement the top 3 quick wins? Reply:
- **yes** → I'll implement all three
- **high** → only critical gaps (Dimensions 5 and 1 if ❌)
- **1, 3** → specific items by number from findings
- **none** → keep the report, no changes"

Дочекайся явної відповіді користувача, перш ніж щось робити.
````

---

## 5. Чого очікувати

### Приклад executive summary

```
## Executive Summary

Total Score: 52/100 — Growing

Detected Stack: TypeScript + Next.js + Prisma

Top 3 Quick Wins:
- Add permissions.deny for .env* (15 min) → fixes Dimension 5 critical gap
- Install /investigate and /qa commands (5 min) → +4 pts on Dimension 7
- Add paths: frontmatter to 3 always-on rules (20 min) → reduces fixed context ~3K tokens

Top 3 Critical Gaps:
1. ❌ Security — no permissions.deny, no PreToolUse hooks (0/20)
2. ⚠️ Memory — project CLAUDE.md missing, global is 22K tokens (8/20)
3. ❌ Workflow — 3/5 core commands absent (4/10)
```

### Приклад картки оцінок за вимірами

| # | Вимір | Бал | Макс | Статус | Ключовий висновок |
|---|-----------|-------|-----|--------|-------------|
| 1 | Memory & Context | 8 | 20 | ⚠️ | 22K фіксованих токенів, немає проєктного CLAUDE.md |
| 2 | Rules Hygiene | 7 | 10 | ⚠️ | 4 правила, жодне не має поля paths: |
| 3 | Skills Quality | 8 | 10 | ✅ | 3 skills, усі мають effort + allowed-tools |
| 4 | Agents/Commands Quality | 6 | 10 | ⚠️ | 8 команд, у 2 немає argument-hint |
| 5 | Security Posture | 0 | 20 | ❌ | Немає правил deny, немає hooks |
| 6 | MCP Ecosystem | 7 | 10 | ✅ | Налаштовано Context7 + Sequential |
| 7 | Workflow Commands | 4 | 10 | ⚠️ | /investigate ✅ /qa ❌ /canary ❌ |
| 8 | Freshness & Best Practices | 12 | 10 | — | обмежено максимумом |
| | **TOTAL** | **52** | **100** | ⚠️ | |

---

## 6. Розуміння результатів

### Глосарій

| Термін | Визначення |
|------|------------|
| **Memory Files** | Файли CLAUDE.md, що надають Claude постійний контекст між сесіями |
| **Context Budget** | Загальна вартість постійних (always-on) токенів до початку будь-якої задачі. Пороги: зелений <20K, жовтий 20-40K, червоний >40K |
| **Rules (auto-loaded)** | Файли `.claude/rules/*.md`, що завантажуються на початку кожної сесії. Файли з `paths:` завантажуються лише тоді, коли читається відповідний файл |
| **paths: frontmatter** | Поле в YAML правила, що обмежує правило певними шаблонами файлів і зменшує постійні накладні витрати |
| **Eval Skill** | Спеціалізований skill, що перевіряє одну область: `eval-skills`, `eval-rules`, `token-audit`, `audit-agents-skills` |
| **Single Source of Truth** | Патерн, за якого конвенції документуються один раз і підключаються через `@path` |
| **Tool SEO** | Написання описів агентів/команд так, щоб Claude автоматично обирав правильний інструмент |
| **MCP Servers** | Model Context Protocol: зовнішні інструменти, що розширюють можливості Claude. Конфігурація зберігається в `~/.claude.json` для кожного проєкту |
| **Hook Profiles** | Рівні безпеки hooks minimal/standard/strict, що перемикаються змінною середовища (додано у v3.38.0) |
| **PreToolUse** | Hook, що спрацьовує ПЕРЕД тим, як Claude виконує інструмент: використовується для перевірок безпеки та воріт схвалення |
| **effort: field** | Поле frontmatter skill із сигналом складності low/medium/high: Claude використовує його для розподілу бюджету мислення |
| **argument-hint** | Поле frontmatter, що показує текст-підказку в меню slash-команд для команд, які використовують `$ARGUMENTS` |
| **Threat Database** | `examples/commands/resources/threat-db.yaml`: версіоновані CVE, техніки атак, записи IOC та мінімальні безпечні версії |
| **Cache Bug #40524** | Баг 2 (HIGH): `--resume` спричиняє повне повторне оголошення контексту (87-118K токенів перебудовується при кожному відновленні) |
| **Scope Drift** | Коли PR змінює файли поза заявленим наміром плану. Виявляється порівнянням `~/.claude/plans/` і `git diff --stat` |
| **Fix-First Heuristic** | Патерн рецензування: автоматично виправляти механічні проблеми, питати про рішення, що потребують судження, щодо безпеки/дизайну |
| **LLM Output Trust Boundary** | Категорія рецензування для значень, згенерованих ШІ й записаних до БД без валідації формату |
| **managed-settings.d/** | Корпоративний drop-in каталог для правил керування, що перекривають налаштування користувача (додано у v2.1.83) |
| **Routines** | Заплановані задачі в хмарі з 3 типами тригерів: розклад, API, події GitHub (запущено в квітні 2026) |
| **Context Zones** | <70% оптимально, 75% тригер auto-compact, 85% рекомендовано передачу |
| **Sandbox** | Ізоляція на рівні ОС (контейнер Docker або нативна на рівні процесу). Налаштовується в settings.json |
| **Iron Law** | Принцип налагодження: жодних виправлень без попереднього дослідження першопричини. Див. `/investigate` |

### Пороги оцінок

| Оцінка | Рівень | Що це означає |
|-------|------|----------------|
| 80-100 | Optimized | Конфігурація міцна. Зосередьтеся на Freshness і крайніх випадках |
| 60-79 | Established | Добрий фундамент. Заповніть виміри з ⚠️ |
| 40-59 | Growing | Основні елементи є, але кілька прогалин. Дотримуйтесь Quick Wins |
| <40 | Starter | Почніть із Виміру 5 (Security) і 1 (Memory) |

### Значки статусу

| Значок | Значення |
|------|---------|
| ✅ | ≥80% від максимуму балів для цього виміру |
| ⚠️ | 50-79% від максимуму балів |
| ❌ | <50% від максимуму балів |

---

## 7. Типові проблеми

### "Audit skills not installed"

**Причина**: спеціалізовані skills необов'язкові й типово не доступні глобально.

**Що відбувається**: prompt працює в запасному режимі для цього виміру. Оцінки обмежені нижче (8 балів замість 10 для деяких вимірів). Результати все одно придатні до дії, лише менш детальні.

**Виправлення**: використайте команди встановлення з розділу «Deepen Your Audit» у звіті. Кожен skill встановлюється ~1 хв і одразу покращує майбутні аудити.

### "Claude didn't find my files"

**Причина**: неправильний робочий каталог або відмінності шляхів між платформами.

**Виправлення**:
- Переконайтеся, що запускаєте `claude` з кореня проєкту
- У Windows шляхи використовують `%USERPROFILE%\.claude\`, а не `~/.claude/`

### "Score seems off"

**Причина**: оцінювання в запасному режимі спрощене: воно не може перевірити чинність glob, виконати 14-бальні перевірки skills чи зіставити з базою загроз.

**Виправлення**: встановіть відповідні skills аудиту (див. «Deepen Your Audit»). Запустіть повторно, щоб отримати точні оцінки за вимірами.

### "Too many recommendations"

**Причина**: перший аудит проєкту без конфігурації Claude Code.

**Виправлення**: скористайтеся Quick Wins з Executive Summary. Впровадьте ці три. Проведіть аудит повторно. Будуйте поступово.

### "Claude made changes without asking"

**Причина**: Фазу 4 з підтвердженням не було досягнуто або її пропущено.

**Виправлення**: переконайтеся, що скопіювали повний prompt разом із Фазою 4. Використовуйте Plan Mode (`Shift+Tab` двічі) для додаткової безпеки перед вставкою.

---

## 8. Пов'язані ресурси

**Додаткові інструменти аудиту** (глибше в окремі виміри):

| Інструмент | Вимір | Встановлення |
|------|-----------|---------|
| `/token-audit` | Memory & Context | `mkdir -p ~/.claude/skills/token-audit && curl -sL .../examples/skills/token-audit/SKILL.md > ...` |
| `/eval-rules` | Rules Hygiene | Той самий шаблон |
| `/eval-skills` | Skills Quality | Той самий шаблон |
| `/audit-agents-skills` | Agents/Commands | Той самий шаблон |
| `/security-check` | Security Posture (швидко, ~30 с) | `mkdir -p ~/.claude/skills/security-check && curl -sL ...` |
| `/security-audit` | Security Posture (повний, 2-5 хв, оцінка /100) | Той самий шаблон |
| [`tools/context-audit-prompt.md`](context-audit-prompt.uk.md) | Поглиблений розбір context engineering | Самодостатній prompt, встановлення не потрібне |
| [`tools/onboarding-prompt.md`](onboarding-prompt.uk.md) | Налаштування з нуля | Самодостатній prompt, встановлення не потрібне |
| [context-evaluator.ai](https://context-evaluator.ai) | Memory & Context (альтернатива): LLM-native, 17 оцінювачів, авто `.patch` | Вебінструмент без встановлення |

**Довідкові документи**:
- [The Ultimate Claude Code Guide](../guide/ultimate-guide.uk.md): повний довідник
- [Cheatsheet](../guide/cheatsheet.uk.md): швидка щоденна довідка
- [Security Hardening](../guide/security/security-hardening.uk.md): патерни безпеки для продакшну
- [Context Engineering](../guide/core/architecture.uk.md): стратегії бюджету токенів
- [Claude Code Official Docs](https://docs.anthropic.com/en/docs/claude-code): документація Anthropic

**Для інтеграції CI/CD** (вивід JSON, пакетний режим): [`examples/scripts/audit-scan.sh`](../examples/scripts/audit-scan.sh)

---

*Версія 5.2 (посібник v3.41.0+) | v5.2: виявлення skills оновлено для уніфікації skills і commands у CC 2.1.3: bash для Вимірів 4/7/8 тепер перевіряє і `.claude/skills/`, і `.claude/commands/`; шлях встановлення security-check виправлено на канонічний SKILL.md. v5.1: додано context-evaluator.ai. v5.0: перероблено з контрольного списку на оркестратор із 8 зваженими вимірами.*
