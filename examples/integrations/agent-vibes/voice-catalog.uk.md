---
title: "Agent Vibes — повний каталог голосів"
description: "Довідковий каталог доступних TTS-голосів з оцінками якості та підтримкою мов"
tags: [reference, tts, integration]
---

# Agent Vibes — повний каталог голосів

**Усього голосів**: 15 встановлених + понад 50 доступних
**Мови**: французька (4 моделі, 128 дикторів), англійська (12 моделей)

---

## Французькі голоси (voix françaises)

### Огляд

| ID голосу | Стать | Якість | Дикторів | Розмір | Рекомендація |
|----------|--------|---------|----------|------|-------------|
| **fr_FR-tom-medium** | Чоловічий | Середня | 1 | 60MB | ⭐️⭐️⭐️⭐️⭐️ Найкращий чоловічий FR |
| fr_FR-siwis-medium | Жіночий | Середня | 1 | 60MB | ⭐️⭐️⭐️⭐️ Чіткий, природний |
| fr_FR-upmc-medium | Нейтральний | Середня | 1 | 73MB | ⭐️⭐️⭐️ Універсальний |
| **fr_FR-mls-medium** | Змішаний | Середня | **124** | 73MB | ⭐️⭐️⭐️⭐️⭐️ Максимальна різноманітність |

---

### fr_FR-tom-medium ⭐️⭐️⭐️⭐️⭐️

**Стать**: чоловічий
**Якість**: середня
**Характер**: професійний, чітка вимова, нейтральний акцент
**Найкраще для**: технічної документації, рев'ю коду, професійного контексту
**Затримка**: ~200ms

**Використання**:
```bash
# In Claude Code
/agent-vibes:switch fr_FR-tom-medium

# Manual test
echo "Bonjour, je m'appelle Tom. Je suis une voix synthétique française." | \
  piper -m ~/.claude/piper-voices/fr_FR-tom-medium.onnx \
  --output-file /tmp/tom.wav && afplay /tmp/tom.wav
```

**Аудіозразок**: слухайте на https://rhasspy.github.io/piper-samples/ (шукайте "fr_FR tom")

---

### fr_FR-siwis-medium ⭐️⭐️⭐️⭐️

**Стать**: жіночий
**Якість**: середня
**Характер**: теплий, природний, з легким швейцарським акцентом
**Найкраще для**: туторіалів, навчального контенту, дружніх взаємодій
**Затримка**: ~200ms

**Використання**:
```bash
# In Claude Code
/agent-vibes:switch fr_FR-siwis-medium

# Manual test
echo "Bonjour, je suis Siwis. J'ai une voix claire et agréable." | \
  piper -m ~/.claude/piper-voices/fr_FR-siwis-medium.onnx \
  --output-file /tmp/siwis.wav && afplay /tmp/siwis.wav
```

**Аудіозразок**: https://rhasspy.github.io/piper-samples/ (шукайте "fr_FR siwis")

---

### fr_FR-upmc-medium ⭐️⭐️⭐️

**Стать**: нейтральний (трохи ближчий до жіночого)
**Якість**: середня
**Характер**: технічний, точний, академічний тон
**Найкраще для**: наукового контенту, аналізу даних, офіційних презентацій
**Затримка**: ~220ms (більша модель)

**Використання**:
```bash
# In Claude Code
/agent-vibes:switch fr_FR-upmc-medium

# Manual test
echo "Analyse des données en cours. Résultats disponibles dans quelques instants." | \
  piper -m ~/.claude/piper-voices/fr_FR-upmc-medium.onnx \
  --output-file /tmp/upmc.wav && afplay /tmp/upmc.wav
```

**Аудіозразок**: https://rhasspy.github.io/piper-samples/ (шукайте "fr_FR upmc")

---

### fr_FR-mls-medium ⭐️⭐️⭐️⭐️⭐️ (кілька дикторів)

**Стать**: змішаний (49 жіночих, 75 чоловічих)
**Якість**: середня
**Диктори**: **124 різні голоси**
**Характер**: величезна різноманітність (молоді, літні, акценти, тони)
**Найкраще для**: симуляції діалогів, різноманітності, голосів персонажів
**Затримка**: ~200ms + вибір диктора

