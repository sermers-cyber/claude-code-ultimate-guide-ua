---
title: "Agent Vibes TTS - повний посібник зі встановлення"
description: "Покроковий посібник зі встановлення інтеграції синтезу мовлення Agent Vibes на macOS"
tags: [guide, tts, integration]
---

# Agent Vibes TTS - повний посібник зі встановлення

**Потрібний час**: ~18 хвилин
**Складність**: середня
**Система**: macOS (Apple Silicon або Intel)

---

## Перевірка передумов

Перш ніж почати, переконайтеся, що у вас є:

| Вимога | Команда перевірки | Мінімальна версія |
|-------------|---------------|-------------|
| **macOS** | `sw_vers` | 10.15+ |
| **Homebrew** | `brew --version` | Будь-яка свіжа |
| **Node.js** | `node --version` | 16.0.0+ |
| **Python** | `python3 --version` | 3.10.0+ |
| **Git** | `git --version` | Будь-яка свіжа |

---

## Огляд встановлення (5 етапів)

```
Phase 1: System Dependencies     (~5 min)
    ├─ Bash 5.x
    ├─ sox, ffmpeg, util-linux
    └─ espeak-ng

Phase 2: Agent Vibes Install     (~5 min)
    ├─ Interactive installer
    ├─ Provider selection (Piper)
    ├─ Voice selection
    └─ Configuration

Phase 3: Piper TTS + Voices       (~5 min)
    ├─ Piper via pipx
    ├─ Download FR voices (4)
    └─ Download EN voices (12)

Phase 4: Configuration            (~2 min)
    ├─ Set provider: piper
    ├─ Set voice: fr_FR-tom-medium
    └─ Test audio

Phase 5: Verification             (~1 min)
    ├─ Test in Claude Code
    └─ Verify hooks active
```

---

## Етап 1: системні залежності

### Крок 1.1: встановіть bash 5.x

Agent Vibes потребує Bash 5.x (macOS постачається з 3.2).

```bash
# Install Bash 5.x
brew install bash

# Verify installation
/opt/homebrew/bin/bash --version
# Expected: GNU bash, version 5.x
```

**Чому**: скрипти Agent Vibes використовують можливості Bash 5.x (асоціативні масиви тощо)

### Крок 1.2: встановіть аудіоінструменти

```bash
# Install audio processing tools
brew install sox ffmpeg util-linux

# Verify sox
sox --version

# Verify ffmpeg
ffmpeg -version

# Verify flock (from util-linux)
/opt/homebrew/opt/util-linux/bin/flock --version
```

**Примітка**: `util-linux` має статус "keg-only" (без символьних посилань), але Agent Vibes знаходить його автоматично.

### Крок 1.3: встановіть espeak-ng (залежність Piper)

```bash
# Install espeak-ng
brew install espeak-ng

# Verify installation
espeak-ng --version
```

**Чому**: Piper TTS потребує бібліотеки `libespeak-ng` для обробки фонем.

### Контрольна точка 1: залежності встановлено ✅

```bash
# Verify all dependencies
command -v /opt/homebrew/bin/bash && \
command -v sox && \
command -v ffmpeg && \
command -v espeak-ng && \
echo "✅ All dependencies installed"
```

---

## Етап 2: встановлення Agent Vibes

### Крок 2.1: запустіть інтерактивний інсталятор

```bash
# Navigate to your Claude Code project
cd /path/to/your/project

# Launch installer (interactive, 4 pages)
npx agentvibes install
```

**Очікувано**: банер в ASCII-графіці + вітальний екран

### Крок 2.2: пройдіть сторінки встановлення

**Сторінка 1/4: System Dependencies**
- Перегляньте виявлені залежності
- Усі мають показувати `✓` (зелена галочка)
- Натисніть **"Next →"**

**Сторінка 2/4: Provider Selection**
- Варіанти: `macOS Say`, `Piper TTS`, `Termux SSH`
- **Оберіть**: `Piper TTS` (найкраща якість, офлайн)
- Натисніть **"Next →"**

**Сторінка 3/4: Voice Selection**
- **Для французької**: оберіть `fr_FR-tom-medium` (чоловічий) або `fr_FR-siwis-medium` (жіночий)
- **Для англійської**: оберіть `en_US-ryan-high` (найкраща якість)
- Натисніть **"Next →"**

