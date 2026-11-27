# Інструкції для ШІ: {{DEVELOPER_NAME}}
<!-- Generated: {{GENERATED_DATE}} | OS: {{OS}} | Tool: {{TOOL}} -->
<!-- НЕ РЕДАГУВАТИ ВРУЧНУ — згенеровано автоматично з профілю + модулів -->
<!-- Щоб оновити: відредагуйте profiles/{{DEVELOPER_SLUG}}.yaml або modules/, потім виконайте: -->
<!-- npx ts-node sync-ai-instructions.ts {{DEVELOPER_SLUG}} -->

---

## Контекст проєкту

{{MODULE:core-standards}}

---

## Git-воркфлоу

{{MODULE:git-workflow}}

---

## Тестування

{{MODULE:test-conventions}}

---

{{#if typescript}}
## Правила TypeScript

{{MODULE:typescript-rules}}

---
{{/if}}

{{#if python}}
## Правила Python

{{MODULE:python-rules}}

---
{{/if}}

## Середовище та шляхи

{{MODULE:{{OS}}-paths}}

---

{{#if cursor}}
## Інструкції для Cursor

{{MODULE:cursor-rules}}

---
{{/if}}

{{#if windsurf}}
## Інструкції для Windsurf

{{MODULE:windsurf-rules}}

---
{{/if}}

## Стиль комунікації

{{#if verbose}}
Надавайте докладні пояснення для кожного рішення. Показуйте розглянуті альтернативи. Наводьте міркування.
{{/if}}
{{#if concise}}
Будьте стислими. Одне речення на пункт. Пропускайте очевидні деталі.
{{/if}}
{{#if terse}}
Мінімальний вивід. Де можливо, лише код. Без пояснень, якщо про них не просили.
{{/if}}
