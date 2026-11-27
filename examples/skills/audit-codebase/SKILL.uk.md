---
name: audit-codebase
description: Аудит здоров'я кодової бази з оцінкою 7 категорій і планом розвитку
argument-hint: "[path] [--focus security|performance|quality]"
effort: medium
disable-model-invocation: true
---

# Аудит здоров'я кодової бази

Оцініть кодову базу за 7 категоріями здоров'я, виявіть слабкі місця й отримайте пріоритезований план розвитку. Кожна категорія оцінюється від 1 до 10 з конкретними висновками, на які можна діяти.

**Час**: 3-8 хвилин залежно від розміру кодової бази | **Охоплення**: увесь проєкт

## Інструкції

Ви старший інженерний консультант, який проводить оцінку здоров'я кодової бази. Проаналізуйте проєкт за всіма 7 категоріями (або за підмножиною, якщо `$ARGUMENTS` задає категорії), оцініть кожну й підготуйте план розвитку.

Якщо `$ARGUMENTS` містить назви категорій (наприклад, "secrets security tests"), перевіряйте лише ці категорії. Інакше перевіряйте всі 7.

---

### Категорія 1: Секрети (вага: 15%)

Шукайте жорстко прописані облікові дані, API-ключі та чутливі дані в коді.

```bash
# API keys and tokens in code
grep -rn --include="*.{js,ts,py,go,java,rb,php,yaml,yml,json,toml,env,cfg,ini,conf}" \
  -E '(?i)(api[_-]?key|apikey|secret[_-]?key|password|passwd|token|bearer)\s*[=:]\s*["'\''"][^"'\'']{8,}' \
  --exclude-dir={node_modules,vendor,.git,dist,build,target,__pycache__,.venv} . 2>/dev/null | head -20

# Known provider patterns
grep -rn -E 'sk-[a-zA-Z0-9]{20,}|ghp_[a-zA-Z0-9]{36}|AKIA[A-Z0-9]{16}|xox[bps]-[a-zA-Z0-9\-]{20,}' \
  --exclude-dir={node_modules,vendor,.git,dist,build,target} . 2>/dev/null | head -10

# .env files committed
find . -name ".env*" -not -name ".env.example" -not -path "*/node_modules/*" -not -path "*/.git/*" -type f 2>/dev/null

# .gitignore coverage
[ -f ".gitignore" ] && {
  for pattern in ".env" "*.pem" "*.key" "*.p12"; do
    grep -q "$pattern" .gitignore 2>/dev/null && echo "OK: $pattern in .gitignore" || echo "MISSING: $pattern not in .gitignore"
  done
}
```

**Оцінювання:**
- 10: жодних секретів, .gitignore покриває всі чутливі патерни, є .env.example
- 7-9: секретів у коді немає, дрібні прогалини в .gitignore
- 4-6: знайдено 1-3 потенційні секрети (можливі хибні спрацьовування), або .env закомічено
- 1-3: багато секретів у коді, закомічені приватні ключі, немає захисту через .gitignore

---

### Категорія 2: Безпека (вага: 15%)

Перевірте вразливості в стилі OWASP і небезпечні патерни.

