from datetime import datetime
from uuid import uuid4
from enum import Enum

from sqlalchemy import String, Text, ForeignKey, DateTime, Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base

class Action(str, Enum):
    COLLECTED = "collected"
    TRANSFERED = "transfered"
    CHECKED_OUT = "checked_out"
    RETURNED = "returned"
    ARCHIVED = "archived"

def ChainOfCustody(Base):
    __tablename__ = "chain_of_custody"

    id: Mapped[str] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid4
    )

    evidence_id: Mapped[str] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("evidence_items.id"),
        nullable=False
    )

    action: Mapped[Action] = mapped_column(
        SQLEnum(Action, name="chain_of_custody_actions"),
        nullable=False
    )

    performed_by: Mapped[str] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=False
    )

    from_person: Mapped[str] = mapped_column(
        String(255)
    )

    to_person: Mapped[str] = mapped_column(
        String(255)
    )

    notes: Mapped[str] = mapped_column(
        Text
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )
