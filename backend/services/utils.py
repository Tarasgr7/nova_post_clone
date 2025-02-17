from ..dependencies import SessionLocal,logger
from typing import Annotated
from fastapi import Depends,HTTPException,status
from sqlalchemy.orm import Session
from ..services.auth_service import get_current_user

def get_db():
  db= SessionLocal()
  try:
    yield db
  finally:
    db.close()

db_dependency=Annotated[Session,Depends(get_db)]


user_dependency=Annotated[dict,Depends(get_current_user)]


def check_admin_role(user):
    if user.get("role") != "admin":
        logger.warning(f"Невдала спроба доступу користувача: {user.get('id')} з роллю: {user.get('role')}")
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Ви не є адміністратором")
    logger.info(f"Користувач {user.get('id')} підтверджений як адміністратор.")
