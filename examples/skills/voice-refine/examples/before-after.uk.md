---
title: "Voice Refine - приклади до/після"
description: "Реальні приклади багатослівного голосового введення, перетвореного на структуровані промпти"
tags: [reference, tts, skill]
---

# Voice refine - приклади до/після

Реальні перетворення багатослівного голосового введення на структуровані промпти.

---

## Приклад 1: компонент React-таблиці (французькою)

### До (147 слів)

> Alors euh j'aimerais que tu m'aides à faire un truc, en fait j'ai une API
> qui renvoie des données utilisateurs et je voudrais les afficher dans un
> tableau React, mais attention il faut que ça soit paginé parce que y'a
> beaucoup de données, genre des milliers d'utilisateurs, et aussi faudrait
> pouvoir trier par nom ou par date d'inscription, ah et on utilise Tailwind
> dans le projet donc faut que ça matche avec ça, et euh je sais pas si c'est
> important mais on a déjà un composant Button qu'on utilise partout donc
> faudrait l'utiliser aussi, et puis j'imagine qu'il faut un état de
> chargement aussi quand les données arrivent...

### Після (45 слів)

```markdown
## Contexte
App React + Tailwind, API users existante, composant Button réutilisable

## Objectif
Tableau utilisateurs avec pagination et tri

## Contraintes
- Pagination (milliers d'entrées)
- Tri: nom, date inscription
- Loading state
- Utiliser Button existant

## Output
Composant React + TypeScript
```

**Коефіцієнт**: стиснення в 3,3 раза

---

## Приклад 2: потік автентифікації (англійською)

### До (189 слів)

> So I've been thinking about the authentication flow and like basically
> what we need is something that handles both regular login and also
> social login with Google and maybe GitHub too, and um the thing is
> we already have some code for this but it's kind of a mess and I want
> to clean it up, so we're using Next.js 15 by the way and we have
> Prisma for the database, and I think we should use JWT tokens but
> maybe with refresh tokens too because we don't want users to have to
> log in every hour, that would be annoying, and oh we also need to
> handle the case where someone's token expires while they're in the
> middle of doing something, like filling out a form, we shouldn't just
> kick them out, and I guess we need some kind of middleware to check
> the auth status on protected routes, does that make sense?

### Після (52 слова)

```markdown
## Context
Next.js 15 + Prisma, existing auth code needs refactoring

## Objective
Implement clean auth flow with credentials + OAuth (Google, GitHub)

## Constraints
- JWT + refresh tokens
- Graceful token expiry handling (no mid-action logout)
- Middleware for protected routes
- Silent token refresh

## Output
Auth module with middleware and hooks
```

**Коефіцієнт**: стиснення в 3,6 раза

---

## Приклад 3: баг-репорт (змішана мова)

### До (112 слів)

> Hey so there's this weird bug, basically when users try to upload
> an image that's like really big, you know like over 5MB or something,
> the app just kind of hangs and then eventually it times out I think,
> and the error message isn't helpful at all it just says "something
> went wrong" which is pretty useless, so we need to fix this, probably
> add some validation before the upload starts, and show a proper
> error message if the file is too big, oh and maybe we should also
> add a progress bar so users know something is happening...

### Після (38 слів)

```markdown
## Bug
Image upload hangs/times out for files >5MB, unhelpful error message

## Fix Required
- Client-side size validation before upload
- Clear error message for oversized files
- Progress indicator during upload

## Files
Likely: upload component, API route
```

**Коефіцієнт**: стиснення в 2,9 раза

---

## Приклад 4: запит на функцію (докладний)

### До (203 слова)

> OK so product wants this new dashboard feature and basically the idea
> is that we show some key metrics at the top, like total users and
> active users and maybe revenue if we have access to that, and then
> below that there should be some charts, probably a line chart showing
> user growth over time, and maybe a bar chart for like monthly active
> users or something, and they want it to be filterable by date range,
> like last 7 days, last 30 days, last 90 days, that kind of thing,
> and oh they also mentioned wanting to export the data to CSV at some
> point but that might be phase 2, and the design team sent over some
> mockups but they're not final yet so we should probably make it
> flexible enough to change the styling later, and we're using Chart.js
> in other parts of the app so we should probably stick with that for
> consistency, and this needs to be ready for the demo next week so
> it's kind of urgent...

### Після (58 слів)

```markdown
## Context
Dashboard feature, mockups pending finalization, Chart.js already in use

## Objective
Metrics dashboard with KPIs + charts

## Requirements
- KPIs: total users, active users, revenue (if available)
- Charts: user growth (line), MAU (bar)
- Date filters: 7d, 30d, 90d
- CSV export (phase 2)

## Constraints
- Flexible styling (design WIP)
- Demo deadline: next week

## Output
Dashboard page + components
```

**Коефіцієнт**: стиснення в 3,5 раза

---

## Підсумок стиснення

| Приклад | До | Після | Коефіцієнт | Збережена інформація |
|---------|----|-------|------------|----------------------|
| React-таблиця | 147 | 45 | 3,3x | 100% |
| Потік автентифікації | 189 | 52 | 3,6x | 100% |
| Баг-репорт | 112 | 38 | 2,9x | 100% |
| Запит на функцію | 203 | 58 | 3,5x | 100% |
| **Середнє** | **163** | **48** | **3,3x** | **100%** |

---

## Виявлені патерни

### Типові фрази-паразити, що видаляються

- "basically", "like", "you know", "I mean"
- "kind of", "sort of", "I think", "I guess"
- "so yeah", "that kind of thing", "or something"
- "by the way", "oh and", "also"

### Відповідність структурі

| Мовний зворот | Структурований розділ |
|---------------|-----------------------|
| "we're using X" | Context |
| "I want to..." | Objective |
| "it needs to..." | Constraints |
| "probably should..." | Constraints (якщо технічне) |
| "deadline is..." | Constraints |
| "output should be..." | Output |
