---
name: git-worktree-remove
description: Безпечне видалення git worktree з очищенням гілки та перевірками безпеки
argument-hint: <worktree_name>
effort: low
when_to_use: "Використовуйте для видалення конкретного worktree за назвою."
disable-model-invocation: true
---

# Видалення git worktree

Безпечне видалення одного git worktree з очищенням гілки, перевіркою злиття та видаленням гілки бази даних.

**Основний принцип:** спершу перевірки безпеки, потім акуратне видалення worktree + гілки + ресурсів БД.

**Частина:** [Набору життєвого циклу worktree](../../commands/git-worktree.uk.md) | [`/git-worktree`](../../commands/git-worktree.uk.md) | [`/git-worktree-status`](../../commands/git-worktree-status.uk.md) | [`/git-worktree-clean`](../../commands/git-worktree-clean.uk.md)

## Процес

1. **Перевірте ціль**: визначте worktree для видалення
2. **Перевірка безпеки**: захистіть гілки main/develop
3. **Перевірте статус злиття**: попередьте, якщо гілка має незлиті зміни
4. **Перевірте незакомічені зміни**: попередьте, якщо worktree має «брудний» стан
5. **Видаліть worktree**: `git worktree remove`
6. **Видаліть локальну гілку**: `git branch -d` (або `-D` з підтвердженням)
7. **Видаліть віддалену гілку**: `git push origin --delete` (з підтвердженням)
8. **Нагадування про очищення бази даних**: запропонуйте видалити гілку БД, якщо доречно
9. **Приберіть посилання**: `git worktree prune`

## Перевірки безпеки

### Захищені гілки

```bash
# Never remove worktrees for these branches (configurable)
PROTECTED_BRANCHES="main master develop staging production"

if echo "$PROTECTED_BRANCHES" | grep -qw "$BRANCH"; then
  echo "BLOCKED: Cannot remove worktree for protected branch '$BRANCH'"
  echo "Protected branches: $PROTECTED_BRANCHES"
  exit 1
fi
```

### Незакомічені зміни

```bash
cd "$WORKTREE_PATH"
if [ -n "$(git status --porcelain)" ]; then
  echo "WARNING: Worktree has uncommitted changes:"
  git status --short
  echo ""
  echo "Options:"
  echo "  1. Commit changes first"
  echo "  2. Force remove (--force)"
  echo "  3. Cancel"
  # Wait for user decision
fi
```

### Статус злиття

```bash
# Check if branch is merged into main
MAIN_BRANCH=$(git symbolic-ref refs/remotes/origin/HEAD | sed 's@^refs/remotes/origin/@@')

if git merge-base --is-ancestor "$BRANCH" "$MAIN_BRANCH" 2>/dev/null; then
  echo "Branch '$BRANCH' is merged into $MAIN_BRANCH. Safe to delete."
  MERGED=true
else
  echo "WARNING: Branch '$BRANCH' is NOT merged into $MAIN_BRANCH."
  echo "You may lose work if you delete this branch."
  MERGED=false
fi
```

## Кроки видалення

```bash
# 1. Remove the worktree
git worktree remove "$WORKTREE_PATH"
# If dirty state and user confirmed force:
# git worktree remove --force "$WORKTREE_PATH"

# 2. Delete local branch
if [ "$MERGED" = true ]; then
  git branch -d "$BRANCH"
else
  echo "Delete unmerged branch '$BRANCH'? (requires confirmation)"
  # On confirmation:
  git branch -D "$BRANCH"
fi

# 3. Delete remote branch (with confirmation)
if git ls-remote --heads origin "$BRANCH" | grep -q "$BRANCH"; then
  echo "Delete remote branch 'origin/$BRANCH'?"
  # On confirmation:
  git push origin --delete "$BRANCH"
fi

# 4. Prune stale references
git worktree prune
```

## Очищення гілки бази даних

**Після видалення worktree нагадайте про пов'язані гілки бази даних:**

```bash
# Detect database provider (same logic as /git-worktree)
if [ -f ".env" ] && grep -q "neon" ".env"; then
  echo ""
  echo "DB Cleanup: neonctl branches delete $BRANCH_SLUG"
elif [ -f ".pscale.yml" ]; then
  echo ""
  DB_NAME=$(grep 'database:' .pscale.yml | awk '{print $2}')
  echo "DB Cleanup: pscale branch delete $DB_NAME $BRANCH_SLUG"
elif [ -f ".env" ] && grep -q "postgresql" ".env"; then
  echo ""
  echo "DB Cleanup: psql \$DATABASE_URL -c \"DROP SCHEMA ${BRANCH_SLUG} CASCADE;\""
fi
```

## Формат звіту

**Успішне видалення (злита гілка):**

```
Removed worktree: .worktrees/feat/auth
  Worktree directory: deleted
  Local branch feat/auth: deleted (was merged)
  Remote branch origin/feat/auth: deleted
  References: pruned

DB reminder: neonctl branches delete feat-auth
```

**Видалення з попередженнями (незлита гілка):**

```
Removed worktree: .worktrees/feat/experimental
  Worktree directory: deleted
  Local branch feat/experimental: deleted (was NOT merged - forced)
  Remote branch: no remote branch found
  References: pruned

WARNING: Branch was not merged. Changes may be lost.
Last commit: a1b2c3d "WIP: experimental auth flow"
```

## Прапорці

| Прапорець | Дія |
|------|--------|
| `--force` | Пропустити попередження про незакомічені зміни |
| `--keep-branch` | Видалити worktree, але залишити гілку |
| `--keep-remote` | Не видаляти віддалену гілку |

## Короткий довідник

| Ситуація | Дія |
|-----------|--------|
| Гілку злито | Безпечне видалення (branch -d) |
| Гілку не злито | Попередити + вимагати підтвердження (branch -D) |
| Незакомічені зміни | Попередити + запропонувати force/скасування |
| Захищена гілка (main/develop) | Заблокувати видалення |
| Існує віддалена гілка | Запитати про видалення віддаленої |
| Виявлено гілку БД | Нагадати з точною командою |
| Застарілі посилання | Автоматичний prune |

## Поширені помилки

**Видалення worktree для main/develop**
- Завжди блокується перевіркою безпеки. За потреби переналаштуйте список захищених гілок.

**Видалення незлитої гілки без перевірки**
- Завжди перевіряйте статус злиття. Незлиті гілки потребують явного `--force` або `-D`.

**Забуте очищення гілки бази даних**
- Залишає осиротілі гілки БД, які споживають ресурси. Команда нагадує про це автоматично.

**Використання `rm -rf` замість `git worktree remove`**
- Залишає застарілі посилання на worktree в `.git/worktrees/`. Завжди використовуйте команди git.

## Використання

```
/git-worktree-remove feat/auth
/git-worktree-remove fix/login-bug --force
/git-worktree-remove refactor/db --keep-branch
```

Гілка або шлях до worktree: $ARGUMENTS