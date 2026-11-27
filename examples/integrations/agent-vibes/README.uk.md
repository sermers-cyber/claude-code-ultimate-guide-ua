---
title: "Agent Vibes TTS - синтез мовлення для Claude Code"
description: "Спільнотний MCP-сервер, що додає до Claude Code можливості синтезу мовлення"
tags: [mcp, integration, plugin]
---

# Agent Vibes TTS - синтез мовлення для Claude Code

**Статус**: спільнотний MCP-сервер (необов'язковий)
**Версія**: 3.0.0
**Мейнтейнер**: [Paul Preibisch](https://github.com/paulpreibisch/AgentVibes)
**Ліцензія**: Apache 2.0

---

## Швидка матриця рішень

Чи варто встановлювати Agent Vibes? Скористайтеся цією матрицею:

| Сценарій використання | Рекомендація | Причина |
|----------|----------------|--------|
| Рев'ю коду (слухати, займаючись іншим) | ⭐️⭐️⭐️⭐️⭐️ | Озвучування звільняє ваші очі |
| Довгі сесії налагодження | ⭐️⭐️⭐️⭐️ | Звукові сповіщення тримають вас у курсі |
| Робота, що потребує зосередженості | ⚠️ Може відволікати | Варто вимикати звук під час глибокої роботи |
| Офлайн TTS (без інтернету) | ✅ Ідеально підходить | Piper TTS працює на 100% офлайн |
| Преміальна якість голосу | ❌ Використовуйте ElevenLabs | Agent Vibes = безкоштовно, добра якість |
| Французька мова | ⭐️⭐️⭐️⭐️ | 4 французькі голоси (128 дикторів) |
| Англійська мова | ⭐️⭐️⭐️⭐️⭐️ | 12 англійських голосів (висока якість) |

---

## Огляд за 30 секунд

Agent Vibes додає **звукове озвучування** відповідей Claude Code, використовуючи:

- **15 голосів** (12 англійських, 4 французькі, зокрема 124 диктори)
- **100% безкоштовно** (Piper TTS + macOS Say)
- **100% офлайн** (без залежності від хмари)
- **Встановлення за 18 хвилин** (5 етапів із контрольними точками)
- **34 slash-команди** для керування голосом

**Встановлення**: [Повний посібник](./installation.uk.md) | [Швидкий воркфлоу](../../../guide/workflows/tts-setup.uk.md)
**Використання**: [Каталог голосів](./voice-catalog.uk.md) | [Усунення несправностей](./troubleshooting.uk.md)

---

## Як це працює

### Архітектура

```
Claude Code Response
    ↓
.claude/hooks/play-tts.sh (Router)
    ↓
[Mute Check] → Exit if muted
    ↓
[Provider Manager]
    ├─ piper   → Piper TTS (offline, neural voices)
    ├─ macos   → macOS Say (native, instant)
    └─ termux  → Android via SSH
    ↓
[Voice Processing]
    ├─ Load voice model (~60MB)
    ├─ Generate audio (~200ms)
    ├─ Apply effects (reverb, echo)
    └─ Mix background music (optional)
    ↓
[Audio Output] → afplay (macOS) / speaker
```

**Продуктивність (Mac на M1)**:
- Генерування аудіо: ~200 мс
- Загальна затримка: ~280 мс (генерування + ефекти + відтворення)
- Використання RAM: ~50 МБ
- CPU: сплеск ~80% (200 мс), потім простій

---

## Швидкий старт (5 хвилин)

### Передумови

- macOS із Homebrew
- Bash 5.x (Agent Vibes допоможе встановити)
- Node.js 16+ (для встановлення)

### Встановлення

```bash
# 1. Install Agent Vibes (interactive, 4 pages)
npx agentvibes install

# 2. Choose Piper TTS provider (recommended)
# Select: Piper > fr_FR-tom-medium > Light reverb > Low verbosity

# 3. Verify installation
ls -la .claude/hooks/play-tts.sh
ls -la ~/.claude/piper-voices/
```

**Застрягли?** Див. [повний посібник зі встановлення](./installation.uk.md) або [усунення несправностей](./troubleshooting.uk.md)

### Перший тест

```bash
# Launch Claude Code
claude

# In Claude, test TTS
/agent-vibes:whoami
/agent-vibes:list
> "Say hello in French"
```

Ви маєте почути звукове озвучування!

---

## Увімкнення та вимкнення

### Швидке вимкнення/увімкнення звуку

```bash
# In Claude Code
/agent-vibes:mute      # Mute (persists across sessions)
/agent-vibes:unmute    # Unmute

# Or manually
touch .claude/agentvibes-muted      # Project mute
touch ~/.agentvibes-muted           # Global mute
rm .claude/agentvibes-muted         # Project unmute
```

### Ієрархія вимкнення звуку

```
Priority 1: .claude/agentvibes-unmuted  (project override)
Priority 2: .claude/agentvibes-muted    (project mute)
Priority 3: ~/.agentvibes-muted         (global mute)
Priority 4: Active by default
```

**Приклад**: вимкнути звук глобально, увімкнути для конкретного проєкту:
```bash
touch ~/.agentvibes-muted                 # All projects muted
touch .claude/agentvibes-unmuted          # This project unmuted
```

### Повне видалення

```bash
# Automated uninstall
npx agentvibes uninstall --yes

# Manual cleanup (if needed)
rm -rf .claude/hooks/*vibes*
rm -rf .claude/commands/agent-vibes/
rm -rf .claude/audio/
rm -rf ~/.claude/piper-voices/
pipx uninstall piper-tts
```

---

## Основні команди

### Керування провайдерами

```bash
/agent-vibes:provider list              # List available providers
/agent-vibes:provider switch piper      # Switch to Piper TTS
/agent-vibes:provider switch macos      # Switch to macOS Say
/agent-vibes:provider info              # Current provider details
```

### Керування голосами

```bash
/agent-vibes:list                       # List all voices
/agent-vibes:list first 5               # Show first 5 voices
/agent-vibes:switch fr_FR-tom-medium    # Switch to French male voice
/agent-vibes:whoami                     # Current voice & provider
/agent-vibes:preview                    # Preview first 3 voices
/agent-vibes:sample fr_FR-tom-medium    # Test specific voice
```

### Керування аудіо

```bash
/agent-vibes:mute                       # Mute all TTS
/agent-vibes:unmute                     # Unmute TTS
/agent-vibes:replay                     # Replay last audio
/agent-vibes:replay 2                   # Replay second-to-last
/agent-vibes:verbosity low              # Speak less (recommended)
/agent-vibes:verbosity medium           # Speak more
```

### Ефекти та персоналізація

```bash
/agent-vibes:effects reverb light       # Add light reverb
/agent-vibes:effects off                # Disable all effects
/agent-vibes:background-music on        # Enable background music
/agent-vibes:background-music off       # Disable background music
/agent-vibes:personality sarcastic      # Change personality
/agent-vibes:personality professional   # Professional mode
```

### Службові команди

```bash
/agent-vibes:hide                       # Hide all 34 commands
/agent-vibes:show                       # Show commands again
/agent-vibes:version                    # Agent Vibes version
/agent-vibes:update                     # Update Agent Vibes
```

**Повний довідник команд**: доступно 34 команди. Використовуйте `/agent-vibes:hide`, якщо вони захаращують палітру команд.

---

## Короткий довідник каталогу голосів

### Французькі голоси (4 моделі, 128 дикторів)

| Голос | Стать | Якість | Диктори | Сценарій використання |
|-------|--------|---------|----------|----------|
| **fr_FR-tom-medium** | Чоловічий | Середня | 1 | ⭐️⭐️⭐️⭐️⭐️ Найкращий французький чоловічий |
| fr_FR-siwis-medium | Жіночий | Середня | 1 | Чіткий, природний |
| fr_FR-upmc-medium | Нейтральний | Середня | 1 | Універсальний |
| **fr_FR-mls-medium** | Змішаний | Середня | 124 | ⭐️⭐️⭐️⭐️⭐️ Максимальна різноманітність |

**Кілька дикторів**: `fr_FR-mls-medium` має 124 різні голоси (49 жіночих, 75 чоловічих). Використовуйте прапорець `-s 0-123`, щоб вибрати конкретного диктора.

### Англійські голоси (12 моделей)

| Голос | Стать | Якість | Характер |
|-------|--------|---------|-----------|
| **en_US-ryan-high** | Чоловічий | Висока | ⭐️⭐️⭐️⭐️⭐️ Професійний |
| en_US-amy-medium | Жіночий | Середня | Теплий, природний |
| en_US-lessac-medium | Чоловічий | Середня | Авторитетний |
| en_US-libritts-high | Змішаний | Висока | Дуже природний |
| ... | ... | ... | Ще 8 голосів |

**Повний каталог зі зразками звучання**: [Каталог голосів](./voice-catalog.uk.md)

---

## Типові сценарії використання

### 1. Слухати під час рев'ю коду

```bash
# Enable TTS with low verbosity
/agent-vibes:verbosity low

# Work on other tasks while listening to Claude's analysis
> "Review the authentication middleware for security issues"
```

### 2. Звукові сповіщення для довгих завдань

```bash
# Run long test suite, get notified when done
> "Run the full test suite and report failures"
# → Audio alert when tests complete
```

### 3. Режим вивчення мов

```bash
# Enable dual-language TTS
/agent-vibes:learn on
/agent-vibes:target es_ES
/agent-vibes:target-voice es_ES-davefx-medium

# Responses spoken in both English and Spanish
> "Explain dependency injection"
```

### 4. Власні hooks (лише помилки)

```bash
# Create selective TTS hook
cat > .claude/hooks/speak-errors-only.sh << 'EOF'
#!/opt/homebrew/bin/bash
INPUT=$(cat)
BODY=$(echo "$INPUT" | jq -r '.notification.body // empty')

# Speak only if contains "error" or "failed"
if [[ "$BODY" =~ (error|failed|Error|Failed) ]]; then
  ~/.claude/hooks/play-tts.sh "$BODY"
fi
exit 0
EOF

chmod +x .claude/hooks/speak-errors-only.sh
```

---

## Поради щодо продуктивності

### Зменшення затримки

```bash
# Use low-quality voice (faster generation)
/agent-vibes:switch fr_FR-siwis-low  # If available

# Disable effects
/agent-vibes:effects off

# Disable background music
/agent-vibes:background-music off

# Result: ~150ms latency instead of ~280ms
```

### Оптимізація для батареї

```bash
# macOS Say (instant, no CPU burst)
/agent-vibes:provider switch macos

# Trade-off: Lower quality, but 0ms generation time
```

### Менше відволікань

```bash
# Minimum verbosity
/agent-vibes:verbosity low

# Professional personality (less chatty)
/agent-vibes:personality professional

# Or mute during focus work
/agent-vibes:mute
```

---

## Усунення несправностей

### Немає звуку

```bash
# 1. Check mute status
ls -la .claude/agentvibes-muted ~/.agentvibes-muted

# 2. Verify provider
cat .claude/tts-provider.txt

# 3. Test Piper manually
echo "Test" | piper -m ~/.claude/piper-voices/fr_FR-tom-medium.onnx \
  --output-file /tmp/test.wav && afplay /tmp/test.wav
```

**Рішення**: детальну діагностику див. у [посібнику з усунення несправностей](./troubleshooting.uk.md).

### Голос звучить як у робота

**Рішення**: перейдіть на модель високої якості:
```bash
# Download high-quality voice
cd ~/.claude/piper-voices
curl -L -o fr_FR-siwis-high.onnx \
  "https://huggingface.co/rhasspy/piper-voices/resolve/main/fr/fr_FR/siwis/high/fr_FR-siwis-high.onnx"

/agent-vibes:switch fr_FR-siwis-high
```

### 34 команди захаращують палітру команд

**Рішення**: приховайте їх:
```bash
/agent-vibes:hide

# Unhide later if needed
/agent-vibes:show
```

**Інші проблеми?** Перегляньте [посібник з усунення несправностей](./troubleshooting.uk.md)

---

## Файли конфігурації

| Файл | Призначення | Формат |
|------|---------|--------|
| `.claude/tts-provider.txt` | Активний провайдер | `piper`, `macos` або `termux` |
| `.claude/tts-voice.txt` | Активний голос | `fr_FR-tom-medium` |
| `.claude/agentvibes-muted` | Стан вимкнення звуку проєкту | Наявність = звук вимкнено |
| `~/.agentvibes-muted` | Глобальний стан вимкнення звуку | Наявність = звук вимкнено |
| `.claude/config/audio-effects.cfg` | Конфігурація аудіоефектів | Формат Key=Value |
| `~/.claude/piper-voices/*.onnx` | Голосові моделі | Моделі нейронних мереж |

---

## Пов'язана документація

- **[Посібник зі встановлення](./installation.uk.md)** - повна 18-хвилинна процедура налаштування
- **[Каталог голосів](./voice-catalog.uk.md)** - усі 15 голосів зі зразками звучання
- **[Усунення несправностей](./troubleshooting.uk.md)** - типові проблеми та рішення
- **[Воркфлоу налаштування TTS](../../../guide/workflows/tts-setup.uk.md)** - покрокове встановлення
- **[Екосистема AI](../../../guide/ecosystem/ai-ecosystem.uk.md#5-голосові-інструменти-введення-wispr-flow-superwhisper)** - TTS у контексті AI

---

## Ресурси

- **GitHub**: https://github.com/paulpreibisch/AgentVibes
- **Вебсайт**: https://agentvibes.org
- **Демо-відео**: https://youtu.be/ngLiA_KQtTA
- **Голоси Piper**: https://huggingface.co/rhasspy/piper-voices
- **Зразки Piper**: https://rhasspy.github.io/piper-samples/

---

## Участь у розвитку

Agent Vibes — спільнотний проєкт. Повідомляйте про проблеми або робіть внесок:
- **Issues**: https://github.com/paulpreibisch/AgentVibes/issues
- **Ліцензія**: Apache 2.0

---

*Посібник з інтеграції підтримує [Claude Code Ultimate Guide](https://github.com/FlorianBruniaux/claude-code-ultimate-guide)*
*Останнє оновлення: 2026-01-22 | Agent Vibes v3.0.0 | Piper TTS v1.3.0*
