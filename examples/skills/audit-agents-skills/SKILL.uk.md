---
name: audit-agents-skills
description: "Аудит агентів, skills і команд Claude Code на якість і готовність до продакшену. Використовуйте, коли треба оцінити якість skill, перевірити бали готовності до продакшену або порівняти агентів із шаблонами найкращих практик."
allowed-tools: Read Grep Glob Bash Write
effort: high
disable-model-invocation: true
metadata:
  version: 1.0.0
---

# Аудит агентів/skills/команд (розширений skill)

Комплексна система аудиту якості для агентів, skills і команд Claude Code. Дає кількісну оцінку, порівняльний аналіз і оцінку готовності до продакшену на основі найкращих галузевих практик.

## Призначення

**Проблема**: ручна перевірка агентів/skills схильна до помилок і непослідовна. Згідно з LangChain Agent Report 2026, 29,5% організацій розгортають агентів без систематичного оцінювання, через що «баги агентів» стали головним викликом (18% команд).

**Рішення**: автоматичне оцінювання якості за 16 зваженими критеріями з порогами готовності до продакшену (80% = мінімальна оцінка B для розгортання в продакшені).

**Ключові можливості**:
- Кількісна оцінка (32 бали для агентів/skills, 20 для команд)
- Зважені критерії (Identity 3x, Prompt 2x, Validation 1x, Design 2x)
- Оцінка готовності до продакшену (шкала A-F з порогом 80%)
- Порівняльний аналіз з еталонними шаблонами
- Подвійний вивід JSON/Markdown для програмної інтеграції
- Пропозиції виправлень для непройдених критеріїв

---

## Режими

| Режим | Використання | Вивід |
|------|-------|--------|
| **Quick Audit** | Лише топ-5 критичних критеріїв | Швидкий pass/fail (3-5 хв на 20 файлів) |
| **Full Audit** | Усі 16 критеріїв для кожного файлу | Детальні бали + рекомендації (10-15 хв) |
| **Comparative** | Full + порівняння з шаблонами | Аналіз + виявлення прогалин (15-20 хв) |

**За замовчуванням**: Full Audit (рекомендовано для першого запуску)

---

## Методологія

### Чому саме ці критерії?

Система з 16 критеріїв побудована на основі:
1. **Найкращих практик Claude Code** (Ultimate Guide, рядок 4921: Agent Validation Checklist)
2. **Галузевих даних** (LangChain Agent Report 2026: прогалини в оцінюванні)
3. **Збоїв у продакшені** (відгуки спільноти про жорстко прописані шляхи, відсутню обробку помилок)
4. **Патернів композиції** (skills мають посилатися на інші skills, агенти мають бути модульними)

### Філософія оцінювання

**Обґрунтування ваг**:
- **Identity (3x)**: якщо користувачі не можуть знайти/викликати агента, якість не має значення (виявлюваність > якість)
- **Prompt (2x)**: визначає надійність і точність результатів
- **Validation (1x)**: підвищує стійкість, але другорядна щодо основної функціональності
- **Design (2x)**: впливає на довгострокову підтримуваність і масштабованість

**Стандарти оцінок**:
- **A (90-100%)**: готово до продакшену, мінімальний ризик
- **B (80-89%)**: добре, відповідає порогу продакшену
- **C (70-79%)**: потребує покращень перед продакшеном
- **D (60-69%)**: суттєві прогалини, не готово до продакшену
- **F (<60%)**: критичні проблеми, потребує серйозного рефакторингу

**Відповідність галузі**: поріг 80% узгоджується з найкращими практиками програмної інженерії для розгортання в продакшені (наприклад, покриття коду >80%, частка успішних проходжень сканування безпеки).

---

## Робочий процес

### Фаза 1: Виявлення

1. **Скануйте директорії**:
   ```
   .claude/agents/
   .claude/skills/
   .claude/commands/
   examples/agents/      (if exists)
   examples/skills/      (if exists)
   examples/commands/    (if exists)
   ```

2. **Класифікуйте файли** за типом (agent/skill/command)

3. **Завантажте еталонні шаблони** (для режиму Comparative):
   ```
   guide/examples/agents/     (benchmark files)
   guide/examples/skills/     (benchmark files)
   guide/examples/commands/   (benchmark files)
   ```

### Фаза 2: Рушій оцінювання

Завантажте критерії оцінювання з `scoring/criteria.yaml`:

