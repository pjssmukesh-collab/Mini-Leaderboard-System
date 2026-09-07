# app/schemas/auth.py
# ──────────────────────────────────────────────
# Pydantic Schemas for Authentication & User Data
# ──────────────────────────────────────────────

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field, ConfigDict

from app.core.security import UserRole


class UserRegister(BaseModel):
    """Payload for user registration."""
    name: str = Field(..., min_length=2, max_length=100, examples=["Alice Smith"])
    email: EmailStr = Field(..., examples=["alice@example.com"])
    password: str = Field(..., min_length=6, max_length=128, examples=["SecurePassword123!"])
    role: UserRole = Field(default=UserRole.PLAYER, examples=["player", "creator", "admin"])


class UserLogin(BaseModel):
    """Payload for user login."""
    email: EmailStr = Field(..., examples=["alice@example.com"])
    password: str = Field(..., min_length=1, examples=["SecurePassword123!"])


class UserResponse(BaseModel):
    """Public user response schema."""
    id: int
    name: str
    email: str
    role: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class TokenResponse(BaseModel):
    """JWT Token authentication response."""
    access_token: str
    token_type: str = "bearer"
    user: UserResponse
