---
name: autoresearch
description: "Автономний цикл покращення: виміряти метрики кодової бази, створити файли експерименту, запускати ітерації агента, доки метрика не покращиться"
argument-hint: "[--scaffold <loop-name>] [--run <loop-name>] [--status]"
effort: high
disable-model-invocation: true
---

# Autoresearch: автономний цикл покращення

Вимірюйте метрики якості кодової бази, пропонуйте цикли покращення й запускайте автономні ітерації агента. Натхненно [karpathy/autoresearch](https://github.com/karpathy/autoresearch), адаптовано з досліджень ML до якості коду.

**Концепція**: агент пропонує зміну коду, запускає вимірювання, залишає зміну, якщо метрика покращилася, відкочує через `git reset`, якщо ні, і повторює, доки його не зупинять вручну.

**Час**: сканування ~30 с | одна ітерація: залежить від обсягу | цикл: працює безкінечно, доки ви його не зупините

---

## Режим 1: Сканування (за замовчуванням)

Виміряйте поточний стан, знайдіть наявні цикли, запропонуйте наступні дії.

### Інструкції

Запустіть наведені нижче вимірювання й покажіть пріоритезовану таблицю пропозицій.

**Крок 1: Виміряйте метрики кодової бази**

Адаптуйте патерни grep до конвенцій свого проєкту. Це типові значення для TypeScript, налаштуйте їх під свій стек.

```bash
# M1: Function declarations (prefer arrow functions)
M1=$(grep -r "export function " src/ --include="*.ts" --include="*.tsx" -l 2>/dev/null | wc -l | tr -d ' ')

# M2: Interface declarations (prefer type aliases)
M2=$(grep -r "export interface " src/ --include="*.ts" --include="*.tsx" -l 2>/dev/null | wc -l | tr -d ' ')

# M3: ESLint disables
M3=$(grep -r "eslint-disable" src/ --include="*.ts" --include="*.tsx" -l 2>/dev/null | wc -l | tr -d ' ')

# M4: Type casts to any
M4=$(grep -r " as any" src/ --include="*.ts" --include="*.tsx" -l 2>/dev/null | wc -l | tr -d ' ')

# M5: TODO comments
M5=$(grep -r "// TODO" src/ --include="*.ts" --include="*.tsx" -l 2>/dev/null | wc -l | tr -d ' ')
```

**Крок 2: Знайдіть наявні цикли**

```bash
for dir in scripts/autoresearch/loop-*/; do
  [ -d "$dir" ] || continue
  LOOP_NAME=$(basename "$dir")
  # Check if loop has results
  if [[ -f "$dir/results.tsv" ]]; then
    ITERS=$(wc -l < "$dir/results.tsv" | tr -d ' ')
    BEST=$(sort -t$'\t' -k2 -n "$dir/results.tsv" | head -1 | cut -f2)
    echo "ACTIVE:$LOOP_NAME:iterations=$ITERS:best=$BEST"
  else
    echo "SCAFFOLDED:$LOOP_NAME"
  fi
done
```

**Крок 3: Покажіть результат**

```
Autoresearch Scan: {date}

Codebase metrics:

| # | Loop              | Metric            | Current | Target | Priority | Risk |
|---|-------------------|-------------------|---------|--------|----------|------|
| A | loop-remove-as-any| `as any` casts    | {M4}    | 0      | P1       | LOW  |
| B | loop-eslint-disable| eslint-disable   | {M3}    | 0      | P2       | MED  |
| C | loop-export-fn    | export function   | {M1}    | 0      | P1       | LOW  |
| D | loop-interface-type| export interface | {M2}    | 0      | P1       | LOW  |
| E | loop-todo-comments| TODO comments     | {M5}    | 0      | P3       | LOW  |

Existing loops: {detected loops or "none yet"}

Recommended next step (P1, LOW risk):
  /autoresearch --scaffold loop-remove-as-any
  Then write program.md, create a worktree, and run the loop.
```

---

## Режим 2: `--scaffold <loop-name>`

Згенеруйте 3 механічні файли для циклу. **Не генерує `program.md`**: напишіть його самостійно, щоб закласти обмеження, специфічні для проєкту.

### Інструкції

Створіть такі файли в `scripts/autoresearch/{loop-name}/`:

**`measure.sh`**: оцінювальний harness (одна метрика, повертає ціле число):

```bash
#!/usr/bin/env bash
# measure.sh: {loop-name}
# Returns an integer. Direction: lower = better (unless loop targets coverage/score).
set -euo pipefail
grep -r "PATTERN" src/ --include="*.ts" --include="*.tsx" 2>/dev/null | wc -l | tr -d ' '
```

**`direction.txt`**: напрям покращення:

```
lower
```

(Використовуйте `higher` для метрик на кшталт тестового покриття чи бала якості.)

**`files.txt`**: область, у якій має працювати агент:

```
src/
```

Після створення файлів покажіть:

```
Loop scaffolded: scripts/autoresearch/{loop-name}/

  measure.sh  : {pattern} in {scope} -> {N} occurrences today
  direction   : lower (fewer = better)
  files.txt   : src/

Current metric: {N} (target: 0)

Next steps:
  1. Write program.md -- agent behavior, constraints, what it can/cannot touch
     Reference: scripts/autoresearch/loop-remove-as-any/program.md
  2. Create a worktree: /worktree feature/autoresearch-{loop-name}
  3. cd into the worktree
  4. bash scripts/autoresearch/runner.sh {loop-name} 0 15
```

---

## Режим 3: `--run <loop-name>`

Запустіть автономний цикл. Агент працює безкінечно: зупиніть його вручну, коли результат вас задовольнить.

### Інструкції

**Перевірте передумови:**

```bash
[ -f "scripts/autoresearch/{loop-name}/measure.sh" ] || { echo "ERROR: measure.sh missing. Run --scaffold first."; exit 1; }
[ -f "scripts/autoresearch/{loop-name}/program.md" ] || { echo "ERROR: program.md missing. Write it first, this encodes your constraints."; exit 1; }
```

**Запустіть цикл:**

Перед стартом повністю прочитайте `scripts/autoresearch/{loop-name}/program.md`. Потім увійдіть у такий цикл і повторюйте його, доки вас не зупинять:

```
LOOP ITERATION #{N}

1. Current metric: bash scripts/autoresearch/{loop-name}/measure.sh
2. Read program.md constraints
3. Propose ONE targeted change to files in files.txt
4. Apply the change
5. Re-measure: bash scripts/autoresearch/{loop-name}/measure.sh
6. Evaluate:
   - direction=lower AND new < previous -> KEEP (git add -p && git commit -m "autoresearch: {description}")
   - otherwise -> REVERT (git checkout -- .)
7. Log to results.tsv: {timestamp}\t{metric}\t{status}\t{description}
8. Continue to iteration #{N+1}
```

**Критерії зупинки** (з program.md):
- Метрика досягає цілі (наприклад, 0)
- Механічних змін більше не можна зробити
- Користувач зупиняє процес вручну

**Показуйте кожну ітерацію:**

```
[iter #{N}] metric: {before} -> {after} | {KEPT/REVERTED} | {change description}
```

---

## Режим 4: `--status`

Покажіть стан усіх циклів у проєкті.

### Інструкції

```bash
for dir in scripts/autoresearch/loop-*/; do
  [ -d "$dir" ] || continue
  NAME=$(basename "$dir")
  CURRENT=$(bash "$dir/measure.sh" 2>/dev/null || echo "?")
  ITERS=$([ -f "$dir/results.tsv" ] && wc -l < "$dir/results.tsv" | tr -d ' ' || echo "0")
  KEPT=$([ -f "$dir/results.tsv" ] && grep -c "KEPT" "$dir/results.tsv" || echo "0")
  echo "$NAME | current: $CURRENT | iters: $ITERS | kept: $KEPT"
done
```

Покажіть:

```
Autoresearch Status

| Loop                | Current | Iterations | Kept | Status    |
|---------------------|---------|------------|------|-----------|
| loop-remove-as-any  | {N}     | {N}        | {N}  | ACTIVE    |
| loop-export-fn      | {N}     | 0          | 0    | SCAFFOLDED|
```

---

## Написання `program.md`: найважливіший файл

`program.md` є контрактом поведінки агента. Пишіть його самі, ніколи не генеруйте автоматично. Він має фіксувати, чого агент може і чого не може торкатися саме у вашій кодовій базі.

**Мінімальна структура:**

```markdown
# Program: {loop-name}

## Objective
Reduce `{metric}` in `src/` to 0. One mechanical change per iteration.

## Measurement
bash scripts/autoresearch/{loop-name}/measure.sh
Lower = better. Target: 0.

## What you CAN do
- Replace `export function X(` with `export const X = (`
- Keep the function signature identical

## What you CANNOT do
- Modify test files
- Change function signatures
- Touch files outside src/
- Make multiple changes per iteration

## Stop when
- Metric = 0
- No more mechanical replacements exist
```

---

## Патерн (передісторія)

Ця команда реалізує патерн **autoresearch loop** з [karpathy/autoresearch](https://github.com/karpathy/autoresearch):

| Дослідження ML (karpathy) | Якість коду (ця команда) |
|------------------------|----------------------------|
| Змінити `train.py` | Змінити файли в `src/` |
| Виміряти `val_bpb` | Виміряти кількість збігів grep |
| 5-хвилинний бюджет GPU | Одна атомарна зміна за ітерацію |
| Залишити, якщо val_bpb покращився | Залишити, якщо кількість зменшилась |
| `git reset`, якщо ні | `git checkout -- .`, якщо ні |
| `program.md` = skill агента | `program.md` = skill агента |

Ключова думка: фіксована об'єктивна метрика + git як механізм відкату = безпечна автономна ітерація. Агенту не потрібне схвалення людини для кожної зміни, бо кожна погана зміна автоматично відкочується.

---

## Використання

**Сканувати й запропонувати цикли:**
```
/autoresearch
```

**Створити файли для конкретного циклу:**
```
/autoresearch --scaffold loop-remove-as-any
```

**Запустити автономний цикл (після написання program.md):**
```
/autoresearch --run loop-remove-as-any
```

**Перевірити стан усіх циклів:**
```
/autoresearch --status
```

$ARGUMENTS
