from pydantic import BaseModel
from uuid import UUID
from datetime import datetime


class CaseBase(BaseModel):
    title: str
    description: str
    status: str = "open"
    priority: str = "medium"


class CaseCreate(CaseBase):
    pass


class CaseUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    status: str | None = None
    priority: str | None = None
    assigned_to: UUID | None = None
    closed_at: datetime | None = None


class CaseOut(CaseBase):
    id: UUID
    case_number: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True