---
title: "Керування інструкціями для командної AI"
description: "Масштабування CLAUDE.md у команді розробників за допомогою профільного збирання модулів (Profile-Based Module Assembly)"
tags: [workflow, team, claude-md, configuration]
---

# Керування інструкціями для командної AI

Керуйте інструкціями для AI (CLAUDE.md, .cursorrules) у команді без виникнення фрагментації.

**Шаблон**: Профільне збирання модулів (Profile-Based Module Assembly): спільні модулі плюс профілі окремих розробників плюс автоматичний збирач (assembler).

**Коли використовувати**: Команда від 5 розробників, використання кількох інструментів AI (Claude Code + Cursor/Windsurf), змішані операційні системи.
**Пропустити, якщо**: Один розробник, однорідна команда (однаковий інструмент, однакова ОС), короткий проект (<3 місяців).

---

## Проблема: Фрагментація N x M x P

Коли команда зростає, інструкції для AI швидко фрагментуються:

| Фактор | Значення | Приклад |
|--------|--------|---------|
| **N розробників** | 5-20 | Alice, Bob, Charlie... |
| **M інструментів** | 2-4 | Claude Code, Cursor, Windsurf, Copilot |
| **P операційних систем** | 2-3 | macOS, Linux, WSL |

**Загальна кількість варіантів**: N x M x P = 5 x 3 x 2 = **30 можливих конфігурацій**.

Що відбувається без системи:

```
Тиждень 1: Команда узгоджує спільний файл CLAUDE.md
Тиждень 3: Alice локально додає строгі правила для TypeScript
Тиждень 5: Bob копіює файл у Alice, видаляючи половину правил
Тиждень 8: Новий працівник Charlie отримує застарілу копію Bob
Тиждень 12: 5 розробників, 5 різних файлів CLAUDE.md, ніхто не знає, який з них канонічний
```

**Першопричина**: CLAUDE.md розглядається як монолітний файл замість складеної конфігурації.

---

## Огляд архітектури

```
profiles/                    modules/
├── alice.yaml               ├── core-standards.md
├── bob.yaml                 ├── git-workflow.md
├── charlie.yaml             ├── typescript-rules.md
│                            ├── test-conventions.md
│                            ├── macos-paths.md
│                            ├── linux-paths.md
│                            ├── cursor-rules.md
│                            └── communication-verbose.md
│
├── skeleton/
│   └── claude-skeleton.md   ← Шаблон із плейсхолдерами {{MODULE:name}}
│
└── sync-ai-instructions.ts  ← Зчитує профіль → додає модулі → записує результат
        │
        ▼
output/
├── alice/CLAUDE.md          ← Згенерований (тільки для читання)
├── bob/CLAUDE.md
└── charlie/CLAUDE.md
```

**Потік даних**: Профіль (YAML) + Каркас (шаблон) + Модулі (фрагменти) → Збирач → Згенерований CLAUDE.md

---

## Фаза 1: Аудит вашого поточного CLAUDE.md

**Мета**: Класифікувати кожен рядок як універсальний, умовний або персональний.

```markdown
# Шаблон аудиту

## Універсальні (для всіх розробників та інструментів)
- Архітектура: гексагональна
- Тести: мають проходити перед створенням PR
- Іменування: kebab-case для назв файлів

## Умовні (залежать від інструменту або ОС)
- Cursor: використання синтаксису @filename → module: cursor-rules
- macOS шляхи: /opt/homebrew → module: macos-paths
- Linux шляхи: /usr/local → module: linux-paths

## Персональні (індивідуальні вподобання)
- Стиль: детальні пояснення (verbose) → налаштування профілю
- Мова: коментарі французькою → налаштування профілю
```

**Команда для вимірювання**:
```bash
wc -l CLAUDE.md  # Загальна кількість рядків до модульної організації
# Позначте кожен рядок як [U]ніверсальний, [C]умовний або [P]ерсональний
# Підрахуйте категорії для оцінки поділу на модулі
```

**Типовий результат**: 60% універсальних, 25% умовних, 15% персональних.

---

## Фаза 2: Вилучення модулів

**Мета**: Один `.md` файл на кожну тематичну групу.

**Рекомендована структура**:

