# Аудит повноти специфікації для coding agents

> Самодостатній prompt, що перевіряє, наскільки добре кодову базу специфіковано для делегування агентам.
> Ґрунтується на 5-шаровому фреймворку з «Your coding agent is under-specified» Hamidreza Saghir.

**Сценарій використання**: запустіть на будь-якому проєкті перед масштабним делегуванням агентам, щоб виявити прогалини в специфікації, які спричинять непомітний архітектурний дрейф.

**Час**: ~3–5 хв. Жодних змін без явного підтвердження.

---

## Як користуватися

```bash
cd your-project-directory
claude
```

Вставте prompt нижче й натисніть Enter.

---

## Prompt

````markdown
# Аудит повноти специфікації — v1.0

Ти перевіряєш, наскільки добре цей проєкт специфіковано для безпечного делегування агентам.

Мета: знайти прогалини, через які агент мовчки домислюватиме архітектурні,
життєві (lifecycle) та культурні рішення зі своїх тренувальних припущень замість намірів проєкту.

НЕ змінюй жодних файлів. НЕ вноси жодних змін. Лише аудит і звіт.

---

## Фреймворк: 5 шарів специфікації

Кожне завдання з кодування потребує специфікації на 5 шарах. Відсутні шари агенти заповнюють мовчки.

| Шар | Що охоплює | Якщо відсутній, агент заповнює |
|-------|---------------|---------------------------|
| 1. Поведінковий | Що робить код (функції, endpoints, потоки) | Припущення про поведінку з тренувальних даних |
| 2. Інтерфейсний | Типи, контракти помилок, інваріанти, форми I/O | Оптимістична обробка помилок, нещільні типи |
| 3. Архітектурний | Чого НЕ створювати, межі модулів, обмеження повторного використання | Дублювання, порушені межі |
| 4. Життєвий цикл | Як код старіє, що відкладено і чому, наміри щодо підтримки | Короткострокові виправлення, латки |
| 5. Культурний | Командні конвенції, що тут означає «добре», смак | Середня якість публічного коду |

---

## Фаза 1 — Інвентаризація проєкту (bash)

Виконай цей блок. Збережи повний вивід для оцінювання.

