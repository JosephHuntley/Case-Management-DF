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
    created_at: str
    performed_by: UUID
    evidence_id: UUID
    action: CustodyAction
    from_person: str | None = None
    to_person: str | None = None
    notes: str | None = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)