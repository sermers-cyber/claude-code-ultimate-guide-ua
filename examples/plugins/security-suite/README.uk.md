# Плагін Security suite

**Повне посилення безпеки воркфлоу Claude Code за 5 хвилин.**

Цей плагін об'єднує все необхідне для захисту вашого налаштування Claude Code: автоматизоване сканування безпеки, шлюзи перед комітом, відстеження загроз, перевірки відповідності та аудити конфігурації.

## Що входить

✓ **Агент Security Auditor**: спеціаліст із моделювання загроз і аналізу CVE
✓ **Швидка перевірка безпеки**: 30-секундне сканування конфігурації
✓ **Повний аудит безпеки**: 6-фазний глибокий аналіз з оцінкою /100
✓ **Шлюзи безпеки перед комітом**: блокують небезпечні операції до виконання
✓ **Аудити конфігурації**: перевіряють якість агентів, skills, команд
✓ **Шаблони відповідності**: автоматизовані чеклисти для governance

## Швидке встановлення

```bash
# From this directory:
bash install.sh

# Verify installation:
/security-check
/security-audit
/audit-agents-skills
```

**Час:** 5 хвилин. Без зовнішніх залежностей.

## Компоненти

### 1. Агент security auditor

Спеціалізований агент, зосереджений виключно на аналізі безпеки.

```bash
# Assign to a complex threat modeling task:
@security-auditor Analyze this multi-agent setup for supply chain risks
```

**Можливості:**
- Відстеження CVE та оцінка їхнього впливу
- Виявлення вразливостей ланцюга постачання
- Перевірка безпеки MCP-серверів
- Аналіз ризиків власних skills/hooks
- Зіставлення з вимогами відповідності

### 2. Швидка перевірка безпеки (`/security-check`)

30-секундне сканування. Запускайте перед комітами чи розгортаннями.

```bash
/security-check
```

**Що перевіряє:**
- ✓ Ізоляцію CLAUDE.md (жодних розкритих секретів)
- ✓ Конфігурації MCP-серверів (небезпечні дозволи?)
- ✓ Область виконання hooks (надто широкі дозволи?)
- ✓ Обмеження інструментів агентів (належна ізоляція?)
- ✓ Дозволи в Settings.json (усе закрито?)

**Вивід:**
```
Security Check: 87/100 ✓ PASS
- Agents properly isolated ✓
- No dangerous MCP configs ⚠️ REVIEW: 1 issue
- Hooks validated ✓
- CLAUDE.md secure ✓
```

### 3. Повний аудит безпеки (`/security-audit`)

6-фазний глибокий аналіз, 2-5 хвилин. Комплексна оцінка загроз.

```bash
/security-audit
```

**6 фаз:**
1. **Аудит конфігурації**: налаштування, дозволи, секрети
2. **Безпека агентів**: обмеження інструментів, ізоляція, можливості
3. **Аналіз skills/hooks**: якість коду, небезпечні патерни
4. **Перевірка MCP**: дозволи серверів, поводження з токенами
5. **Ланцюг постачання**: аналіз залежностей, зовнішні інтеграції
6. **Перевірка відповідності**: корпоративні вимоги, governance

**Вивід:**
```
Security Audit Report
════════════════════════════════════════════
Config Audit:      ████░░░░░░  80/100
Agent Security:    ██████░░░░  85/100
Skill/Hook Review: ██░░░░░░░░  20/100  ⚠️ ACTION REQUIRED
MCP Vetting:       ███░░░░░░░  65/100  ⚠️ WARNINGS
Supply Chain:      ████░░░░░░  78/100
Compliance:        ██████░░░░  88/100

OVERALL: 72/100 — Intermediate Security Posture

Critical Issues (fix immediately):
  • 3 skills use eval() — Replace with safe parsing
  • GitHub MCP has write access to all repos — Scope to specific repos
  • Hook security-check.sh runs as root — Drop privileges

Warnings (fix within 2 weeks):
  • CLAUDE.md stores test API keys — Use environment variables
  • Agent tool permissions not clearly documented

Recommendations:
  • Read: guide/security/security-hardening/
  • Reference: guide/security/ for threat patterns
  • Use: /self-assessment → identify security gaps → take training
```

### 4. Аудит конфігурації (`/audit-agents-skills`)

Перевіряє якість ваших власних агентів, skills, команд.

