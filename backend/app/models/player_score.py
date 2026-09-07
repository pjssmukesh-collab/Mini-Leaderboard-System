# app/models/player_score.py
# ──────────────────────────────────────────────
# PlayerScore Model
#
# Stores the aggregate calculated score of a participant for an event.
# Evaluated and updated by the Rule Engine.
# ──────────────────────────────────────────────

from datetime import datetime, timezone

from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey, Index, UniqueConstraint
from sqlalchemy.orm import relationship

from app.database.database import Base


class PlayerScore(Base):
    __tablename__ = "player_scores"

    # ── Primary Key ──
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    # ── Foreign Keys ──
    event_id = Column(
        Integer,
        ForeignKey("events.id", ondelete="CASCADE"),
        nullable=False,
    )
    participant_id = Column(
        Integer,
        ForeignKey("participants.id", ondelete="CASCADE"),
        nullable=False,
    )

    # ── Fields ──
    score = Column(
        Float,
        nullable=False,
        default=0.0,
    )
    updated_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    # ── Relationships ──
    event = relationship("Event", back_populates="player_scores")
    participant = relationship("Participant", back_populates="player_score")

    # ── Indexes & Constraints ──
    __table_args__ = (
        Index("ix_player_scores_event_id", "event_id"),
        Index("ix_player_scores_participant_id", "participant_id"),
        Index("ix_player_scores_event_score", "event_id", "score"),
        UniqueConstraint("event_id", "participant_id", name="uq_player_score_event_participant"),
    )

    def __repr__(self):
        return (
            f"<PlayerScore(id={self.id}, event_id={self.event_id}, "
            f"participant_id={self.participant_id}, score={self.score})>"
        )
