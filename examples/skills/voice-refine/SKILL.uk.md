---
name: voice-refine
description: "Перетворює багатослівне голосове введення на структуровані промпти для Claude, економні щодо токенів. Використовуйте для очищення голосових нотаток, виводу диктування або транскрипцій speech-to-text, що містять слова-паразити, повтори та неструктуровані думки."
allowed-tools: Read
effort: low
---

# Skill voice refine

Перетворює багатослівне диктування голосом у потоці свідомості на структуровані,
економні щодо токенів промпти для Claude Code.

## Коли використовувати

- Введення з голосового диктування (Wispr Flow, Superwhisper, диктування macOS)
- Багатослівний текст >150 слів
- Містить слова-паразити, повтори або відступи від теми
- Природні мовні звороти, що потребують структури

## Конвеєр перетворення

```
1. DEDUPE    → Remove repetitions and filler words
2. EXTRACT   → Identify core requirements and constraints
3. STRUCTURE → Organize into standard sections
4. COMPRESS  → Reduce to ~30% of original while preserving intent
```

## Формат виводу

```markdown
## Contexte
[Project context, existing stack, relevant files]

## Objectif
[Single sentence: what needs to be built/changed]

## Contraintes
- [Constraint 1]
- [Constraint 2]
- [etc.]

## Output attendu
[Expected deliverables: files, format, tests]
```

## Прапорці

| Прапорець | Ефект |
|-----------|-------|
| `--confirm` | Показати уточнений промпт перед надсиланням Claude (за замовчуванням) |
| `--direct` | Надіслати уточнений промпт одразу без підтвердження |
| `--verbose` | Зберегти більше деталей, менше стиснення |
| `--en` | Вивід англійською (за замовчуванням: мова збігається з вхідною) |

## Приклади використання

### Базове використання

```
/voice-refine

Alors euh j'aimerais que tu m'aides à faire un truc, en fait j'ai une API
qui renvoie des données utilisateurs et je voudrais les afficher dans un
tableau React, mais attention il faut que ça soit paginé parce que y'a
beaucoup de données, genre des milliers d'utilisateurs, et aussi faudrait
pouvoir trier par nom ou par date d'inscription, ah et on utilise Tailwind
dans le projet donc faut que ça matche avec ça...
```

### З прапорцями

```
/voice-refine --direct --en

[voice input in any language → sends English prompt directly]
```

## Метрики стиснення

| Метрика | Ціль |
|---------|------|
| Зменшення токенів | 60-70% |
| Збереження інформації | >95% |
| Чіткість структури | Висока |

## Правила фільтрації

**Видаляти**: слова-паразити («euh», «um», «like», «basically»), повтори, відступи від теми, ухильні формулювання («maybe», «probably», якщо вони не суттєві), ввічливі заповнювачі («please», «could you»).

**Зберігати**: технічні вимоги, обмеження, контекст наявного коду, очікуваний формат виводу, крайні випадки, правила бізнес-логіки.

## Див. також

- `guide/ecosystem/ai-ecosystem.md` - розділ Voice-to-Text Tools
- `examples/before-after.md` - повні приклади перетворення
