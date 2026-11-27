---
name: "source-command-sync"
description: "Перевірити стан синхронізації посібника та лендингу"
---

# source-command-sync

Використовуй цей skill, коли користувач просить виконати мігровану вихідну команду `sync`.

## Command Template

# Перевірка синхронізації

Виконай комплексну перевірку синхронізації між репозиторієм посібника та сайтом лендингу.

## Що перевіряти

Виконай `./scripts/check-landing-sync.sh` і покажи результати з покращеним форматуванням.

## Формат виводу

```
🔄 Guide ↔ Landing Synchronization Check

═══════════════════════════════════════════════════════════

1️⃣ Guide Version
   Guide:   3.9.11
   Landing: 3.9.11
   Status:  ✅ Synchronized

2️⃣ Templates Count
   Guide Files:      65
   Landing (index):  65
   Landing (examples): 65
   Status:  ✅ Synchronized

3️⃣ Quiz Questions
   Source (JSON):     227
   Landing (index):   227
   Landing (quiz):    227
   Status:  ✅ Synchronized

4️⃣ Guide Lines
   Actual Count:      11,560
   Landing Display:   11,000+ (approximate)
   Status:  ✅ Within Tolerance

5️⃣ Codex Version
   Releases YAML:     v2.1.14
   Landing Badge:     v2.1.14
   Status:  ✅ Synchronized

═══════════════════════════════════════════════════════════

✅ All Components Synchronized

No action required. Guide and landing site are in sync.
```

## Якщо виявлено розбіжності

```
🔄 Guide ↔ Landing Synchronization Check

═══════════════════════════════════════════════════════════

1️⃣ Guide Version
   [... as above ...]

2️⃣ Templates Count
   Guide Files:      65
   Landing (index):  63
   Landing (examples): 65
   Status:  ⚠️ MISMATCH

3️⃣ Quiz Questions
   [... etc ...]

═══════════════════════════════════════════════════════════

❌ Synchronization Issues Detected (1 issue)

Issues to Fix:

1. Templates Count Mismatch
   Location: Codex-ultimate-guide-landing/index.html
   Current:  63
   Expected: 65
   Action:   Update badge and meta tags with correct count

Quick Fixes:
   # Update landing templates count
   cd /Users/florianbruniaux/Sites/perso/Codex-ultimate-guide-landing
   # Edit index.html lines: 6, 9, 188, 204, 455
   # Change "63 templates" → "65 templates"
   git add index.html
   git commit -m "fix: sync templates count (63 → 65)"
   git push

Recommended:
   Run /update-infos-release to automate synchronization
```

## Реалізація

1. Виконати скрипт перевірки синхронізації
2. Зафіксувати вивід і розібрати коди статусів
3. Відформатувати результати з чіткою візуальною ієрархією
4. Якщо виявлено проблеми:
   - Перелічити кожну розбіжність
   - Вказати розташування файлів
   - Запропонувати точні виправлення
   - Порекомендувати команди автоматизації
5. Позначити індикатори статусу кольорами
6. Додати практичні наступні кроки

## Пов'язані команди

- `/update-infos-release` - Автоматизована синхронізація + керування версіями
- `/version` - Переглянути поточні версії
- `/changelog` - Переглянути останні записи CHANGELOG
