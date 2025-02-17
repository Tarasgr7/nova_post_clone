import uuid
from ..models.shipment_model import Shipment,ShipmentStatus
from fastapi import HTTPException,status

def create_tracking_number():
    return str(uuid.uuid4().int)[:18] 

def existing_status(status):
    statuses = ["created","shipped","in_transit","delivered","cancelled"]
    if status in statuses:
        return True
    else:
        return False

def add_shipment_status(tracking_number,status,db):
    if existing_status(status) == False:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid status")
    shipment = db.query(Shipment).filter(Shipment.tracking_number == tracking_number).first()
    if not shipment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Замовлення не знайдено")
    shipment_status = ShipmentStatus(
        shipment_id=shipment.id,
        status=status
    )
    db.add(shipment_status)
    db.commit()




