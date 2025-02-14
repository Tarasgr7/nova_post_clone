from ..dependencies import SessionLocal,logger
from typing import Annotated
from fastapi import Depends,HTTPException,status
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from ..services.auth_service import get_current_user

def get_db():
  db= SessionLocal()
  try:
    yield db
  finally:
    db.close()

db_dependency=Annotated[Session,Depends(get_db)]


user_dependency=Annotated[dict,Depends(get_current_user)]
