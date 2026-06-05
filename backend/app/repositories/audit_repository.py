import hashlib
import json

from uuid import UUID

from app.models import AuditLog
from app.schemas import AuditLogCreate
from app.db.session import SessionLocal


class AuditRepository:
    def __init__(self, db):
        self.db = db

    def create(self, log: AuditLogCreate):
        previous_hash = self.get_last_hash(log.entity_type, log.entity_id)


        db_log = AuditLog(
            **log.model_dump(),
            previous_hash=previous_hash,
        )

        payload = {
            "entity_type": db_log.entity_type,
            "entity_id": str(db_log.entity_id),
            "action": db_log.action,
            "changed_by": str(db_log.changed_by),
            "old_values": db_log.old_values,
            "new_values": db_log.new_values,
            "previous_hash": previous_hash,
        }


        db_log.row_hash = hashlib.sha256(
            json.dumps(payload, sort_keys=True, default=str).encode()
        ).hexdigest()

        print(db_log)

        self.db.add(db_log)
        self.db.flush()

        return db_log
    
    def get_last_hash(self, entity_type: str, entity_id: UUID) -> str | None:
        last = (
            self.db.query(AuditLog)
            .filter_by(entity_type=entity_type, entity_id=entity_id)
            .order_by(AuditLog.id.desc())
            .first()
        )
        return last.row_hash if last else None