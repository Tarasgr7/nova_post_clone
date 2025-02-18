from ..models.shipment_model import Shipment
from fastapi import status, HTTPException
from ..models.payment_model import Payment 
from ..dependencies import logger
def is_shipment_paid(shipment_id,db):
  shipment=db.query(Payment).filter(Payment.shipment_id == shipment_id).first()
  if shipment:
    logger.warning(f"Спроба повторної оплати для посилки ID: {shipment_id}")
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Оплата вже існує")


def is_sender_or_receiver(shipments_id,user_id,db):
  shipment=db.query(Shipment).filter(Shipment.id == shipments_id).first()
  if not shipment:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Замовлення не знайдено")
  if user_id != shipment.sender_id and user_id != shipment.receiver_id:
    raise HTTPException(status_code=403, detail="Тільки відправник та отримувач можуть редагувати замовлення")
  