---
name: git-worktree-status
description: Перевірка стану фонових завдань верифікації, що виконуються в git worktree
effort: low
when_to_use: "Використовуйте, щоб побачити всі активні worktrees і стан їхніх поточних гілок."
disable-model-invocation: true
---

# Статус git worktree

Перевірте фонові завдання верифікації (перевірка типів, тести, збірка), запущені командою `/git-worktree`.

**Основний принцип:** неблокувальний зворотний зв'язок про стан worktree без переривання процесу розробки.

**Частина:** [набору для життєвого циклу worktree](../../commands/git-worktree.uk.md) | [`/git-worktree`](../../commands/git-worktree.uk.md) | [`/git-worktree-remove`](../../commands/git-worktree-remove.uk.md) | [`/git-worktree-clean`](../../commands/git-worktree-clean.uk.md)

## Процес

1. **Визначити поточний worktree**: переконатися, що ми всередині git worktree
2. **Перевірити лог-файли**: прочитати `.worktree-logs/` на результати фонових завдань
3. **Розібрати результати**: отримати кількість успішних/невдалих перевірок і помилки
4. **Показати статус**: підсумок із кольоровою індикацією та практичними наступними кроками

## Визначення worktree

```bash
# Check if inside a worktree (not main repo)
git rev-parse --git-common-dir 2>/dev/null | grep -q "\.git/worktrees" || {
  echo "Not inside a worktree. Use from a worktree directory."
  exit 1
}

# Get worktree info
WORKTREE_PATH=$(git rev-parse --show-toplevel)
BRANCH=$(git rev-parse --abbrev-ref HEAD)
MAIN_REPO=$(git rev-parse --git-common-dir | sed 's|/\.git/worktrees/.*||')
```

## Перевірки фонових завдань

### Статус перевірки типів

```bash
LOG=".worktree-logs/typecheck.log"

if [ -f "$LOG" ]; then
  if grep -q "error TS" "$LOG"; then
    ERROR_COUNT=$(grep -c "error TS" "$LOG")
    echo "Type check: FAIL ($ERROR_COUNT errors)"
    # Show first 5 errors
    grep "error TS" "$LOG" | head -5
  else
    echo "Type check: PASS"
  fi
elif pgrep -f "tsc --noEmit" > /dev/null; then
  echo "Type check: RUNNING..."
else
  echo "Type check: NOT RUN"
fi
```

### Статус тестів

```bash
LOG=".worktree-logs/tests.log"

if [ -f "$LOG" ]; then
  if grep -q '"numFailedTests":0' "$LOG"; then
    TOTAL=$(grep -o '"numTotalTests":[0-9]*' "$LOG" | cut -d: -f2)
    echo "Tests: PASS ($TOTAL tests)"
  else
    FAILED=$(grep -o '"numFailedTests":[0-9]*' "$LOG" | cut -d: -f2)
    echo "Tests: FAIL ($FAILED failures)"
    # Show failed test names
    grep '"fullName"' "$LOG" | head -5
  fi
elif pgrep -f "vitest run" > /dev/null; then
  echo "Tests: RUNNING..."
else
  echo "Tests: NOT RUN"
fi
```

### Статус збірки

```bash
LOG=".worktree-logs/build.log"

if [ -f "$LOG" ]; then
  if [ $? -eq 0 ]; then
    echo "Build: PASS"
  else
    echo "Build: FAIL"
    tail -10 "$LOG"
  fi
elif pgrep -f "cargo build\|next build\|go build" > /dev/null; then
  echo "Build: RUNNING..."
else
  echo "Build: NOT RUN"
fi
```

## Формат звіту

```
Worktree Status: .worktrees/feat/auth
Branch: feat/auth (from main, 3 commits ahead)

Checks:
  Type check:  PASS
  Tests:       PASS (142 tests)
  Build:       NOT RUN

Dependencies: symlinked from main
Disk usage: 2.3 MB (excl. node_modules)

Log files: .worktree-logs/
```

**Якщо виявлено збої:**

```
Worktree Status: .worktrees/feat/auth
Branch: feat/auth (from main, 3 commits ahead)

Checks:
  Type check:  FAIL (3 errors)
    src/auth.ts:42 - error TS2345: Argument of type 'string' is not assignable
    src/auth.ts:67 - error TS2304: Cannot find name 'AuthConfig'
    src/middleware.ts:12 - error TS7006: Parameter 'req' implicitly has an 'any' type
  Tests:       FAIL (2 failures)
    auth.test.ts > should validate token
    auth.test.ts > should reject expired token
  Build:       NOT RUN

Action: Fix type errors before proceeding. Run `npx tsc --noEmit` for full output.
```

## Керування логами

```bash
# Clean old logs (useful for re-running checks)
rm -rf .worktree-logs/*.log

# Re-run all checks
npx tsc --noEmit > .worktree-logs/typecheck.log 2>&1 &
npx vitest run --reporter=json > .worktree-logs/tests.log 2>&1 &
```

## Швидкий довідник

| Ситуація | Вивід |
|-----------|--------|
| Усі перевірки пройдено | Зелений статус, можна працювати |
| Перевірки ще виконуються | «RUNNING...» із PID |
| Знайдено помилки типів | Кількість помилок + перші 5 помилок |
| Збої тестів | Кількість збоїв + назви невдалих тестів |
| Логів не знайдено | «NOT RUN» (використано `--fast` або логи видалено) |
| Не у worktree | Повідомлення про помилку з інструкціями |

## Використання

```
/git-worktree-status
```

Аргументи не потрібні. Запускайте з будь-якої директорії worktree.
