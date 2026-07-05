from uuid import UUID, uuid4
from sqlalchemy.orm import Session
from passlib.context import CryptContext

from app.models import User
from app.schemas import UserCreate, UserOut, UserUpdate, UserRoleUpdate
from app.repositories import UserRepository
from app.services.audit_service import AuditService
from app.security import hash_password


class UserService:
    @staticmethod
    def create_user(db: Session, payload: UserCreate, current_user: User) -> User:
        user = User(
            id=uuid4(),
            password_hash=hash_password(payload.password),
            **payload.model_dump(exclude={"password"}),
            )
        
        user = UserRepository.create(db, user)

        audit_data = UserOut.model_validate(user).model_dump(mode="json")
        AuditService(db).log_create(
            entity_type="user",
            entity_id=user.id,
            user_id=current_user.id,
            new_values=audit_data
        )

        db.commit()
        db.refresh(user)
        return user

    @staticmethod
    def get_user_by_id(db: Session, user_id: UUID) -> User | None:
        return UserRepository.get_by_id(db, user_id)

    @staticmethod
    def get_all_users(db: Session) -> list[User]:
        return UserRepository.get_all(db)

    @staticmethod
    def update_user(db: Session, user_id: UUID, payload: UserUpdate, current_user: User) -> User | None:
        # TODO: require current_password confirmation for self-service changes
        user = UserRepository.get_by_id(db, user_id)
        if not user:
            return None

        old_data = UserOut.model_validate(user).model_dump(mode="json")
        update_data = payload.model_dump(exclude_unset=True)

        if "password" in update_data:
            raw_password = update_data.pop("password")
            update_data["password_hash"] = hash_password(raw_password)

        UserRepository.update(db=db, user=user, data=update_data)

        new_data = UserOut.model_validate(user).model_dump(mode="json")
        AuditService(db).log_update(
            entity_type="user",
            entity_id=user.id,
            user_id=current_user.id,
            old_values=old_data,
            new_values=new_data
        )

        db.commit()
        db.refresh(user)
        return user
    
    @staticmethod
    def update_user_role(db: Session, user_id: UUID, payload: UserRoleUpdate, current_user: User) -> User | None:
        user = UserRepository.get_by_id(db, user_id)
        if not user:
            return None

        old_data = UserOut.model_validate(user).model_dump(mode="json")
        update_data = payload.model_dump(exclude_unset=True)

        UserRepository.update(db=db, user=user, data=update_data)

        new_data = UserOut.model_validate(user).model_dump(mode="json")
        AuditService(db).log_update(
            entity_type="user",
            entity_id=user.id,
            user_id=current_user.id,
            old_values=old_data,
            new_values=new_data
        )

        db.commit()
        db.refresh(user)
        return user

    @staticmethod
    def delete_user(db: Session, user_id: UUID, current_user: User) -> User | None:
        user = UserRepository.get_by_id(db, user_id)
        if not user:
            return None

        UserRepository.soft_delete(db, user)

        AuditService(db).log_delete(
            entity_type="user",
            entity_id=user.id,
            user_id=current_user.id,
            old_values=UserOut.model_validate(user).model_dump(mode="json")
        )

        db.commit()
        db.refresh(user)
        return user