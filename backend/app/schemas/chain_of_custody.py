from uuid import UUID
from pydantic import BaseModel, ConfigDict
from app.models import CustodyAction
from datetime import datetime


class ChainOfCustodyBase(BaseModel):
    evidence_id: UUID
    action: CustodyAction
    from_person: str | None = None
    to_person: str | None = None
    notes: str | None = None

class ChainOfCustodyCreate(ChainOfCustodyBase):
    pass

class ChainOfCustodyOut(ChainOfCustodyBase):
    id: UUID
    performed_by: UUID
    created_at: datetime
    previous_hash: str | None = None
    row_hash: str

    model_config = ConfigDict(from_attributes=True)


class ChainOfCustodyVerifyOut(BaseModel):
    evidence_id: UUID
    is_valid: bool
    entry_count: int
    broken_entry_ids: list[UUID]