**Використання**:
```bash
# In Claude Code (uses default speaker)
/agent-vibes:switch fr_FR-mls-medium

# Manual test with specific speaker (0-123)
echo "Je suis le speaker numéro 42" | \
  piper -m ~/.claude/piper-voices/fr_FR-mls-medium.onnx -s 42 \
  --output-file /tmp/mls-42.wav && afplay /tmp/mls-42.wav

# Test multiple speakers
for speaker in {0..5}; do
  echo "Bonjour, speaker $speaker" | \
    piper -m ~/.claude/piper-voices/fr_FR-mls-medium.onnx -s $speaker \
    --output-file /tmp/mls-$speaker.wav
  afplay /tmp/mls-$speaker.wav
  sleep 1
done
```

**Вибір диктора**:
- `0-48`: жіночі голоси (усього 49)
- `49-123`: чоловічі голоси (усього 75)

**Рекомендовані диктори**:
| ID диктора | Стать | Характер |
|------------|--------|-----------|
| 7 | Жіночий | Молодий, енергійний |
| 15 | Жіночий | Зрілий, професійний |
| 23 | Жіночий | Теплий, дружній |
| 55 | Чоловічий | Глибокий, авторитетний |
| 72 | Чоловічий | Чіткий, технічний |
| 99 | Чоловічий | Молодий, невимушений |

**Аудіозразки**: https://rhasspy.github.io/piper-samples/ (шукайте "fr_FR mls")

---

## Англійські голоси (voix anglaises)

### Огляд

| ID голосу | Стать | Якість | Характер | Рекомендація |
|----------|--------|---------|-----------|-------------|
| **en_US-ryan-high** | Чоловічий | Висока | Професійний | ⭐️⭐️⭐️⭐️⭐️ Найкращий EN |
| en_US-amy-medium | Жіночий | Середня | Теплий, природний | ⭐️⭐️⭐️⭐️ |
| en_US-lessac-medium | Чоловічий | Середня | Авторитетний | ⭐️⭐️⭐️⭐️ |
| en_US-libritts-high | Змішаний | Висока | Дуже природний | ⭐️⭐️⭐️⭐️⭐️ |
| en_US-hfc_female-medium | Жіночий | Середня | Технічний | ⭐️⭐️⭐️ |
| en_US-bryce-medium | Чоловічий | Середня | Молодий, динамічний | ⭐️⭐️⭐️ |
| en_US-danny-low | Чоловічий | Низька | Швидкий, ефективний | ⭐️⭐️ |
| en_US-kathleen-low | Жіночий | Низька | Швидкий, ефективний | ⭐️⭐️ |
| en_US-kusal-medium | Чоловічий | Середня | Індійський акцент | ⭐️⭐️⭐️ |
| en_US-kristin-medium | Жіночий | Середня | Чіткий, нейтральний | ⭐️⭐️⭐️⭐️ |
| en_US-libritts_r-high | Змішаний | Висока | Дуже природний | ⭐️⭐️⭐️⭐️⭐️ |
| 16Speakers | Кілька | Середня | 16 різних | ⭐️⭐️⭐️⭐️ |

---

### en_US-ryan-high ⭐️⭐️⭐️⭐️⭐️

**Стать**: чоловічий
**Якість**: висока (найкращий англійський голос)
**Характер**: професійний ведучий новин, чітка вимова
**Найкраще для**: професійних презентацій, документації, рев'ю коду
**Затримка**: ~400ms (високоякісна модель)

**Використання**:
```bash
/agent-vibes:switch en_US-ryan-high
```

---

### en_US-amy-medium ⭐️⭐️⭐️⭐️

**Стать**: жіночий
**Якість**: середня
**Характер**: теплий, дружній, розмовний
**Найкраще для**: туторіалів, невимушених взаємодій, навчального контенту
**Затримка**: ~200ms

**Використання**:
```bash
/agent-vibes:switch en_US-amy-medium
```

---

### en_US-libritts-high ⭐️⭐️⭐️⭐️⭐️

