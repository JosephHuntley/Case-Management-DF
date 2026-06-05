from http.client import HTTPException
from uuid import UUID, uuid4

from sqlalchemy.orm import Session

from app.repositories import TagRepository
from app.models import User, Tag
from app.schemas import TagCreate, TagOut
from app.services.audit_service import AuditService

class TagService:
    @staticmethod
    def create_tag(db: Session, payload: TagCreate, current_user: User) -> Tag:
        tag = Tag(
            id=str(uuid4()),
            name=payload.name,
            description=payload.description,
            color=payload.color
        )

        TagRepository.create(db, tag)

        audit_data = TagOut.model_validate(tag).model_dump(mode="json")

        audit_service = AuditService(db)
        audit_service.log_create(
            entity_type="tag",
            entity_id=tag.id,
            user_id=current_user.id,
            new_values=audit_data
        )

        db.commit()
        db.refresh(tag)
        return tag
    
    @staticmethod
    def get_tag(db: Session, tag_id: str) -> Tag | None:
        return TagRepository.get_by_id(db, tag_id)
    
    @staticmethod
    def get_tags(db: Session) -> list[Tag]:
        return TagRepository.get_all(db)
    
    @staticmethod
    def update_tag(
        db: Session,
        tag_id: UUID,
        payload: TagCreate,
        current_user: User
    ) -> Tag:

        tag = TagRepository.get_by_id(db, tag_id)

        if not tag:
            raise HTTPException(status_code=404, detail="Tag not found")

        old_data = TagOut.model_validate(tag).model_dump(mode="json")

        updates = payload.model_dump(exclude_unset=True)

        tag = TagRepository.update(db, tag, updates)


        new_data = TagOut.model_validate(tag).model_dump(mode="json")

        audit_service = AuditService(db)
        audit_service.log_update(
            entity_type="tag",
            entity_id=tag.id,
            user_id=current_user.id,
            old_values=old_data,
            new_values=new_data
        )
        db.commit()
        db.refresh(tag)

        return tag
    
    @staticmethod
    def delete_tag(db: Session, tag_id: str, current_user: User):
        tag = TagRepository.get_by_id(db, tag_id)

        if not tag:
            raise HTTPException(status_code=404, detail="Tag not found")

        TagRepository.delete(db, tag)

        audit_service = AuditService(db)
        audit_service.log_delete(
            entity_type="tag",
            entity_id=tag.id,
            user_id=current_user.id,
            old_values=TagOut.model_validate(tag).model_dump(mode="json")
        )
        db.commit()
        return True

    
    