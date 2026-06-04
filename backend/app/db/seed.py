from uuid import uuid4, UUID
from .session import SessionLocal
from ..models.user import User, UserRole
from ..models.case import Case, CaseStatus, CasePriority
from ..models.tag import Tag


def seed_db():
    db = SessionLocal()

    if db.query(User).first():
        db.close()
        return

    admin = User(
        id=UUID("3fa85f64-5717-4562-b3fc-2c963f66afa6"),
        username="admin",
        email="admin@test.local",
        password_hash="not_real_hash",
        role=UserRole.ADMIN
    )
    investigator = User(
        id=uuid4(),
        username="investigator",
        email="investigator@test.local",
        password_hash="not_real_hash",
        role=UserRole.INVESTIGATOR
    )
    db.add_all([admin, investigator])

    malware_tag = Tag(
        id=uuid4(),
        name="malware",
        description="Cases involving malware",
        color="#FF0000"
    )
    windows_tag = Tag(
        id=uuid4(),
        name="windows",
        description="Cases involving Windows OS",
        color="#0078D7"
    )
    triage_tag = Tag(
        id=uuid4(),
        name="triage",
        description="Cases that need to be triaged",
        color="#FFA500"
    )
    db.add_all([malware_tag, windows_tag, triage_tag])

    case = Case(
        id=uuid4(),
        case_number="CASE-2026-0001",
        title="Test Forensic Case",
        description="Development seed data",
        status=CaseStatus.OPEN,
        priority=CasePriority.HIGH,
        created_by=investigator.id
    )
    case.tags.extend([malware_tag, windows_tag, triage_tag])
    db.add(case)

    db.commit()
    db.close()