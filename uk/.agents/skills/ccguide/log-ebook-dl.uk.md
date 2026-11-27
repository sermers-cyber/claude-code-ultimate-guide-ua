---
description: Записати завантаження ебуку в CSV-файл обліку за скриншотом
argument-hint: "[screenshot path or description]"
---

Подивись на наданий скриншот (або на наданий контекст) і витягни:
- **date**: дата завантаження (формат YYYY-MM-DD, використай сьогоднішню, якщо її не видно)
- **prenom**: ім'я отримувача
- **email**: електронна адреса отримувача
- **ebook**: назва посібника/ебуку (наприклад, "Prompts Efficaces", "Introduction à l'IA" тощо)
- **langue**: FR або EN залежно від назви/вмісту ебуку
- **notes**: будь-який важливий контекст (залиш порожнім, якщо нічого вартого уваги немає)

Потім додай новий рядок до:
`/Users/florianbruniaux/Sites/perso/claude-code-ultimate-guide/claudedocs/ebook-downloads.csv`

Використовуй саме такий формат CSV (без лапок, якщо поле не містить коми):
```
YYYY-MM-DD,Prenom,email@example.com,Ebook Name,FR,notes
```

Після запису підтверди: "Logged: [Prenom] — [email] — [ebook] ([date])"

$ARGUMENTS
