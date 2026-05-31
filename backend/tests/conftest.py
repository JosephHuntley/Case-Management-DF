from uuid import UUID

from app.models.user import User
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.db.base import Base
from app.db.session import get_db
from app.main import app

from tests.setup_tests_db import create_test_db
from app.security import get_current_user

TEST_DB_URL = "postgresql+psycopg://postgres:password@localhost:5432/case_db_test"

engine = create_engine(TEST_DB_URL)
TestingSessionLocal = sessionmaker(bind=engine)


@pytest.fixture(scope="session", autouse=True)
def setup_db():
    create_test_db()
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


from uuid import UUID
from app.models.user import User

@pytest.fixture()
def db_session():
    session = TestingSessionLocal()

    test_user = session.query(User).filter(
        User.id == UUID("11111111-1111-1111-1111-111111111111")
    ).first()

    if not test_user:
        test_user = User(
            id=UUID("11111111-1111-1111-1111-111111111111"),
            username="testuser",
            email="test@test.com",
            password_hash="hash",
            role="investigator"
        )

        session.add(test_user)
        session.commit()

    try:
        yield session
    finally:
        session.rollback()
        session.close()



@pytest.fixture()
def client(db_session):
    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    from fastapi.testclient import TestClient
    with TestClient(app) as c:
        yield c

def override_current_user():
    return User(
        id=UUID("11111111-1111-1111-1111-111111111111"),
        username="testuser123",
        email="test@test123.com",
        password_hash="hash",
        role="investigator"
    )

app.dependency_overrides[get_current_user] = override_current_user