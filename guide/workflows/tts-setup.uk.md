---
title: "Робочий процес налаштування TTS — встановлення Agent Vibes"
description: "Додавання голосового озвучення тексту (text-to-speech) для Claude Code на macOS"
tags: [workflow, tts, tutorial]
---

# Робочий процес налаштування TTS — встановлення Agent Vibes

**Мета**: Додати голосове озвучення тексту (TTS) для Claude Code
**Час**: 18 хвилин
**Складність**: Середня
**Система**: macOS (потрібен Homebrew)

---

## Точка прийняття рішення: Чи варто встановлювати TTS?

Скористайтеся цим швидким тестом для оцінки:

| Запитання | Відповідь | Бали |
|----------|--------|-------|
| Чи робите ви тривалі перегляди коду (code reviews)? | Так | +2 |
| Чи виконуєте ви інші завдання під час налагодження (debugging)? | Так | +2 |
| Чи віддаєте ви перевагу звуковим сповіщенням? | Так | +1 |
| Чи потрібен вам офлайн-режим TTS (без хмари)? | Так | +2 |
| Чи критична для вас затримка (<100мс)? | Так | -2 |
| Чи працюєте ви в публічних місцях (без звуку)? | Так | -3 |
| Чи віддаєте ви перевагу тиші під час роботи? | Так | -2 |

**Результат**:
- **≥3**: Встановлюйте TTS (ідеально підходить)
- **0-2**: Опціонально (спробуйте, за потреби можна видалити)
- **<0**: Пропустіть TTS (не підходить)

---

## Огляд робочого процесу

```
Фаза 1: Необхідні умови (5 хв)
    ↓
Фаза 2: Встановлення Agent Vibes (5 хв)
    ↓
Фаза 3: Piper TTS + голоси (5 хв)
    ↓
Фаза 4: Тестування та налаштування (3 хв)
    ↓
Фаза 5: Верифікація (1 хв)
```

---

## Фаза 1: Необхідні умови (5 хвилин)

### Контрольна точка 1.1: Системні вимоги

```bash
# Перевірка версії macOS
sw_vers
# Вимога: macOS 10.15+

# Перевірка Homebrew
brew --version
# Якщо відсутній: /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Перевірка Node.js
node --version
# Вимога: 16.0.0+
```

### Контрольна точка 1.2: Встановлення Bash 5.x

```bash
# Встановлення
brew install bash

# Перевірка
/opt/homebrew/bin/bash --version
# Очікується: GNU bash, версія 5.x

# ✅ Контрольна точка: Bash 5.x встановлено
```

### Контрольна точка 1.3: Встановлення залежностей

```bash
# Встановлення аудіо-утиліт
brew install sox ffmpeg util-linux espeak-ng

# Перевірка встановлення всіх залежностей
command -v sox && command -v ffmpeg && command -v espeak-ng && echo "✅ Dependencies OK"

# ✅ Контрольна точка: залежності встановлено
```

**Загальний час Фази 1**: ~5 хвилин

---

## Фаза 2: Встановлення Agent Vibes (5 хвилин)

### Крок 2.1: Запуск інсталятора

```bash
# Перейдіть до вашого проекту
cd /path/to/your/claude-project

# Запустіть інтерактивний інсталятор
npx agentvibes install
```

**Очікується**: відображення ASCII-банера + 4-сторінковий інтерактивний інсталятор.

### Крок 2.2: Проходження сторінок інсталятора

**Сторінка 1/4 — Залежності**:
- Огляд: має відображатися зелена галочка ✓ для всіх пунктів
- Дія: натисніть "Next →"

**Сторінка 2/4 — Провайдер**:
- **Оберіть**: `Piper TTS` (найкраща якість, робота в офлайні)
- Дія: натисніть "Next →"

**Сторінка 3/4 — Голос**:
- **Французька**: оберіть `fr_FR-tom-medium` (чоловічий, професійний)
- **Англійська**: оберіть `en_US-ryan-high` (найвища якість)
- Дія: натисніть "Next →"

**Сторінка 4/4 — Налаштування**:
- **Реверберація**: `Light` (рекомендовано)
- **Фонова музика**: `Disabled` (щоб не відволікати)
- **Деталізація (Verbosity)**: `Low` (менше розмов)
- Дія: натисніть "Start Installation"

### Контрольна точка 2.3: Перевірка встановлення

```bash
# Перевірка встановлених файлів
ls .claude/hooks/play-tts.sh
ls .claude/commands/agent-vibes/
cat .claude/tts-provider.txt
# Очікується: файли існують, провайдер показує "macos" або "piper"

# ✅ Контрольна точка: Agent Vibes встановлено
```

**Загальний час Фази 2**: ~5 хвилин

---

## Фаза 3: Piper TTS + французькі голоси (5 хвилин)

### Крок 3.1: Встановлення Piper через pipx

```bash
# Встановлення Piper TTS
pipx install piper-tts

# Перевірка
piper --help
# Очікується: інструкції з використання Piper

# ✅ Контрольна точка: Piper встановлено
```

### Крок 3.2: Завантаження французьких голосів

