from enum import Enum
from datetime import datetime
from uuid import uuid4

from sqlalchemy import String, Text, Boolean, DateTime, Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class UserRole(str, Enum):
    ADMIN = "admin"
    INVESTIGATOR = "investigator"
    ANALYST = "analyst"
    VIEWER = "viewer"


class User(Base):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(
        UUID(as_uuid=True),
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
        default=datetime.utcnow,
        nullable=False
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False
    )