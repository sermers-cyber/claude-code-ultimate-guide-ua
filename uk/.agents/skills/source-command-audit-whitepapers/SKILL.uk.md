---
name: "source-command-audit-whitepapers"
description: "Аудит актуальності версій, паритету FR/EN та якості метаданих усіх whitepapers і карток-конспектів"
---

# source-command-audit-whitepapers

Використовуй цей skill, коли користувач просить виконати мігровану вихідну команду `audit-whitepapers`.

## Command Template

# Аудит whitepapers і карток-конспектів

Комплексний аудит актуальності та якості всіх whitepapers (FR + EN) і карток-конспектів (FR + EN). Оцінює кожен документ щодо поточної версії посібника, перевіряє паритет FR/EN і валідує узгодженість метаданих.

## Аргументи

- `--fix` - Згенерувати пропозиції оновлень і патчі frontmatter (файли не змінюються)
- `--verbose` - Показати всі критерії, зокрема пройдені, а не лише збої
- `--cards-only` - Аудит лише карток-конспектів (пропустити основні whitepapers)
- `--wp-only` - Аудит лише основних whitepapers (пропустити картки-конспекти)

## Використання

```bash
/audit-whitepapers                  # Full audit, failures only
/audit-whitepapers --fix            # Audit + prioritized update suggestions
/audit-whitepapers --verbose        # Full details for all criteria
/audit-whitepapers --cards-only     # Recap cards only
/audit-whitepapers --wp-only        # Whitepapers only
```

---

## Фаза 1: Виявлення

**Мета**: знайти й інвентаризувати всі документи, що підлягають аудиту.

### Кроки

1. **Прочитай поточну версію посібника**: прочитай файл `VERSION` у корені проєкту. Це цільова версія, із якою мають бути синхронізовані всі документи.

2. **Скануй теки** на файли `.qmd`:
   ```
   whitepapers/fr/         (main whitepapers FR)
   whitepapers/en/         (main whitepapers EN)
   whitepapers/recap-cards/fr/    (recap cards FR)
   whitepapers/recap-cards/en/    (recap cards EN)
   ```

3. **Класифікуй кожен файл**:
   - **Основний whitepaper**: файли, що відповідають `[0-9][0-9]-*.qmd` у `whitepapers/fr/` або `whitepapers/en/`
   - **Cheatsheet**: файли, що відповідають `*cheatsheet*.qmd` (відстежуються окремо, не оцінюються)
   - **Кастомний whitepaper**: файли, що відповідають `*-whitepaper.qmd` або `*-cheatsheet.qmd` від зовнішніх партнерів (strangebee, purchasely, devwithai) -- виключаються з оцінювання, перелічуються окремо
   - **Картка-конспект**: усі файли `.qmd` у `recap-cards/fr/` або `recap-cards/en/`
   - **Bundle/include**: `fiches-recap-serie.qmd`, файли в підтеці `fiches/` -- виключаються (це складені документи)

4. **Розбери YAML frontmatter** кожного включеного файлу (читай між першим `---` і другим `---`). Витягни:
   - `title`, `subtitle`, `author`, `date`
   - `version` (версія посібника, що відстежується в основних WP і картках-конспектах)
   - `wp-version` (власний semver whitepaper, лише основні WP)
   - `guide-version` (явне поле версії посібника, що використовується в картках-конспектах)
   - `card-number`, `category`, `difficulty` (лише картки-конспекти)
   - `series` (лише основні WP)

5. **Покажи підсумок виявлення**:
   ```
   Guide version: {VERSION}
   Found: {N} main whitepapers ({FR}/{EN} FR/EN), {N} recap cards ({FR}/{EN} FR/EN)
   Excluded: {N} custom files (strangebee, purchasely, devwithai), {N} bundle files
   ```

---

## Фаза 2: Аналіз розриву версій (40 балів на файл)

**Мета**: оцінити, наскільки актуальний кожен документ щодо посібника.

### Логіка порівняння semver

Розбери рядки версій як `MAJOR.MINOR.PATCH`. Метрика застарілості: `minor_gap = current_minor - file_minor` (за тієї самої MAJOR). Якщо MAJOR відрізняється, вважай це критичним.

Для **основних whitepapers** полем версії посібника є `version`.
Для **карток-конспектів** полем версії посібника є `guide-version` (якщо його немає, використовуй `version`).

### Таблиця оцінювання

