from math import radians, sin, cos, sqrt, atan2
import uuid
from ..models.shipment_model import Shipment,ShipmentStatus
from fastapi import HTTPException
from ..dependencies import logger



def create_tracking_number():
    return str(uuid.uuid4().int)[:18] 

def existing_status(status):
    statuses = ["created","shipped","in_transit","delivered","cancelled","awaiting shipment"]
    if status in statuses:
        return True
    else:
        return False

def add_shipment_status(tracking_number,status,db):
    if existing_status(status) == False:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid status")
    shipment = db.query(Shipment).filter(Shipment.tracking_number == tracking_number).first()
    if not shipment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Замовлення із номером {tracking_number} не знайдено")
    shipment_status = ShipmentStatus(
        shipment_id=shipment.id,
        status=status
    )
    db.add(shipment_status)
    db.commit()



def calculate_distance(lat1, lon1, lat2, lon2):
    R = 6371  # Радіус Землі в км
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    
    a = sin(dlat / 2) ** 2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    
    return round(R * c,3)

def calculate_delivery_price(distance_km, weight, length, width):
    base_price = 50  # Базова вартість
    price_per_km = 0.1  # Вартість за 1 км
    weight_price = 10 * weight  # Додатковий тариф за вагу
    volume_coefficient = (length + width) / 100  # Врахування габаритів
    
    total_price = base_price + (distance_km * price_per_km) + weight_price + volume_coefficient
    return round(total_price, 2)







