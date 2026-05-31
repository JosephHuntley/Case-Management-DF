from app.models.user import User
from uuid import UUID

def get_current_user():
    return User(
        id=UUID("3fa85f64-5717-4562-b3fc-2c963f66afa6"),
        username="admin",
        email="admin@test.local",
        password_hash="not_real_hash",
        role="admin"
    )