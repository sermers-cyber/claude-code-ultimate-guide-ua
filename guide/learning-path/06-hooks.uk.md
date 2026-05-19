# Module 06: Hooks & Events

**Час**: 1 година | **Складність**: ⭐⭐ Intermediate

## Мета

Автоматизувати реагування на системні події. Створювати скрипти, які виконуються перед операціями Claude Code або після них.

---

## Що ви дізнаєтеся

- Як працюють hooks та коли вони запускаються
- Створення валідації перед комітом (pre-commit validation)
- Побудова сповіщень після виконання дій (post-action notifications)
- Написання безпечних скриптів автоматизації
- Популярні шаблони (patterns) використання hooks

---

## Що таке Hooks?

**Hook** — це скрипт, який автоматично запускається у відповідь на певну подію в системі.

### Приклад: Pre-Commit Hook

Перед тим як зробити commit ваших змін:

```
Ви запускаєте: git commit -m "Fix bug"
       ↓
Запускається hook: Перевіряє консистентність номерів версій
       ↓
Якщо версія неправильна:
  ❌ Commit заблоковано
  З'являється повідомлення про помилку з поясненням
       ↓
Ви виправляєте: Оновлюєте файл VERSION
       ↓
Commit успішно виконано
```

Hooks запобігають потраплянню типових помилок до git.

### Події для Hooks (Hook Events)

Hooks можуть запускатися на такі події:

| Подія | Час запуску | Сценарій використання |
|-------|-------------|-----------------------|
| **PreToolUse** | Перед тим, як Claude запускає інструмент (tool) | Валідація запиту |
| **PostToolUse** | Після того, як Claude запускає інструмент (tool) | Логування результатів, перевірка виводу |
| **PreCommit** | Перед виконанням git commit | Валідація змін |
| **PostPush** | Після виконання git push | Сповіщення команди |

---

## Створення вашого першого Hook

Hooks є звичайними скриптами bash (або PowerShell) і розміщуються в директорії `.claude/hooks/`.

### Базова структура Hook

```bash
#!/bin/bash

# Hook: validate-version
# Event: PreCommit
# Description: Check that VERSION file is updated with other changes

# Отримуємо файли, що готуються до коміту (staged files)
FILES=$(git diff --cached --name-only)

# Перевіряємо, чи були змінені файли посібника (guide)
if echo "$FILES" | grep -q "guide/"; then
  # Якщо змінилася директорія guide/, файл VERSION також має змінитися
  if ! echo "$FILES" | grep -q "VERSION"; then
    echo "❌ Error: guide/ was modified but VERSION wasn't updated"
    echo "Run: echo '3.x.x' > VERSION"
    exit 1  # Блокувати commit
  fi
fi

exit 0  # Дозволити commit
```

### Розташування файлів

```
my-project/
└── .claude/
    └── hooks/
        ├── validate-version.sh
        └── notify-team.sh
```

### Коди виходу (Exit Codes) для Hooks

```bash
exit 0   # Успіх — дозволити виконання операції
exit 1   # Помилка — заблокувати операцію та показати повідомлення
exit 2   # Попередження — дозволити виконання, але вивести попередження
```

---

## Шаблони використання Hooks

### Шаблон 1: Pre-Commit Валідація

Блокування commits, які не проходять перевірку:

```bash
#!/bin/bash
# Hook: security-check.sh
# Блокувати commit при виявленні проблем безпеки

# Перевірка на наявність жорстко закодованих (hardcoded) API-ключів
if grep -r "sk_live_" .; then
  echo "❌ ERROR: Found hardcoded Stripe key"
  exit 1
fi

# Перевірка на наявність console.log у коді (окрім тестів)
if grep -r "console.log" src/ --exclude-dir=tests; then
  echo "❌ ERROR: Found console.log in source code"
  exit 1
fi

# Пошук коментарів TODO (попередження, без блокування)
if grep -r "TODO:" src/; then
  echo "⚠️  Warning: TODO comments found (not blocking)"
fi

exit 0
```

