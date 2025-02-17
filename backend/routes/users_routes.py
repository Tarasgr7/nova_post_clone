from fastapi import APIRouter, status,HTTPException
from ..services.utils import user_dependency,db_dependency
from ..models.user_model import User
from ..schemas.user_schemas import UserUpdateModel
from ..dependencies import logger


router = APIRouter(
  prefix="/users",
  tags=["Users"],
)


@router.get('/me',status_code=status.HTTP_200_OK)
async def get_user_info(db:db_dependency ,user: user_dependency):
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication required")
    user_info = db.query(User).filter(User.id == user.get('id')).first()
    if not user_info:
        raise HTTPException(status_code=404, detail="User not found")
    return user_info

@router.put('/me', status_code=status.HTTP_200_OK)
async def update_user_info(user_data: UserUpdateModel, db: db_dependency, user:user_dependency):
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication required")
    update_user=db.query(User).filter(User.id==user.get("id")).first()
    if not update_user:
        raise HTTPException(status_code=404, detail="User not found")
    if user_data.full_name:
        update_user.full_name=user_data.full_name
    if user_data.email:
        update_user.email=user_data.email
    if user_data.phone:
        update_user.phone=user_data.phone
    db.commit()


@router.get('/users', status_code=status.HTTP_200_OK)
async def read_all(db: db_dependency,user:user_dependency):
    logger.info("Отримання всіх користувачів з бази даних")
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication required")
    if user.get("role")!= "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='You are not admin')
    users = db.query(User).all()
    if users:
        logger.info(f"Знайдено {len(users)} користувачів")
    else:
        logger.warning("Користувачів не знайдено")
    
    return users


@router.get('/{user_id}', status_code=status.HTTP_200_OK)
async def read_all(user_id:int , db: db_dependency,user:user_dependency):
    logger.info("Отримання всіх користувачів з бази даних")
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication required")
    if user.get("role")!= "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='You are not admin')
    user_found = db.query(User).filter(User.id == user_id).first()
    if not user_found:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user_found
