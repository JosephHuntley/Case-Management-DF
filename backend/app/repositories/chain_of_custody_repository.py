from uuid import UUID, uuid4

from app.schemas import ChainOfCustodyCreate
from app.models import ChainOfCustody, User

class ChainOfCustodyRepository:
    def __init__(self, db):
        self.db = db

    async def create_chain_of_custody(self, chain_of_custody_data: ChainOfCustodyCreate, current_user: User) -> ChainOfCustody:
        new_chain = ChainOfCustody(
            id=uuid4(),
            evidence_id=chain_of_custody_data.evidence_id,
            performed_by=current_user.id,
            action=chain_of_custody_data.action,
            from_person=chain_of_custody_data.from_person,
            to_person=chain_of_custody_data.to_person,
            notes=chain_of_custody_data.notes
        )
        self.db.add(new_chain)
        self.db.flush()
        return new_chain

    async def get_chain_of_custody_by_id(self, chain_of_custody_id:UUID) -> ChainOfCustody | None:
        chain_of_custody = self.db.query(ChainOfCustody).filter(
            ChainOfCustody.id == chain_of_custody_id
        ).all()
        return chain_of_custody
    
    async def get_chain_of_custody_by_evidence_id(self, evidence_id: UUID):
        chain_of_custody_records = self.db.query(ChainOfCustody).filter(
            ChainOfCustody.evidence_id == evidence_id
        ).all()
        return chain_of_custody_records