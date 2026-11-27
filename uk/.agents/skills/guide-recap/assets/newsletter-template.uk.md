# Шаблон розсилки

Ціль: ~500 слів. Структуровані розділи з глибиною.

## Шаблон FR

```markdown
# {title_fr}

{intro_paragraph_fr}

## Ce qui a change

{highlights_section_fr}

## En detail

{detail_section_fr}

## A retenir

{takeaway_fr}

---

[Guide complet]({landing_url}) | [GitHub]({github_url})
```

## Шаблон EN

```markdown
# {title_en}

{intro_paragraph_en}

## What changed

{highlights_section_en}

## In detail

{detail_section_en}

## Key takeaway

{takeaway_en}

---

[Full guide]({landing_url}) | [GitHub]({github_url})
```

## Правила полів

### title (макс. 80 символів)

Подання через версію або тиждень, описове.

```
FR: "Guide v3.20.5 : Reference visuelle enrichie"
EN: "Guide v3.20.5: Enhanced Visual Reference"

FR: "Semaine du 27 janvier : 4 releases, 9 patterns avances"
EN: "Week of January 27: 4 releases, 9 advanced patterns"
```

### intro_paragraph (2-3 речення, макс. 150 слів)

Що сталося і чому це важливо. Без гучних слів.

```
FR: "La version 3.20.5 du Claude Code Ultimate Guide ajoute 4 nouveaux
diagrammes ASCII a la reference visuelle. Le guide contient maintenant
20 diagrammes couvrant TDD, securite et workflows d'apprentissage."

EN: "Version 3.20.5 of the Claude Code Ultimate Guide adds 4 new ASCII
diagrams to the visual reference. The guide now contains 20 diagrams
covering TDD, security, and learning workflows."
```

### highlights_section (маркований список, 3-5 пунктів)

Записи з найвищими оцінками, перетворені. Кожен пункт: щонайбільше 1-2 речення.

```
FR:
- **Cycle TDD Red-Green-Refactor** : Diagramme du flux iteratif test-code-refactor
- **Protocole UVAL** : Visualisation du framework Comprendre-Verifier-Appliquer-Apprendre
- **Defense securite 3 couches** : Prevention, detection, reponse avec guide d'adoption
- **Timeline d'exposition de secrets** : Actions d'urgence par fenetre temporelle (15min/1h/24h)

EN:
- **TDD Red-Green-Refactor Cycle**: Diagram of the iterative test-code-refactor flow
- **UVAL Protocol Flow**: Visualization of the Understand-Verify-Apply-Learn framework
- **Security 3-Layer Defense**: Prevention, detection, response with adoption guide
- **Secret Exposure Timeline**: Emergency actions by time window (15min/1h/24h)
```

### detail_section (1-2 абзаци, макс. 200 слів)

Розгорни найцікавішу головну подію. Дай контекст, поясни, що отримує користувач.
Вказуй джерела, якщо застосовно.

### takeaway (1-2 речення)

Одна практична думка або підсумок.

```
FR: "Si vous apprenez mieux en visuel, les 20 diagrammes du guide couvrent
maintenant les workflows les plus frequents, de TDD a la gestion d'incidents."

EN: "If you're a visual learner, the guide's 20 diagrams now cover the most
common workflows, from TDD to incident management."
```

## Обмеження

- Усього: 400-600 слів
- Бюджет емодзі: 2-3 (лише в заголовках розділів)
- Без гучних слів
- FR: звертання на "vous"
- EN: американська англійська
- Обидва посилання (лендинг + GitHub) у футері
- Вказуй усі названі джерела
