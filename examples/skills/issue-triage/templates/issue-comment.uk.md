# Шаблони коментарів до issues

Використовуйте ці шаблони для генерації коментарів до issues у GitHub під час Фази 3 `/issue-triage`. Коментарі публікуються **англійською** (міжнародна аудиторія).

---

## Шаблон 1 — підтвердження / запит інформації

Використовуйте, коли: issue має статус `Unclear` або `needs-info`, у тілі бракує контексту, немає кроків відтворення.

```markdown
Thanks for opening this issue!

To help us investigate, could you provide the following?

- **Steps to reproduce**: A minimal sequence of actions that triggers the behavior
- **Expected behavior**: What you expected to happen
- **Actual behavior**: What actually happened
- **Environment**: OS, version, relevant config (if applicable)

Once we have this information, we can prioritize and route the issue appropriately.

---
*Triaged via Claude Code /issue-triage*
```

---

## Шаблон 2 — дублікат

Використовуйте, коли: схожість Жаккара >= 60% з наявною відкритою або нещодавно закритою issue.

```markdown
Thanks for reporting this! After reviewing the backlog, this appears to be a duplicate of #{original_number}.

{original_number} is tracking the same underlying behavior: {one-sentence description of original}.

I'm closing this issue to consolidate discussion there. If you believe this is a distinct issue with different root cause or scope, please reopen with additional context explaining the difference.

---
*Triaged via Claude Code /issue-triage*
```

---

## Шаблон 3 — закриття застарілої

Використовуйте, коли: issue не мала активності понад 90 днів і не має виконавця, або немає відповіді на попередній запит інформації понад 30 днів.

```markdown
This issue has been inactive for {days} days without updates or response.

We're closing it to keep the backlog actionable. If this is still relevant to you, please reopen and provide:

- Current status: is this still reproducible?
- Any additional context or workarounds you've found

We're happy to pick this back up if it's still blocking you.

---
*Triaged via Claude Code /issue-triage*
```

---

## Шаблон 4 — закриття як поза межами проєкту

Використовуйте, коли: issue описує функціональність, що явно виходить за заявлені межі проєкту.

```markdown
Thanks for the suggestion! After review, this falls outside the current scope of this project.

{Briefly explain why — e.g., "This project focuses on X; Y is handled by Z" or "This would require changes to the underlying architecture that are not planned."}

You might find what you're looking for in:
- {alternative project or tool if known}
- {documentation link if relevant}

Feel free to open a discussion if you'd like to explore this further.

---
*Triaged via Claude Code /issue-triage*
```

---

## Правила форматування

**Тон**: професійний, прямий, шанобливий. Автор витратив час на створення issue.

**Правила**:
- Ніколи не натякайте, що автор помиляється або марно витратив час
- Будьте конкретними, посилаючись на дублікати (назва + номер, а не лише номер)
- Для закриття застарілої: завжди запрошуйте перевідкрити, не створюйте відчуття остаточності
- Для OOS: пропонуйте альтернативу, коли можливо, навіть якщо вона розпливчаста
- Без найвищих ступенів («чудова issue», «класний звіт») — лише факти

**Точки кастомізації** (замініть у всіх шаблонах):
- `{original_number}`: номер issue-оригіналу, на яку дублікат
- `{one-sentence description}`: короткий опис оригінальної issue
- `{days}`: днів від останньої активності (з `updatedAt`)
- Вбудовані пояснення, позначені `{...}`: завжди заповнюйте перед публікацією

**Підпис** (обов'язковий для всіх коментарів):
```
*Triaged via Claude Code /issue-triage*
```
