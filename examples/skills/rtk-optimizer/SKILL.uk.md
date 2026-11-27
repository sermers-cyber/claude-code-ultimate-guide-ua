---
name: rtk-optimizer
description: "Обгортає багатослівні shell-команди через RTK, щоб зменшити витрату токенів. Використовуйте, коли виконуються git log, git diff, cargo test, pytest або інший багатослівний вивід CLI, що марнує токени context window."
allowed-tools: Bash
effort: low
metadata:
  version: 1.0.0
---

# Skill RTK optimizer

**Призначення**: Автоматично пропонувати обгортки RTK для багатослівних команд, щоб зменшити витрату токенів.

## Як це працює

1. **Виявляє багатослівні команди** у запитах користувача
2. **Пропонує обгортку RTK**, якщо застосовно
3. **Виконує через RTK**, коли користувач підтвердить
4. **Відстежує економію** протягом сесії

## Підтримувані команди

### Git (зменшення >70%)
- `git log` → `rtk git log` (зменшення 92.3%)
- `git status` → `rtk git status` (зменшення 76.0%)
- `find` → `rtk find` (зменшення 76.3%)

### Середня цінність (зменшення 50-70%)
- `git diff` → `rtk git diff` (зменшення 55.9%)
- `cat <large-file>` → `rtk read <file>` (зменшення 62.5%)

### Стек JS/TS (зменшення 70-90%)
- `pnpm list` → `rtk pnpm list` (зменшення 82%)
- `pnpm test` / `vitest run` → `rtk vitest run` (зменшення 90%)

### Інструментарій Rust (зменшення 80-90%)
- `cargo test` → `rtk cargo test` (зменшення 90%)
- `cargo build` → `rtk cargo build` (зменшення 80%)
- `cargo clippy` → `rtk cargo clippy` (зменшення 80%)

### Python і Go (зменшення 90%)
- `pytest` → `rtk python pytest` (зменшення 90%)
- `go test` → `rtk go test` (зменшення 90%)

### GitHub CLI (зменшення 79-87%)
- `gh pr view` → `rtk gh pr view` (зменшення 87%)
- `gh pr checks` → `rtk gh pr checks` (зменшення 79%)

### Файлові операції
- `ls` → `rtk ls` (стислий вивід)
- `grep` → `rtk grep` (відфільтрований вивід)

## Приклади активації

**Користувач**: "Show me the git history"
**Skill**: Виявляє `git log` → Пропонує `rtk git log` → Пояснює економію токенів 92.3%

**Користувач**: "Find all markdown files"
**Skill**: Виявляє `find` → Пропонує `rtk find "*.md" .` → Пояснює економію 76.3%

## Перевірка встановлення

Перед першим використанням переконайтеся, що RTK встановлено:
```bash
rtk --version  # Should output: rtk 0.16.0+
```

Якщо не встановлено:
```bash
# Homebrew (macOS/Linux)
brew install rtk-ai/tap/rtk

# Cargo (all platforms)
cargo install rtk
```

## Шаблон використання

```markdown
# When user requests high-verbosity command:

1. Acknowledge request
2. Suggest RTK optimization:
   "I'll use `rtk git log` to reduce token usage by ~92%"
3. Execute RTK command
4. Track savings (optional):
   "Saved ~13K tokens (baseline: 14K, RTK: 1K)"
```

## Відстеження сесії

Необов'язково: відстежуйте сукупну економію протягом сесії:

```bash
# At session end
rtk gain  # Shows total token savings for session (SQLite-backed)
```

## Граничні випадки

- **Малі виводи** (<100 символів): пропустіть RTK (накладні витрати не виправдані)
- **Уже використовуються інструменти Claude**: інструменти Grep/Read уже оптимізовані
- **Кілька команд**: обгортайте через RTK один раз пакетом, а не на кожну команду

## Конфігурація

Увімкніть через CLAUDE.md:
```markdown
## Token Optimization

Use RTK (Rust Token Killer) for high-verbosity commands:
- git operations (log, status, diff)
- package managers (pnpm, npm)
- build tools (cargo, go)
- test frameworks (vitest, pytest)
- file finding and reading
```

## Метрики (перевірені)

За результатами реального тестування:
- `git log`: 13 994 символи → 1 076 символів (зменшення 92.3%)
- `git status`: 100 символів → 24 символи (зменшення 76.0%)
- `find`: 780 символів → 185 символів (зменшення 76.3%)
- `git diff`: 15 815 символів → 6 982 символи (зменшення 55.9%)
- `read file`: 163 587 символів → 61 339 символів (зменшення 62.5%)

**У середньому: зменшення токенів на 72.6%**

## Обмеження

- 446 зірок на GitHub, активно підтримується (30 релізів за 23 дні)
- Не підходить для інтерактивних команд
- Швидкий темп розробки (перевіряйте зміни, що ламають сумісність)

## Рекомендація

**Використовуйте RTK для**: git-воркфлоу, файлових операцій, тестових фреймворків, інструментів збірки, менеджерів пакетів
**Пропускайте RTK для**: малих виводів, швидкого дослідження, інтерактивних команд

## Джерела

- RTK GitHub: https://github.com/rtk-ai/rtk
- Вебсайт RTK: https://www.rtk-ai.app/
- Оцінка: `docs/resource-evaluations/rtk-evaluation.md`
- Шаблон CLAUDE.md: `examples/claude-md/rtk-optimized.md`
