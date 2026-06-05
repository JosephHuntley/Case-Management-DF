from uuid import UUID

from app.repositories import AuditRepository
from app.schemas import AuditLogCreate
from app.models import AuditLog


def test_audit_repository_only(db_session):
    repo = AuditRepository(db_session)

    log1 = AuditLogCreate(
        entity_type="case",
        entity_id="11111111-1111-1111-1111-111111111111",
        action="create",
        changed_by="11111111-1111-1111-1111-111111111111",
        old_values=None,
        new_values={"a": 1}
    )

    repo.create(log1)

    log2 = AuditLogCreate(
        entity_type="case",
        entity_id="11111111-1111-1111-1111-111111111111",
        action="update",
        changed_by="11111111-1111-1111-1111-111111111111",
        old_values={"a": 1},
        new_values={"a": 2}
    )

    repo.create(log2)
    audits = db_session.query(AuditLog).all()

    assert len(audits) == 2
    assert audits[0].action == "create"
    assert audits[0].entity_type == "case"
    assert audits[0].previous_hash == None
    assert audits[0].row_hash is not None
    assert audits[1].previous_hash == audits[0].row_hash
    assert audits[1].old_values == {"a": 1}
    assert audits[1].new_values == {"a": 2}
    assert audits[1].changed_by == UUID("11111111-1111-1111-1111-111111111111")
    assert audits[1].new_values == {"a": 2}