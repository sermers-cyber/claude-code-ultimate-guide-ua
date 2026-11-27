---
name: ccboard-install
description: Встановити або оновити ccboard
category: setup
---

# Команда встановлення ccboard

Встановлює або оновлює бінарник ccboard через cargo.

## Що таке ccboard?

ccboard є повноцінним TUI/Web-дашбордом для моніторингу та керування Claude Code:

- **8 інтерактивних вкладок**: Dashboard, Sessions, Config, Hooks, Agents, Costs, History, MCP
- **Моніторинг у реальному часі**: відстеження файлів для живих оновлень
- **Керування MCP**: стан і конфігурація серверів
- **Аналітика витрат**: відстеження використання токенів і цін
- **Оглядач сесій**: перегляд історії розмов і пошук у ній
- **Подвійний інтерфейс**: термінал (TUI) і веб-UI

## Вимоги

- **Rust**: версія 1.70 або новіша
- **Cargo**: менеджер пакетів Rust (постачається разом із Rust)

Якщо Rust не встановлено:
```bash
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
```

## Використання

```bash
# Install ccboard
/ccboard-install

# Or manually
cargo install ccboard
```

## Процес встановлення

1. Перевіряє, чи встановлено cargo
2. Виявляє наявне встановлення ccboard
3. Просить підтвердити оновлення, якщо ccboard уже встановлено
4. Встановлює через `cargo install ccboard --force`
5. Перевіряє встановлення й показує версію

## Після встановлення

Після встановлення використовуйте такі команди:

- `/dashboard` - запустити TUI-дашборд
- `/mcp-status` - відкрити вкладку MCP-серверів
- `/costs` - відкрити аналіз витрат
- `/sessions` - переглянути історію сесій
- `/ccboard-web` - запустити веб-інтерфейс

Або запускайте напряму:
```bash
ccboard              # Launch TUI
ccboard web          # Launch web UI
ccboard --help       # Show all options
```

## Усунення несправностей

### Cargo не знайдено
```bash
# Install Rust and cargo
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh

# Reload shell
source $HOME/.cargo/env
```

### Встановлення не вдається
```bash
# Update Rust toolchain
rustup update

# Try manual installation from source
git clone https://github.com/{OWNER}/ccboard
cd ccboard
cargo install --path crates/ccboard
```

### Відмовлено в доступі
```bash
# Ensure ~/.cargo/bin is in PATH
echo 'export PATH="$HOME/.cargo/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

## Реалізація

```bash
#!/bin/bash

# Run installation script
exec "$(dirname "$0")/../scripts/install-ccboard.sh"
```

## Видалення

Щоб видалити ccboard:
```bash
cargo uninstall ccboard
```
