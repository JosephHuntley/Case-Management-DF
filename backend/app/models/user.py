from enum import Enum
from datetime import datetime
from uuid import UUID, uuid4
from typing import TYPE_CHECKING
from sqlalchemy import String, Text, Boolean, DateTime, Enum as SQLEnum, func
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..db.base import Base

if TYPE_CHECKING:
    from app.models.case import Case
    from app.models.case_note import CaseNote
    from app.models.evidence_item import EvidenceItem
    from app.models.report import Report
    from app.models.audit_log import AuditLog
    from app.models.chain_of_custody import ChainOfCustody


class UserRole(str, Enum):
    ADMIN = "admin"
    INVESTIGATOR = "investigator"
    ANALYST = "analyst"
    VIEWER = "viewer"


class User(Base):
    __tablename__ = "users"

    id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True),
        primary_key=True,
        default=uuid4
    )
    username: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False
    )
    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False
    )
    password_hash: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )
    role: Mapped[UserRole] = mapped_column(
        SQLEnum(UserRole, name="user_roles"),
        nullable=False,
        default=UserRole.VIEWER
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False
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
    created_cases: Mapped[list["Case"]] = relationship(
        "Case",
        foreign_keys="Case.created_by",
        back_populates="creator"
    )
    assigned_cases: Mapped[list["Case"]] = relationship(
        "Case",
        foreign_keys="Case.assigned_to",
        back_populates="assignee"
    )
    notes: Mapped[list["CaseNote"]] = relationship(
        "CaseNote",
        foreign_keys="CaseNote.author_id",
        back_populates="author"
    )
    updated_notes: Mapped[list["CaseNote"]] = relationship(
        "CaseNote",
        foreign_keys="CaseNote.updated_by",
        back_populates="updated_by_user"
    )
    acquired_evidence: Mapped[list["EvidenceItem"]] = relationship(
        "EvidenceItem",
        back_populates="acquirer"
    )
    reports: Mapped[list["Report"]] = relationship(
        "Report",
        back_populates="author"
    )
    audit_logs: Mapped[list["AuditLog"]] = relationship(
        "AuditLog",
        back_populates="actor",
        foreign_keys="AuditLog.changed_by"
    )
    custody_actions: Mapped[list["ChainOfCustody"]] = relationship(
        "ChainOfCustody",
        back_populates="performer"
    )
