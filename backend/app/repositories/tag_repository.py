from uuid import uuid4
from datetime import datetime
from app.models.tag import Tag
from sqlalchemy.orm import Session

class TagRepository:

    @staticmethod
    def create(db: Session, tag: Tag) -> Tag:
        db.add(tag)
        db.flush()
        return tag

    @staticmethod
    def get_by_id(db: Session, tag_id: str) -> Tag | None:
        return db.query(Tag).filter(Tag.id == tag_id).first()

    @staticmethod
    def get_all(db: Session) -> list[Tag]:
        return db.query(Tag).all()

    @staticmethod
    def update(db: Session, tag: Tag, data: dict) -> Tag:
        for key, value in data.items():
            setattr(tag, key, value)

        db.flush()
        return tag

    @staticmethod
    def delete(db: Session, tag: Tag) -> None:
        db.delete(tag)
        db.flush()