---
title: "Патерни надійності у продакшені"
description: "Проєктування ескалації, circuit breakers, структурована передача помилок, плавна деградація, передача людині та розв'язання конфліктів джерел для систем на базі Claude"
tags: [workflow, reliability, production, escalation, circuit-breaker, error-handling]
---

# Патерни надійності у продакшені

> **Рівень довіри**: Tier 2. Патерни, виведені з продакшен-розгортань. Базові принципи проєктування стабільні; конкретні пороги та назви полів залежатимуть від системи.

Системи на базі Claude дають збої інакше, ніж традиційне програмне забезпечення. Модель може згенерувати синтаксично коректний, але семантично хибний результат, може відмовитися продовжувати, коли не може просунутися далі, або видати часткові результати, коли вихідні дані неповні. Наведені нижче патерни розв'язують кожен із цих режимів збою в продакшені.

---

## Зміст

1. [Проєктування ескалації](#проєктування-ескалації)
2. [Патерн Circuit Breaker](#патерн-circuit-breaker)
3. [Структурована передача помилок](#структурована-передача-помилок)
4. [Часткові результати та анотації покриття](#часткові-результати-та-анотації-покриття)
5. [Структурована передача людині](#структурована-передача-людині)
6. [Розв'язання конфліктів джерел](#розвязання-конфліктів-джерел)
7. [Антипатерни](#антипатерни)
8. [Дивіться також](#дивіться-також)

---

## Проєктування ескалації

Найпоширеніша помилка надійності — використання показників упевненості LLM як основного сигналу ескалації. Показники упевненості не є каліброваними ймовірностями: модель може вивести високе значення упевненості, помиляючись по суті. Ескалацію в продакшені мають визначати програмні сигнали, а не числові значення упевненості.

### Три канонічні тригери ескалації

У добре спроєктованій системі ескалація відбувається, коли виконується рівно одна з трьох умов.

**1. Явний запит користувача:** Клієнт прямо просить людину. Це не обговорюється і має пріоритет над будь-яким іншим сигналом, зокрема над виявленням роздратування. «Я хочу поговорити з людиною» — це інший сигнал, ніж сердитий тон, і він вимагає негайної передачі незалежно від того, що ШІ міг би зробити далі.

**2. Прогалина в політиці:** Запит виходить за визначені межі системи й не може бути оброблений жодним доступним інструментом чи знанням. Це не збій моделі, а межа обсягу. Правильна відповідь — структурована ескалація з контекстом, а не цикл вибачень.

**3. Неможливість просунутися:** Після визначеної кількості спроб чи викликів інструментів система не видала валідного результату. Це вимірюється програмно: вичерпано бюджет повторних спроб, circuit breaker відкритий або цикл валідації провалився.

### Програмні сигнали ескалації

```python
from enum import Enum
from dataclasses import dataclass

class EscalationReason(Enum):
    EXPLICIT_REQUEST = "explicit_request"
    POLICY_GAP = "policy_gap"
    MAX_RETRIES_EXCEEDED = "max_retries_exceeded"
    CIRCUIT_BREAKER_OPEN = "circuit_breaker_open"
    MISSING_REQUIRED_TOOL = "missing_required_tool"

@dataclass
class EscalationSignal:
    should_escalate: bool
    reason: EscalationReason | None
    context: dict

def evaluate_escalation(
    user_message: str,
    attempt_count: int,
    policy_coverage: str,  # "covered" | "gap" | "out_of_scope"
    max_attempts: int = 3
) -> EscalationSignal:

    # Пріоритет 1: явний запит користувача, перевіряємо першим, безумовно
    if contains_explicit_escalation_request(user_message):
        return EscalationSignal(
            should_escalate=True,
            reason=EscalationReason.EXPLICIT_REQUEST,
            context={"trigger": "user_stated_intent"}
        )

    # Пріоритет 2: прогалина в політиці
    if policy_coverage in ("gap", "out_of_scope"):
        return EscalationSignal(
            should_escalate=True,
            reason=EscalationReason.POLICY_GAP,
            context={"coverage": policy_coverage}
        )

    # Пріоритет 3: неможливість просунутися
    if attempt_count >= max_attempts:
        return EscalationSignal(
            should_escalate=True,
            reason=EscalationReason.MAX_RETRIES_EXCEEDED,
            context={"attempts": attempt_count, "max": max_attempts}
        )

    return EscalationSignal(should_escalate=False, reason=None, context={})

def contains_explicit_escalation_request(message: str) -> bool:
    explicit_phrases = [
        "speak to a human", "talk to a person", "real agent",
        "human agent", "transfer me", "escalate this",
        "supervisor", "manager"
    ]
    message_lower = message.lower()
    return any(phrase in message_lower for phrase in explicit_phrases)
```

### Роздратування проти явної ескалації

Це два абсолютно різні сигнали, що потребують протилежних реакцій. Роздратування (сердитий тон, повторювані запитання, «це марно») — сигнал визнати проблему з емпатією та спробувати інший підхід. Явний запит на ескалацію («Я хочу поговорити з людиною») — сигнал негайно передати розмову.

Змішувати їх — поширена помилка з реальними наслідками: спрямовувати роздратованих користувачів до людей, коли вони просто хотіли кращої відповіді, або продовжувати старатися, коли користувач уже вирішив, що хоче людину-агента.

```python
def classify_user_signal(message: str) -> dict:
    # Ці патерни можуть співіснувати: перевіряємо обидва незалежно
    frustration_markers = [
        "this is ridiculous", "not helpful", "keep asking",
        "not answering", "useless", "terrible", "waste"
    ]
    escalation_markers = [
        "speak to a human", "real person", "agent", "transfer",
        "supervisor", "escalate", "don't want ai"
    ]

    message_lower = message.lower()

    return {
        "frustrated": any(m in message_lower for m in frustration_markers),
        "wants_escalation": any(m in message_lower for m in escalation_markers)
    }

# Використання:
signals = classify_user_signal(user_message)

if signals["wants_escalation"]:
    initiate_human_handoff(context)   # негайно, безумовно
elif signals["frustrated"]:
    adjust_response_approach()        # емпатичніше, з іншого боку
```

### Маршрутизація за правилами зі структурованого виводу

Де можливо, виводьте рішення про ескалацію зі структурованих полів виводу, а не з упевненості на рівні моделі. Якщо модель видає структурований результат із `policy_gap: true` або `requires_human_review: true`, ці поля є детермінованими сигналами маршрутизації, і тлумачення показника упевненості не потрібне.

```python
@dataclass
class AgentDecision:
    response_text: str
    policy_gap: bool
    requires_human_review: bool
    coverage_level: str  # "full" | "partial" | "none"
    missing_information: list[str]

def route_from_structured_output(decision: AgentDecision) -> str:
    if decision.policy_gap or decision.coverage_level == "none":
        return "escalate"
    if decision.requires_human_review or decision.coverage_level == "partial":
        return "queue_for_review"
    return "respond"
```

---

## Патерн Circuit Breaker

Circuit breaker не дає збійній залежності (API, інструменту, зовнішньому сервісу) спричинити каскадні збої. Без нього кожен виклик агента, що торкається збійного сервісу, зависатиме до тайм-ауту, споживаючи ресурси та погіршуючи роботу всього конвеєра.

```python
import time
from enum import Enum

class CircuitState(Enum):
    CLOSED = "closed"        # нормальна робота
    OPEN = "open"            # збій, негайно відхиляти виклики
    HALF_OPEN = "half_open"  # перевірка відновлення

class CircuitBreaker:
    def __init__(
        self,
        failure_threshold: int = 5,
        recovery_timeout: float = 60.0,
        success_threshold: int = 2
    ):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.success_threshold = success_threshold

        self.state = CircuitState.CLOSED
        self.failure_count = 0
        self.success_count = 0
        self.last_failure_time: float | None = None

    def call(self, func, *args, **kwargs):
        if self.state == CircuitState.OPEN:
            if self._should_attempt_recovery():
                self.state = CircuitState.HALF_OPEN
                self.success_count = 0
            else:
                raise CircuitOpenError(
                    f"Circuit open since {self.last_failure_time:.0f}. "
                    f"Recovery in {self._time_until_recovery():.0f}s"
                )

        try:
            result = func(*args, **kwargs)
            self._on_success()
            return result
        except Exception:
            self._on_failure()
            raise

    def _on_success(self):
        if self.state == CircuitState.HALF_OPEN:
            self.success_count += 1
            if self.success_count >= self.success_threshold:
                self.state = CircuitState.CLOSED
                self.failure_count = 0

    def _on_failure(self):
        self.failure_count += 1
        self.last_failure_time = time.time()
        if self.failure_count >= self.failure_threshold:
            self.state = CircuitState.OPEN

    def _should_attempt_recovery(self) -> bool:
        if self.last_failure_time is None:
            return True
        return time.time() - self.last_failure_time >= self.recovery_timeout

    def _time_until_recovery(self) -> float:
        if self.last_failure_time is None:
            return 0.0
        return max(0.0, self.recovery_timeout - (time.time() - self.last_failure_time))

class CircuitOpenError(Exception):
    pass
```

### Ізоляція на рівні документа в пакетних конвеєрах

У конвеєрах пакетної обробки кожен документ має мати власну межу помилок. Збій одного документа не повинен переривати решту пакета.

```python
def process_document_batch(documents: list[str], processor) -> list[dict]:
    results = []
    circuit_breaker = CircuitBreaker(failure_threshold=3, recovery_timeout=30.0)

    for doc_id, document in enumerate(documents):
        try:
            result = circuit_breaker.call(processor, document)
            results.append({"doc_id": doc_id, "status": "success", "result": result})
        except CircuitOpenError as e:
            # Circuit відкритий: пропустити решту документів і повідомити про стан вище
            results.append({"doc_id": doc_id, "status": "circuit_open", "error": str(e)})
            for remaining_id in range(doc_id + 1, len(documents)):
                results.append({
                    "doc_id": remaining_id,
                    "status": "skipped",
                    "reason": "circuit_open"
                })
            break
        except Exception as e:
            results.append({"doc_id": doc_id, "status": "error", "error": str(e)})

    return results
```

Circuit breaker замикається на рівні пакета, а не документа. Коли він відкривається, ви хочете знати, що базовий сервіс недоступний, а не те, що три окремі документи випадково провалилися підряд.

---

## Структурована передача помилок

У мультиагентних системах помилки, передані як загальні рядки винятків, втрачають контекст, потрібний для відновлення. Структуровані помилки несуть інформацію, за якою оркестратор вище вирішує, чи повторити спробу, перемаршрутизувати чи ескалувати.

```python
from dataclasses import dataclass

@dataclass
class StructuredAgentError:
    error_category: str           # "tool_failure" | "validation_error" | "policy_gap" | "timeout"
    is_retryable: bool
    failure_type: str             # конкретний підтип у межах категорії
    attempted_query: str | None   # що було спробувано (корисно для налагодження)
    partial_results: dict | None  # будь-який придатний вивід, отриманий до збою
    alternative_approach: str | None  # пропозиція для оркестратора
    error_message: str
    attempt_count: int = 1

    def to_dict(self) -> dict:
        return {
            "error_category": self.error_category,
            "is_retryable": self.is_retryable,
            "failure_type": self.failure_type,
            "attempted_query": self.attempted_query,
            "has_partial_results": self.partial_results is not None,
            "alternative_approach": self.alternative_approach,
            "error_message": self.error_message,
            "attempt_count": self.attempt_count
        }

# Використання в субагенті:
def search_database(query: str) -> dict:
    try:
        return db.search(query)
    except DatabaseTimeoutError:
        raise StructuredAgentError(
            error_category="tool_failure",
            is_retryable=True,
            failure_type="database_timeout",
            attempted_query=query,
            partial_results=None,
            alternative_approach="retry with narrower query or use cached results",
            error_message="Database query timed out after 30s"
        )
    except NoResultsError:
        raise StructuredAgentError(
            error_category="tool_failure",
            is_retryable=False,
            failure_type="no_results",
            attempted_query=query,
            partial_results=None,
            alternative_approach="try broader search terms or escalate to human",
            error_message=f"No results found for query: {query}"
        )

# Обробка в оркестраторі:
def orchestrate_with_recovery(agent_fn, query: str, max_retries: int = 2) -> dict:
    for attempt in range(max_retries + 1):
        try:
            return agent_fn(query)
        except StructuredAgentError as e:
            if not e.is_retryable or attempt == max_retries:
                return {
                    "status": "failed",
                    "error": e.to_dict(),
                    "partial_results": e.partial_results,
                    "requires_escalation": not e.is_retryable
                }
            # Можна повторити: застосувати запропонований альтернативний підхід, якщо він є
            if e.alternative_approach:
                query = refine_query(query, e.alternative_approach)
```

Ключове поле — `is_retryable`. Оркестратор, який не може відрізнити, чи повторювати спробу, чи ескалувати, за замовчуванням повторюватиме все: це марнує бюджет на помилки, які повторенню не підлягають, і втрачає шанс на тимчасових.

---

## Часткові результати та анотації покриття

Коли конвеєр не може повністю виконати завдання, повернення часткових результатів із явними анотаціями покриття корисніше, ніж не повертати нічого. Споживач тоді може вирішити, чи придатний частковий результат до дії, не розбираючись у внутрішній будові того, що саме збійнуло.

```python
from dataclasses import dataclass

@dataclass
class AnalysisResult:
    full_analysis: str | None
    section_results: dict[str, dict]  # section_id -> результат
    coverage_summary: dict

def annotate_coverage(section_results: dict) -> dict:
    coverage_map = {}
    for section_id, result in section_results.items():
        if result.get("status") == "success" and result.get("confidence", 0) >= 0.8:
            coverage_map[section_id] = "well-supported"
        elif result.get("status") == "success":
            coverage_map[section_id] = "partially-supported"
        else:
            coverage_map[section_id] = "gap"

    counts = {"well-supported": 0, "partially-supported": 0, "gap": 0}
    for v in coverage_map.values():
        counts[v] += 1

    return {
        "sections": coverage_map,
        "counts": counts,
        "overall_coverage": counts["well-supported"] / len(coverage_map) if coverage_map else 0.0,
        "has_gaps": counts["gap"] > 0
    }
```

Виводьте анотації покриття у відповіді, щоб споживачі нижче за потоком могли діяти на їх основі без розбору внутрішнього стану:

```
CONTRACT ANALYSIS SUMMARY

Section 1 (Payment Terms): well-supported (full analysis available)
Section 2 (Liability Clauses): partially-supported (analysis based on partial text; recommend manual review)
Section 3 (Termination Rights): gap (source text was unreadable; human review required)

Overall coverage: 67% (2 of 3 sections fully analyzed)
```

Цей патерн застосовний скрізь, де конвеєр може видати неповний результат: витяг із документів, дослідження з кількох джерел, пакетний переклад або перевірки регуляторної відповідності, де для деяких положень бракує підтверджувальних даних.

---

## Структурована передача людині

Коли відбувається ескалація, людина-агент отримує структуроване навантаження, а не сиру історію розмови. Мета в тому, щоб людина могла почати працювати протягом 30 секунд, не перечитуючи весь журнал розмови.

```python
from dataclasses import dataclass
from datetime import datetime

@dataclass
class HandoffPayload:
    customer_id: str
    session_id: str
    escalation_reason: str        # з enum EscalationReason
    original_request: str         # дослівне перше повідомлення користувача
    conversation_summary: str     # підсумок того, що сталося, у 3-5 реченнях
    root_cause: str               # чому ШІ не зміг це розв'язати
    actions_taken: list[str]      # що було спробувано
    recommended_next_action: str  # конкретна пропозиція для людини-агента
    partial_results: dict | None  # будь-який корисний вивід
    urgency: str                  # "high" | "medium" | "low"
    created_at: str               # ISO 8601

def build_handoff(
    session: dict,
    escalation_signal: EscalationSignal,
    conversation_history: list[dict]
) -> HandoffPayload:
    return HandoffPayload(
        customer_id=session["customer_id"],
        session_id=session["session_id"],
        escalation_reason=escalation_signal.reason.value,
        original_request=conversation_history[0]["content"] if conversation_history else "",
        conversation_summary=summarize_conversation(conversation_history),
        root_cause=derive_root_cause(escalation_signal),
        actions_taken=extract_actions_taken(session),
        recommended_next_action=suggest_next_action(escalation_signal),
        partial_results=session.get("partial_results"),
        urgency="high" if escalation_signal.reason == EscalationReason.EXPLICIT_REQUEST else "medium",
        created_at=datetime.utcnow().isoformat()
    )
```

### Формат відображення передачі

Те, що людина-агент бачить насправді, має читатися як структурований бриф, а не як вивантаження даних:

```
ESCALATION BRIEF: Session a1b2c3d4
Reason: Customer requested human agent
Urgency: HIGH

ORIGINAL REQUEST
"I need to cancel my subscription and get a refund for last month's charge"

WHAT HAPPENED
The customer asked to cancel their subscription and requested a refund for the
charge processed on May 18. The AI confirmed account details and found the charge
($49.00) but hit a policy gap: refund approval for charges older than 7 days
requires manual authorization. Two escalation attempts were made; the customer
then explicitly requested a human agent.

ACTIONS TAKEN
- Account verified (customer_id: 88821)
- Charge located: $49.00 on 2026-05-18
- Subscription status: active

RECOMMENDED NEXT ACTION
Authorize refund for $49.00 (charge is 6 days old, within 7-day window) and
process cancellation. No additional verification needed.
```

Поле `recommended_next_action` — найцінніша частина. Людина-агент, яка отримує конкретну рекомендацію, розв'язує випадок швидше й рідше просить клієнта повторювати інформацію.

---

## Розв'язання конфліктів джерел

Коли кілька джерел розходяться, стратегія розв'язання залежить від того, чому вони розходяться. Часові відмінності (одне джерело новіше за інше) потребують іншого підходу, ніж фактичні конфлікти (джерела про один і той самий період розходяться у фактах).

```python
@dataclass
class Source:
    source_id: str
    content: str
    publication_date: str | None  # ISO 8601, обов'язкове для часового розрізнення
    source_type: str              # "official" | "news" | "user_generated" | "internal"
    authority_score: float        # 0.0-1.0, залежить від предметної області

def resolve_conflict(sources: list[Source], field: str) -> dict:
    values = [s for s in sources if get_field_value(s, field) is not None]

    if len(values) <= 1:
        return {"resolved": values[0] if values else None, "conflict": False}

    # Спершу перевіряємо часову різницю
    dated = [s for s in values if s.publication_date is not None]
    if len(dated) == len(values):
        sorted_by_date = sorted(dated, key=lambda s: s.publication_date, reverse=True)
        newest = sorted_by_date[0]
        second_newest = sorted_by_date[1] if len(sorted_by_date) > 1 else None

        if (second_newest is not None and
                get_field_value(newest, field) == get_field_value(second_newest, field)):
            # Два найновіших джерела збігаються: ймовірно, коректне оновлення
            return {
                "resolved": newest,
                "conflict": False,
                "resolution_method": "temporal_precedence"
            }

    # Справжній фактичний конфлікт: не розв'язувати автоматично
    return {
        "resolved": None,
        "conflict": True,
        "conflict_type": "factual",
        "conflicting_sources": [s.source_id for s in values],
        "requires_human_review": True
    }
```

Завжди включайте `publication_date` у метадані джерела. Без неї часове розрізнення неможлива, і те, що виглядає як фактичний конфлікт, може бути просто застарілим джерелом, яке ще не вивели з обігу.

### Виведення конфліктів у результат

Коли справжній конфлікт не можна розв'язати автоматично, виводьте його явно, а не мовчки обирайте одне джерело:

```
FIELD: regulatory_status

SOURCE A (internal-policy-doc, 2026-01-15): "Approved for EU markets"
SOURCE B (legal-review-2026, 2026-03-22): "Pending re-approval: EU regulatory update in progress"

CONFLICT TYPE: factual (same field, same jurisdiction, different values)
RESOLUTION: Cannot auto-resolve. Human review required before using this field.
```

Це краще, ніж повертати єдину відповідь без атрибуції. Споживач, який бачить упевнену відповідь, не знаючи, що її оскаржували, не може зробити обґрунтоване рішення, чи діяти на її підставі.

---

## Антипатерни

**Використання показників упевненості як логіки маршрутизації.** Показники упевненості LLM не є каліброваними ймовірностями. Натомість використовуйте програмні сигнали: кількість повторних спроб, стан circuit, поля структурованого виводу.

**Змішування роздратування з наміром ескалації.** Роздратовані користувачі часто хочуть кращої відповіді, а не людини. Користувачі, які кажуть «Я хочу людину», завжди хочуть людину. Ставтеся до них як до окремих сигналів з окремими реакціями.

**Передача неструктурованих винятків між агентами.** Рядок на кшталт `"DatabaseError: connection refused"` нічого не каже оркестратору про те, чи повторювати спробу, чи ескалувати. Використовуйте структуровані типи помилок з `is_retryable`, `error_category` та `alternative_approach`.

**Повернення нічого, коли частковий результат існує.** Частковий результат із чіткою анотацією покриття майже завжди корисніший за порожню відповідь з повідомленням про помилку. Споживач може вирішити, що робити з «покриття 67%»; з «аналіз не вдався» він не може вирішити нічого.

**Пропуск `publication_date` у метаданих джерела.** Без дат часові конфлікти виглядають як фактичні. Кожне джерело, що надходить у конвеєр, має нести дату, навіть приблизну.

**Побудова передач як вивантажень розмови.** Вставлення останніх 20 реплік розмови в тікет не є передачею; це перекладання роботи. Структуроване навантаження передачі з `recommended_next_action` відрізняє хорошу систему ескалації від повільної.

---

## Дивіться також

- [Agent Teams](agent-teams.uk.md): архітектура оркестратора/субагентів і маршрутизація інструментів
- [Event-Driven Agents](event-driven-agents.uk.md): автоматизація на основі тригерів і цикли повторних спроб
- [Task Management](task-management.uk.md): постійний стан для багатокрокових робочих процесів агентів
- [Plan-Driven Workflow](plan-driven.uk.md): етап планування перед виконанням для зменшення збоїв посеред завдання
