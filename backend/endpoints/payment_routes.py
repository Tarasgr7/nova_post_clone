from fastapi import APIRouter, status, HTTPException
from ..dependencies import logger
from ..models.payment_model import Payment
from ..schemas.payment_schema import PaymentCreate
from ..services.utils import db_dependency,user_dependency
from ..models.shipment_model import Shipment
from ..services.payment_service import is_sender_or_receiver,is_shipment_paid
router = APIRouter(
    prefix="/payment",
    tags=["Payment"],
)

@router.post("/{shipment_id}", status_code=status.HTTP_201_CREATED)
def create_payment(shipment_id: int, payment_data: PaymentCreate, db: db_dependency,user: user_dependency):
    shipment = db.query(Shipment).filter(Shipment.id == shipment_id).first()
    if not shipment:
        logger.warning(f"Спроба оплати для неіснуючої посилки ID: {shipment_id}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Посилку не знайдено")
    is_shipment_paid(shipment_id,db)
    is_sender_or_receiver(shipment_id,user.get("id"),db)
    payment = Payment(
        shipment_id=shipment_id,
        amount=payment_data.amount,
        payment_method=payment_data.payment_method, 
        payment_status="paid",
    )
    shipment.payment_status = "paid"
    
    db.add(payment)
    db.commit()
    db.refresh(payment)
    logger.info(f"Оплата успішно створена для посилки ID: {shipment_id}")
    
    return payment

@router.get("/{shipment_id}", status_code=status.HTTP_200_OK)
def get_payment_status(shipment_id: int, db: db_dependency):
    payment = db.query(Payment).filter(Payment.shipment_id == shipment_id).first()
    if not payment:
        logger.warning(f"Запит статусу оплати для неіснуючої посилки ID: {shipment_id}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Оплату не знайдено")
    
    logger.info(f"Отримано статус оплати для посилки ID: {shipment_id}")
    return payment
