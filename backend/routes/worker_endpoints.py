from fastapi import APIRouter, status,HTTPException
from ..dependencies import logger
from ..models.payment_model import Payment
from ..schemas.payment_schema import PaymentCreate
from ..services.utils import db_dependency,user_dependency
from ..models.shipment_model import Shipment
from ..schemas.shipment_shema import ShipmentCreateAtBranch
from ..services.payment_service import is_shipment_paid
from ..services.shipment_service import create_tracking_number, existing_status, add_shipment_status


router = APIRouter(
    prefix="/worker_endpoints",
    tags=["Wocker Endpoints",]
)

@router.post("/create_shipment",status_code=status.HTTP_201_CREATED)
def create_shipment_at_branch(shipment_data: ShipmentCreateAtBranch, db: db_dependency, user: user_dependency):
  tracking_number = create_tracking_number()
  if not user:
    raise HTTPException(status_code=401, detail="Authentication required")
  if user.get('role') != "worker":
    raise HTTPException(status_code=403, detail="Only workers can create shipments at branch")
  if shipment_data.branch_from == shipment_data.branch_to:
    raise HTTPException(status_code=400, detail="Sender and receiver can't be at the same branch")
  if shipment_data.sender_id == shipment_data.receiver_id:
    raise HTTPException(status_code=400, detail="Sender and receiver can't be the same person")
  existing_shipment = db.query(Shipment).filter(Shipment.tracking_number == tracking_number).first()
  if existing_shipment:
    raise HTTPException(status_code=400, detail="Tracking number already exists")
  shipment = Shipment(
    tracking_number=tracking_number,
    sender_id=shipment_data.sender_id,
    receiver_id=shipment_data.receiver_id,
    branch_from=shipment_data.branch_from,
    branch_to=shipment_data.branch_to,
    weight=shipment_data.weight,
    length=shipment_data.length,
    width=shipment_data.width,
    location=shipment_data.branch_from,
    price=shipment_data.price,
    payment_status="unpaid",
    status="awaiting shipment"
  )
  db.add(shipment)
  db.commit()
  logger.info(f"Створення ново�� посилки в відділенні: {shipment_data.branch_from}")
  add_shipment_status(tracking_number, "awaiting shipment", db)
  return {"message": "Посилка створена", "tracking_number": tracking_number}