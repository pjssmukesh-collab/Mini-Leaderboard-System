# app/models/raw_result.py
# ──────────────────────────────────────────────
# RawResult Model
#
# Stores unparsed/raw match or contest data ingested from an upload.
# Uses JSON to flexibly preserve original payloads regardless of format.
# ──────────────────────────────────────────────

from datetime import datetime, timezone

from sqlalchemy import Column, Integer, DateTime, ForeignKey, Index, JSON
from sqlalchemy.orm import relationship

from app.database.database import Base


class RawResult(Base):
    __tablename__ = "raw_results"

    # ── Primary Key ──
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    # ── Foreign Keys ──
    upload_id = Column(
        Integer,
        ForeignKey("result_uploads.id", ondelete="CASCADE"),
        nullable=False,
    )
    event_id = Column(
        Integer,
        ForeignKey("events.id", ondelete="CASCADE"),
        nullable=False,
    )

    # ── Fields ──
    raw_data = Column(
        JSON,
        nullable=False,
        # Stores the original parsed JSON/dict payload or row content
    )
    created_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    # ── Relationships ──
    upload = relationship("ResultUpload", back_populates="raw_results")
    event = relationship("Event", back_populates="raw_results")

    # ── Indexes ──
    __table_args__ = (
        Index("ix_raw_results_upload_id", "upload_id"),
        Index("ix_raw_results_event_id", "event_id"),
    )

    def __repr__(self):
        return f"<RawResult(id={self.id}, upload_id={self.upload_id}, event_id={self.event_id})>"
