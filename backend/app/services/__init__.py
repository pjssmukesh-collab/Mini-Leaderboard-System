# app/services/__init__.py
# Business logic services package

from app.services.auth_service import AuthService, auth_service
from app.services.event_service import EventService, event_service

__all__ = ["AuthService", "auth_service", "EventService", "event_service"]
