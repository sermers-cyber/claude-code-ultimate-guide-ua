---
title: "reMarkable 2 + AI: хаки, інструменти та воркфлоу"
description: "Повна карта інтеграцій ШІ для reMarkable 2 — сервер MCP, OCR, пайплайни Obsidian/Notion та автоматизації"
tags: [mcp, integration, hardware, workflow, remarkable]
---

# reMarkable 2 + AI: Повна карта хаків, інструментів та воркфлоу

**Останнє підтвердження**: Лютий 2026

reMarkable 2 — це e-ink планшет на базі Linux із повним рут-доступом (full-root-access). Його філософія відсутності відволікань робить його чудовим інструментом для мислення, але його нативні інтеграції є мінімалістичними. Ця сторінка охоплює все, що існує для його підсилення за допомогою ШІ — від найпростішого до високотехнологічного.

## Зміст

1. [remarkable-mcp: Зміна правил гри (game-changer)](#1-remarkable-mcp-зміна-правил-гри-game-changer)
2. [Ghostwriter: Інтерфейс Vision-LLM](#2-ghostwriter-інтерфейс-vision-llm)
3. [Синхронізація reMarkable → Obsidian](#3-синхронізація-remarkable-obsidian)
4. [Кастомний пайплайн OCR + ШІ](#4-кастомний-пайплайн-ocr-шї)
5. [Доступ по SSH та інструменти спільноти](#5-доступ-по-ssh-та-інструменти-спільноти)
6. [Недостатньо використані нативні функції](#6-недостатньо-використані-нативні-функції)
7. [Офіційний API та портал для розробників](#7-офіційний-api-та-портал-для-розробників)
8. [Автоматизація через Zapier](#8-автоматизація-через-zapier)
9. [Read-it-later: Веб → reMarkable](#9-read-it-later-веб-remarkable)
10. [Нотатки із зустрічей → Самарі за допомогою ШІ](#10-нотатки-із-зустрічей-самарі-за-допомогою-шї)
11. [Zotero → reMarkable (дослідження)](#11-zotero-remarkable-дослідження)
12. [Показ екрана як дошка з підтримкою ШІ](#12-показ-екрана-як-дошка-з-підтримкою-шї)
13. [Кастомні застосунки та цікаві хаки](#13-кастомні-застосунки-та-цікаві-хаки)
14. [ШІ-посилені воркфлоу для самостійної розробки](#14-шї-посилені-воркфлоу-для-самостійної-розробки)
15. [З чого почати](#15-з-чого-почати)

---

## 1. remarkable-mcp: Зміна правил гри (game-changer)

**ROI: максимальний | Зусилля: середні | Підключення: SSH over USB (без хмари)**

Сем Морроу (Sam Morrow) створив **сервер MCP**, який безпосередньо з'єднує reMarkable з Claude Code, VS Code Copilot та будь-яким ШІ-асистентом, сумісним із MCP.

| Атрибут | Деталі |
|---------|--------|
| **Репозиторій** | https://github.com/SamMorrowDrums/remarkable-mcp |
| **Блог** | https://sam-morrow.com/blog/building-an-mcp-server-for-remarkable |
| **Підключення** | SSH over USB — без хмари, без підписок |
| **Мова** | Python (FastMCP) |

### Що це робить

- **Нативне вилучення введеного тексту** (Type Folio / віртуальна клавіатура) — миттєво, без OCR.
- **OCR рукописного тексту** через Google Cloud Vision (1000 безкоштовних запитів на місяць).
- **Розумний пошук** по всій вашій бібліотеці.
- **Вилучення тексту** з PDF та EPUB + анотації.
- **Повний обхід (traverse)** документів.

### Чому це №1

Ви можете запитати у Claude: «Що я записав про X під час зустрічі 15 січня?» — він шукатиме у ваших рукописних нотатках. reMarkable стає **«другим мозком», до якого можна робити запити (queryable second brain)**.

### Технічний стек

```
FastMCP + rmscene (parsing .rm natif) + PyMuPDF (PDF)
+ Google Cloud Vision (OCR) + Paramiko (SSH)
```

### Швидке встановлення

```bash
# 1. Активувати SSH на reMarkable
# Settings → Help → Copyrights and licenses → IP + root password

# 2. Клонувати репозиторій
git clone https://github.com/SamMorrowDrums/remarkable-mcp
cd remarkable-mcp && pip install -e .

# 3. Додати до Claude Code
# У ~/.claude.json або через "claude mcp add"
```

### Конфігурація в Claude Code

```json
{
  "mcpServers": {
    "remarkable": {
      "command": "python",
      "args": ["-m", "remarkable_mcp"],
      "env": {
        "REMARKABLE_HOST": "10.11.99.1",
        "REMARKABLE_PASSWORD": "<root-password>"
      }
    }
  }
}
```

---

## 2. Ghostwriter: Інтерфейс Vision-LLM

**ROI: експериментальний | Зусилля: низькі (потрібно скопіювати один бінарний файл Rust)**

| Атрибут | Деталі |
|---------|--------|
| **Репозиторій** | https://github.com/awwaiid/ghostwriter |
| **Модель** | GPT-4o Vision |
| **Обговорення на HN** | https://news.ycombinator.com/item?id=42979986 |

### Концепція

Ви пишете промпт вручную на reMarkable. Мультимодальна модель (GPT-4o Vision) зчитує ваш почерк + ваші малюнки та відповідає **безпосередньо на планшеті**.

### Встановлення

```bash
# 1. Завантажити скомпільований бінарний файл Rust
scp ghostwriter root@10.11.99.1:/home/root/

# 2. SSH + запуск
ssh root@10.11.99.1
chmod +x ghostwriter && ./ghostwriter
```

### Підтримувані взаємодії

- Розпізнавання рукописного тексту (Handwriting recognition).
- Аналіз ескізів (wireframes, схеми).
- Невелика іконографічна мова.
- Жести.

### Конкретний юзкейс

Ви малюєте схему архітектури, пишете «оптимізуй це» — LLM візуально аналізує та відповідає. Захоплюючий прототип для взаємодії людини та ШІ за допомогою пера.

**Чесне обмеження**: нативний застосунок для малювання на reMarkable є мінімалістичним (немає вільного розміщення тексту у відповіді).

---

## 3. Синхронізація reMarkable → Obsidian

**ROI: високий, якщо ви використовуєте Obsidian | Зусилля: від низьких до середніх**

### Варіант А: Scrybble (найбільш повний)

| Атрибут | Деталі |
|---------|--------|
| **Сайт** | scrybble.ink |
| **Плагін Obsidian** | Community plugin (налаштування сховища) |
| **Хостинг** | Self-hosted або сервер Scrybble |
| **Обговорення** | https://forum.obsidian.md/t/scrybble-sync-plugin/103194 |

**Що це робить:**

- Синхронізує блокноти, PDF, ePub → сховище Obsidian.
- Вилучає виділення (highlights) з PDF/ePub у форматі Markdown.
- Вилучає введений текст у форматі Markdown.
- Повністю рендерить блокноти в PDF всередині сховища.
- Організовує за сторінками та тегами.

**Юзкейс**: академічні дослідження, ведення нотаток на зустрічах з подальшим пошуком в Obsidian.

### Варіант Б: Кастомний плагін Cloud Sync

- **Демо**: https://www.youtube.com/watch?v=EsRdi8J9Cnc
- Команда `remarkable insert` → завантаження файлів із хмари reMarkable.
- PDF у папці `rm/` → вбудовування (embed) в нотатки Obsidian.
- Автоматичне повторне завантаження при змінах на планшеті.

---

## 4. Кастомний пайплайн OCR + ШІ

**ROI: високий для персоналізованого воркфлоу | Зусилля: від середніх до високих**

### rmirror + Claude API (рекомендований патерн)

Джерело: https://news.ycombinator.com/item?id=47110872 (лютий 2026)

**Концепція**: фоновий агент macOS, який:
1. Синхронізує нотатки з reMarkable.
2. Виконує OCR через Claude API (краще за Tesseract для рукописного тексту завдяки розумінню контексту).
3. Надсилає транскрибовані нотатки в Notion як сторінки для пошуку.

**Чому Claude кращий за Tesseract для OCR**: Claude розуміє контекст, виправляє погано сформовані слова, автоматично структурує списки та таблиці.

### Пайплайн «Зроби сам» (DIY Pipeline)

```
reMarkable → SSH/USB
  → extract .rm files
  → rmscene parse (нативний текст, якщо використовувався Type Folio)
  → Claude Vision API (скриншоти сторінок для рукописного тексту)
  → структурований текст + автотеги
  → Notion/Obsidian/GitHub через API
```

### Інструменти для парсингу

| Інструмент | Використання | Посилання |
|------------|--------------|-----------|
| **rmscene** | Нативний парсинг файлів .rm | https://github.com/ricklupton/rmscene |
| **rmc** | Конвертує .rm → SVG/PNG | https://github.com/ricklupton/rmc |
| **rmapi** | Інтерфейс Cloud API на Go | https://github.com/juruen/rmapi |

---

## 5. Доступ по SSH та інструменти спільноти

**Необхідна база для всього іншого**

### Активація SSH

```bash
# Через інтерфейс планшета:
# Settings → Help → Copyrights and licenses
# → Показує: IP + root password

# USB (пряме підключення)
ssh root@10.11.99.1

# WiFi (після активації)
rm-ssh-over-wlan on
# або через "Simply Customize It"
```

### Основні інструменти

| Інструмент | Використання | Посилання |
|------------|--------------|-----------|
| **RMHacks/xovi** | Фреймворк модів для rM1/2/Paper Pro | https://www.nilorea.net/2025/08/11/latest-rmhacks-with-xovi-for-remarkable-1-2-paper-pro/ |
| **Simply Customize It** | GUI для перемикання функцій (WLAN SSH тощо) | Сторонній застосунок |
| **ReMy** | GUI для перегляду/експорту документів через SSH (без хмари) | https://github.com/bordaigorl/remy |
| **rmirro** | Двонаправлена синхронізація PDF «планшет ↔ локальна папка» | https://github.com/hersle/rmirro |
| **reStream** | Стрімінг екрана reMarkable на Mac/PC | https://github.com/rien/reStream |
| **KOReader** | Альтернативний рідер (більше форматів, кастомізація) | Через SSH |
| **reGitable** | Автоматичний бекап через git | awesome-reMarkable |

### Кастомні шаблони (templates)

```bash
# Створити SVG-шаблон → скопіювати через SSH
scp mon-template.svg root@10.11.99.1:/usr/share/remarkable/templates/

# Відредагувати templates.json для його реєстрації
ssh root@10.11.99.1 'vi /usr/share/remarkable/templates/templates.json'
```

**Інструменти генерації**: ReCalendar.me, Remarkable Grid Generator, Remarkably Planner Builder.

---

## 6. Недостатньо використані нативні функції

**Зусилля: нульові | Включено в підписку Connect (~6 €/місяць)**

| Функція | Використання |
|---------|--------------|
| **Handwriting conversion** | Виділити → Конвертувати → Скопіювати/Вставити в будь-який застосунок |
| **Cloud sync** | Інтеграція з Google Drive, Dropbox, OneDrive |
| **Send to Slack** | Надсилання нотаток із зустрічей безпосередньо в канал |
| **Handwriting search** (beta AI) | Пошук по минулих рукописних нотатках |
| **Screen sharing** | Демонстрація екрана на ПК (презентації, зустрічі) |
| **Send to email** | Надсилання як PDF або PNG |

**Порада**: перетворення рукописного тексту на друкований добре працює для окремих слів, але гірше для щільних курсивних речень. Для кращого перетворення намагайтеся писати розбірливіше.

---

## 7. Офіційний API та портал для розробників

| Ресурс | Посилання |
|--------|-----------|
| **Developer Portal** | https://developer.remarkable.com |
| **Cloud API docs** | https://github.com/splitbrain/ReMarkableAPI |
| **Community guide** | https://remarkable.guide/ |
| **rmfakecloud** | Self-hosted хмара (без підписки Connect) |

**ОС**: Linux (Codex), повний SSH root-доступ, сумісний із GPL. Крос-компіляторний інструментарій дозволяє розгортати кастомні нативні застосунки.

**rmfakecloud**: альтернатива з відкритим кодом для хмари reMarkable для самостійного хостингу синхронізації та відмови від підписки Connect.

---

## 8. Автоматизація через Zapier

**ROI: середній | Зусилля: низькі | Код не потрібен**

**Механізм**: reMarkable → email (my@remarkable.com) → Zapier перехоплює → автоматична дія.

### Можливі напрямки

Google Drive, Asana, ClickUp, Trello, Slack, WordPress, Evernote, Notion.

### Безкоштовний тариф

- 100 завдань на місяць.
- 2-етапні Zaps.
- Перевірка кожні 15 хвилин.

### Конкретні воркфлоу

```
Нотатки з зустрічі → PDF автозавантажується на Google Drive
Ескіз → Файл надсилається в Slack-канал
Action items → Створення завдань в Asana/ClickUp
```

**Джерело**: https://myremarkable.substack.com/p/integrating-remarkable

---

## 9. Read-it-later: Веб → reMarkable

**ROI: високий для читання | Зусилля: майже нульові**

| Інструмент | Опис |
|------------|------|
| **Розширення Chrome "Read on reMarkable"** | Зберігає будь-яку веб-сторінку → EPUB/PDF на планшеті (з видаленням реклами) |
| **Goosepaper** | Щоденний збір RSS-стрічок + новин + Wikipedia → оптимізований під e-ink формат |
| **remarkable_news** | Новини/комікси/зображення дня як заставка екрана |
| **Обхідний шлях для Instapaper** | Завантаження статей у форматі EPUB → імпорт через десктопний застосунок |

**Варіант PDF**: Клацнути правою кнопкою миші на розширенні → "Read on reMarkable as PDF" (налаштовувані поля для зручного анотування).

---

## 10. Нотатки із зустрічей → Самарі за допомогою ШІ

**ROI: високий | Зусилля: дуже низькі**

### Ручний воркфлоу (без MCP)

```
1. Ведення рукописних нотаток під час зустрічі
2. Скриншот через мобільний застосунок reMarkable (або хмарна синхронізація)
3. Завантаження зображення в Claude/ChatGPT
4. Промпт: "Résume ces notes, extrais les action items avec deadlines et responsables" (або українською)
```

### Воркфлоу з MCP (із встановленим remarkable-mcp)

```
Claude, résume mes notes de la réunion d'aujourd'hui
→ Claude завантажує файли через SSH
→ Виконує OCR за потреби
→ Створює структуроване резюме (самарі) одразу
```

**Перевага MCP**: пропускає кроки створення скриншотів та завантаження файлів. Працює навіть без підписки Connect.

### Рекомендований шаблон

Paper Pro Move Meeting Notebook: 60 зустрічей, 5 пов'язаних сторінок на зустріч (огляд + нотатки + завдання + подальші кроки).

---

## 11. Zotero → reMarkable (дослідження)

**ROI: високий, якщо ви читаєте наукові статті (papers) | Зусилля: середні**

| Інструмент | Використання |
|------------|--------------|
| **Zotero2reMarkable Bridge** | Синхронізація PDF із Zotero з підтримкою виділень (highlights) |
| **KOReader + Toltec + Zotero plugin** | Найкраще читання двоколонкових PDF, двонаправлена синхронізація |
| **sync_zotero_remarkable** | Легша альтернатива |

**Чесне обмеження**: reMarkable — це закрита система. Інтеграція із Zotero вимагає обхідних шляхів. Вона не така плавна, как на e-reader з Android та нативним Zotero. Все працює, але з певним тертям.

---

## 12. Показ екрана як дошка з підтримкою ШІ

**ROI: презентація/фасилітація | Зусилля: нульові (нативна функція Connect)**

- **Screen Share**: Ваші записи з'являються в реальному часі на зовнішньому екрані / віртуальній зустрічі.
- **Laser pointer**: Стилус поблизу верхньої частини екрана → активує лазерну указку.
- **Комбінований воркфлоу**: Screen Share + колега, який надсилає ваші нотатки в ChatGPT в реальному часі = інтерактивна ШІ-дошка.

**Ціна**: Включено в підписку Connect (~30 $/рік у США, ~6 €/місяць в ЄС).

---

## 13. Кастомні застосунки та цікаві хаки

| Застосунок/Хак | Опис |
|----------------|------|
| **Ephemeris** | Щоденний розклад, згенерований із ваших календарів (Python) |
| **Remarcal** | Синхронізація календарів Google/Outlook/Apple → reMarkable |
| **reMarkable keywriter** | Застосунок для ведення нотаток за допомогою клавіатури без відволікань |
| **remarkable-wikipedia** | Офлайн-читач Вікіпедії |
| **whiteboard-hypercard** | Спільне малювання та взаємодія в реальному часі |
| **NetSurf** | Мінімалістичний веб-браузер (через SSH) |
| **pdf2remarkable** | Завантаження PDF у хмару через командний рядок |
| **send-to-remarkable** | Завантаження документів через email (в стилі send-to-Kindle) |
| **libreMarkable** | Фреймворк для розробки нативних застосунків |
| **oxide/remux/draft** | Лаунчери для багатозадачності |
| **latex-yearly-planner** | Річний планер, згенерований у LaTeX |

**Повний каталог**: https://github.com/reHackable/awesome-reMarkable

---

## 14. ШІ-посилені воркфлоу для самостійної розробки

Воркфлоу, які ще не упаковані як готові рішення, але можуть бути створені за допомогою наявних інструментів.

### А. Щоденник із ШІ-аналізом

```
Щовечора → запис 1 сторінки роздумів на reMarkable
→ remarkable-mcp + Claude → щотижневий аналіз паттернів, емоцій, рішень
→ Вихідний результат: інсайти в Obsidian із графом зв'язків
```

### Б. Допоміжне опрацювання вхідних (Inbox Processing)

```
Статті/дослідження прочитані та анотовані на reMarkable
→ OCR через Claude Vision → структуровані резюме (самарі)
→ Автоматичні теги + сортування в Obsidian/Notion
```

### В. Від ескізу до коду (Sketch-to-code)

```
Малювання ескізу інтерфейсу користувача (wireframe UI) на reMarkable
→ Скриншот → Claude Vision → код HTML/React
```

### Г. Автоматичні картки (Flashcards)

```
Нотатки з лекцій/читання на reMarkable
→ remarkable-mcp → Claude виділяє ключові концепції
→ Автоматично генерує картки Anki
```

### Д. Автоматизований щоденний стендап (Daily Standup)

```
Список завдань, записаний щоранку (кастомний шаблон)
→ OCR → автоматично відформатований звіт у Slack/email
→ Кінець дня: відмітка виконаних пунктів, надсилається звіт про різницю (diff)
```

### Е. Захоплення брейншторму → Ментальна карта (Mind Map)

```
Вільно накидані ідеї на сторінці
→ Claude Vision аналізує просторове розташування та текст
→ Генерує структуровану ментальну карту (Mermaid/Markmap)
```

---

## 15. З чого почати

### Фаза 1 — Цими вихідними (2 год)

1. Активувати SSH через Settings → Help → Copyrights and licenses.
2. Встановити **remarkable-mcp** та підключити його до Claude Code.
3. Тест: попросити Claude здійснити пошук у ваших нотатках.

### Фаза 2 — Наступного тижня

4. Якщо ви використовуєте Obsidian → встановити Scrybble.
5. Протестувати **Ghostwriter** (10 хвилин на встановлення, гарантоване задоволення).

### Фаза 3 — Коли захочете піти далі

6. Налаштувати кастомний OCR-пайплайн за допомогою Claude Vision API.
7. Дослідити rmfakecloud для роботи без підписки Connect.

---

## Джерела

**Проєкти GitHub**

- https://github.com/SamMorrowDrums/remarkable-mcp (MCP-сервер, листопад 2025)
- https://github.com/awwaiid/ghostwriter (інтерфейс Vision-LLM)
- https://github.com/reHackable/awesome-reMarkable (каталог спільноти)
- https://github.com/hersle/rmirro (синхронізація без хмари)
- https://github.com/bordaigorl/remy (GUI для SSH)
- https://github.com/rien/reStream (стрімінг екрана)
- https://github.com/splitbrain/ReMarkableAPI (документація Cloud API)
- https://github.com/ricklupton/rmscene (нативний парсинг .rm)

**Статті та обговорення**

- https://sam-morrow.com/blog/building-an-mcp-server-for-remarkable
- https://news.ycombinator.com/item?id=47110872 (rmirror + Claude OCR, лютий 2026)
- https://news.ycombinator.com/item?id=42979986 (Ghostwriter на HN)
- https://news.ycombinator.com/item?id=46099997 (Hacking reMarkable 2, HN 2025)
- https://sgt.hootr.club/blog/hacking-on-the-remarkable-2/ (керівництво з SSH хакінгу)
- https://myremarkable.substack.com/p/integrating-remarkable (інтеграція Zapier)

**Obsidian**

- https://forum.obsidian.md/t/scrybble-sync-plugin/103194
- https://www.youtube.com/watch?v=EsRdi8J9Cnc (демо Cloud sync)

**Офіційні ресурси**

- https://developer.remarkable.com (Developer Portal, SDK, API)
- https://remarkable.guide/ (посібник спільноти)

---
**Локалізація**: [Serhii (MacPlus Software)](https://macplus-software.com)
*Остання синхронізація: Травень 2026*