**Стать**: змішаний (кілька дикторів)
**Якість**: висока
**Характер**: дуже природний, виразний
**Найкраще для**: високоякісного аудіооповідання
**Затримка**: ~400ms

**Використання**:
```bash
/agent-vibes:switch en_US-libritts-high
```

---

### 16Speakers ⭐️⭐️⭐️⭐️ (англійська, кілька дикторів)

**Стать**: змішаний (8 жіночих, 8 чоловічих)
**Якість**: середня
**Диктори**: 16 різних англійських голосів
**Характер**: різноманітні вік, акценти, тони
**Найкраще для**: діалогів, різноманітності, оповіді за персонажів
**Затримка**: ~200ms + вибір диктора

**Використання**:
```bash
# Default speaker
/agent-vibes:switch 16Speakers

# Specific speaker (0-15)
echo "I am speaker number 5" | \
  piper -m ~/.claude/piper-voices/16Speakers.onnx -s 5 \
  --output-file /tmp/16sp-5.wav && afplay /tmp/16sp-5.wav
```

---

## Голоси низької якості (швидші, нижча якість)

### Коли використовувати низьку якість

- Економія заряду батареї (генерація на 50% швидша)
- Застосунки, чутливі до затримки (вимога <150ms)
- Швидке прототипування чи тестування
- Фонові сповіщення (якість менш важлива)

### Доступні моделі низької якості

| ID голосу | Стать | Затримка | Якість |
|----------|--------|---------|---------|
| en_US-danny-low | Чоловічий | ~100ms | ⭐️⭐️ |
| en_US-kathleen-low | Жіночий | ~100ms | ⭐️⭐️ |
| fr_FR-gilles-low | Чоловічий | ~100ms | ⭐️⭐️ |
| fr_FR-siwis-low | Жіночий | ~100ms | ⭐️⭐️ |

**Завантаження голосу низької якості**:
```bash
cd ~/.claude/piper-voices
curl -L -o fr_FR-gilles-low.onnx \
  "https://huggingface.co/rhasspy/piper-voices/resolve/main/fr/fr_FR/gilles/low/fr_FR-gilles-low.onnx"
curl -L -o fr_FR-gilles-low.onnx.json \
  "https://huggingface.co/rhasspy/piper-voices/resolve/main/fr/fr_FR/gilles/low/fr_FR-gilles-low.onnx.json"
```

---

## Голоси високої якості (повільніші, краща якість)

### Коли використовувати високу якість

- Професійні презентації
- Створення контенту (відео, подкасти)
- Демонстрації або публічні покази
- Коли затримка некритична

### Доступні моделі високої якості

| ID голосу | Стать | Затримка | Якість |
|----------|--------|---------|---------|
| en_US-ryan-high | Чоловічий | ~400ms | ⭐️⭐️⭐️⭐️⭐️ |
| en_US-libritts-high | Змішаний | ~400ms | ⭐️⭐️⭐️⭐️⭐️ |
| en_US-libritts_r-high | Змішаний | ~400ms | ⭐️⭐️⭐️⭐️⭐️ |
| fr_FR-siwis-high | Жіночий | ~400ms | ⭐️⭐️⭐️⭐️⭐️ |

**Завантаження голосу високої якості**:
```bash
cd ~/.claude/piper-voices
curl -L -o fr_FR-siwis-high.onnx \
  "https://huggingface.co/rhasspy/piper-voices/resolve/main/fr/fr_FR/siwis/high/fr_FR-siwis-high.onnx"
curl -L -o fr_FR-siwis-high.onnx.json \
  "https://huggingface.co/rhasspy/piper-voices/resolve/main/fr/fr_FR/siwis/high/fr_FR-siwis-high.onnx.json"
```

---

## Додаткові мови

Piper TTS підтримує **понад 50 мов**. Додаткові голоси можна завантажити з Hugging Face.

### Доступні популярні мови

