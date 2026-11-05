import hashlib
import hmac
import os
from datetime import datetime, timedelta, timezone
import jwt
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.config import settings
from app.database import get_db
from app.models.appointment import User

bearer = HTTPBearer(auto_error=False)

def hash_password(password: str) -> str:
    salt = os.urandom(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, 240000)
    return salt.hex() + ":" + digest.hex()

def verify_password(password: str, saved: str) -> bool:
    try:
        salt, digest = saved.split(":", 1)
        candidate = hashlib.pbkdf2_hmac("sha256", password.encode(), bytes.fromhex(salt), 240000)
        return hmac.compare_digest(candidate, bytes.fromhex(digest))
    except (ValueError, TypeError):
        return False

def create_token(user: User):
    payload = {"sub": str(user.id), "role": user.role, "exp": datetime.now(timezone.utc) + timedelta(hours=2)}
    return jwt.encode(payload, settings.jwt_secret, algorithm="HS256")

def current_user(credentials: HTTPAuthorizationCredentials | None = Depends(bearer), db: Session = Depends(get_db)):
    if credentials is None:
        raise HTTPException(401, "Требуется Bearer-токен", headers={"WWW-Authenticate": "Bearer"})
    try:
        payload = jwt.decode(credentials.credentials, settings.jwt_secret, algorithms=["HS256"])
        user = db.get(User, int(payload["sub"]))
    except (jwt.PyJWTError, ValueError, KeyError):
        raise HTTPException(401, "Недействительный токен")
    if user is None:
        raise HTTPException(401, "Пользователь не найден")
    return user

def require_admin(user: User = Depends(current_user)):
    if user.role != "ADMIN":
        raise HTTPException(403, "Требуется роль ADMIN")
    return user
