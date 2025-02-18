from fastapi import HTTPException

from ..models.worker_model import Worker
from ..models.shipment_model import Shipment



def get_shipment(tracking_number: str, db):
    shipment = db.query(Shipment).filter(Shipment.tracking_number == tracking_number).first()
    if not shipment:
        raise HTTPException(status_code=404, detail="Замовлення не знайдено")
    return shipment

def get_worker(user, db):
    worker = db.query(Worker).filter(Worker.user_id == user.get("id")).first()
    if not worker:
        raise HTTPException(status_code=403, detail="Worker not found")
    return worker

def verify_worker_role(user):
    if not user:
        raise HTTPException(status_code=401, detail="Authentication required")
    if user.get('role') != "worker":
        raise HTTPException(status_code=403, detail="Only workers can perform this action")