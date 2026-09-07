# app/routers/auth.py
# ──────────────────────────────────────────────
# Authentication & User Profile Routes
# ──────────────────────────────────────────────

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.deps import get_current_user
from app.database.database import get_db
from app.models.user import User
from app.schemas.auth import UserRegister, UserLogin, UserResponse, TokenResponse
from app.services.auth_service import auth_service

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user",
    description="Registers a new user account with role ('player', 'creator', or 'admin').",
)
def register(user_in: UserRegister, db: Session = Depends(get_db)):
    """Register a new user account with secure password hashing."""
    user = auth_service.register_user(db, user_in)
    return user


@router.post(
    "/login",
    response_model=TokenResponse,
    summary="Authenticate user and obtain JWT token",
    description="Validates email and password, returning a JWT bearer token.",
)
def login(login_data: UserLogin, db: Session = Depends(get_db)):
    """Authenticate and obtain JWT access token."""
    return auth_service.login_user(db, login_data)


@router.get(
    "/me",
    response_model=UserResponse,
    summary="Get current user profile",
    description="Returns the profile information of the currently authenticated user.",
)
def get_current_user_profile(current_user: User = Depends(get_current_user)):
    """Fetch current logged-in user profile."""
    return current_user
