# app/core/deps.py
# ──────────────────────────────────────────────
# FastAPI Dependencies for Authentication & Role-Based Access Control (RBAC)
# ──────────────────────────────────────────────

from typing import Callable, List, Union
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.core.security import decode_access_token, UserRole
from app.database.database import get_db
from app.models.user import User

# HTTP Bearer scheme (handles "Authorization: Bearer <token>")
security_bearer = HTTPBearer(auto_error=False)


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security_bearer),
    db: Session = Depends(get_db),
) -> User:
    """
    Dependency to authenticate and retrieve the current user from the JWT token.
    Raises HTTP 401 Unauthorized if token is missing, invalid, expired, or user not found.
    """
    if credentials is None or not credentials.credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication token is required",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = credentials.credentials
    payload = decode_access_token(token)
    user_id_str = payload.get("sub")
    if not user_id_str:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload",
            headers={"WWW-Authenticate": "Bearer"},
        )

    try:
        user_id = int(user_id_str)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid user identifier in token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User no longer exists",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user


def require_roles(*allowed_roles: Union[UserRole, str]) -> Callable:
    """
    Factory creating a dependency that verifies the authenticated user has one of the allowed roles.
    
    Roles & Permissions Matrix:
      - Admin: full platform management (users, events, results, leaderboards).
      - Creator: manage events & scoring rules.
      - Player: browse/join events & view personal information.
      - Players are strictly forbidden from modifying scores or rules.
    """
    role_values = [r.value if isinstance(r, UserRole) else str(r) for r in allowed_roles]

    def role_checker(current_user: User = Depends(get_current_user)) -> User:
        if current_user.role not in role_values:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Access forbidden: requires one of roles {role_values} (your role: {current_user.role})",
            )
        return current_user

    return role_checker


# ──────────────────────────────────────────────
# Convenience Role Dependencies
# ──────────────────────────────────────────────
# Only Admin can manage users, system-wide settings, and force overrides
require_admin = require_roles(UserRole.ADMIN)

# Tournament Creators and Admins can create/edit events and define scoring rules
require_creator = require_roles(UserRole.CREATOR, UserRole.ADMIN)

# Creators and Admins can manage uploads and score modifications (Players are blocked)
require_score_manager = require_roles(UserRole.CREATOR, UserRole.ADMIN)

# Any authenticated role (Player, Creator, Admin)
require_authenticated = require_roles(UserRole.PLAYER, UserRole.CREATOR, UserRole.ADMIN)
