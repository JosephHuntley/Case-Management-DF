from pydantic import BaseModel, ConfigDict, Field
from uuid import UUID
from datetime import datetime
from .tag import TagOut


class CaseBase(BaseModel):
    title: str
    description: str
    status: str = "open"
    priority: str = "medium"
    created_by: UUID
    deleted_at: datetime | None = None


class CaseCreate(CaseBase):
    pass


class CaseUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    status: str | None = None
    priority: str | None = None
    assigned_to: UUID | None = None
    closed_at: datetime | None = None
    tag_ids: list[UUID] | None = None


class CaseOut(CaseBase):
    id: UUID
    case_number: str
    created_at: datetime
    updated_at: datetime

    tags: list[TagOut] = Field(default_factory=list)

    model_config = ConfigDict(from_attributes=True)

