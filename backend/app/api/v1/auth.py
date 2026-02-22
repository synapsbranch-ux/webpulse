"""Authentication API endpoints."""
from __future__ import annotations

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user
from app.core.database import get_db
from app.models.user import User
from app.schemas.auth import (
    OAuthCallback,
    PasswordForgot,
    PasswordReset,
    Token,
    TokenRefresh,
    UserLogin,
    UserRegister,
)
from app.services import auth_service

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=dict)
async def register(data: UserRegister, db: AsyncSession = Depends(get_db)) -> dict:
    """Register a new user account and send a verification email."""
    return await auth_service.register_user(db, data)


@router.post("/login", response_model=Token)
async def login(data: UserLogin, db: AsyncSession = Depends(get_db)) -> dict:
    """Authenticate with email and password, receive access + refresh tokens."""
    return await auth_service.login_user(db, data)


@router.get("/verify-email", response_model=dict)
async def verify_email(
    token: str = Query(..., description="Email verification token"),
    db: AsyncSession = Depends(get_db),
) -> dict:
    """Verify a user's email address using the token sent by email."""
    return await auth_service.verify_email(db, token)


@router.post("/refresh", response_model=Token)
async def refresh(data: TokenRefresh, db: AsyncSession = Depends(get_db)) -> dict:
    """Exchange a valid refresh token for a new access + refresh token pair."""
    return await auth_service.refresh_tokens(db, data.refresh_token)


@router.post("/logout", response_model=dict)
async def logout(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> dict:
    """Revoke all refresh tokens for the authenticated user."""
    return await auth_service.logout_user(db, current_user.id)


@router.post("/forgot-password", response_model=dict)
async def forgot_password(data: PasswordForgot, db: AsyncSession = Depends(get_db)) -> dict:
    """Request a password reset email."""
    return await auth_service.forgot_password(db, data.email)


@router.post("/reset-password", response_model=dict)
async def reset_password(data: PasswordReset, db: AsyncSession = Depends(get_db)) -> dict:
    """Reset password using a valid reset token."""
    return await auth_service.reset_password(db, data)


@router.post("/oauth/google", response_model=Token)
async def oauth_google(data: OAuthCallback, db: AsyncSession = Depends(get_db)) -> dict:
    """Authenticate via Google OAuth2 authorization code."""
    return await auth_service.oauth_google(db, data)


@router.post("/oauth/github", response_model=Token)
async def oauth_github(data: OAuthCallback, db: AsyncSession = Depends(get_db)) -> dict:
    """Authenticate via GitHub OAuth authorization code."""
    return await auth_service.oauth_github(db, data)
