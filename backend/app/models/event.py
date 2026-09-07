# app/models/event.py
# ──────────────────────────────────────────────
# Event Model
#
# An "event" is a tournament, competition, or contest.
# Examples: a Free Fire tournament, a chess match, a coding contest.
#
# The creator defines:
#   - What type of event it is (free_fire, chess, coding, quiz, sports)
#   - How many participants can join
#   - The start/end dates
#   - The scoring rules (stored in EventRule)
# ──────────────────────────────────────────────

from datetime import datetime, timezone

from sqlalchemy import (
    Column, Integer, String, Text, DateTime, ForeignKey, Index,
)
from sqlalchemy.orm import relationship

from app.database.database import Base


class Event(Base):
    __tablename__ = "events"

    # ── Primary Key ──
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    # ── Foreign Key ──
    # Which user created this event
    creator_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )

    # ── Fields ──
    name = Column(String(200), nullable=False)
    event_type = Column(
        String(50),
        nullable=False,
        # Examples: "free_fire", "chess", "coding", "quiz", "sports"
    )
    description = Column(Text, nullable=True)
    start_date = Column(DateTime, nullable=True)
    end_date = Column(DateTime, nullable=True)
    participant_limit = Column(Integer, nullable=True)  # None = unlimited
    status = Column(
        String(20),
        nullable=False,
        default="draft",
        # Lifecycle: draft → active → completed → archived
    )
    created_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    # ── Relationships ──
    creator = relationship("User", back_populates="created_events")
    rules = relationship("EventRule", back_populates="event", cascade="all, delete-orphan")
    participants = relationship("Participant", back_populates="event", cascade="all, delete-orphan")
    result_uploads = relationship("ResultUpload", back_populates="event", cascade="all, delete-orphan")
    raw_results = relationship("RawResult", back_populates="event", cascade="all, delete-orphan")
    player_results = relationship("PlayerResult", back_populates="event", cascade="all, delete-orphan")
    player_scores = relationship("PlayerScore", back_populates="event", cascade="all, delete-orphan")
    rankings = relationship("Ranking", back_populates="event", cascade="all, delete-orphan")

    # ── Indexes ──
    __table_args__ = (
        Index("ix_events_event_type", "event_type"),
        Index("ix_events_status", "status"),
        Index("ix_events_creator_id", "creator_id"),
    )

    def __repr__(self):
        return f"<Event(id={self.id}, name='{self.name}', type='{self.event_type}')>"
