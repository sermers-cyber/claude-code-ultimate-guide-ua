---
name: source-command-update-infos-release
description: "Оновити відстеження релізів CLI в Claude Code Ultimate Guide і, за потреби, підняти версію посібника. Використовуй для 'mets à jour le suivi des releases Claude Code dans le guide', 'synchronise la dernière version CLI avec le landing' або команди update-infos-release. Не для релізів Codex CLI, перевірки оновлень встановленого ПЗ, написання загального changelog чи публікації без дозволу."
---

# Оновлення відстеження релізів Claude Code в посібнику

Канонічний skill: `.claude/skills/source-command-update-infos-release/`. Копія для Codex генерується `scripts/sync-release-tracking-skill.py`; редагуй канонічне джерело й перегенеруй її.

1. Визнач корінь Claude Code Ultimate Guide і запитаний користувачем обсяг: лише відстеження CLI або явне підвищення версії посібника. Готово, коли відомі репозиторій і вибір щодо підвищення версії.
2. Прочитай повністю `.claude/commands/update-infos-release.md` із кореня посібника разом із `docs/workflows/releases-tracking.md` і `docs/workflows/landing-sync.md`. Ці файли керують воркфлоу та поділом джерел RSS. Збережи назву продукту Claude Code і фактичні шляхи репозиторію на обох хостах. Готово, коли визначено поточний воркфлоу й дозволені правки.
3. Виконай лише авторизовану гілку. Підготовка чи локальна перевірка не дає права на коміт, push, публікацію пакета чи розгортання; отримай бракуючий дозвіл до цих дій. Повідом точні зміни, тести та неперевірені пункти. Готово, коли результат у межах обсягу перевірено або явно названо блокувальну умову.
