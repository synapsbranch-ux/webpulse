"""Authentication business logic — registration, login, OAuth, password reset."""
from __future__ import annotations

import logging
import uuid
from datetime import datetime, timedelta, timezone
from typing import Any

import httpx
from fastapi import HTTPException, status
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.core.redis import check_rate_limit
from app.core.security import (
    create_access_token,
    create_refresh_token,
    create_reset_token,
    create_verification_token,
    decode_token,
    hash_password,
    verify_password,
)
from app.models.refresh_tokens import RefreshToken
from app.models.user import AuthProvider, User
from app.schemas.auth import OAuthCallback, PasswordReset, UserLogin, UserRegister

logger = logging.getLogger(__name__)


# ── helpers ──

async def _create_token_pair(db: AsyncSession, user: User) -> dict[str, str]:
    """Generate an access + refresh token pair and persist the refresh token."""
    user_id_str = str(user.id)
    access_token = create_access_token(sub=user_id_str)
    refresh_token = create_refresh_token(sub=user_id_str)

    db_token = RefreshToken(
        user_id=user.id,
        token=refresh_token,
        expires_at=datetime.now(timezone.utc) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS),
    )
    db.add(db_token)
    await db.flush()

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }


# ── public API ──

async def register_user(db: AsyncSession, data: UserRegister) -> dict[str, str]:
    """Register a new user with email/password and send a verification email.

    Returns a message dict; does NOT return tokens (user must verify first).
    """
    existing = await db.execute(select(User).where(User.email == data.email))
    if existing.scalar_one_or_none() is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )

    user = User(
        email=data.email,
        password_hash=hash_password(data.password),
        name=data.name,
        auth_provider=AuthProvider.email,
        is_verified=False,
    )
    db.add(user)
    await db.flush()

    token = create_verification_token(data.email)
    try:
        from app.services.email_service import send_verification_email
        await send_verification_email(data.email, token)
    except Exception:
        logger.exception("Failed to send verification email to %s", data.email)

    return {"message": "Registration successful. Please check your email to verify your account."}


async def login_user(db: AsyncSession, data: UserLogin) -> dict[str, str]:
    """Authenticate via email + password and return an access/refresh token pair."""
    allowed = await check_rate_limit(f"login:{data.email}", max_attempts=5, window_seconds=60)
    if not allowed:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Too many login attempts. Please try again later.",
        )

    result = await db.execute(select(User).where(User.email == data.email))
    user = result.scalar_one_or_none()

    if user is None or user.password_hash is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    if not verify_password(data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    if not user.is_verified:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Email not verified. Please check your inbox.",
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account deactivated",
        )

    return await _create_token_pair(db, user)


async def verify_email(db: AsyncSession, token: str) -> dict[str, str]:
    """Decode a verification token and mark the user as verified."""
    payload = decode_token(token)
    if payload is None or payload.get("type") != "verify":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired verification token",
        )

    email: str = payload["sub"]
    result = await db.execute(select(User).where(User.email == email))
    user = result.scalar_one_or_none()

    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    if user.is_verified:
        return {"message": "Email already verified"}

    user.is_verified = True
    await db.flush()
    return {"message": "Email verified successfully"}


async def refresh_tokens(db: AsyncSession, refresh_token_str: str) -> dict[str, str]:
    """Validate a refresh token, revoke it, and issue a new pair."""
    payload = decode_token(refresh_token_str)
    if payload is None or payload.get("type") != "refresh":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired refresh token",
        )

    result = await db.execute(
        select(RefreshToken).where(
            RefreshToken.token == refresh_token_str,
            RefreshToken.is_revoked == False,  # noqa: E712
        )
    )
    db_token = result.scalar_one_or_none()
    if db_token is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token not found or already revoked",
        )

    if db_token.expires_at.replace(tzinfo=timezone.utc) < datetime.now(timezone.utc):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token expired",
        )

    db_token.is_revoked = True
    await db.flush()

    user_result = await db.execute(select(User).where(User.id == db_token.user_id))
    user = user_result.scalar_one_or_none()
    if user is None or not user.is_active:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")

    return await _create_token_pair(db, user)


async def logout_user(db: AsyncSession, user_id: uuid.UUID) -> dict[str, str]:
    """Revoke all refresh tokens for the given user."""
    await db.execute(
        update(RefreshToken)
        .where(RefreshToken.user_id == user_id, RefreshToken.is_revoked == False)  # noqa: E712
        .values(is_revoked=True)
    )
    await db.flush()
    return {"message": "Logged out successfully"}


async def forgot_password(db: AsyncSession, email: str) -> dict[str, str]:
    """Send a password-reset email. Always returns 200 to prevent user enumeration."""
    result = await db.execute(select(User).where(User.email == email))
    user = result.scalar_one_or_none()

    if user is not None:
        token = create_reset_token(email)
        try:
            from app.services.email_service import send_reset_email
            await send_reset_email(email, token)
        except Exception:
            logger.exception("Failed to send reset email to %s", email)

    return {"message": "If that email is registered, a reset link has been sent."}


