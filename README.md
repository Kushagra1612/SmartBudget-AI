# Smart Budget AI — Agentic Personal Finance Assistant

Upload a bank statement PDF and get transactions auto-extracted and categorized,
a personalized monthly budget, alerts on unusual spending, and a Gemini-powered
chat assistant that answers things like "where am I overspending?" — all
coordinated by a LangGraph multi-agent pipeline: a coordinator that routes each
request to the relevant specialist agents (dashboard/budget/spending/goal),
which run in parallel and feed into a final response.

B.Tech AIML mini project.

## Tech stack

- **Frontend:** React, Tailwind CSS, React Router, Recharts, Axios
- **Backend:** FastAPI
- **Database:** PostgreSQL
- **AI orchestration:** LangGraph — a coordinator node routes each request to whichever of 4 specialist agent nodes (dashboard/budget/spending/goal) are relevant; they run in parallel and feed into a responder node that generates the final answer
- **ML:** scikit-learn Isolation Forest for anomaly detection
- **LLM:** Google Gemini API
- **PDF parsing:** pdfplumber (+ Camelot for complex tables)
- **Auth:** JWT

## Build status

Built phase by phase.

- [x] Phase 1 — Backend setup
- [x] Phase 2 — Database
- [x] Phase 3 — Authentication
- [x] Phase 4 — PDF upload
- [x] Phase 5 — Transaction extraction
- [x] Phase 6 — Dashboard
- [x] Phase 7 — ML model (Isolation Forest)
- [x] Phase 8 — LangGraph agents
- [x] Phase 9 — Gemini integration
- [x] Phase 10 — Testing

**Honest scope notes — "done" above means built and verified working, not**
**that there's nothing left to extend:**
- **Phase 7** has real coverage in its own unit tests (outliers, income
  exclusion, score bounds, a sparse-category edge case), but hasn't yet flagged
  a real anomaly of your own — needs 15+ of your own expense transactions
  before it runs on real data instead of seeded test data.
- **Phase 8** is a real `StateGraph`: `coordinator` → up to 4 parallel agent
  nodes (`dashboard_agent`/`budget_agent`/`spending_agent`/`goal_agent`) →
  `responder`. Chat gets dynamic routing (Gemini decides which agents a
  question needs); pulse/advice always route to all of dashboard+budget+
  spending, since "give me advice" doesn't need a routing decision. Structure
  is checked directly in `tests/test_ai_graph.py`, not just exercised
  indirectly through the endpoints.
- **Phase 10** covers auth, anomalies, goals, budgets, transactions, dashboard,
  AI (Gemini mocked), and upload (parser mocked) — 76 tests. Not covered:
  frontend tests (would need separate tooling — Vitest/RTL aren't part of the
  stack yet) and real, un-mocked PDF parsing against an actual bank statement
  layout.
- Along the way: fixed a `bcrypt`/`passlib` version conflict that broke
  password hashing on a clean install, and fixed AI chat memory being shared
  across every user instead of scoped per-user.

Also built, ahead of the original phase plan: a full **Goals** feature (model,
migration, API, AI tool, frontend pages).

Frontend pages land alongside the backend phase that powers them (Login/Register
with Phase 3, dashboard charts with Phase 6, and so on) rather than all at once
at the end.

## Project structure

```
smart-budget-ai/
├── backend/
│   ├── app/
│   │   ├── main.py        # FastAPI app, middleware, router registration
│   │   ├── config.py      # settings, loaded from .env
│   │   ├── database/      # engine, session, declarative base      (Phase 2)
│   │   ├── models/        # SQLAlchemy ORM models                  (Phase 2)
│   │   ├── schemas/       # Pydantic request/response schemas
│   │   ├── routers/       # API route handlers                    (Phase 3+)
│   │   ├── services/      # business logic                        (Phase 3+)
│   │   ├── ai/            # LangGraph coordinator + 4 agent nodes  (Phase 8)
│   │   ├── ml/            # Isolation Forest model                 (Phase 7)
│   │   ├── prompts/       # Gemini prompt templates                (Phase 9)
│   │   └── utils/         # shared helpers
│   ├── tests/     # 76 tests, real Postgres + mocked Gemini (Phase 10)
│   ├── requirements.txt
│   └── .env.example
└── frontend/               # fully built — see frontend/src/pages
```

(Simplified — `app/` has grown a few more folders since Phase 1: `alembic/`,
`analytics/`, `categorizer/`, `parsers/`, `repositories/`, `dependencies/`,
`exceptions/`.)

## Running the backend

```bash
cd backend
python3 -m venv venv && source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env        # fill in DATABASE_URL and GEMINI_API_KEY
alembic upgrade head        # creates the tables (needed from Phase 2 on)
uvicorn app.main:app --reload --port 8000
```

Then check:
- `http://localhost:8000/health` → `{"status": "ok"}`
- `http://localhost:8000/docs` → interactive Swagger UI

## Running the frontend

```bash
cd frontend
npm install
npm run dev
```

Needs the backend running on port 8000 — see `frontend/src/api/axios.js` for
the base URL it expects.

## Running the tests

```bash
cd backend
createdb smart_budget_ai_test    # once, on the same Postgres instance
pytest -v
```

76 tests, all real — no `unittest.mock`-only fakes standing in for the whole
app. Gemini calls are mocked (no API quota used, no key needed), everything
else runs against an actual Postgres test database, never your dev one.

## A note on this sandbox

This was written and smoke-tested (clean install, server boots, both endpoints
return the expected JSON) in a sandboxed container. From Phase 2 you'll need a
real PostgreSQL database, and from Phase 9 a real Gemini API key — both are
supplied by you via `.env` when you run this on your own machine, since I can't
provision either from inside the sandbox.
