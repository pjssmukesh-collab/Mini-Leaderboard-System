# app/models/result_upload.py
# ──────────────────────────────────────────────
# ResultUpload Model
#
# Tracks result batch files uploaded to an event (CSV, JSON, OCR images, etc.).
# Provides an audit trail of who uploaded what and the overall processing state.
# ──────────────────────────────────────────────

from datetime import datetime, timezone

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Index
from sqlalchemy.orm import relationship

from app.database.database import Base


class ResultUpload(Base):
    __tablename__ = "result_uploads"

    # ── Primary Key ──
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    # ── Foreign Keys ──
    event_id = Column(
        Integer,
        ForeignKey("events.id", ondelete="CASCADE"),
        nullable=False,
    )
    uploaded_by = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )

    # ── Fields ──
    filename = Column(String(255), nullable=False)
    file_type = Column(
        String(50),
        nullable=False,
        # Examples: "csv", "json", "ocr_image", "api", "manual"
    )
    status = Column(
        String(20),
        nullable=False,
        default="pending",
        # Lifecycle: pending → processing → completed → failed
    )
    uploaded_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    # ── Relationships ──
    event = relationship("Event", back_populates="result_uploads")
    uploader = relationship("User", back_populates="uploads")
    raw_results = relationship("RawResult", back_populates="upload", cascade="all, delete-orphan")
    logs = relationship("UploadLog", back_populates="upload", cascade="all, delete-orphan")

    # ── Indexes ──
    __table_args__ = (
        Index("ix_result_uploads_event_id", "event_id"),
        Index("ix_result_uploads_uploaded_by", "uploaded_by"),
        Index("ix_result_uploads_status", "status"),
    )

    def __repr__(self):
        return (
            f"<ResultUpload(id={self.id}, event_id={self.event_id}, "
            f"filename='{self.filename}', status='{self.status}')>"
        )
