# Оцінка: «Claude Code built-in git worktree support» — LinkedIn, Guillaume Moigneu

**Дата оцінювання**: 2026-02-22
**Оцінювач**: Claude Code (auto)
**Ресурс**: допис у LinkedIn від Guillaume Moigneu

---

## Метадані

| Поле | Значення |
|-------|--------|
| **Джерело** | Допис у LinkedIn від Guillaume Moigneu, 2026-02-22 |
| **Автор** | Guillaume Moigneu — Solution Architecture/Advocacy @ Upsun, технічний спікер |
| **Авторитетність** | Практик (не Anthropic) — Solution Architect з досвідом розгортання |
| **Категорія** | Productivity — Worktrees + Subagents |
| **Пов'язана стаття** | https://lnkd.in/gCicQRHP (особиста стаття про worktrees) |
| **Зв'язок** | Доповнення до [2026-02-22-boris-cherny-worktree-tips-reddit.uk.md](./2026-02-22-boris-cherny-worktree-tips-reddit.uk.md) |

---

## 📄 Підсумок змісту

- **Subagent + worktree разом**: Claude може створювати worktrees для власних subagents — масштабні паралельні міграції без конфліктів запису
- **Декларативний `isolation: worktree`** (v2.1.50): у визначеннях агентів його більше не потрібно вказувати під час кожного виклику
- **Hooks `WorktreeCreate`/`WorktreeRemove`**: власне налаштування/завершення для VCS → **підтримка не-git SCM** (Perforce, SVN тощо)
- **Доступно в**: CLI (`--worktree`), Desktop app, IDE — не лише в CLI
- **Детальна стаття**: його власна стаття про worktrees (lnkd.in/gCicQRHP)

---

## 🔍 Уточнення щодо версій

Guillaume приписує все версії v2.1.50 — це трохи неточно:

| Функція | Реальна версія |
|---------|----------------|
| Прапорець CLI `--worktree` / `-w` | **v2.1.49** (2026-02-20) |
| `isolation: "worktree"` для subagents | **v2.1.49** (2026-02-20) |
| Hooks `WorktreeCreate`/`WorktreeRemove` | **v2.1.50** (2026-02-21) |
| Декларативний `isolation: worktree` у визначеннях агентів | **v2.1.50** (2026-02-21) |
| Підтримка Desktop + IDE | **v2.1.50** (підтверджено) |

---

## 🎯 Оцінка релевантності

**Оцінка: 3/5** (доповнення — не виправдовує окремої інтеграції)

**Обґрунтування**: допис не дає достатньо самостійного змісту для окремого розділу. Його цінність — у **різницях** порівняно з основним оцінюванням:
1. Hooks `WorktreeCreate`/`WorktreeRemove` → не-git SCM (деінде не охоплено)
2. Декларативний `isolation: worktree` у визначеннях агентів (бракує уточнення про v2.1.50)
3. Підтвердження Desktop + IDE (замість лише CLI в іншому оцінюванні)
4. Зовнішня стаття, на яку варто послатися

---

## ⚖️ Різниця порівняно з основним оцінюванням (Boris Cherny, Reddit)

| Аспект | Reddit/Tweet | LinkedIn Guillaume | У посібнику |
|--------|-------------|-------------------|---------------|
| `--worktree` у CLI | ✅ | ✅ | ❌ основний посібник |
| Subagents + worktrees | Згадано | **Детально (паралельні міграції)** | ❌ |
| Hooks `WorktreeCreate`/`WorktreeRemove` | ❌ | **✅ Не-git SCM** | ❌ |
| Декларативний `isolation: worktree` | ❌ | **✅** | ❌ |
| Desktop + IDE (не лише CLI) | ❌ | **✅** | ❌ |
| Зовнішня довідкова стаття | ❌ | **✅** | ❌ |

---

## 📍 Рекомендована інтеграція

**Доповнює інтеграцію, визначену в основному оцінюванні.** Додати в той самий розділ `guide/ultimate-guide.md:13408`:

```markdown
#### Subagents + Worktree Isolation

Claude can spin up worktrees for its own subagents. Declare isolation directly in agent definitions:

```yaml
# .claude/agents/migration-agent.md
---
isolation: worktree   # Each invocation gets its own worktree (v2.1.50+)
background: true
---
```

This enables write-safe parallel migrations: 4 agents refactoring different modules,
no merge conflicts because each works in its own copy.
```

**Також**: додати примітку про hooks `WorktreeCreate`/`WorktreeRemove` до розділу hooks посібника (сценарій використання з не-git SCM).

---

## ✅ Перевірка фактів

| Твердження | Перевірено | Джерело |
|-------------|----------|--------|
| Hooks `WorktreeCreate`/`WorktreeRemove` у v2.1.50 | ✅ | `guide/core/claude-code-releases.md`, рядки 30-31 |
| Декларативний `isolation: worktree` у v2.1.50 | ✅ | `guide/core/claude-code-releases.md`, рядок 32 |
| `--worktree` у v2.1.49 (не v2.1.50) | ✅ | `guide/core/claude-code-releases.md`, рядок 53 |
| Підтримка Desktop + IDE | ✅ (неявно) | Нотатки до v2.1.50 |
| Не-git SCM через hooks | ✅ | Події hooks `WorktreeCreate`/`WorktreeRemove` |
| Стаття Guillaume: lnkd.in/gCicQRHP | ⚠️ | Скорочений URL LinkedIn — не перевірено безпосередньо |

---

## 🎯 Остаточне рішення

- **Остаточна оцінка**: 3/5
- **Дія**: **Інтегрувати як доповнення**: без окремого розділу, збагачує інтеграцію з основного оцінювання
- **Нові елементи для додавання до посібника**:
  1. Декларативний `isolation: worktree` у визначеннях агентів (приклад YAML)
  2. Hooks `WorktreeCreate`/`WorktreeRemove` → розділ hooks
  3. Згадка про підтримку Desktop + IDE
  4. Стаття Guillaume як зовнішнє посилання