```bash
# SQL injection patterns
grep -rn --include="*.{js,ts,py,java,go,rb,php}" \
  -E '(query|execute|exec)\s*\(\s*[`"'\''"].*\+|\$\{|%s|\.format\(' \
  --exclude-dir={node_modules,vendor,.git,dist,build,target,test,__test__} . 2>/dev/null | head -15

# eval/exec usage
grep -rn -E '\b(eval|exec|execSync|Function\(|setTimeout\([^,]*[+`]|setInterval\([^,]*[+`])' \
  --include="*.{js,ts,py}" --exclude-dir={node_modules,vendor,.git,dist} . 2>/dev/null | head -10

# Unsafe deserialization
grep -rn -E '(pickle\.loads|yaml\.load\(|JSON\.parse\(.*user|unserialize\()' \
  --exclude-dir={node_modules,vendor,.git,dist} . 2>/dev/null | head -10

# Missing input validation on routes/endpoints
grep -rn -E '(app\.(get|post|put|delete|patch)|router\.(get|post|put|delete))' \
  --include="*.{js,ts}" --exclude-dir={node_modules,.git,dist} . 2>/dev/null | wc -l
```

**Оцінювання:**
- 10: немає патернів ін'єкцій, немає eval/exec, валідація вводу на всіх ендпоінтах, заголовки CSP
- 7-9: дрібні проблеми (1-2 використання eval у коді, що не працює з користувачем)
- 4-6: деякі патерни ін'єкцій, відсутня валідація на кількох ендпоінтах
- 1-3: реальний ризик SQL-ін'єкцій, eval із вводом користувача, жодної санітизації вводу

---

### Категорія 3: Залежності (вага: 15%)

Перевірте стан пакетів, відомі CVE та актуальність.

```bash
# Node.js audit
[ -f "package-lock.json" ] && npm audit --json 2>/dev/null | jq '.metadata.vulnerabilities' 2>/dev/null
[ -f "package.json" ] && npx npm-check 2>/dev/null | tail -20

# Python
[ -f "requirements.txt" ] && pip-audit -r requirements.txt 2>/dev/null | tail -20
[ -f "pyproject.toml" ] && pip-audit 2>/dev/null | tail -20

# Rust
[ -f "Cargo.toml" ] && cargo audit 2>/dev/null | tail -20

# Go
[ -f "go.mod" ] && govulncheck ./... 2>/dev/null | tail -20

# Lockfile presence
for lockfile in package-lock.json yarn.lock pnpm-lock.yaml Cargo.lock go.sum poetry.lock; do
  [ -f "$lockfile" ] && echo "OK: $lockfile exists"
done
[ ! -f "package-lock.json" ] && [ ! -f "yarn.lock" ] && [ ! -f "pnpm-lock.yaml" ] && [ -f "package.json" ] && echo "MISSING: No lockfile for Node.js project"
```

**Оцінювання:**
- 10: нуль CVE, є lockfile, усі залежності молодші за 6 місяців
- 7-9: немає критичних/високих CVE, дрібні застарілі пакети
- 4-6: 1-3 високі CVE, або >50% залежностей застаріли на рік і більше
- 1-3: критичні CVE, немає lockfile, покинуті залежності

---

### Категорія 4: Структура (вага: 10%)

Оцініть організацію файлів, конвенції іменування та межі модулів.

```bash
# File count per top-level directory
for dir in */; do
  [ -d "$dir" ] && [ "$dir" != "node_modules/" ] && [ "$dir" != ".git/" ] && [ "$dir" != "vendor/" ] && \
    echo "$dir: $(find "$dir" -type f -not -path "*/node_modules/*" -not -path "*/.git/*" 2>/dev/null | wc -l) files"
done

# Deeply nested files (complexity indicator)
find . -type f -not -path "*/node_modules/*" -not -path "*/.git/*" -not -path "*/vendor/*" -mindepth 6 2>/dev/null | head -10

# Mixed naming conventions
find . -type f -name "*_*" -not -path "*/node_modules/*" -not -path "*/.git/*" 2>/dev/null | head -5
find . -type f -name "*-*" -not -path "*/node_modules/*" -not -path "*/.git/*" 2>/dev/null | head -5

# Circular dependency indicators (for JS/TS projects)
[ -f "package.json" ] && npx madge --circular --extensions ts,js src/ 2>/dev/null | head -20
```

**Оцінювання:**
- 10: чіткі межі модулів, послідовне іменування, немає циклічних залежностей, пласка ієрархія
- 7-9: добра структура з дрібними непослідовностями
- 4-6: змішані конвенції, деякі циклічні залежності, нечіткі межі модулів
- 1-3: немає чіткої структури, глибоко вкладені файли, поширені циклічні залежності

---

### Категорія 5: Тести (вага: 15%)

Оцініть тестове покриття, якість тестів і практики тестування.

```bash
# Test file count vs source file count
TEST_COUNT=$(find . -type f \( -name "*.test.*" -o -name "*.spec.*" -o -name "test_*" -o -path "*/test/*" -o -path "*/__tests__/*" \) \
  -not -path "*/node_modules/*" -not -path "*/.git/*" 2>/dev/null | wc -l)
SRC_COUNT=$(find . -type f \( -name "*.ts" -o -name "*.js" -o -name "*.py" -o -name "*.go" -o -name "*.java" \) \
  -not -name "*.test.*" -not -name "*.spec.*" -not -name "test_*" \
  -not -path "*/node_modules/*" -not -path "*/.git/*" -not -path "*/dist/*" 2>/dev/null | wc -l)
echo "Test files: $TEST_COUNT | Source files: $SRC_COUNT | Ratio: $(echo "scale=2; $TEST_COUNT / ($SRC_COUNT + 1)" | bc)"

# Coverage config presence
for cfg in jest.config.* vitest.config.* .nycrc .coveragerc pytest.ini setup.cfg; do
  [ -f "$cfg" ] && echo "OK: $cfg exists"
done

# Coverage report (if available)
[ -d "coverage" ] && [ -f "coverage/coverage-summary.json" ] && cat coverage/coverage-summary.json | jq '.total' 2>/dev/null

# Snapshot test count (potential maintenance burden)
find . -name "*.snap" -not -path "*/node_modules/*" 2>/dev/null | wc -l
```

**Оцінювання:**
- 10: співвідношення тестів >0.8, покриття >80%, CI запускає тести, немає застарілих snapshot
- 7-9: співвідношення тестів >0.5, покриття >60%, є конфігурація покриття
- 4-6: тести є, але прогалини очевидні, покриття не відстежується
- 1-3: співвідношення тестів <0.2 або тестів немає зовсім

---

### Категорія 6: Імпорти (вага: 10%)

Перевірте невикористані імпорти, циклічні залежності та покриття типами.

```bash
# Unused imports (TypeScript/JavaScript)
[ -f "tsconfig.json" ] && npx tsc --noEmit 2>&1 | grep -c "declared but" 2>/dev/null
[ -f "tsconfig.json" ] && npx tsc --noEmit 2>&1 | grep "declared but" | head -10

# TypeScript strict mode
[ -f "tsconfig.json" ] && grep -E '"strict"|"noImplicitAny"|"strictNullChecks"' tsconfig.json 2>/dev/null

# Python unused imports
[ -f "pyproject.toml" ] || [ -f "setup.py" ] && python -m pyflakes . 2>/dev/null | grep "imported but unused" | head -10

# Wildcard imports (code smell)
grep -rn 'import \*' --include="*.{py,ts,js}" --exclude-dir={node_modules,vendor,.git} . 2>/dev/null | head -10
```

**Оцінювання:**
- 10: нуль невикористаних імпортів, строгий режим TypeScript, немає wildcard-імпортів
- 7-9: <5 невикористаних імпортів, строгий режим увімкнено з дрібними прогалинами
- 4-6: 5-20 невикористаних імпортів, немає строгого режиму, деякі wildcard-імпорти
- 1-3: >20 невикористаних імпортів, поширені wildcard-імпорти, немає перевірки типів

---

### Категорія 7: AI-патерни (вага: 20%)

Оцініть зрілість конфігурації Claude Code і готовність до розробки за допомогою AI.

```bash
# CLAUDE.md presence and quality
[ -f "CLAUDE.md" ] && echo "OK: CLAUDE.md exists ($(wc -l < CLAUDE.md) lines)" || echo "MISSING: No CLAUDE.md"
[ -f ".claude/settings.json" ] && echo "OK: .claude/settings.json exists" || echo "MISSING: No .claude/settings.json"

# Custom commands
COMMANDS=$(find .claude/commands -name "*.md" 2>/dev/null | wc -l)
echo "Custom commands: $COMMANDS"

# Hooks
HOOKS_CFG=$(grep -c "hooks" .claude/settings.json 2>/dev/null || echo "0")
echo "Hook configurations: $HOOKS_CFG"

# Rules files
RULES=$(find .claude/rules -name "*.md" 2>/dev/null | wc -l)
echo "Rule files: $RULES"

# Agents
AGENTS=$(find .claude/agents -name "*.md" 2>/dev/null | wc -l)
echo "Agent definitions: $AGENTS"

# Skills
SKILLS=$(find .claude/skills -name "*.md" 2>/dev/null | wc -l)
echo "Skills: $SKILLS"

# .gitignore for AI artifacts
grep -q "claude" .gitignore 2>/dev/null && echo "OK: Claude patterns in .gitignore" || echo "INFO: No Claude patterns in .gitignore"
```

**Оцінювання:**
- 10: CLAUDE.md з конвенціями, налаштовані hooks, власні команди, правила, агенти
- 7-9: CLAUDE.md є і містить контекст проєкту, деякі команди чи правила
- 4-6: базовий CLAUDE.md, немає hooks чи команд
- 1-3: немає CLAUDE.md або він порожній

---

## Оцінювання та звіт

### Обчислення загального балу

```
Overall = (Secrets * 0.15) + (Security * 0.15) + (Dependencies * 0.15) +
          (Structure * 0.10) + (Tests * 0.15) + (Imports * 0.10) +
          (AI Patterns * 0.20)
```

Округліть до одного знака після коми.

### Формат виводу

```markdown
## Codebase Health Audit

**Project**: [directory name]
**Date**: [timestamp]
**Categories audited**: [all 7 or filtered subset]

### Overall Score: [X.X] / 10

| Category | Score | Weight | Weighted | Key Finding |
|----------|-------|--------|----------|-------------|
| Secrets | X/10 | 15% | X.XX | [one-line summary] |
| Security | X/10 | 15% | X.XX | [one-line summary] |
| Dependencies | X/10 | 15% | X.XX | [one-line summary] |
| Structure | X/10 | 10% | X.XX | [one-line summary] |
| Tests | X/10 | 15% | X.XX | [one-line summary] |
| Imports | X/10 | 10% | X.XX | [one-line summary] |
| AI Patterns | X/10 | 20% | X.XX | [one-line summary] |
| **Overall** | | **100%** | **X.XX** | |

### Detailed Findings

#### 🔴 Critical (fix immediately)
- [Finding with file:line reference and concrete fix]

#### 🟡 Warning (fix this week)
- [Finding with context and suggested approach]

#### 🟢 Info (nice to improve)
- [Observation with optional suggestion]

### Progression Plan

[Based on overall score, show the appropriate tier]

#### Tier 1: Foundation (current score <5, target: 5)
Focus on eliminating critical risks before anything else.

| Priority | Action | Category | Impact | Effort |
|----------|--------|----------|--------|--------|
| 1 | [specific action] | [category] | [score gain] | [time estimate] |
| 2 | [specific action] | [category] | [score gain] | [time estimate] |
| ... | | | | |

#### Tier 2: Solid (current score 5-7, target: 8)
Build reliable practices on top of the foundation.

| Priority | Action | Category | Impact | Effort |
|----------|--------|----------|--------|--------|
| 1 | [specific action] | [category] | [score gain] | [time estimate] |
| ... | | | | |

#### Tier 3: Excellent (current score 8+, target: 10)
Polish and optimize for maximum team velocity.

| Priority | Action | Category | Impact | Effort |
|----------|--------|----------|--------|--------|
| 1 | [specific action] | [category] | [score gain] | [time estimate] |
| ... | | | | |

### Quick Wins (< 30 minutes each)
1. [Action that improves score with minimal effort]
2. [...]
3. [...]
```

### Розподіл за серйозністю

Приблизно 70% висновків мають бути автоматизованими (скрипти, лінтери, перевірки CI здатні їх виявити). Решту 30% позначте як такі, що потребують людського судження, і поясніть, чому автоматизації для цих випадків недостатньо.

---

**Джерела**:
- Плагін аналізатора кодової бази Variant Systems (variantsystems.io, лютий 2026): система аналізу з 7 категорій
- OWASP Top 10 (2021): патерни для категорії безпеки
- Claude Code Security Hardening Guide: базовий рівень для категорії AI-патернів

$ARGUMENTS
