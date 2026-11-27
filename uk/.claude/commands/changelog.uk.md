---
name: changelog
description: Переглянути останні записи CHANGELOG
argument-hint: "[count]"
---

# Перегляд CHANGELOG

Показати останні записи з CHANGELOG.md з необов'язковим обмеженням кількості.

## Використання

```
/changelog       # Show last 5 entries (default)
/changelog 10    # Show last 10 entries
/changelog all   # Show all entries
```

## Що показувати

Прочитай `CHANGELOG.md` і витягни останні N записів версій із:
- Номером версії
- Датою релізу
- Усіма розділами (Added, Changed, Fixed тощо)
- Повним вмістом кожного розділу

## Формат виводу

```
📋 Останні записи CHANGELOG

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

[... ще записи ...]

───────────────────────────────────────────────────────────
Показано 5 із N записів
Використайте /changelog 10, щоб побачити більше, або /changelog all для повної історії
```

## Реалізація

1. Прочитай CHANGELOG.md
2. Розбери записи за regex: `## \[(\d+\.\d+\.\d+)\] - (\d{4}-\d{2}-\d{2})`
3. Витягни вміст між заголовками версій
4. Обмеж до N записів (за замовчуванням 5)
5. Відформатуй із чіткими розділювачами
6. Додай підвал із загальною кількістю

## Особливі випадки

- Пропускай розділ `[Unreleased]`, якщо він є нагорі
- Коректно обробляй відсутні дати
- Зберігай markdown-форматування в описах
- Показуй ієрархію розділів (###, марковані пункти)
