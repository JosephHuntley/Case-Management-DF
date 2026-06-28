from pydantic import BaseModel, ConfigDict
from uuid import UUID
from datetime import datetime
from app.models import UserRole

class UserBase(BaseModel):
    username: str
    email: str
    role: str

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    # Must not include role mass assignment / privilege escalation risk
    username: str | None = None
    email: str | None = None
    is_active: bool | None = None

class UserRoleUpdate(BaseModel):
    role: UserRole

class UserOut(UserBase):
    id: UUID
    is_active: bool
    created_at: datetime
    deleted_at: datetime | None

    model_config = ConfigDict(from_attributes=True)