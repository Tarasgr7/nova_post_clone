from fastapi import APIRouter,status,HTTPException
from ..dependencies import logger
from ..models.courier_model import Courier
from ..models.vehicle_model import Vehicle
from ..schemas.vehicle_schema import VehicleCreate,VehicleUpdate
from ..services.utils import user_dependency,db_dependency


router = APIRouter(
  prefix="/vehicle",
  tags=["Vehicle"],
)

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_vehicle(vehicle: VehicleCreate, db:  db_dependency, user:  user_dependency):
  if user.get('role')!="admin":
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only admin users can create vehicles")
  existing_vehicle = db.query(Vehicle).filter(Vehicle.license_plate == vehicle.license_plate).first()
  if existing_vehicle:
    raise HTTPException(status_code=400, detail="Vehicle with the same license plate already exists")
  new_vehicle = Vehicle(**vehicle.dict())
  db.add(new_vehicle)
  db.commit()
  return new_vehicle

@router.get("/", status_code=status.HTTP_200_OK)
async def get_vehicles(db: db_dependency,user:user_dependency):
  if user.get('role')!="admin":
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only admin users can view vehicles")
  return db.query(Vehicle).all()

@router.put("/{license_plate}", status_code=status.HTTP_200_OK)
async def update_vehicle(license_plate: str, vehicle_update: VehicleUpdate, db: db_dependency, user: user_dependency):
  if user.get('role')!="admin":
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only admin users can update vehicles")
  vehicle = db.query(Vehicle).filter(Vehicle.license_plate == license_plate).first()
  if not vehicle:
    raise HTTPException(status_code=404, detail="Vehicle not found")
  for key, value in vehicle_update.dict().items():
    setattr(vehicle, key, value)
    db.commit()
    db.refresh(vehicle)
    return vehicle

@router.delete("/{license_plate}", status_code=status.HTTP_200_OK)
async def delete_vehicle(license_plate: str, db: db_dependency, user: user_dependency):
  if user.get('role')!="admin":
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only admin users can delete vehicles")
  vehicle = db.query(Vehicle).filter(Vehicle.license_plate == license_plate).first()
  if not vehicle:
    raise HTTPException(status_code=404, detail="Vehicle not found")
  db.delete(vehicle)
  db.commit()
