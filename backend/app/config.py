"""
Centralized application configuration.

All settings are read from environment variables (via backend/.env in
development, or real environment variables in production). Nothing
sensitive is hard-coded -- copy .env.example to .env and fill in real
values before running the app.
"""

from pathlib import Path
from typing import List

from pydantic_settings import BaseSettings, SettingsConfigDict

# backend/ -- two levels up from this file (backend/app/config.py)
BASE_DIR = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    # --- General -----------------------------------------------------------
    ENVIRONMENT: str = "development"

    # --- Database (Phase 2) -------------------------------------------------
    DATABASE_URL: str = "postgresql://postgres:postgres@localhost:5432/smart_budget_ai"

    # --- JWT auth (Phase 3) --------------------------------------------------
    SECRET_KEY: str = "change-this-secret-key"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 43200

    # --- Gemini LLM (Phase 7) -------------------------------------------------
    GEMINI_API_KEY: str = ""
    GEMINI_MODEL: str = "gemini-3.6-flash"

    # --- CORS ------------------------------------------------------------------
    # Comma-separated list of origins allowed to call the API.
    CORS_ORIGINS: str = "http://localhost:5173,http://localhost:3000"

    model_config = SettingsConfigDict(
        env_file=str(BASE_DIR / ".env"),
        env_file_encoding="utf-8",
        extra="ignore",
    )

    @property
    def cors_origins_list(self) -> List[str]:
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",") if origin.strip()]


settings = Settings()
