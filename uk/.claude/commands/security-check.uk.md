# Перевірка безпеки

Швидка перевірка безпеки конфігурації за базою відомих загроз. Перевіряє налаштування Claude Code на відомі шкідливі skills, вразливі MCP, небезпечні патерни та витік секретів.

**Час**: ~30 секунд | **Охоплення**: лише конфігурація Claude Code

## Інструкції

Ти аналітик безпеки. Перевір конфігурацію Claude Code користувача за базою розвідданих про загрози, що постачається в `examples/commands/resources/threat-db.yaml`. Створи стислий звіт, придатний до дій.

### Фаза 1: Завантажити базу загроз

Прочитай `examples/commands/resources/threat-db.yaml` із цього репозиторію, щоб завантажити:
- Відомих шкідливих авторів і skills
- База CVE для MCP-серверів
- Підозрілі патерни для hooks, агентів і конфігурації

### Фаза 2: Аудит MCP-серверів

Прочитай конфігурацію MCP користувача:

```bash
# Global MCP config
cat ~/.claude/mcp.json 2>/dev/null

# Project MCP config
cat .claude/mcp.json 2>/dev/null
```

**Перевір за threat-db.yaml:**
- [ ] Чи є MCP-сервер, що збігається із записом CVE? → CRITICAL
- [ ] Закріплення версій: чи всі MCP-сервери закріплено на точних версіях (не `@latest`)? → HIGH, якщо не закріплено
- [ ] Чи є прапорці `--dangerous-*` в аргументах MCP? → CRITICAL
- [ ] Чи є MCP-сервери поза безпечним списком (див. `guide/security/security-hardening.md` §1.1)? → MEDIUM (позначити для ручного перегляду)

### Фаза 3: Аудит skills і агентів

```bash
# List installed skills
ls -la .claude/skills/ 2>/dev/null
ls -la ~/.claude/skills/ 2>/dev/null

# List agents
ls -la .claude/agents/ 2>/dev/null
ls -la ~/.claude/agents/ 2>/dev/null

# Check agent allowed-tools
grep -r "allowed-tools" .claude/agents/ 2>/dev/null
grep -r "allowed-tools" ~/.claude/agents/ 2>/dev/null
```

**Перевір за threat-db.yaml:**
- [ ] Чи збігається назва skill/агента із записами `malicious_skills`? → CRITICAL
- [ ] Чи збігається автор skill/агента із записами `malicious_authors`? → CRITICAL
- [ ] Чи є агент лише з `allowed-tools: ["Bash"]`? → HIGH
- [ ] Чи є агент із надто широким доступом до інструментів + розмитим описом? → MEDIUM

**Глибокий аналіз вмісту skills (за мотивами SkillSpector):**

```bash
# Hidden instructions: HTML comments, zero-width chars, base64 blobs in skill files
grep -rn '<!--' .claude/skills/ ~/.claude/skills/ 2>/dev/null | grep -iv 'example\|comment\|html'
grep -rPn '[\x{200B}-\x{200D}\x{FEFF}\x{00AD}]' .claude/skills/ ~/.claude/skills/ 2>/dev/null
grep -rn -E '[A-Za-z0-9+/]{40,}={0,2}' .claude/skills/ ~/.claude/skills/ 2>/dev/null | grep -v 'sha\|hash\|checksum' | head -10

# Unicode deception: RTL override, homoglyphs, mixed-script identifiers
grep -rPn '[\x{202E}\x{202D}\x{200F}]' .claude/skills/ ~/.claude/skills/ 2>/dev/null

# Trigger abuse: broad/generic triggers that shadow built-in commands
grep -rn "trigger\|keyword\|when.*user" .claude/skills/ ~/.claude/skills/ 2>/dev/null | \
  grep -iE '\b(help|run|go|do|yes|ok|the|a |an |it)\b' | head -10

# Supply chain: curl|bash or remote execution in skill scripts
find .claude/skills/ ~/.claude/skills/ -name "*.sh" -o -name "*.py" 2>/dev/null | \
  xargs grep -l "curl.*|\|wget.*|\|bash.*http\|eval.*curl" 2>/dev/null

# Self-modification or persistence: cron/startup hooks written by skill scripts
find .claude/skills/ ~/.claude/skills/ -type f 2>/dev/null | \
  xargs grep -l "crontab\|launchctl\|systemctl\|~/.bashrc\|~/.zshrc\|autostart" 2>/dev/null

# Env variable harvesting: skills that read and transmit env vars
find .claude/skills/ ~/.claude/skills/ -type f 2>/dev/null | \
  xargs grep -l "os.environ\|process.env\|getenv\|printenv" 2>/dev/null | \
  xargs grep -l "curl\|requests\|fetch\|http" 2>/dev/null
```

- [ ] Приховані HTML-коментарі чи символи нульової ширини у файлах skills? → HIGH
- [ ] Blob-и Base64 (>40 символів) у вмісті skill? → HIGH (перевірити: може бути підписом чи легітимним хешем)
- [ ] Перевизначення RTL або символи unicode-обману? → HIGH
- [ ] Тригер skill перекриває вбудовану команду (help, run, clear…)? → HIGH
- [ ] Виконувані скрипти з `curl | bash` або віддаленим eval? → CRITICAL
- [ ] Skill пише в crontab, launchctl чи rc-файли shell? → CRITICAL
- [ ] Skill читає змінні середовища І робить мережеві виклики? → CRITICAL

### Фаза 4: Безпека hooks

