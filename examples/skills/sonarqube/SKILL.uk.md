---
name: sonarqube
description: Аналізує проблеми якості SonarCloud для конкретного PR
argument-hint: "[project_key]"
effort: medium
when_to_use: "Use when running SonarQube analysis or interpreting SonarQube findings."
disable-model-invocation: true
---

# Аналіз SonarQube

Аналізує проблеми якості SonarCloud для конкретного PR. Генерує повний звіт із метриками, головними порушниками та планом дій.

**Основний принцип:** лише аналіз = жодних змін коду, суто інсайти.

## Процес

1. **Перевірте токен**: перевірте змінну середовища `$SONARQUBE_TOKEN`
2. **Отримайте проблеми**: викличте SonarCloud API для проблем PR
3. **Розберіть дані**: згрупуйте за серйозністю, типом, файлом, правилом
4. **Згенеруйте звіт**: структурований вивід із планом дій
5. **Прибирання**: видаліть тимчасові файли

## Передумови

### Змінна середовища

```bash
# Set SonarQube token (add to ~/.bashrc or ~/.zshrc)
export SONARQUBE_TOKEN="your_token_here"

# Verify token is set
echo $SONARQUBE_TOKEN
```

**Щоб отримати токен:**
1. Перейдіть у SonarCloud → My Account → Security
2. Згенеруйте новий токен
3. Скопіюйте його й експортуйте як змінну середовища

### Конфігурація проєкту

Налаштуйте дані свого проєкту SonarCloud:

```bash
# Add to project's CLAUDE.md or as environment variables
SONAR_ORGANIZATION="your-org-name"
SONAR_PROJECT_KEY="your-org_your-project"
SONAR_BASE_URL="https://sonarcloud.io/api"
```

**Якщо не задано:** попросіть користувача вказати організацію та ключ проєкту.

## Отримання проблем

**Важливо:** прямий curl із `-u "$SONARQUBE_TOKEN:"` не працює в zsh через розбір автентифікації. Використовуйте обгортку у вигляді bash-скрипта:

```bash
# Create temporary bash script to handle authentication
cat > /tmp/fetch_sonar.sh << 'SCRIPT'
#!/bin/bash
curl -s -u "${SONARQUBE_TOKEN}:" \
  "https://sonarcloud.io/api/issues/search?componentKeys=${SONAR_PROJECT_KEY}&pullRequest=$1&issueStatuses=OPEN,CONFIRMED&sinceLeakPeriod=true&ps=500"
SCRIPT

chmod +x /tmp/fetch_sonar.sh
/tmp/fetch_sonar.sh $PR_NUMBER > /tmp/sonar_pr_$PR_NUMBER.json
```

