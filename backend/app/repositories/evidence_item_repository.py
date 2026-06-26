from uuid import UUID, uuid4
from sqlalchemy.orm import Session

from app.models import EvidenceItem, User
from app.schemas import EvidenceItemCreate, EvidenceItemUpdate

class EvidenceItemRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_evidence(self, new_item: EvidenceItemCreate) -> EvidenceItem:
        item = EvidenceItem(
            id=uuid4(),
            case_id=new_item.case_id,
            acquired_by=new_item.acquired_by,
            evidence_tag=new_item.evidence_tag,
            name=new_item.name,
            description=new_item.description,
            evidence_type=new_item.evidence_type,
            source_path=new_item.source_path,
            acquisition_method=new_item.acquisition_method,
            acquired_at=new_item.acquired_at,
            sha256=new_item.sha256,
            md5=new_item.md5,
            size_bytes=new_item.size_bytes,
            is_verified=new_item.is_verified,
        )
        self.db.add(item)
        self.db.flush()
        return item

    def get_evidence_item_by_id(self, evidence_id: UUID) -> EvidenceItem | None:
        return self.db.query(EvidenceItem).filter(EvidenceItem.id == evidence_id).first()
    
    def get_evidence_item_by_case_id(self, case_id: UUID) -> list[EvidenceItem] | None:
        return self.db.query(EvidenceItem).filter(EvidenceItem.case_id == case_id).order_by(EvidenceItem.updated_at.desc()).all()

    def update_evidence_item(self, item: EvidenceItem, data: EvidenceItemUpdate, db: Session) -> EvidenceItem:
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(item, key, value)
        db.flush()
        return item