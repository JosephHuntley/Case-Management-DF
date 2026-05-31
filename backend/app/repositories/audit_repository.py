from ..models.audit_log import AuditLog
from app.schemas.audit_log import AuditLogCreate
from app.db.session import SessionLocal


class AuditRepository:
    def __init__(self, db):
        self.db = db

    def create(self, log: AuditLogCreate):
        print("CREATING AUDIT LOG")
        db_log = AuditLog(
            entity_type=log.entity_type,
            entity_id=log.entity_id,
            action=log.action,
            changed_by=log.changed_by,
            old_values=log.old_values,
            new_values=log.new_values,
        )
    
        test = self.db.add(db_log)
        print(f"TEST: {test}")
        self.db.flush()
        return db_log