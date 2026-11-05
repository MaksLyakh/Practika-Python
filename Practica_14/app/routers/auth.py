from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.appointment import User
from app.schemas.appointment import UserCreate, UserResponse, TokenResponse
from app.security import hash_password, verify_password, create_token, current_user

router = APIRouter(tags=["Авторизация"])

@router.post("/auth/register", response_model=UserResponse, status_code=201, summary="Регистрация пользователя")
def register(data: UserCreate, db: Session = Depends(get_db)):
    if db.scalar(select(User).where(User.username == data.username)):
        raise HTTPException(409, "Имя пользователя занято")
    user = User(username=data.username, password_hash=hash_password(data.password), role="USER")
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@router.post("/auth/login", response_model=TokenResponse, summary="Получить JWT")
def login(data: UserCreate, db: Session = Depends(get_db)):
    user = db.scalar(select(User).where(User.username == data.username))
    if user is None or not verify_password(data.password, user.password_hash):
        raise HTTPException(401, "Неверные учётные данные")
    return {"access_token": create_token(user)}

@router.get("/profile", response_model=UserResponse, summary="Профиль пользователя")
def profile(user: User = Depends(current_user)):
    return user
