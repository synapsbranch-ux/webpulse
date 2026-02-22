import uuid
from datetime import datetime
from typing import Any

from pydantic import BaseModel

from app.models.scan_result import ScanModule


# ──────────────────────────────────────────────────────
# Scan Result Schemas
# ──────────────────────────────────────────────────────

class ScanResultCreate(BaseModel):
    module: ScanModule
    score: int
    grade: str | None = None
    data: dict[str, Any] = {}
    issues_critical: int = 0
    issues_high: int = 0
    issues_medium: int = 0
    issues_low: int = 0


class ScanResultSchema(ScanResultCreate):
    id: uuid.UUID
    scan_id: uuid.UUID
    created_at: datetime

    model_config = {"from_attributes": True}