```bash
# List all hooks
find .claude/hooks/ -type f 2>/dev/null
find ~/.claude/hooks/ -type f 2>/dev/null

# Scan hooks for suspicious patterns
grep -rn "curl\|wget\|nc \|ncat\|netcat\|base64\|eval\|exec\|/dev/tcp\|/dev/udp" .claude/hooks/ 2>/dev/null
grep -rn "curl\|wget\|nc \|ncat\|netcat\|base64\|eval\|exec\|/dev/tcp\|/dev/udp" ~/.claude/hooks/ 2>/dev/null

# Check for credential access in hooks
grep -rn "ssh\|id_rsa\|id_ed25519\|\.env\|credentials\|secret\|password\|token\|api.key" .claude/hooks/ 2>/dev/null
grep -rn "ssh\|id_rsa\|id_ed25519\|\.env\|credentials\|secret\|password\|token\|api.key" ~/.claude/hooks/ 2>/dev/null
```

**Перевір за `suspicious_patterns.hooks` у threat-db.yaml:**
- [ ] Мережеві виклики (`curl`, `wget`) → HIGH
- [ ] Ознаки reverse shell (`nc`, `/dev/tcp`) → CRITICAL
- [ ] Доступ до облікових даних (`ssh`, `.env`, `password`) → CRITICAL
- [ ] Кодування Base64 → MEDIUM (перевірити контекст)

**Архіви та виконувані файли Windows у директоріях агентів:**

```bash
# FakeGit lures hid SmartLoader ZIPs under .claude/hooks/config/ (Nov 2026)
find .claude .codex .agents .cursor .gemini ~/.claude/skills -type f \
  \( -iname '*.zip' -o -iname '*.7z' -o -iname '*.rar' -o -iname '*.exe' \
     -o -iname '*.dll' -o -iname '*.bat' -o -iname '*.cmd' -o -iname '*.msi' \) 2>/dev/null
```

- [ ] Архів або виконуваний файл Windows у директорії агента? → HIGH (ніколи не розпаковуй і не запускай його; порівняй його SHA-256 із хешами FakeGit у `iocs.malware_hashes`)

### Фаза 5: Перевірка отруєння пам'яті

```bash
# Check for suspicious instructions in memory/config files
grep -in "ignore\|forget\|override\|disregard\|you are now\|new role\|system prompt" \
  CLAUDE.md .claude/CLAUDE.md SOUL.md .claude/SOUL.md MEMORY.md .claude/MEMORY.md \
  ~/.claude/CLAUDE.md ~/.claude/MEMORY.md 2>/dev/null
```

- [ ] Патерни prompt injection у CLAUDE.md / SOUL.md / MEMORY.md? → HIGH
- [ ] Інструкції вимкнути безпеку, пропустити рев'ю чи надати широкі дозволи? → CRITICAL

### Фаза 6: Дозволи та налаштування

```bash
# Check settings
cat .claude/settings.json 2>/dev/null
cat ~/.claude/settings.json 2>/dev/null
```

- [ ] Чи існує `permissions.deny` і чи охоплює він `.env*`, `*.pem`, `*.key`, секрети? → MEDIUM, якщо відсутній
- [ ] Немає wildcard-значення `permissions.allow` для Bash чи Write? → HIGH, якщо є
- [ ] Немає `dangerouslySkipPermissions` чи подібних прапорців? → CRITICAL, якщо є

### Фаза 7: Витік секретів у конфігурації

```bash
# Check for secrets in .claude/ directory
grep -rn "sk-[a-zA-Z0-9]\{20,\}\|sk-ant-[a-zA-Z0-9]\{20,\}\|ghp_[a-zA-Z0-9]\{36\}\|AKIA[A-Z0-9]\{16\}" \
  .claude/ ~/.claude/ 2>/dev/null

# Check for private keys
grep -rn "BEGIN.*PRIVATE KEY" .claude/ ~/.claude/ 2>/dev/null
```

- [ ] API-ключі чи токени у конфігураційних файлах? → CRITICAL
- [ ] Приватні ключі в конфігурації? → CRITICAL

## Формат виводу

```
## 🛡️ Звіт перевірки безпеки

**Дата**: [мітка часу]
**Охоплення**: конфігурація Claude Code

### Підсумок результатів

| Критичність | Кількість | Статус |
|----------|-------|--------|
| 🔴 CRITICAL | X | [PASS/FAIL] |
| 🟠 HIGH | X | [PASS/FAIL] |
| 🟡 MEDIUM | X | [PASS/FAIL] |
| 🟢 LOW | X | [PASS/FAIL] |

### 🔴 Критичні проблеми
[Перелічи кожну критичну знахідку з розташуванням і виправленням]

### 🟠 Проблеми високого рівня
[Перелічи кожну знахідку високого рівня з розташуванням і виправленням]

### 🟡 Проблеми середнього рівня
[Перелічи кожну знахідку середнього рівня з розташуванням і виправленням]

### ✅ Пройдені перевірки
[Перелічи, що пройшло — важливо для впевненості]

### 🔧 Рекомендовані дії (за пріоритетом)
1. [Найтерміновіше виправлення з точною командою]
2. [Другий пріоритет]
3. [...]

### 📚 Посилання
- Повний посібник із безпеки: guide/security/security-hardening.md
- База загроз: examples/commands/resources/threat-db.yaml
- Сканування MCP: `uvx snyk-agent-scan@latest` (Snyk Agent Scan, раніше mcp-scan)
```

Якщо ВСІ перевірки пройдено, виведи:

```
## 🛡️ Звіт перевірки безпеки — УСЕ ЧИСТО ✅

**Дата**: [мітка часу]
У вашій конфігурації Claude Code відомих загроз не виявлено.

**Рекомендації для підтримання безпеки:**
- Повторно запускайте `/security-check` після встановлення нових skills чи MCP-серверів
- Запустіть `/security-audit` для комплексного аудиту проєкту + конфігурації
- Підтримуйте Claude Code оновленим (актуальні виправлення безпеки у v2.1.34+)
```

$ARGUMENTS
