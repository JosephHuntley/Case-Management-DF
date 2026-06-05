from app.repositories import AuditRepository
from app.schemas import AuditLogCreate


class AuditService:
    def __init__(self, db):
        self.repo = AuditRepository(db)

    
    def log_create(self, *, entity_type, entity_id, user_id, new_values):
        return self.repo.create(
            AuditLogCreate(
                entity_type=entity_type,
                entity_id=entity_id,
                action="create",
                changed_by=user_id,
                old_values=None,
                new_values=new_values
            )
        )

    def log_update(self, *, entity_type, entity_id, user_id, old_values, new_values):
        return self.repo.create(
            AuditLogCreate(
                entity_type=entity_type,
                entity_id=entity_id,
                action="update",
                changed_by=user_id,
                old_values=old_values,
                new_values=new_values
            )
        )

    def log_delete(self, *, entity_type, entity_id, user_id, old_values):
        return self.repo.create(
            AuditLogCreate(
                entity_type=entity_type,
                entity_id=entity_id,
                action="delete",
                changed_by=user_id,
                old_values=old_values,
                new_values=None
            )
        )