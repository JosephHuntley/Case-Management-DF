from uuid import UUID, uuid4

from sqlalchemy.orm import Session

from app.models import User, Case
from app.repositories import CaseRepository
from app.schemas import CaseCreate, CaseOut, CaseUpdate
from app.services.audit_service import AuditService



class CaseService:

    @staticmethod
    def create_case(
        db: Session,
        payload: CaseCreate,
        current_user: User
    ) -> Case:
        
        case = Case(
            id=uuid4(),
            case_number=f"CASE-{str(uuid4())[:8]}",
            title=payload.title,
            description=payload.description,
            status=payload.status,
            priority=payload.priority,
            created_by=payload.created_by
        )
        
        CaseRepository.create(db, case)

        audit_data = CaseOut.model_validate(case).model_dump(mode="json")

        audit_service = AuditService(db)
        audit_service.log_create(
            entity_type="case",
            entity_id=case.id,
            user_id=current_user.id, 
            new_values=audit_data
            )

        db.commit()
        db.refresh(case)



        return case

    @staticmethod
    def get_case(
        db: Session,
        case_id: UUID
    ) -> Case | None:

        return CaseRepository.get_by_id(db, case_id)

    @staticmethod
    def get_cases(
        db: Session
    ) -> list[Case]:

        return CaseRepository.get_all(db)

    @staticmethod
    def update_case(
        db: Session,
        case_id: UUID,
        payload: CaseUpdate,
        current_user: User
    ) -> Case | None:

        case = CaseRepository.get_by_id(db, case_id)
        old_data = CaseOut.model_validate(case).model_dump(mode="json")

        if not case:
            return None

        update_data = payload.model_dump(exclude_unset=True)

        tag_ids = update_data.pop("tag_ids", None)

        CaseRepository.update(
            db=db,
            case=case,
            data=update_data
        )

        if tag_ids is not None:
            CaseRepository.update_tags(
                db=db,
                case=case,
                tag_ids=tag_ids
            )

        new_data = CaseOut.model_validate(case).model_dump(mode="json")
        

        audit_service = AuditService(db)
        audit_service.log_update(
            entity_type="case",
            entity_id=case.id,
            user_id=current_user.id,
            old_values=old_data,
            new_values=new_data
            )

        db.commit()
        db.refresh(case)

        return case

    @staticmethod
    def delete_case(
        db: Session,
        case_id: UUID,
        current_user: User
    ) -> bool:

        case = CaseRepository.get_by_id(db, case_id)

        audit_data = CaseOut.model_validate(case).model_dump(mode="json") # Placed here to capture data before marked for deletion.

        if not case:
            return False

        CaseRepository.soft_delete(
            db=db,
            case=case
        )
        
        audit_service = AuditService(db)
        audit_service.log_delete(
            entity_type="case",
            entity_id=case.id,
            user_id=current_user.id,
            old_values=audit_data,
            )

        db.commit()

        return True