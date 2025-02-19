import uuid
from fastapi import status, HTTPException
from ..models.user_model import User
from ..dependencies import logger

def get_user_or_404(db, user_id):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        logger.warning(f"Користувач з ID {user_id} не знайдений")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user

def create_barcode_id():
    return str(uuid.uuid4().int)[:14] 