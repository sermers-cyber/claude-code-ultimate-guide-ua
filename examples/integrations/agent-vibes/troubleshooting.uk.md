---
title: "Agent Vibes — посібник з усунення несправностей"
description: "Кроки діагностики та рішення для поширених проблем із TTS в Agent Vibes"
tags: [guide, tts, debugging, integration]
---

# Agent Vibes — посібник з усунення несправностей

**Поширені проблеми**: 7 сценаріїв із покроковими рішеннями
**Засоби діагностики**: команди та скрипти для виявлення проблеми

---

## Проблема 1: немає звуку

### Симптом
```
Claude responds but no TTS audio plays
```

### Кроки діагностики

```bash
# 1. Check if muted
ls -la .claude/agentvibes-muted ~/.agentvibes-muted
# If file exists → TTS is muted

# 2. Check provider configuration
cat .claude/tts-provider.txt
# Expected: "piper" or "macos"

# 3. Check voice configuration
cat .claude/tts-voice.txt
# Expected: voice name like "fr_FR-tom-medium"

# 4. Test Piper directly
echo "Test audio" | piper -m ~/.claude/piper-voices/fr_FR-tom-medium.onnx \
  --output-file /tmp/test.wav && afplay /tmp/test.wav
```

### Рішення

**Якщо звук вимкнено**:
```bash
# Unmute
rm .claude/agentvibes-muted
rm ~/.agentvibes-muted 2>/dev/null

# Or in Claude Code
/agent-vibes:unmute
```

**Якщо провайдера налаштовано неправильно**:
```bash
# Set Piper as provider
echo "piper" > .claude/tts-provider.txt

# Verify
cat .claude/tts-provider.txt
```

**Якщо голосу бракує**:
```bash
# Download missing voice
cd ~/.claude/piper-voices
curl -L -o fr_FR-tom-medium.onnx \
  "https://huggingface.co/rhasspy/piper-voices/resolve/main/fr/fr_FR/tom/medium/fr_FR-tom-medium.onnx"
curl -L -o fr_FR-tom-medium.onnx.json \
  "https://huggingface.co/rhasspy/piper-voices/resolve/main/fr/fr_FR/tom/medium/fr_FR-tom-medium.onnx.json"
```

**Якщо команда Piper завершується з помилкою**:
```bash
# Reinstall Piper via pipx
pipx uninstall piper-tts
pipx install piper-tts

# Verify
piper --help
```

---

## Проблема 2: не знайдено libespeak-ng.1.dylib

### Симптом
```
dyld[xxx]: Library not loaded: @rpath/libespeak-ng.1.dylib
  Referenced from: /Users/.../piper
  Reason: tried: '/usr/local/lib/libespeak-ng.1.dylib' (no such file)
```

### Першопричина
Бінарному файлу Piper потрібна бібліотека `espeak-ng`, яку не встановлено.

### Рішення

```bash
# Install espeak-ng
brew install espeak-ng

# Verify installation
espeak-ng --version
# Expected: eSpeak NG text-to-speech: 1.52.0

# Find library location
find /opt/homebrew -name "libespeak-ng*.dylib"
# Expected: /opt/homebrew/lib/libespeak-ng.1.dylib

# If Piper still fails, reinstall via pipx (not binary)
pipx uninstall piper-tts 2>/dev/null
pipx install piper-tts

# Test again
piper --help
```

### Запобігання
Завжди встановлюйте `espeak-ng` **до** встановлення Piper TTS.

---

## Проблема 3: голос звучить роботизовано або неякісно

### Симптом
```
Audio plays but voice quality is poor, robotic, unnatural
```

### Діагностика

```bash
# Check which voice model is loaded
cat .claude/tts-voice.txt

# Check voice quality level
ls -lh ~/.claude/piper-voices/*.onnx | grep $(cat .claude/tts-voice.txt)
# Low quality: ~20-30MB
# Medium quality: ~50-70MB
# High quality: ~100-150MB
```

### Рішення

**Перейдіть на високоякісну модель**:
```bash
# Download high-quality French voice
cd ~/.claude/piper-voices
curl -L -o fr_FR-siwis-high.onnx \
  "https://huggingface.co/rhasspy/piper-voices/resolve/main/fr/fr_FR/siwis/high/fr_FR-siwis-high.onnx"
curl -L -o fr_FR-siwis-high.onnx.json \
  "https://huggingface.co/rhasspy/piper-voices/resolve/main/fr/fr_FR/siwis/high/fr_FR-siwis-high.onnx.json"

# Switch to high-quality voice
/agent-vibes:switch fr_FR-siwis-high
```

