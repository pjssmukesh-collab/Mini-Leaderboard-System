# app/schemas/event.py
# ──────────────────────────────────────────────
# Pydantic Schemas for Event Management
# ──────────────────────────────────────────────

from datetime import datetime
from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict, model_validator

from app.schemas.auth import UserResponse


class EventType(str, Enum):
    GAMING = "gaming"
    CHESS = "chess"
    CODING = "coding"
    QUIZ = "quiz"
    SPORTS = "sports"
    OTHER = "other"


class EventStatus(str, Enum):
    DRAFT = "draft"
    ACTIVE = "active"
    COMPLETED = "completed"
    ARCHIVED = "archived"


class EventBase(BaseModel):
    """Base shared attributes for events."""
    name: str = Field(..., min_length=2, max_length=200, examples=["Summer Battle Royale Invitational"])
    event_type: str = Field(..., min_length=2, max_length=50, examples=["gaming"])
    description: Optional[str] = Field(default=None, max_length=2000, examples=["Official weekend esports tournament."])
    start_date: Optional[datetime] = Field(default=None, examples=["2026-09-01T10:00:00Z"])
    end_date: Optional[datetime] = Field(default=None, examples=["2026-09-03T18:00:00Z"])
    participant_limit: Optional[int] = Field(default=None, ge=1, examples=[100])
    status: EventStatus = Field(default=EventStatus.DRAFT, examples=["draft"])

    @model_validator(mode="after")
    def validate_dates(self) -> "EventBase":
        """Ensure end_date is after start_date if both are specified."""
        if self.start_date and self.end_date and self.end_date < self.start_date:
            raise ValueError("end_date must be greater than or equal to start_date")
        return self


class EventCreate(EventBase):
    """Payload for creating a new event."""
    pass


class EventUpdate(BaseModel):
    """Payload for updating an existing event (partial updates allowed)."""
    name: Optional[str] = Field(default=None, min_length=2, max_length=200)
    event_type: Optional[str] = Field(default=None, min_length=2, max_length=50)
    description: Optional[str] = Field(default=None, max_length=2000)
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    participant_limit: Optional[int] = Field(default=None, ge=1)
    status: Optional[EventStatus] = None

    @model_validator(mode="after")
    def validate_dates(self) -> "EventUpdate":
        """Ensure end_date is after start_date if both are specified."""
        if self.start_date and self.end_date and self.end_date < self.start_date:
            raise ValueError("end_date must be greater than or equal to start_date")
        return self


class EventResponse(BaseModel):
    """Event response representation."""
    id: int
    creator_id: int
    name: str
    event_type: str
    description: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    participant_limit: Optional[int] = None
    status: str
    created_at: datetime
    creator: Optional[UserResponse] = None

    model_config = ConfigDict(from_attributes=True)
