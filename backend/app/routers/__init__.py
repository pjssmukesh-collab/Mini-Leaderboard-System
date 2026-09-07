# app/routers/__init__.py
# API route controllers package

from app.routers.auth import router as auth_router
from app.routers.events import router as events_router
from app.routers.rules import router as rules_router
from app.routers.participants import router as participants_router
from app.routers.uploads import router as uploads_router
from app.routers.validation import router as validation_router
from app.routers.leaderboard import router as leaderboard_router

__all__ = ["auth_router", "events_router", "rules_router", "participants_router", "uploads_router", "validation_router", "leaderboard_router"]
