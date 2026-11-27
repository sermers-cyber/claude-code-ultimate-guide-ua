---
name: "source-command-changelog"
description: "Переглянути останні записи CHANGELOG"
---

# source-command-changelog

Використовуй цей skill, коли користувач просить виконати мігровану вихідну команду `changelog`.

## Command Template

# Перегляд CHANGELOG

Показати останні записи з CHANGELOG.md з необов'язковим обмеженням кількості.

## Використання

```
/changelog       # Show last 5 entries (default)
/changelog 10    # Show last 10 entries
/changelog all   # Show all entries
```

## Що показувати

Прочитай `CHANGELOG.md` і витягни останні N записів про версії з:
- Номером версії
- Датою релізу
- Усіма розділами (Added, Changed, Fixed тощо)
- Повним вмістом кожного розділу

## Формат виводу

```
📋 Recent CHANGELOG Entries

═══════════════════════════════════════════════════════════

## [3.9.11] - 2026-01-20

### Added
- Production Safety Rules (Section 14.3)
  - Critical safety practices for production deployments
  - Rollback procedures and monitoring guidelines

### Documentation
- Enhanced deployment workflow documentation
- Added safety checklist templates

═══════════════════════════════════════════════════════════

## [3.9.10] - 2026-01-19

### Added
- DevOps & SRE Guide with FIRE Framework
  - Fault tolerance patterns
  - Incident response protocols
  - Recovery procedures
  - Escalation guidelines

### Documentation
- New Section 9.18: DevOps & SRE Practices
- 45+ operational best practices

═══════════════════════════════════════════════════════════

[... more entries ...]

───────────────────────────────────────────────────────────
Showing 5 of N total entries
Use /changelog 10 for more, or /changelog all for complete history
```

## Реалізація

1. Прочитати CHANGELOG.md
2. Розібрати записи за регулярним виразом: `## \[(\d+\.\d+\.\d+)\] - (\d{4}-\d{2}-\d{2})`
3. Витягти вміст між заголовками версій
4. Обмежити N записами (за замовчуванням 5)
5. Відформатувати з чіткими роздільниками
6. Додати підсумок із загальною кількістю

## Особлива обробка

- Пропускати розділ `[Unreleased]`, якщо він є на початку
- Коректно обробляти відсутні дати
- Зберігати markdown-форматування в описах
- Показувати ієрархію розділів (###, марковані пункти)
