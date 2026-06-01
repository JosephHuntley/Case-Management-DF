from pydantic import BaseModel, ConfigDict
from uuid import UUID
from datetime import datetime

class UserBase(BaseModel):
    username: str
    email: str
    role: str

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    username: str | None = None
    email: str | None = None
    role: str | None = None
    is_active: bool | None = None

class UserOut(UserBase):
    id: UUID
    is_active: bool
    created_at: datetime
    deleted_at: datetime | None

    model_config = ConfigDict(from_attributes=True)