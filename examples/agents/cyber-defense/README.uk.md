# Команда агентів кіберзахисту

Конвеєр із 4 агентів, що виявляє загрози безпеці у файлах логів. Побудований нативно на Claude Code Agent Teams.

**Цей приклад існує, щоб порівняти два підходи**: LangGraph (Python-фреймворк) і Claude Code Agent Teams (нативний). Та сама система, дві архітектури. Різниця між ними підказує, коли що використовувати.

---

## Архітектура

```
log-ingestor (haiku)
      ↓
anomaly-detector (sonnet)
      ↓
risk-classifier (sonnet)
      ↓
threat-reporter (sonnet)
      ↓
cyber-defense-report.md
```

Кожен агент має єдиний обов'язок і передає дані наступному через спільні JSON-файли. Skill оркестрації (`/cyber-defense-team`) задає послідовність запусків і повідомляє результати.

**Використання**: `/cyber-defense-team /var/log/nginx/access.log`

---

## LangGraph і Claude Code agent teams

Ту саму систему побудовано двічі. Ось повне порівняння.

### Версія на LangGraph (~150 рядків Python)

```python
from typing import TypedDict, List
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
import json

# ─── State Definition ─────────────────────────────────────────────────────────
class DefenseState(TypedDict):
    raw_logs: str
    parsed_events: List[dict]
    anomalies: List[dict]
    risk_level: str      # LOW | MEDIUM | HIGH | CRITICAL
    report: str

# ─── Tools (Python functions the LLM can call) ────────────────────────────────
@tool
def detect_patterns(logs: str) -> List[dict]:
    """Extract structured events from raw log text."""
    events = []
    for line in logs.split("\n"):
        if any(k in line for k in ["ERROR", "FAILED", "UNAUTHORIZED"]):
            events.append({"type": "security_event", "raw": line})
        elif "WARNING" in line:
            events.append({"type": "warning", "raw": line})
    return events

@tool
def detect_anomalies(events: List[dict]) -> List[dict]:
    """Detect statistical anomalies in event patterns."""
    anomalies = []
    error_count = sum(1 for e in events if e["type"] == "security_event")
    if error_count > 5:
        anomalies.append({"type": "high_error_rate", "count": error_count, "severity": "HIGH"})
    return anomalies

@tool
def lookup_threat(event_type: str) -> dict:
    """Look up known threat signatures."""
    db = {
        "UNAUTHORIZED": {"description": "Auth bypass attempt"},
        "SQL_INJECTION": {"cve": "CVE-2021-1234", "description": "SQLi pattern"}
    }
    return db.get(event_type, {"description": "Unknown threat"})

# ─── LLM Setup ────────────────────────────────────────────────────────────────
llm = ChatOpenAI(model="gpt-4o-mini")
llm_with_tools = llm.bind_tools([detect_patterns, detect_anomalies, lookup_threat])

# ─── Nodes (one function per agent role) ──────────────────────────────────────
def ingest_node(state: DefenseState) -> DefenseState:
    events = detect_patterns.invoke(state["raw_logs"])
    return {**state, "parsed_events": events}

def detect_node(state: DefenseState) -> DefenseState:
    anomalies = detect_anomalies.invoke(state["parsed_events"])
    return {**state, "anomalies": anomalies}

def classify_node(state: DefenseState) -> DefenseState:
    result = llm_with_tools.invoke([
        SystemMessage("Classify risk as LOW/MEDIUM/HIGH/CRITICAL."),
        HumanMessage(f"Anomalies: {json.dumps(state['anomalies'])}")
    ])
    risk = "HIGH" if state["anomalies"] else "LOW"
    return {**state, "risk_level": risk}

def report_node(state: DefenseState) -> DefenseState:
    result = llm_with_tools.invoke([
        SystemMessage("You are a Senior Security Analyst. Write a Markdown incident report."),
        HumanMessage(f"Risk: {state['risk_level']}\nAnomalies: {json.dumps(state['anomalies'])}")
    ])
    return {**state, "report": result.content}

# ─── Conditional Edge ─────────────────────────────────────────────────────────
def should_report(state: DefenseState) -> str:
    return "report" if state["anomalies"] else END

# ─── Graph Assembly ───────────────────────────────────────────────────────────
builder = StateGraph(DefenseState)
builder.add_node("ingest", ingest_node)
builder.add_node("detect", detect_node)
builder.add_node("classify", classify_node)
builder.add_node("report", report_node)

builder.set_entry_point("ingest")
builder.add_edge("ingest", "detect")
builder.add_edge("detect", "classify")
builder.add_conditional_edges("classify", should_report)
builder.add_edge("report", END)

# ─── Memory ───────────────────────────────────────────────────────────────────
checkpointer = MemorySaver()
app = builder.compile(checkpointer=checkpointer)

# ─── Entry Point ──────────────────────────────────────────────────────────────
def analyze_logs(logs: str) -> str:
    config = {"configurable": {"thread_id": "security-session-1"}}
    result = app.invoke(
        {"raw_logs": logs, "parsed_events": [], "anomalies": [], "risk_level": "", "report": ""},
        config
    )
    return result.get("report", "No threats detected.")
```