### Шаблон 2: Post-Commit Сповіщення

Після успішного виконання commit:

```bash
#!/bin/bash
# Hook: notify-team.sh
# Сповіщення команди після певних commits

COMMIT_MSG=$(git log -1 --pretty=%B)

# Якщо commit стосується безпеки
if echo "$COMMIT_MSG" | grep -i "security"; then
  echo "🔐 Security commit: $COMMIT_MSG"
  # Надіслати у Slack (опціонально)
  # curl -X POST $SLACK_WEBHOOK -d "Security update: $COMMIT_MSG"
fi

exit 0
```

### Шаблон 3: Перевірка залежностей (Dependency Check)

Попередження, якщо залежності потребують оновлення:

```bash
#!/bin/bash
# Hook: check-deps.sh
# Перевірити, чи змінився package.json без оновлення lock-файлу

FILES=$(git diff --cached --name-only)

if echo "$FILES" | grep -q "package.json"; then
  if ! echo "$FILES" | grep -q "package-lock.json"; then
    echo "⚠️  Warning: package.json changed but lock file wasn't updated"
    echo "Run: npm install"
  fi
fi

exit 0
```

---

## Реєстрація Hooks

Hooks реєструються у файлі `.claude/settings.json`:

```json
{
  "hooks": {
    "pre_commit": ["validate-version.sh", "security-check.sh"],
    "post_commit": ["notify-team.sh"],
    "post_push": ["deploy-staging.sh"]
  }
}
```

Або у `settings.yaml`:

```yaml
hooks:
  pre_commit:
    - path: hooks/validate-version.sh
      description: "Check VERSION file updated"
      blocking: true
    - path: hooks/security-check.sh
      blocking: true
  post_commit:
    - path: hooks/notify-team.sh
      blocking: false
```

---

## Найкращі практики для безпечних Hooks

### РЕКОМЕНДУЄТЬСЯ

✅ Робити hooks **ідемпотентними** (ідемпотентність — безпечність багаторазового запуску)
✅ Логувати дії, які виконує hook
✅ Завершувати роботу з чіткими повідомленнями про помилки
✅ Використовувати `set -e` на початку скрипту для зупинки при першій помилці
✅ Робити файли hooks виконуваними: `chmod +x hook.sh`

### НЕ РЕКОМЕНДУЄТЬСЯ

❌ Робити hooks, які виконуються довше 5 секунд (це гальмує роботу)
❌ Використовувати мережеві запити всередині hooks (вони ненадійні)
❌ Дозволяти hooks самостійно змінювати файли (вони мають лише валідувати)
❌ Робити правила перевірок занадто суворими (це дратує розробників)
❌ Забувати протестувати hooks локально перед впровадженням

---

## Безпечний шаблон (Template) для Hook

```bash
#!/bin/bash
set -euo pipefail

# Шаблон hook для безпечної та зрозумілої автоматизації

HOOK_NAME="my-hook"
HOOK_VERSION="1.0.0"

# Кольори для виводу
RED='\033[0;31m'
YELLOW='\033[1;33m'
GREEN='\033[0;32m'
NC='\033[0m' # Без кольору

log_error() {
  echo -e "${RED}❌ $1${NC}"
}

log_warn() {
  echo -e "${YELLOW}⚠️  $1${NC}"
}

log_success() {
  echo -e "${GREEN}✅ $1${NC}"
}

# Головна логіка валідації
main() {
  echo "Running: $HOOK_NAME ($HOOK_VERSION)"
  
  # Ваші перевірки тут
  if some_check_fails; then
    log_error "Check failed because X"
    return 1
  fi
  
  log_success "All checks passed"
  return 0
}

# Запуск та вихід
main
exit $?
```

---

## Вправа: Створення Hook для валідації

### Сценарій

