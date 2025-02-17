from fastapi import APIRouter, status, HTTPException
from ..services.utils import user_dependency, db_dependency,check_admin_role
from ..services.users_service import get_user_or_404
from ..models.user_model import User
from ..schemas.user_schemas import UserUpdateModel
from ..dependencies import logger

router = APIRouter(prefix="/users", tags=["Users"])



@router.get("/me", status_code=status.HTTP_200_OK)
async def get_user_info(db: db_dependency, user: user_dependency):
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication required")
    return get_user_or_404(db, user.get("id"))


@router.put("/me", status_code=status.HTTP_200_OK)
async def update_user_info(user_data: UserUpdateModel, db: db_dependency, user: user_dependency):
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication required")
    
    update_user = get_user_or_404(db, user.get("id"))
    for key, value in user_data.dict(exclude_unset=True).items():
        setattr(update_user, key, value)
    
    db.commit()
    db.refresh(update_user)
    logger.info(f"Оновлено дані користувача ID {update_user.id}")
    return update_user


@router.get("/", status_code=status.HTTP_200_OK)
async def read_all_users(db: db_dependency, user: user_dependency):
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication required")
    check_admin_role(user)
    
    users = db.query(User).all()
    logger.info(f"Отримано {len(users)} користувачів")
    return users


@router.get("/{user_id}", status_code=status.HTTP_200_OK)
async def read_user(user_id: int, db: db_dependency, user: user_dependency):
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication required")
    check_admin_role(user)
    
    return get_user_or_404(db, user_id)