| Критерій | Бали | Виявлення |
|----------|------|-----------|
| Версія посібника актуальна (відставання на 0-1 minor) | 15 | `minor_gap` <= 1 |
| Версія посібника недавня (відставання на 2-3 minor) | 10 | `minor_gap` 2-3 (часткові бали, замінює 15) |
| Версія посібника стара (відставання на 4-10 minor) | 5 | `minor_gap` 4-10 (часткові бали) |
| Поле wp-version присутнє та є валідним semver | 5 | Поле існує І відповідає `\d+\.\d+\.\d+` (лише WP) |
| wp-version узгоджена з парою FR/EN | 10 | Те саме значення `wp-version` у парному файлі (лише WP) |
| guide-version узгоджена з парою FR/EN | 10 | Те саме `guide-version` (або `version`) у парному файлі (картки) |

**Мітки актуальності**:
- Відставання на 0-1 minor: Fresh
- Відставання на 2-3 minor: Stale
- Відставання на 4-10 minor: Very Stale
- Відставання на 11+ minor: Critical

Примітка: 15, 10, 5 балів за версію посібника взаємовиключні (нараховуй лише найвищий застосовний рівень).

---

## Фаза 3: Перевірка застарілості вмісту (20 балів на файл)

**Мета**: виявити, чи змінилися розділи посібника, які охоплює whitepaper, відтоді як його востаннє оновлювали.

### Зіставлення whitepaper → посібник (вбудоване)

| WP# | Префікс імені файлу FR | Префікс імені файлу EN | Розділи посібника |
|-----|------------------------|------------------------|-------------------|
| 00 | `00-introduction` | `00-series-introduction` | `guide/ultimate-guide.md` Ch.1-2 |
| 01 | `01-prompts` | `01-effective-prompts` | Ch.2 prompting sections |
| 02 | `02-personnalisation` | `02-customization` | Ch.3 Memory, Ch.4 Agents, Ch.5 Skills |
| 03 | `03-securite` | `03-security` | Ch.7 Hooks, security sections |
| 04 | `04-architecture` | `04-architecture` | Ch.2 internals, architecture sections |
| 05 | `05-equipe` | `05-team` | Ch.3 team config, Ch.9 CI/CD |
| 06 | `06-privacy` | `06-privacy` | Ch.2 data/privacy sections |
| 07 | `07-guide-reference` | `07-reference-guide` | Ch.10 Reference |
| 08 | `08-agent-teams` | `08-agent-teams` | Ch.9 agent teams |
| 09 | `09-apprendre` | `09-learning` | `guide/roles/learning-with-ai.md` |
| 10 | `10-budget` | `10-ai-budget` | Business/ROI content |

### Кроки

1. Для кожного основного whitepaper витягни поле `date`. Якщо дата не у форматі `YYYY-MM-DD`, розбери її (наприклад, "2026-02-12" або "March 2026").
2. Виконай `git log --since="{date}" --oneline -- guide/ultimate-guide.md guide/roles/ guide/core/`, щоб порахувати коміти, які зачепили вміст посібника відтоді, як датовано whitepaper.
3. Оціни:

| Критерій | Бали | Виявлення |
|----------|------|-----------|
| Немає комітів посібника з дати wp | 10 | `git log` повертає 0 комітів |
| Мало комітів з дати wp (1-5) | 7 | 1-5 комітів (частково) |
| Помірно комітів (6-15) | 4 | 6-15 комітів (частково) |
| Багато комітів (>15) | 0 | Понад 15 комітів |
| Для цього WP визначено зіставлення | 5 | Номер WP є в таблиці зіставлення вище |
| Історія git доступна | 5 | Команда `git log` виконується без помилок |

**Картки-конспекти**: пропусти детальний git-аналіз. Нарахуй фіксований бал застарілості на основі `minor_gap`:
- Відставання 0-1: 20 балів
- Відставання 2-3: 15 балів
- Відставання 4-10: 8 балів
- Відставання 11+: 0 балів

---

## Фаза 4: Перевірка паритету FR/EN (20 балів на файл)

**Мета**: кожен документ має мати повну, узгоджену за версією пару іншою мовою.

### Стратегія зіставлення пар

**Основні whitepapers**: зіставляй за двоцифровим числовим префіксом (наприклад, `00`, `03`, `10`). Імена файлів FR і EN відрізняються, але префікс однаковий.

**Картки-конспекти**: зіставляй за ідентичним ім'ям файлу (обидві мовні теки використовують однакові імена файлів).

### Таблиця оцінювання

| Критерій | Бали | Виявлення |
|----------|------|-----------|
| Парний файл існує іншою мовою | 10 | Знайдено файл із відповідним префіксом (WP) або ідентичним ім'ям (картки) |
| wp-version збігається в парі | 5 | Те саме значення `wp-version` (лише WP) |
| Версія посібника збігається в парі | 5 | Те саме значення `version`/`guide-version` |

