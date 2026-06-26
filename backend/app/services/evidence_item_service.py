from uuid import UUID, uuid4

from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models import User, EvidenceItem
from app.schemas import EvidenceItemCreate, EvidenceItemOut, EvidenceItemUpdate
from app.repositories import EvidenceItemRepository
from app.services import AuditService

class EvidenceService:
    @staticmethod
    def create_evidence(db: Session, payload: EvidenceItemCreate, current_user: User) -> EvidenceItem:
        item = EvidenceItemRepository(db).create_evidence(payload)

        audit_data = EvidenceItemOut.model_validate(item).model_dump(mode="json")
        AuditService(db).log_create(
            entity_type="evidence_item",
            entity_id=item.id,
            user_id=current_user.id,
            new_values=audit_data
        )

        db.commit()
        db.refresh(item)
        return item
    
    @staticmethod
    def get_by_id(db:Session, evidence_id:UUID) -> EvidenceItem:
        data = EvidenceItemRepository(db).get_evidence_item_by_id(evidence_id)
        if data is None:
            raise HTTPException(status_code=404, detail="Evidence Item not found")
        return data
    
    def get_by_case_id(db:Session, case_id:UUID) -> list[EvidenceItem]:
        response = EvidenceItemRepository(db).get_evidence_item_by_case_id(case_id)
        if response is None:
            raise HTTPException(status_code=404, detail=f"Evidence item for case {case_id} not found")
        return response
    
    def update_evidence(db: Session, evidence_id: UUID, payload: EvidenceItemUpdate, current_user: User) -> EvidenceItem | None:
        item = EvidenceItemRepository(db).get_evidence_item_by_id(evidence_id)
        if item is None:
            raise HTTPException(status_code=404, detail="Evidence Item not found")

        old_data = EvidenceItemOut.model_validate(item).model_dump(mode="json")
        response = EvidenceItemRepository(db).update_evidence_item(item, payload, db)
        new_data = EvidenceItemOut.model_validate(response).model_dump(mode="json")

        AuditService(db).log_update(
            entity_id=response.id,
            entity_type="Evidence Item",
            user_id=current_user.id,
            old_values=old_data,
            new_values=new_data,
        )
        db.commit()
        db.refresh(response)
        return response