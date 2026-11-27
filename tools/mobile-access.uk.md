# Мобільний доступ до Claude Code

> **⚠️ СТАТУС: WIP / НЕ ПРОТЕСТОВАНО**
>
> Цей посібник ще в роботі. Налаштування не було повністю протестовано в різних середовищах.
> Використовуйте на власний ризик. Внески та відгуки вітаються.

---

## Проблема

Claude Code CLI є **локальним інтерактивним процесом**, а не сервісом із API сесій. Кожен екземпляр автономний. Навіть `claude --remote` лише переносить виконання: релейної системи він не створює.

**Чого бракує**: нативного режиму `claude --serve`, який відкривав би API WebSocket, дозволяв би кілька клієнтів і зберігав той самий контекст розмови.

**Обхідний шлях**: відкрити свій термінал у веббраузері за допомогою `ttyd`, доступного звідусіль через VPN `Tailscale`.

---

## Рішення: ttyd + Tailscale

```
ВАШ КОМП'ЮТЕР                     ВАШ ТЕЛЕФОН
┌─────────────────┐               ┌─────────────────┐
│  Claude Code    │◄──────────────│  Браузер        │
│  (працює тут)   │   Tailscale   │  (та сама сесія)│
│                 │   (VPN)       │                 │
└─────────────────┘               └─────────────────┘
```

- **ttyd**: відкриває ваш термінал у веббраузері
- **Tailscale**: безкоштовний VPN, що дає вашому комп'ютеру фіксовану IP-адресу, доступну звідусіль (4G, публічний WiFi тощо)
- **tmux**: тримає сесію живою, навіть якщо закрити браузер

**Сценарій використання**: стежити за сесіями Claude Code та продовжувати їх із телефона (у дорозі, поза робочим місцем тощо)

---

## Порівняння архітектур

### ttyd + Tailscale (самостійний хостинг)

```
ВАШ КОМП'ЮТЕР                     ВАШ ТЕЛЕФОН
┌─────────────────┐               ┌─────────────────┐
│  Claude Code    │◄──────────────│  Браузер        │
│  (працює тут)   │   Tailscale   │  (та сама сесія)│
│  ┌───────────┐  │   VPN         │                 │
│  │   ttyd    │  │               └─────────────────┘
│  └───────────┘  │
└─────────────────┘
✅ Безпечно щодо ToS: офіційний CLI, без хмарного посередника
```

### Happy Coder (нативний застосунок)

```
ВАШ КОМП'ЮТЕР                     ВАШ ТЕЛЕФОН
┌─────────────────┐               ┌─────────────────┐
│  Claude Code    │               │  Happy App      │
│  (офіційний CLI)│◄─────────────►│  (Expo native)  │
│       ▲         │  Локальна     │                 │
│  subprocess     │  синхр.       └─────────────────┘
│  ┌───────────┐  │
│  │ Happy Hub │  │
│  └───────────┘  │
└─────────────────┘
✅ Безпечно щодо ToS: локальна обгортка, subprocess Node.js
```

### Remoto.sh (хмарний релей)

```
ХМАРА REMOTO                       ВАШ ТЕЛЕФОН
┌─────────────────┐               ┌─────────────────┐
│  Docker         │◄──────────────│  Браузер        │
│  Container      │   WebSocket   │                 │
│  ┌───────────┐  │               └─────────────────┘
│  │ Claude    │  │
│  │ Code CLI  │  │
│  └───────────┘  │
└─────────────────┘
⚠️ Ризик щодо ToS: хмарна обгортка = потенційний "несанкціонований проксі"
```

---

## Чому саме цей підхід?

### Міркування щодо ToS

Деякі сторонні обгортки (як-от OpenCode) були заблоковані Anthropic за порушення ToS. Цей підхід **безпечний щодо ToS**, бо:

- Ви використовуєте **офіційний Claude Code CLI**
- ttyd лише відкриває ваш термінал через браузер (без обгортки)
- Tailscale є просто VPN для безпечного доступу
- Жоден сторонній клієнт не взаємодіє з API Claude

---

## Вимоги

- macOS або Linux
- Встановлений і автентифікований Claude Code CLI
- Обліковий запис Tailscale (достатньо безкоштовного тарифу)

---

## Встановлення

### Скрипт швидкого налаштування

