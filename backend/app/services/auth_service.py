# app/services/auth_service.py
# ──────────────────────────────────────────────
# Authentication Service Business Logic
# ──────────────────────────────────────────────

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.security import hash_password, verify_password, create_access_token
from app.models.user import User
from app.schemas.auth import UserRegister, UserLogin, TokenResponse, UserResponse


class AuthService:
    """Service handling user registration, credential verification, and JWT generation."""

    @staticmethod
    def register_user(db: Session, user_in: UserRegister) -> User:
        """
        Registers a new user after verifying email uniqueness and hashing the password.
        """
        # Normalize email
        email_normalized = user_in.email.strip().lower()

        # Check duplicate email
        existing_user = db.query(User).filter(User.email == email_normalized).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="A user with this email already exists",
            )

        # Hash password securely
        pwd_hash = hash_password(user_in.password)

        # Create user record
        user = User(
            name=user_in.name.strip(),
            email=email_normalized,
            password_hash=pwd_hash,
            role=user_in.role.value if hasattr(user_in.role, "value") else str(user_in.role),
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    @staticmethod
    def authenticate_user(db: Session, login_data: UserLogin) -> User:
        """
        Authenticates a user with email and password.
        """
        email_normalized = login_data.email.strip().lower()
        user = db.query(User).filter(User.email == email_normalized).first()
        if not user or not verify_password(login_data.password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return user

    @classmethod
    def login_user(cls, db: Session, login_data: UserLogin) -> TokenResponse:
        """
        Validates credentials and returns JWT access token with user details.
        """
        user = cls.authenticate_user(db, login_data)
        token = create_access_token(subject=user.id, role=user.role)
        return TokenResponse(
            access_token=token,
            token_type="bearer",
            user=UserResponse.model_validate(user),
        )


auth_service = AuthService()
