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
from app.routers import budget 
from app.routers import  auth_router,upload_router
from app.routers import transactions
from app.routers.dashboard import router as dashboard_router
from app.routers.ai import router as ai_router
from app.routers.goal import router as goal_router

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
app.include_router(transactions.router)
app.include_router(budget.router)
app.include_router(dashboard_router)
app.include_router(ai_router)
app.include_router(goal_router)
