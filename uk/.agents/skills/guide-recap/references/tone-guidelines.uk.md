# Настанови щодо тону

Правила для контенту соцмереж, згенерованого із записів CHANGELOG. Центральний принцип: **залучення через цінність, а не ажіотаж**.

## Чек-лист DO / DON'T

### DO

- Використовуй конкретні числа з CHANGELOG (`227 -> 257`, `+522 lines`, `4 new diagrams`)
- Кажи, що користувач може робити тепер (`Test your knowledge`, `New visual guide for...`)
- Став щирі запитання (`Visual learner?`, `How do you review PRs?`)
- Вказуй названі джерела (`Based on Pat Cullen's workflow`, `From Addy Osmani's research`)
- Використовуй точні дієслова дії (`added`, `integrated`, `documented`, `evaluated`)
- Посилайся на конкретні шаблони за назвою (`Permutation Frameworks`, `Split-Role Agents`)

### DON'T

- Не використовуй гучні слова: `game-changer`, `revolutionary`, `incredible`, `amazing`, `must-have`
- Не використовуй FOMO: `You're missing out`, `Don't fall behind`, `Everyone is using this`
- Не використовуй фальшиву терміновість: `Act now`, `Limited time`, `Before it's too late`
- Не використовуй клікбейтні гачки: `This ONE trick`, `You won't believe`, `Hidden feature`
- Не вигадуй метрики: `10x faster`, `saves hours`, `boosts productivity by 300%`
- Не використовуй понад 3-4 емодзі в пості LinkedIn, 2 у твіті
- Не перебільшуй обіцянки: `The only guide you'll ever need`, `Complete mastery`

## Мовні правила

### Французька (FR)

| Формат | Регістр | Приклад |
|--------|---------|---------|
| LinkedIn | Vouvoiement | `Vous utilisez Claude Code au quotidien ?` |
| Newsletter | Vouvoiement | `Vous trouverez dans cette version...` |
| Twitter/X | Tutoiement | `Tu connais les Permutation Frameworks ?` |
| Slack | Tutoiement | `Nouvelle version dispo, check ca` |

### Англійська (EN)

- Пряме звертання (`you`) у всіх форматах
- Американський правопис (`optimize`, `analyze`, а не `optimise`, `analyse`)
- Жодних британських ідіом чи написань

## Бюджет емодзі

| Формат | Макс. емодзі | Розміщення |
|--------|--------------|------------|
| LinkedIn | 3-4 | Рядок-гачок (0-1), пункти (по 1, макс. 3), CTA (0-1) |
| Twitter | 2 | Гачок (1), ключова теза (1) |
| Newsletter | 2-3 | Лише в заголовках розділів |
| Slack | 4-6 | Маркери статусу, акценти |

Дозволені емодзі: `+`, `->`, перевага технічним символам над декоративними.
Уникай: fire, rocket, explosion, 100, mind-blown (маркетингові кліше).

## Правила CTA

| Формат | Стиль CTA | Ціль посилання |
|--------|-----------|----------------|
| LinkedIn | М'яке запитання або твердження про цінність | URL сайту лендингу |
| Twitter | Коротка дія або посилання | Репозиторій GitHub |
| Newsletter | Явне посилання з контекстом | URL сайту лендингу |
| Slack | Пряме посилання | Репозиторій GitHub |

Жодних шаблонів `Click here`, `Check this out`, `Link in bio`.

## Чек-лист якості (перед виводом)

Перед виведенням будь-якого контенту для соцмереж перевір:

1. [ ] Кожне число походить із реального запису CHANGELOG
2. [ ] Немає гучних слів (звір зі списком DON'T)
3. [ ] Кількість емодзі в межах бюджету
4. [ ] Регістр FR відповідає формату (vous/tu)
5. [ ] EN використовує американське написання
6. [ ] CTA веде на правильну ціль
7. [ ] Названі джерела вказано, коли їх використано
8. [ ] Немає вигаданих метрик чи відсотків
