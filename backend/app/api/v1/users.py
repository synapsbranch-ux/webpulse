"""User profile management endpoints."""
from __future__ import annotations

import logging

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user
from app.core.database import get_db
from app.core.security import hash_password, verify_password
from app.models.user import User

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/users", tags=["Users"])


# ── Request / Response schemas (local to this router) ──

class UserResponse(BaseModel):
    """Public user profile representation."""
    id: str
    email: str
    name: str
    avatar_url: str | None
    is_verified: bool
    auth_provider: str
    created_at: str

    model_config = {"from_attributes": True}


class UserUpdate(BaseModel):
    """Fields a user can update on their profile."""
    name: str | None = Field(None, min_length=1, max_length=100)
    avatar_url: str | None = None


class PasswordChange(BaseModel):
    """Payload for changing password."""
    old_password: str
    new_password: str = Field(..., min_length=8)


# ── Endpoints ──

@router.get("/me", response_model=UserResponse)
async def get_me(current_user: User = Depends(get_current_user)) -> dict:
    """Return the authenticated user's profile."""
    return {
        "id": str(current_user.id),
        "email": current_user.email,
        "name": current_user.name,
        "avatar_url": current_user.avatar_url,
        "is_verified": current_user.is_verified,
        "auth_provider": current_user.auth_provider.value,
        "created_at": current_user.created_at.isoformat(),
    }


@router.put("/me", response_model=UserResponse)
async def update_me(
    data: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> dict:
    """Update the authenticated user's profile (name, avatar)."""
    if data.name is not None:
        current_user.name = data.name
    if data.avatar_url is not None:
        current_user.avatar_url = data.avatar_url

    await db.flush()

    return {
        "id": str(current_user.id),
        "email": current_user.email,
        "name": current_user.name,
        "avatar_url": current_user.avatar_url,
        "is_verified": current_user.is_verified,
        "auth_provider": current_user.auth_provider.value,
        "created_at": current_user.created_at.isoformat(),
    }


@router.put("/me/password", response_model=dict)
async def change_password(
    data: PasswordChange,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> dict:
    """Change the authenticated user's password (requires current password)."""
    if current_user.password_hash is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="OAuth users cannot change password this way",
        )

    if not verify_password(data.old_password, current_user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Current password is incorrect",
        )

    current_user.password_hash = hash_password(data.new_password)
    await db.flush()
    return {"message": "Password changed successfully"}


@router.delete("/me", response_model=dict)
async def delete_me(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> dict:
    """Soft-delete the authenticated user's account (deactivate)."""
    current_user.is_active = False
    await db.flush()
    logger.info("User %s deactivated their account", current_user.id)
    return {"message": "Account deactivated successfully"}