**Альтернатива: спробуйте інший голос**:
```bash
# Test multiple voices to find preferred one
/agent-vibes:preview

# Or test manually
for voice in fr_FR-tom-medium fr_FR-siwis-medium fr_FR-upmc-medium; do
  echo "Test voix $voice" | \
    piper -m ~/.claude/piper-voices/${voice}.onnx \
    --output-file /tmp/${voice}.wav
  afplay /tmp/${voice}.wav
  sleep 2
done
```

**Порівняння якості**:
| Якість | Розмір | Затримка | Природність |
|---------|------|---------|-------------|
| Низька | ~25MB | ~100ms | ⭐️⭐️ |
| Середня | ~60MB | ~200ms | ⭐️⭐️⭐️⭐️ |
| Висока | ~120MB | ~400ms | ⭐️⭐️⭐️⭐️⭐️ |

---

## Проблема 4: висока затримка (>500ms)

### Симптом
```
Noticeable delay between Claude response and audio playback
```

### Діагностика

```bash
# Time audio generation
time (echo "Test rapide" | \
  piper -m ~/.claude/piper-voices/fr_FR-tom-medium.onnx \
  --output-file /tmp/test.wav > /dev/null 2>&1)
# Expected: ~0.2s for medium quality

# Check if effects are enabled
cat .claude/config/audio-effects.cfg 2>/dev/null
# Look for REVERB_ENABLED=true, ECHO_ENABLED=true

# Check if background music enabled
cat .claude/config/background-music.cfg 2>/dev/null
# Look for ENABLED=true
```

### Рішення

**Перейдіть на голос низької якості** (на 50% швидше):
```bash
cd ~/.claude/piper-voices
curl -L -o fr_FR-gilles-low.onnx \
  "https://huggingface.co/rhasspy/piper-voices/resolve/main/fr/fr_FR/gilles/low/fr_FR-gilles-low.onnx"
curl -L -o fr_FR-gilles-low.onnx.json \
  "https://huggingface.co/rhasspy/piper-voices/resolve/main/fr/fr_FR/gilles/low/fr_FR-gilles-low.onnx.json"

/agent-vibes:switch fr_FR-gilles-low
```

**Вимкніть аудіоефекти**:
```bash
# In Claude Code
/agent-vibes:effects off

# Or manually
echo "REVERB_ENABLED=false" > .claude/config/audio-effects.cfg
echo "ECHO_ENABLED=false" >> .claude/config/audio-effects.cfg
```

**Вимкніть фонову музику**:
```bash
# In Claude Code
/agent-vibes:background-music off

# Or manually
echo "ENABLED=false" > .claude/config/background-music.cfg
```

**Перейдіть на macOS Say** (миттєво, нижча якість):
```bash
/agent-vibes:provider switch macos
```

**Порівняння продуктивності**:
| Конфігурація | Затримка | Якість |
|---------------|---------|---------|
| Piper High + ефекти + музика | ~500ms | ⭐️⭐️⭐️⭐️⭐️ |
| Piper Medium + ефекти | ~280ms | ⭐️⭐️⭐️⭐️ |
| Piper Medium (без ефектів) | ~200ms | ⭐️⭐️⭐️⭐️ |
| Piper Low (без ефектів) | ~100ms | ⭐️⭐️ |
| macOS Say | ~50ms | ⭐️⭐️⭐️ |

---

## Проблема 5: команди Agent Vibes захаращують палітру

### Симптом
```
34 /agent-vibes:* commands clutter Claude Code command palette
```

### Рішення

```bash
# Hide all Agent Vibes commands
/agent-vibes:hide

# Commands still work, just hidden from autocomplete

# Unhide later if needed
/agent-vibes:show
```

### Альтернатива: повністю видаліть Agent Vibes

```bash
npx agentvibes uninstall --yes
```

---

## Проблема 6: звук відтворюється кілька разів (луна/повтор)

### Симптом
```
Same audio plays 2-3 times in rapid succession
```

### Першопричина
`flock` (блокування файлів) недоступний, що спричиняє стан гонитви при швидких повідомленнях.

### Діагностика

```bash
# Check if flock is available
which flock || /opt/homebrew/opt/util-linux/bin/flock --version
```

### Рішення

```bash
# Install util-linux (contains flock)
brew install util-linux

# Add flock to PATH (optional)
echo 'export PATH="/opt/homebrew/opt/util-linux/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc

# Verify
flock --version
```

### Обхідний шлях (якщо flock недоступний)
```bash
# Reduce verbosity to minimize rapid messages
/agent-vibes:verbosity low
```

---

## Проблема 7: встановлення зависає або переривається

### Симптом
```
npx agentvibes install exits with:
ExitPromptError: User force closed the prompt
```

### Першопричина
Інтерактивний інсталятор потребує введення в терміналі, його не можна автоматизувати.

### Рішення

