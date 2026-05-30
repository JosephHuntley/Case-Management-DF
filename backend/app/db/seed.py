from uuid import uuid4
from .session import SessionLocal
from ..models.user import User
from ..models.case import Case

def seed_db():
    db = SessionLocal()

    # Don't reseed if data already exists
    if db.query(User).first():
        db.close()
        return

    user = User(
        id=uuid4(),
        username="admin",
        email="admin@test.local",
        password_hash="not_real_hash",
        role="admin"
    )

    db.add(user)

    user = User(
        id=uuid4(),
        username="investigator",
        email="investigator.test@local.com",
        password_hash="not_real_hash",
        role="investigator"
    )

    db.add(user)
    db.flush() 

    case = Case(
        id=uuid4(),
        case_number="CASE-2026-0001",
        title="Test Forensic Case",
        description="Development seed data",
        status="open",
        priority="high",
        created_by=user.id
    )

    db.add(case)
    db.commit()
    db.close()