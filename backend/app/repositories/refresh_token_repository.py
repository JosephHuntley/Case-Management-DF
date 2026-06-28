from datetime import datetime, timezone
from uuid import UUID
from app.models import RefreshToken

class RefreshTokenRepository:
    def __init__(self, db):
        self.db = db

    def create(self, user_id: UUID, token_hash: str, expires_at: datetime) -> RefreshToken:
        token = RefreshToken(user_id=user_id, token_hash=token_hash, expires_at=expires_at)
        self.db.add(token)
        self.db.flush()
        return token

    def get_by_hash(self, token_hash: str) -> RefreshToken | None:
        return self.db.query(RefreshToken).filter(RefreshToken.token_hash == token_hash).first()

    def revoke(self, token: RefreshToken) -> None:
        token.revoked = True
        self.db.flush()