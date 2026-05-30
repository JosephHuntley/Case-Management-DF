from datetime import datetime
from uuid import uuid4

from sqlalchemy import String, Text, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

class Tag(Base):
    __tablename__ = "tags"

    id: Mapped[str] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid4
    )

    name: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False
    )

    description: Mapped[str] = mapped_column(
        Text
    )

    color: Mapped[str] = mapped_column(
        String(7)  # Hex color code, e.g., #FF5733
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )

    cases = relationship(
        "Case",
        secondary="case_tags",
        back_populates="tags"
    )
