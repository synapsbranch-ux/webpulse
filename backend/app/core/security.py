"""JWT token creation/decoding and password hashing utilities."""
from __future__ import annotations

import logging
from datetime import datetime, timedelta, timezone
from typing import Any, Optional

from jose import JWTError, jwt
from passlib.context import CryptContext

from app.config import settings

logger = logging.getLogger(__name__)

# ── Password hashing ──
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """Hash a plaintext password using bcrypt."""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plaintext password against its bcrypt hash."""
    return pwd_context.verify(plain_password, hashed_password)


# ── JWT helpers ──

def _create_token(
    data: dict[str, Any],
    token_type: str,
    expires_delta: timedelta,
) -> str:
    """Internal helper to create a signed JWT with an expiration and type claim."""
    now = datetime.now(timezone.utc)
    payload = {
        **data,
        "type": token_type,
        "iat": now,
        "exp": now + expires_delta,
    }
    return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)


def create_access_token(
    sub: str,
    expires_delta: Optional[timedelta] = None,
) -> str:
    """Create a short-lived access token (default 30 min).

    Args:
        sub: Subject claim — typically the user UUID as a string.
        expires_delta: Custom expiration; falls back to settings.
    """
    delta = expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return _create_token({"sub": sub}, token_type="access", expires_delta=delta)


def create_refresh_token(
    sub: str,
    expires_delta: Optional[timedelta] = None,
) -> str:
    """Create a long-lived refresh token (default 7 days)."""
    delta = expires_delta or timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    return _create_token({"sub": sub}, token_type="refresh", expires_delta=delta)


def create_verification_token(email: str) -> str:
    """Create a 24-hour email verification token."""
    return _create_token(
        {"sub": email},
        token_type="verify",
        expires_delta=timedelta(hours=24),
    )


def create_reset_token(email: str) -> str:
    """Create a 1-hour password reset token."""
    return _create_token(
        {"sub": email},
        token_type="reset",
        expires_delta=timedelta(hours=1),
    )


def decode_token(token: str) -> Optional[dict[str, Any]]:
    """Decode and validate a JWT token.

    Returns:
        The decoded payload dict on success, or None if the token is
        invalid, expired, or cannot be decoded.
    """
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET,
            algorithms=[settings.JWT_ALGORITHM],
        )
        return payload
    except JWTError as exc:
        logger.debug("Token decode failed: %s", exc)
        return None
