from datetime import datetime, timezone
from enum import Enum
from typing import TYPE_CHECKING
from uuid import UUID, uuid4
from sqlalchemy import String, Text, ForeignKey, DateTime, Enum as SQLEnum, func
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..db.base import Base

if TYPE_CHECKING:
    from app.models.tag import Tag
    from app.models.user import User
    from app.models.case_note import CaseNote
    from app.models.evidence_item import EvidenceItem
    from app.models.report import Report


class CaseStatus(str, Enum):
    OPEN = "open"
    CLOSED = "closed"
    ARCHIVED = "archived"
    PENDING = "pending"
    IN_PROGRESS = "in progress"


class CasePriority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class Case(Base):
    __tablename__ = "cases"

    id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True),
        primary_key=True,
        default=uuid4
    )
    case_number: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False
    )
    title: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )
    description: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )
    status: Mapped[CaseStatus] = mapped_column(
        SQLEnum(CaseStatus, name="case_status"),
        nullable=False,
        default=CaseStatus.OPEN
    )
    priority: Mapped[CasePriority] = mapped_column(
        SQLEnum(CasePriority, name="case_priority"),
        nullable=False,
        default=CasePriority.MEDIUM
    )
    created_by: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True),
        ForeignKey("users.id", ondelete="RESTRICT"),
        nullable=False
    )
    assigned_to: Mapped[UUID | None] = mapped_column(
        PGUUID(as_uuid=True),
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True
    )
    opened_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )
    closed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )
    deleted_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True
    )

    # Relationships
    creator: Mapped["User"] = relationship(
        "User",
        foreign_keys="Case.created_by",
        back_populates="created_cases"
    )
    assignee: Mapped["User | None"] = relationship(
        "User",
        foreign_keys="Case.assigned_to",
        back_populates="assigned_cases"
    )
    tags: Mapped[list["Tag"]] = relationship(
        "Tag",
        secondary="case_tags",
        back_populates="cases"
    )
    notes: Mapped[list["CaseNote"]] = relationship(
        "CaseNote",
        back_populates="case",
        cascade="all, delete-orphan"
    )
    evidence_items: Mapped[list["EvidenceItem"]] = relationship(
        "EvidenceItem",
        back_populates="case",
        cascade="all, delete-orphan"
    )
    reports: Mapped[list["Report"]] = relationship(
        "Report",
        back_populates="case",
        cascade="all, delete-orphan"
    )