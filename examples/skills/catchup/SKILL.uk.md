---
name: catchup
description: Відновити контекст після /clear, підсумувавши нещодавню роботу і стан проєкту
argument-hint: "[branch] [--since <date>]"
effort: low
when_to_use: "Використовуйте після /clear або на початку сесії, щоб відновити контекст."
disable-model-invocation: true
---

# Відновлення контексту

Відновіть контекст після `/clear`: підсумуйте нещодавню роботу і стан проєкту.

## Призначення

Після очищення контексту через `/clear` використайте цю команду, щоб швидко відновити розуміння того:
- Що нещодавно змінювалося
- Який поточний стан проєкту
- Які TODO і проблеми ще не закрито
- Звідки продовжити роботу

## Інструкції

### Крок 1: Аналіз історії git

```bash
# Recent commits (last 10)
git log --oneline -10

# Files modified in last 5 commits
git diff --stat HEAD~5 2>/dev/null || git diff --stat $(git rev-list --max-parents=0 HEAD)

# Current branch and status
git branch --show-current
git status --short
```

### Крок 2: Підсумок нещодавніх змін

```bash
# What changed today
git log --oneline --since="midnight" --author="$(git config user.name)" 2>/dev/null

# Uncommitted work
git diff --name-only
git diff --cached --name-only
```

### Крок 3: Пошук TODO/FIXME

```bash
# Find outstanding work markers in recently modified files
git diff --name-only HEAD~5 2>/dev/null | head -20 | xargs grep -n "TODO\|FIXME\|XXX\|HACK" 2>/dev/null | head -30
```

### Крок 4: Перевірка стану проєкту

```bash
# Check for common state indicators
[ -f "package.json" ] && echo "📦 Node project: $(jq -r '.name // "unnamed"' package.json)"
[ -f "Cargo.toml" ] && echo "🦀 Rust project: $(grep '^name' Cargo.toml | head -1)"
[ -f "pyproject.toml" ] && echo "🐍 Python project"
[ -f "go.mod" ] && echo "🐹 Go project: $(head -1 go.mod | cut -d' ' -f2)"

# Active branch purpose (from branch name)
BRANCH=$(git branch --show-current)
echo "🌿 Branch: $BRANCH"
```

## Формат виводу

Надайте структурований підсумок:

---

### 📍 Контекст відновлено

**Проєкт**: [назва з package.json/Cargo.toml тощо]
**Гілка**: [поточна гілка]
**Остання активність**: [час останнього коміту]

### 🔄 Нещодавня робота (останні 5 комітів)

1. [повідомлення коміту 1] - [змінені файли]
2. [повідомлення коміту 2] - [змінені файли]
...

### 📝 Незакомічені зміни

- [список змінених файлів зі стислим описом змін]

### ⚠️ Незакриті TODO

- [file:line] TODO: [опис]
- [file:line] FIXME: [опис]

### 🎯 Пропоновані наступні кроки

На основі нещодавньої активності:
1. [Найімовірніша наступна дія з огляду на патерни]
2. [Альтернативний напрям роботи]

---

## Приклади використання

**Після довгої перерви:**
```
/catchup
```
→ Повне відновлення контексту

**Швидка перевірка стану:**
```
/catchup --brief
```
→ Лише коміти й незакомічені зміни

**Фокус на конкретній області:**
```
/catchup auth
```
→ Фільтр змін, пов'язаних з auth

## Професійні поради

1. **Документуйте перед `/clear`**: перед очищенням контексту напишіть коротку нотатку в повідомленні коміту або в CLAUDE.md
2. **Використовуйте з Memory Bank**: поєднуйте з файлами `.claude/memory/` для сталого стану
3. **Іменування гілок**: використовуйте описові назви гілок (наприклад, `feat/user-auth`), щоб полегшити відновлення контексту

$ARGUMENTS
