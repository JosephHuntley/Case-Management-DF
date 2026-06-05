from datetime import datetime
from enum import Enum
from typing import TYPE_CHECKING
from uuid import UUID, uuid4
from sqlalchemy import String, Text, Boolean, DateTime, BigInteger, ForeignKey, func
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base

if TYPE_CHECKING:
    from app.models import Case, User, ChainOfCustody

class EvidenceType(str, Enum):
    DISK_IMAGE = "disk_image"
    MEMORY_DUMP = "memory_dump"
    NETWORK_CAPTURE = "network_capture"
    LOG_FILE = "log_file"
    DOCUMENT = "document"
    PHOTOGRAPH = "photograph"
    OTHER = "other"


class AcquisitionMethod(str, Enum):
    DD = "dd"
    FTK = "ftk"
    ENCASE = "encase"
    CELLEBRITE = "cellebrite"
    MANUAL = "manual"
    OTHER = "other"


class EvidenceItem(Base):
    __tablename__ = "evidence_items"

    id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True),
        primary_key=True,
        default=uuid4
    )
    case_id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True),
        ForeignKey("cases.id", ondelete="CASCADE"),
        nullable=False
    )
    acquired_by: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True),
        ForeignKey("users.id", ondelete="RESTRICT"),
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
    evidence_type: Mapped[EvidenceType] = mapped_column(
        SQLEnum(EvidenceType, name="evidence_type"),
        nullable=False
    )
    source_path: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )
    acquisition_method: Mapped[AcquisitionMethod | None] = mapped_column(
        SQLEnum(AcquisitionMethod, name="acquisition_method"),
        nullable=True
    )
    acquired_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False
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
        default=False,
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

    # Relationships
    case: Mapped["Case"] = relationship(
        "Case",
        back_populates="evidence_items"
    )
    acquirer: Mapped["User"] = relationship(
        "User",
        back_populates="acquired_evidence"
    )
    custody_chain: Mapped[list["ChainOfCustody"]] = relationship(
    "ChainOfCustody",
    back_populates="evidence",
    cascade="all, delete-orphan",
    order_by="ChainOfCustody.created_at"
)