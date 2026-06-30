from app.schemas import AuthLogCreate
from app.models import AuthEvent
from sqlalchemy.orm import Session

class AuthRepository:
    @staticmethod
    def create(db: Session, log: AuthLogCreate) -> AuthEvent:

        db_log = AuthEvent(
            username_attempted = log.username_attempted,
            ip_addr = log.ip_addr,
            user_agent = log.user_agent,
            event_type = log.event_type
        )

        db.add(db_log)
        db.commit()
        db.refresh(db_log)
        return db_log