# app/core/security.py
# ──────────────────────────────────────────────
# Security Utilities: Password Hashing, JWT Tokens & Role Definitions
# ──────────────────────────────────────────────

from datetime import datetime, timedelta, timezone
from enum import Enum
from typing import Any, Optional, Union
import bcrypt
import jwt
from fastapi import HTTPException, status

from app.core.config import settings


# ──────────────────────────────────────────────
# 1. Role Definitions
# ──────────────────────────────────────────────
class UserRole(str, Enum):
    CREATOR = "creator"  # Tournament Creator: creates events & scoring rules
    ADMIN = "admin"      # Organizer / Admin: full platform management
    PLAYER = "player"    # Player / Participant: joins events, views leaderboards


# ──────────────────────────────────────────────
# 2. Password Hashing (bcrypt)
# ──────────────────────────────────────────────
def hash_password(password: str) -> str:
    """
    Hashes a plain-text password using bcrypt with automatic salt generation.
    """
    pwd_bytes = password.encode("utf-8")
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(pwd_bytes, salt).decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifies a plain-text password against a bcrypt hashed password.
    """
    try:
        return bcrypt.checkpw(
            plain_password.encode("utf-8"),
            hashed_password.encode("utf-8"),
        )
    except Exception:
        return False


# ──────────────────────────────────────────────
# 3. JWT Token Generation & Verification
# ──────────────────────────────────────────────
def create_access_token(
    subject: Union[str, int],
    role: str,
    extra_claims: Optional[dict[str, Any]] = None,
    expires_delta: Optional[timedelta] = None,
) -> str:
    """
    Generates a signed JWT access token containing subject (user_id/email) and role.
    """
    now = datetime.now(timezone.utc)
    if expires_delta:
        expire = now + expires_delta
    else:
        expire = now + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    payload: dict[str, Any] = {
        "sub": str(subject),
        "role": role,
        "iat": int(now.timestamp()),
        "exp": int(expire.timestamp()),
    }
    if extra_claims:
        payload.update(extra_claims)

    encoded_jwt = jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def decode_access_token(token: str) -> dict[str, Any]:
    """
    Decodes and validates a JWT token signature and expiration.
    Raises HTTPException(401) if invalid or expired.
    """
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
        )
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