### Версія на Claude Code (~60 рядків YAML/markdown)

Чотири файли агентів, один файл skill. Жодного складання графа, жодного TypedDict, жодного шаблонного коду.

```
examples/agents/cyber-defense/
├── log-ingestor.md       (~40 lines)
├── anomaly-detector.md   (~50 lines)
├── risk-classifier.md    (~55 lines)
└── threat-reporter.md    (~45 lines)

examples/skills/cyber-defense-team/
└── SKILL.md              (~70 lines)
```

Кожен файл агента складається з YAML-frontmatter (name, model, tools) і системного промпту звичайною англійською, що описує роль, вхідні дані, результати й обмеження. Файл skill задає послідовність агентів через виклики `Agent tool`.

---

## Порівняння пліч-о-пліч

| Вимір | LangGraph | Claude Code Agent Teams |
|-----------|-----------|------------------------|
| **Загальний обсяг коду** | ~150 рядків Python | ~60 рядків YAML/Markdown |
| **Керування станом** | Явне визначення `TypedDict` | Неявне: JSON-файли між агентами |
| **Пам'ять** | Ручне налаштування `MemorySaver` | Нативна (файли зберігаються за замовчуванням) |
| **Визначення інструментів** | Python-функції з декоратором `@tool` | MCP-сервери або вбудовані інструменти |
| **Умовна логіка** | `add_conditional_edges()` | Природна мова в skill ("if no anomalies, skip to Step 5") |
| **Вибір моделі** | Одна модель для всіх вузлів | Для кожного агента окремо (haiku для парсингу, sonnet для міркувань) |
| **Налагодження** | `print()` + LangSmith (платний) | Нативний UI Claude Code |
| **Нова роль агента** | Нова функція + `add_node()` + `add_edge()` | Новий файл `.md` |
| **Онбординг** | Вивчити API LangGraph | Прочитати Markdown-файл |
| **Розгортання** | FastAPI або Gradio (~50 рядків додатково) | CLI `claude`, і все |
| **Залежності** | `langgraph`, `langchain`, `langchain-openai` | Жодних (вбудовано в Claude Code) |

---

## Коли що використовувати

**Використовуй Claude Code Agent Teams, коли:**
- Хочеш рухатися швидко: від прототипу до робочої системи за 30 хвилин
- У команді є не-розробники, які можуть читати чи редагувати промпти агентів
- Конвеєр є внутрішнім інструментом (а не публічним API-ендпоінтом)
- Потрібно часто ітерувати поведінку агентів (відредагував файл `.md`, і готово)

**Використовуй LangGraph, коли:**
- Потрібно вбудувати систему в більший Python-застосунок
- Хочеш відкрити конвеєр як REST API для зовнішніх споживачів
- Потрібні детерміновані переходи станів, які мають покриватися модульними тестами
- Команда вже працює на Python і має досвід із LangGraph

**Чесний компроміс**: LangGraph дає більше програмного контролю й доступ до екосистеми Python. Claude Code Agent Teams дають менше шаблонного коду, швидші ітерації й жодної інфраструктури для підтримки. Для внутрішніх інструментів і конвеєрів роботи зі знаннями підхід Claude Code зазвичай виграє за сукупною вартістю володіння.

---

## Файли в цьому прикладі

| Файл | Роль агента | Модель | Обов'язок |
|------|-----------|-------|----------------|
| `log-ingestor.md` | Етап 1 | haiku | Розбір сирих логів → `cyber-defense-events.json` |
| `anomaly-detector.md` | Етап 2 | sonnet | Виявлення патернів → `cyber-defense-anomalies.json` |
| `risk-classifier.md` | Етап 3 | sonnet | Оцінка ризику → `cyber-defense-risk.json` |
| `threat-reporter.md` | Етап 4 | sonnet | Генерація → `cyber-defense-report.md` |
| `../skills/cyber-defense-team/SKILL.md` | Оркестратор | — | Послідовність агентів, обробка помилок, підсумок |

---

**Натхнення**: фреймворк SMART COMPASS Мар'ям Міраді — та сама система, інший стек.
