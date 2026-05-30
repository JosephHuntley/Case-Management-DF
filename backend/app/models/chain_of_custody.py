from datetime import datetime
from uuid import uuid4
from enum import Enum

from sqlalchemy import (
    String,
    Text,
    ForeignKey,
    DateTime,
    Enum as SQLEnum
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Action(str, Enum):
    COLLECTED = "collected"
    TRANSFERRED = "transferred"
    CHECKED_OUT = "checked_out"
    RETURNED = "returned"
    ARCHIVED = "archived"


class ChainOfCustody(Base):
    __tablename__ = "chain_of_custody"

    id: Mapped[str] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid4
    )

    evidence_id: Mapped[str] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("evidence_items.id", ondelete="RESTRICT"),
        nullable=False,
        index=True
    )

    action: Mapped[Action] = mapped_column(
        SQLEnum(Action, name="chain_of_custody_actions"),
        nullable=False
    )

    performed_by: Mapped[str] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="RESTRICT"),
        nullable=False
    )

    from_person: Mapped[str] = mapped_column(
        String(255),
        nullable=True
    )

    to_person: Mapped[str] = mapped_column(
        String(255),
        nullable=True
    )

    notes: Mapped[str] = mapped_column(
        Text,
        nullable=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        nullable=False,
        index=True
    )