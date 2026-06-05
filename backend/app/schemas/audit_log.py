from pydantic import BaseModel
from uuid import UUID
from typing import Any, Optional


class AuditLogCreate(BaseModel):
    entity_type: str
    entity_id: UUID
    action: str 
    changed_by: UUID
    old_values: Optional[dict[str, Any]] = None
    new_values: Optional[dict[str, Any]] = None