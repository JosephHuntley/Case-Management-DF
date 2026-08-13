import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Reads from the environment (set in docker-compose.yml as "postgres" host).
# Falls back to localhost for when you run the backend directly on your machine.
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg://postgres:password@localhost:5432/casedf",
)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()