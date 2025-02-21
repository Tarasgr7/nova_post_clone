from ..dependencies import SessionLocal,logger
from typing import Annotated
from fastapi import Depends,HTTPException,status
from sqlalchemy.orm import Session
from ..services.auth_service import get_current_user
import barcode
from barcode.writer import ImageWriter
import os

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


def generate_barcode(data: str, filename: str,user:bool):
    if user ==True:
      barcode_path = f"backend/static/barcodes/users/{filename}.png"
      code128 = barcode.get_barcode_class('code128')
      barcode_instance = code128(data, writer=ImageWriter())
      barcode_instance.save(barcode_path[:-4])
    else:
      barcode_path = f"backend/static/barcodes/shipments/{filename}.png"
      code128 = barcode.get_barcode_class('code128')
      barcode_instance = code128(data, writer=ImageWriter())
      barcode_instance.save(barcode_path[:-4])
    return barcode_path  # Повертаємо шлях до зображення

