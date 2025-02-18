from fastapi import APIRouter, status, HTTPException
from ..dependencies import logger
from ..services.utils import user_dependency,db_dependency
from ..models.worker_model import Worker
from ..models.shipment_model import Shipment
from ..schemas.shipment_shema import ShipmentCreateAtBranch
from ..services.payment_service import is_shipment_paid
from ..services.shipment_service import create_tracking_number, add_shipment_status

router = APIRouter()

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

@router.post("/create_shipment", status_code=status.HTTP_201_CREATED)
def create_shipment_at_branch(shipment_data: ShipmentCreateAtBranch, db: db_dependency, user: user_dependency):
    verify_worker_role(user)
    if shipment_data.branch_from == shipment_data.branch_to:
        raise HTTPException(status_code=400, detail="Sender and receiver can't be at the same branch")
    if shipment_data.sender_id == shipment_data.receiver_id:
        raise HTTPException(status_code=400, detail="Sender and receiver can't be the same person")
    
    tracking_number = create_tracking_number()
    if db.query(Shipment).filter(Shipment.tracking_number == tracking_number).first():
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
    logger.info(f"Створено нову посилку у відділенні: {shipment_data.branch_from}")
    add_shipment_status(tracking_number, "awaiting shipment", db)
    return {"message": "Посилка створена", "tracking_number": tracking_number}

@router.put("/accept_shipment/{tracking_number}", status_code=status.HTTP_202_ACCEPTED)
def accept_shipment(tracking_number: str, db: db_dependency, user: user_dependency):
    verify_worker_role(user)
    shipment = get_shipment(tracking_number, db)
    worker = get_worker(user, db)
    shipment.location = worker.branch_id
    shipment.status = "awaiting shipment"
    add_shipment_status(tracking_number, "awaiting shipment", db)
    db.commit()
    logger.info(f"Посилка прийнята у відділення: {worker.branch_id}")
    return {"message": "Замовлення прийнято у відділення"}

@router.put("/accept_shipment_from_courier/{tracking_number}", status_code=status.HTTP_202_ACCEPTED)
def accept_shipment_from_courier(tracking_number: str, db: db_dependency, user: user_dependency):
    verify_worker_role(user)
    shipment = get_shipment(tracking_number, db)
    worker = get_worker(user, db)
    shipment.location = worker.branch_id
    shipment.status = "delivered"
    add_shipment_status(tracking_number, "delivered", db)
    db.commit()
    logger.info(f"Посилка прибула у відділення: {worker.branch_id}")
    return {"message": "Замовлення прийнято у відділення"}

@router.put("/pay_shipment/{tracking_number}", status_code=status.HTTP_202_ACCEPTED)
def pay_shipment(tracking_number: str, db: db_dependency, user: user_dependency):
    verify_worker_role(user)
    shipment = get_shipment(tracking_number, db)
    if shipment.payment_status == "paid":
        raise HTTPException(status_code=400, detail="Замовлення вже оплачено")
    is_shipment_paid(shipment.id, db)
    shipment.payment_status = "paid"
    db.commit()
    logger.info(f"Оплата посилки завершена: {tracking_number}")
    return {"message": "Оплата замовлення успішно завершена"}

@router.put("/pick_up_shipment/{tracking_number}", status_code=status.HTTP_200_OK)
def pick_up_shipment(tracking_number: str, db: db_dependency, user: user_dependency):
    verify_worker_role(user)
    shipment = get_shipment(tracking_number, db)
    if shipment.status != "delivered":
        raise HTTPException(status_code=400, detail="Замовлення не в стані delivered")
    shipment.status = "picked up"
    db.commit()
    logger.info(f"Посилка взята у відділення: {shipment.branch_to}")
    return {"message": "Посилка взята у відділення"}