```bash
#!/bin/bash
# claude-mobile-setup.sh

set -e

echo "=== Setup Claude Code Mobile ==="

# 1. Install ttyd + tmux
echo "[1/2] Installing ttyd..."
if [[ "$OSTYPE" == "darwin"* ]]; then
    brew install ttyd tmux
else
    sudo apt install -y tmux
    sudo snap install ttyd --classic
fi

# 2. Install Tailscale
echo "[2/2] Installing Tailscale..."
if [[ "$OSTYPE" == "darwin"* ]]; then
    brew install tailscale
else
    curl -fsSL https://tailscale.com/install.sh | sh
fi

# 3. Create launcher script
mkdir -p ~/.local/bin
cat > ~/.local/bin/claude-mobile << 'EOF'
#!/bin/bash
PORT=7681
PASS="${CLAUDE_MOBILE_PASS:-claude123}"

TS_IP=$(tailscale ip -4 2>/dev/null || echo "not connected")

echo "══════════════════════════════════"
echo "  CLAUDE CODE MOBILE"
echo "══════════════════════════════════"
echo "  URL:  http://$TS_IP:$PORT"
echo "  User: claude"
echo "  Pass: $PASS"
echo "══════════════════════════════════"
echo ""
echo "Open this URL on your phone."
echo "Press Ctrl+C to stop."
echo ""

# Kill existing session if any
tmux kill-session -t cc 2>/dev/null || true

# Start Claude in tmux, expose via ttyd
tmux new-session -d -s cc 'claude'
exec ttyd -W -p $PORT -c "claude:$PASS" tmux attach -t cc
EOF

chmod +x ~/.local/bin/claude-mobile

# Add to PATH
if [[ ":$PATH:" != *":$HOME/.local/bin:"* ]]; then
    echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.zshrc
    echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
fi

echo ""
echo "=== Installation Complete ==="
echo ""
echo "Next steps:"
echo "  1. Run: tailscale up"
echo "  2. Run: source ~/.zshrc"
echo "  3. Run: claude-mobile"
echo ""
```

### Ручне встановлення

```bash
# macOS
brew install ttyd tmux tailscale

# Linux (Debian/Ubuntu)
sudo apt install -y tmux
sudo snap install ttyd --classic
curl -fsSL https://tailscale.com/install.sh | sh
```

---

## Використання

### Перше налаштування

```bash
# 1. Підключіться до Tailscale (одноразово)
tailscale up
# Перейдіть за посиланням, щоб автентифікуватися через Google/GitHub тощо.

# 2. Встановіть Tailscale на телефон
# iOS: App Store → Tailscale
# Android: Play Store → Tailscale
# Увійдіть тим самим обліковим записом

# 3. Запустіть Claude Code Mobile
claude-mobile
```

### Вивід

```
══════════════════════════════════
  CLAUDE CODE MOBILE
══════════════════════════════════
  URL:  http://100.78.42.15:7681
  User: claude
  Pass: claude123
══════════════════════════════════
```

### На телефоні

1. Відкрийте Safari/Chrome
2. Перейдіть на `http://100.78.42.15:7681` (використайте свою справжню IP-адресу Tailscale)
3. Увійдіть із `claude` / `claude123`
4. Тепер Claude Code у вас у браузері

---

## Конфігурація

### Змінити пароль

```bash
export CLAUDE_MOBILE_PASS="your-secure-password"
claude-mobile
```

Або додайте до конфігурації оболонки:

```bash
echo 'export CLAUDE_MOBILE_PASS="your-secure-password"' >> ~/.zshrc
```

### Змінити порт

Відредагуйте `~/.local/bin/claude-mobile` і змініть `PORT=7681` на бажаний порт.

---

## Безпека

