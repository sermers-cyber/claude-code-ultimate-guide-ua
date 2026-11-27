# GenAI Days Nantes: звіт Емманюеля Сьяри про конференцію

Переглянуто 19 листопада 2026 року. Оцінка: **3/5**, корисні приклади з чітким авторством для наявних сторінок, без жодних тверджень про бенчмарки. Інтеграцію запросив автор цього посібника. Технічне рецензування зафіксовано окремо від схвалення публікації людиною.

## Межі джерела

Emmanuel Sciara, *Retour sur la conférence GenAI Days Nantes 2026*, датовано 19 листопада 2026 року. Звіт переказує доповіді Трістана Франсена (Pennylane), Шарлі Ідрака (Brevo), Ніколя Мартіньоля (Back Market) і Жан-Іва Сімона (Mirakl), серед інших. URL оригінальної статті не перевірено. [Програма конференції](https://genai-days-nantes.com/) називає доповідачів і теми, але не реалізації чи показники продуктивності. Для цих доповнень не перевірялися ні записи доповідей, ні слайди, ні реалізації, ні набори даних для оцінювання.

Розглядайте статтю як переказ практика з других рук. Вона обґрунтовує патерни, які варто перевірити. Вона не встановлює причинності, порівняльної точності, надійності в продакшені чи приросту продуктивності. В інтеграції пропущено показники пропускної здатності та продуктивності, умови вимірювання яких недоступні. Згадану програму чемпіонів на 40 команд збережено як організаційний контекст з авторством Мартіньоля через Сьяру.

## Рішення

| Випадок | Розміщення | Внесок і межі |
| --- | --- | --- |
| Pennylane | [Оцінювання агентів](../../guide/roles/agent-evaluation.uk.md#criterion-specific-judges-and-human-calibration) | Невеликі судді на кожен критерій, розбір розбіжностей і агрегація, придатна до дій. Без доведеної переваги над більшим суддею, без висновку, що голосування усуває спільне упередження. |
| Back Market | [Підходи до впровадження](../../guide/roles/adoption-approaches.uk.md#back-market-champions-and-role-specific-support) | Чемпіони й навчання під конкретні ролі як ситуативний приклад добровільного впровадження, без порівняння з обов'язковим розгортанням. |
| Brevo | [Робочий процес підтримки](../../guide/workflows/support-csm-agent.uk.md#brevo-explicit-procedures-before-open-ended-routing) | Явні процедури підтримки й фіксоване отримання даних, окремо від іншого проєкту інструментів, створених співробітниками. Без твердження, що MCP за своєю природою додає випадковості. |

Приклад Mirakl щодо продуктових інвестицій інтегровано в наявну двомовну організаційну чернетку портфоліо. Окрема сторінка посібника для нього не потрібна.

## Французький переклад доповнення про Pennylane

### Évaluateurs spécialisés par critère et calibration humaine

Un juge plus gros est une option. Dans « Retour sur la conférence GenAI Days Nantes 2026 », publié le 19 novembre 2026, Emmanuel Sciara rapporte le dispositif décrit par Tristan Fransen chez Pennylane : de petits évaluateurs prennent chacun un critère, comme le respect des consignes ou les signes d’insatisfaction. Le récit décrit aussi, lorsque les données manquent, un vote d’évaluateurs paramétrés différemment sur un même critère, puis une agrégation nocturne qui produit une liste de corrections. C’est un récit de praticien rapporté par un tiers, sans comparaison établissant que ces petits juges dépassent un juge plus gros.

Pour tester cette variante, conserver séparément le résultat de l’agent, sa trace d’actions, les signaux d’expérience utilisateur et le verdict du juge. Comparer un juge unique et des juges spécialisés sur les mêmes cas annotés indépendamment. Relever les fausses acceptations, les faux rejets, le coût et la latence par critère. Examiner les désaccords avec les annotations humaines avant de modifier un juge ou sa grille, puis évaluer la modification sur des cas réservés.

Une réponse copiée peut indiquer un usage et des reformulations répétées une friction. Aucun de ces signaux n’établit la justesse. Les pouces peuvent révéler des désaccords, mais leur sélection et les cas sans retour limitent la calibration. L’agrégation ne démontre ni l’indépendance des erreurs ni la disparition d’un biais partagé. Un vote sur un critère reste distinct de l’autorité d’accepter un changement ou de le publier.

Це переклад лише доданого розділу. Це не французький переклад усього розділу «Оцінювання агентів». Реєстр перекладів повного посібника не змінено, бо його відстежуване англійське джерело не змінювалося.

## Технічне рецензування

Окремий агент-технічний редактор підтвердив оцінку 3/5 для вибіркової інтеграції. Його рецензія звузила фрагмент про файл внесків Back Market до запрошення, без твердження про впровадження, і відновила у французькій статті про робочий процес явне розмежування архітектурних компромісів і рівнів можливостей. Зміни застосовано. Це було документальне рецензування, а не експеримент і не схвалення публікації людиною.
