---
name: park
description: Запаркувати поточну сесію для подальшого відновлення (дописати у Markdown-файл)
argument-hint: "[session description]"
---

# Парковка сесії

Зберегти інформацію про поточну сесію, щоб відновити її після перезавантаження.

## Використання

```
/park fix du bug auth JWT     # опис одразу в команді
/park                          # попросить опис
```

## Крок 1: Отримати опис

Якщо `$ARGUMENTS` не порожній → використай його як опис сесії.
Інакше → запитай:

> "Як описати цю сесію? (напр.: виправлення бага автентифікації JWT, рефакторинг сторінки цін, міграція БД)"

## Крок 2: Вибрати файл призначення

Запитай користувача, куди зберегти:

> "Файл призначення?"

Варіанти:
1. `~/Desktop/parked-sessions.md` (за замовчуванням, рекомендовано)
2. `~/.claude/parked-sessions.md` (прихований, завжди доступний)
3. Інший (довільний текст)

Якщо користувач просто натискає Enter → використай варіант 1.

## Крок 3: Визначити ID сесії

Виконай ці команди, щоб знайти поточну сесію:

```bash
# Get current directory encoded path (/ → -, prefixed with -)
PWD_ENCODED=$(pwd | sed 's|/|-|g' | sed 's|^|projects-|' | sed 's|^projects-||')
SESSIONS_FILE="$HOME/.claude/projects/-$(echo "$PWD" | sed 's|/|-|g' | sed 's|^-||')/sessions-index.json"
```

Точніше, шлях до індексу сесій Claude такий:
```
~/.claude/projects/<encoded-pwd>/sessions-index.json
```

Де `<encoded-pwd>` — шлях поточної директорії, у якому кожен `/` замінено на `-` (початковий `/` стає початком закодованого шляху, тож `/Users/flo/myproject` → `-Users-flo-myproject`).

**Щоб визначити ID сесії:**

1. Виконай: `ls -t ~/.claude/projects/ | head -5`, щоб знайти найімовірнішу папку проєкту
2. Прочитай `sessions-index.json` зі знайденої папки
3. sessions-index.json містить масив об'єктів сесій — візьми найсвіжішу (останню в масиві або з найбільшою міткою часу)
4. Витягни поле `id` сесії (формат UUID: `xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx`)

**Запасний варіант, якщо визначення не вдалося**: у виводі використай `claude --continue` замість `claude --resume <id>`.

## Крок 4: Зібрати контекст

Виконай паралельно:
```bash
pwd                         # → repo path
git branch --show-current   # → active branch (or "no git" if not a repo)
date "+%Y-%m-%d %H:%M"     # → timestamp
```

## Крок 5: Записати у файл

**Перевір, чи існує файл:**
- Якщо НЕ існує → створи його із заголовком: `# Parked Sessions\n\n`
- Якщо існує → допиши в кінець (НІКОЛИ не перезаписуй наявний вміст)

**Допиши цей Markdown-блок:**

```markdown
## <description>
- **Дата** : <YYYY-MM-DD HH:MM>
- **Репо** : <вивід pwd>
- **Гілка** : <git-гілка або "N/A">
- **Відновлення** : `cd <pwd> && claude --resume <session-id>`

---
```

Якщо ID сесії не визначено, використай:
```markdown
- **Відновлення** : `cd <pwd> && claude --continue`
```

## Крок 6: Показати підсумок

Виведи в термінал:

```
Сесію запарковано в <destination-file>

Щоб відновити:
  cd <pwd> && claude --resume <session-id>
```

Якщо раніше було запарковано кілька сесій, нагадай: "Тепер у цьому файлі N сесій. Щоб побачити всі свої сесії: cat <destination-file>"

## Обробка помилок

| Помилка | Дія |
|-------|--------|
| Не git-репозиторій | Використай `N/A` для гілки, продовжуй |
| sessions-index.json не знайдено | Використай `claude --continue` як запасний варіант |
| Немає прав на запис у файл | Спробуй `~/.claude/parked-sessions.md` як запасний варіант |
| sessions-index.json пошкоджено | Використай `claude --continue` як запасний варіант |

## Приклад виводу (успіх)

```
Сесію запарковано в ~/Desktop/parked-sessions.md

Щоб відновити:
  cd /Users/flo/Sites/perso/mon-projet && claude --resume 84287c0d-8778-4a8d-abf1-eb2807e327a8
```
