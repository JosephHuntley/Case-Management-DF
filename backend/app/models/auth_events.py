from sqlalchemy import String, DateTime, JSON, BigInteger, func

from app.db.base import Base
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from enum import Enum
from sqlalchemy import Enum as SQLEnum

class AuthEventType(str, Enum):
    INVALID_USER = "Invalid User"
    INVALID_PASSWORD = "Invalid Password"

class AuthEvent(Base):
    __tablename__ = "auth_events"

    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        autoincrement=True
    )

    # Failed username attempted
    username_attempted: Mapped[str] = mapped_column(
        String(100),
        nullable=True
    )

    ip_addr: Mapped[str] = mapped_column(
        String(42), # 42 to future proof for IPv6
        nullable=False
    )
    
    user_agent: Mapped[str] = mapped_column(
        String(512),
        nullable=False
    )

    # This is mostly for future versions that may log every auth type not just failed logins
    event_type: Mapped[AuthEventType] = mapped_column(
        SQLEnum(AuthEventType, name="auth_event_type"), 
        nullable=False, 
        index=True)

    timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
        index=True
    )
