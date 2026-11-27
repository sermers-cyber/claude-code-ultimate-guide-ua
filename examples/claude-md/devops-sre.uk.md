---
title: "Шаблон CLAUDE.md для DevOps/SRE"
description: "Конфігурація CLAUDE.md для інфраструктурних проєктів і SRE-воркфлоу"
tags: [claude-md, template, devops, ci-cd, observability]
---

# Шаблон CLAUDE.md для DevOps/SRE

Конфігурація CLAUDE.md, оптимізована для інфраструктурних проєктів і SRE-воркфлоу.

## Використання

Скопіюйте цей вміст у файл `CLAUDE.md` свого проєкту й налаштуйте розділи, позначені `[квадратними дужками]`.

---

## Шаблон

```markdown
# Конфігурація проєкту DevOps/SRE

## Інфраструктурний контекст

### Середовище
- Хмарний провайдер: [AWS/GCP/Azure/On-prem]
- Kubernetes: [EKS/GKE/AKS/k3s/none]
- Інструмент IaC: [Terraform/Pulumi/CloudFormation/Ansible]
- CI/CD: [GitHub Actions/GitLab CI/Jenkins/ArgoCD]

### Карта сервісів
- [service-1]: [опис, критичний шлях: так/ні]
- [service-2]: [опис, критичний шлях: так/ні]
- [database]: [PostgreSQL/MySQL/MongoDB, де розміщено]

### Схеми доступу
- Доступ до кластера: [назва контексту kubectl]
- Хмарний CLI: [назва профілю aws/gcloud/az]
- Секрети: [Vault/SSM/Secrets Manager - ніколи не розголошуй значення]

## Типові налаштування фреймворку FIRE

Використовуй фреймворк FIRE для всіх інфраструктурних проблем:
- **F**irst Response (перша реакція): з'ясуй симптом, вплив, нещодавні зміни
- **I**nvestigate (розслідування): систематична діагностика з доказами
- **R**emediate (усунення): запропонуй варіанти, дочекайся схвалення
- **E**valuate (оцінювання): склади postmortem, заходи запобігання

## Правила безпеки

### Ніколи не виконуй без схвалення
- `kubectl delete` або `kubectl scale down`
- `terraform destroy`
- Будь-які записи в продакшн-базу даних
- Зміни IAM/security group
- Будь-яку команду в продакшн-namespace

### Завжди вимагай
- План відкату перед змінами
- Підтвердження середовища (prod чи staging)
- Оцінку впливу для операцій масштабування

## Вподобання щодо відповідей

### Для інцидентів
- Починай з оцінки впливу
- Став пом'якшення наслідків вище за пошук першопричини (на початку)
- Давай точні команди, а не лише поради
- Додавай часові мітки до всіх дій

### Для рев'ю коду
- Зосереджуйся на: безпеці, лімітах ресурсів, ідемпотентності
- Позначай: жорстко прописані значення, відсутню обробку помилок
- Пропонуй: доповнення до моніторингу/алертингу

### Для документації
- Формат: Markdown із блоками коду
- Стиль: формат runbook (нумеровані кроки)
- Додавай: передумови, відкат, кроки перевірки

## Типові контексти

### Namespaces Kubernetes
- `production`: [критичні сервіси, потрібне схвалення]
- `staging`: [тестуй вільно]
- `monitoring`: [Prometheus, Grafana]
- `ingress`: [nginx, cert-manager]

### Workspaces/модулі Terraform
- `modules/`: [спільні інфраструктурні компоненти]
- `environments/prod/`: [продакшн, за замовчуванням лише plan]
- `environments/staging/`: [можна безпечно застосовувати apply]

### Моніторинг
- Метрики: [URL Prometheus/CloudWatch/Datadog]
- Логи: [URL ELK/CloudWatch/Loki]
- Алерти: [інтеграція PagerDuty/OpsGenie]

## Командні домовленості

### Повідомлення комітів
- Формат: [conventional commits / ваш формат]
- Приклад: `fix(k8s): increase memory limit for payment-service`

### Вимоги до PR
- [ ] Додано вивід terraform plan
- [ ] Перелічено зачеплені сервіси
- [ ] Задокументовано процедуру відкату

### Формат runbook
```
# [Назва runbook]
## Симптоми
## Передумови
## Кроки
## Перевірка
## Відкат
## Ескалація
```
```

---

## Посібник із налаштування

### Для команд, що активно використовують Kubernetes

Додайте до «Типових контекстів»:
```markdown
### Критичні pods
- `payment-api`: прямий вплив на виручку, максимум 30 с простою
- `auth-service`: блокує всі автентифіковані запити
- `api-gateway`: єдина точка входу

### Правила масштабування
- payment-api: мін. 3, макс. 10, масштабування при CPU > 70%
- auth-service: мін. 2, макс. 5, масштабування за кількістю з'єднань
```

### Для команд, що активно використовують Terraform

Додайте розділ:
```markdown
## Домовленості щодо Terraform
- State backend: [S3 bucket / GCS bucket]
- Таблиця блокувань: [назва таблиці DynamoDB]
- Реєстр модулів: [внутрішній / Terraform registry]
- Потрібні версії провайдерів: [див. versions.tf]

### Стандарти модулів
- Усі ресурси позначаються тегами: var.tags
- Іменування: {project}-{environment}-{resource}
- Outputs: завжди експортуй ARN, ID, name
```

### Для мультихмарних команд

Додайте до «Середовища»:
```markdown
### Хмарні облікові дані
- AWS: профіль `company-prod` / `company-staging`
- GCP: проєкт `company-prod-123` / `company-staging-456`
- Azure: підписка `prod-sub-id` / `staging-sub-id`

### Міжхмарні сервіси
- DNS: [AWS Route53 / Cloudflare]
- CDN: [CloudFront / Cloud CDN]
- Секрети: [HashiCorp Vault - URL]
```

---

## Інтеграція з агентами

Поєднайте цей CLAUDE.md з агентом DevOps/SRE:

```json
{
  "agents": {
    "sre": {
      "path": ".claude/agents/devops-sre.md",
      "model": "sonnet"
    }
  }
}
```

Потім викликайте так: `@sre investigate this pod crash`

---

## Див. також

- [Посібник DevOps і SRE](../../guide/ops/devops-sre.uk.md): повна документація фреймворку FIRE
- [Агент DevOps](../agents/devops-sre.uk.md): персона агента для інфраструктурних завдань
- [Посилення безпеки](../../guide/security/security-hardening.uk.md): найкращі практики безпеки