Ви хочете запобігти випадковим комітам із:
- Пробілами наприкінці рядків (trailing whitespace)
- Відсутніми файлами тестів для нового коду
- Невирішеними конфліктами злиття (merge conflicts)

### Крок 1: Створіть скрипт Hook

```bash
cat > .claude/hooks/pre-commit-validation.sh << 'EOF'
#!/bin/bash
set -euo pipefail

echo "🔍 Running pre-commit validation..."

# Перевірка 1: Пробіли наприкінці рядків
if git diff --cached | grep -E '^[+].*\s+$' > /dev/null; then
  echo "❌ Trailing whitespace found:"
  git diff --cached | grep -E '^[+].*\s+$'
  exit 1
fi

# Перевірка 2: Маркери конфліктів злиття
if git diff --cached | grep -E '^[+].*<<<<<<|^[+].*======|^[+].*>>>>>>' > /dev/null; then
  echo "❌ Merge conflict markers found"
  exit 1
fi

# Перевірка 3: Наявність тестів для нових файлів
STAGED_FILES=$(git diff --cached --name-only)
for file in $STAGED_FILES; do
  if [[ $file == src/*.ts && $file != *test* ]]; then
    TEST_FILE="${file%.ts}.test.ts"
    if ! git ls-files | grep -q "$TEST_FILE"; then
      echo "⚠️  Warning: New file $file has no test file"
    fi
  fi
done

echo "✅ Pre-commit validation passed"
exit 0
EOF

chmod +x .claude/hooks/pre-commit-validation.sh
```

### Крок 2: Зареєструйте його в settings.json

```json
{
  "hooks": {
    "pre_commit": ["hooks/pre-commit-validation.sh"]
  }
}
```

### Крок 3: Протестуйте його роботу

Створіть файл із пробілами в кінці рядка:

```bash
echo "test line   " > test.txt  # Зверніть увагу на пробіли наприкінці рядка
git add test.txt
```

Спробуйте зробити commit:

```bash
git commit -m "Test hook"
```

Hook заблокує дію:

```
❌ Trailing whitespace found:
+test line   
```

### Крок 4: Виправте та спробуйте знову

```bash
echo "test line" > test.txt  # Видаляємо пробіли наприкінці рядка
git add test.txt
git commit -m "Test hook (fixed)"
```

Тепер все проходить успішно:

```
✅ Pre-commit validation passed
```

---

## Налагодження (Debugging) Hooks

Якщо hook не працює або поводиться дивно:

1. **Запустіть його вручну**:
```bash
bash .claude/hooks/my-hook.sh
```

2. **Увімкніть детальний вивід**:
```bash
set -x  # Виводитиме кожну команду перед виконанням
```

3. **Перевірте код виходу**:
```bash
bash .claude/hooks/my-hook.sh; echo "Exit: $?"
```

4. **Тестуйте умови роботи**:
```bash
# Перевірка, чи змінювався певний файл
git diff --cached --name-only | grep "VERSION"
echo $?  # 0 = знайдено, 1 = не знайдено
```

---

## Валідація: Ви готові, якщо...

✓ Ви створили принаймні один працюючий скрипт hook

✓ Ви розумієте різні типи подій для hooks (pre-commit, post-commit тощо)

✓ Ви вмієте реєструвати hooks у файлах settings.json або settings.yaml

✓ Ви успішно протестували роботу hook локально

✓ Ви знаєте значення кодів виходу (0 = успіх, 1 = помилка)

---

## Що далі?

**Module 07: Advanced Patterns** охоплює:
- Складні сценарії оркестрації з кількома agents (multi-agent orchestration)
- Побудову складних workflows
- Обробку помилок та відновлення після них
- Сценарії автоматизації рівня production
- Шаблони координації для команд

Це навчить вас поєднувати всі попередні концепції для побудови складних multi-agent систем.

---
**Локалізація**: [Serhii (MacPlus Software)](https://macplus-software.com)
*Остання синхронізація: Травень 2026*