Оцінюй обидва файли пари, FR і EN, однаково за паритетом (якщо пара повна, обидва отримують 20; якщо одного бракує, наявний файл отримує 0 за паритет).

---

## Фаза 5: Якість метаданих (20 балів на файл)

**Мета**: перевірити повноту frontmatter, формати полів і узгодженість між файлами одного типу.

### Основні whitepapers (макс. 20 балів)

| Критерій | Бали | Виявлення |
|----------|------|-----------|
| Обов'язкові поля присутні | 6 | Є всі: `title`, `subtitle`, `author`, `date`, `version`, `wp-version`, `series` |
| `version` відповідає шаблону semver | 3 | Відповідає `\d+\.\d+\.\d+` |
| `wp-version` відповідає шаблону semver | 3 | Відповідає `\d+\.\d+\.\d+` |
| `date` можна розібрати й вона не з майбутнього | 3 | Валідна дата, не пізніша за сьогодні |
| Значення `series` узгоджене | 2 | Дорівнює "Codex Ultimate Guide" |
| Немає відсутнього `wp-version` (не порожній і не пропущений) | 3 | Поле має непорожнє значення |

### Картки-конспекти (макс. 20 балів)

| Критерій | Бали | Виявлення |
|----------|------|-----------|
| Обов'язкові поля присутні | 5 | Є всі: `title`, `subtitle`, `card-number`, `category`, `difficulty`, `guide-version`, `author`, `version`, `date` |
| `card-number` збігається з префіксом імені файлу | 4 | наприклад, `C01` у `card-number` збігається з `c01-` в імені файлу |
| `category` допустима для мови | 4 | FR: одна з "Technique", "Methodologie", "Conception"; EN: одна з "Technical", "Methodology", "Design" (познач "Conceptual" як неузгоджене в EN) |
| `difficulty` має допустиме значення | 3 | Одне з: "beginner", "intermediate", "advanced" |
| Поля `guide-version` і `version` збігаються між собою | 4 | Обидва поля існують і мають однакове значення в одному файлі |

**Відома проблема, яку слід виявляти автоматично**: картки серії C в EN використовують два різні значення категорії ("Conceptual" у c01-c05, "Design" у c06+). Явно познач цю неузгодженість у розділі Metadata Issues звіту.

---

## Фаза 6: Оцінювання та виставлення оцінок

### Формула балів (на файл)

```
Total = Version Gap (40) + Content Staleness (20) + FR/EN Parity (20) + Metadata Quality (20)
Score = (Total / 100) * 100  [as a percentage]
```

### Шкала оцінок

| Оцінка | Бали | Статус |
|--------|------|--------|
| A | 90-100 | Свіжий, повністю синхронізований |
| B | 80-89 | Добре (поріг для продакшену) |
| C | 70-79 | Незабаром потребує оновлення |
| D | 60-69 | Застарілий, слід пріоритезувати |
| F | <60 | Критично: вміст імовірно застарів |

### Загальний показник здоров'я

```
Weighted Health = (Sum of WP scores * 2 + Sum of card scores * 1) / (WP count * 2 + card count * 1)
```

Whitepapers мають вагу 2x, бо мають по 20-80 сторінок проти 2-сторінкових карток-конспектів. Застарілий whitepaper несе більший ризик.

---

## Фаза 7: Звіт

Виведи наведений нижче звіт у Markdown. Використовуй блоки `<details>` для розбивки за окремими файлами, щоб верхній рівень було легко проглядати.