```
modules/
├── core-standards.md         # Архітектура, іменування, шаблони (для всіх)
├── git-workflow.md           # Правила роботи з Git (для всіх)
├── typescript-rules.md       # Строгі налаштування TS (якщо TypeScript)
├── test-conventions.md       # Шаблони тестування (для всіх)
├── macos-paths.md            # macOS-специфічні шляхи (якщо macOS)
├── linux-paths.md            # Шляхи для Linux (якщо Linux)
├── cursor-rules.md           # Правила для Cursor (якщо використовується Cursor)
└── communication-verbose.md  # Детальний стиль спілкування (за бажанням)
```

**Формат модуля** (кожен модуль є окремим фрагментом Markdown):

```markdown
<!-- modules/typescript-rules.md -->
## TypeScript Rules

- Use strict mode: `"strict": true` in tsconfig
- Prefer `type` over `interface` for unions
- No `any` — use `unknown` + type guards
- Zod for runtime validation at boundaries
```

**Рекомендації**:
- Робіть модулі самодостатніми (без перехресних посилань між ними)
- Оптимальний розмір модуля — 15–50 рядків
- Називайте модулі за їхньою предметною областю, а не за аудиторією
- Один модуль = одна причина для зміни

---

## Фаза 3: Створення профілів розробників

**Мета**: Один YAML-файл для кожного розробника зі списком їхніх модулів.

```yaml
# profiles/alice.yaml
name: "Alice"
os: "macos"
tools:
  - claude-code
  - cursor
communication_style: "concise"
modules:
  core:
    - core-standards
    - git-workflow
    - typescript-rules
    - test-conventions
  conditional:
    - macos-paths          # додається автоматично, якщо os: macos
    - cursor-rules         # додається автоматично, якщо cursor у tools
preferences:
  language: "english"
```

**Правила профілю**:
- Модулі `core`: включаються для кожного розробника (стандарти команди)
- Модулі `conditional`: включаються на основі полів `os` та `tools`
- `preferences`: персональні налаштування, які підставляються у змінні шаблону (каркаса)

**Шаблон для нових членів команди**: Див. [profile-template.yaml](../../examples/team-config/profile-template.yaml)

---

## Фаза 4: Написання скрипту збирання (Assembler)

**Мета**: Скрипт, який зчитує профіль, додає модулі та генерує CLAUDE.md.

```typescript
// sync-ai-instructions.ts (спрощений варіант ~30 рядків)
import { readFileSync, writeFileSync, mkdirSync } from 'fs';
import { parse } from 'yaml';
import { join } from 'path';

const profile = parse(readFileSync(`profiles/${process.argv[2]}.yaml`, 'utf8'));
let skeleton = readFileSync('skeleton/claude-skeleton.md', 'utf8');

// Collect modules from profile
const modules = [...profile.modules.core, ...profile.modules.conditional];

// Replace each placeholder with module content
for (const mod of modules) {
  const content = readFileSync(`modules/${mod}.md`, 'utf8');
  skeleton = skeleton.replace(`{{MODULE:${mod}}}`, content);
}

// Remove unused placeholders
skeleton = skeleton.replace(/\{\{MODULE:\w+\}\}/g, '');

// Write output
const outDir = `output/${process.argv[2]}`;
mkdirSync(outDir, { recursive: true });
writeFileSync(join(outDir, 'CLAUDE.md'), skeleton);
console.log(`Generated ${outDir}/CLAUDE.md (${modules.length} modules)`);
```

**Запуск**:
```bash
npx ts-node sync-ai-instructions.ts alice   # Для одного розробника
npx ts-node sync-ai-instructions.ts --all   # Згенерувати всі профілі
npx ts-node sync-ai-instructions.ts --check # Перевірити наявність відхилень (drift)
```

Повний шаблон: [sync-script.ts](../../examples/team-config/sync-script.ts)

---

## Фаза 5: Виявлення відхилень на етапі CI (Drift Detection)

**Мета**: Виявляти випадки, коли вихідні файли не відповідають профілям/модулям.

```yaml
# .github/workflows/ai-instructions-check.yml
name: AI Instructions Drift Check
on:
  push:
    paths:
      - 'modules/**'
      - 'profiles/**'
      - 'skeleton/**'
  schedule:
    - cron: '0 9 * * 1-5'  # У робочі дні о 09:00
end:

jobs:
  check-drift:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: npx ts-node sync-ai-instructions.ts --check
      - name: Fail if drift detected
        run: |
          if git diff --quiet output/; then
            echo "No drift detected"
          else
            echo "::error::AI instructions are out of sync!"
            git diff output/
            exit 1
          fi
```

