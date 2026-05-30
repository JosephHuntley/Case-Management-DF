from pydantic import BaseModel, ConfigDict
from uuid import UUID

class TagBase(BaseModel):
    name: str
    description: str | None = None
    color: str | None = None

class TagCreate(TagBase):
    pass

class TagUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    color: str | None = None

class TagOut(TagBase):
    id: UUID
    name: str
    color: str | None = None
    description: str | None = None

    model_config = ConfigDict(from_attributes=True)