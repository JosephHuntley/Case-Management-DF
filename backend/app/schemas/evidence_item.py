from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, ConfigDict
from app.models.evidence_item import EvidenceType, AcquisitionMethod


class EvidenceItemBase(BaseModel):
    case_id: UUID
    acquired_by: UUID
    evidence_tag: str
    name: str
    description: str
    evidence_type: EvidenceType
    acquisition_method: AcquisitionMethod | None = None
    acquired_at: datetime
    sha256: str
    md5: str | None = None
    size_bytes: int
    is_verified: bool = False
    source_path: str | None = None


class EvidenceItemCreate(EvidenceItemBase):
    pass


class EvidenceItemUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    evidence_type: EvidenceType | None = None
    md5: str | None = None
    is_verified: bool | None = None
    source_path: str | None = None


class EvidenceItemOut(EvidenceItemBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)