```yaml
agents:
  max_points: 32
  categories:
    identity:
      weight: 3
      criteria:
        - id: A1.1
          name: "Clear name"
          points: 3
          detection: "frontmatter.name exists and is descriptive"
        # ... (16 total criteria)
```

Для кожного файлу:
1. Розберіть frontmatter (YAML)
2. Витягніть розділи вмісту
3. Запустіть патерни виявлення (regex, пошук за ключовими словами)
4. Обчисліть бал: `(points / max_points) × 100`
5. Присвойте оцінку (A-F)

### Фаза 3: Порівняльний аналіз (лише режим comparative)

Для кожного файлу проєкту:
1. Знайдіть найближчий відповідний шаблон (за схожістю опису)
2. Порівняйте бали за кожним критерієм
3. Визначте прогалини: `template_score - project_score`
4. Позначте суттєві прогалини (різниця >10 балів)

**Приклад**:
```
Project file: .claude/agents/debugging-specialist.md (Score: 78%, Grade C)
Closest template: examples/agents/debugging-specialist.md (Score: 94%, Grade A)

Gaps:
- Anti-hallucination measures: -2 points (template has, project missing)
- Edge cases documented: -1 point (template has 5 examples, project has 1)
- Integration documented: -1 point (template references 3 skills, project none)

Total gap: 16 points (explains C vs A difference)
```

### Фаза 4: Генерація звіту

**Звіт Markdown** (`audit-report.md`):
- Зведена таблиця (загалом + за типами)
- Окремі бали з головними проблемами
- Детальна розбивка для кожного файлу (згортається)
- Пріоритезовані рекомендації

**Вивід JSON** (`audit-report.json`):
```json
{
  "metadata": {
    "project_path": "/path/to/project",
    "audit_date": "2026-02-07",
    "mode": "full",
    "version": "1.0.0"
  },
  "summary": {
    "overall_score": 82.5,
    "overall_grade": "B",
    "total_files": 15,
    "production_ready_count": 10,
    "production_ready_percentage": 66.7
  },
  "by_type": {
    "agents": { "count": 5, "avg_score": 85.2, "grade": "B" },
    "skills": { "count": 8, "avg_score": 78.9, "grade": "C" },
    "commands": { "count": 2, "avg_score": 92.0, "grade": "A" }
  },
  "files": [
    {
      "path": ".claude/agents/debugging-specialist.md",
      "type": "agent",
      "score": 78.1,
      "grade": "C",
      "points_obtained": 25,
      "points_max": 32,
      "failed_criteria": [
        {
          "id": "A2.4",
          "name": "Anti-hallucination measures",
          "points_lost": 2,
          "recommendation": "Add section on source verification"
        }
      ]
    }
  ],
  "top_issues": [
    {
      "issue": "Missing error handling",
      "affected_files": 8,
      "impact": "Runtime failures unhandled",
      "priority": "high"
    }
  ]
}
```

### Фаза 5: Пропозиції виправлень (необов'язково)

Для кожного непройденого критерію згенеруйте **конкретне виправлення**:

```markdown
### File: .claude/agents/debugging-specialist.md
**Issue**: Missing anti-hallucination measures (2 points lost)

**Fix**:
Add this section after "Methodology":

## Source Verification

- Always cite sources for technical claims
- Use phrases: "According to [documentation]...", "Based on [tool output]..."
- If uncertain, state: "I don't have verified information on..."
- Never invent: statistics, version numbers, API signatures, stack traces

**Detection**: Grep for keywords: "verify", "cite", "source", "evidence"
```

---

## Критерії оцінювання

Повні визначення див. у `scoring/criteria.yaml`. Стисло:

### Агенти (максимум 32 бали)

| Категорія | Вага | Кількість критеріїв | Макс. балів |
|----------|--------|----------------|------------|
| Identity | 3x | 4 | 12 |
| Prompt Quality | 2x | 4 | 8 |
| Validation | 1x | 4 | 4 |
| Design | 2x | 4 | 8 |

**Ключові критерії**:
- Зрозуміла назва (3 бали): не загальна на кшталт "agent1"
- Опис із тригерами (3 бали): містить "when"/"use"
- Визначена роль (2 бали): твердження "You are..."
- 3+ приклади (1 бал): задокументовані сценарії використання
- Єдина відповідальність (2 бали): сфокусований, не "general purpose"

### Skills (максимум 32 бали)

| Категорія | Вага | Кількість критеріїв | Макс. балів |
|----------|--------|----------------|------------|
| Structure | 3x | 4 | 12 |
| Content | 2x | 4 | 8 |
| Technical | 1x | 4 | 4 |
| Design | 2x | 4 | 8 |

