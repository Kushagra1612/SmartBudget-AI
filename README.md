# Smart Budget AI — Agentic Personal Finance Assistant

Upload a bank statement PDF and get transactions auto-extracted and categorized,
a personalized monthly budget, alerts on unusual spending, and a Gemini-powered
chat assistant that answers things like "where am I overspending?" — all
coordinated by a LangGraph multi-agent pipeline.

B.Tech AIML mini project.

## Tech stack

- **Frontend:** React, Tailwind CSS, React Router, Recharts, Axios
- **Backend:** FastAPI
- **Database:** PostgreSQL
- **AI orchestration:** LangGraph — 4 agents + a coordinator
- **ML:** scikit-learn Isolation Forest for anomaly detection
- **LLM:** Google Gemini API
- **PDF parsing:** pdfplumber (+ Camelot for complex tables)
- **Auth:** JWT

## Build status

Built phase by phase; each phase is fully working before the next one starts.

- [x] **Phase 1 — Backend setup**
- [ ] Phase 2 — Database
- [ ] Phase 3 — Authentication
- [ ] Phase 4 — PDF upload
- [ ] Phase 5 — Transaction extraction
- [ ] Phase 6 — Dashboard
- [ ] Phase 7 — ML model (Isolation Forest)
- [ ] Phase 8 — LangGraph agents
- [ ] Phase 9 — Gemini integration
- [ ] Phase 10 — Testing

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
│   │   ├── agents/        # LangGraph agents + coordinator         (Phase 8)
│   │   ├── ml/            # Isolation Forest model                 (Phase 7)
│   │   ├── prompts/       # Gemini prompt templates                (Phase 9)
│   │   └── utils/         # shared helpers
│   ├── requirements.txt
│   └── .env.example
└── frontend/               # not started yet
```

## Running Phase 1

```bash
cd backend
python3 -m venv venv && source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env        # defaults are fine for Phase 1
uvicorn app.main:app --reload --port 8000
```

Then check:
- `http://localhost:8000/health` → `{"status": "ok"}`
- `http://localhost:8000/docs` → interactive Swagger UI

## A note on this sandbox

This was written and smoke-tested (clean install, server boots, both endpoints
return the expected JSON) in a sandboxed container. From Phase 2 you'll need a
real PostgreSQL database, and from Phase 9 a real Gemini API key — both are
supplied by you via `.env` when you run this on your own machine, since I can't
provision either from inside the sandbox.