```bash
bash -c '
echo "=== PROJECT TYPE ==="
[ -f package.json ] && node -e "const p=require(\"./package.json\"); console.log(\"node:\", p.name, p.version)" 2>/dev/null
[ -f pyproject.toml ] && grep "^name\|^version" pyproject.toml | head -2
[ -f Cargo.toml ] && grep "^name\|^version" Cargo.toml | head -2
[ -f go.mod ] && head -2 go.mod
[ -f *.qmd ] && echo "quarto: documentation project"
[ -d guide ] && echo "docs: guide project"

echo ""
echo "=== SPEC DOCUMENTS ==="
for f in CLAUDE.md .claude/CLAUDE.md README.md AGENTS.md CONTRIBUTING.md \
          docs/ARCHITECTURE.md docs/architecture.md docs/ADR docs/adr \
          .cursor/rules .github/copilot-instructions.md; do
  [ -e "$f" ] && echo "  ✅ $f" || echo "  ❌ $f"
done

echo ""
echo "=== CLAUDE.md COVERAGE (layer mapping) ==="
if [ -f CLAUDE.md ]; then
  wc -l CLAUDE.md | awk "{print \"  Lines:\", \$1}"
  echo "  Layer 1 (behavior): $(grep -ci "what\|feature\|endpoint\|flow\|purpose\|goal\|objective" CLAUDE.md 2>/dev/null || echo 0) keyword hits"
  echo "  Layer 2 (interface): $(grep -ci "type\|schema\|contract\|error\|invariant\|input\|output\|interface" CLAUDE.md 2>/dev/null || echo 0) keyword hits"
  echo "  Layer 3 (arch): $(grep -ci "don.t\|avoid\|never\|not\|boundary\|module\|reuse\|pattern\|structure\|forbidden\|prohibited" CLAUDE.md 2>/dev/null || echo 0) keyword hits"
  echo "  Layer 4 (lifecycle): $(grep -ci "TODO\|defer\|later\|debt\|evolv\|future\|maintain\|migration\|tradeoff" CLAUDE.md 2>/dev/null || echo 0) keyword hits"
  echo "  Layer 5 (culture): $(grep -ci "convention\|style\|taste\|prefer\|standard\|naming\|format" CLAUDE.md 2>/dev/null || echo 0) keyword hits"
else
  echo "  ❌ No CLAUDE.md — all layers unspecified from agent perspective"
fi

echo ""
echo "=== INTERFACE SPEC ==="
# TypeScript
ts_files=$(find . -name "*.ts" -o -name "*.tsx" 2>/dev/null | grep -v node_modules | grep -v .git | wc -l | tr -d " ")
echo "  TypeScript files: $ts_files"
zod=$(grep -rl "z\.\|zod\|Zod" . --include="*.ts" 2>/dev/null | grep -v node_modules | wc -l | tr -d " ")
echo "  Zod schemas: $zod files"

# OpenAPI / swagger
for f in openapi.yaml openapi.json swagger.yaml swagger.json api.yaml; do
  [ -f "$f" ] && echo "  ✅ API spec: $f"
done

# Error handling
error_files=$(grep -rl "catch\|Error\|exception\|throw" . --include="*.ts" --include="*.py" --include="*.rs" 2>/dev/null | grep -v node_modules | wc -l | tr -d " ")
echo "  Files with error handling: $error_files"

echo ""
echo "=== ARCHITECTURAL CONSTRAINTS ==="
# Negative constraints (what NOT to do)
negatives=0
for f in CLAUDE.md .claude/CLAUDE.md .claude/rules/*.md; do
  [ -f "$f" ] && count=$(grep -ci "don.t\|avoid\|never\|do not\|forbidden\|prohibited\|not allowed\|no \(mocks\|stubs\|placeholders\)\|pas de\|jamais\|éviter\|ne pas\|interdit" "$f" 2>/dev/null || echo 0)
  negatives=$(( negatives + count ))
done
echo "  Negative constraints found: $negatives"

# ADR (architecture decision records)
adr_count=0
for d in docs/adr docs/ADR .adr adr; do
  [ -d "$d" ] && adr_count=$(find "$d" -name "*.md" 2>/dev/null | wc -l | tr -d " ") && echo "  ✅ ADR directory: $d ($adr_count records)"
done
[ $adr_count -eq 0 ] && echo "  ❌ No ADR directory"

# Module boundary docs
boundary=$(grep -ril "boundary\|module\|layer\|package\|service\|domain" . --include="*.md" 2>/dev/null | grep -v node_modules | grep -v ".git" | head -5)
[ -n "$boundary" ] && echo "  Module boundary docs:" && echo "$boundary" | sed "s/^/    /" || echo "  ❌ No module boundary documentation"

echo ""
echo "=== LIFECYCLE SPEC ==="
# Technical debt tracking
td=$(grep -rl "TODO\|FIXME\|HACK\|DEBT\|technical.debt" . --include="*.ts" --include="*.py" --include="*.rs" --include="*.md" 2>/dev/null | grep -v node_modules | wc -l | tr -d " ")
echo "  Files with TODO/FIXME/HACK/DEBT: $td"

# Changelog
for f in CHANGELOG.md CHANGELOG.rst docs/CHANGELOG.md; do
  [ -f "$f" ] && wc -l "$f" | awk "{print \"  ✅ Changelog: \" \$1 \" lines\"}"
done

# Migration guides
migrations=$(find . -name "*.md" 2>/dev/null | xargs grep -l "migration\|migrate\|upgrade\|breaking" 2>/dev/null | grep -v node_modules | wc -l | tr -d " ")
echo "  Migration/upgrade docs: $migrations files"

echo ""
echo "=== CULTURAL SPEC ==="
# Linters
for f in .eslintrc* .eslintrc.json .eslintrc.js eslint.config.* .pylintrc pyproject.toml .rubocop.yml; do
  [ -f "$f" ] && echo "  ✅ Linter config: $f"
done

# Formatting
for f in .prettierrc* biome.json .editorconfig rustfmt.toml; do
  [ -f "$f" ] && echo "  ✅ Formatter: $f"
done

# Naming / convention docs
naming=$(grep -rl "naming\|convention\|camelCase\|snake_case\|kebab" . --include="*.md" 2>/dev/null | grep -v node_modules | head -3)
[ -n "$naming" ] && echo "  Convention docs: $naming" || echo "  ❌ No naming/convention documentation"

echo ""
echo "=== REUSE CONSTRAINTS ==="
# Does the agent know what already exists?
reuse=$(grep -ril "already exists\|use existing\|reuse\|don.t create\|see \|refer to" CLAUDE.md .claude/CLAUDE.md .claude/rules/*.md 2>/dev/null | wc -l | tr -d " ")
echo "  Reuse/existing-code references in specs: $reuse"

# Map of what exists (README sections, module index)
index_quality=0
[ -f README.md ] && index_quality=$(wc -l < README.md | tr -d " ")
echo "  README lines: $index_quality"
'
```

---

## Фаза 2 — Оцінювання по шарах

Оціни кожен шар. Використай вивід Фази 1. За потреби прочитай ключові файли.

### Шар 1 — Поведінкова специфікація (15 балів)