```bash
/audit-agents-skills
/audit-agents-skills --fix          # Get fix suggestions
/audit-agents-skills ~/other-dir    # Audit another project
```

**Перевірки:**
- ✓ Агенти мають належні обмеження інструментів
- ✓ Skills використовують правильну структуру frontmatter
- ✓ Команди мають зрозумілі описи
- ✓ Жодних захардкоджених секретів чи API-ключів
- ✓ Усі виклики інструментів безпечні

### 5. Hooks безпеки

**Hook перед комітом:** `security-gate.sh`
Блокує небезпечні операції до їх виконання:
- Запобігає `eval()` у власному коді
- Зупиняє розкриття секретів (API-ключі, токени)
- Валідує синтаксис hooks
- Перевіряє на патерни ін'єкції команд

**Hook після виконання:** `security-check.sh`
Перевіряє вивід на проблеми безпеки:
- Виявляє випадкове розкриття секретів
- Перевіряє спроби обходу шляхів (path traversal)
- Відстежує використання ресурсів (виявлення DoS)
- Позначає небезпечні патерни

## Сценарії використання

### Сценарій 1: захист командного налаштування

```
1. Run: /security-audit
2. Review report and fix Critical issues
3. Run: /audit-agents-skills --fix
4. Share results with team
5. Monthly re-audits to track improvement
```

### Сценарій 2: оцінювання стороннього skill

```
1. Download skill to examples/skills/
2. Run: /audit-agents-skills
3. Review tool restrictions and code patterns
4. If safe, integrate; otherwise reject
```

### Сценарій 3: посилення для продакшену

```
1. Run: /security-audit (current posture baseline)
2. Address all Critical issues
3. Read: guide/security/production-safety/
4. Implement recommended patterns
5. Re-audit until 90+ score achieved
```

### Сценарій 4: перевірка відповідності

```
1. Run: /security-audit
2. Check Compliance phase (item 6)
3. Map gaps to regulatory requirements
4. Create compliance.md documenting adherence
5. Audit quarterly
```

## Конфігурація

### Увімкнення hooks

Якщо hooks не вмикаються автоматично, додайте до `.claude/settings.json`:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "bash .claude/hooks/bash/security-gate.sh",
            "timeout": 3000
          }
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": ".*",
        "hooks": [
          {
            "type": "command",
            "command": "bash .claude/hooks/bash/security-check.sh",
            "async": true
          }
        ]
      }
    ]
  }
}
```

### Змінні середовища

Налаштуйте параметри безпеки:

```bash
# Maximum tool timeouts (prevent DoS)
export CLAUDE_SECURITY_TIMEOUT=30000

# Enable strict mode (block all unreviewed code)
export CLAUDE_SECURITY_STRICT=true

# Security audit level (quick|standard|paranoid)
export CLAUDE_SECURITY_LEVEL=standard
```

## Шлях навчання

**Після встановлення:**

1. **Зрозумійте загрози** → прочитайте `guide/security/security-hardening/`
2. **Оцініть своє налаштування** → запустіть `/security-check`
3. **Отримайте детальний звіт** → запустіть `/security-audit`
4. **Виправте проблеми** → дотримуйтеся рекомендацій
5. **Заглибтеся** → скористайтеся `/self-assessment`, щоб виявити прогалини в знаннях із безпеки
6. **Перевірте** → повторюйте аудит, доки не досягнете цільової оцінки (рекомендовано 85+/100)

## Видалення

```bash
bash uninstall.sh
```

Це видаляє всі компоненти Security Suite, але зберігає ваші резервні копії (файли `.bak`).

## Отримання допомоги

- **Питання?** → дивіться `guide/security/` щодо патернів загроз і способів їх пом'якшення
- **Конкретні питання щодо аудиту?** → скористайтеся агентом Security Auditor
- **Потрібна розвідка загроз?** → перегляньте `guide/core/known-issues/` щодо активних CVE
- **Впровадження в команді?** → проведіть аудит у всій команді, зведіть результати, виявіть спільні прогалини

## Версія

- **Версія плагіна:** 1.0.0
- **Потребує:** Claude Code 2.1.0+
- **Сумісні моделі:** Opus 5.5, Sonnet 5.5, Haiku 5.5

## Ліцензія

CC BY-SA 4.0 — вільно використовуйте, змінюйте за потреби, діліться покращеннями.

---

**Готові посилити своє налаштування?** Запустіть `/security-check` просто зараз.
