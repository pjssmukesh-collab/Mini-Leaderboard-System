# app/models/player_result.py
# ──────────────────────────────────────────────
# PlayerResult Model
#
# Holds normalized performance metrics for a participant in a specific match/round.
# Uses JSON for flexible event metrics (e.g. kills, placement, score, coding time).
# ──────────────────────────────────────────────

from datetime import datetime, timezone

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Index, JSON
from sqlalchemy.orm import relationship

from app.database.database import Base


class PlayerResult(Base):
    __tablename__ = "player_results"

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
    match_id = Column(
        String(100),
        nullable=True,
        # e.g., "match_01", "round_3", "game_uuid"
    )
    metrics = Column(
        JSON,
        nullable=False,
        default=dict,
        # Flexible event metrics, e.g.:
        # {"kills": 12, "placement": 1, "damage": 2450} or {"solved": 4, "time": 120}
    )
    validation_status = Column(
        String(20),
        nullable=False,
        default="valid",
        # Lifecycle: "valid", "flagged", "rejected", "duplicate"
    )
    created_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    # ── Relationships ──
    event = relationship("Event", back_populates="player_results")
    participant = relationship("Participant", back_populates="player_results")

    # ── Indexes ──
    __table_args__ = (
        Index("ix_player_results_event_id", "event_id"),
        Index("ix_player_results_participant_id", "participant_id"),
        Index("ix_player_results_match_id", "match_id"),
        Index("ix_player_results_validation_status", "validation_status"),
        Index("ix_player_results_event_participant", "event_id", "participant_id"),
    )

    def __repr__(self):
        return (
            f"<PlayerResult(id={self.id}, event_id={self.event_id}, "
            f"participant_id={self.participant_id}, match_id='{self.match_id}', "
            f"status='{self.validation_status}')>"
        )
