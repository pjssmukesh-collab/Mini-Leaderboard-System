# app/models/upload_log.py
# ──────────────────────────────────────────────
# UploadLog Model
#
# Detailed log entries for a result upload processing pipeline.
# Records step actions, warnings, errors, and validation milestones.
# ──────────────────────────────────────────────

from datetime import datetime, timezone

from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Index
from sqlalchemy.orm import relationship

from app.database.database import Base


class UploadLog(Base):
    __tablename__ = "upload_logs"

    # ── Primary Key ──
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    # ── Foreign Key ──
    upload_id = Column(
        Integer,
        ForeignKey("result_uploads.id", ondelete="CASCADE"),
        nullable=False,
    )

    # ── Fields ──
    action = Column(
        String(50),
        nullable=False,
        # Examples: "FILE_UPLOADED", "PARSE_START", "ROW_VALIDATED", "PARSE_ERROR"
    )
    message = Column(Text, nullable=False)
    created_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    # ── Relationships ──
    upload = relationship("ResultUpload", back_populates="logs")

    # ── Indexes ──
    __table_args__ = (
        Index("ix_upload_logs_upload_id", "upload_id"),
        Index("ix_upload_logs_action", "action"),
    )

    def __repr__(self):
        return f"<UploadLog(id={self.id}, upload_id={self.upload_id}, action='{self.action}')>"
