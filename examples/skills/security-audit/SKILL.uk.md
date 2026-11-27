---
name: security-audit
description: Комплексний аудит безпеки з оцінкою рівня захищеності за балами
argument-hint: "[path] [--owasp] [--verbose]"
effort: high
disable-model-invocation: true
---

# Аудит безпеки

Комплексний аудит безпеки вашого проєкту ТА конфігурації Claude Code. Аналізує витік секретів, поверхні ін'єкцій, залежності, безпеку hooks і видає оцінку рівня захищеності за балами.

**Час**: 2-5 хвилин | **Обсяг**: Увесь проєкт + конфігурація Claude Code

> Для швидкої перевірки лише конфігурації використовуйте натомість `/security-check`.

## Інструкції

Ви старший інженер із безпеки застосунків. Виконайте 6-фазовий аудит безпеки та створіть звіт з оцінкою й пріоритизованим планом усунення.

---

### Попередній крок: Встановіть контекст аудиту

**Перед виконанням будь-яких перевірок** використайте `AskUserQuestion`, щоб запитати:

1. **Середовище**: Цей код працює в production, staging чи локальній розробці?
2. **Обсяг**: Повний аудит чи конкретні області для пріоритизації?

Це критично для точності знахідок:
- **Локальна розробка**: `DEBUG=True`, CORS `*`, HTTP без TLS, файли `.env`, усе нормально. НЕ позначайте як вразливості. Натомість згадайте в інформаційному розділі "Перед виходом у production".
- **Staging**: Конфігурації мають віддзеркалювати production. Відхилення позначайте як MEDIUM.
- **Production**: Будь-яка неправильна конфігурація є реальною знахідкою з повною серйозністю.

Якщо користувач не відповідає або не впевнений, за замовчуванням вважайте **production** (консервативно).

---

### Фаза 1: Безпека конфігурації (через /security-check)

Виконайте всі перевірки з `/security-check` (команда `examples/skills/security-check/SKILL.md`). Це охоплює:
- Аудит MCP-серверів за базою CVE
- Skills і agents щодо відомих шкідливих записів
- Патерни ексфільтрації в hooks
- Виявлення отруєння пам'яті
- Огляд дозволів і налаштувань
- Викриті секрети в конфігурації Claude Code

Фіксуйте знахідки, адже вони впливають на фінальну оцінку.

---

### Фаза 2: Сканування секретів проєкту

Проскануйте весь проєкт на викриті секрети та облікові дані:

```bash
# API keys and tokens
grep -rn --include="*.{js,ts,py,go,java,rb,php,yaml,yml,json,toml,env,cfg,ini,conf}" \
  -E '(?i)(api[_-]?key|apikey|secret|password|passwd|token|bearer|auth)\s*[=:]\s*["'\''"][^"'\'']{8,}["'\''"]\s' \
  --exclude-dir={node_modules,vendor,.git,dist,build,target,__pycache__,.venv} . 2>/dev/null | head -30

# Known provider key patterns
grep -rn -E 'sk-[a-zA-Z0-9]{20,}|sk-ant-[a-zA-Z0-9]{20,}|ghp_[a-zA-Z0-9]{36}|AKIA[A-Z0-9]{16}|xox[bps]-[a-zA-Z0-9\-]{20,}' \
  --exclude-dir={node_modules,vendor,.git,dist,build,target} . 2>/dev/null | head -20

# Private keys
grep -rn 'BEGIN.*PRIVATE KEY' --exclude-dir={node_modules,vendor,.git} . 2>/dev/null

# .env files that might be committed
find . -name ".env*" -not -path "*/node_modules/*" -not -path "*/.git/*" -type f 2>/dev/null

# Check .gitignore coverage
[ -f ".gitignore" ] && {
  grep -q "\.env" .gitignore && echo "✅ .env in .gitignore" || echo "⚠️ .env NOT in .gitignore"
  grep -q "\.pem" .gitignore && echo "✅ .pem in .gitignore" || echo "⚠️ .pem NOT in .gitignore"
  grep -q "\.key" .gitignore && echo "✅ .key in .gitignore" || echo "⚠️ .key NOT in .gitignore"
}
```

