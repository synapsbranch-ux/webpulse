import uuid
import enum
from datetime import datetime

from sqlalchemy import String, Text, Integer, Enum as SAEnum, DateTime, ForeignKey, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class ScanStatus(str, enum.Enum):
    pending = "pending"
    running = "running"
    completed = "completed"
    failed = "failed"


class Scan(Base):
    __tablename__ = "scans"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    url: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[ScanStatus] = mapped_column(
        SAEnum(ScanStatus, name="scan_status_enum"), default=ScanStatus.pending, nullable=False
    )
    current_phase: Mapped[str | None] = mapped_column(String(50), nullable=True)
    overall_score: Mapped[int | None] = mapped_column(Integer, nullable=True)
    started_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    duration_seconds: Mapped[int | None] = mapped_column(Integer, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="scans")
    results: Mapped[list["ScanResult"]] = relationship(
        "ScanResult", back_populates="scan", cascade="all, delete-orphan"
    )
    report: Mapped["Report | None"] = relationship(
        "Report", back_populates="scan", cascade="all, delete-orphan", uselist=False
    )

    def __repr__(self) -> str:
        return f"<Scan id={self.id} url={self.url} status={self.status}>"