```bash
# Створення каталогу для голосів
mkdir -p ~/.claude/piper-voices
cd ~/.claude/piper-voices

# Завантаження французького чоловічого голосу (рекомендовано)
curl -L -o fr_FR-tom-medium.onnx \
  "https://huggingface.co/rhasspy/piper-voices/resolve/main/fr/fr_FR/tom/medium/fr_FR-tom-medium.onnx"
curl -L -o fr_FR-tom-medium.onnx.json \
  "https://huggingface.co/rhasspy/piper-voices/resolve/main/fr/fr_FR/tom/medium/fr_FR-tom-medium.onnx.json"

# Завантаження французького жіночого голосу (опціонально)
curl -L -o fr_FR-siwis-medium.onnx \
  "https://huggingface.co/rhasspy/piper-voices/resolve/main/fr/fr_FR/siwis/medium/fr_FR-siwis-medium.onnx"
curl -L -o fr_FR-siwis-medium.onnx.json \
  "https://huggingface.co/rhasspy/piper-voices/resolve/main/fr/fr_FR/siwis/medium/fr_FR-siwis-medium.onnx.json"

# ✅ Контрольна точка: голоси завантажено (~120MB)
```

**Загальний час Фази 3**: ~5 хвилин

---

## Фаза 4: Конфігурація та тестування (3 хвилини)

### Крок 4.1: Налаштування провайдера та голосу

```bash
# Встановлення Piper як провайдера
echo "piper" > .claude/tts-provider.txt

# Встановлення французького чоловічого голосу
echo "fr_FR-tom-medium" > .claude/tts-voice.txt

# Перевірка конфігурації
cat .claude/tts-provider.txt  # Очікується: piper
cat .claude/tts-voice.txt     # Очікується: fr_FR-tom-medium

# ✅ Контрольна точка: налаштування збережено
```

### Крок 4.2: Тестування аудіо-потоку

```bash
# Безпосередній тест Piper
echo "Bonjour, je suis Claude et je parle français" | \
  piper -m ~/.claude/piper-voices/fr_FR-tom-medium.onnx \
  --output-file /tmp/test-fr.wav && afplay /tmp/test-fr.wav

# Тест хука TTS
~/.claude/hooks/play-tts.sh "Ceci est un test audio"

# ✅ Контрольна точка: звук працює
```

**Очікується**: ви почуєте французький чоловічий голос.

**Загальний час Фази 4**: ~3 хвилини

---

## Фаза 5: Верифікація в Claude Code (1 хвилина)

### Крок 5.1: Запуск та тестування

```bash
# Запуск Claude Code
claude

# У Claude виконайте команду:
/agent-vibes:whoami
# Очікується: відображення провайдера "piper" та голосу "fr_FR-tom-medium"

# Перевірка простого запиту
> "Dis-moi bonjour en français"
# Очікується: голосова відповідь французьким чоловічим голосом

# ✅ Контрольна точка: TTS активовано в Claude Code
```

### Крок 5.2: Налаштування вподобань

```bash
# Зменшення деталізації (рекомендовано)
/agent-vibes:verbosity low

# Приховати 34 команди, якщо вони захаращують екран
/agent-vibes:hide

# ✅ Контрольна точка: вподобання налаштовано
```

**Загальний час Фази 5**: ~1 хвилина

---

## Загальний час: ~18 хвилин ✅

---

## Рекомендації після налаштування

### Оптимізація під ваш робочий процес

**Для переглядів коду (code reviews)**:
```bash
/agent-vibes:verbosity low
/agent-vibes:effects off
```

**Для зосередженої роботи**:
```bash
/agent-vibes:mute  # Тимчасово вимкнути звук
# Робота без звукового супроводу
/agent-vibes:unmute  # Увімкнути звук після завершення
```

**Для економії заряду акумулятора**:
```bash
# Перемикання на macOS Say (миттєво, без навантаження на CPU)
/agent-vibes:provider switch macos
```

### Додавання до .gitignore

```bash
# Запобігання коміту великих аудіофайлів
echo ".claude/audio/" >> .gitignore
echo ".claude/piper-voices/" >> .gitignore
echo "*.wav" >> .gitignore
echo "*.onnx" >> .gitignore
```

---

## Швидка довідка з усунення несправностей

| Проблема | Швидке вирішення |
|-------|-----------|
| Немає звуку | Перевірте `cat .claude/tts-provider.txt` |
| Неправильний голос | Виконайте команду `/agent-vibes:switch fr_FR-tom-medium` |
| Забагато розмов | Виконайте команду `/agent-vibes:verbosity low` |
| Забагато команд на екрані | Виконайте команду `/agent-vibes:hide` |

**Повний посібник з усунення несправностей**: [Усунення несправностей Agent Vibes](../../examples/integrations/agent-vibes/troubleshooting.uk.md)

---

## Наступні кроки

- **[Каталог голосів](../../examples/integrations/agent-vibes/voice-catalog.uk.md)** — ознайомтеся з 15 доступними голосами
- **[Посібник з інтеграції](../../examples/integrations/agent-vibes/README.uk.md)** — вивчіть доступні команди
- **[Деталі встановлення](../../examples/integrations/agent-vibes/installation.uk.md)** — глибоке занурення в архітектуру

---

## Інструкції з видалення

Щоб повністю видалити Agent Vibes:

```bash
# Автоматичне видалення
npx agentvibes uninstall --yes

# Ручне очищення (за потреби)
rm -rf .claude/hooks/*vibes*
rm -rf .claude/commands/agent-vibes/
rm -rf .claude/audio/
rm -rf ~/.claude/piper-voices/
pipx uninstall piper-tts
```

---

*Посібник з робочого процесу підтримується спільнотою [Claude Code Ultimate Guide](https://github.com/FlorianBruniaux/claude-code-ultimate-guide)*
*Остання версія: 2026-01-22 | Agent Vibes v3.0.0*

---
**Локалізація**: [Serhii (MacPlus Software)](https://macplus-software.com)
*Остання синхронізація: Травень 2026*
