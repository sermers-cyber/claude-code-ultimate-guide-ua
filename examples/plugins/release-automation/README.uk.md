# Плагін Release automation

Семантичне версіонування, генерація changelog і керування релізами.

## Встановлення

```bash
bash install.sh
```

## Компоненти

- **Команда /release**: підвищення семантичної версії та створення тегів
- **Команда /changelog**: генерація release notes із комітів
- **Skill release-notes-generator**: автоматизована документація релізів
- **Hook version-sync**: підтримує узгоджену версію в усіх файлах

## Швидкий старт

```bash
# Bump version and create release
/release patch      # v1.0.0 → v1.0.1
/release minor      # v1.0.1 → v1.1.0
/release major      # v1.1.0 → v2.0.0

# Generate changelog
/changelog 10       # Last 10 releases

# The hook auto-syncs VERSION across docs
```

## Можливості

✓ Семантичне версіонування
✓ Автоматизований changelog
✓ Git-теги
✓ Release notes
✓ Узгодженість версій

---

Про керування версіями дивіться `guide/workflows/releases-tracking.md`.
