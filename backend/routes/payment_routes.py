from fastapi import APIRouter,status,HTTPException
from ..dependencies import logger
from ..models.payment_model import Payment
from ..schemas.payment_schema import PaymentCreate
from ..services.utils import db_dependency,user_dependency
from ..models.shipment_model import Shipment


router = APIRouter(
  prefix="/payment",
  tags=["Payment"],
)

@router.post("/{shipment_id}",)
def create_payment(shipment_id: str, payment_data: PaymentCreate, db: db_dependency):
    shipment = db.query(Shipment).filter(Shipment.id == shipment_id).first()
    if not shipment:
        raise HTTPException(status_code=404, detail="Shipment not found")

    existing_payment = db.query(Payment).filter(Payment.shipment_id == shipment_id).first()
    if existing_payment:
        raise HTTPException(status_code=400, detail="Payment already exists for this shipment")

    payment = Payment(
        shipment_id=shipment_id,
        amount=payment_data.amount,
        payment_method=payment_data.payment_method, 
        payment_status="paid",  # Симулюємо успішну оплату
    )
    shipment.payment_status= "paid"

    db.add(payment)
    db.commit()
    db.refresh(payment)

    return payment


@router.get("/{shipment_id}")
def get_payment_status(shipment_id: str, db: db_dependency):
    payment = db.query(Payment).filter(Payment.shipment_id == shipment_id).first()
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    return payment
