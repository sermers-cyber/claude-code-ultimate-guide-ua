---
name: source-command-update-infos-release
description: "Оновити відстеження релізів CLI в Claude Code Ultimate Guide та, за потреби, підвищити версію посібника. Використовуй для запитів 'mets à jour le suivi des releases Claude Code dans le guide', 'synchronise la dernière version CLI avec le landing' або команди update-infos-release. Не для релізів Codex CLI, перевірки оновлень встановленого ПЗ, написання універсального changelog чи публікації без дозволу."
---

# Оновлення відстеження релізів Claude Code у посібнику

Канонічний skill: `.claude/skills/source-command-update-infos-release/`. Копію для Codex генерує `scripts/sync-release-tracking-skill.py`; редагуй канонічне джерело й перегенеровуй її.

1. Визнач корінь Claude Code Ultimate Guide та запитаний користувачем обсяг: лише відстеження CLI чи явне підвищення версії посібника. Готово, коли відомі репозиторій і вибір підвищення.
2. Прочитай повністю `.claude/commands/update-infos-release.md` від кореня посібника разом із `docs/workflows/releases-tracking.md` і `docs/workflows/landing-sync.md`. Ці файли керують робочим процесом і поділом джерел RSS. Зберігай назву продукту Claude Code та фактичні шляхи репозиторію на будь-якому хості. Готово, коли визначено поточний робочий процес і дозволені правки.
3. Виконуй лише дозволену гілку. Підготовка чи локальна перевірка не дозволяє коміт, push, публікацію пакета чи деплой; отримай будь-який бракуючий дозвіл перед такими діями. Повідом точні зміни, тести та нерозв'язані перевірки. Готово, коли результат у межах обсягу перевірено або блокувальну умову названо явно.