**Параметри API:**
- `componentKeys`: ключ вашого проєкту
- `pullRequest`: номер PR
- `issueStatuses`: OPEN,CONFIRMED (без розв'язаних)
- `sinceLeakPeriod`: лише нові проблеми в цьому PR
- `ps`: розмір сторінки (максимум 500)

## Скрипт аналізу

Створіть Node.js-скрипт аналізу в `/tmp/sonar_analyze.js`:

```javascript
const fs = require('fs');
const prNumber = process.argv[2];
const data = JSON.parse(fs.readFileSync(`/tmp/sonar_pr_${prNumber}.json`, 'utf8'));
const issues = data.issues || [];

// Group by severity
const bySeverity = issues.reduce((acc, i) => {
  acc[i.severity] = (acc[i.severity] || 0) + 1;
  return acc;
}, {});

// Group by type
const byType = issues.reduce((acc, i) => {
  acc[i.type] = (acc[i.type] || 0) + 1;
  return acc;
}, {});

// Group by file
const byFile = issues.reduce((acc, i) => {
  const file = i.component.split(':')[1] || i.component;
  acc[file] = (acc[file] || 0) + 1;
  return acc;
}, {});

// Group by rule
const byRule = issues.reduce((acc, i) => {
  if (!acc[i.rule]) {
    acc[i.rule] = {
      count: 0,
      severity: i.severity,
      message: i.message
    };
  }
  acc[i.rule].count++;
  return acc;
}, {});

// Output structured data
console.log(JSON.stringify({
  total: data.total,
  bySeverity,
  byType,
  topFiles: Object.entries(byFile)
    .sort((a, b) => b[1] - a[1])
    .slice(0, 10),
  topRules: Object.entries(byRule)
    .map(([rule, d]) => ({ rule, ...d }))
    .sort((a, b) => b.count - a.count)
    .slice(0, 5)
}, null, 2));
```

**Запуск аналізу:**
```bash
node /tmp/sonar_analyze.js $PR_NUMBER > /tmp/sonar_analysis_$PR_NUMBER.json
```

## Формат звіту

Згенеруйте відформатований звіт на основі аналізу:

```
📊 SonarCloud Analysis - PR #XXX

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📈 EXECUTIVE SUMMARY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Total Issues: {TOTAL}

By Severity:
🔴 Blocker/Critical: {COUNT} ({PERCENTAGE}%)
🟡 Major: {COUNT} ({PERCENTAGE}%)
🔵 Minor/Info: {COUNT} ({PERCENTAGE}%)

By Type:
🐛 Bugs: {COUNT}
🛡️ Vulnerabilities: {COUNT}
🧹 Code Smells: {COUNT}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📂 TOP 10 FILES WITH ISSUES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. src/components/UserProfile.tsx - 8 issues
2. src/services/auth.service.ts - 5 issues
3. src/utils/validation.ts - 4 issues
...

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚠️ TOP 5 VIOLATED RULES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. typescript:S1854 (MAJOR) - 12 occurrences
   "Dead stores should be removed"

2. typescript:S3776 (CRITICAL) - 8 occurrences
   "Cognitive Complexity of functions should not be too high"

3. typescript:S1186 (MINOR) - 6 occurrences
   "Functions should not be empty"
...

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ ACTION PLAN
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Priority 1 - CRITICAL/BLOCKER ({COUNT} issues):
  • Fix immediately before merge
  • Focus on: {TOP_FILES}

Priority 2 - MAJOR ({COUNT} issues):
  • Address in this PR if possible
  • Consider technical debt ticket if extensive

Priority 3 - MINOR/INFO ({COUNT} issues):
  • Can be addressed in follow-up PR
  • Add to backlog for refactoring sprint

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔗 LINKS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

View in SonarCloud:
https://sonarcloud.io/project/pull_requests_list?id={PROJECT_KEY}&pullRequest={PR_NUMBER}
```

## Відповідність серйозності

| SonarCloud | Символ | Пріоритет | Дія |
|------------|--------|-----------|-----|
| BLOCKER | 🔴 | P0 | Виправити негайно |
| CRITICAL | 🔴 | P0 | Виправити негайно |
| MAJOR | 🟡 | P1 | Виправити в цьому PR |
| MINOR | 🔵 | P2 | Розглянути для наступного PR |
| INFO | 🔵 | P3 | Необов'язкове покращення |

## Типи проблем

| Тип | Символ | Опис |
|-----|--------|------|
| BUG | 🐛 | Код, який очевидно хибний |
| VULNERABILITY | 🛡️ | Проблеми безпеки |
| CODE_SMELL | 🧹 | Проблема з підтримуваністю |
| SECURITY_HOTSPOT | 🔒 | Критичний для безпеки код, що потребує перегляду |

## Прибирання

Завжди прибирайте тимчасові файли після виконання:

```bash
rm -f /tmp/fetch_sonar.sh
rm -f /tmp/sonar_pr_$PR_NUMBER.json
rm -f /tmp/sonar_analyze.js
rm -f /tmp/sonar_analysis_$PR_NUMBER.json
```

## Обробка помилок

| Помилка | Причина | Дія |
|---------|---------|-----|
| Токен не задано | Відсутній `$SONARQUBE_TOKEN` | Попросити користувача експортувати токен |
| 401 Unauthorized | Недійсний або прострочений токен | Запросити новий токен у SonarCloud |
| 404 Not Found | PR не існує в SonarCloud | Перевірити номер PR і ключ проєкту |
| Порожня відповідь | Проблем не знайдено | Повідомити про чистий PR, привітати команду |
| >500 проблем | Досягнуто ліміту пагінації | Попередити про неповні дані, запропонувати фільтрацію |
| Помилка мережі | API недоступний | Перевірити з'єднання з інтернетом, повторити |

## Параметри конфігурації

### Конфігурація на рівні проєкту

Створіть `.sonarcloud.properties` або додайте в `CLAUDE.md`:

```properties
# SonarCloud Configuration
SONAR_ORGANIZATION=your-org
SONAR_PROJECT_KEY=your-org_your-project
SONAR_EXCLUSIONS=**/*.test.ts,**/*.spec.ts,**/migrations/**
SONAR_COVERAGE_EXCLUSIONS=**/*.test.ts,src/test/**
```

### Ліміти запитів API

Ліміти SonarCloud API:
- Безкоштовний тариф: 10 000 запитів на добу
- Платний тариф: без обмежень

**Порада:** кешуйте результати для повторних запитів до того самого PR.

## Приклади інтеграції

### GitHub Actions

```yaml
- name: SonarQube Analysis
  run: |
    export SONARQUBE_TOKEN=${{ secrets.SONAR_TOKEN }}
    export SONAR_PROJECT_KEY="${{ secrets.SONAR_PROJECT }}"
    claude -p "/sonarqube ${{ github.event.pull_request.number }}"
```

### Pre-merge hook

Додайте в `.claude/hooks/pre-merge.sh`:

```bash
#!/bin/bash
PR_NUMBER=$(gh pr view --json number -q .number)
claude -p "/sonarqube $PR_NUMBER"
```

## Червоні прапорці: НІКОЛИ не робіть

**Ніколи:**
- ❌ Не змінюйте код і не виправляйте проблеми автоматично (команда лише для аналізу)
- ❌ Не пропускайте перевірку токена (ризик для безпеки)
- ❌ Не залишайте тимчасові файли в `/tmp` (прибирання обов'язкове)
- ❌ Не комітьте токен SonarQube в репозиторій (використовуйте змінні середовища)
- ❌ Не запускайте без перевірки терміну дії токена

**Завжди:**
- ✅ Генеруйте структурований звіт із конкретними діями
- ✅ Прибирайте після виконання
- ✅ Коректно обробляйте помилки API
- ✅ Перевіряйте дійсність токена перед викликами API
- ✅ Розбирайте й подавайте дані зрозуміло

## Розширене використання

### Власні фільтри

```bash
# Only show critical/blocker issues
/sonarqube 123 --severity BLOCKER,CRITICAL

# Only show bugs and vulnerabilities
/sonarqube 123 --types BUG,VULNERABILITY

# Specific file pattern
/sonarqube 123 --files "src/services/**"
```

### Кілька PR

```bash
# Compare issues across PRs
/sonarqube 123,124,125 --compare
```

## Усунення несправностей

### Проблема: "curl: (22) The requested URL returned error: 401"

**Причина:** недійсний або відсутній токен

**Виправлення:**
```bash
# Regenerate token in SonarCloud
# Export new token
export SONARQUBE_TOKEN="new_token_here"
```

### Проблема: "Empty response or no issues"

**Причина:** аналіз ще не завершено або PR не проаналізовано

**Виправлення:** зачекайте завершення аналізу SonarCloud (~2-5 хвилин після створення PR)

### Проблема: "componentKeys not found"

**Причина:** хибний ключ проєкту

**Виправлення:** перевірте ключ проєкту в URL SonarCloud:
```
https://sonarcloud.io/project/overview?id=YOUR_PROJECT_KEY
```

## Приклади використання

```bash
# Basic usage
/sonarqube 170

# With PR prefix
/sonarqube PR #234

# Using PR URL
/sonarqube https://github.com/org/repo/pull/170

# Custom severity filter (if implemented)
/sonarqube 170 --critical-only
```

Номер PR: $ARGUMENTS
