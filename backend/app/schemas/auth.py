import uuid
from datetime import datetime

from pydantic import BaseModel, EmailStr, Field


# ──────────────────────────────────────────────────────
# Auth Schemas
# ──────────────────────────────────────────────────────

class UserRegister(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8)
    name: str = Field(..., min_length=1, max_length=100)


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class TokenRefresh(BaseModel):
    refresh_token: str


class TokenPayload(BaseModel):
    sub: str  # user UUID as string
    exp: int


class PasswordForgot(BaseModel):
    email: EmailStr


class PasswordReset(BaseModel):
    token: str
    new_password: str = Field(..., min_length=8)


class OAuthCallback(BaseModel):
    code: str
    redirect_uri: str
