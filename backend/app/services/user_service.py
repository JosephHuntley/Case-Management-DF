from uuid import UUID, uuid4
from app.models.user import User
from app.schemas.user import UserCreate
from sqlalchemy.orm import Session
from app.repositories.user_repository import UserRepository
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserService:


    @staticmethod
    def create_user(
        db: Session,
        payload: UserCreate
    ) -> User:
        
        user = User(
            id=uuid4(),
            username=payload.username,
            email=payload.email,
            password_hash=pwd_context.hash(payload.password)
        )

        user = UserRepository.create(db, user)
        db.commit()
        db.refresh(user)
        return user


    @staticmethod
    def get_user_by_id(db: Session, user_id: UUID) -> User | None:
        return UserRepository.get_by_id(db, user_id)
    
    @staticmethod
    def get_all_users(db: Session) -> list[User]:
        return UserRepository.get_all(db)
