# app/models/participant.py
# ──────────────────────────────────────────────
# Participant Model
#
# Represents a player participating in an event.
# A participant can be linked to a registered User account
# or identified via an external_player_id (e.g., in-game handle/tag).
# ──────────────────────────────────────────────

from datetime import datetime, timezone

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Index, UniqueConstraint
from sqlalchemy.orm import relationship

from app.database.database import Base


class Participant(Base):
    __tablename__ = "participants"

    # ── Primary Key ──
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    # ── Foreign Keys ──
    event_id = Column(
        Integer,
        ForeignKey("events.id", ondelete="CASCADE"),
        nullable=False,
    )
    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
    )

    # ── Fields ──
    external_player_id = Column(
        String(100),
        nullable=True,
        # e.g., gamer tag, chess username, student ID
    )
    joined_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
    status = Column(
        String(20),
        nullable=False,
        default="registered",
        # Lifecycle: registered → confirmed → active → disqualified → withdrawn
    )

    # ── Relationships ──
    event = relationship("Event", back_populates="participants")
    user = relationship("User", back_populates="participations")
    player_results = relationship("PlayerResult", back_populates="participant", cascade="all, delete-orphan")
    player_score = relationship("PlayerScore", back_populates="participant", uselist=False, cascade="all, delete-orphan")
    ranking = relationship("Ranking", back_populates="participant", uselist=False, cascade="all, delete-orphan")

    # ── Indexes & Constraints ──
    __table_args__ = (
        Index("ix_participants_event_id", "event_id"),
        Index("ix_participants_user_id", "user_id"),
        Index("ix_participants_external_player_id", "external_player_id"),
        Index("ix_participants_event_status", "event_id", "status"),
        UniqueConstraint("event_id", "user_id", name="uq_participant_event_user"),
    )

    def __repr__(self):
        return (
            f"<Participant(id={self.id}, event_id={self.event_id}, "
            f"user_id={self.user_id}, external_player_id='{self.external_player_id}', "
            f"status='{self.status}')>"
        )
