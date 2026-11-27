---
name: "source-command-audit-prose"
description: "Додати описову прозу до «голих» розділів у whitepapers (FR + EN) за допомогою 9 паралельних агентів"
---

# source-command-audit-prose

Використовуй цей skill, коли користувач просить виконати мігровану вихідну команду `audit-prose`.

## Command Template

# Audit Prose — збагачення «голих» розділів

Додає описову прозу (2-4 речення) перед кожним «голим» розділом whitepapers.
«Голий» розділ = заголовок, одразу за яким іде таблиця, блок коду або список без вступного абзацу.

## Використання

```
/audit-prose        # Tous les WPs (00-08), FR + EN
/audit-prose 07     # WP07 seulement (FR + EN)
/audit-prose 03 07  # WP03 et WP07 seulement
```

## Визначення «голого розділу»

Розділ (`##` або `###`), за яким БЕЗПОСЕРЕДНЬО йде:
- Markdown-таблиця (`|`)
- Блок коду (` ``` `)
- Маркований (`-`) або нумерований список

Без вступного абзацу (мінімум 2 речення).

## Суворі правила (не підлягають обговоренню)

1. **НІКОЛИ** не завершуй абзац символом `:` перед маркованим списком → баг Typst, який зливає пункти списку в один рядок
2. **НЕ вигадуй** цифр, метрик чи цитат
3. **НЕ додавай** callouts (`:::`), Mermaid чи сценарії з персонами
4. **НЕ перевищуй** +15% рядків на файл
5. Версії залишаються на **3.27.6**
6. Проза EN = природна англійська, **не** дослівний переклад FR
7. Кожне додавання = **мінімум 2 речення, максимум 4 речення**

## Приклад трансформації

```
AVANT :
### Exit Codes
| Code | Signification |
|------|---------------|
| 0    | Autorisé      |

APRÈS :
### Exit Codes
Les hooks communiquent avec Codex via des codes de sortie standardisés.
C'est le mécanisme qui permet de bloquer ou autoriser une action en temps réel,
sans intervention humaine.

| Code | Signification |
|------|---------------|
| 0    | Autorisé      |
```

## Воркфлоу: 9 паралельних агентів

### Джерела контексту

- `machine-readable/reference.yaml`: зіставлення тем → рядків основного посібника
- `guide/ultimate-guide.md`: довідковий посібник (за рядками, указаними в reference.yaml)
- Знання Codex (v3.27.6, MCP, hooks, agent teams тощо)

### Зіставлення WP

| # | FR | EN | ~«Голих» розділів |
|---|----|----|-------------------|
| 00 | `whitepapers/fr/00-introduction-serie.qmd` | `whitepapers/en/00-series-introduction.qmd` | ~10 |
| 01 | `whitepapers/fr/01-prompts-efficaces.qmd` | `whitepapers/en/01-effective-prompts.qmd` | ~14 |
| 02 | `whitepapers/fr/02-personnalisation.qmd` | `whitepapers/en/02-customization.qmd` | ~18 |
| 03 | `whitepapers/fr/03-securite.qmd` | `whitepapers/en/03-security.qmd` | ~20 |
| 04 | `whitepapers/fr/04-architecture.qmd` | `whitepapers/en/04-architecture.qmd` | ~14 |
| 05 | `whitepapers/fr/05-equipe.qmd` | `whitepapers/en/05-team.qmd` | ~20 |
| 06 | `whitepapers/fr/06-privacy.qmd` | `whitepapers/en/06-privacy.qmd` | ~12 |
| 07 | `whitepapers/fr/07-guide-reference.qmd` | `whitepapers/en/07-reference-guide.qmd` | ~36 |
| 08 | `whitepapers/fr/08-agent-teams.qmd` | `whitepapers/en/08-agent-teams.qmd` | ~16 |

### Виконання

**Якщо аргумент = номер конкретного WP**: запусти 1 агента лише для цієї пари FR/EN.

**Якщо аргументу немає (або "all")**: створи команду `audit-prose-{date}` і запусти 9 агентів паралельно.

Для кожного цільового WP запусти агента з цим промптом:

```
Tu es un éditeur technique senior. Ta mission : ajouter de la PROSE DESCRIPTIVE
aux sections "bare" du whitepaper [XX - Titre].

## Définition "bare section"
Section (## ou ###) suivie DIRECTEMENT par une table, un code block, ou une
liste à puces, SANS paragraphe d'introduction (2+ phrases).

## Ce que tu fais
Pour CHAQUE bare section identifiée :
1. Ajouter 2-4 phrases AVANT le contenu structuré
2. Chaque phrase apporte une INFO NOUVELLE : le pourquoi, le quand utiliser,
   les implications, le choix de design, ou le contexte pratique
3. PAS de reformulation de ce qui suit — COMPLETER avec du contexte manquant

## Sources de contexte
- `machine-readable/reference.yaml` : mapping complet sujets → guide principal
- Ta connaissance de Codex (v3.27.6, MCP, hooks, agent teams, etc.)

## Règles strictes
- NE PAS inventer de chiffres, métriques, ou citations
- NE PAS ajouter de callouts (:::), Mermaid, ou scénarios persona
- NE JAMAIS terminer un paragraphe par ":" avant une liste à puces (bug Typst)
- NE PAS dépasser +15% de lignes
- Garder les versions à 3.27.6
- Prose EN = anglais naturel, pas traduction mot-à-mot
- Chaque ajout = minimum 2 phrases, maximum 4 phrases

## Processus
1. LIRE reference.yaml (sections pertinentes au WP)
2. LIRE le WP FR complet
3. IDENTIFIER toutes les bare sections
4. ÉDITER le fichier FR (Edit tool, section par section)
5. LIRE le WP EN complet
6. ÉDITER le fichier EN
7. VÉRIFIER : aucun paragraphe ne finit par ":" avant une liste
8. Rapporter : sections traitées, delta lignes FR/EN
```

### Очікування та звітність

Дочекайся відповідей усіх агентів. Для кожного завершеного WP виведи:

```
WP[XX] ✅ — [N] sections, +[X]% FR/EN
```

### Завершення

Коли всі агенти завершать роботу, надішли shutdown_request кожному, потім TeamDelete.

## Перевірка після збагачення

```bash
# 1. Delta lignes (max +15%)
for f in whitepapers/fr/*.qmd; do
  echo "$(wc -l < "$f") $(basename $f)"
done

# 2. Vérifier bug Typst : paragraphe finissant par ":" suivi de liste
grep -n ':$' whitepapers/fr/*.qmd whitepapers/en/*.qmd | head -20

# 3. Versions intactes
grep "^version:" whitepapers/fr/*.qmd whitepapers/en/*.qmd

# 4. Rebuild PDFs
for f in whitepapers/fr/*.qmd whitepapers/en/*.qmd; do
  quarto render "$f"
done
```

## Бюджет рядків на WP

| WP | Макс. бюджет FR | Макс. бюджет EN |
|----|-----------------|-----------------|
| 00 | +54 рядки | +54 рядки |
| 01 | +142 рядки | +142 рядки |
| 02 | +189 рядків | +189 рядків |
| 03 | +145 рядків | +145 рядків |
| 04 | +120 рядків | +120 рядків |
| 05 | +143 рядки | +143 рядки |
| 06 | +79 рядків | +79 рядків |
| 07 | +281 рядок | +281 рядок |
| 08 | +241 рядок | +241 рядок |