async def reset_password(db: AsyncSession, data: PasswordReset) -> dict[str, str]:
    """Decode a reset token and update the user's password."""
    payload = decode_token(data.token)
    if payload is None or payload.get("type") != "reset":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired reset token",
        )

    email: str = payload["sub"]
    result = await db.execute(select(User).where(User.email == email))
    user = result.scalar_one_or_none()

    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    user.password_hash = hash_password(data.new_password)
    await db.flush()

    # Revoke all refresh tokens as a security measure
    await db.execute(
        update(RefreshToken)
        .where(RefreshToken.user_id == user.id, RefreshToken.is_revoked == False)  # noqa: E712
        .values(is_revoked=True)
    )
    await db.flush()

    return {"message": "Password reset successfully"}


async def oauth_google(db: AsyncSession, data: OAuthCallback) -> dict[str, str]:
    """Handle Google OAuth callback: exchange code for user info, create or find user."""
    async with httpx.AsyncClient() as client:
        token_response = await client.post(
            "https://oauth2.googleapis.com/token",
            data={
                "code": data.code,
                "client_id": settings.GOOGLE_CLIENT_ID,
                "client_secret": settings.GOOGLE_CLIENT_SECRET,
                "redirect_uri": data.redirect_uri,
                "grant_type": "authorization_code",
            },
        )

    if token_response.status_code != 200:
        logger.error("Google token exchange failed: %s", token_response.text)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to authenticate with Google",
        )

    tokens = token_response.json()
    access_token = tokens.get("access_token")

    async with httpx.AsyncClient() as client:
        userinfo_response = await client.get(
            "https://www.googleapis.com/oauth2/v2/userinfo",
            headers={"Authorization": f"Bearer {access_token}"},
        )

    if userinfo_response.status_code != 200:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to fetch Google user info",
        )

    google_user: dict[str, Any] = userinfo_response.json()
    email = google_user.get("email")
    name = google_user.get("name", email)
    avatar = google_user.get("picture")
    provider_id = google_user.get("id")

    if not email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Google account has no email",
        )

    return await _upsert_oauth_user(
        db, email=email, name=name, avatar_url=avatar,
        provider=AuthProvider.google, provider_id=provider_id,
    )


async def oauth_github(db: AsyncSession, data: OAuthCallback) -> dict[str, str]:
    """Handle GitHub OAuth callback: exchange code for user info, create or find user."""
    async with httpx.AsyncClient() as client:
        token_response = await client.post(
            "https://github.com/login/oauth/access_token",
            json={
                "client_id": settings.GITHUB_CLIENT_ID,
                "client_secret": settings.GITHUB_CLIENT_SECRET,
                "code": data.code,
                "redirect_uri": data.redirect_uri,
            },
            headers={"Accept": "application/json"},
        )

    if token_response.status_code != 200:
        logger.error("GitHub token exchange failed: %s", token_response.text)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to authenticate with GitHub",
        )

    tokens = token_response.json()
    access_token = tokens.get("access_token")
    if not access_token:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="GitHub did not return an access token",
        )

    async with httpx.AsyncClient() as client:
        user_response = await client.get(
            "https://api.github.com/user",
            headers={"Authorization": f"Bearer {access_token}"},
        )
        email_response = await client.get(
            "https://api.github.com/user/emails",
            headers={"Authorization": f"Bearer {access_token}"},
        )

    if user_response.status_code != 200:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to fetch GitHub user info",
        )

    github_user: dict[str, Any] = user_response.json()
    name = github_user.get("name") or github_user.get("login", "")
    avatar = github_user.get("avatar_url")
    provider_id = str(github_user.get("id", ""))

    email = None
    if email_response.status_code == 200:
        emails = email_response.json()
        for e in emails:
            if e.get("primary") and e.get("verified"):
                email = e.get("email")
                break
        if email is None and emails:
            email = emails[0].get("email")

    if not email:
        email = github_user.get("email")
    if not email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="GitHub account has no email",
        )

    return await _upsert_oauth_user(
        db, email=email, name=name, avatar_url=avatar,
        provider=AuthProvider.github, provider_id=provider_id,
    )


async def _upsert_oauth_user(
    db: AsyncSession,
    *,
    email: str,
    name: str,
    avatar_url: str | None,
    provider: AuthProvider,
    provider_id: str | None,
) -> dict[str, str]:
    """Find or create a user from an OAuth provider, then return tokens."""
    result = await db.execute(select(User).where(User.email == email))
    user = result.scalar_one_or_none()

    if user is None:
        user = User(
            email=email,
            name=name,
            avatar_url=avatar_url,
            auth_provider=provider,
            provider_id=provider_id,
            is_verified=True,
        )
        db.add(user)
        await db.flush()
        logger.info("Created OAuth user %s via %s", email, provider.value)
    else:
        if user.avatar_url is None and avatar_url:
            user.avatar_url = avatar_url
        if user.provider_id is None and provider_id:
            user.provider_id = provider_id
            user.auth_provider = provider
        if not user.is_verified:
            user.is_verified = True
        await db.flush()

    return await _create_token_pair(db, user)
