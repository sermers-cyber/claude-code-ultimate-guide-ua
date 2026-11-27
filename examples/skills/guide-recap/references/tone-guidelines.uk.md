# Настанови щодо тону

Правила для контенту соцмереж, згенерованого із записів CHANGELOG. Центральний принцип: **залучення через цінність, а не через гіпе**.

## Чекліст DO / DON'T

### DO

- Використовуйте конкретні числа з CHANGELOG (`227 -> 257`, `+522 lines`, `4 new diagrams`)
- Кажіть, що користувач може робити тепер (`Test your knowledge`, `New visual guide for...`)
- Ставте щирі запитання (`Visual learner?`, `How do you review PRs?`)
- Вказуйте названі джерела (`Based on Pat Cullen's workflow`, `From Addy Osmani's research`)
- Використовуйте точні дієслова дії (`added`, `integrated`, `documented`, `evaluated`)
- Посилайтеся на конкретні патерни за назвою (`Permutation Frameworks`, `Split-Role Agents`)

### DON'T

- Не вживайте гіпе-слова: `game-changer`, `revolutionary`, `incredible`, `amazing`, `must-have`
- Не використовуйте FOMO: `You're missing out`, `Don't fall behind`, `Everyone is using this`
- Не створюйте фальшиву терміновість: `Act now`, `Limited time`, `Before it's too late`
- Не використовуйте клікбейтні гачки: `This ONE trick`, `You won't believe`, `Hidden feature`
- Не вигадуйте метрики: `10x faster`, `saves hours`, `boosts productivity by 300%`
- Не використовуйте понад 3-4 емодзі в дописі LinkedIn і 2 у твіті
- Не обіцяйте зайвого: `The only guide you'll ever need`, `Complete mastery`

## Мовні правила

### Французька (FR)

| Формат | Регістр | Приклад |
|--------|----------|---------|
| LinkedIn | Vouvoiement | `Vous utilisez Claude Code au quotidien ?` |
| Розсилка | Vouvoiement | `Vous trouverez dans cette version...` |
| Twitter/X | Tutoiement | `Tu connais les Permutation Frameworks ?` |
| Slack | Tutoiement | `Nouvelle version dispo, check ca` |

### Англійська (EN)

- Пряме звертання (`you`) в усіх форматах
- Американське написання (`optimize`, `analyze`, а не `optimise`, `analyse`)
- Без британських ідіом чи написання

## Бюджет емодзі

| Формат | Макс. емодзі | Розміщення |
|--------|-----------|-----------|
| LinkedIn | 3-4 | Гачок (0-1), маркери (по 1, макс. 3), CTA (0-1) |
| Twitter | 2 | Гачок (1), ключова думка (1) |
| Розсилка | 2-3 | Лише в заголовках розділів |
| Slack | 4-6 | Маркери статусу, акцентування |

Дозволені емодзі: `+`, `->`, технічні символи краще за декоративні.
Уникайте: вогонь, ракета, вибух, 100, «вибух мозку» (маркетингові штампи).

## Правила CTA

| Формат | Стиль CTA | Ціль посилання |
|--------|-----------|-------------|
| LinkedIn | М'яке запитання або ствердження цінності | URL сайту-лендингу |
| Twitter | Коротка дія або посилання | Репозиторій GitHub |
| Розсилка | Явне посилання з контекстом | URL сайту-лендингу |
| Slack | Пряме посилання | Репозиторій GitHub |

Жодних патернів `Click here`, `Check this out`, `Link in bio`.

## Чекліст якості (перед виводом)

Перед виводом будь-якого контенту для соцмереж перевірте:

1. [ ] Кожне число походить із реального запису CHANGELOG
2. [ ] Немає гіпе-слів (звірте зі списком DON'T через grep)
3. [ ] Кількість емодзі в межах бюджету
4. [ ] Регістр FR відповідає формату (vous/tu)
5. [ ] EN використовує американське написання
6. [ ] CTA веде на правильну ціль
7. [ ] Названі джерела вказано, коли вони використані
8. [ ] Немає вигаданих метрик чи відсотків
