from sqlalchemy import String, Text, Boolean, DateTime, BigInteger, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from datetime import datetime
from uuid import uuid4

from app.db.base import Base


class EvidenceItem(Base):
    __tablename__ = "evidence_items"

    id: Mapped[str] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid4
    )

    case_id: Mapped[str] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("cases.id"),
        nullable=False
    )

    evidence_tag: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False
    )

    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    description: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    evidence_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )

    source_path: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    acquisition_method: Mapped[str] = mapped_column(
        String(100),
    )

    acquired_by: Mapped[str] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=False
    )

    acquired_at: Mapped[datetime] = mapped_column(
        DateTime,
    )

    sha256: Mapped[str] = mapped_column(
        String(64),
        nullable=False
    )

    md5: Mapped[str | None] = mapped_column(
        String(32),
        nullable=True
    )

    size_bytes: Mapped[int] = mapped_column(
        BigInteger,
        nullable=False
    )

    is_verified: Mapped[bool] = mapped_column(
        Boolean,
        default=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )