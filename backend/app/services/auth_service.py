from datetime import datetime, timedelta, timezone
from app.schemas import AuthLogCreate 
from fastapi import HTTPException
from app.models import User, AuthEventType
from app.repositories import RefreshTokenRepository
from app.security import generate_refresh_token, hash_token, create_access_token
from app.core.config import settings
from app.repositories import AuthRepository

class AuthService:
    @staticmethod
    def issue_tokens(db, user: User) -> dict:
        access_token = create_access_token(data={"sub": str(user.id)})

        raw_refresh = generate_refresh_token()
        expires_at = datetime.now(timezone.utc) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
        RefreshTokenRepository(db).create(user.id, hash_token(raw_refresh), expires_at)
        db.commit()

        return {"access_token": access_token, "refresh_token": raw_refresh, "token_type": "bearer"}

    @staticmethod
    def refresh_access_token(db, raw_refresh_token: str) -> dict:
        repo = RefreshTokenRepository(db)
        token_hash = hash_token(raw_refresh_token)
        stored = repo.get_by_hash(token_hash)

        if stored is None:
            raise HTTPException(status_code=401, detail="Invalid refresh token")

        if stored.revoked:
            # Reuse of an already-rotated token — treat as a potential theft signal.
            raise HTTPException(status_code=401, detail="Refresh token has been revoked")

        if stored.expires_at < datetime.now(timezone.utc):
            raise HTTPException(status_code=401, detail="Refresh token expired")

        # Rotate: revoke the used token, issue a new pair
        repo.revoke(stored)
        user = db.query(User).filter(User.id == stored.user_id).first()
        if user is None:
            raise HTTPException(status_code=401, detail="User no longer exists")

        return AuthService.issue_tokens(db, user)
    
    def log_failed_login(db, username:str, ip_addr:str, agent:str, reason:AuthEventType):
        log = AuthLogCreate(
            username_attempted = username,
            ip_addr = ip_addr,
            user_agent = agent, 
            event_type = reason
        )

        AuthRepository.create(db,log)