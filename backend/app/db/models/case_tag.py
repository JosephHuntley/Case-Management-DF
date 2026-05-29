from datetime import datetime
from uuid import uuid4

from sqlalchemy import String, Text, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base

def CaseTag(Base):
    __tablename__ = "case_tags"

    case_id: Mapped[str] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("cases.id"),
        nullable=False
    )

    tag_id: Mapped[str] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("tags.id"),
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )

    from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, PrimaryKeyConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class CaseTag(Base):
    __tablename__ = "case_tags"

    case_id: Mapped[str] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("cases.id"),
        nullable=False
    )

    tag_id: Mapped[str] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("tags.id"),
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    __table_args__ = (
        PrimaryKeyConstraint("case_id", "tag_id"),
    )