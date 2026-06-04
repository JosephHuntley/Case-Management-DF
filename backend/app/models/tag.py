from datetime import datetime
from uuid import UUID, uuid4
from typing import TYPE_CHECKING
from sqlalchemy import String, Text, DateTime, func
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base

if TYPE_CHECKING:
    from app.models.case import Case


class Tag(Base):
    __tablename__ = "tags"

    id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True),
        primary_key=True,
        default=uuid4
    )
    name: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False
    )
    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )
    color: Mapped[str | None] = mapped_column(
        String(7),  # Hex color code, e.g., #FF5733
        nullable=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )

    cases: Mapped[list["Case"]] = relationship(
        "Case",
        secondary="case_tags",
        back_populates="tags"
    )