**Сторінка 4/4: Audio Settings**
- **Reverb**: оберіть `Light` (рекомендовано)
- **Background Music**: оберіть `Disabled` (щоб не відволікатися)
- **Verbosity**: оберіть `Low` (менше балакучості)
- Натисніть **"Start Installation"**

### Крок 2.3: хід встановлення

Agent Vibes встановить:
- 34 slash-команди
- Скрипти TTS (40 bash-скриптів)
- Шаблони особистостей
- 16 фонових музичних треків
- 7 файлів конфігурації

**Очікуваний вивід**:
```
✔ Installed 34 slash commands!
✔ Installed TTS scripts!
✔ Installed personality templates!
✔ Installed 16 background music tracks!
✔ Installed 7 config files!

✅ AgentVibes is Ready!
```

### Контрольна точка 2: Agent Vibes встановлено ✅

```bash
# Verify installation
ls -la .claude/hooks/play-tts.sh
ls -la .claude/commands/agent-vibes/
ls -la .claude/audio/tracks/

# Check provider config
cat .claude/tts-provider.txt
# Expected: "macos" or "piper"
```

---

## Етап 3: Piper TTS + голосові моделі

### Крок 3.1: встановіть Piper TTS через pipx

Якщо ви обрали провайдера Piper, Agent Vibes спробує встановити його. Якщо це не вдасться, встановіть вручну:

```bash
# Install Piper via pipx (Python package manager)
pipx install piper-tts

# Verify installation
piper --help
```

**Типова проблема**: попередньо скомпільований бінарний файл завершується з помилкою `libespeak-ng.1.dylib`.

**Рішення**: `pipx install piper-tts` працює надійно (версія на Python, а не бінарна).

### Крок 3.2: завантажте французькі голоси

```bash
# Navigate to voice storage
cd ~/.claude/piper-voices

# Download 4 French voice models
curl -L -o fr_FR-tom-medium.onnx \
  "https://huggingface.co/rhasspy/piper-voices/resolve/main/fr/fr_FR/tom/medium/fr_FR-tom-medium.onnx"
curl -L -o fr_FR-tom-medium.onnx.json \
  "https://huggingface.co/rhasspy/piper-voices/resolve/main/fr/fr_FR/tom/medium/fr_FR-tom-medium.onnx.json"

curl -L -o fr_FR-siwis-medium.onnx \
  "https://huggingface.co/rhasspy/piper-voices/resolve/main/fr/fr_FR/siwis/medium/fr_FR-siwis-medium.onnx"
curl -L -o fr_FR-siwis-medium.onnx.json \
  "https://huggingface.co/rhasspy/piper-voices/resolve/main/fr/fr_FR/siwis/medium/fr_FR-siwis-medium.onnx.json"

curl -L -o fr_FR-upmc-medium.onnx \
  "https://huggingface.co/rhasspy/piper-voices/resolve/main/fr/fr_FR/upmc/medium/fr_FR-upmc-medium.onnx"
curl -L -o fr_FR-upmc-medium.onnx.json \
  "https://huggingface.co/rhasspy/piper-voices/resolve/main/fr/fr_FR/upmc/medium/fr_FR-upmc-medium.onnx.json"

curl -L -o fr_FR-mls-medium.onnx \
  "https://huggingface.co/rhasspy/piper-voices/resolve/main/fr/fr_FR/mls/medium/fr_FR-mls-medium.onnx"
curl -L -o fr_FR-mls-medium.onnx.json \
  "https://huggingface.co/rhasspy/piper-voices/resolve/main/fr/fr_FR/mls/medium/fr_FR-mls-medium.onnx.json"
```

**Розмір**: ~60-73 МБ на голос (4 голоси = ~260 МБ загалом)

### Крок 3.3: завантажте англійські голоси (необов'язково)

Agent Vibes автоматично завантажує 12 англійських голосів під час встановлення. Перевірте:

```bash
ls ~/.claude/piper-voices/en_US-*.onnx
```

**Очікувано**: 12 файлів (ryan, amy, lessac, bryce тощо)

### Контрольна точка 3: голоси завантажено ✅