**Ключові критерії**:
- Коректний SKILL.md (3 бали): правильне іменування
- Коректна назва (3 бали): малі літери, 1-64 символи, без пробілів
- Описана методологія (2 бали): є розділ із робочим процесом
- Без жорстко прописаних шляхів (1 бал): жодних `/Users/`, `/home/`
- Зрозумілі тригери (2 бали): розділ "When to use"

### Команди (максимум 20 балів)

| Категорія | Вага | Кількість критеріїв | Макс. балів |
|----------|--------|----------------|------------|
| Structure | 3x | 4 | 12 |
| Quality | 2x | 4 | 8 |

**Ключові критерії**:
- Коректний frontmatter (3 бали): name + description
- Підказка аргументів (3 бали): якщо використовується `$ARGUMENTS`
- Покроковий робочий процес (3 бали): нумеровані розділи
- Обробка помилок (2 бали): згадано режими збоїв

---

## Патерни виявлення

### Розбір frontmatter

```python
import yaml
import re

def parse_frontmatter(content):
    match = re.search(r'^---\n(.*?)\n---', content, re.DOTALL)
    if match:
        return yaml.safe_load(match.group(1))
    return None
```

### Виявлення ключових слів

```python
def has_keywords(text, keywords):
    text_lower = text.lower()
    return any(kw in text_lower for kw in keywords)

# Example
has_trigger = has_keywords(description, ['when', 'use', 'trigger'])
has_error_handling = has_keywords(content, ['error', 'failure', 'fallback'])
```

### Виявлення перетинів (перевірка на дублювання)

```python
def jaccard_similarity(text1, text2):
    words1 = set(text1.lower().split())
    words2 = set(text2.lower().split())
    intersection = words1 & words2
    union = words1 | words2
    return len(intersection) / len(union) if union else 0

# Flag if similarity > 0.5 (50% keyword overlap)
if jaccard_similarity(desc1, desc2) > 0.5:
    issues.append("High overlap with another file")
```

### Підрахунок токенів (приблизний)

```python
def estimate_tokens(text):
    # Rough estimate: 1 token ≈ 0.75 words
    word_count = len(text.split())
    return int(word_count * 1.3)

# Check budget
tokens = estimate_tokens(file_content)
if tokens > 5000:
    issues.append("File too large (>5K tokens)")
```

---

## Галузевий контекст

**Джерело**: LangChain Agent Report 2026 (публічний звіт, с. 14-22)

**Ключові висновки**:
- **29,5%** організацій розгортають агентів без систематичного оцінювання
- **18%** називають «баги агентів» своїм головним викликом
- **Лише 12%** використовують автоматичні перевірки якості (88% вручну або ніяк)
- **43%** повідомляють про труднощі з підтриманням якості агентів з часом
- **Головні проблеми**: галюцинації (31%), слабка обробка помилок (28%), нечіткі тригери (22%)

**Наслідки**:
1. **Прогалина в автоматизації**: більшість команд покладаються на ручні чеклісти (схильні до помилок у масштабі)
2. **Борг якості**: агенти, розгорнуті без перевірки, накопичують технічний борг
3. **Тягар підтримки**: 43% мають проблеми з якістю з часом (немає системи відстеження)

**Цей skill закриває**:
- Автоматизацію: замінює ручні чеклісти кількісною оцінкою
- Відстеження: вивід JSON дає змогу аналізувати тренди з часом
- Стандарти: поріг 80% задає чіткий бар'єр для продакшену

---

## Приклади виводу

### Швидкий аудит (топ-5 критеріїв)

```markdown
# Quick Audit: Agents/Skills/Commands

**Files**: 15 (5 agents, 8 skills, 2 commands)
**Critical Issues**: 3 files fail top-5 criteria

## Top-5 Criteria (Pass/Fail)

| File | Valid Name | Has Triggers | Error Handling | No Hardcoded Paths | Examples |
|------|------------|--------------|----------------|--------------------|----------|
| agent1.md | ✅ | ✅ | ❌ | ✅ | ❌ |
| skill2/ | ✅ | ❌ | ✅ | ❌ | ✅ |

## Action Required

1. **Add error handling**: 5 files
2. **Remove hardcoded paths**: 3 files
3. **Add usage examples**: 4 files
```

### Повний аудит

Повну структуру див. вище у Фазі 4: Генерація звіту.

### Порівняльний (full + бенчмарки)

