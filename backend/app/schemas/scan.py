import uuid
from datetime import datetime

from pydantic import BaseModel, HttpUrl

from app.models.scan import ScanStatus
from app.schemas.result import ScanResultSchema


# ──────────────────────────────────────────────────────
# Scan Schemas
# ──────────────────────────────────────────────────────

class ScanCreate(BaseModel):
    url: str  # validated by the orchestrator


class ScanSchema(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    url: str
    status: ScanStatus
    current_phase: str | None
    overall_score: int | None
    started_at: datetime | None
    completed_at: datetime | None
    duration_seconds: int | None
    created_at: datetime

    model_config = {"from_attributes": True}


class ScanDetailSchema(ScanSchema):
    """Scan with its module results embedded."""
    results: list[ScanResultSchema] = []