```markdown
# Whitepaper & Recap Card Audit

**Date**: {today}
**Guide Version**: {VERSION}
**Overall Health**: {score}% ({grade})
**Files Audited**: {total} ({wp_count} whitepapers, {card_count} recap cards)

---

## Version Status Dashboard

| Status | Whitepapers | Recap Cards | Total |
|--------|-------------|-------------|-------|
| Fresh (0-1 minor behind)   | N | N | N |
| Stale (2-3 minor behind)   | N | N | N |
| Very Stale (4-10 behind)   | N | N | N |
| Critical (11+ behind)      | N | N | N |

**Versions currently in use**:
- Main WP 00-09: {version} ({gap} minor versions behind)
- Main WP 10: {version} ({gap} minor versions behind)
- Recap cards: {guide-version} ({gap} minor versions behind)

---

## Whitepaper Scores

| WP# | Title | version | Gap | wp-version | Parity | Score | Grade |
|-----|-------|---------|-----|------------|--------|-------|-------|
| 00  | ...   | ...     | -N  | ...        | OK/gap | N%    | X     |
...

<details>
<summary>Individual criteria breakdown (WP 00)</summary>

| Phase | Criterion | Result | Points |
|-------|-----------|--------|--------|
| Version Gap | Guide version current | Critical (-11) | 0/15 |
| Version Gap | wp-version valid semver | OK | 5/5 |
| ... | ... | ... | ... |
| **Total** | | | **N/100** |
</details>

---

## Recap Card Scores

| Series | Cards | Avg guide-version | Avg Gap | Avg Score | Grade |
|--------|-------|-------------------|---------|-----------|-------|
| T (Technical)    | 22 | ... | -N | N% | X |
| M (Methodology)  | 22 | ... | -N | N% | X |
| C (Conceptual)   | 13 | ... | -N | N% | X |

<details>
<summary>Individual card scores</summary>

| Card | Category | guide-version | Gap | Parity | Metadata | Score | Grade |
|------|----------|---------------|-----|--------|----------|-------|-------|
...
</details>

---

## FR/EN Parity Report

### Whitepapers
| WP# | FR | EN | wp-version Match | version Match |
|-----|----|----|------------------|---------------|
...

### Recap Cards
- **FR count**: {N} | **EN count**: {N}
- **Missing FR**: [list or "None"]
- **Missing EN**: [list or "None"]
- **Version mismatches**: [list or "None"]

---

## Metadata Issues

### Known: EN Recap Card Category Inconsistency
EN C-series cards use two different values for the "Conceptual/Design" category:
- "Conceptual": c01, c02, c03, c04, c05
- "Design": c06, c07, c08, ...
Recommendation: standardize to "Design" to match guide terminology.
Affected files: whitepapers/recap-cards/en/c01-*.qmd through c05-*.qmd (change "Conceptual" to "Design")

### Other issues
[List any missing fields, bad formats, date issues...]

---

## Prioritized Action Items

### Critical (Grade F, 11+ versions behind)
[List specific whitepapers with filename paths]

### High (Grade D-F, 2+ versions behind)
[List specific files]

### Medium (Metadata quality, category fixes)
[List specific issues]

### Low (Polish, date alignment)
[List specific issues]

---

## Next Steps

1. Run `/update-whitepapers --since {oldest_version}` to update all stale WPs
2. Fix EN category inconsistency (5 files: c01 through c05, change "Conceptual" to "Design")
3. Re-run `/audit-whitepapers` after updates to track progress
4. Target: 80%+ health (Grade B) across all files
```

---

## Режим виправлення (`--fix`)

Коли передано `--fix`, додай розділ **Fix Suggestions** після звіту. Цей розділ дає конкретні патчі, але НЕ змінює жодних файлів.

### Патчі версії у frontmatter

Для кожного файлу із застарілою версією посібника виведи:
```yaml
# File: whitepapers/fr/00-introduction-serie.qmd
# Change:
version: "3.27.6"  ->  version: "{current_VERSION}"
date: 2026-02-12   ->  date: {today}
```

### Патчі категорій (картки-конспекти EN)

```
Files to update (category: "Conceptual" -> "Design"):
- whitepapers/recap-cards/en/c01-trust-calibration.qmd
- whitepapers/recap-cards/en/c02-*.qmd
- whitepapers/recap-cards/en/c03-*.qmd
- whitepapers/recap-cards/en/c04-*.qmd
- whitepapers/recap-cards/en/c05-*.qmd
```

### Чек-лист команд оновлення

На основі виявлених застарілих WP виведи команди `/update-whitepapers`, які слід виконати по порядку:
```
Suggested update sequence:
1. /update-whitepapers --since {oldest_stale_version} --wp 00,01,02,03,04,05,06,07,08,09
2. /update-whitepapers --since {oldest_stale_version} --wp 10
3. Review and bump wp-version for each updated WP (patch = content corrections, minor = new sections)
4. Bump guide-version in all recap cards to {current_VERSION}
5. Re-run /audit-whitepapers to verify
```

---

## Докладний режим (`--verbose`)

Коли передано `--verbose`, розгорни всі блоки `<details>` за замовчуванням і покажи повну таблицю критеріїв для кожного перевіреного файлу (усі критерії, а не лише збої).

---

## Довідник винятків

Наведені нижче файли виключаються з оцінювання (перелічуються лише в підсумку виявлення):

| Шаблон | Причина |
|--------|---------|
| `strangebee-*.qmd`, `purchasely-*.qmd`, `devwithai-*.qmd` | Кастомні файли клієнтів/партнерів, окремий життєвий цикл |
| `fiches-recap-serie.qmd`, `fiches/*.qmd` | Bundle/include файли, немає незалежного версіонування |
| `*_quarto.yml`, `references.bib` | Конфігурація збірки, не вміст |
| `cheatsheet.qmd` | Перелічено окремо у виявленні, не оцінюється в основному аудиті |