**Правило проти хибних спрацювань (ОБОВ'ЯЗКОВО перед повідомленням про будь-яку знахідку секрета):**

Перед тим, як заявити знахідку секрета, виконайте ці команди перевірки:

```bash
# 1. Verify .env is actually in .gitignore (if yes, local .env is NOT a finding)
grep -n '\.env' .gitignore 2>/dev/null || echo ".env NOT in .gitignore"

# 2. Verify secrets were actually committed (empty output = no finding)
git log --all -p -- '*.env' '*.key' '*.pem' '*.secret' 2>/dev/null | grep -E '^\+.*(password|secret|api_key|token)' | head -20

# 3. Check git history for provider-specific patterns
git log --all -p 2>/dev/null | grep -E '^\+(sk-[a-zA-Z0-9]{20,}|AKIA[A-Z0-9]{16}|ghp_[a-zA-Z0-9]{36})' | head -10
```

Повідомляйте про знахідку секрета, лише якщо маєте **конкретний доказ із цих команд**. Локальний файл `.env` не є знахідкою, якщо він у `.gitignore`. Ніколи не повідомляйте "секрети можуть бути викриті" лише на підставі зіставлення патернів.

**Оцінювання:**
- Секретів не знайдено → +20 балів
- 1-3 секрети → +10 балів
- 4+ секретів → 0 балів
- Закомічено приватний ключ → -10 балів

---

### Фаза 3: Поверхня prompt injection

Проаналізуйте файли markdown і конфігурації на вектори ін'єкцій:

```bash
# Zero-width characters (invisible instructions)
grep -rPn '[\x{200B}-\x{200D}\x{FEFF}]' --include="*.md" --include="*.yaml" --include="*.json" . 2>/dev/null

# Hidden HTML comments with instructions
grep -rn '<!--' --include="*.md" . 2>/dev/null | grep -i 'ignore\|system\|admin\|instruction\|override\|forget'

# Base64 in comments (potential hidden payloads)
grep -rn -E '[#;].*[A-Za-z0-9+/]{20,}={0,2}' --include="*.py" --include="*.js" --include="*.ts" --include="*.md" \
  --exclude-dir={node_modules,vendor,.git} . 2>/dev/null | head -10

# ANSI escape sequences
grep -rPn '\x1b\[|\x1b\]|\x1b\(' --exclude-dir={node_modules,vendor,.git} . 2>/dev/null | head -10

# Null bytes
grep -rPn '\x00' --exclude-dir={node_modules,vendor,.git,dist} . 2>/dev/null | head -5

# Nested command execution in markdown/config
grep -rn -E '\$\([^)]+\)|`[^`]+`' --include="*.md" --include="*.yaml" --include="*.json" \
  --exclude-dir={node_modules,vendor,.git} . 2>/dev/null | head -10
```

**Оцінювання:**
- 0 векторів ін'єкцій → +15 балів
- 1-2 вектори (ймовірно хибні спрацювання) → +10 балів
- 3+ вектори → +5 балів
- Підтверджена ін'єкція в CLAUDE.md → 0 балів

---

### Фаза 4: Аудит залежностей

Виконайте відповідний аудит пакетів для проєкту:

```bash
# Node.js
[ -f "package-lock.json" ] && npm audit --json 2>/dev/null | jq '{total: .metadata.vulnerabilities.total, critical: .metadata.vulnerabilities.critical, high: .metadata.vulnerabilities.high}' 2>/dev/null

# Python
[ -f "requirements.txt" ] && pip-audit -r requirements.txt 2>/dev/null || [ -f "pyproject.toml" ] && pip-audit 2>/dev/null

# Rust
[ -f "Cargo.toml" ] && cargo audit 2>/dev/null

# Go
[ -f "go.mod" ] && govulncheck ./... 2>/dev/null
```

Якщо менеджер пакетів не виявлено, зазначте це й пропустіть (без штрафу).

**Оцінювання:**
- 0 вразливостей → +20 балів
- 0 critical + 0 high → +15 балів
- 1-3 high → +10 балів
- Будь-яка critical → +5 балів
- 10+ high або 3+ critical → 0 балів

---

### Фаза 5: Оцінка безпеки hooks

Перевірте, що hooks безпеки з `guide/security/security-hardening.md` правильно встановлено:

```bash
# Check for recommended security hooks
echo "=== Checking security hooks ==="

# PreToolUse hooks (should block dangerous patterns)
ls .claude/hooks/PreToolUse* 2>/dev/null || echo "⚠️ No PreToolUse hooks found"

# PostToolUse hooks (should monitor output)
ls .claude/hooks/PostToolUse* 2>/dev/null || echo "⚠️ No PostToolUse hooks found"

# Check if prompt injection detector exists
find . -path "*/hooks/*injection*" -o -path "*/hooks/*security*" -o -path "*/hooks/*scanner*" 2>/dev/null

# Check settings for hook configuration
grep -c "hooks" .claude/settings.json 2>/dev/null || echo "No hooks in settings.json"
```

**Оцінювання:**
- Встановлено security hooks PreToolUse → +10 балів
- Встановлено сканер виводу PostToolUse → +5 балів
- Hook-детектор prompt injection → +5 балів
- Жодного hook → 0 балів

---

### Фаза 6: Оцінка рівня захищеності та звіт

Обчисліть загальну оцінку та згенеруйте звіт.

**Розбивка оцінювання:**

| Категорія | Макс. балів | Джерело |
|-----------|-------------|---------|
| Безпека конфігурації (Фаза 1) | 30 | Результати /security-check |
| Сканування секретів (Фаза 2) | 20 | Секрети, знайдені в проєкті |
| Поверхня ін'єкцій (Фаза 3) | 15 | Знайдені вектори ін'єкцій |
| Залежності (Фаза 4) | 20 | Аудит вразливостей |
| Безпека hooks (Фаза 5) | 15 | Встановлені security hooks |
| **Разом** | **100** | |

**Деталі оцінювання Фази 1:**
- 0 знахідок CRITICAL → +15 балів
- 0 знахідок HIGH → +10 балів
- 0 знахідок MEDIUM → +5 балів
- Будь-яка CRITICAL → 0 для цього підбалу

**Шкала оцінок:**

| Бали | Оцінка | Значення |
|------|--------|----------|
| 90-100 | A | Відмінно: рівень безпеки, готовий до production |
| 75-89 | B | Добре: рекомендовано незначні покращення |
| 60-74 | C | Прийнятно: усуньте проблеми HIGH до production |
| 40-59 | D | Погано: суттєві прогалини в безпеці |
| 0-39 | F | Критично: не розгортайте, негайно усуньте проблеми CRITICAL |

## Формат виводу

```
## 🛡️ Security Audit Report

**Date**: [timestamp]
**Project**: [directory name]
**Scope**: Full project + Claude Code configuration

### Security Posture Score: [XX]/100 (Grade [X])

[1-sentence assessment]

### Phase Results

| Phase | Score | Max | Key Finding |
|-------|-------|-----|-------------|
| 1. Config Security | XX | 30 | [summary] |
| 2. Secrets Scan | XX | 20 | [summary] |
| 3. Injection Surface | XX | 15 | [summary] |
| 4. Dependencies | XX | 20 | [summary] |
| 5. Hook Security | XX | 15 | [summary] |
| **Total** | **XX** | **100** | |

### 🔴 Critical Findings
[Each finding with location, description, and exact fix]

### 🟠 High Findings
[Each finding with location, description, and fix]

### 🟡 Medium Findings
[Each finding with location, description, and fix]

### 🔧 Remediation Plan (Priority Order)

| # | Action | Severity | Effort | Command/Steps |
|---|--------|----------|--------|---------------|
| 1 | [action] | CRITICAL | [time] | [how] |
| 2 | [action] | HIGH | [time] | [how] |
| ... | | | | |

### 📊 Benchmark

Your score vs security-hardening.md recommendations:
- [X] items from the guide are implemented
- [X] items are missing
- Top 3 missing items to implement next: [...]

### 📚 References
- Security hardening guide: guide/security/security-hardening.md
- Threat database: examples/commands/resources/threat-db.yaml
- Quick check: `/security-check`
- MCP scan tool: `uvx snyk-agent-scan@latest` (Snyk Agent Scan, formerly mcp-scan)
```

$ARGUMENTS