```bash
# Count voices
ls ~/.claude/piper-voices/*.onnx | wc -l
# Expected: 15+ files (12 EN + 4 FR minimum)

# Test French voice manually
echo "Bonjour, je suis Claude et je parle français" | \
  piper -m ~/.claude/piper-voices/fr_FR-tom-medium.onnx \
  --output-file /tmp/test-fr.wav && afplay /tmp/test-fr.wav
```

---

## Етап 4: конфігурація

### Крок 4.1: встановіть Piper як провайдера

```bash
# Switch to Piper TTS (if not already set)
echo "piper" > .claude/tts-provider.txt

# Verify
cat .claude/tts-provider.txt
# Expected: "piper"
```

### Крок 4.2: встановіть французький чоловічий голос

```bash
# Set default voice
echo "fr_FR-tom-medium" > .claude/tts-voice.txt

# Verify
cat .claude/tts-voice.txt
# Expected: "fr_FR-tom-medium"
```

### Крок 4.3: протестуйте генерування аудіо

```bash
# Test TTS pipeline manually
~/.claude/hooks/play-tts.sh "Ceci est un test audio"
```

**Очікувано**: аудіо відтворюється французьким чоловічим голосом.

**Усунення несправностей**: якщо звуку немає, див. [посібник з усунення несправностей](./troubleshooting.uk.md#проблема-1-немає-звуку).

### Контрольна точка 4: конфігурацію завершено ✅

```bash
# Verify config files
test -f .claude/tts-provider.txt && \
test -f .claude/tts-voice.txt && \
test -f .claude/hooks/play-tts.sh && \
echo "✅ Configuration complete"
```

---

## Етап 5: перевірка в Claude Code

### Крок 5.1: запустіть Claude Code

```bash
# Start Claude Code session
claude
```

### Крок 5.2: протестуйте команди TTS

```bash
# In Claude, run:
/agent-vibes:whoami
# Expected: Shows current voice and provider

/agent-vibes:list
# Expected: Lists all 15+ voices

# Test TTS with simple request
> "Dis-moi bonjour en français"
# Expected: Audio response in French
```

### Крок 5.3: перевірте, що hooks активні

```bash
# Exit Claude, check hook was triggered
ls -la /tmp/tts-*.wav
# Expected: Temporary audio files

# Check last played audio
ls -la ~/.claude/tts-last-played.wav
# Expected: File exists
```

### Контрольна точка 5: перевірку завершено ✅

```bash
# Final verification
cat .claude/tts-provider.txt && \
cat .claude/tts-voice.txt && \
piper --help > /dev/null 2>&1 && \
ls ~/.claude/piper-voices/*.onnx | wc -l && \
echo "✅ Installation successful!"
```

---

## Конфігурація після встановлення

### Зменшіть детальність (рекомендовано)

```bash
# In Claude Code
/agent-vibes:verbosity low
```

**Чому**: зменшує частоту озвучування, менше відволікає.

### Приховайте 34 команди (необов'язково)

```bash
# In Claude Code
/agent-vibes:hide
```

**Чому**: розвантажує палітру команд. Використовуйте `/agent-vibes:show`, щоб показати їх знову.

### Вимкніть фонову музику

```bash
# In Claude Code
/agent-vibes:background-music off
```

**Чому**: фонова музика може відволікати під час зосередженої роботи.

### Вимкніть звук для проєкту (необов'язково)

```bash
# Mute TTS for this project only
touch .claude/agentvibes-muted
```

**Чому**: деяким проєктам звук не потрібен (наприклад, репозиторіям лише з документацією).

---

## Бенчмарки продуктивності

**Система**: M1 MacBook Pro, 16 ГБ RAM, macOS Sequoia 24.6.0

| Метрика | Piper Medium | Piper High | macOS Say |
|--------|--------------|------------|-----------|
| **Генерування аудіо** | ~200 мс | ~400 мс | Миттєво |
| **Загальна затримка** | ~280 мс | ~480 мс | ~50 мс |
| **Використання RAM** | ~50 МБ | ~70 МБ | ~10 МБ |
| **Сплеск CPU** | 80% (200 мс) | 90% (400 мс) | 5% (50 мс) |
| **Якість голосу** | ⭐️⭐️⭐️⭐️ | ⭐️⭐️⭐️⭐️⭐️ | ⭐️⭐️⭐️ |
| **Офлайн** | ✅ | ✅ | ✅ |

**Рекомендація**: Piper Medium = найкращий компроміс між якістю та швидкістю.

---

## Використання диска

| Компонент | Розмір | Розташування |
|-----------|------|----------|
| **Piper TTS** | ~5 МБ | `~/.local/pipx/venvs/piper-tts/` |
| **Голосові моделі** | ~1 ГБ | `~/.claude/piper-voices/` (15 голосів × 60 МБ) |
| **Фонова музика** | ~300 МБ | `.claude/audio/tracks/` (16 треків) |
| **Скрипти** | ~2 МБ | `.claude/hooks/` (40 bash-скриптів) |
| **Разом** | **~1.3 ГБ** | - |

**Порада щодо прибирання**: видаліть голоси, якими не користуєтеся, щоб звільнити місце.

---

## Інструкції з видалення

### Автоматичне видалення

```bash
# Uninstall Agent Vibes completely
npx agentvibes uninstall --yes
```

### Ручне прибирання

```bash
# Remove Agent Vibes files
rm -rf .claude/hooks/*vibes*
rm -rf .claude/commands/agent-vibes/
rm -rf .claude/audio/

# Remove Piper TTS
pipx uninstall piper-tts

# Remove voice models
rm -rf ~/.claude/piper-voices/

# Remove config files
rm .claude/tts-provider.txt
rm .claude/tts-voice.txt
rm .claude/agentvibes-muted 2>/dev/null
rm ~/.agentvibes-muted 2>/dev/null
```

---

## Типові проблеми під час встановлення

### Проблема 1: не знайдено `libespeak-ng.1.dylib`

**Симптом**:
```
dyld[xxx]: Library not loaded: @rpath/libespeak-ng.1.dylib
```

**Рішення**:
```bash
# Install espeak-ng
brew install espeak-ng

# Reinstall Piper via pipx (not binary)
pipx uninstall piper-tts
pipx install piper-tts
```

### Проблема 2: попередження `flock` (необов'язковий інструмент)

**Симптом**:
```
⚠ flock - TTS queue locking
```

**Вплив**: незначний. TTS працює без `flock`, але за швидкої послідовності повідомлень аудіо може накладатися.

**Рішення** (необов'язково):
```bash
# flock is in util-linux, already installed
# Add to PATH if needed
export PATH="/opt/homebrew/opt/util-linux/bin:$PATH"
```

### Проблема 3: інсталятор Agent Vibes завершує роботу

**Симптом**:
```
ExitPromptError: User force closed the prompt
```

**Причина**: інтерактивний інсталятор потребує введення від користувача (його не можна автоматизувати).

**Рішення**: запускайте `npx agentvibes install` в інтерактивному терміналі (не через скрипт).

### Проблема 4: немає звуку після встановлення

**Діагностика**:
```bash
# 1. Check mute status
ls .claude/agentvibes-muted ~/.agentvibes-muted

# 2. Check provider
cat .claude/tts-provider.txt

# 3. Test Piper manually
echo "Test" | piper -m ~/.claude/piper-voices/fr_FR-tom-medium.onnx \
  --output-file /tmp/test.wav && afplay /tmp/test.wav
```

**Рішення**: див. [посібник з усунення несправностей](./troubleshooting.uk.md).

---

## Наступні кроки

Після встановлення:

1. **[Каталог голосів](./voice-catalog.uk.md)** - перегляньте 15 голосів і оберіть улюблений
2. **[README](./README.uk.md)** - вивчіть основні команди та сценарії використання
3. **[Усунення несправностей](./troubleshooting.uk.md)** - розв'язуйте типові проблеми
4. **[Екосистема AI](../../../guide/ecosystem/ai-ecosystem.uk.md#5-голосові-інструменти-введення-wispr-flow-superwhisper)** - TTS у ширшому контексті AI

---

## Ресурси

- **Agent Vibes на GitHub**: https://github.com/paulpreibisch/AgentVibes
- **Репозиторій голосів Piper**: https://huggingface.co/rhasspy/piper-voices
- **Зразки голосів Piper**: https://rhasspy.github.io/piper-samples/
- **Вебсайт Agent Vibes**: https://agentvibes.org

---

*Посібник зі встановлення підтримує [Claude Code Ultimate Guide](https://github.com/FlorianBruniaux/claude-code-ultimate-guide)*
*Останнє оновлення: 2026-01-22 | Протестовано на: macOS Sequoia 24.6.0 (Apple Silicon)*