**Що перевірити**: чи може агент зрозуміти, що має робити цей проєкт (функції, користувацькі потоки, критерії приймання), не вгадуючи?

Прочитай верхній розділ README.md, якщо він є.

Оцінювання:
- README з призначенням і ключовими функціями: 5 балів (3, якщо мінімальний, 0, якщо відсутній)
- CLAUDE.md описує, що робить проєкт: 3 бали
- Існують критерії приймання або контракти функцій (тести як специфікація, описи тестів, feature-файли): 4 бали
- Відстеження завдань/issues підключене або узагальнене там, де його бачить агент: 3 бали

### Шар 2 — Інтерфейсна специфікація (20 балів)

**Що перевірити**: чи є форми вводу/виводу, контракти помилок та інваріанти машинозчитуваними або задокументованими?

```bash
# Sample 3 key files for type coverage quality
find . -name "*.ts" -o -name "*.tsx" 2>/dev/null | grep -v node_modules | grep -v ".git" | \
  shuf 2>/dev/null | head -3 | xargs grep -l "interface\|type\|z\.\|Schema" 2>/dev/null | head -3
```

Коротко прочитай 1-2 файли з вибірки, щоб оцінити якість типізації.

Оцінювання:
- TypeScript у strict mode АБО типізований Python (mypy/pyright) АБО Rust (автоматично): 6 балів (3, якщо частково)
- Zod/Pydantic/Joi або еквівалентна валідація схем на межах: 4 бали
- Обробка помилок явна, з типізованими помилками (а не просто загальний catch): 4 бали
- Контракти API задокументовані (OpenAPI, tRPC, схема GraphQL, Protobuf): 4 бали
- Інваріанти задокументовані (передумови/постумови, переходи станів): 2 бали

### Шар 3 — Архітектурна специфікація (30 балів)

**Це найчастіше відсутній шар. Вага це відображає.**

**Що перевірити**: чи знає агент, чого НЕ створювати, як усе поєднується між собою і що вже існує?

Прочитай архітектурні розділи CLAUDE.md, якщо вони є. Перевір наявність ADR.

```bash
# Check CLAUDE.md for architectural content depth
[ -f CLAUDE.md ] && grep -n "not\|avoid\|don.t\|never\|boundary\|module\|reuse\|exist\|pattern\|structure" CLAUDE.md | head -20
```

Оцінювання:
- CLAUDE.md містить явні негативні обмеження («ніколи не створюй X», «не вводь Y», «повторно використовуй Z»): 8 балів (4, якщо неявні/слабкі, 0, якщо відсутні)
- Межі модулів/сервісів задокументовані: 6 балів
- «Що вже існує» доступне агенту (індекс, мапа, reference.yaml або подібне): 6 балів
- ADR або еквівалентний журнал архітектурних рішень: 5 балів
- Патерни, які використовує кодова база, названі й пояснені: 5 балів

### Шар 4 — Специфікація життєвого циклу (20 балів)

**Що перевірити**: чи знає агент, що свідомо відкладено, що є боргом і яких майбутніх змін очікувати?

Оцінювання:
- CHANGELOG.md існує й підтримується: 4 бали
- Маркери TODO/FIXME/DEBT змістовні (мають контекст, а не просто «виправити потім»): 4 бали (перевір вибірку)
- Політика breaking changes задокументована: 3 бали
- Відомий технічний борг задокументований із обґрунтуванням: 5 балів
- Заплановані зміни або roadmap видимі агенту: 4 бали

### Шар 5 — Культурна специфікація (15 балів)

**Що перевірити**: чи знає агент, як виглядає «добре» саме для цієї кодової бази?

Оцінювання:
- Конфігурація linter забезпечує стиль коду: 3 бали
- Конфігурація formatter забезпечує форматування: 2 бали
- Конвенції іменування явно задокументовані: 3 бали
- Критерії code review або планка якості задокументовані: 3 бали
- Є посилання на приклади «доброго» коду або вони присутні: 2 бали
- Заборонені патерни закодовані (у linter або CLAUDE.md): 2 бали

---

## Фаза 3 — Оцінка ризику домислювання прогалин

Для кожного шару з оцінкою нижче 60% оціни, що агент мовчки домислить.

```
Шар X (N/макс. балів) — РИЗИК: [низький/середній/високий/критичний]
Мовчазні домислювання: [перелік 2-3 конкретних рішень, які агент ухвалить зі своїх тренувальних припущень]
Найнебезпечніше: [те, що найімовірніше спричинить незворотний архітектурний дрейф]
```

