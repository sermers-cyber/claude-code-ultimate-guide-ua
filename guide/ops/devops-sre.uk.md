---
title: "DevOps та SRE з Claude Code"
description: "Фреймворк FIRE для діагностики інфраструктури та DevOps-воркфлоу з Claude Code"
tags: [devops, guide, ci-cd, workflows]
---

# DevOps та SRE з Claude Code

**Час читання**: 30 хвилин
**Рівень навичок**: Середній (передбачає знання основ DevOps)
**Передумови**: Основи Claude Code ([Розділи 1-2](#getting-started) основного посібника)

---

> **Фреймворк FIRE**: Системний підхід до діагностики інфраструктури за допомогою Claude Code.
>
> **F**irst Response (Перша відповідь) → **I**nvestigate (Дослідження) → **R**emediate (Усунення) → **E**valuate (Оцінка)

---

## Зміст

1. [Швидкий старт](#швидкий-старт)
2. [Патерн: Діагностика інфраструктури](#pattern-діагностика-інфраструктури)
3. [Патерн: Реагування на інциденти](#pattern-реагування-на-інциденти)
4. [Патерн: Інфраструктура як код](#pattern-інфраструктура-як-код)
5. [Запобіжники та впровадження](#запобіжники-та-впровадження)
6. [Швидкий довідник](#швидкий-довідник)

---

# Швидкий старт

**Мета**: Почати ефективно використовувати Claude Code для DevOps за 5 хвилин.

## Швидка самоперевірка

| Ситуація | Перейти до |
|-----------|---------|
| У мене активний інцидент ПРЯМО ЗАРАЗ | [Екстрено: Усунення несправностей K8s](#kubernetes-troubleshooting) |
| Вперше використовую Claude для DevOps | [Туторіал: Перша діагностика](#ваша-перша-діагностика-інфраструктури) |
| Хочу автоматизувати свої регламенти | [Патерн: Реагування на інциденти](#pattern-реагування-на-інциденти) |
| Оцінюю інструмент для своєї команди | [Запобіжники та впровадження](#запобіжники-та-впровадження) |
| Потрібні готові промпти | [Швидкий довідник](#швидкий-довідник) |

## Фреймворк FIRE

Кожна діагностика інфраструктури з Claude слідує цьому патерну:

```
F - First Response (Перша відповідь)   → Надайте Claude симптом + контекст
I - Investigate (Дослідження)          → Claude аналізує логи, метрики, конфігурацію
R - Remediate (Усунення)               → Claude пропонує виправлення (з вашим схваленням)
E - Evaluate (Оцінка)                  → Постмортем, документація, запобігання
```

### Чому FIRE?

| Фаза | Роль людини | Роль Claude |
|-------|------------|-------------|
| **F**irst Response | Описати симптом, надати контекст | Тріаж, пріоритезація перевірок |
| **I**nvestigate | Запускати команди, копіювати вивід | Аналізувати, корелювати, будувати гіпотези |
| **R**emediate | **Схвалити або відхилити** | Пропонувати виправлення, пояснювати вплив |
| **E**valuate | Переглянути, поділитися знаннями | Генерувати постмортем, документацію |

**Важливо**: Claude пропонує, ви схвалюєте. Це особливо критично для:
- Деструктивних операцій (видалення, масштабування вниз, перезапуск)
- Продуктових середовищ (Production)
- Змін, чутливих до безпеки

## Ваша перша діагностика інфраструктури

### Приклад: Pod у стані CrashLoopBackOff

```bash
# Крок 1: FIRST RESPONSE - Надайте контекст
claude "I have a pod in CrashLoopBackOff in the payment-service namespace.
Environment: production
Cluster: gke-prod-us-east1
Started: 10 minutes ago
What are the first 3 things I should check?"

# Крок 2: INVESTIGATE - Запустіть запропоновані команди та поділіться виводом
kubectl describe pod payment-api-7d4b8c6f5-x2j9k -n payment-service
# Скопіюйте вивід та вставте в Claude

# Крок 3: REMEDIATE - Claude пропонує, ви схвалюєте
claude "Based on this describe output, what's the fix?
CONSTRAINT: Show me the exact command but don't execute anything."

# Крок 4: EVALUATE - Задокументуйте інцидент
claude "Create a brief incident note for our wiki:
- What happened
- Root cause
- Fix applied
- Prevention recommendation"
```

### Що повертає Claude (Приклад першої відповіді)

```markdown
## CrashLoopBackOff Triage (Priority Order)

1. **Check exit code and last logs**
   ```bash
   kubectl logs payment-api-7d4b8c6f5-x2j9k -n payment-service --previous
   ```
   Most common: OOM (exit 137), config errors (exit 1), dependency failures

2. **Check pod events and resource limits**
   ```bash
   kubectl describe pod payment-api-7d4b8c6f5-x2j9k -n payment-service
   ```
   Look for: OOMKilled, ImagePullBackOff, liveness probe failures

3. **Check recent deployment changes**
   ```bash
   kubectl rollout history deployment/payment-api -n payment-service
   ```
   If recent: consider rollback while investigating
```

---

# Pattern: Діагностика інфраструктури

**Мета**: Системне усунення несправностей для поширених проблем інфраструктури.

## Kubernetes Troubleshooting

### Налаштування MCP-сервера K8s

Для постійного доступу до контексту K8s встановіть MCP-сервер:

```json
// ~/.claude.json (або .mcp.json)
{
  "mcpServers": {
    "kubernetes": {
      "command": "npx",
      "args": ["-y", "kubernetes-mcp-server@latest"]
    }
  }
}
```

**Переваги**: Claude може запитувати стан кластера безпосередньо, що скорочує кількість ручних операцій та копіювання-вставки.

**Без MCP**: Ви будете вручную передавати вивід kubectl до Claude (це все ще дуже ефективно).

### Промпти за симптомами

Скопіюйте ці промпти, замінивши значення у `<кужках>`.

#### CrashLoopBackOff

```bash
kubectl describe pod <pod> -n <ns> | claude "Analyze this CrashLoopBackOff:
1. What's the exit code and what does it mean?
2. Check the last 5 restarts pattern (timing, consistent or escalating?)
3. Suggest 3 most likely root causes based on the events
4. Give me the exact commands to investigate each hypothesis"
```

**Типові причини, які виявить Claude**:
- Exit 137: OOMKilled (перевищено ліміт пам'яті)
- Exit 1: Помилка застосунку (неправильний конфіг, відсутня залежність)
- Exit 143: SIGTERM (тайм-аут коректного завершення)

#### OOMKilled

```bash
kubectl top pods -n <ns> && kubectl describe pod <pod> -n <ns> | claude "This pod was OOMKilled:
1. Compare requests vs limits vs actual usage
2. Is this a memory leak or under-provisioning?
3. If leak: what patterns in the container suggest investigation paths?
4. If under-provisioned: suggest optimal resource settings based on this data"
```

**Наступні кроки для дослідження витоку пам'яті**:
```bash
claude "The pod has been restarting every 2 hours with OOMKilled.
Memory grows linearly from 200Mi to 512Mi limit before crash.
Language: Node.js 18
What are the top 3 things to check for memory leaks in this stack?"
```

#### ImagePullBackOff

```bash
kubectl describe pod <pod> -n <ns> | claude "ImagePullBackOff diagnosis:
1. Is this an auth issue, network issue, or wrong image name?
2. What's the exact error message telling us?
3. Give me commands to verify the image exists and credentials work"
```

#### Завислий под (Pending Pod - не розгортається)

```bash
kubectl describe pod <pod> -n <ns> && kubectl describe nodes | claude "Pod stuck in Pending:
1. Is this resource constraints, node selectors, or affinity rules?
2. Which nodes were considered and why rejected?
3. What's the quickest fix vs proper solution?"
```

#### Недоступний сервіс (Service Not Reachable)

```bash
kubectl get svc,endpoints -n <ns> && kubectl describe svc <svc> -n <ns> | claude "Service not reachable:
1. Are there healthy endpoints?
2. Is the selector matching pods correctly?
3. Is it a network policy blocking traffic?
Give me diagnostic commands for each possibility"
```

### Кейс: Коренева причина збою в продакшені

**Ситуація**: Платформа електронної комерції, виклик о 3 ранку, сервіс оформлення замовлень повертає 503 помилки.

**FIRE в дії**:

```bash
# F - First Response
claude "INCIDENT: checkout-service returning 503s, started 10 min ago.
Impact: 100% of checkout attempts failing.
Environment: AWS EKS production, us-east-1.
Recent changes: deployment 2 hours ago (new feature flag logic).
What's the fastest diagnostic path?"

# I - Investigate (Claude запропонував перевірити поди спочатку)
kubectl get pods -n checkout -l app=checkout-service
# Вивід: 3/5 подів у CrashLoopBackOff

kubectl logs checkout-service-xxx --previous | tail -50 | claude "Analyze crash logs"
# Claude виявляє: panic: nil pointer dereference у коді feature flag

# R - Remediate
claude "Root cause identified: nil pointer in feature flag logic from recent deploy.
Options:
A) Rollback to previous version
B) Hotfix the nil check
Which is faster and safer at 3 AM?"
# Claude рекомендує: Rollback (швидше, гарантовано стабільний стан, фікс завтра вдень)

kubectl rollout undo deployment/checkout-service -n checkout
# Сервіс відновлено за 2 хвилини

# E - Evaluate (наступного дня)
claude "Create postmortem from this incident:
Timeline: 3:02 AM alert, 3:15 AM root cause found, 3:17 AM rollback, 3:19 AM resolved
Root cause: Feature flag nil pointer from commit abc123
Impact: 15 minutes checkout downtime
Format: Blameless, focused on prevention"
```

**Результат**: MTTR 15 хвилин, чіткий постмортем, визначені заходи щодо запобігання подібним інцидентам.

## Аналіз та кореляція логів

### Кореляція логів між кількома сервісами

```bash
# Збір логів із суміжних сервісів
kubectl logs -l app=api-gateway -n ingress --since=10m > gateway.log
kubectl logs -l app=auth-service -n auth --since=10m > auth.log
kubectl logs -l app=payment-service -n payment --since=10m > payment.log

# Кореляційний аналіз
cat gateway.log auth.log payment.log | claude "Correlate these logs:
1. Find the request flow for failed transactions
2. Identify where the failure originates
3. Are there patterns in timing or specific endpoints?
4. Create a timeline of events"
```

### Виявлення аномальних патернів у логах

```bash
# Пошук аномалій у помилках
grep -E "ERROR|WARN|Exception" app.log | claude "Analyze error patterns:
1. Cluster similar errors (group by type, not timestamp)
2. What's the most frequent vs most severe?
3. Which errors are correlated (same root cause)?
4. Prioritize investigation order"
```

### Допомога із запитами Prometheus/Grafana

```bash
claude "I need a PromQL query to:
- Show p99 latency for the payment-service
- Group by endpoint
- Alert if > 500ms for 5 minutes
Include the alert rule YAML too"
```

## Що Claude НЕ МОЖЕ (Обмеження)

Розуміння обмежень запобігає розчаруванню та небезпечній довірі до інструменту.

| Обмеження | Вплив | Спосіб вирішення |
|------------|--------|------------|
| **Немає стану кластера в реальному часі** | Не бачить поточний статус подів | Використовуйте K8s MCP або копіюйте вивід kubectl |
| **Немає прямого доступу до API хмари** | Не може викликати API AWS/GCP | Використовуйте MCP-сервери або діліться виводом CLI |
| **Ліміти вікна контексту** | Макс. ~100K токенів | Передавайте релевантні фрагменти логів, а не повні дапми |
| **Немає постійної пам'яті** | Забуває контекст між сесіями | Записуйте специфіку проекту в CLAUDE.md |
| **Ризик галюцинацій** | Може запропонувати неіснуючі прапорці команд | Завжди перевіряйте критичні команди перед запуском |
| **Немає метрик у реальному часі** | Не бачить графіки моніторингу | Опишіть значення метрик або надайте вивід `kubectl top` |
| **Немає доступу до секретів** | Не може читати паролі та ключі | Чудово! Ніколи не діліться секретами з LLM |

### Коли НЕ ВАРТО використовувати Claude

- **Критичні рішення за 30 секунд**: Ваша м'язова пам'ять та знання інфраструктури спрацюють швидше.
- **Інциденти з високим ступенем конфіденційності**: Розслідування витоків даних (юридичні наслідки).
- **Прості та очевидні виправлення**: Якщо ви вже знаєте, що робити — просто зробіть це.
- **Суворі регуляторні обмеження (compliance)**: Переконайтеся, що політики безпеки компанії дозволяють використовувати AI-помічників для таких даних.
- **Специфічні інциденти безпеки ШІ**: Виявлено ін'єкцію промптів, скомпрометовано MCP-сервер або помічено підозрілий витік даних агентом → див. [Посилення безпеки: Реагування](../security/security-hardening.uk.md#частина-3-реагування-коли-щось-пішло-не-так) для вивчення аварійного вимкнення (kill switch), рівнів локалізації та ведення хронології.

### Де Claude демонструє найкращі результати

- **Аналіз складних кореневих причин**: Взаємодія кількох складних систем.
- **Генерація документації**: Написання постмортемів, регламентів (runbooks), інструкцій.
- **Вивчення нових інструментів**: Незнайомі хмарні сервіси, нові можливості Kubernetes.
- **«Друга думка» (Second opinion)**: Валідація ваших здогадок та гіпотез перед деплоєм.
- **Групові операції**: Генерація шаблонних конфігурацій для багатьох середовищ.

---

# Pattern: Реагування на інциденти

**Мета**: Структуровані робочі процеси для управління інцидентами.

## Соло-інцидент (Нічний виклик)

**Реальність**: О 3 ранку ви самі на чергуванні. Цей робочий процес розроблено спеціально для однієї людини.

### FIRE в дії: Соло-інцидент

#### F - First Response (30 секунд)

```bash
claude "INCIDENT: [symptom - be specific]
Context: [service], [environment], [time started]
Recent changes: [deploys, infra changes, traffic spikes]
Current impact: [% users affected, revenue impact if known]
What are the 3 most critical things to check first?"
```

*Приклад*:
```bash
claude "INCIDENT: API returning 500 errors on /checkout endpoint
Context: checkout-service, production-us-east-1, started 5 min ago
Recent changes: deployed v2.3.4 at 2:45 AM, added new payment provider
Current impact: ~30% of checkout requests failing
What are the 3 most critical things to check first?"
```

#### I - Investigate (2-5 хвилин)

Запускайте запропоновані Claude команди та діліться результатами:

```bash
# Claude запропонував перевірити стан подів
kubectl get pods -n checkout | claude "Quick assessment of this pod list"

# Далі — перевірити останні логи
kubectl logs -l app=checkout --since=5m | head -100 | claude "Analyze for error patterns"

# Потім — перевірити історію розгортання
kubectl rollout history deployment/checkout-service -n checkout | claude "What changed in the last deployment?"
```

**Порада**: Тримайте один термінал для виконання команд, а інший — для спілкування з Claude.

#### R - Remediate (із обов'язковим схваленням)

```bash
claude "Based on investigation:
- Root cause: [your understanding]
- Evidence: [key findings]

Propose remediation options:
1. Quick mitigation (restore service)
2. Proper fix (address root cause)

CONSTRAINT: I need to approve before any action. Show exact commands."
```

*Приклад шлюзу схвалення*:
```
Claude: "Recommended: Rollback to v2.3.3
Command: kubectl rollout undo deployment/checkout-service -n checkout
Risk: Low - previous version was stable for 2 weeks
Alternative: Scale down the new payment provider feature flag

Which approach do you want to take?"

You: "Proceed with rollback"
```

#### E - Evaluate (проводиться після інциденту, не під час нього)

```bash
claude "Create incident postmortem:

Timeline:
- 2:45 AM: Deployed v2.3.4
- 3:00 AM: First alerts fired
- 3:05 AM: Incident declared
- 3:12 AM: Root cause identified (nil pointer in new payment provider code)
- 3:15 AM: Rollback initiated
- 3:17 AM: Service restored

Format: Blameless, focus on systems not people
Include: Action items with owners"
```

## Комунікація під час інцидентів

### Генератор статус-оновлень для стейкхолдерів

```bash
claude "Generate incident update for stakeholders:

Incident: Checkout service degradation
Current status: Mitigated, monitoring
Impact: 15 minutes of 30% checkout failures
ETA to full resolution: 2 hours (proper fix in next deploy)

Audience: Non-technical executives
Tone: Professional, reassuring, factual
Length: 3 sentences max"
```

*Приклад результату*:
> Ми зафіксували 15-хвилинне погіршення роботи нашого сервісу оформлення замовлень, яке торкнулося приблизно 30% транзакцій; наразі роботу повністю відновлено. Проблема була викликана програмною помилкою в нещодавньому оновленні, і систему було швидко відкочено до стабільної версії. Ми розгорнемо остаточне виправлення під час наступного планового технічного вікна без очікуваного впливу на користувачів.

### Ведення «мосту» інциденту (Incident Bridge)

Для оновлення інформації в реальному часі:

```bash
claude "I'm managing an incident bridge. Help me:
1. Maintain a running timeline of events
2. Suggest next investigation steps when we hit dead ends
3. Draft comms updates every 15 minutes
4. Flag when I should escalate

Current status: [paste latest update]
What should I communicate to the bridge now?"
```

## Багатоагентний патерн: Пост-інцидентний аналіз

**Коли використовувати**: Тільки після повного завершення інциденту. Не використовуйте під час активної аварії.

```bash
# Агент 1: Реконструкція хронології
claude "You are an incident timeline analyst.
From these logs and Slack messages, reconstruct a precise timeline:
[paste logs and comms]
Output: Timestamped events, who did what when"

# Агент 2: Аналіз кореневих причин (RCA)
claude "You are a root cause analyst.
Given this timeline and system architecture, perform 5-whys analysis:
[paste timeline from Agent 1]
Output: Root cause chain, contributing factors"

# Агент 3: Заходи запобігання
claude "You are an SRE process improvement specialist.
Given this root cause analysis:
[paste RCA from Agent 2]
Output: Prioritized prevention measures, effort estimates, ownership suggestions"
```

### Кейс: Оптимізація та скорочення MTTR в OpsWorker.ai

**Контекст**: Команда SRE управляє 200+ мікросервісами, 5 інженерів на чергуванні.

**До впровадження Claude**:
- Середній MTTR: 45 хвилин
- Написання постмортемів: Часто відкладалося або пропускалося
- Силоси знань: Кожен інженер глибоко знав лише обмежену кількість сервісів

**Інтеграція Claude**:
1. Фреймворк FIRE впроваджено як обов'язковий стандарт для всіх інцидентів.
2. Автоматична генерація першої версії постмортему протягом години після вирішення.
3. Збагачення інструкцій та регламентів інтерактивними порадами від Claude.

**Через 3 місяці**:
- Середній MTTR: 18 хвилин (скорочення на 60%)
- Складання постмортемів: 95% готові протягом 24 годин
- Обмін знаннями: Згенеровані за допомогою Claude регламенти стали доступними та зрозумілими для кожного інженера

**Головний інсайт**: Найбільший виграш дали узгодженість і документація, а не швидкість.

---

# Pattern: Інфраструктура як код

**Мета**: Використання Claude для Terraform, Ansible та GitOps робочих процесів.

## Terraform з Claude

### Джерело: Terraform Skill від Антона Бабенка

Найбільш повний та детальний скіл (вміння) для Terraform в Claude Code:

**Репозиторій**: [antonbabenko/terraform-skill](https://github.com/antonbabenko/terraform-skill)
**Автор**: Anton Babenko (творець terraform-aws-modules, 1 млрд+ завантажень)

```bash
# Встановлення
cd ~/.claude/skills/
git clone https://github.com/antonbabenko/terraform-skill.git terraform
```

**Що він додає**:
- Найкращі практики побудови модульної архітектури.
- Перевірені шаблони для AWS, GCP, Azure.
- Рекомендації щодо управління файлом стану (state file).
- Інтеграція в CI/CD конвеєри.

### Типові промпти для Terraform

#### Рев'ю плану змін (Plan Review)

```bash
terraform plan -out=plan.txt && cat plan.txt | claude "Review this Terraform plan:
1. Any dangerous changes? (data loss, downtime)
2. Are the changes what we expect?
3. Any missing changes we should add?
4. Cost implications if visible"
```

#### Генерація модуля

```bash
claude "Generate a Terraform module for:
- AWS ECS Fargate service
- With ALB and target group
- Auto-scaling based on CPU
- Secrets from SSM Parameter Store

Follow these conventions:
- Use for_each over count
- All resources tagged with var.tags
- Output the service URL and ARN"
```

#### Допомога при хірургії файлу стану (State Surgery)

```bash
claude "I need to move a resource to a different state file:
Current state: terraform-prod/terraform.tfstate
Resource: aws_s3_bucket.logs
Target state: terraform-shared/terraform.tfstate

What's the safest procedure? Include rollback steps."
```

### Процес виявлення відхилень конфігурації (Drift Detection)

```bash
# Виявлення відхилень
terraform plan -detailed-exitcode 2>&1 | tee drift.txt

# Аналіз відхилень за допомогою Claude
cat drift.txt | claude "Analyze this Terraform drift:
1. What changed outside of Terraform?
2. Is this drift expected (manual change) or concerning?
3. Should we import the changes or revert to Terraform state?
4. What's the safest remediation path?"
```

## Ansible з Claude

### Рев'ю плейбуків (Playbook Review)

```bash
cat playbook.yml | claude "Review this Ansible playbook:
1. Idempotency issues?
2. Security concerns?
3. Error handling gaps?
4. Performance optimizations?"
```

### Генерація ролей (Role Generation)

```bash
claude "Generate an Ansible role for:
- Installing and configuring Nginx
- SSL certificates via Let's Encrypt (certbot)
- Hardened configuration (disable server tokens, etc.)
- Log rotation

Follow best practices:
- Use handlers for service restarts
- Variables in defaults/main.yml
- Include molecule tests structure"
```

## GitOps з Claude

### Рев'ю конфігурацій ArgoCD

```bash
cat application.yaml | claude "Review this ArgoCD Application:
1. Sync policy appropriate for the environment?
2. Resource health checks defined?
3. Any sync wave ordering issues?
4. Namespace and project permissions correct?"
```

### Генерація Helm Values

```bash
claude "Generate Helm values for deploying [application] to:
- Environment: staging
- Resources: Limited (cost-conscious)
- Replicas: 2
- Ingress: Internal only
- Secrets: From external-secrets operator

Base chart: [chart name]
Include comments explaining each value"
```

## Автоматизація перевірки безпеки

### Аналіз безпеки інфраструктури (IaC Scan)

```bash
# Запуск tfsec або checkov та аналіз результатів
tfsec . --format=json | claude "Analyze these security findings:
1. Prioritize by severity and exploitability
2. Which are false positives in our context?
3. For real issues: what's the fix?
4. Which can we ignore with a documented reason?"
```

### Рев'ю політик IAM (IAM Policy Review)

```bash
cat iam-policy.json | claude "Review this IAM policy:
1. Does it follow least privilege?
2. Any overly permissive actions? (*, admin, etc.)
3. Resource constraints appropriate?
4. Suggest a more restrictive version that still works"
```

---

# Запобіжники та впровадження

**Мета**: Безпечне та раціональне впровадження Claude Code з підтримкою всієї команди.

## Контроль витрат

### Вартість токенів Claude Code

| Модель | Вхід (1 млн токенів) | Вихід (1 млн токенів) |
|-------|-------------------|-------------------|
| Sonnet 5.5 | $2 | $10 |
| Opus 5.5 | $4 | $20 |

Стандартні тарифи API перевірено 24 вересня 2026 року. Для визначення вартості сесії потрібні окремі підрахунки вхідних, вихідних, кешованих токенів і повторних спроб. [Офіційні ціни](https://platform.claude.com/docs/en/about-claude/pricing).

**Стратегії контролю витрат**:
1. Оцініть Sonnet для рутинних завдань; це вибір маршрутизації, а не типове налаштування акаунта.
2. Залишайте Opus для особливо складного крос-системного аналізу архітектур та великих логів.
3. Використовуйте команду `/compact` для зменшення обсягу активного контексту під час довгих діалогів.
4. Уникайте прямого копіювання гігантських лог-файлів; спочатку фільтруйте їх за допомогою grep/tail.

### Оцінка вартості пропонованої інфраструктури

Claude не бачить вашого рахунку в хмарі. Завжди запитуйте перед застосуванням:

```bash
claude "Before I apply these changes, estimate:
1. Monthly cost impact (compute, storage, network)
2. Any resources that could scale unbounded?
3. Cost optimization alternatives?"
```

## Кордони безпеки

### Дані, якими НІКОЛИ не можна ділитися з Claude

| Тип даних | Чому ні | Альтернатива / Заміна |
|-----------|---------|-------------|
| API ключі, токени доступу | Ризик компрометації/витоку | Текстові плейсхолдери: `<API_KEY>` |
| Продакшн-паролі та секрети | Високий ризик безпеки | Вказуйте тільки тип секрету, а не значення |
| Дані користувачів (PII) | Захист конфіденційності | Використовуйте вигадані чи анонімізовані дані |
| Комерційна таємниця, ноу-хау | Захист інтелектуальної власності | Описуйте загальну логіку поведінки |
| Матеріали інцидентів із PII | Юридична відповідальність | Ретельно очищуйте логи перед відправкою |

### Безпечний шаблон промпту

```bash
claude "Debug this authentication issue:
- Service: auth-service
- Error: 401 Unauthorized for valid tokens
- Environment: staging (not production)
- Token format: JWT with claims [user_id, org_id, exp]
- NOTE: I've redacted all actual token values

Here's the sanitized log:
[paste log with secrets replaced]"
```

### Шлюзи схвалення для Production

Завжди вимагайте ручного підтвердження та перевірки для наступних дій:

```yaml
# Приклад: Чек-лист змін у Production
approval_required:
  - kubectl delete
  - kubectl scale (down)
  - terraform destroy
  - DROP TABLE / DELETE FROM
  - rm -rf (поза папками tmp)
  - Будь-який запис у продуктових базах даних
  - Зміна будь-якої IAM політики
  - Модифікація правил Security Group
```

## Чек-лист впровадження в команді

### Фаза 1: Пілотний запуск (1-2 інженери, 2 тижні)

- [ ] Встановити Claude Code для пілотних користувачів.
- [ ] Створити загальнокомандний файл CLAUDE.md із базовим контекстом проекту.
- [ ] Задокументувати перші 5 успішних кейсів автоматизації інфраструктури.
- [ ] Визначити та стандартизувати один ключовий DevOps робочий процес.
- [ ] Оцінити та порівняти збережений час розробки (до/після).

### Фаза 2: Розширення (Команда, 4 тижні)

- [ ] Поділитися результатами пілоту на командній зустрічі.
- [ ] Створити спільну бібліотеку корисних промптів для команди.
- [ ] Затвердити чіткі інструкції з безпеки (що можна і не можна надсилати).
- [ ] Налаштувати загальний репозиторій для кастомних скілів та скриптів.
- [ ] Чітко визначити межі, де використання Claude є небажаним.

### Фаза 3: Постійна оптимізація (Постійно)

- [ ] Щомісячний перегляд та оновлення бібліотеки промптів.
- [ ] A/B тестування: Швидкість та точність вирішення інцидентів з Claude та без.
- [ ] Внесок у розвиток спільноти (awesome-списки, доповнення цього гайду).
- [ ] Відстеження MTTR, регулярності постмортемів та повноти документації.

### Помилки впровадження, яких слід уникати

| Помилка | Чому це трапляється | Як запобігти |
|---------|---------------|------------|
| **Сліпа довіра** | Claude пропонує дуже впевнено | Впровадити правило: завжди перевіряти команду перед запуском |
| **Надмірна залежність** | Навіщо думати, якщо Claude зробить | Сприяти навчанню інженерів, а не простому копіюванню результатів |
| **Context dumping** | Сподівання, що Claude розбереться в хаосі | Надавати структурований, відфільтрований контекст |
| **Пропуск перевірок** | Тиск дедлайнів або стрес при аварії | Зробити валідацію обов'язковим кроком регламенту |
| **Тіньове використання** | Небажання показувати використання ШІ | Робити успіхи публічними, нормалізувати роботу з AI-помічниками |

---

# Швидкий довідник

## Резюме фреймворку FIRE

```
┌─────────────────────────────────────────────────────────────┐
│ F - FIRST RESPONSE (Перша відповідь)                        │
│   "INCIDENT: [symptom]. Context: [service, env, time].      │
│    Recent changes: [what]. Impact: [who affected].          │
│    What are the 3 most critical things to check?"           │
├─────────────────────────────────────────────────────────────┤
│ I - INVESTIGATE (Дослідження)                               │
│   Запускайте запропоновані Claude команди                   │
│   Діліться виводом: "[output] | claude 'Analyze this'"      │
│   Ітеруйте до виявлення кореневої причини (RCA)             │
├─────────────────────────────────────────────────────────────┤
│ R - REMEDIATE (Усунення)                                    │
│   "Based on [findings], propose remediation.                │
│    CONSTRAINT: I need to approve before any action."        │
│   СХВАЛИТИ → Виконання │ ВІДХИЛИТИ → Продовження аналізу    │
├─────────────────────────────────────────────────────────────┤
│ E - EVALUATE (Оцінка)                                       │
│   "Create postmortem: Timeline, root cause, prevention.     │
│    Format: Blameless, action items with owners."            │
└─────────────────────────────────────────────────────────────┘
```

## Промпти за симптомами

### Kubernetes

| Симптом | Промпт |
|---------|--------|
| CrashLoopBackOff | `kubectl describe pod <pod> -n <ns> \| claude "Exit code meaning? 3 likely causes? Commands to investigate?"` |
| OOMKilled | `kubectl top pods && describe pod \| claude "Leak or under-provisioned? Optimal resources?"` |
| ImagePullBackOff | `kubectl describe pod \| claude "Auth, network, or wrong image? Verification commands?"` |
| Pending | `kubectl describe pod && describe nodes \| claude "Resource, selector, or affinity issue?"` |
| Service unreachable | `kubectl get svc,endpoints \| claude "Healthy endpoints? Selector matching? Network policy?"` |

### Хмара та Інфраструктура

| Симптом | Промпт |
|---------|--------|
| Висока затримка (Latency) | `[metrics] \| claude "Bottleneck location? Is it compute, network, or dependency?"` |
| Переповнення диску | `df -h && du -sh /* \| claude "What's consuming space? Safe to delete?"` |
| Відмова у з'єднанні (Refused) | `netstat -tlnp \| claude "Service listening? Port correct? Firewall rules?"` |
| Закінчення терміну SSL | `openssl s_client -connect host:443 \| claude "Days until expiry? Renewal steps?"` |
| Проблеми з DNS | `dig +trace domain \| claude "Where does resolution fail?"` |

### Terraform

| Завдання | Промпт |
|------|--------|
| Рев'ю плану (Plan Review) | `terraform plan \| claude "Dangerous changes? Missing changes? Cost impact?"` |
| Аналіз відхилень (Drift) | `terraform plan -detailed-exitcode \| claude "What drifted? Expected? Remediation?"` |
| Запит модуля | `claude "Generate Terraform module for [resource] with [requirements]"` |

## MCP-сервери для DevOps

| Сервер | Призначення | Встановлення |
|--------|---------|---------|
| Kubernetes | Прямий доступ до стану кластера | `npx -y kubernetes-mcp-server@latest` |
| AWS | Взаємодія з API AWS | `uvx awslabs.aws-api-mcp-server@latest` (Python) |
| GCP | Взаємодія з API GCP | `npx -y @google-cloud/gcloud-mcp` |
| Prometheus | Прямі запити до метрик | Спільнота: awesome-mcp-servers |
| Terraform | Аналіз стану та планів | Спільнота: awesome-mcp-servers |

Жоден із цих серверів не створений Anthropic: сервер Kubernetes підтримує [організація containers](https://github.com/containers/kubernetes-mcp-server) (Red Hat), сервер AWS підтримує [AWS Labs](https://github.com/awslabs/mcp), а сервер GCP підтримує [Google](https://github.com/googleapis/gcloud-mcp).

**Розташування файлу конфігурації**: `~/.claude.json` (ключ `"mcpServers"`)

```json
{
  "mcpServers": {
    "kubernetes": {
      "command": "npx",
      "args": ["-y", "kubernetes-mcp-server@latest"]
    }
  }
}
```

## Зовнішні ресурси

### Корисні списки (Awesome Lists)

- **[awesome-claude-code-subagents](https://github.com/VoltAgent/awesome-claude-code-subagents)** (23.8K зірок, перевірено 2026-07-27, було 8.1k): Корисні інструменти та профілі агентів, включаючи SRE.
- **[awesome-claude-skills](https://github.com/travisvn/awesome-claude-skills)** (14.4K зірок, перевірено 2026-07-27, було 4.6k): Готові скіли, у тому числі для роботи з інфраструктурою.

### Офіційні репозиторії

- **[terraform-skill](https://github.com/antonbabenko/terraform-skill)**: Професійний скіл Terraform від Антона Бабенка.
- **[Claude Code Docs](https://code.claude.com/docs)**: Офіційна документація розробника.

### Спільнота

- **Anthropic Discord**: Канал `#claude-code`.
- **Reddit**: Спільнота `r/ClaudeAI`.
- **GitHub**: Відкривайте issues або пропонуйте свої покращення.

---

## Дивіться також

- **[Шаблон агента](https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/examples/agents/devops-sre.md)**: Налаштування персонажу DevOps/SRE для Claude.
- **[CLAUDE.md для DevOps](https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/examples/claude-md/devops-sre.md)**: Специфічний шаблон конфігурації проекту для DevOps-команд.
- **[Гайд з посилення безпеки](../security/security-hardening.uk.md)**: Додаткові інструкції з безпеки.
- **[Гайд з архітектури](../core/architecture.uk.md)**: Як влаштовані внутрішні процеси Claude Code.

---
**Локалізація**: [Serhii (MacPlus Software)](https://macplus-software.com)
*Остання синхронізація: Травень 2026*
