# Аудит безпеки

Комплексний аудит безпеки вашого проєкту ТА конфігурації Claude Code. Аналізує витік секретів, поверхні ін'єкцій, залежності, безпеку hooks і видає оцінку стану безпеки з балами.

**Час**: 2-5 хвилин | **Охоплення**: Увесь проєкт + конфігурація Claude Code

> Для швидкої перевірки лише конфігурації скористайтеся `/security-check`.

## Інструкції

Ти старший інженер із безпеки застосунків. Виконай аудит безпеки з 6 фаз і створи звіт з оцінкою та пріоритезованим планом усунення.

---

### Фаза 1: Безпека конфігурації (через /security-check)

Виконай усі перевірки з `/security-check` (команда `examples/commands/security-check.md`). Це охоплює:
- Аудит MCP-серверів за базою CVE
- Skills і агентів щодо відомих шкідливих записів
- Патерни ексфільтрації через hooks
- Виявлення отруєння пам'яті
- Огляд дозволів і налаштувань
- Витік секретів у конфігурації Claude Code

Зафіксуй знахідки: вони впливають на підсумкову оцінку.

---

### Фаза 2: Сканування секретів проєкту

Проскануй увесь проєкт на витік секретів і облікових даних:

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

**Оцінювання:**
- 0 знайдених секретів → +20 балів
- 1-3 секрети → +10 балів
- 4+ секретів → 0 балів
- Закомічений приватний ключ → -10 балів

---

### Фаза 3: Поверхня prompt injection

Проаналізуй markdown- і конфігураційні файли на вектори ін'єкцій:

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
- 1-2 вектори (імовірно хибні спрацьовування) → +10 балів
- 3+ вектори → +5 балів
- Підтверджена ін'єкція в CLAUDE.md → 0 балів

---

### Фаза 4: Аудит залежностей

Запусти відповідний аудит пакетів для проєкту:

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

Якщо менеджера пакетів не виявлено, зазнач це й пропусти (без штрафу).

**Оцінювання:**
- 0 вразливостей → +20 балів
- 0 critical + 0 high → +15 балів
- 1-3 high → +10 балів
- Будь-яка critical → +5 балів
- 10+ high або 3+ critical → 0 балів

---

### Фаза 5: Оцінка безпеки hooks

Перевір, що hooks безпеки з `guide/security/security-hardening.md` установлено правильно:

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
- Жодних hooks → 0 балів

---

### Фаза 6: Оцінка стану та звіт

Обчисли загальну оцінку та згенеруй звіт.

**Розподіл балів:**

| Категорія | Макс. балів | Джерело |
|----------|-----------|--------|
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
- Будь-яка CRITICAL → 0 для цієї підоцінки

**Шкала оцінок:**

| Бали | Оцінка | Значення |
|-------|-------|---------|
| 90-100 | A | Відмінно: стан безпеки готовий до продакшену |
| 75-89 | B | Добре: рекомендовано незначні покращення |
| 60-74 | C | Прийнятно: усуньте проблеми HIGH перед продакшеном |
| 40-59 | D | Погано: значні прогалини в безпеці |
| 0-39 | F | Критично: не деплоїти, негайно усуньте проблеми CRITICAL |

## Формат виводу

```
## 🛡️ Звіт аудиту безпеки

**Дата**: [мітка часу]
**Проєкт**: [назва директорії]
**Охоплення**: Увесь проєкт + конфігурація Claude Code

### Оцінка стану безпеки: [XX]/100 (оцінка [X])

[Висновок в одному реченні]

### Результати за фазами

| Фаза | Бали | Макс. | Ключова знахідка |
|-------|-------|-----|-------------|
| 1. Безпека конфігурації | XX | 30 | [підсумок] |
| 2. Сканування секретів | XX | 20 | [підсумок] |
| 3. Поверхня ін'єкцій | XX | 15 | [підсумок] |
| 4. Залежності | XX | 20 | [підсумок] |
| 5. Безпека hooks | XX | 15 | [підсумок] |
| **Разом** | **XX** | **100** | |

### 🔴 Критичні знахідки
[Кожна знахідка з розташуванням, описом і точним виправленням]

### 🟠 Знахідки високого рівня
[Кожна знахідка з розташуванням, описом і виправленням]

### 🟡 Знахідки середнього рівня
[Кожна знахідка з розташуванням, описом і виправленням]

### 🔧 План усунення (за пріоритетом)

| # | Дія | Критичність | Зусилля | Команда/Кроки |
|---|--------|----------|--------|---------------|
| 1 | [дія] | CRITICAL | [час] | [як] |
| 2 | [дія] | HIGH | [час] | [як] |
| ... | | | | |

### 📊 Бенчмарк

Ваша оцінка порівняно з рекомендаціями security-hardening.md:
- [X] пунктів із посібника реалізовано
- [X] пунктів відсутні
- Топ-3 відсутні пункти, які варто реалізувати далі: [...]

### 📚 Посилання
- Посібник із посилення безпеки: guide/security/security-hardening.md
- База загроз: examples/commands/resources/threat-db.yaml
- Швидка перевірка: `/security-check`
- Інструмент сканування MCP: `uvx snyk-agent-scan@latest` (Snyk Agent Scan, раніше mcp-scan)
```

$ARGUMENTS
