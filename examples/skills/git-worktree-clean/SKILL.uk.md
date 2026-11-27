---
name: git-worktree-clean
description: Очищення застарілих git worktrees з виявленням злитих гілок і звітом про використання диска
argument-hint: "[--dry-run]"
effort: low
when_to_use: "Використовуйте для прибирання злитих або застарілих worktrees."
disable-model-invocation: true
---

# Очищення git worktree

Пакетне очищення застарілих git worktrees. Безпечно видаляє злиті гілки, звітує про використання диска й інтерактивно обробляє незлиті гілки.

**Основний принцип:** автоматично очищати злиті worktrees, інтерактивно переглядати незлиті, завжди звітувати, скільки місця звільнено.

**Частина:** [Набору життєвого циклу worktree](../../commands/git-worktree.uk.md) | [`/git-worktree`](../../commands/git-worktree.uk.md) | [`/git-worktree-status`](../../commands/git-worktree-status.uk.md) | [`/git-worktree-remove`](../../commands/git-worktree-remove.uk.md)

## Процес

1. **Перелічіть усі worktrees**: `git worktree list`
2. **Класифікуйте кожен**: злитий, незлитий чи захищений
3. **Обчисліть використання диска**: розмір кожного worktree
4. **Автоматичний режим**: видаліть усі злиті worktrees (безпечно)
5. **Інтерактивний режим**: перегляньте незлиті worktrees по одному
6. **Нагадування про очищення бази даних**: перелічіть гілки БД, які треба прибрати
7. **Звіт**: підсумок виконаних дій і звільненого місця

## Прапорці

| Прапорець | Дія |
|------|--------|
| `--dry-run` | Попередній перегляд того, що буде очищено, без змін |
| `--all` | Включити незлиті worktrees (з інтерактивним підтвердженням кожного) |
| `--force` | Видалити всі worktrees без підтвердження (небезпечно) |

## Пошук worktrees

```bash
# Get main branch name
MAIN_BRANCH=$(git symbolic-ref refs/remotes/origin/HEAD 2>/dev/null | sed 's@^refs/remotes/origin/@@')
MAIN_BRANCH=${MAIN_BRANCH:-main}

# Protected branches (never auto-clean)
PROTECTED="main master develop staging production"

# List all worktrees (skip main working tree)
git worktree list --porcelain | while read line; do
  # Parse worktree path and branch
  # Skip the main worktree (first entry)
done
```

## Класифікація

```bash
for WORKTREE in $WORKTREES; do
  BRANCH=$(git -C "$WORKTREE" rev-parse --abbrev-ref HEAD)

  # Skip protected
  if echo "$PROTECTED" | grep -qw "$BRANCH"; then
    echo "PROTECTED: $BRANCH (skipped)"
    continue
  fi

  # Check merge status
  if git merge-base --is-ancestor "$BRANCH" "$MAIN_BRANCH" 2>/dev/null; then
    echo "MERGED: $BRANCH → safe to remove"
    MERGED_LIST="$MERGED_LIST $WORKTREE"
  else
    echo "UNMERGED: $BRANCH → requires review"
    UNMERGED_LIST="$UNMERGED_LIST $WORKTREE"
  fi
done
```

## Обчислення використання диска

```bash
for WORKTREE in $ALL_WORKTREES; do
  # Calculate size excluding symlinked node_modules
  SIZE=$(du -sh --exclude='node_modules' "$WORKTREE" 2>/dev/null | cut -f1)
  # Or on macOS:
  SIZE=$(du -sh -I 'node_modules' "$WORKTREE" 2>/dev/null | cut -f1)
  echo "  $WORKTREE: $SIZE"
done
```

## Режим пробного запуску

```bash
# --dry-run: show what would happen without making changes

echo "=== Dry Run ==="
echo ""
echo "Would remove (merged):"
for WT in $MERGED_LIST; do
  echo "  $WT ($BRANCH) - $SIZE"
done
echo ""
echo "Would ask about (unmerged):"
for WT in $UNMERGED_LIST; do
  echo "  $WT ($BRANCH) - $SIZE - last commit: $(git log -1 --format='%s' $BRANCH)"
done
echo ""
echo "Total space to reclaim: $TOTAL_SIZE"
echo ""
echo "Run without --dry-run to execute."
```

