---
name: security
description: Швидка оцінка безпеки з фокусом на вразливостях OWASP Top 10
argument-hint: "[path] [--depth quick|full]"
effort: medium
when_to_use: "Використовуйте при рев'ю коду на вразливості безпеки або перед мерджем чутливих змін."
disable-model-invocation: true
---

# Швидкий аудит безпеки

Швидка оцінка безпеки з фокусом на вразливостях OWASP Top 10.

## Призначення

Виконайте швидке сканування безпеки, щоб виявити поширені вразливості:
- Захардкожені секрети та облікові дані
- Ризики SQL-ін'єкцій
- Вразливості XSS
- Небезпечні залежності
- Проблеми автентифікації/авторизації

## Інструкції

### Крок 1: Сканування секретів

```bash
# Common secret patterns
grep -rn --include="*.{js,ts,py,go,java,rb,php,env}" \
  -E "(password|secret|api_key|apikey|token|auth|credential).*[=:].*['\"][^'\"]{8,}['\"]" \
  --exclude-dir={node_modules,vendor,.git,dist,build} . 2>/dev/null | head -20

# .env files that might be committed
find . -name ".env*" -not -path "*/node_modules/*" -type f 2>/dev/null

# Check if secrets are gitignored
[ -f ".gitignore" ] && grep -q "\.env" .gitignore && echo "✅ .env in .gitignore" || echo "⚠️ .env NOT in .gitignore"
```

### Крок 2: Вразливості ін'єкцій

```bash
# SQL injection patterns (raw queries with string concat)
grep -rn --include="*.{js,ts,py,go,java,php}" \
  -E "(query|execute|raw|sql).*\+.*\$|f['\"].*SELECT|\.format\(.*SELECT" \
  --exclude-dir={node_modules,vendor,.git} . 2>/dev/null | head -15

# Command injection patterns
grep -rn --include="*.{js,ts,py,go,rb,php}" \
  -E "(exec|spawn|system|shell_exec|popen)\s*\(" \
  --exclude-dir={node_modules,vendor,.git} . 2>/dev/null | head -15
```

### Крок 3: Патерни XSS

```bash
# Dangerous innerHTML/dangerouslySetInnerHTML usage
grep -rn --include="*.{js,ts,jsx,tsx,vue}" \
  -E "(innerHTML|dangerouslySetInnerHTML|v-html)" \
  --exclude-dir={node_modules,.git,dist} . 2>/dev/null | head -15

# Unescaped template literals in HTML context
grep -rn --include="*.{js,ts,jsx,tsx}" \
  -E "\`.*\$\{.*\}.*<" \
  --exclude-dir={node_modules,.git,dist} . 2>/dev/null | head -10
```

### Крок 4: Перевірка залежностей

```bash
# Check for known vulnerabilities in npm packages
[ -f "package-lock.json" ] && npm audit --json 2>/dev/null | jq '{vulnerabilities: .metadata.vulnerabilities}' 2>/dev/null

# Check for outdated packages with security issues
[ -f "package.json" ] && npm outdated --json 2>/dev/null | jq 'to_entries | map(select(.value.current != .value.latest)) | length' 2>/dev/null
```

### Крок 5: Проблеми auth і сесій

```bash
# Hardcoded JWT secrets
grep -rn --include="*.{js,ts,py,go}" \
  -E "(jwt|JWT).*secret.*[=:].*['\"].{8,}['\"]" \
  --exclude-dir={node_modules,vendor,.git} . 2>/dev/null

# Missing CSRF protection patterns
grep -rn --include="*.{js,ts,py}" \
  -E "(POST|PUT|DELETE|PATCH).*fetch|axios\.(post|put|delete|patch)" \
  --exclude-dir={node_modules,vendor,.git} . 2>/dev/null | head -10
```

## Формат виводу

---

### 🛡️ Звіт про аудит безпеки

**Дата сканування**: [часова мітка]
**Обсяг**: [проскановано каталог]

### 🔴 Критичні проблеми

| Проблема | Розташування | Опис |
|----------|--------------|------|
| [тип] | [file:line] | [стислий опис] |

### 🟠 Висока серйозність

| Проблема | Розташування | Рекомендація |
|----------|--------------|--------------|
| [тип] | [file:line] | [пропозиція виправлення] |

### 🟡 Середня серйозність

| Проблема | Розташування | Примітка |
|----------|--------------|----------|
| [тип] | [file:line] | [контекст] |

### 📊 Підсумок

- **Критичні**: X проблем
- **Високі**: X проблем
- **Середні**: X проблем
- **Залежності**: X вразливостей

### 🔧 Швидкі виправлення

1. [Виправлення найвищого пріоритету з командою/кодом]
2. [Другий пріоритет]
3. [Третій пріоритет]

---

## Рівні серйозності

| Рівень | Приклади | Дія |
|--------|----------|-----|
| 🔴 Critical | Захардкожені продакшен-секрети, SQL-ін'єкція | Виправити негайно |
| 🟠 High | Відсутня auth, вектори XSS | Виправити до деплою |
| 🟡 Medium | Застарілі залежності, відсутній CSRF | Запланувати усунення |
| 🟢 Low | Порушення best practices | Відстежувати для покращення |

## Використання

**Повний аудит:**
```
/security
```

**Сфокусуватися на конкретній області:**
```
/security auth
/security deps
/security injection
```

**Конкретний файл/каталог:**
```
/security src/api/
```

## Примітки

- Це швидке евристичне сканування, а не вичерпний аудит безпеки
- Для продакшен-систем доповнюйте спеціалізованими інструментами (Snyk, SonarQube, OWASP ZAP)
- Можливі хибні спрацювання - перевіряйте знахідки вручну
- Див. `examples/hooks/security-hooks.sh` щодо автоматичних pre-commit перевірок безпеки

$ARGUMENTS
