# Заплановий пошук публічних згадок

Використовуйте цей промпт для щотижневого Scheduled Search у Perplexity. Пошук призначений лише для виявлення: локальний skill `source-command-track-mentions` пізніше перевіряє кандидатів, прибирає дублікати й застосовує схвалені.

## Запланований промпт

```text
Search the public web for third-party references to Florian Bruniaux's active public projects,
especially Claude Code Ultimate Guide, Claude Cowork Guide, StarMapper, CCBoard,
CC-Copilot Bridge, ctxharness, Dep Scope, flow-lean, Google Search Console MCP,
Claude Code Plugins, CC-Sessions, cc-skill-usage, YouTube Video Insights,
AgentSec Triage, and GitHub Roast TPC.

Search articles, newsletters, podcasts, YouTube, Reddit, Hacker News, LinkedIn, X,
GitHub repositories and discussions, package or MCP registries, automated directories,
translations, adaptations, and mirrors. Search broadly on every run because pages may be
indexed late. Exclude Florian Bruniaux's own sites, repositories, and social posts from
third-party totals.

Confirm a result only when the page, public metadata, or indexed snippet contains an explicit
project name, canonical repository slug, or official domain. A generic title such as
"ultimate Claude Code guide" is not evidence.

Return exactly three sections:
1. new_confirmed
2. already_tracked
3. rejected_or_unverified

For every result return: canonical URL, title, author, platform, publication date when available,
language, project, identifier found, evidence location, classification, confidence, metadata
problems, and one sentence describing the reference.

Classifications: editorial, social, forum, translation, mirror, adoption, registry,
automated_directory.

Do not treat directory counters, token counts, trust scores, saves, or repository stars as
audience measurements. Flag stale install commands, package names, content counts, authorship,
or capabilities. Do not modify a repository or publish a result.
```

## Контракт перевірки

1. Експортуйте або вставте результат запланованого пошуку в завдання посібника.
2. Запустіть `/track-mentions --dry-run` для `mentions.yaml` і `review-queue.yaml`.
3. Незалежно перевірте кожен URL із `new_confirmed`.
4. Недоступних кандидатів додайте до черги перевірки.
5. Відхиляйте збіги за назвою та власні ресурси автора.
6. Застосовуйте лише ті записи, які користувач явно схвалив.
7. Запустіть `python3 scripts/check-media-mentions.py`.
8. Робіть коміт лише тоді, коли було запитано `/track-mentions --commit`.

Заплановий пошук ніколи не є джерелом істини. Ним є `mentions.yaml` і каталог портфоліо.
