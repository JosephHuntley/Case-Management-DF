from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, ConfigDict


class CaseNoteBase(BaseModel):
    note: str
    case_id: UUID


class CaseNoteCreate(CaseNoteBase):
    pass


class CaseNoteUpdate(BaseModel):
    note: str | None = None


class CaseNoteOut(CaseNoteBase):
    id: UUID
    author_id: UUID
    updated_by: UUID | None = None
    is_archived: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)