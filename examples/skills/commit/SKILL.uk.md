---
name: commit
description: Згенерувати повідомлення коміту у форматі conventional commit для проіндексованих змін
argument-hint: "[--amend] [message]"
effort: low
when_to_use: "Використовуйте, коли готові закомітити проіндексовані зміни й потрібне повідомлення у форматі conventional commit."
disable-model-invocation: true
---

# Conventional commit

Згенеруйте повідомлення коміту у форматі conventional commit для проіндексованих змін.

## Інструкції

1. Запустіть `git diff --cached`, щоб побачити проіндексовані зміни
2. Проаналізуйте характер змін
3. Згенеруйте повідомлення коміту в наведеному нижче форматі

## Формат коміту

```
<type>(<scope>): <subject>

[optional body]

[optional footer]
```

### Типи
- `feat`: нова функціональність
- `fix`: виправлення бага
- `docs`: лише документація
- `style`: форматування, пропущені крапки з комою тощо
- `refactor`: зміна коду, що не виправляє баг і не додає функціональності
- `perf`: покращення продуктивності
- `test`: додавання відсутніх тестів
- `chore`: завдання з обслуговування

### Правила
- Subject: наказовий спосіб, без крапки в кінці, максимум 50 символів
- Body: пояснюйте ЩО і ЧОМУ, а не ЯК
- Footer: несумісні зміни, посилання на issues

## Приклади

```
feat(auth): add password reset functionality

Implement password reset flow with email verification.
Users can now request a reset link and set new password.

Closes #123
```

```
fix(api): prevent race condition in order processing

Add mutex lock to ensure orders are processed sequentially.
This fixes duplicate charge issues reported by users.

Fixes #456
```

```
refactor(cart): extract pricing logic to separate module

No functional changes. Improves testability and
separates concerns for future discount feature.
```

## Виконання

Проаналізувавши проіндексовані зміни, запропонуйте повідомлення коміту.
Перед виконанням `git commit -m "..."` попросіть підтвердження.

$ARGUMENTS
