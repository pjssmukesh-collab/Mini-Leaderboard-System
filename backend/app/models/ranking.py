# app/models/ranking.py
# ──────────────────────────────────────────────
# Ranking Model
#
# Represents the assigned leaderboard rank and score of a participant for an event.
# Optimized for fast leaderboard queries and sort orders.
# ──────────────────────────────────────────────

from datetime import datetime, timezone

from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey, Index, UniqueConstraint
from sqlalchemy.orm import relationship

from app.database.database import Base


class Ranking(Base):
    __tablename__ = "rankings"

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
    rank = Column(Integer, nullable=False)
    score = Column(Float, nullable=False)
    updated_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    # ── Relationships ──
    event = relationship("Event", back_populates="rankings")
    participant = relationship("Participant", back_populates="ranking")

    # ── Indexes & Constraints ──
    __table_args__ = (
        Index("ix_rankings_event_id", "event_id"),
        Index("ix_rankings_participant_id", "participant_id"),
        Index("ix_rankings_event_rank", "event_id", "rank"),
        Index("ix_rankings_event_score", "event_id", "score"),
        UniqueConstraint("event_id", "participant_id", name="uq_ranking_event_participant"),
    )

    def __repr__(self):
        return (
            f"<Ranking(id={self.id}, event_id={self.event_id}, "
            f"participant_id={self.participant_id}, rank={self.rank}, score={self.score})>"
        )
