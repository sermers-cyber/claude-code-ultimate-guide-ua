---
name: cyber-defense-team
description: "Оркестрація конвеєра кіберзахисту з 4 агентів для аналізу лог-файлів на загрози. Використовуйте, коли розслідуєте журнали безпеки, виявляєте аномалії в патернах доступу, класифікуєте серйозність зламу або генеруєте звіти про інциденти з файлів nginx/auth/syslog."
allowed-tools: Read Bash
argument-hint: "[log-file-path]"
effort: high
metadata:
  version: 1.0.0
---

# Skill команди кіберзахисту

Оркеструє конвеєр із 4 агентів, який аналізує лог-файли на загрози безпеці й готує звіт про інцидент.

## Архітектура конвеєра

```
[You] -> Team Lead (this skill)
           |
           |-[1]-> log-ingestor    (haiku)  -> cyber-defense-events.json
           |
           |-[2]-> anomaly-detector (sonnet) -> cyber-defense-anomalies.json
           |                                    (reads events.json)
           |-[3]-> risk-classifier  (sonnet) -> cyber-defense-risk.json
           |                                    (reads anomalies.json)
           `-[4]-> threat-reporter  (sonnet) -> cyber-defense-report.md
                                               (reads all 3 JSON files)
```

Етапи 2 і 3 послідовні (кожен залежить від виводу попереднього). Етап 4 запускається, коли всі дані готові.

## Кроки виконання

### Крок 1: Перевірте вхідні дані

Переконайтеся, що лог-файл існує (або що вміст логу надано безпосередньо в повідомленні). Якщо шляху не існує, одразу скажіть про це користувачу й не продовжуйте.

### Крок 2: Запустіть log ingestor

Використайте інструмент Agent, щоб запустити агента `log-ingestor`:

```
Task: Parse the log file at [log_path] and write structured events to cyber-defense-events.json.
Log path: [log_path]
```

Дочекайтеся завершення. Переконайтеся, що `cyber-defense-events.json` створено.

### Крок 3: Запустіть anomaly detector

Використайте інструмент Agent, щоб запустити агента `anomaly-detector`:

```
Task: Read cyber-defense-events.json and detect anomalies. Write results to cyber-defense-anomalies.json.
```

Дочекайтеся завершення. Якщо `anomalies_found: 0`, перейдіть до Кроку 5 (reporter однаково запускається).

### Крок 4: Запустіть risk classifier

Використайте інструмент Agent, щоб запустити агента `risk-classifier`:

```
Task: Read cyber-defense-anomalies.json and classify overall risk. Write result to cyber-defense-risk.json.
```

### Крок 5: Запустіть threat reporter

Використайте інструмент Agent, щоб запустити агента `threat-reporter`:

```
Task: Read cyber-defense-events.json, cyber-defense-anomalies.json, and cyber-defense-risk.json. Generate a complete incident report and save it to cyber-defense-report.md.
```

### Крок 6: Підсумуйте для користувача

Прочитайте `cyber-defense-risk.json` і покажіть:

```
Analysis complete

Risk Level : HIGH
Score      : 74/100
Threats    : 2 anomalies detected
Report     : cyber-defense-report.md

Primary threat: Brute force attack from 192.168.1.105
Immediate action required: [first recommended_action]
```

## Обробка помилок

- Агент падає на кроці 2: повідомте користувача, зупиніть конвеєр, покажіть необроблену помилку.
- Агент падає на кроці 3+: покажіть часткові результати, зазначте, на якому етапі стався збій.
- Лог-файл не знайдено: «Файл [path] не знайдено. Вкажіть коректний шлях або вставте вміст логу.»

## Оцінка вартості

| Етап | Модель | Типова кількість токенів |
|-------|-------|----------------|
| log-ingestor | haiku | ~2K |
| anomaly-detector | sonnet | ~3K |
| risk-classifier | sonnet | ~2K |
| threat-reporter | sonnet | ~3K |
| **Усього** | | **~10K** |

Для великих лог-файлів (>10K рядків) log-ingestor може використати до 20K токенів.

## Приклад використання

```
/cyber-defense-team /var/log/nginx/access.log
/cyber-defense-team /tmp/auth.log
```
