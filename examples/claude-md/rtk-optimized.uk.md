---
title: "Шаблон оптимізації токенів з RTK"
description: "Конфігурація CLAUDE.md для мінімізації споживання токенів за допомогою CLI-проксі RTK"
tags: [claude-md, template, performance]
---

# Оптимізація токенів з RTK

**Контекст**: використання RTK (Rust Token Killer) для мінімізації споживання токенів виводом команд.

## Команди для оптимізації

Для цих команд із багатослівним виводом завжди використовуй обгортку RTK:

### Операції Git (у середньому скорочення на 92.3%)
- `rtk git log` замість `git log`
- `rtk git status` замість `git status`
- `rtk git diff` замість `git diff`

### Операції з файлами (у середньому скорочення на 69.4%)
- `rtk find "*.md" .` замість `find . -name "*.md"`
- `rtk read <file>` замість `cat <file>` (для великих файлів >10K рядків)
- `rtk ls .` замість `ls -la`
- `rtk grep "pattern"` замість `grep -r "pattern"`

### Стек JS/TS (скорочення на 70-90%)
- `rtk vitest run` замість `pnpm test`
- `rtk pnpm list` замість `pnpm list`
- `rtk pnpm outdated` замість `pnpm outdated`
- `rtk prisma migrate status` замість `pnpm prisma migrate status`

### Інструменти Rust (скорочення на 80-90%)
- `rtk cargo test` замість `cargo test`
- `rtk cargo build` замість `cargo build`
- `rtk cargo clippy` замість `cargo clippy`

### Python (скорочення на 90%)
- `rtk python pytest` замість `pytest`

### Go (скорочення на 90%)
- `rtk go test` замість `go test`

### GitHub CLI (скорочення на 79-87%)
- `rtk gh pr view <num>` замість `gh pr view <num>`
- `rtk gh pr checks <num>` замість `gh pr checks <num>`

## Цільова економія токенів

**Базовий рівень**: ~150K токенів за 30-хвилинну сесію
**З RTK**: ~45K токенів (скорочення на 70%)

## Встановлення

```bash
# Homebrew (macOS/Linux)
brew install rtk-ai/tap/rtk

# Cargo (all platforms)
cargo install rtk

# Hook-first install
rtk init
```

## Перевірка

Перевірте доступність RTK:
```bash
rtk --version  # Should show: rtk 0.16.0+
```

## Коли НЕ варто використовувати RTK

- Швидке дослідження (1-2 команди): накладні витрати не виправдані
- Ви вже використовуєте інструменти на кшталт Grep/Read (нативні інструменти Claude оптимізовані)
- Короткий вивід (<100 символів): мінімальний виграш

## Автоматизація

Використовуйте RTK автоматично через hook (див. `.claude/hooks/bash/rtk-wrapper.sh`) або `rtk init` для налаштування з hook.
