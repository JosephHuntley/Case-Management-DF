import pytest
from uuid import UUID
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from app.db.base import Base
from app.db.session import get_db
from app.main import app
from app.models.user import User, UserRole
from app.security import get_current_user
from tests.setup_tests_db import create_test_db

TEST_DB_URL = "postgresql+psycopg://postgres:password@localhost:5432/case_db_test"
TEST_USER_ID = UUID("11111111-1111-1111-1111-111111111111")

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

    # Ensure test user exists
    test_user = session.get(User, TEST_USER_ID)
    if not test_user:
        test_user = User(
            id=TEST_USER_ID,
            username="testuser",
            email="test@test.com",
            password_hash="hash",
            role=UserRole.INVESTIGATOR
        )
        session.add(test_user)
        session.commit()

    try:
        yield session
    finally:
        session.execute(text("""
            TRUNCATE TABLE
                audit_log,
                chain_of_custody,
                case_tags,
                case_notes,
                evidence_items,
                reports,
                cases,
                tags
            CASCADE
        """))
        session.commit()
        session.close()


@pytest.fixture()
def client(db_session):
    def override_get_db():
        yield db_session

    def override_current_user():
        return db_session.get(User, TEST_USER_ID)

    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_current_user] = override_current_user

    with TestClient(app) as c:
        yield c

    app.dependency_overrides.clear()