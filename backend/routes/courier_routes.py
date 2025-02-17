from fastapi import APIRouter,status,HTTPException
from ..dependencies import logger
from ..models.courier_model import Courier
from ..models.vehicle_model import Vehicle
from ..schemas.courier_schema import CourierCreate,CourierUpdate
from ..services.utils import user_dependency,db_dependency


router = APIRouter(
  prefix="/courier",
  tags=["Courier"],
)

@router.post("/",status_code=status.HTTP_201_CREATED)
async def create_courier(courier: CourierCreate, db:db_dependency):
  existing_courier = db.query(Courier).filter(Courier.user_id == courier.user_id).first()
  if existing_courier:
    raise HTTPException(status_code=400, detail="Courier with the same phone number already exists")
  create_courier=Courier(
    user_id=courier.user_id,
    vehicle_id=courier.vehicle_id,
    active=courier.active,
    locate=courier.locate
  )
  db.add(create_courier)
  db.commit()
  return create_courier

@router.get('/',status_code=status.HTTP_200_OK)
async def get_couriers(db: db_dependency, user: user_dependency):
  if not user:
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication required")
  couriers = db.query(Courier).all()
  return couriers
