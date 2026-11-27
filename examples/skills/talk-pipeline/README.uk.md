# Skills конвеєра доповіді

Конвеєр skills із 6 етапів, що перетворює сирий матеріал (статтю, транскрипт, нотатки) на готову конференційну доповідь зі слайдами, згенерованими ШІ.

## Встановлення

Скопіюйте каталог `talk-pipeline/` у папку `.claude/skills/` свого проєкту:

```bash
cp -r examples/skills/talk-pipeline ~/.claude/skills/
```

Або встановіть лише потрібні етапи (кожен етап незалежний).

## Етапи

| Етап | Файл skill | Режим | Опис |
|------|-----------|-------|------|
| 1 | `stage-1-extract/SKILL.md` | REX + Concept | Витяг вихідного матеріалу в структурований підсумок |
| 2 | `stage-2-research/SKILL.md` | лише REX | Git-археологія + хронологія |
| 3 | `stage-3-concepts/SKILL.md` | REX + Concept | Каталог концепцій з оцінками |
| 4 | `stage-4-position/SKILL.md` | REX + Concept | Ракурси, назви, описи + CHECKPOINT |
| 5 | `stage-5-script/SKILL.md` | REX + Concept | Пітч у 5 діях + специфікація слайдів + промпт для Kimi |
| 6 | `stage-6-revision/SKILL.md` | REX + Concept | Аркуші повторення + шпаргалка Q&A |
| — | `orchestrator/SKILL.md` | REX + Concept | Запуск повного конвеєра одним викликом |

## Швидкий старт

**Повний конвеєр (рекомендовано)**:
```
/talk-pipeline
```
Оркестратор запитує метадані й запускає всі застосовні етапи.

**Окремий етап**:
```
/talk-stage1-extract
/talk-stage4-position
```

**З прапорцями**:
```
/talk-pipeline --rex --slug=my-talk --event="Conf 2026" --duration=30
/talk-pipeline --concept --slug=my-idea
```

## Угода про вивід

Усі файли потрапляють у `talks/` у корені проєкту:
```
talks/{YYYY}-{slug}-summary.md
talks/{YYYY}-{slug}-git-archaeology.md
talks/{YYYY}-{slug}-concepts.md
talks/{YYYY}-{slug}-angles.md
talks/{YYYY}-{slug}-pitch.md
talks/{YYYY}-{slug}-kimi-prompt.md
...
```

## Використання промпту для Kimi

Етап 5 генерує `{slug}-kimi-prompt.md`. Щоб згенерувати слайди:
1. Відкрийте файл і переконайтеся, що не залишилося жодного `{PLACEHOLDER}`
2. Перейдіть на [kimi.com](https://kimi.com) (безкоштовно, API не потрібен)
3. Скопіюйте й вставте весь промпт
4. Kimi згенерує презентацію в темній темі з вашим вмістом слайдів

## Документація

Повний посібник із воркфлоу: [guide/workflows/talk-pipeline.md](../../../guide/workflows/talk-pipeline.uk.md)
