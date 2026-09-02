from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field
from app.models import CustodyAction
from datetime import datetime
from app.schemas.user import UserOut


class ChainOfCustodyBase(BaseModel):
    evidence_id: UUID
    action: CustodyAction
    from_person: UUID | None = None
    to_person: UUID | None = None
    notes: str | None = None

# TODO: Create doesn't require action since it should only be COLLECTED
class ChainOfCustodyCreate(BaseModel):
    evidence_id: UUID
    action: CustodyAction
    to_person: UUID | None = None
    notes: str | None = None

class ChainOfCustodyAppend(ChainOfCustodyCreate):
    pass

class ChainOfCustodyOut(ChainOfCustodyBase):
    id: UUID
    performed_by: UserOut = Field(validation_alias="performer")
    from_person: UserOut | None = Field(default=None, validation_alias="from_person_user")
    to_person: UserOut | None = Field(default=None, validation_alias="to_person_user")
    created_at: datetime
    previous_hash: str | None = None
    row_hash: str

    model_config = ConfigDict(from_attributes=True)


class ChainOfCustodyVerifyOut(BaseModel):
    evidence_id: UUID
    is_valid: bool
    entry_count: int
    broken_entry_ids: list[UUID]