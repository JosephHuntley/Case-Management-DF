from sqlalchemy import create_engine, text

ADMIN_DB_URL = "postgresql+psycopg://postgres:password@localhost:5432/postgres"
TEST_DB_NAME = "case_db_test"

engine = create_engine(ADMIN_DB_URL, isolation_level="AUTOCOMMIT")

def create_test_db():
    with engine.connect() as conn:
        conn.execute(text(f"DROP DATABASE IF EXISTS {TEST_DB_NAME}"))
        conn.execute(text(f"CREATE DATABASE {TEST_DB_NAME}"))