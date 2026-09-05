"""
Smart Budget AI - Agentic Personal Finance Assistant
FastAPI application entry point.

This module wires together the FastAPI app instance, middleware, and (from
Phase 3 onward) the API routers. Keeping the assembly in one file makes it
easy to see the whole backend surface at a glance as phases are added.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

from app.config import settings
from app.routers import (
    ai_router,
    anomaly_router,
    auth_router,
    budget_router,
    dashboard_router,
    goal_router,
    transactions_router,
    upload_router,
)

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



app.include_router(auth_router)
app.include_router(upload_router)
app.include_router(transactions_router)
app.include_router(budget_router)
app.include_router(dashboard_router)
app.include_router(ai_router)
app.include_router(goal_router)
app.include_router(anomaly_router)
