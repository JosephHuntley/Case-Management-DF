import hashlib
import json
from uuid import UUID, uuid4

from app.schemas import ChainOfCustodyCreate
from app.models import ChainOfCustody, User


class ChainOfCustodyRepository:
    def __init__(self, db):
        self.db = db

    def create_chain_of_custody(self, chain_of_custody_data: ChainOfCustodyCreate, current_user: User) -> ChainOfCustody:
        previous_hash = self.get_last_hash(chain_of_custody_data.evidence_id)

        new_chain = ChainOfCustody(
            id=uuid4(),
            evidence_id=chain_of_custody_data.evidence_id,
            performed_by=current_user.id,
            action=chain_of_custody_data.action,
            from_person=chain_of_custody_data.from_person,
            to_person=chain_of_custody_data.to_person,
            notes=chain_of_custody_data.notes,
            previous_hash=previous_hash,
        )

        new_chain.row_hash = self._compute_row_hash(new_chain, previous_hash)

        self.db.add(new_chain)
        self.db.flush()
        return new_chain

    def get_last_hash(self, evidence_id: UUID) -> str | None:
        last = (
            self.db.query(ChainOfCustody)
            .filter(ChainOfCustody.evidence_id == evidence_id)
            .order_by(ChainOfCustody.created_at.desc())
            .first()
        )
        return last.row_hash if last else None

    def get_chain_of_custody_by_id(self, chain_of_custody_id: UUID) -> ChainOfCustody | None:
        return self.db.query(ChainOfCustody).filter(
            ChainOfCustody.id == chain_of_custody_id
        ).first()

    def get_chain_of_custody_by_evidence_id(self, evidence_id: UUID) -> list[ChainOfCustody]:
        
        return (
            self.db.query(ChainOfCustody)
            .filter(ChainOfCustody.evidence_id == evidence_id)
            .order_by(ChainOfCustody.created_at.asc())
            .all()
        )

    def verify_chain_of_custody(self, evidence_id: UUID) -> dict:
        """
        Walks every custody entry for an evidence item in order and
        recomputes each entry's hash from its stored fields, confirming:
          1. entry.previous_hash matches the previous entry's row_hash
             (or None, for the first entry)
          2. entry.row_hash matches what recomputing the hash from the
             entry's own fields produces

        A mismatch on either means either a record was edited after the
        fact, or a record is missing/out of order — either way, the chain
        is not trustworthy from that point forward.
        """
        entries = self.get_chain_of_custody_by_evidence_id(evidence_id)

        is_valid = True
        broken_entry_ids: list[UUID] = []
        expected_previous_hash: str | None = None

        for entry in entries:
            entry_ok = True

            if entry.previous_hash != expected_previous_hash:
                entry_ok = False

            recomputed = self._compute_row_hash(entry, entry.previous_hash)
            if recomputed != entry.row_hash:
                entry_ok = False

            if not entry_ok:
                is_valid = False
                broken_entry_ids.append(entry.id)

            expected_previous_hash = entry.row_hash

        return {
            "evidence_id": evidence_id,
            "is_valid": is_valid,
            "entry_count": len(entries),
            "broken_entry_ids": broken_entry_ids,
        }

    @staticmethod
    def _compute_row_hash(entry: ChainOfCustody, previous_hash: str | None) -> str:
        action_value = entry.action.value if hasattr(entry.action, "value") else entry.action
        payload = {
            "evidence_id": str(entry.evidence_id),
            "performed_by": str(entry.performed_by),
            "action": action_value,
            "from_person": entry.from_person,
            "to_person": entry.to_person,
            "notes": entry.notes,
            "previous_hash": previous_hash,
        }
        return hashlib.sha256(
            json.dumps(payload, sort_keys=True, default=str).encode()
        ).hexdigest()