| Рівень | Захист |
|-------|------------|
| **Мережа** | Tailscale використовує шифрування WireGuard |
| **Автентифікація** | Basic auth (ім'я користувача:пароль) через ttyd |
| **Доступ** | Доступно лише з вашої мережі Tailscale |

**Рекомендації**:
- Використовуйте надійний пароль (не типовий `claude123`)
- Не відкривайте ttyd безпосередньо в інтернет без Tailscale
- Підтримуйте клієнт Tailscale оновленим на всіх пристроях

---

## Усунення несправностей

### "not connected" замість IP

```bash
# Перевірте стан Tailscale
tailscale status

# Якщо відключено, підключіться знову
tailscale up
```

### Немає доступу з телефона

1. Переконайтеся, що застосунок Tailscale встановлено на телефон і підключено до того самого облікового запису
2. Перевірте, що брандмауер не блокує порт 7681
3. Спершу спробуйте відкрити локально: `http://localhost:7681`

### Сесія не зберігається

Сесія tmux має зберігатися. Щоб під'єднатися вручну:

```bash
tmux attach -t cc
```

### Команду ttyd не знайдено

```bash
# macOS
brew reinstall ttyd

# Linux
sudo snap install ttyd --classic
```

---

## Порівняння альтернатив

| Рішення | Тип | Переваги | Недоліки | ToS | Зірки |
|----------|------|------|------|-----|-------|
| **ttyd + Tailscale** ✅ | Самостійний хостинг | Безкоштовно, максимальний контроль, офіційний CLI | Ручне налаштування, UX терміналу | ✅ Безпечно | Н/Д |
| [Happy Coder](https://github.com/slopus/happy) | Нативний застосунок | Голос, шифрування, кілька екземплярів, mobile-first | Залежність від стороннього проєкту | ✅ Безпечно | 7.8K |
| [Remoto.sh](https://remoto.sh) | Хмарний релей | Швидке налаштування, лише браузер | Хмарна обгортка, затримка, вартість | ⚠️ Ризик | Н/Д |
| tmux + SSH | Самостійний хостинг | Без залежностей, офіційний CLI | Потрібен мобільний SSH-клієнт | ✅ Безпечно | Н/Д |
| [swe-mux](https://github.com/jatoran/swe-mux) | Самостійний хостинг (PWA через Tailscale) | Офіційний CLI в реальних PTY, ті самі живі сесії на десктопі й телефоні, статус кожної сесії, push-сповіщення, попередній перегляд dev-серверів, сесії переживають перезапуски, без релея | Застосунок для Windows; macOS/Linux через браузер; молодий проєкт | ✅ Безпечно | Н/Д |

Ми обрали ttyd + Tailscale, тому що:
- Це просто ваш термінал, відкритий через браузер
- Жодної сторонньої обгортки навколо Claude Code
- Нульовий ризик щодо ToS: ви використовуєте офіційний CLI

---

### Happy Coder: рекомендована альтернатива

Якщо ви віддаєте перевагу **нативному застосунку** замість вебтерміналу:

- **Репозиторій**: [github.com/slopus/happy](https://github.com/slopus/happy)
- **Зірки**: 7.8K (січень 2026)
- **Ліцензія**: MIT
- **Стек**: Tauri (desktop) + Expo (mobile)
- **Провайдери**: Claude Code, Codex, Gemini

**Чому безпечно щодо ToS**: Happy Coder є локальною обгорткою, що запускає офіційний CLI через subprocess Node.js. Жодних прямих викликів API, жодного хмарного проксі.

**Встановлення**:
```bash
npm i -g happy-coder && happy
```

---

### Remoto.sh: хмарна альтернатива (з ризиками)

**Чому ризиковано**: Remoto.sh використовує хмарні контейнери Docker як релей. Згідно з ToS Anthropic (§4.2), "несанкціоновані проксі, що приховують походження запитів", заборонені. На Reddit/HN повідомляли про блокування облікових записів за подібне використання.

> **Рекомендація**: віддавайте перевагу Happy Coder або ttyd+Tailscale, щоб уникнути ризиків щодо ToS.

---

## Пов'язані ресурси

- [ttyd GitHub](https://github.com/tsl0922/ttyd): вебсервер терміналу
- [Tailscale](https://tailscale.com/): VPN без налаштувань
- [ttyd + Claude Code Guide](https://aiengineerguide.com/blog/agentic-cli-browser-ttyd/): спільнотний туторіал
- [VPS Setup Guide](https://joshualent.com/snippets/claude-phone/): альтернатива: запуск на VPS

---

## Джерела

- [Happy Coder GitHub](https://github.com/slopus/happy): 7.8K ⭐, ліцензія MIT
- [ttyd GitHub](https://github.com/tsl0922/ttyd): вебсервер терміналу
- [Tailscale](https://tailscale.com/): VPN без налаштувань
- [Remoto.sh](https://remoto.sh): хмарний термінал (зазначено ризик щодо ToS)
- ToS Anthropic §4.2: несанкціоновані проксі

---

## Внесок

Цей документ **WIP/НЕ ПРОТЕСТОВАНО**. Якщо ви протестуєте це налаштування, поділіться, будь ласка:
- Вашою ОС/середовищем
- Будь-якими проблемами, що виникли
- Пропозиціями щодо покращення

Відкрийте issue або PR у цьому репозиторії.

---

*Востаннє оновлено: січень 2026 | Статус: WIP/НЕ ПРОТЕСТОВАНО | Дані перевірено: Happy Coder 7.8K ⭐ (2026-01-19)*
