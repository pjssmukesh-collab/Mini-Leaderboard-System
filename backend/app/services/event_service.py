# app/services/event_service.py
# ──────────────────────────────────────────────
# Event Management Service Business Logic
# ──────────────────────────────────────────────

from typing import List, Optional
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.event import Event
from app.models.user import User
from app.schemas.event import EventCreate, EventUpdate


class EventService:
    """Business logic for creating, querying, updating, and deleting events."""

    @staticmethod
    def create_event(db: Session, event_in: EventCreate, creator: User) -> Event:
        """
        Creates a new event associated with the authenticated tournament creator or admin.
        """
        event = Event(
            creator_id=creator.id,
            name=event_in.name.strip(),
            event_type=event_in.event_type.strip().lower(),
            description=event_in.description.strip() if event_in.description else None,
            start_date=event_in.start_date,
            end_date=event_in.end_date,
            participant_limit=event_in.participant_limit,
            status=event_in.status.value if hasattr(event_in.status, "value") else str(event_in.status),
        )
        db.add(event)
        db.commit()
        db.refresh(event)
        return event

    @staticmethod
    def get_event(db: Session, event_id: int) -> Event:
        """
        Retrieves a single event by ID or raises 404 Not Found.
        """
        event = db.query(Event).filter(Event.id == event_id).first()
        if not event:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Event with id {event_id} was not found",
            )
        return event

    @staticmethod
    def list_events(
        db: Session,
        event_type: Optional[str] = None,
        status_filter: Optional[str] = None,
        creator_id: Optional[int] = None,
        search: Optional[str] = None,
        skip: int = 0,
        limit: int = 50,
    ) -> List[Event]:
        """
        Retrieves a paginated list of events with optional filtering.
        """
        query = db.query(Event)

        if event_type:
            query = query.filter(Event.event_type == event_type.strip().lower())
        if status_filter:
            query = query.filter(Event.status == status_filter.strip().lower())
        if creator_id is not None:
            query = query.filter(Event.creator_id == creator_id)
        if search:
            query = query.filter(Event.name.ilike(f"%{search.strip()}%"))

        return query.order_by(Event.created_at.desc()).offset(skip).limit(limit).all()

    @staticmethod
    def update_event(
        db: Session,
        event_id: int,
        event_in: EventUpdate,
        current_user: User,
    ) -> Event:
        """
        Updates an event. Only the owner creator or an admin can update the event.
        """
        event = EventService.get_event(db, event_id)

        # Authorization check: only owner or admin
        if current_user.role != "admin" and event.creator_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to modify this event",
            )

        update_data = event_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            if field == "status" and hasattr(value, "value"):
                value = value.value
            elif field == "event_type" and isinstance(value, str):
                value = value.strip().lower()
            elif field == "name" and isinstance(value, str):
                value = value.strip()
            setattr(event, field, value)

        db.commit()
        db.refresh(event)
        return event

    @staticmethod
    def delete_event(db: Session, event_id: int, current_user: User) -> None:
        """
        Deletes an event. Only the owner creator or an admin can delete the event.
        """
        event = EventService.get_event(db, event_id)

        # Authorization check: only owner or admin
        if current_user.role != "admin" and event.creator_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to delete this event",
            )

        db.delete(event)
        db.commit()


event_service = EventService()
