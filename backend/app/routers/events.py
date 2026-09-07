# app/routers/events.py
# ──────────────────────────────────────────────
# Event Management API Endpoints
# ──────────────────────────────────────────────

from typing import List, Optional
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.core.deps import get_current_user, require_creator
from app.database.database import get_db
from app.models.user import User
from app.schemas.event import EventCreate, EventUpdate, EventResponse
from app.services.event_service import event_service

router = APIRouter(prefix="/events", tags=["Events"])


@router.post(
    "",
    response_model=EventResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new event",
    description="Creates a new tournament or contest. Allowed for Tournament Creators and Admins.",
)
def create_event(
    event_in: EventCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_creator),
):
    """Create a new event."""
    return event_service.create_event(db, event_in, current_user)


@router.get(
    "",
    response_model=List[EventResponse],
    summary="List all events",
    description="Returns a paginated list of events with optional filters (type, status, creator, search).",
)
def list_events(
    event_type: Optional[str] = Query(None, description="Filter by event type (e.g. gaming, chess, coding, quiz, sports, other)"),
    status_filter: Optional[str] = Query(None, alias="status", description="Filter by status (draft, active, completed, archived)"),
    creator_id: Optional[int] = Query(None, description="Filter by tournament creator ID"),
    search: Optional[str] = Query(None, description="Search event name by keyword"),
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(50, ge=1, le=100, description="Max records to return"),
    db: Session = Depends(get_db),
):
    """List events with filtering and pagination."""
    return event_service.list_events(
        db,
        event_type=event_type,
        status_filter=status_filter,
        creator_id=creator_id,
        search=search,
        skip=skip,
        limit=limit,
    )


@router.get(
    "/{id}",
    response_model=EventResponse,
    summary="Get event by ID",
    description="Returns the complete details of a specific event.",
)
def get_event(
    id: int,
    db: Session = Depends(get_db),
):
    """Fetch event details by ID."""
    return event_service.get_event(db, id)


@router.put(
    "/{id}",
    response_model=EventResponse,
    summary="Update an event",
    description="Updates event fields. Only the event creator who owns it or an Admin can perform updates.",
)
def update_event(
    id: int,
    event_in: EventUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Update event details."""
    return event_service.update_event(db, id, event_in, current_user)


@router.delete(
    "/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete an event",
    description="Deletes an event and cascades to associated data. Only the event creator who owns it or an Admin can delete it.",
)
def delete_event(
    id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Delete an event by ID."""
    event_service.delete_event(db, id, current_user)
    return None
