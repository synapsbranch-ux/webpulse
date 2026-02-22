import uuid
import enum
from datetime import datetime

from sqlalchemy import String, Integer, Enum as SAEnum, DateTime, ForeignKey, func
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class ScanModule(str, enum.Enum):
    dns = "dns"
    ssl = "ssl"
    performance = "performance"
    security = "security"
    seo = "seo"


class ScanResult(Base):
    __tablename__ = "scan_results"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    scan_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("scans.id", ondelete="CASCADE"), nullable=False, index=True
    )
    module: Mapped[ScanModule] = mapped_column(
        SAEnum(ScanModule, name="scan_module_enum"), nullable=False
    )
    score: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    grade: Mapped[str | None] = mapped_column(String(5), nullable=True)
    data: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)
    issues_critical: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    issues_high: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    issues_medium: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    issues_low: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    scan: Mapped["Scan"] = relationship("Scan", back_populates="results")

    def __repr__(self) -> str:
        return f"<ScanResult scan_id={self.scan_id} module={self.module} score={self.score}>"
