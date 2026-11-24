# Візуальні промпти про ШІ-підписки та інференс

Ці промпти охоплюють стратегію підписок на кількох провайдерів, шляхи розгортання Mistral, видимість шлюзу та вибір агентних інструментів. Згенеруйте одне зображення на промпт. Перед публікацією перевірте кожен відтворений підпис, змініть розмір вибраного джерела до 1600 x 900 і конвертуйте у WebP.

## Запис вибору

| Опублікований ресурс | Джерело Gemini | Статус |
|---|---|---|
| `subscription-provider-portfolio.webp` | `Gemini_Generated_Image_m1miyom1miyom1mi.jpeg` | Вибрано й опубліковано |
| `mistral-deployment-paths.webp` | `Gemini_Generated_Image_xxlnb4xxlnb4xxln.jpeg` | Вибрано й опубліковано |
| `gateway-visibility-boundary.webp` | `Gemini_Generated_Image_x9ycs7x9ycs7x9yc.jpeg` | Вибрано й опубліковано |
| `agentic-tool-selection-map.webp` | `Gemini_Generated_Image_sfqljesfqljesfql.jpeg` | Відхилено: незапитаний надзаголовок з помилкою у `EDITORIAL` — `EDTORIAL` |

## Спільний арт-напрям

Використовуйте теплий кремовий фон у стилі міліметрівки (`#f5f1e8`), ледь помітну сітку (`#d4cfb8`), точні темні лінії чорнила (`#1a1a1a`) і стримані акценти: помаранчевий (`#d97706`), зелений (`#16a34a`) та жовтий (`#fbbf24`). Червоний залишайте для невдалих контрольних гейтів. Не використовуйте фото, 3D, маскотів, декоративні дудли, логотипи компаній, номери сторінок чи зайвий надзаголовок. Весь видимий текст англійською. Не використовуйте довгі тире. Цільовий розмір 1600 x 900 пікселів.

## 1. Портфель провайдерів для 300 інженерів

Вивід: `guide/images/subscription-provider-portfolio.webp`

Alt-текст: Організація зі 300 інженерів, розділена на керовані інтерактивні підписки для працівників, кероване сервісне автоматизування та приватний інференс, кожне з окремими мірами вартості та приймання.

```text
Create a clean editorial infographic for a technical documentation guide, landscape 16:9 at 1600x900. Use the shared warm cream graph-paper art direction. No photos, no 3D, no mascots, no decorative doodles, no company logos, no page number, and no pretitle. All visible text must be exactly in English and spelled correctly. Do not use em dashes.

Headline: “ONE FLEET, THREE CONTROL PLANES”

At the top center, show one group labeled “300 ENGINEERS”. Split it into three clearly separated paths.

Path 1: “INTERACTIVE WORKFORCE”. Subtitle: “Managed user identities”. Show six compact labels: “Claude”, “Codex”, “Copilot”, “Gemini”, “Cursor”, “Mistral Vibe”. Below them show “Active users”, “Accepted tasks”, and “Seat and overage cost”.

Path 2: “AUTOMATION”. Subtitle: “Service identities through a gateway”. Show “CI”, “Shared agents”, and “Scheduled workflows” connected to one box titled “Gateway”. Inside it show “Budgets”, “Attribution”, “Routing”, and “Fallback”.

Path 3: “SENSITIVE WORKLOADS”. Subtitle: “Private or self-hosted inference”. Show one “Private inference cluster” with “Quality gate”, “Latency gate”, “Capacity gate”, and “Loaded cost”.

Footer: “ASSIGN BY POPULATION. MEASURE ACCEPTED OUTCOMES.”

Make the three control planes unmistakably different. Do not imply that one provider should serve every workload.
```

## 2. Шляхи розгортання Mistral

Вивід: `guide/images/mistral-deployment-paths.webp`

Alt-текст: Mistral Vibe, API Devstral і Devstral з відкритими вагами порівняно як шляхи керованого робочого середовища для співробітників, сервісу з обліком за використанням та приватного інференсу за спільними гейтами якості, суверенності, паралельності, затримки та повної вартості.

