# Schemas package
from app.schemas.auth import (
    UserRegister,
    UserLogin,
    Token,
    TokenRefresh,
    TokenPayload,
    PasswordForgot,
    PasswordReset,
    OAuthCallback,
)
from app.schemas.scan import ScanCreate, ScanSchema, ScanDetailSchema
from app.schemas.result import ScanResultCreate, ScanResultSchema
from app.schemas.report import ReportCreate, ReportSchema, AIScanAnalysis

__all__ = [
    "UserRegister",
    "UserLogin",
    "Token",
    "TokenRefresh",
    "TokenPayload",
    "PasswordForgot",
    "PasswordReset",
    "OAuthCallback",
    "ScanCreate",
    "ScanSchema",
    "ScanDetailSchema",
    "ScanResultCreate",
    "ScanResultSchema",
    "ReportCreate",
    "ReportSchema",
    "AIScanAnalysis",
]
