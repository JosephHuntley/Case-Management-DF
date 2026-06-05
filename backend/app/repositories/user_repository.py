from datetime import datetime, timezone
from uuid import UUID

from sqlalchemy.orm import Session

from app.models import User

class UserRepository:

    @staticmethod
    def create(db: Session, user: User) -> User:
        db.add(user)
        db.flush()
        return user
    
    @staticmethod
    def get_by_id(db: Session, user_id: UUID) -> User | None:
        return db.query(User).filter(User.id == user_id).first()
    
    @staticmethod
    def get_all(db: Session) -> list[User]:
        return db.query(User).filter(User.is_active == True).all()
    
    @staticmethod
    def update(db: Session, user: User, data: dict) -> User:
        for key, value in data.items():
            setattr(user, key, value)
        
        db.flush()
        return user
    
    @staticmethod
    def soft_delete(db: Session, user: User) -> User | None:
        user.is_active = False
        user.deleted_at = datetime.now(timezone.utc)
        db.flush()
        return user