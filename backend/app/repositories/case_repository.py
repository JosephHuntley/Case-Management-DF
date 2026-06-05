from uuid import UUID
from datetime import datetime, timezone

from sqlalchemy.orm import Session, joinedload

from app.models import Case, Tag


class CaseRepository:

    @staticmethod
    def create(db: Session, case: Case) -> Case:
        db.add(case)
        db.flush()
        return case

    @staticmethod
    def get_by_id(db: Session, case_id: UUID) -> Case | None:
        return (
            db.query(Case)
            .options(joinedload(Case.tags))
            .filter(
                Case.id == case_id
            )
            .first()
        )

    @staticmethod
    def get_all(db: Session) -> list[Case]:
        return (
            db.query(Case)
            .options(joinedload(Case.tags))
            .filter(Case.deleted_at.is_(None))
            .all()
        )

    @staticmethod
    def update(
        db: Session,
        case: Case,
        data: dict
    ) -> Case:

        for key, value in data.items():
            setattr(case, key, value)

        db.flush()
        return case

    @staticmethod
    def update_tags(
        db: Session,
        case: Case,
        tag_ids: list[UUID]
    ) -> Case:

        tags = (
            db.query(Tag)
            .filter(Tag.id.in_(tag_ids))
            .all()
        )

        case.tags = tags

        db.flush()
        return case

    @staticmethod
    def soft_delete(
        db: Session,
        case: Case
    ) -> Case:

        case.deleted_at = datetime.now(timezone.utc)

        db.flush()
        return case