```markdown
# Comparative Audit

## Project vs Templates

| File | Project Score | Template Score | Gap | Top Missing |
|------|---------------|----------------|-----|-------------|
| debugging-specialist.md | 78% (C) | 94% (A) | -16 pts | Anti-hallucination, edge cases |
| testing-expert/ | 85% (B) | 91% (A) | -6 pts | Integration docs |

## Recommendations

Focus on these gaps to reach template quality:
1. **Anti-hallucination measures** (8 files): Add source verification sections
2. **Edge case documentation** (5 files): Add failure scenario examples
3. **Integration documentation** (4 files): List compatible agents/skills
```

---

## Використання

### Базове (повний аудит)

```bash
# In Claude Code
Use skill: audit-agents-skills

# Specify path
Use skill: audit-agents-skills for ~/projects/my-app
```

### З параметрами

```bash
# Quick audit (fast)
Use skill: audit-agents-skills with mode=quick

# Comparative (benchmark analysis)
Use skill: audit-agents-skills with mode=comparative

# Generate fixes
Use skill: audit-agents-skills with fixes=true

# Custom output path
Use skill: audit-agents-skills with output=~/Desktop/audit.json
```

### Лише вивід JSON

```bash
# For programmatic integration
Use skill: audit-agents-skills with format=json output=audit.json
```

---

## Інтеграція з CI/CD

### Pre-commit hook

```bash
#!/bin/bash
# .git/hooks/pre-commit

# Run quick audit on changed agent/skill/command files
changed_files=$(git diff --cached --name-only | grep -E "^\.claude/(agents|skills|commands)/")

if [ -n "$changed_files" ]; then
    echo "Running quick audit on changed files..."
    # Run audit (requires Claude Code CLI wrapper)
    # Exit with 1 if any file scores <80%
fi
```

### GitHub Actions

```yaml
name: Audit Agents/Skills
on: [pull_request]
jobs:
  audit:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run quality audit
        run: |
          # Run audit skill
          # Parse JSON output
          # Fail if overall_score < 80
```

---

## Порівняння: команда чи skill

| Аспект | Команда (`/audit-agents-skills`) | Skill (цей файл) |
|--------|----------------------------------|-------------------|
| **Охоплення** | Лише поточний проєкт | Кілька проєктів, порівняльний |
| **Вивід** | Звіт Markdown | Markdown + JSON |
| **Швидкість** | Швидко (5-10 хв) | Повільніше (10-20 хв із comparative) |
| **Глибина** | Стандартні 16 критеріїв | Те саме + аналіз бенчмарків |
| **Пропозиції виправлень** | Через прапорець `--fix` | Вбудовані, з рекомендаціями |
| **Програмна інтеграція** | Вивід у термінал | JSON для інтеграції з CI/CD |
| **Найкраще для** | Швидких перевірок, робочого процесу розробки | Глибоких аудитів, відстеження якості |

**Рекомендація**: використовуйте команду для щоденних перевірок, а skill для релізних бар'єрів і відстеження якості.

---

## Підтримка

### Оновлення критеріїв

Відредагуйте `scoring/criteria.yaml`:
```yaml
agents:
  categories:
    identity:
      criteria:
        - id: A1.5  # New criterion
          name: "API versioning specified"
          points: 3
          detection: "mentions API version or compatibility"
```

Підвищення версії: збільшуйте `version` у frontmatter, коли змінюються критерії.

### Додавання типів файлів

Щоб підтримати нові типи файлів (наприклад, "workflows"):
1. Додайте до `scoring/criteria.yaml`:
   ```yaml
   workflows:
     max_points: 24
     categories: [...]
   ```
2. Оновіть логіку виявлення (патерни шляхів до файлів)
3. Оновіть шаблони звітів

---

## Пов'язане

- **Версія-команда**: `.claude/commands/audit-agents-skills.md`
- **Agent Validation Checklist**: посібник, рядок 4921 (16 критеріїв вручну)
- **Skill Validation**: посібник, рядок 5491 (документація специфікації)
- **Еталонні шаблони**: `examples/agents/`, `examples/skills/`, `examples/commands/`

---

## Журнал змін

**v1.0.0** (2026-02-07):
- Перший реліз
- Система з 16 критеріїв (agents/skills/commands)
- 3 режими аудиту (quick/full/comparative)
- Вивід JSON + Markdown
- Пропозиції виправлень
- Галузевий контекст (звіт LangChain 2026)

---

**Skill готовий до використання**: `audit-agents-skills`
