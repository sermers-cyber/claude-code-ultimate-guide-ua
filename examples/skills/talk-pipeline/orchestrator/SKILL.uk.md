---
name: talk-pipeline
description: "Оркеструє повний конвеєр підготовки доповіді від сирого матеріалу до аркушів повторення, виконуючи 6 етапів послідовно з контрольними точками за участі людини для доповідей у режимі REX або Concept. Використовуйте, коли починаєте новий конвеєр доповіді, відновлюєте конвеєр із певного етапу або запускаєте повний наскрізний процес підготовки."
allowed-tools: Write Read AskUserQuestion Task
effort: high
---

# Оркестратор конвеєра доповіді

Оркеструє повний конвеєр підготовки доповіді від сирого матеріалу до аркушів повторення. Може запускати повний конвеєр або один ізольований етап.

## Режими

- `--rex`: доповідь REX із доказами з git/коду (changelog, коміти, виміряні метрики)
- `--concept`: концептуальна доповідь зі статті, ідей, нотаток (пропускає етап 2)

## Використання

```
/talk-pipeline                          # full pipeline, asks for context
/talk-pipeline --stage=extract          # run a single isolated stage
/talk-pipeline --rex                    # REX mode (git archaeology included)
/talk-pipeline --concept                # Concept mode (skip research)
/talk-pipeline --rex --slug=my-talk --event="Conf 2026" --date=2026-06-15 --duration=30
```

## Збір контексту

Якщо не надано, запитайте через AskUserQuestion:

```
- slug         : kebab-case identifier (e.g., my-talk-topic)
- event        : event name (e.g., Conf 2026, Tech Meetup)
- date         : talk date (YYYY-MM-DD)
- duration     : duration in minutes (e.g., 30)
- audience     : audience profile (e.g., senior devs, tech leads, non-tech)
- type         : --rex or --concept
- source_path  : path to source material (article .mdx, transcript .md, notes)
- repo_path    : (REX only) path to git repository for archaeology
```

## Робочий процес

1. **Зберіть контекст** через AskUserQuestion для обов'язкових метаданих
2. **Маршрутизація за режимом** (`--rex` чи `--concept`, пропустіть етап 2 для concept)
3. **Запустіть етап 1** (`/talk-stage1-extract`, завжди першим)
4. **Запустіть етапи 2-4 паралельно** (після підтвердження етапу 1)
   - REX: extract -> research + concepts + position (паралельно)
   - Concept: extract -> concepts + position (паралельно, без research)
5. **CHECKPOINT**: дочекайтеся вибору ракурсу й назви (вивід етапу 4)
6. **Запустіть етап 5** (`/talk-stage5-script` із підтвердженим вибором)
7. **Запустіть етап 6** (`/talk-stage6-revision`)
8. **Фінальний підсумок**: перелічіть усі згенеровані файли з їхніми шляхами

## Граф залежностей

```
         extract (Stage 1)
               |
    +----------+-----------+
    v          v           v
research    concepts   position
(Stage 2)   (Stage 3)  (Stage 4)
[--rex only]            [CHECKPOINT]
    |          |           |
    +----------+-----------+
               v
          script (Stage 5)
               |
               v
         revision (Stage 6)
```

## Маршрутизація етапів (--stage=X)

Якщо вказано `--stage`, запускайте лише відповідний skill:

| Етап | Skill для виклику |
|------|-------------------|
| extract | /talk-stage1-extract |
| research | /talk-stage2-research |
| concepts | /talk-stage3-concepts |
| position | /talk-stage4-position |
| script | /talk-stage5-script |
| revision | /talk-stage6-revision |

## Угода про іменування виводу

```
talks/{YYYY}-{slug}-summary.md           # extract
talks/{YYYY}-{slug}-git-archaeology.md   # research
talks/{YYYY}-{slug}-changelog-analysis.md
talks/{YYYY}-{slug}-timeline.md
talks/{YYYY}-{slug}-concepts.md          # concepts
talks/{YYYY}-{slug}-concepts-enriched.md
talks/{YYYY}-{slug}-angles.md            # position
talks/{YYYY}-{slug}-titre.md
talks/{YYYY}-{slug}-descriptions.md
talks/{YYYY}-{slug}-feedback-draft.md
talks/{YYYY}-{slug}-pitch.md             # script
talks/{YYYY}-{slug}-slides.md
talks/{YYYY}-{slug}-kimi-prompt.md
talks/{YYYY}-{slug}-revision-sheets.md   # revision
```

## Формат фінального підсумку

Після завершення етапу 6 покажіть:

```
Pipeline complete. Files generated:

Stage 1: Extract
  v talks/{YYYY}-{slug}-summary.md

Stage 2: Research (REX only)
  v talks/{YYYY}-{slug}-git-archaeology.md
  v talks/{YYYY}-{slug}-changelog-analysis.md
  v talks/{YYYY}-{slug}-timeline.md

Stage 3: Concepts
  v talks/{YYYY}-{slug}-concepts.md
  v talks/{YYYY}-{slug}-concepts-enriched.md (if repo available)

Stage 4: Position
  v talks/{YYYY}-{slug}-angles.md
  v talks/{YYYY}-{slug}-titre.md
  v talks/{YYYY}-{slug}-descriptions.md
  v talks/{YYYY}-{slug}-feedback-draft.md

Stage 5: Script
  v talks/{YYYY}-{slug}-pitch.md
  v talks/{YYYY}-{slug}-slides.md
  v talks/{YYYY}-{slug}-kimi-prompt.md   <- copy-paste into kimi.com

Stage 6: Revision
  v talks/{YYYY}-{slug}-revision-sheets.md

Next step: open kimi-prompt.md, verify no {PLACEHOLDER} remains, paste into kimi.com.
```

## Антипатерни

- Не запускайте етап 5 без явного вибору ракурсу й назви від користувача
- Не запускайте етап 2 (research) у режимі `--concept`
- Не переходьте до наступного етапу, якщо попередній зазнав невдачі
- Не вигадуйте метрик чи дат, яких немає у вихідному матеріалі

## Валідація

- [ ] Усі файли попередніх етапів існують до запуску наступного
- [ ] CHECKPOINT етапу 4 дотримано перед script
- [ ] Виводи названо за угодою `talks/{YYYY}-{slug}-{stage}.md`
- [ ] У згенерованих файлах немає порожніх плейсхолдерів

## Поради

- Оркестратор є рекомендованою точкою входу для першого використання
- Для тих, хто вже знає конвеєр, швидше запускати окремі skills етапів
- Прапорець `--stage=X` корисний для повторного запуску одного етапу без повторного проходження всього конвеєра

## Пов'язане

- [Етап 1: Extract](../stage-1-extract/SKILL.uk.md)
- [Етап 2: Research](../stage-2-research/SKILL.uk.md)
- [Етап 3: Concepts](../stage-3-concepts/SKILL.uk.md)
- [Етап 4: Position](../stage-4-position/SKILL.uk.md)
- [Етап 5: Script](../stage-5-script/SKILL.uk.md)
- [Етап 6: Revision](../stage-6-revision/SKILL.uk.md)
- [Повний посібник із воркфлоу](../../../../guide/workflows/talk-pipeline.uk.md)
