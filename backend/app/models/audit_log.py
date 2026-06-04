from datetime import datetime
from enum import Enum
from typing import TYPE_CHECKING
from uuid import UUID
from sqlalchemy import String, DateTime, ForeignKey, JSON, BigInteger, func
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base

if TYPE_CHECKING:
    from app.models.user import User


class AuditAction(str, Enum):
    CREATE = "create"
    UPDATE = "update"
    DELETE = "delete"
    ARCHIVE = "archive"
    RESTORE = "restore"
    LOGIN = "login"
    LOGOUT = "logout"
    EXPORT = "export"


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
    entity_id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True),
        nullable=False,
        index=True
    )
    action: Mapped[AuditAction] = mapped_column(
        SQLEnum(AuditAction, name="audit_action"),
        nullable=False,
        index=True
    )
    changed_by: Mapped[UUID | None] = mapped_column(
        PGUUID(as_uuid=True),
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True
    )
    old_values: Mapped[dict | None] = mapped_column(
        JSON,
        nullable=True
    )
    new_values: Mapped[dict | None] = mapped_column(
        JSON,
        nullable=True
    )
    previous_hash: Mapped[str | None] = mapped_column(
        String(64),
        nullable=True
    )
    row_hash: Mapped[str] = mapped_column(
        String(64),
        nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
        index=True
    )

    # Relationships
    actor: Mapped["User | None"] = relationship(
        "User",
        back_populates="audit_logs"
    )