```text
Create a clean technical decision infographic, landscape 16:9 at 1600x900. Use the shared warm cream graph-paper art direction. No photos, no 3D, no mascots, no logos, no page number, and no pretitle. All visible text must be exactly in English and spelled correctly. Do not use em dashes.

Headline: “THREE MISTRAL PATHS, THREE OPERATING MODELS”

Create three large vertical lanes.

Lane 1: “MISTRAL VIBE”. Subtitle: “Managed workforce”. Show “User seats”, “Organization controls”, “Included usage + PAYG”, and “Managed operations”.

Lane 2: “DEVSTRAL API”. Subtitle: “Metered service”. Show “Service identity”, “Token usage”, “Gateway budgets”, and “Provider operations”.

Lane 3: “OPEN-WEIGHT DEVSTRAL”. Subtitle: “Private inference”. Show “GPU capacity”, “Queue depth”, “TTFT + TPOT”, “Availability”, and “Operator time”.

Under the lanes, create five connected decision gates: “TASK QUALITY” → “DATA BOUNDARY” → “CONCURRENCY” → “LATENCY” → “LOADED COST”. End with three result cards: “Choose managed”, “Choose API”, and “Choose private”.

Red rejection note: “Hardware fit is not production capacity.”

Footer: “Provider nationality does not prove workload sovereignty.”
```

## 3. Межа видимості шлюзу

Вивід: `guide/images/gateway-visibility-boundary.webp`

Alt-текст: Підписки користувачів обходять бюджети та атрибуцію шлюзу, тоді як CI, спільні агенти, заплановані робочі процеси та внутрішні сервіси проходять через централізовані ключі, квоти, allowlist моделей, fallback і спостережуваність.

```text
Create a clean editorial architecture infographic, landscape 16:9 at 1600x900. Use the shared warm cream graph-paper art direction. No photos, no 3D, no mascots, no logos, no page number, and no pretitle. All visible text must be exactly in English and spelled correctly. Do not use em dashes.

Headline: “A GATEWAY SEES ONLY ROUTED TRAFFIC”

Build two horizontal traffic paths.

Top path in red: “USER SUBSCRIPTIONS”. Show “Claude”, “Codex”, “Cursor”, and “Mistral Vibe” connected directly to external provider boxes. Add “Outside gateway budgets”, “Outside gateway attribution”, and “Separate audit boundary”.

Bottom path in green: “GOVERNED SERVICE TRAFFIC”. Show “CI”, “Shared agents”, “Scheduled workflows”, and “Internal services” routed through one central box labeled “AI GATEWAY”. Inside it show “Central keys”, “Budgets”, “Quotas”, “Cost attribution”, “Model allowlist”, and “Fallback”. Connect the gateway to “Provider A”, “Provider B”, and “Private model”.

Add an orange observability panel containing “Logs”, “Latency”, “Errors”, and “Token usage”.

Footer: “CENTRALIZED CONTROL REQUIRES CENTRALIZED TRAFFIC.”
```

## 4. Карта вибору агентних інструментів

Запланований вивід: `guide/images/agentic-tool-selection-map.webp`

Статус: не опубліковано. Згенеруйте заново з цього чистого промпту, бо перший вивід додав надзаголовок із помилкою.

```text
Create a clean editorial selection infographic for an AI coding tools guide, landscape 16:9 at 1600x900. Use the shared warm cream graph-paper art direction. No photos, no 3D, no mascots, no company logos, no page number, and no pretitle above the headline. All visible text must be exactly in English and spelled correctly. Do not use em dashes.

Headline: “CHOOSE THE JOB BEFORE THE TOOL”

Create four large job cards connected to four tool categories.

1. “INTERACTIVE REPOSITORY WORK” connects to “Coding agent”, with “Claude Code, Codex, Gemini CLI”.
2. “IDE-CENTERED DEVELOPMENT” connects to “AI-native editor or extension”, with “Cursor, Copilot”.
3. “CI AND SHARED AUTOMATION” connects to “Agent runtime + governed API”, with “Service identity”, “Budget”, “Retry policy”, and “Audit trail”.
4. “PRIVATE INFERENCE” connects to “Open-weight model + serving engine”, with “Task quality”, “Concurrency”, “Latency”, and “Operations”.

Below the cards, add one measurement strip: “ACCEPTED TASKS”, “TOTAL WORKFLOW COST”, “REVIEW TIME”, and “FAILURES + RETRIES”.

Red warning: “Mismatch: Do not compare a seat, a gateway, a model, and a runtime as equivalent products.”

Footer: “THE RIGHT CATEGORY COMES BEFORE THE PROVIDER.”
```

## Запис верифікації

| Ресурс | Розміри | Результат QA |
|---|---:|---|
| `subscription-provider-portfolio.webp` | 1600 x 900 | Текст і макет перевірено після конвертації |
| `mistral-deployment-paths.webp` | 1600 x 900 | Текст і макет перевірено після конвертації |
| `gateway-visibility-boundary.webp` | 1600 x 900 | Текст і макет перевірено після конвертації |
| `agentic-tool-selection-map.webp` | Не опубліковано | Джерело відхилено через надзаголовок із помилкою |
