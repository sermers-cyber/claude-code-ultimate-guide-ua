# Плагін DevOps pipeline

Автоматизація CI/CD, розгортання та керування інфраструктурою.

## Встановлення

```bash
bash install.sh
```

## Компоненти

- **Агент devops-sre**: спеціаліст з інфраструктури та розгортання
- **Команда /ship**: повний воркфлоу розгортання
- **Воркфлоу GitHub Actions**: автоматизований CI/CD у вашому репозиторії

## Швидкий старт

```bash
# Deploy to production
/ship --env production

# Check deployment status
!git log --oneline -5

# Configure CI/CD
# Review .github/workflows/claude-code-review.yml
```

## Можливості

✓ Автоматизовані розгортання
✓ Валідація інфраструктури
✓ Підтримка відкату
✓ Моніторинг стану
✓ Інтеграція зі сповіщеннями

---

Повну документацію дивіться в `guide/ops/devops-sre.md`.
