# Перетворення контенту

Відображає технічну мову CHANGELOG на цінність для користувача в соцмережах. Застосовуйте правила з tone-guidelines.md до всіх результатів.

## Принцип перетворення

```
Technical fact (CHANGELOG) -> User benefit (social post)
```

Ніколи не вигадуйте переваг. Кожне перетворення має спиратися на конкретний рядок CHANGELOG.

## Таблиця відповідностей

### Новий контент

| Технічне (CHANGELOG) | Соцмережі (цінність для користувача) |
|---|---|
| `N new ASCII diagrams (X -> Y total)` | `Visual learner? N new diagrams for [topics]` |
| `N New Quiz Questions (X -> Y total)` | `Test your Claude Code knowledge: N new questions covering [top categories]` |
| `New [guide-name].md (N lines)` | `New guide: [topic in plain language]` |
| `New section: [Section Name] (~N lines)` | `[What you can now learn/do]: [plain description]` |
| `New workflow: [name]` | `Step-by-step: how to [action] with Claude Code` |
| `Enhanced [command/agent] (+N lines)` | `[Command] now supports [new capability]` |
| `N new entries in reference.yaml` | Пропустити (внутрішнє індексування, немає цінності для користувача) |

### Дослідження та джерела

| Технічне (CHANGELOG) | Соцмережі (цінність для користувача) |
|---|---|
| `Score: 5/5 - [Source]` | `Critical finding from [Author]: [key insight]` |
| `Score: 4/5 - [Source]` | `From [Author]'s research: [practical takeaway]` |
| `Score: 3/5 - [Source]` | `[Author] confirms: [relevant finding]` |
| `Source: [URL] ([Author], [Date])` | `Based on [Author]'s work` |
| `Competitive Analysis: N Gaps from [source]` | `N advanced patterns identified: [top 2-3 names]` |
| `Resource evaluation: [file]` | Пропустити (внутрішній процес, не для користувачів) |
| `Fact-checked: N/N claims verified` | Можна згадати як сигнал довіри: `All N claims verified` |

### Метрики зростання

| Технічне (CHANGELOG) | Соцмережі (цінність для користувача) |
|---|---|
| `Guide line count: X -> Y (+N lines)` | `+N lines of documentation added this [week/version]` |
| `X -> Y total [items]` | `Now Y [items] (was X)` |
| `+N lines: X -> Y` | `[Feature] expanded with N lines of [content type]` |

### Виправлення та зміни

| Технічне (CHANGELOG) | Соцмережі (цінність для користувача) |
|---|---|
| `Fixed [technical issue]` | `Corrected: [what users see fixed]` |
| `[File]: Updated [field] (X -> Y)` | Пропустити, якщо зміна не помітна користувачу |
| `Landing synced` | Пропустити (інфраструктура) |
| `Badge updated` | Пропустити (інфраструктура) |

### Супровід (зазвичай пропускати)

| Технічне (CHANGELOG) | Цінність для соцмереж |
|---|---|
| `README.md: Added [X] to table` | Пропустити |
| `Updated counts in [files]` | Пропустити |
| `Sync: [description]` | Пропустити |
| `reference.yaml: +N entries` | Пропустити |
| `CLAUDE.md: [update]` | Пропустити |

## Розпізнавання патернів

### Числа для акценту

Якщо запис містить числові зміни, витягніть і відформатуйте їх:

```
"30 New Quiz Questions (227 -> 257)"
-> number: 30
-> growth: "227 -> 257"
-> highlight: "30 new questions" or "now 257 questions"

"4 new ASCII diagrams (16 -> 20 total)"
-> number: 4
-> growth: "16 -> 20"
-> highlight: "4 new diagrams" or "now 20 diagrams"

"+522 lines"
-> number: 522
-> highlight: "+522 lines of new content"
```

### Названі джерела для атрибуції

Витягуйте імена авторів і правильно вказуйте авторство:

```
"Pat Cullen's Final Review Gist" -> "From Pat Cullen's production workflow"
"Addy Osmani's 80% Problem"     -> "Based on Addy Osmani's research"
"Shen & Tamkin RCT"             -> "From Shen & Tamkin's study (Anthropic)"
"claudelog.com (InventorBlack)"  -> "Identified via claudelog.com community"
"Jude Gao (Vercel)"             -> "From Vercel's benchmarks (Jude Gao)"
```

### Групування за темами

Коли кілька записів мають спільну тему, згрупуйте їх:

```
Entries about code review:
- "Multi-Agent PR Review"
- "Enhanced /review-pr command"
- "Enhanced code-reviewer agent"
-> Cluster: "Code review overhaul: multi-agent workflow, anti-hallucination rules, severity classification"

Entries about security:
- "Docker sandbox isolation"
- "Security 3-Layer Defense diagram"
- "Secret Exposure Timeline diagram"
-> Cluster: "Security focus: sandbox isolation, defense layers, incident response timeline"
```

## Подання: версія чи тиждень

### Одна версія

```
FR: "Claude Code Ultimate Guide v3.20.5"
EN: "Claude Code Ultimate Guide v3.20.5"
```

### Тиждень (кілька версій)

```
FR: "Cette semaine dans le guide (N releases)"
EN: "This week in the guide (N releases)"
```

### Тиждень (одна версія)

```
FR: "Cette semaine : guide v3.20.5"
EN: "This week: guide v3.20.5"
```
