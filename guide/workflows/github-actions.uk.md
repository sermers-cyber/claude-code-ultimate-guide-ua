---
title: "GitHub Actions Workflows with Claude Code"
description: "Step-by-step setup for claude-code-action in GitHub Actions: PR code review on mention, automatic review on push, issue triage. Includes permissions config and real YAML examples."
tags: [workflow, ci-cd, github-actions, automation]
---

# GitHub Actions workflows з Claude Code

> **Confidence**: Tier 1, офіційний Anthropic action (`anthropics/claude-code-action`, 8.5K зірок станом на 2026-07-27, було 6.2k, v1.0).

Автоматизуйте рев'ю коду, сортування ішью та гейти якості, підключивши Claude безпосередньо до вашого GitHub-пайплайну. Дві моделі тригерів: згадки `@claude` (ініційовані людиною) та заплановані/подієві автоматизації (повністю автономні).

---

## Table of contents

1. [TL;DR](#tldr)
2. [Two models](#two-models)
3. [Setup](#setup)
4. [Pattern 1: PR code review on @claude mention](#pattern-1-pr-code-review-on-claude-mention)
5. [Pattern 2: Automatic PR review on push](#pattern-2-automatic-pr-review-on-push)
6. [Pattern 3: Issue triage and labeling](#pattern-3-issue-triage-and-labeling)
7. [Pattern 4: Security-Focused review](#pattern-4-security-focused-review)
8. [Pattern 5: Scheduled repo maintenance](#pattern-5-scheduled-repo-maintenance)
9. [Authentication alternatives](#authentication-alternatives)
10. [Cost control](#cost-control)
11. [Security checklist](#security-checklist)
12. [See also](#see-also)

---

## TL;DR

```yaml
# Minimal working example — paste into .github/workflows/claude.yml
name: Claude Code Review
on:
  issue_comment:
    types: [created]

jobs:
  claude:
    if: contains(github.event.comment.body, '@claude')
    runs-on: ubuntu-latest
    permissions:
      contents: write
      pull-requests: write
      issues: write
    steps:
      - uses: anthropics/claude-code-action@v1
        with:
          anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}
```

Прокоментуйте `@claude review this PR` у будь-якому PR → Claude прочитає diff та опублікує рев'ю.

---

## Two models

| Model | Trigger | Use case |
|-------|---------|----------|
| **Interactive** | `@claude` mention in PR/issue comment | On-demand reviews, questions, fixes |
| **Automated** | Push, PR open, schedule, label | Continuous quality gates, triage |

Обидві моделі використовують один і той самий action: різниця полягає у блоці `on:` та у наявності умови `if:`.

---

## Setup

### Quickstart (30 seconds)

У вашому терміналі Claude Code всередині будь-якого проєкту, підключеного до GitHub-репозиторію:

```
/install-github-app
```

Це допоможе вам створити GitHub App, додати `ANTHROPIC_API_KEY` до секретів вашого репозиторію та згенерувати базовий воркфлоу `claude.yml`.

### Manual setup

1. Додайте `ANTHROPIC_API_KEY` до секретів вашого GitHub-репозиторію
2. Створіть `.github/workflows/claude.yml` (див. патерни нижче)
3. Надайте воркфлоу необхідні дозволи: `contents: write`, `pull-requests: write`, `issues: write`

---

## Pattern 1: PR code review on @claude mention

Ініційовано людиною. Розробник залишає коментар `@claude review this PR`, і Claude відповідає безпосередньо в обговоренні.

```yaml
# .github/workflows/claude-review.yml
name: Claude Interactive Review
on:
  issue_comment:
    types: [created, edited]
  pull_request_review_comment:
    types: [created]

jobs:
  claude:
    if: |
      contains(github.event.comment.body, '@claude') ||
      contains(github.event.review_comment.body, '@claude')
    runs-on: ubuntu-latest
    permissions:
      contents: write
      pull-requests: write
      issues: write
    steps:
      - uses: anthropics/claude-code-action@v1
        with:
          anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}
          claude_env: |
            GITHUB_TOKEN=${{ secrets.GITHUB_TOKEN }}
```

**Приклади використання:**
- `@claude review this PR` : повний аналіз diff з пропозиціями
- `@claude is this change backwards compatible?` : точкове запитання
- `@claude fix the failing test in src/auth.test.ts` : Claude відкриває наступний PR із виправленням

---

## Pattern 2: Automatic PR review on push

Кожен PR отримує рев'ю в момент відкриття або оновлення. Згадка не потрібна.

```yaml
# .github/workflows/claude-auto-review.yml
name: Claude Auto PR Review
on:
  pull_request:
    types: [opened, synchronize]
    # Optional: only trigger on specific paths
    # paths:
    #   - 'src/**'
    #   - '!**/*.md'

jobs:
  claude-review:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      pull-requests: write
    steps:
      - uses: anthropics/claude-code-action@v1
        with:
          anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}
          prompt: |
            Review this pull request. Focus on:
            - Logic errors and edge cases
            - Security issues (injection, auth, secrets)
            - Performance regressions
            - Missing error handling

            Format your response as:
            ## Summary
            One paragraph describing the change.

            ## Issues Found
            Numbered list, severity (Critical/Major/Minor), file:line reference.

            ## Suggestions
            Optional improvements.

            Keep it under 400 words. Be direct.
```

**Порада**: Додайте `paths:`, щоб уникнути тригерів на PR, які змінюють лише документацію, або `if: github.event.pull_request.draft == false`, щоб пропускати чернетки PR.

---

## Pattern 3: Issue triage and labeling

Claude читає нові ішью, призначає лейбли та додає структурований коментар сортування.

```yaml
# .github/workflows/claude-triage.yml
name: Issue Triage
on:
  issues:
    types: [opened]

jobs:
  triage:
    runs-on: ubuntu-latest
    permissions:
      issues: write
      contents: read
    steps:
      - uses: anthropics/claude-code-action@v1
        with:
          anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}
          prompt: |
            Triage this GitHub issue:

            1. Assign one label from: bug, enhancement, question, documentation, performance, security
            2. Assign a priority label: priority:critical, priority:high, priority:medium, priority:low
            3. Post a comment with:
               - Issue type classification
               - Which component is likely affected (based on the issue description)
               - Next step recommendation for the reporter (reproduce steps needed? version info missing?)

            Be brief. One sentence per point.
```

---

## Pattern 4: Security-Focused review

Запускається спеціально для PR, що зачіпають чутливі шляхи (auth, payments, config).

```yaml
# .github/workflows/claude-security.yml
name: Security Review
on:
  pull_request:
    paths:
      - 'src/auth/**'
      - 'src/payments/**'
      - '**/config/**'
      - '**/.env*'
      - '**/secrets/**'

jobs:
  security-review:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      pull-requests: write
    steps:
      - uses: anthropics/claude-code-action@v1
        with:
          anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}
          prompt: |
            Perform a security-focused review of this PR. Check for:

            - Injection vulnerabilities (SQL, command, LDAP)
            - Authentication and authorization bypasses
            - Secrets or credentials in code or comments
            - Insecure direct object references
            - Missing input validation
            - Unsafe deserialization
            - OWASP Top 10 patterns

            Rate overall risk: Low / Medium / High / Critical.
            If High or Critical, add the label 'security-review-required'.
            List each finding with: file:line, vulnerability type, and recommended fix.
```

---

## Pattern 5: Scheduled repo maintenance

Щотижнева перевірка стану: запускається без жодного тригера від людини.

```yaml
# .github/workflows/claude-maintenance.yml
name: Weekly Repo Health Check
on:
  schedule:
    - cron: '0 9 * * 1'  # Every Monday at 9am UTC
  workflow_dispatch:       # Also allows manual trigger

jobs:
  maintenance:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      issues: write
    steps:
      - uses: actions/checkout@v4

      - uses: anthropics/claude-code-action@v1
        with:
          anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}
          prompt: |
            Perform a weekly repository health check:

            1. Scan package.json (or equivalent) for outdated major dependencies
            2. Check for TODO/FIXME comments older than 30 days in src/
            3. Identify any test files without corresponding implementation files
            4. List any documentation files that reference deleted or renamed files

            Open a GitHub issue titled "Weekly Health Check - [date]" with your findings.
            If nothing requires attention, post a comment "Health check passed — no issues found."
```

---

## Authentication alternatives

Наведені вище приклади використовують `ANTHROPIC_API_KEY` безпосередньо. Для команд, які використовують хмарних провайдерів:

**Amazon Bedrock:**
```yaml
- uses: anthropics/claude-code-action@v1
  with:
    use_bedrock: 'true'
  env:
    AWS_ACCESS_KEY_ID: ${{ secrets.AWS_ACCESS_KEY_ID }}
    AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
    AWS_REGION: us-east-1
    ANTHROPIC_MODEL: 'anthropic.claude-3-5-sonnet-20241022-v2:0'
```

**Google Vertex AI:**
```yaml
- uses: anthropics/claude-code-action@v1
  with:
    use_vertex: 'true'
  env:
    ANTHROPIC_VERTEX_PROJECT_ID: ${{ secrets.GCP_PROJECT_ID }}
    CLOUD_ML_REGION: us-east5
    ANTHROPIC_MODEL: 'claude-3-5-sonnet-v2@20241022'
```

Використання хмарних провайдерів дає переваги у відповідності до вимог розміщення даних (data residency) та дозволяє використовувати існуючі політики IAM замість керування окремим API-ключем.

---

## Cost control

Автоматизовані воркфлоу запускаються без участі людини: встановлюйте явні обмеження.

```yaml
- uses: anthropics/claude-code-action@v1
  with:
    anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}
    # Cap spend per workflow run
    claude_args: '--max-budget-usd 0.50'
    # Use Haiku for triage, Sonnet for reviews — don't default to Opus
    prompt: |
      ...
```

**Рекомендації щодо бюджету за патернами:**

| Pattern | Model | Approx. cost / run |
|---------|-------|--------------------|
| PR review (medium PR) | Sonnet | $0.05–0.15 |
| Issue triage | Haiku | $0.01–0.03 |
| Security review (large PR) | Sonnet | $0.10–0.25 |
| Scheduled maintenance | Sonnet | $0.05–0.20 |

Відстежуйте фактичні витрати за допомогою `ccusage` або панелі використання в Anthropic Console.

**Запобігання неконтрольованим витратам:**
- Використовуйте фільтри `paths:`, щоб не запускати Claude для невідповідних змін
- Додайте `if: github.event.pull_request.draft == false`, щоб пропускати чернетки PR
- Встановіть `concurrency:` для запобігання паралельним запускам на одному PR

```yaml
jobs:
  claude-review:
    concurrency:
      group: claude-${{ github.event.pull_request.number }}
      cancel-in-progress: true
```

---

## Security checklist

Перед розгортанням у репозиторії команди переконайтеся:

- [ ] `ANTHROPIC_API_KEY` збережено як секрет GitHub, а не у воркфлоу YAML
- [ ] Дозволи воркфлоу є мінімально необхідними: використовуйте `contents: read`, якщо запис не потрібен
- [ ] Для публічних репозиторіїв: додайте `if: github.event.pull_request.head.repo.full_name == github.repository`, щоб запобігти викликам API з PR від форків
- [ ] Перевіряйте, що саме воркфлоу публікує відкрито: коментарі Claude видно всім учасникам
- [ ] Використовуйте `pull_request_target` з обережністю: він запускається з правами на запис навіть для форків

**Патерн безпеки форків (для публічних репозиторіїв):**
```yaml
jobs:
  claude:
    # Only run on PRs from the same repo, not forks
    if: github.event.pull_request.head.repo.full_name == github.repository
```

---

## See also

- [AI Design Patterns: Pipes and Filters](../core/ai-design-patterns.uk.md#pipes-and-filters): `claude -p` як один фільтр у shell- або CI-пайплайні
- [Monitor, Channels and Safe Delegation to Codex](./monitor-event-delegation.uk.md): безпечний патерн Codex із розділенням на окремі job і чому hosted runner відокремлений від локального Monitor

- [Section 9.3 CI/CD Integration](#93-cicd-integration): headless-режим, Unix-пайпінг, `--output-format json`
- [Production Safety](../security/production-safety.uk.md): обмеження для автоматизованих агентів
- [Security Hardening](../security/security-hardening.uk.md): безпека MCP та вебхуків
- [Official action docs](https://github.com/anthropics/claude-code-action): інструкція з вирішення проблем, міграція, хмарні провайдери
- [Community workflow blueprint](https://github.com/alirezarezvani/claude-code-github-workflow): 8 воркфлоу + 4 автономні агенти для просунутих команд

---
**Локалізація**: [Serhii (MacPlus Software)](https://macplus-software.com)
*Остання синхронізація: Травень 2026*
