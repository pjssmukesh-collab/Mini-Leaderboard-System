# app/models/event_rule.py
# ──────────────────────────────────────────────
# EventRule Model
#
# Scoring rules that the event creator defines.
# These are NOT hard-coded — the creator chooses what metrics
# matter and how many points each is worth.
#
# EXAMPLES:
#   Free Fire: kills / each / +2 pts | placement / equals / 1 / +10 pts
#   Chess:     result / equals / "WIN" / +3 pts | result / equals / "DRAW" / +1 pt
#   Coding:    problems_solved / each / +10 pts | wrong_submissions / each / -2 pts
# ──────────────────────────────────────────────

from sqlalchemy import (
    Column, Integer, String, Float, ForeignKey, Index,
)
from sqlalchemy.orm import relationship

from app.database.database import Base


class EventRule(Base):
    __tablename__ = "event_rules"

    # ── Primary Key ──
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    # ── Foreign Key ──
    event_id = Column(
        Integer,
        ForeignKey("events.id", ondelete="CASCADE"),
        nullable=False,
    )

    # ── Fields ──
    metric = Column(
        String(100),
        nullable=False,
        # The data field to evaluate (e.g. "kills", "placement", "result", "problems_solved")
    )
    condition = Column(
        String(255),
        nullable=True,
        # Human-readable description (e.g. "Each kill awards +2 points")
    )
    operator = Column(
        String(50),
        nullable=False,
        # Operators: "equals", "==", ">=", "<=", ">", "<", "!=", "each", "multiplier"
    )
    value = Column(
        String(100),
        nullable=True,
        # The threshold or target value to compare against (e.g. "1", "WIN", "10", or null for "each")
    )
    points = Column(
        Float,
        nullable=False,
        # Points to award/deduct (can be positive +10 or negative penalty -2)
    )
    priority = Column(
        Integer,
        nullable=False,
        default=0,
        # Evaluation precedence order (higher priority evaluated first)
    )

    # ── Relationships ──
    event = relationship("Event", back_populates="rules")

    # ── Indexes ──
    __table_args__ = (
        Index("ix_event_rules_event_id", "event_id"),
        Index("ix_event_rules_metric", "metric"),
        Index("ix_event_rules_priority", "priority"),
    )

    def __repr__(self):
        return (
            f"<EventRule(id={self.id}, event_id={self.event_id}, metric='{self.metric}', "
            f"operator='{self.operator}', value='{self.value}', points={self.points})>"
        )
