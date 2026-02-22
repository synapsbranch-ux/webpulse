import uuid
from datetime import datetime
from typing import Any

from pydantic import BaseModel


# ──────────────────────────────────────────────────────
# Report Schemas
# ──────────────────────────────────────────────────────

class ReportCreate(BaseModel):
    scan_id: uuid.UUID
    ai_analysis: dict[str, Any] | None = None
    pdf_path: str | None = None


class ReportSchema(ReportCreate):
    id: uuid.UUID
    email_sent: bool
    email_sent_at: datetime | None
    created_at: datetime

    model_config = {"from_attributes": True}


class AIScanAnalysis(BaseModel):
    """Structured shape of the AI-generated analysis stored in JSONB."""
    executive_summary: str
    overall_score: int
    scores_by_category: dict[str, int]
    critical_issues: list[dict[str, Any]]
    warnings: list[dict[str, Any]]
    passed_checks: list[dict[str, Any]]
    recommendations: list[dict[str, Any]]
    performance_analysis: str
    security_analysis: str
    seo_analysis: str
