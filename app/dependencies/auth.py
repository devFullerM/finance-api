from typing import Generator
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from app.core.security import decode_access_token
from app.models.user import User
import jwt


from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

oauth2_scheme = HTTPBearer()


def get_db() -> Generator:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    token = credentials.credentials
    try:
        payload = decode_access_token(token)
        user_id = int(payload.get("sub"))
    except (jwt.PyJWTError, ValueError):
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user