```bash
# Ensure you're in interactive terminal (not script)
# Run directly in terminal, not via automation

npx agentvibes install

# If still fails, try without cache
npx --yes agentvibes@latest install
```

### Альтернатива: ручне встановлення

```bash
# If installer fails repeatedly, install components manually

# 1. Install Piper TTS
pipx install piper-tts

# 2. Download voices
mkdir -p ~/.claude/piper-voices
cd ~/.claude/piper-voices
# ... download voices manually (see voice-catalog.md)

# 3. Create config files
echo "piper" > .claude/tts-provider.txt
echo "fr_FR-tom-medium" > .claude/tts-voice.txt

# 4. Download Agent Vibes scripts
# (Contact maintainer or extract from npm package)
```

---

## Скрипт діагностики

Створіть комплексний скрипт діагностики:

```bash
cat > /tmp/agent-vibes-diagnostic.sh << 'EOF'
#!/bin/bash
echo "=== Agent Vibes Diagnostic ==="
echo ""

echo "1. System Dependencies"
command -v /opt/homebrew/bin/bash && echo "  ✓ Bash 5.x" || echo "  ✗ Bash 5.x missing"
command -v sox && echo "  ✓ sox" || echo "  ✗ sox missing"
command -v ffmpeg && echo "  ✓ ffmpeg" || echo "  ✗ ffmpeg missing"
command -v espeak-ng && echo "  ✓ espeak-ng" || echo "  ✗ espeak-ng missing"
command -v piper && echo "  ✓ piper" || echo "  ✗ piper missing"
echo ""

echo "2. Configuration Files"
test -f .claude/tts-provider.txt && echo "  ✓ Provider: $(cat .claude/tts-provider.txt)" || echo "  ✗ Provider not configured"
test -f .claude/tts-voice.txt && echo "  ✓ Voice: $(cat .claude/tts-voice.txt)" || echo "  ✗ Voice not configured"
test -f .claude/hooks/play-tts.sh && echo "  ✓ TTS hook installed" || echo "  ✗ TTS hook missing"
echo ""

echo "3. Mute Status"
test -f .claude/agentvibes-muted && echo "  ⚠ Project muted" || echo "  ✓ Project unmuted"
test -f ~/.agentvibes-muted && echo "  ⚠ Global muted" || echo "  ✓ Global unmuted"
echo ""

echo "4. Voice Models"
echo "  Installed voices: $(ls ~/.claude/piper-voices/*.onnx 2>/dev/null | wc -l)"
ls ~/.claude/piper-voices/*.onnx 2>/dev/null | sed 's|.*/||' | sed 's|.onnx||' | sed 's/^/    - /'
echo ""

echo "5. Audio Test"
if command -v piper > /dev/null 2>&1; then
  echo "Test" | piper -m ~/.claude/piper-voices/$(cat .claude/tts-voice.txt).onnx \
    --output-file /tmp/diagnostic-test.wav 2>&1 | grep -q "error" && \
    echo "  ✗ Audio generation failed" || echo "  ✓ Audio generation successful"
  afplay /tmp/diagnostic-test.wav 2>/dev/null && echo "  ✓ Audio playback successful" || echo "  ✗ Audio playback failed"
else
  echo "  ✗ Piper not installed, skipping test"
fi
echo ""

echo "=== End Diagnostic ==="
EOF

chmod +x /tmp/agent-vibes-diagnostic.sh

# Run diagnostic
/tmp/agent-vibes-diagnostic.sh
```

---

## Отримання допомоги

Якщо проблеми не зникають:

1. **Запустіть скрипт діагностики** (вище) і поділіться його виводом
2. **Перегляньте GitHub Issues Agent Vibes**: https://github.com/paulpreibisch/AgentVibes/issues
3. **Перегляньте посібник Claude Code**: [AI Ecosystem](../../../guide/ecosystem/ai-ecosystem.md)
4. **Перевірте логи**: `tail -f ~/.claude/tts-debug.log` (якщо файл існує)

---

## Відомі обмеження

| Обмеження | Вплив | Обхідний шлях |
|------------|--------|------------|
| Bash 3.2 (стандартний у macOS) | Скрипти не працюють | Встановіть Bash 5.x через Homebrew |
| Немає підтримки Windows | Не запускається нативно | Використовуйте WSL2 або macOS |
| flock необов'язковий | Звук може накладатися | Встановіть util-linux або зменште докладність |
| Великі файли голосів | ~1GB місця на диску | Видаліть невикористовувані голоси |
| Затримка у високій якості | ~400ms затримки | Використовуйте середню або низьку якість |

---

*Посібник з усунення несправностей підтримує [Claude Code Ultimate Guide](https://github.com/FlorianBruniaux/claude-code-ultimate-guide)*
*Останнє оновлення: 2026-01-22 | Agent Vibes v3.0.0*
