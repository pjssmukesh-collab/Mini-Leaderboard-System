# app/core/config.py
# ──────────────────────────────────────────────
# Centralized application configuration.
#
# WHY THIS FILE EXISTS:
# Instead of scattering settings (database URL, secret keys, app name)
# throughout your code, we put them ALL in one place. This makes it
# easy to change settings without hunting through dozens of files.
#
# We use Pydantic's BaseSettings, which can automatically read values
# from a .env file — so you never hard-code passwords in your code.
# ──────────────────────────────────────────────

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Application settings.

    These values can be overridden by environment variables or a .env file.
    For example, if you set APP_NAME=MyApp in your .env file,
    it will override the default "Mini Leaderboard System" below.
    """

    # ── General ──
    APP_NAME: str = "Mini Leaderboard System"
    APP_VERSION: str = "1.0.0"
    APP_DESCRIPTION: str = "A generic, configurable event-scoring platform"
    DEBUG: bool = True

    # ── Database (placeholder — will be configured later) ──
    DATABASE_URL: str = "sqlite:///./mini_leaderboard.db"

    # ── Security & Authentication ──
    SECRET_KEY: str = "mini-leaderboard-jwt-secret-key-change-in-production-super-secure"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 24 hours


    # ── CORS (Cross-Origin Resource Sharing) ──
    # This allows your React frontend (running on a different port)
    # to talk to this backend API.
    CORS_ORIGINS: list[str] = ["http://localhost:3000", "http://localhost:5173", "http://localhost:5174", "http://127.0.0.1:5174"]

    class Config:
        # Tell Pydantic to look for a .env file in the backend/ folder
        env_file = ".env"
        env_file_encoding = "utf-8"


# ──────────────────────────────────────────────
# Create a single settings instance.
# Import this anywhere: from app.core.config import settings
# ──────────────────────────────────────────────
settings = Settings()
