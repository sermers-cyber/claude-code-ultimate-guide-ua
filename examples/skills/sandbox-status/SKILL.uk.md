---
name: sandbox-status
description: Показати статус нативного sandbox, конфігурацію та нещодавні порушення
effort: low
when_to_use: "Використовуйте, щоб перевірити, чи активний режим sandbox Claude Code і які обмеження застосовуються."
disable-model-invocation: true
---

# Команда sandbox status

Огляньте стан нативного sandbox Claude Code, активну конфігурацію та події безпеки.

## Використання

```
/sandbox-status
```

## Що вона робить

1. **Перевіряє доступність sandbox**
   - Перевіряє встановлення примітивів ОС (bubblewrap на Linux, Seatbelt на macOS)
   - Показує статус підтримки платформи

2. **Показує активну конфігурацію**
   - Режим sandbox (Auto-allow чи звичайні дозволи)
   - Політики файлової системи (дозволені записи, заборонені читання)
   - Мережеві політики (allowlist/denylist доменів)
   - Виключені команди

3. **Перелічує нещодавні порушення sandbox**
   - Заблоковані спроби доступу до файлової системи
   - Заблоковані мережеві з'єднання
   - Виклики аварійного виходу (`dangerouslyDisableSandbox`)

## Реалізація

```bash
#!/bin/bash

echo "=== Native Sandbox Status ==="
echo

# 1. Platform Check
echo "Platform:"
case "$OSTYPE" in
  darwin*)
    echo "  ✅ macOS (Seatbelt built-in)"
    ;;
  linux*)
    if which bubblewrap >/dev/null 2>&1; then
      echo "  ✅ Linux (bubblewrap installed)"
      bubblewrap --version 2>/dev/null | head -1
    else
      echo "  ❌ Linux (bubblewrap NOT installed)"
      echo "     Install: sudo apt-get install bubblewrap socat"
    fi
    if which socat >/dev/null 2>&1; then
      echo "  ✅ socat installed"
    else
      echo "  ❌ socat NOT installed"
    fi
    ;;
  *)
    echo "  ❌ Unsupported platform: $OSTYPE"
    ;;
esac
echo

# 2. Configuration
echo "Configuration (from settings.json):"
if [ -f .claude/settings.json ]; then
  CONFIG=".claude/settings.json"
elif [ -f ~/.claude/settings.json ]; then
  CONFIG="~/.claude/settings.json"
else
  echo "  ⚠️  No settings.json found"
  CONFIG=""
fi

if [ -n "$CONFIG" ]; then
  echo "  Source: $CONFIG"

  # Auto-allow mode
  AUTO_ALLOW=$(jq -r '.sandbox.autoAllowBashIfSandboxed // "not set"' "$CONFIG" 2>/dev/null)
  echo "  Auto-allow: $AUTO_ALLOW"

  # Escape hatch
  ESCAPE=$(jq -r '.sandbox.allowUnsandboxedCommands // "not set"' "$CONFIG" 2>/dev/null)
  echo "  dangerouslyDisableSandbox allowed: $ESCAPE"

  # Allowed write paths
  WRITE_PATHS=$(jq -r '.sandbox.filesystem.allowWrite[]? // empty' "$CONFIG" 2>/dev/null | tr '\n' ', ')
  echo "  Allowed writes: ${WRITE_PATHS:-not set}"

  # Credential files denied to every subprocess
  CRED_FILES=$(jq -r '.sandbox.credentials.files[]?.path // empty' "$CONFIG" 2>/dev/null | tr '\n' ', ')
  echo "  Denied credential files: ${CRED_FILES:-not set}"

  # Strict allowlist switch
  STRICT=$(jq -r '.sandbox.network.strictAllowlist // "not set (default false)"' "$CONFIG" 2>/dev/null)
  echo "  Strict allowlist: $STRICT"

  # Allowed domains
  DOMAINS=$(jq -r '.sandbox.network.allowedDomains[]? // empty' "$CONFIG" 2>/dev/null | head -3 | tr '\n' ', ')
  DOMAINS_COUNT=$(jq -r '.sandbox.network.allowedDomains | length' "$CONFIG" 2>/dev/null)
  if [ -n "$DOMAINS" ]; then
    echo "  Allowed domains: $DOMAINS... ($DOMAINS_COUNT total)"
  else
    echo "  Allowed domains: not set"
  fi

  # Excluded commands
  EXCLUDED=$(jq -r '.sandbox.excludedCommands[]? // empty' "$CONFIG" 2>/dev/null | tr '\n' ', ')
  echo "  Excluded commands: ${EXCLUDED:-not set}"
fi
echo

# 3. Recent Violations (placeholder - actual implementation would read Claude Code logs)
echo "Recent sandbox violations:"
echo "  ℹ️  Log inspection not yet implemented"
echo "  Tip: Check Claude Code session logs for sandbox violation notifications"
echo

# 4. Open-Source Runtime
echo "Open-Source Runtime:"
if which npx >/dev/null 2>&1; then
  echo "  ✅ npx available - can use @anthropic-ai/sandbox-runtime"
  echo "  Usage: npx @anthropic-ai/sandbox-runtime <command>"
else
  echo "  ⚠️  npx not found (install Node.js)"
fi
echo

# 5. Documentation
echo "Documentation:"
echo "  Guide: guide/security/sandbox-native.md"
echo "  Official: https://code.claude.com/docs/en/sandboxing"
echo "  Runtime: https://github.com/anthropic-experimental/sandbox-runtime"
```

## Приклад виводу

```
=== Native Sandbox Status ===

Platform:
  ✅ macOS (Seatbelt built-in)

Configuration (from settings.json):
  Source: .claude/settings.json
  Auto-allow: true
  dangerouslyDisableSandbox allowed: false
  Allowed writes: ${CWD}, /tmp
  Denied credential files: ~/.ssh, ~/.aws, ~/.gnupg
  Strict allowlist: not set (default false)
  Allowed domains: api.anthropic.com, registry.npmjs.com, github.com... (9 total)
  Excluded commands: docker, kubectl, podman

Recent sandbox violations:
  ℹ️  Log inspection not yet implemented
  Tip: Check Claude Code session logs for sandbox violation notifications

Open-Source Runtime:
  ✅ npx available - can use @anthropic-ai/sandbox-runtime
  Usage: npx @anthropic-ai/sandbox-runtime <command>

Documentation:
  Guide: guide/security/sandbox-native.md
  Official: https://code.claude.com/docs/en/sandboxing
  Runtime: https://github.com/anthropic-experimental/sandbox-runtime
```

## Сценарії використання

- **Перед розгортанням**: Перевірте конфігурацію sandbox перед запуском автономних воркфлоу
- **Налагодження**: З'ясуйте, чому певні команди заблоковано
- **Аудит безпеки**: Перегляньте дозволені домени та доступ до файлової системи
- **Онбордінг**: Допоможіть новим членам команди зрозуміти політику sandbox проєкту

## Див. також

- [Посібник із нативного sandboxing](../../../guide/security/sandbox-native.uk.md) - повний технічний довідник
- [/sandbox-unblock](../sandbox-unblock/SKILL.uk.md) - діагностичний протокол, коли щось здається заблокованим
- [Hook валідації sandbox](../../hooks/bash/sandbox-validation.sh) - перевірка перед виконанням команди
- [Приклад конфігурації sandbox](../../config/sandbox-native.json) - готові до продакшену налаштування
