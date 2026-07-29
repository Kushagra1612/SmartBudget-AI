"""
Smart Budget AI - Agentic Personal Finance Assistant
FastAPI application entry point.

This module wires together the FastAPI app instance, middleware, and (from
Phase 3 onward) the API routers. Keeping the assembly in one file makes it
easy to see the whole backend surface at a glance as phases are added.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings

from app.routers import  auth_router,upload_router
from app.routers import transactions

app = FastAPI(
    title="Smart Budget AI",
    description="Agentic Personal Finance Assistant API",
    version="0.1.0",
)

# Allow the React frontend (Vite dev server by default) to call this API.
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", tags=["Health"])
def root():
    """Basic liveness check."""
    return {
        "message": "Smart Budget AI API is running",
        "version": "0.1.0",
        "environment": settings.ENVIRONMENT,
    }


@app.get("/health", tags=["Health"])
def health_check():
    """Used by the frontend / uptime checks to confirm the API is reachable."""
    return {"status": "ok"}


# ---------------------------------------------------------------------------
# Routers are registered here as each phase adds them. Paths match the spec
# exactly (no /api prefix) -- left commented as a map of what's coming.
# ---------------------------------------------------------------------------
# from app.routers import auth            # Phase 3  -> POST /register, POST /login
# from app.routers import upload          # Phase 4  -> POST /upload-pdf
# from app.routers import transactions    # Phase 5  -> GET /transactions
# from app.routers import dashboard       # Phase 6  -> GET /dashboard
# from app.routers import budget          # Phase 8/9 -> GET /budget
# from app.routers import anomalies       # Phase 7/8 -> GET /anomalies
# from app.routers import chat            # Phase 9  -> POST /chat
#
app.include_router(auth_router)
app.include_router(upload_router)
app.include_router(transactions.router)
# app.include_router(transactions.router, tags=["Transactions"])
# app.include_router(dashboard.router, tags=["Dashboard"])
# app.include_router(budget.router, tags=["Budget"])
# app.include_router(anomalies.router, tags=["Anomalies"])
# app.include_router(chat.router, tags=["AI Assistant"])
