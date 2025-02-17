from fastapi import APIRouter
from typing import Annotated
from datetime import timedelta
from fastapi import APIRouter, Depends, status, BackgroundTasks, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from ..dependencies import logger
from ..models.user_model import User
from ..schemas.user_schemas import UserCreate,Token
from ..services.auth_service import *
from ..services.utils import db_dependency,user_dependency

import uuid



router=APIRouter(
  prefix="/auth",
  tags=["Auth",]
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register_user(user: UserCreate, db: db_dependency, background_tasks: BackgroundTasks):
    logger.info(f"Реєстрація нового користувача: {user.email}")
    
    if db.query(User).filter_by(email=user.email).first():
        logger.warning("Email вже зареєстрований")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='Email already registered')
    if db.query(User).filter_by(phone=user.phone).first():
        logger.warning("Номер телефону вже зареєстрований")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='Phone already registered')


    logger.info('Користувач ввів вірну позицію')
    token = str(uuid.uuid4())
    create_user = User(
        email=user.email,
        password_hash=hash_password(user.password),
        full_name=user.full_name,
        phone=user.phone,
        role=user.role
    )
    db.add(create_user)
    db.commit()
    logger.info(f"Користувача {user.email} зареєстровано успішно")
    return {"message": "Користувач був успішно зареєстрований"}



@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
                                 db: db_dependency):
    logger.info(f"Аутентифікація користувача: {form_data.username}")
    
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        logger.warning("Не вдалося автентифікувати користувача")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate user')
    
    token = create_access_token(
        user.email,
        user.id,
        user.role,
        timedelta(minutes=20)
    )
    
    logger.info(f"Користувач {user.email} успішно отримав токен")
    return {'access_token': token, 'token_type': 'bearer'}