## Автоматичний режим (за замовчуванням)

**Видаляє лише злиті worktrees. Безпечний за замовчуванням.**

```bash
echo "Cleaning merged worktrees..."

for WORKTREE in $MERGED_LIST; do
  BRANCH=$(git -C "$WORKTREE" rev-parse --abbrev-ref HEAD)

  # Remove worktree
  git worktree remove "$WORKTREE"

  # Delete local branch
  git branch -d "$BRANCH" 2>/dev/null

  # Delete remote branch
  git push origin --delete "$BRANCH" 2>/dev/null

  echo "  Removed: $WORKTREE ($BRANCH)"
done

# Report unmerged (not touched)
if [ -n "$UNMERGED_LIST" ]; then
  echo ""
  echo "Unmerged worktrees (kept):"
  for WT in $UNMERGED_LIST; do
    echo "  $WT - use /git-worktree-remove or --all to review"
  done
fi
```

## Інтерактивний режим (--all)

**Переглядає незлиті worktrees по одному:**

```bash
for WORKTREE in $UNMERGED_LIST; do
  BRANCH=$(git -C "$WORKTREE" rev-parse --abbrev-ref HEAD)
  LAST_COMMIT=$(git log -1 --format='%h %s (%cr)' "$BRANCH")
  AHEAD=$(git rev-list --count "$MAIN_BRANCH".."$BRANCH")

  echo ""
  echo "Unmerged: $WORKTREE"
  echo "  Branch: $BRANCH ($AHEAD commits ahead of $MAIN_BRANCH)"
  echo "  Last commit: $LAST_COMMIT"
  echo "  Size: $SIZE"
  echo ""
  echo "  [r]emove  [k]eep  [s]kip remaining"

  # Wait for user decision per worktree
done
```

## Формат звіту

**Після очищення:**

```
=== Worktree Cleanup Report ===

Removed (merged):
  .worktrees/feat/auth (feat/auth) - 2.3 MB
  .worktrees/fix/login-bug (fix/login-bug) - 1.1 MB
  .worktrees/chore/deps-update (chore/deps-update) - 0.8 MB

Kept (unmerged):
  .worktrees/feat/experimental (feat/experimental) - 4.2 MB
    Last commit: a1b2c3d "WIP: new auth flow" (3 days ago)

Kept (protected):
  .worktrees/develop (develop)

Space reclaimed: 4.2 MB
Worktrees remaining: 2
References pruned: yes

DB branches to clean:
  neonctl branches delete feat-auth
  neonctl branches delete fix-login-bug
  neonctl branches delete chore-deps-update
```

**Звіт пробного запуску:**

```
=== Dry Run - No Changes Made ===

Would remove (3 merged):
  .worktrees/feat/auth - 2.3 MB
  .worktrees/fix/login-bug - 1.1 MB
  .worktrees/chore/deps-update - 0.8 MB

Would keep (1 unmerged):
  .worktrees/feat/experimental - 4.2 MB

Would keep (1 protected):
  .worktrees/develop

Potential space savings: 4.2 MB
```

## Короткий довідник

| Ситуація | Дія |
|-----------|--------|
| За замовчуванням (без прапорців) | Видалити лише злиті worktrees |
| `--dry-run` | Попередній перегляд без змін |
| `--all` | Злиті (автоматично) + незлиті (інтерактивно) |
| `--force` | Видалити все, крім захищених |
| Захищена гілка | Завжди залишається |
| Злита гілка | Видаляється автоматично |
| Незлита гілка | Залишається (за замовчуванням) або інтерактивно (--all) |
| Виявлено гілки БД | Нагадування з точними командами |

## Поширені помилки

**Запуск `--force` без попереднього `--dry-run`**
- Завжди переглядайте результат через `--dry-run` перед примусовим очищенням

**Забуте очищення гілок БД**
- Очищення worktree не видаляє гілки БД автоматично. Виконайте команди з нагадування.

**Нерегулярне очищення**
- Застарілі worktrees накопичують місце на диску. Запускайте `/git-worktree-clean --dry-run` щотижня.

## Використання

```
/git-worktree-clean
/git-worktree-clean --dry-run
/git-worktree-clean --all
```

Прапорці: $ARGUMENTS