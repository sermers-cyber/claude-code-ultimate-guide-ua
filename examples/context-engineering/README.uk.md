# Шаблони context engineering

Context engineering — це практика свідомого проєктування того, яку інформацію Claude отримує на початку сесії: ви ставитеся до свого `CLAUDE.md` і допоміжних файлів як до продакшн-системи, а не як до одноразового налаштування. Ці шаблони дають усе потрібне, щоб побудувати, виміряти й підтримувати таку систему.

## Файли

| Файл | Опис |
|------|-------------|
| `profile-template.yaml` | Профіль розробника для збирання контексту під конкретну людину |
| `skeleton-template.md` | Анотований каркас `CLAUDE.md` з настановами для кожного розділу |
| `assembler.ts` | Скрипт TypeScript для збирання `CLAUDE.md` з профілю + модулів |
| `eval-questions.yaml` | 20 запитань для самооцінки, щоб провести аудит вашого `CLAUDE.md` |
| `canary-check.sh` | Скрипт тестування поведінкових регресій (структурна валідація) |
| `ci-drift-check.yml` | Воркфлоу GitHub Actions для щотижневого виявлення дрейфу контексту |
| `context-budget-calculator.sh` | Вимірює постійну вартість у токенах вашої конфігурації контексту |
| `rules/knowledge-feeding.md` | Шаблон правила для проактивного оновлення контексту після сесій |
| `rules/update-loop-retro.md` | Шаблон ретроспективи сесії для фіксації висновків |

## Швидкий старт

**Новий проєкт — робочий `CLAUDE.md` за 3 кроки:**

```bash
# 1. Copy the skeleton and fill in your project details
cp examples/context-engineering/skeleton-template.md CLAUDE.md

# 2. Check your context budget (keep it under 10K tokens)
bash examples/context-engineering/context-budget-calculator.sh .

# 3. Run canary checks to validate structure
bash examples/context-engineering/canary-check.sh .
```

**Наявний проєкт — аудит і покращення:**

```bash
# Run the structural check
bash examples/context-engineering/canary-check.sh .

# Then use eval-questions.yaml to score your CLAUDE.md manually
# Target: 16+ / 20
```

**Налаштування для команди — профілі для кожного розробника:**

```bash
# Install dependencies for the assembler
npm install js-yaml @types/js-yaml ts-node typescript

# Copy the profile template and customize
cp examples/context-engineering/profile-template.yaml .claude/profiles/yourname.yaml
# Edit .claude/profiles/yourname.yaml with your stack and preferences

# Assemble your CLAUDE.md
ts-node examples/context-engineering/assembler.ts \
  --profile .claude/profiles/yourname.yaml \
  --modules .claude/modules \
  --output CLAUDE.md
```

**Постійна підтримка:**

```bash
# Weekly: run canary checks
bash examples/context-engineering/canary-check.sh .

# After sessions: use the retro template
# See rules/update-loop-retro.md

# Add the CI workflow for automated drift detection
cp examples/context-engineering/ci-drift-check.yml .github/workflows/context-drift.yml
```

## Розділ посібника

Повна методологія та принципи: `guide/core/context-engineering.md`

Шаблони тут — це операційний рівень, а посібник пояснює міркування, що стоять за кожним рішенням щодо дизайну.
