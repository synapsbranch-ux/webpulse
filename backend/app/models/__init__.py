# Models package — export all models so Alembic can detect them
from app.models.user import User, AuthProvider
from app.models.scan import Scan, ScanStatus
from app.models.scan_result import ScanResult, ScanModule
from app.models.report import Report
from app.models.refresh_tokens import RefreshToken

__all__ = [
    "User",
    "AuthProvider",
    "Scan",
    "ScanStatus",
    "ScanResult",
    "ScanModule",
    "Report",
    "RefreshToken",
]
