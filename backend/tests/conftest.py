import pytest
from uuid import UUID
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from app.db.base import Base
from app.db.session import get_db
from app.main import app
from app.security import get_current_user, hash_password
from tests.setup_tests_db import create_test_db
from app.models import User, UserRole
from app.core.config import settings


TEST_DB_URL = "postgresql+psycopg://postgres:password@localhost:5432/case_db_test"
TEST_USER_ID = UUID("11111111-1111-1111-1111-111111111111")
TEST_AUDITOR_ID = UUID("11111111-1111-1111-1111-111111111112")
TEST_PASSWORD = "testpassword123"

engine = create_engine(TEST_DB_URL)
TestingSessionLocal = sessionmaker(bind=engine)


@pytest.fixture(scope="session", autouse=True)
def setup_db():
    create_test_db()
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture()
def db_session(setup_db):
    session = TestingSessionLocal()

    test_user = User(
        id=TEST_USER_ID,
        username="testuser",
        email="test@test.com",
        password_hash=hash_password(TEST_PASSWORD),
        role=UserRole.ADMIN,
        first_name="John",
        last_name="doe"
    )
    test_audit = User(
        id=TEST_AUDITOR_ID,
        username="testaudit",
        email="testaudit@test.com",
        password_hash=hash_password(TEST_PASSWORD),
        role=UserRole.AUDITOR,
        first_name="John",
        last_name="doe"
    )
    session.add_all([test_user, test_audit])
    session.commit()

    try:
        yield session
    finally:
        
        session.rollback()
        session.execute(text("""
            TRUNCATE TABLE
                audit_log,
                chain_of_custody,
                case_tags,
                case_notes,
                evidence_items,
                reports,
                cases,
                tags,
                users
            CASCADE
        """))
        session.commit()
        session.close()

@pytest.fixture(autouse=True)
def disable_rate_limiting():
    settings.RATE_LIMIT_ENABLED = True

@pytest.fixture()
def client_factory(db_session):
    def _make_client(user_id=TEST_USER_ID):
        def override_get_db():
            yield db_session

        def override_current_user():
            return db_session.get(User, user_id)

        app.dependency_overrides[get_db] = override_get_db
        app.dependency_overrides[get_current_user] = override_current_user
        return TestClient(app)

    yield _make_client
    app.dependency_overrides.clear()