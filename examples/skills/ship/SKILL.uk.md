---
name: ship
description: Комплексна перевірка перед розгортанням, що підтверджує готовність до релізу
argument-hint: "[--no-push] [--changelog-only] [--dry-run]"
effort: medium
when_to_use: "Use when ready to stage, commit, and push the current work."
disable-model-invocation: true
---

# Команда ship: чекліст перед розгортанням

Комплексна перевірка перед розгортанням, що підтверджує готовність до релізу.

## Призначення

Запускайте перед кожним розгортанням у продакшен, щоб перевірити:
- Бар'єри якості коду
- Покриття тестами
- Перевірки безпеки
- Оновлення документації
- Готовність середовища

## Чекліст перед розгортанням

### 🔴 Блокери (мають пройти)

```bash
# 1. All tests passing
npm test 2>/dev/null || pnpm test 2>/dev/null || yarn test 2>/dev/null
echo "Exit code: $?"

# 2. No TypeScript/lint errors
npm run typecheck 2>/dev/null || npx tsc --noEmit
npm run lint 2>/dev/null || npx eslint .

# 3. Build succeeds
npm run build 2>/dev/null || pnpm build 2>/dev/null

# 4. No secrets in code
grep -rn "API_KEY=\|SECRET=\|PASSWORD=" --include="*.{ts,js,json}" . 2>/dev/null | grep -v node_modules | grep -v ".env.example"
```

### 🟠 Високий пріоритет (бажано, щоб пройшли)

```bash
# 5. Security audit
npm audit --audit-level=high 2>/dev/null || echo "Run manually: npm audit"

# 6. No console.log in production code
grep -rn "console\.log\|console\.debug" --include="*.{ts,js,tsx,jsx}" src/ 2>/dev/null | grep -v "// allowed" | head -10

# 7. No TODO/FIXME in critical paths
grep -rn "TODO\|FIXME\|XXX\|HACK" --include="*.{ts,js}" src/ 2>/dev/null | head -10

# 8. Database migrations ready
[ -d "prisma/migrations" ] && echo "Prisma migrations: $(ls prisma/migrations | wc -l) total"
[ -d "migrations" ] && echo "Migrations: $(ls migrations | wc -l) total"
```

### 🟡 Рекомендовано (було б добре)

```bash
# 9. Documentation updated
git diff --name-only HEAD~5 | grep -E "README|CHANGELOG|docs/" | head -10

# 10. Version bumped
cat package.json | jq -r '.version' 2>/dev/null || echo "Check version manually"

# 11. Environment variables documented
[ -f ".env.example" ] && echo "✅ .env.example exists" || echo "⚠️ Missing .env.example"
```

## Формат виводу

---

### 🚀 Звіт про готовність до релізу

**Гілка**: [поточна гілка]
**Коміт**: [короткий хеш HEAD]
**Ціль**: [production/staging]
**Часова позначка**: [дата/час]

### Блокери (виправити до розгортання)

| Перевірка | Статус | Деталі |
|-----------|--------|--------|
| Тести | ✅/❌ | X пройшло, Y провалено |
| TypeScript | ✅/❌ | X помилок |
| Lint | ✅/❌ | X попереджень, Y помилок |
| Збірка | ✅/❌ | Успіх/Збій |
| Секрети | ✅/❌ | X потенційних витоків |

### Високий пріоритет

| Перевірка | Статус | Дія |
|-----------|--------|-----|
| Аудит безпеки | ⚠️/✅ | X вразливостей |
| Console-логи | ⚠️/✅ | X знайдено в src/ |
| TODO | ⚠️/✅ | X критичних TODO |
| Міграції | ⚠️/✅ | X очікують |

### Рекомендовано

| Перевірка | Статус | Примітка |
|-----------|--------|----------|
| Документацію оновлено | ⚠️/✅ | CHANGELOG оновлено |
| Версію піднято | ⚠️/✅ | Поточна: X.Y.Z |
| Env задокументовано | ⚠️/✅ | .env.example наявний |

### 📊 Підсумок

```
🔴 Блокери:      X/5 пройшло
🟠 Високий:      X/4 пройшло
🟡 Рекомендовано: X/3 пройшло
─────────────────────────
Загалом:        [READY TO SHIP / NOT READY]
```

### 🎯 Пункти дій

1. [Найкритичніше виправлення]
2. [Другий пріоритет]
3. [Третій пріоритет]

---

## Перевірки для конкретних середовищ

### Розгортання в продакшен

```bash
# Verify production env vars
[ -f ".env.production" ] && echo "Production env exists"

# Check for debug flags
grep -rn "DEBUG=true\|NODE_ENV=development" .env* 2>/dev/null

# Verify API endpoints point to production
grep -rn "localhost\|127\.0\.0\.1" --include="*.{ts,js,json}" src/ 2>/dev/null | grep -v test | head -5
```

### Розгортання в staging

```bash
# Staging-specific checks
[ -f ".env.staging" ] && echo "Staging env exists"

# Feature flags for staging
grep -rn "FEATURE_FLAG\|ENABLE_" .env* 2>/dev/null
```

## Інтеграція з CI/CD

Додайте до свого конвеєра:

```yaml
# GitHub Actions example
ship-check:
  runs-on: ubuntu-latest
  steps:
    - uses: actions/checkout@v4
    - name: Run ship checklist
      run: |
        npm ci
        npm test
        npm run typecheck
        npm run lint
        npm run build
        npm audit --audit-level=high
```

## Перевірка після розгортання

Після розгортання перевірте:

```bash
# 1. Health check
curl -s https://your-app.com/health | jq .

# 2. Version check
curl -s https://your-app.com/version | jq .

# 3. Smoke tests
npm run test:smoke 2>/dev/null || echo "Run smoke tests manually"
```

## Підготовка до відкату

Перед релізом переконайтеся, що можете відкотитися:

```bash
# Note current production tag
git describe --tags --abbrev=0

# Verify rollback procedure exists
[ -f "docs/runbooks/rollback.md" ] && echo "✅ Rollback docs exist"

# Check database migration reversibility
# Prisma: prisma migrate diff
# Rails: rails db:rollback (dry-run)
```

## Використання

**Повний чекліст:**
```
/ship
```

**Розгортання в продакшен:**
```
/ship --production
```

**Швидка перевірка (лише блокери):**
```
/ship --quick
```

**З конкретною ціллю:**
```
/ship --target=staging
```

## Поради

1. **Запускайте рано й часто**: не чекайте дня розгортання
2. **Автоматизуйте в CI**: нехай блокери валять конвеєр
3. **Домовленість у команді**: визначте, що є блокером, а що попередженням
4. **Документуйте винятки**: якщо пропускаєте перевірку, зазначте чому
5. **Стежте після розгортання**: реліз не завершено, доки моніторинг не підтвердить успіх

## Пов'язані команди

- `/release-notes` - генерація changelog і анонсів
- `/validate-changes` - рев'ю коду на основі LLM
- `/security` - поглиблений аудит безпеки

$ARGUMENTS
