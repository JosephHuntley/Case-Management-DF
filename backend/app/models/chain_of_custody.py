from datetime import datetime
from enum import Enum
from typing import TYPE_CHECKING
from uuid import UUID, uuid4
from sqlalchemy import String, Text, ForeignKey, DateTime, Enum as SQLEnum, func
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base

if TYPE_CHECKING:
    from app.models.evidence_item import EvidenceItem
    from app.models.user import User


class CustodyAction(str, Enum):
    COLLECTED = "collected"
    TRANSFERRED = "transferred"
    CHECKED_OUT = "checked_out"
    RETURNED = "returned"
    ARCHIVED = "archived"


class ChainOfCustody(Base):
    __tablename__ = "chain_of_custody"

    id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True),
        primary_key=True,
        default=uuid4
    )
    evidence_id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True),
        ForeignKey("evidence_items.id", ondelete="RESTRICT"),
        nullable=False,
        index=True
    )
    performed_by: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True),
        ForeignKey("users.id", ondelete="RESTRICT"),
        nullable=False
    )
    action: Mapped[CustodyAction] = mapped_column(
        SQLEnum(CustodyAction, name="custody_action"),
        nullable=False
    )
    from_person: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True
    )
    to_person: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True
    )
    notes: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
        index=True
    )

    # Relationships
    evidence: Mapped["EvidenceItem"] = relationship(
        "EvidenceItem",
        back_populates="custody_chain"
    )
    performer: Mapped["User"] = relationship(
        "User",
        back_populates="custody_actions"
    )