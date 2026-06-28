from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from app.db.session import get_db
from sqlalchemy.orm import Session
from app.models import User, UserRole
from app.core.config import settings
from uuid import UUID
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from jose import jwt
import secrets
import hashlib


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id_str: str = payload.get("sub")
        if user_id_str is None:
            raise credentials_exception
        user_id = UUID(user_id_str)
    except (JWTError, ValueError):
        raise credentials_exception

    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise credentials_exception
    return user

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def generate_refresh_token() -> str:
    return secrets.token_urlsafe(64)

def hash_token(token: str) -> str:
    return hashlib.sha256(token.encode()).hexdigest()

def require_role(*allowed_roles: UserRole):
    def role_checker(current_user: User = Depends(get_current_user)) -> User:
        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=403,
                detail="You do not have permission to perform this action"
            )
        return current_user
    return role_checker

def require_self_or_role(*allowed_roles: UserRole):
    def checker(user_id: str, current_user: User = Depends(get_current_user)) -> User:
        if str(current_user.id) == user_id or current_user.role in allowed_roles:
            return current_user
        raise HTTPException(
            status_code=403,
            detail="You do not have permission to perform this action"
        )
    return checker