Конкретні приклади:
- Відсутній L3 + незнайома кодова база = агент створює новий модуль автентифікації замість того, щоб знайти наявний
- Відсутні контракти помилок L2 = агент пише оптимістичну обробку помилок, повертає 200 при частковому збої
- Відсутній життєвий цикл L4 = агент «виправляє» навмисні скорочення, порушуючи контракт відомого боргу
- Відсутня культура L5 = агент використовує свій найпоширеніший тренувальний патерн, а не ваш

---

## Фаза 4 — Єдиний звіт

### Короткий підсумок

```
Загальна оцінка: X/100
Рівень ризику: Safe (80+) | Supervised (60-79) | Risky (40-59) | Unsafe (<40)

Ризик домислювання: [які шари породять найнебезпечніші мовчазні рішення]
Топ-3 виправлень із найвищим ROI: [відсортовано за: вплив × час на впровадження]
```

### Таблиця оцінок по шарах

| Шар | Назва | Оцінка | Макс. | Ризик | Ключова прогалина |
|-------|------|-------|-----|------|---------|
| 1 | Поведінковий | X | 15 | 🟢/🟡/🔴 | один рядок |
| 2 | Інтерфейсний | X | 20 | 🟢/🟡/🔴 | один рядок |
| 3 | Архітектурний | X | 30 | 🟢/🟡/🔴 | один рядок |
| 4 | Життєвий цикл | X | 20 | 🟢/🟡/🔴 | один рядок |
| 5 | Культурний | X | 15 | 🟢/🟡/🔴 | один рядок |
| | **РАЗОМ** | **X** | **100** | | |

Ризик: 🟢 ≥80% | 🟡 50–79% | 🔴 <50%

### Детальні знахідки

Для кожної прогалини 🔴 і 🟡:

```
[Шар N — Назва]
Прогалина: чого бракує
Мовчазне домислювання: що агент вигадає, щоб її заповнити
Виправлення: конкретний файл для створення або розділ для додавання (з прикладом вмісту)
Трудомісткість: <30 хв / 1 год / півдня
```

### Вердикт щодо делегування

На основі загальної оцінки явно вкажи:

- **Оцінка ≥80**: безпечно для широкого делегування. Задокументуй решту прогалин у CLAUDE.md перед кожним завданням.
- **Оцінка 60–79**: делегуй з обмеженнями. Вказуй архітектурний шар у кожному prompt. Переглядай кожен commit.
- **Оцінка 40–59**: режим посиленого нагляду. Визначай L3 перед кожним делегуванням. Використовуй plan-mode + review agent.
- **Оцінка <40**: не делегуй архітектурну роботу. Лише завдання з кодування з вичерпними специфікаціями на кожне завдання.

---

## Фаза 5 — Швидкі перемоги

Перелічи 3 покращення з найвищим ROI, кожне з:

1. Точним файлом для створення чи зміни
2. Мінімальним шаблоном, який можна додати просто зараз
3. Оцінкою трудомісткості

Потім запитай:

«Впровадити ці швидкі перемоги?
- **yes** → впровадити всі три
- **1, 3** → окремі пункти
- **none** → залишити звіт, без змін»

Дочекайся явної відповіді користувача, перш ніж щось робити.
````

---

## Розуміння результатів

### Рівні ризику

| Оцінка | Рівень | Підхід до делегування агентам |
|-------|------|--------------------------|
| 80–100 | Safe | Широке делегування допустиме. Коротке нагадування про архітектуру на кожне завдання. |
| 60–79 | Supervised | Делегуй з явними обмеженнями L3 на кожне завдання. Переглядай кожен commit. |
| 40–59 | Risky | Plan-mode + reviewer agent. Вказуй архітектуру перед кожною сесією. |
| <40 | Unsafe | Лише завдання з кодування, ніколи архітектурні. Вичерпні специфікації на кожне завдання. |

### Шар, що важить найбільше

**Шар 3 (Архітектурний, 30 балів)** має найбільшу вагу, бо він і найчастіше відсутній, і найважче виявляється, коли помилковий. Агент, який правильно виконує L1, але провалює L3, пише код, що працює сьогодні й гниє вже наступного місяця. Жоден тест цього не ловить.

### Що означає «Safe»

Проєкт з оцінкою 80+ усе одно потребує доповнення prompt специфікою шарів для кожного завдання. «Safe» означає, що в агента достатньо контексту, щоб уникнути найгірших мовчазних домислювань, а не що можна делегувати й піти.

---

## Пов'язане

- [`tools/audit-prompt.md`](audit-prompt.uk.md) — аудит налаштувань Claude Code (безпека, rules, пам'ять, MCP)
- [`tools/context-audit-prompt.md`](context-audit-prompt.uk.md) — бюджет токенів і context engineering
- Джерело: Hamidreza Saghir, «Your coding agent is under-specified» (травень 2026)

---

*Версія 1.0 — spec-completeness-audit*
