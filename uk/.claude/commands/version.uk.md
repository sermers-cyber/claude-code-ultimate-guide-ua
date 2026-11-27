---
name: version
description: Показати поточні версії посібника та Claude Code
---

# Інформація про версії

Показати поточну інформацію про версію посібника та відстежувану версію Claude Code.

## Що показувати

```
Claude Code Ultimate Guide
├─ Версія посібника:        X.Y.Z (з файлу VERSION)
├─ Відстежуваний Claude Code: vA.B.C (з claude-code-releases.yaml)
├─ Останнє оновлення CC:    YYYY-MM-DD
├─ Шаблони:                 N файлів
├─ Питання вікторини:       N питань
├─ Рядки посібника:         ~N рядків
└─ Лендінг синхронізовано:  ✅ Так / ❌ Ні

Останні оновлення посібника:
- [Дата]: Версія X.Y.Z-1 → X.Y.Z (причина)
- [Дата]: Версія X.Y.Z-2 → X.Y.Z-1 (причина)
- [Дата]: Версія X.Y.Z-3 → X.Y.Z-2 (причина)

Останні релізи Claude Code:
- vA.B.C (YYYY-MM-DD): [2-3 основні моменти]
- vA.B.C-1 (YYYY-MM-DD): [2-3 основні моменти]
- vA.B.C-2 (YYYY-MM-DD): [2-3 основні моменти]
```

## Файли для читання

1. `VERSION` - Версія посібника
2. `machine-readable/claude-code-releases.yaml` - Версія CC + дата
3. `CHANGELOG.md` - Останні 3 оновлення посібника
4. `machine-readable/claude-code-releases.yaml` - Останні 3 релізи CC
5. Виконай `find examples/ -type f ! -name README.md ! -name index.html | wc -l` - Кількість шаблонів
6. Виконай `jq '. | length' questions.json` - Кількість питань вікторини
7. Виконай `wc -l guide/ultimate-guide.md | awk '{print $1}'` - Рядки посібника
8. Виконай `./scripts/check-landing-sync.sh` - Статус синхронізації

## Формат виводу

Використовуй чисте, зручне для читання форматування з емодзі для наочності:

```
📊 Claude Code Ultimate Guide - Інформація про версії

📦 Версія посібника: 3.9.11
🔧 Claude Code: v2.1.14 (2026-01-21)

📈 Статистика вмісту:
   • Шаблони:           65 файлів
   • Питання вікторини: 227 питань
   • Рядки посібника:   ~11,560 рядків

🔄 Синхронізація з лендінгом: ✅ Синхронізовано

📝 Останні оновлення посібника:
   • 2026-01-20 - v3.9.10 → v3.9.11: Production Safety Rules
   • 2026-01-19 - v3.9.9 → v3.9.10: DevOps & SRE Guide (FIRE)
   • 2026-01-18 - v3.9.8 → v3.9.9: Documentation improvements

🚀 Останні релізи Claude Code:
   • v2.1.14 (2026-01-21)
     - History-based autocomplete in bash mode
     - Plugin search and SHA pinning
     - Context window + memory fixes

   • v2.1.12 (2026-01-18)
     - Message rendering bugfix

   • v2.1.11 (2026-01-17)
     - MCP connection optimization
```

## Реалізація

1. Прочитай усі потрібні файли
2. Виконай shell-команди для підрахунків
3. Розбери YAML для релізів CC
4. Розбери CHANGELOG для оновлень посібника
5. Відформатуй вивід із правильним вирівнюванням
6. Покажи з чіткою візуальною ієрархією
