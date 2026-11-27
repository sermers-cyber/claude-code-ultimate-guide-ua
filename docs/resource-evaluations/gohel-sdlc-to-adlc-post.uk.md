# Від SDLC до ADLC (Rakesh Gohel, LinkedIn, вересень 2026)

## Метадані оцінки

| Поле | Значення |
|---|---|
| Ресурс | Допис і інфографіка в LinkedIn "The SDLC is dead. Long live the ADLC." (стабільну публічну URL-адресу не зафіксовано) |
| Автор | Rakesh Gohel |
| Опубліковано | Тиждень від 2026-09-21 |
| Оцінено | 2026-09-29 |
| Тип ресурсу | Допис у соцмережі, що підсумовує плейбук постачальника |
| Першоджерело | Anthropic, [The AI-native SDLC playbook](https://claude.com/blog/the-ai-native-sdlc-playbook), уже оцінений у [2026-08-26-anthropic-ai-native-sdlc-playbook.md](./2026-08-26-anthropic-ai-native-sdlc-playbook.uk.md) |
| Рішення | Допис не інтегрувати; внесено два виправлення на основі першоджерела, яке він підсумовує |
| Оцінка | 2/5 |

## Висновок

Допис переказує плейбук Anthropic етап за етапом (intent.md, skills, CLAUDE.md, hooks, безперервні evals, багаторівневе рев'ю, етап Maintain, що повертається до Plan) під новою назвою «ADLC». Посібник інтегрував дві прогалини, виявлені плейбуком, 2026-08-26. Допис не додає жодного механізму, вимірювання чи прикладу понад своє джерело.

Повторне читання першоджерела для перевірки допису виявило два покращення, обидва з посиланням на плейбук, а не на допис:

1. **Цикл Maintain має крок сортування людиною.** Діаграма в посібнику надсилала аномалію в продакшені одразу на схвалення продукту. Плейбук каже, що тригер викликає Claude "with no person in the invocation path", а потім "the service owner or on-call engineer triages the queue" з варіантами "Fix now, schedule, or dismiss", і лише знахідки, що стосуються продукту, передаються власникові продукту. Виправлено в `guide/diagrams/06-development-workflows.md`.
2. **Ланцюжок документів є журналом аудиту.** Плейбук: "Together, the intent, the spec, the plan, the diff and the review findings are the audit trail." Сторінка посібника про відстежуваність охоплювала лише журнал виконання (логи сесій). Додано в `guide/ops/ai-traceability.md`.

До `guide/workflows/spec-first.md` додано примітку щодо назв: плейбук вважає agentic SDLC, AI SDLC і agentic software development синонімами, а «ADLC» уже позначає інше, а саме *Agent* Development Lifecycle, який [Salesforce](https://architect.salesforce.com/docs/architect/fundamentals/guide/agent-development-lifecycle.html) та [IBM](https://www.ibm.com/think/topics/agent-development-lifecycle-adlc) використовують для створення й експлуатації агентів як продуктів.

## Відхилені твердження

| Твердження в дописі | Причина |
|---|---|
| "The SDLC is dead" | Подача як думка. Плейбук зберігає людський контроль на кожному етапі. Див. також попереднє відхилення тієї самої тези в [2026-02-26-boristane-sdlc-dead.md](./2026-02-26-boristane-sdlc-dead.uk.md) |
| "Every gate in that process existed for one reason: writing code was slow and expensive" | Не підкріплено. Контрольні точки існують також для керування ризиками, відповідності вимогам і підзвітності, а розповіді практиків у посібнику показують, що вузьким місцем стає перевірка, а не код (`guide/workflows/agentic-software-factories.md` §5) |
| "The build phase collapses to hours" | Вимірювань не наведено |
| "No human starts it" (Maintain) | Точно лише щодо виклику; пропущено крок сортування, який описує джерело |
