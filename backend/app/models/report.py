import uuid
from datetime import datetime

from sqlalchemy import Text, Boolean, DateTime, ForeignKey, func
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class Report(Base):
    __tablename__ = "reports"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    scan_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("scans.id", ondelete="CASCADE"), nullable=False, unique=True, index=True
    )
    ai_analysis: Mapped[dict | None] = mapped_column(JSONB, nullable=True, default=None)
    pdf_path: Mapped[str | None] = mapped_column(Text, nullable=True)
    email_sent: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    email_sent_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    scan: Mapped["Scan"] = relationship("Scan", back_populates="report")

    def __repr__(self) -> str:
        return f"<Report id={self.id} scan_id={self.scan_id} email_sent={self.email_sent}>"
