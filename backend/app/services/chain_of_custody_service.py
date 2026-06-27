from uuid import UUID

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.repositories import ChainOfCustodyRepository
from app.schemas import ChainOfCustodyCreate, ChainOfCustodyOut
from app.services.audit_service import AuditService
from app.models import User, ChainOfCustody

class ChainOfCustodyService:
    @staticmethod
    def create_chain_of_custody(db: Session, payload: ChainOfCustodyCreate, current_user: User) -> ChainOfCustody:
        chain = ChainOfCustodyRepository(db).create_chain_of_custody(payload, current_user)

        audit_data = ChainOfCustodyOut.model_validate(chain).model_dump(mode="json")
        AuditService(db).log_create(
            entity_type="chain_of_custody",
            entity_id=chain.id,
            user_id=current_user.id,
            new_values=audit_data
        )

        db.commit()
        db.refresh(chain)
        return chain

    @staticmethod
    def get_chain_of_custody_by_id(db: Session, chain_of_custody_id: UUID) -> list[ChainOfCustody] | None:
        response = ChainOfCustodyRepository(db).get_chain_of_custody_by_id(chain_of_custody_id)
        if response is None:
            raise HTTPException(status_code=404, detail="Chain of custody not found")
        return response

    @staticmethod
    def get_chain_of_custody_by_evidence_id(db: Session, evidence_id: UUID) -> list[ChainOfCustody]:
        
        response = ChainOfCustodyRepository(db).get_chain_of_custody_by_evidence_id(evidence_id)
        if response is None:
            raise HTTPException(status_code=404, detail=f"Chain of custody not found for evidence id: {evidence_id}")
        return response
