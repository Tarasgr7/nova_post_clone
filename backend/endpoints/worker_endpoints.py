from fastapi import APIRouter, status, HTTPException
from ..dependencies import logger
from ..services.utils import user_dependency,db_dependency
from ..models.worker_model import Worker
from ..models.user_model import User
from ..models.shipment_model import Shipment
from ..schemas.shipment_shema import ShipmentCreateAtBranch
from ..services.payment_service import is_shipment_paid
from ..services.shipment_service import create_tracking_number, add_shipment_status,add_shipment_status,calculate_distance,calculate_delivery_price
from ..services.worker_service import get_shipment,get_worker,verify_worker_role
from ..models.branch_model import Branch

router = APIRouter()

@router.post("/create_shipment", status_code=status.HTTP_201_CREATED)
def create_shipment_at_branch(shipment_data: ShipmentCreateAtBranch, db: db_dependency, user: user_dependency):
    verify_worker_role(user)
    worker=get_worker(user,db)
    if worker.branch_id != shipment_data.branch_from:
        raise HTTPException(status_code=400, detail="Працівник може оформлювати замовлення тільки з тої пошти на якій він працює")
    if shipment_data.branch_from == shipment_data.branch_to:
        raise HTTPException(status_code=400, detail="Sender and receiver can't be at the same branch")
    if shipment_data.sender_id == shipment_data.receiver_id:
        raise HTTPException(status_code=400, detail="Sender and receiver can't be the same person")
    
    tracking_number = create_tracking_number()
    if db.query(Shipment).filter(Shipment.tracking_number == tracking_number).first():
        raise HTTPException(status_code=400, detail="Tracking number already exists")
    branch_from = db.query(Branch).filter(Branch.id == shipment_data.branch_from).first()
    branch_to = db.query(Branch).filter(Branch.id == shipment_data.branch_to).first()
    
    if not branch_from or not branch_to:
        raise HTTPException(status_code=404, detail="Invalid branch IDs")

    distance = calculate_distance(branch_from.latitude, branch_from.longitude, branch_to.latitude, branch_to.longitude)
    price = calculate_delivery_price(distance, shipment_data.weight, shipment_data.length, shipment_data.width)
    
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
        price=price,
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
    
    if shipment.status == "awaiting shipment":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Посилка вже на пошті")
    worker = get_worker(user, db)
    if worker.branch_id!= shipment.branch_to:
        raise HTTPException(status_code=400, detail="Не можна прийняти посилку на вашу пошту, оскільки місце відправки вказане інше")
    shipment.location = worker.branch_id
    shipment.status = "awaiting shipment"
    add_shipment_status(tracking_number, "awaiting shipment", db)
    db.commit()
    logger.info(f"Посилка прийнята у відділення: {worker.branch_id}")
    return {"message": "Замовлення прийнято у відділення"}

@router.get('user_info_by_barcode/{barcode_id}',status_code=status.HTTP_200_OK)
async def get_user_info_by_barcode(barcode_id: str, db: db_dependency,user:user_dependency):
    verify_worker_role(user)
    user_data = db.query(User).filter(User.barcode_id == barcode_id).first()
    if not user_data:
        raise HTTPException(status_code=404, detail="Користувач не знайдений")
    shipment=db.query(Shipment).filter(Shipment.receiver_id == user_data.id).filter(Shipment.status != "picked up").all()
    return {
        "user_id": user_data.id,
        "name": user_data.full_name,
        "phone_number": user_data.phone,
        "shipments": [
            {"tracking_number": shipment.tracking_number, "status": shipment.status}
            for shipment in shipment
        ]
    }


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
