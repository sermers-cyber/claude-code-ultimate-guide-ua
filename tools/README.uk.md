# Інтерактивні інструменти

Prompts і утиліти для налаштування та оптимізації Claude Code.

## Зміст

| Файл | Опис | Використання |
|------|-------------|------|
| [audit-prompt.md](./audit-prompt.uk.md) | Комплексний аудит налаштувань із персоналізованими рекомендаціями (8 вимірів, оцінка /100) | `cat audit-prompt.md \| claude` |
| [permissions-audit-prompt.md](./permissions-audit-prompt.uk.md) | Перевірка, чи ваші правила дозволів досі утворюють межу: безумовні дозволи на виконання, покриття deny та ask, стан sandbox (6 фаз, оцінка /100, включно з перевіркою всього парку) | `cat permissions-audit-prompt.md \| claude` |
| [context-audit-prompt.md](./context-audit-prompt.uk.md) | Виміряти та покращити архітектуру контексту | `cat context-audit-prompt.md \| claude` |
| [spec-completeness-audit.md](./spec-completeness-audit.uk.md) | Аудит того, наскільки добре проєкт специфіковано для безпечного делегування агенту (5 шарів специфікації, оцінка /100) | `cat spec-completeness-audit.md \| claude` |
| [audit-cheatsheet-prompt.md](./audit-cheatsheet-prompt.uk.md) | Оцінити, чи потрібен проєкту cheatsheet, і провести аудит наявних | `cat audit-cheatsheet-prompt.md \| claude` |
| [onboarding-prompt.md](./onboarding-prompt.uk.md) | Персоналізований екскурс за вашим профілем | `cat onboarding-prompt.md \| claude` |
| [mobile-access.md](./mobile-access.uk.md) | Посібник із налаштування мобільного доступу через ttyd + Tailscale | Крок за кроком |

## Який аудит коли

| Питання | Інструмент |
|----------|------|
| Чи здорове все моє налаштування? | `audit-prompt.md` |
| Чи справді мої правила дозволів щось обмежують? | `permissions-audit-prompt.md` |
| Чи марную я контекст? | `context-audit-prompt.md` |
| Чи можу я безпечно делегувати тут роботу агенту? | `spec-completeness-audit.md` |
| Чи є в цьому репозиторії секрети або поверхні для ін'єкцій? | `/security-audit` (slash-команда) |

## Швидкий аудит

Для швидкого автоматичного сканування використовуйте скрипт:

```bash
# Pinned to a reviewed commit: download, read, then run, instead of piping a moving branch into bash
AUDIT_SCAN_REF=eab8adc215822f67629b6a0f9366f60a1db9b03c
curl -fsSL "https://raw.githubusercontent.com/FlorianBruniaux/claude-code-ultimate-guide/${AUDIT_SCAN_REF}/examples/scripts/audit-scan.sh" -o audit-scan.sh
less audit-scan.sh
bash audit-scan.sh
```

---

*Назад до [головного README](../README.uk.md)*
