from datetime import datetime
from uuid import uuid4

from sqlalchemy import (
    String,
    DateTime,
    ForeignKey,
    JSON,
    BigInteger
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class AuditLog(Base):
    __tablename__ = "audit_log"

    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        autoincrement=True
    )

    entity_type: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        index=True
    )

    entity_id: Mapped[str] = mapped_column(
        UUID(as_uuid=True),
        nullable=False,
        index=True
    )

    action: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )

    changed_by: Mapped[str] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=False
    )

    old_values: Mapped[dict] = mapped_column(
        JSON,
        nullable=True
    )

    new_values: Mapped[dict] = mapped_column(
        JSON,
        nullable=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        nullable=False
    )