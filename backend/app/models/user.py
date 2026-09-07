# app/models/user.py
# ──────────────────────────────────────────────
# User Model
#
# Represents a person who uses the system.
# There are 3 roles:
#   - "creator"   → Creates tournaments/events, defines scoring rules
#   - "admin"     → Manages uploads, validates data, monitors leaderboards
#   - "player"    → Joins events, views leaderboard and stats
# ──────────────────────────────────────────────

from datetime import datetime, timezone

from sqlalchemy import Column, Integer, String, DateTime, Index
from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_property

from app.database.database import Base


class User(Base):
    __tablename__ = "users"

    # ── Primary Key ──
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    # ── Fields ──
    name = Column(String(100), nullable=False)

    @hybrid_property
    def username(self):
        return self.name

    @username.setter
    def username(self, value):
        self.name = value

    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    role = Column(
        String(20),
        nullable=False,
        default="player",  # Default role when someone registers
    )
    created_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    # ── Relationships ──
    # A user can CREATE many events (as a tournament creator)
    created_events = relationship("Event", back_populates="creator")

    # A user can JOIN many events (as a participant)
    participations = relationship("Participant", back_populates="user")

    # A user can UPLOAD many result files (as an admin/organizer)
    uploads = relationship("ResultUpload", back_populates="uploader")

    # ── Indexes ──
    __table_args__ = (
        Index("ix_users_role", "role"),  # Fast lookup by role
    )

    def __repr__(self):
        return f"<User(id={self.id}, name='{self.name}', role='{self.role}')>"
