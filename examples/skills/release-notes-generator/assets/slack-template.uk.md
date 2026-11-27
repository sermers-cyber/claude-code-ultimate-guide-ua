# Шаблон оголошення в Slack

Використовуйте цей шаблон для генерації продуктово-орієнтованих повідомлень у Slack.

```
Version X.Y.Z - Deployed to production

PR : [Release PR URL, e.g.: https://github.com/{owner}/{repo}/pull/XXX]

In brief : [Sentence describing the main objective of this release]

---

New Features

[Feature Name 1]
> [1-2 sentence description of user impact]
> Who is affected: [End-users / Admins / All]

[Feature Name 2]
> [1-2 sentence description]
> Who is affected: [Roles]

---

Important Fixes

- [Bug fix described in user-friendly language]
- [Bug fix described in user-friendly language]

---

Improvements

- [UX/UI or workflow improvement in user language]
- [...]

---

By the numbers

- X new features
- Y bugs fixed
- Z improvements

---

Questions? Contact @[team-lead] or the dev team
```

## Рекомендації

### РОБІТЬ
- Використовуйте доступну мову (без технічного жаргону)
- Фокусуйтеся на впливі на користувача
- Будьте стислі (максимум 10 рядків на розділ)
- Використовуйте емодзі помірно

### УНИКАЙТЕ
- "Implementation of the DataLoader pattern to solve N+1 queries"
- "Complete refactoring of the permissions system with scope ANY/ASSIGNED"
- "Migration from webpack to Turbopack"

### Перетворення технічного на продуктове

| Технічне | Продуктове |
|----------|------------|
| N+1 query optimization with DataLoader | Faster loading of user and feature lists |
| AI embeddings implementation with pgvector | New intelligent search for similar items |
| Fix scope permissions in getPermissionScope() | Fixed a bug preventing some users from accessing their data |
| Migration to kebab-case for files | *Не повідомляти (суто технічне)* |
| Fix DB connection with retry logic | Better database connection stability |
| Add error monitoring for orphan records | Automatic detection of orphan records |

### Необов'язкові розділи

Якщо реліз містить важливі пункти, додайте:

Heads up
- [Important information users should know]
- [Behavior changes they might notice]

Coming soon
- [Teaser for the next big feature]
- [Feature in development coming soon]