**Що виявляє перевірка**:
- Модуль було відредаговано, але збирач не запускався повторно
- Додано новий профіль, але вихідний CLAUDE.md відсутній
- Розробник вручну відредагував свій згенерований файл CLAUDE.md

**Правило**: Згенеровані файли доступні лише для читання. Усі зміни вносяться виключно через профілі або модулі з подальшим перезапуском збирача.

---

## Фаза 6: Адаптація нових розробників (Onboarding)

**Мета**: Новий розробник отримує свій CLAUDE.md менш ніж за 5 хвилин.

```bash
# 1. Клонувати репозиторій
git clone <repo>

# 2. Скопіювати шаблон профілю
cp examples/team-config/profile-template.yaml profiles/dave.yaml
# Редагування: name, os, tools, modules

# 3. Генерація
npx ts-node sync-ai-instructions.ts dave

# 4. Встановлення
cp output/dave/CLAUDE.md .claude/CLAUDE.md
```

**Нагадування про розташування CLAUDE.md**:
- На рівні проекту: `project/CLAUDE.md` (комітиться, містить стандарти команди)
- Персональні перевизначення: `.claude/CLAUDE.md` (додано в gitignore, містить індивідуальні вподобання)

---

## Усунення несправностей

| Проблема | Причина | Вирішення |
|---------|-------|-----|
| Згенерований файл занадто великий | Додано занадто багато модулів | Перевірте профіль: видаліть модулі, які рідко використовуються |
| Модуль відсутній у вихідному файлі | Помилка в плейсхолдері каркаса | Перевірте, чи відповідає `{{MODULE:name}}` назві файлу |
| Попередження про відхилення в CI | Вихідний файл не оновлено після редагування модуля | Запустіть `sync-ai-instructions.ts` та закомітьте зміни |
| У розробника А є правила, яких немає у розробника Б | Це очікувана поведінка | Перевірте правильність профілю для конкретного розробника |
| Застарілий вихідний файл після злиття | Злиття не запустило регенерацію | Запустіть збирач після злиття (додайте git hook) |

---

## Пороги масштабування

| Розмір команди | Підхід |
|-----------|----------|
| 1-2 розробники | Спільний CLAUDE.md + правила пріоритетності ([Розділ 3.4](#34-precedence-rules)) |
| 3-5 розробників, однакові інструменти | Опціонально: лише модулі, без профілів |
| 5+ розробників або різні інструменти | Профільне збирання модулів (цей робочий процес) |
| 20+ розробників | Розгляньте сервер конфігурацій CLAUDE.md + внесення змін до модулів через PR |

---

## Виміряні результати

На основі досвіду реальної команди (5 розробників, 3 інструменти, 2 ОС):

| Показник | До | Після |
|--------|--------|-------|
| Кількість рядків у CLAUDE.md | ~380 (монолітний) | ~185 (зібраний) |
| Скорочення обсягу токенів | N/A | Споживання контексту зменшено на 59% |
| Вилучено модулів | 0 | 12 |
| Час онбордингу | "скопіювати чийсь файл" | 5 хв (шаблон + генерація) |
| Випадки відхилень конфігурацій | Щотижня | 0 (виявляє CI) |

---

## Пов'язані матеріали

- [AI Design Patterns: Facade](../core/ai-design-patterns.uk.md#facade): чому файл CLAUDE.md є контекстом, який читає модель, а не примусовим facade
- [Memory Systems](../core/memory-systems.uk.md): як Claude Code завантажує й об'єднує CLAUDE.md між сесіями
- [Розділ 3.5 Team Configuration at Scale](#35-team-configuration-at-scale): огляд концепції та виміряні результати
- [Розділ 3.4 Precedence Rules](#34-precedence-rules): як саме Claude зчитує кілька файлів CLAUDE.md
- [profile-template.yaml](../../examples/team-config/profile-template.yaml): шаблон профілю
- [claude-skeleton.md](../../examples/team-config/claude-skeleton.md): шаблон каркаса
- [sync-script.ts](../../examples/team-config/sync-script.ts): повний скрипт збирача

---
**Локалізація**: [Serhii (MacPlus Software)](https://macplus-software.com)
*Остання синхронізація: Травень 2026*
