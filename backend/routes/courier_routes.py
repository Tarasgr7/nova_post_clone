from fastapi import APIRouter,status,HTTPException
from ..dependencies import logger
from ..models.user_model import User
from ..models.courier_model import Courier
from ..schemas.courier_schema import CourierCreate,CourierUpdate
from ..services.utils import user_dependency,db_dependency,check_admin_role


router = APIRouter(
  prefix="/courier",
  tags=["Courier"],
)

@router.post("/",status_code=status.HTTP_201_CREATED)
async def create_courier(courier_data: CourierCreate, db:db_dependency,user:user_dependency):
  check_admin_role(user)
  existing_courier = db.query(Courier).filter(Courier.user_id == courier_data.user_id).first()
  if existing_courier:
    raise HTTPException(status_code=400, detail="Courier with the same phone number already exists")
  user_data=db.query(User).filter(User.id == courier_data.user_id).first()
  if not user_data:
    raise HTTPException(status_code=404, detail="User not found")
  if user_data.role!="user":
    raise HTTPException(status_code=400, detail="Юзер вже працює в компанії")
  courier=Courier(
    user_id=courier_data.user_id,
    vehicle=courier_data.vehicle,
    active=courier_data.active,
    locate=courier_data.locate
  )
  user_data.role = "courier"
  db.add(courier)
  db.commit()

  return courier

@router.get('/',status_code=status.HTTP_200_OK)
async def get_couriers(db: db_dependency, user: user_dependency):
  if not user:
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication required")
  check_admin_role(user)
  couriers = db.query(Courier).all()
  return couriers

@router.get('/{courier_id}',status_code=status.HTTP_200_OK)
async def get_courier(courier_id: int, db: db_dependency, user: user_dependency):
  if not user:
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication required")
  check_admin_role(user)
  courier = db.query(Courier).filter(Courier.id == courier_id).first()
  if not courier:
    raise HTTPException(status_code=404, detail="Courier not found")
  return courier

@router.put('/{courier_id}',status_code=status.HTTP_200_OK)
async def update_courier(courier_id: int, courier_data: CourierUpdate, db: db_dependency, user: user_dependency):
  if not user:
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication required")
  check_admin_role(user)
  courier = db.query(Courier).filter(Courier.id == courier_id).first()
  if not courier:
    raise HTTPException(status_code=404, detail="Courier not found")
  if courier_data.locate:
    courier.locate = courier_data.locate
  if courier_data.active is not None:
    courier.active = courier_data.active
  courier.vehicle_id = courier_data.vehicle_id
  db.commit()
  db.refresh(courier)
  return courier

@router.delete('/{courier_id}',status_code=status.HTTP_200_OK)
async def delete_courier(courier_id: int, db: db_dependency, user: user_dependency):
  if not user:
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication required")
  check_admin_role(user)
  courier = db.query(Courier).filter(Courier.id == courier_id).first()
  if not courier:
    raise HTTPException(status_code=404, detail="Courier not found")
  user_data = db.query(User).filter(User.id == courier.user_id).first()
  if not user_data:
    raise HTTPException(status_code=404, detail="User not found")
  user_data.role = "user"
  db.delete(courier)
  db.commit()