| Мова | Доступно голосів | Репозиторій |
|----------|------------------|------------|
| Іспанська (es_ES) | 10+ голосів | [Посилання](https://huggingface.co/rhasspy/piper-voices/tree/main/es/es_ES) |
| Німецька (de_DE) | 8+ голосів | [Посилання](https://huggingface.co/rhasspy/piper-voices/tree/main/de/de_DE) |
| Італійська (it_IT) | 6+ голосів | [Посилання](https://huggingface.co/rhasspy/piper-voices/tree/main/it/it_IT) |
| Португальська (pt_BR) | 5+ голосів | [Посилання](https://huggingface.co/rhasspy/piper-voices/tree/main/pt/pt_BR) |
| Російська (ru_RU) | 4+ голоси | [Посилання](https://huggingface.co/rhasspy/piper-voices/tree/main/ru/ru_RU) |
| Китайська (zh_CN) | 3+ голоси | [Посилання](https://huggingface.co/rhasspy/piper-voices/tree/main/zh/zh_CN) |

### Приклад завантаження іспанського голосу

```bash
cd ~/.claude/piper-voices

# Spanish male voice (Davefx - high quality)
curl -L -o es_ES-davefx-medium.onnx \
  "https://huggingface.co/rhasspy/piper-voices/resolve/main/es/es_ES/davefx/medium/es_ES-davefx-medium.onnx"
curl -L -o es_ES-davefx-medium.onnx.json \
  "https://huggingface.co/rhasspy/piper-voices/resolve/main/es/es_ES/davefx/medium/es_ES-davefx-medium.onnx.json"

# Test
echo "Hola, soy Claude y hablo español" | \
  piper -m es_ES-davefx-medium.onnx \
  --output-file /tmp/es.wav && afplay /tmp/es.wav
```

---

## Рекомендації щодо вибору голосу

### За сценарієм використання

| Сценарій | Рекомендований голос | Причина |
|----------|-------------------|--------|
| **Технічна документація** | fr_FR-tom-medium | Чіткий, професійний, технічний тон |
| **Рев'ю коду** | en_US-ryan-high | Авторитетний, чітка вимова |
| **Туторіали** | fr_FR-siwis-medium | Теплий, дружній, навчальний |
| **Фонові сповіщення** | fr_FR-gilles-low | Швидкий, ефективний, низька затримка |
| **Професійні презентації** | en_US-ryan-high | Найкраща якість, професійний |
| **Різноманітність/діалоги** | fr_FR-mls-medium | 124 різні голоси |
| **Економія батареї** | Будь-який голос "-low" | Генерація на 50% швидша |

### За мовою

| Основна мова | Найкращий голос | Альтернатива |
|------------------|------------|-------------|
| **Французька** | fr_FR-tom-medium | fr_FR-mls-medium (різноманітність) |
| **Англійська** | en_US-ryan-high | en_US-libritts-high |
| **Іспанська** | es_ES-davefx-medium | es_ES-carlfm-medium |
| **Німецька** | de_DE-thorsten-high | de_DE-kerstin-low |

---

## Інструмент порівняння голосів

Порівнюйте голоси пліч-о-пліч:

```bash
# Create comparison script
cat > /tmp/compare-voices.sh << 'EOF'
#!/bin/bash
TEXT="$1"
VOICES=("fr_FR-tom-medium" "fr_FR-siwis-medium" "fr_FR-upmc-medium")

for voice in "${VOICES[@]}"; do
  echo "Testing $voice..."
  echo "$TEXT" | piper -m ~/.claude/piper-voices/${voice}.onnx \
    --output-file /tmp/${voice}.wav
  afplay /tmp/${voice}.wav
  sleep 2
done
EOF

chmod +x /tmp/compare-voices.sh

# Compare voices
/tmp/compare-voices.sh "Bonjour, ceci est un test de comparaison"
```

---

## Ресурси

- **Репозиторій голосів Piper**: https://huggingface.co/rhasspy/piper-voices
- **Аудіозразки**: https://rhasspy.github.io/piper-samples/
- **Навчання голосів**: https://github.com/rhasspy/piper/blob/master/TRAINING.md
- **Власні голоси**: https://community.rhasspy.org/c/piper/

---

*Каталог голосів підтримує [Claude Code Ultimate Guide](https://github.com/FlorianBruniaux/claude-code-ultimate-guide)*
*Останнє оновлення: 2026-01-22 | Piper TTS v1.3.0*
