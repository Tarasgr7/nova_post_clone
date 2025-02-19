from fastapi import APIRouter, status, HTTPException
from ..dependencies import logger
from ..models.user_model import User
from ..models.shipment_model import Shipment, ShipmentStatus
from ..schemas.shipment_shema import ShipmentCreate, ShipmentUpdate,ShipmentCalculate
from ..services.utils import db_dependency, user_dependency,generate_barcode
from ..models.branch_model import Branch
from ..services.shipment_service import create_tracking_number, existing_status, add_shipment_status,calculate_distance,calculate_delivery_price

router = APIRouter()

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_shipment(shipment_data: ShipmentCreate, db: db_dependency, user: user_dependency):
    if not user:
        raise HTTPException(status_code=401, detail="Authentication required")
    receiver=db.query(User).filter(User.id== shipment_data.receiver_id).first()
    if not receiver:
        raise HTTPException(status_code=404, detail="Отримувач не знайдений")
    if shipment_data.receiver_id == user.get("id"):
        raise HTTPException(status_code=400, detail="You can't send your own shipment")
    
    branch_from = db.query(Branch).filter(Branch.id == shipment_data.branch_from).first()
    branch_to = db.query(Branch).filter(Branch.id == shipment_data.branch_to).first()
    
    if not branch_from or not branch_to:
        raise HTTPException(status_code=404, detail="Invalid branch IDs")

    distance = calculate_distance(branch_from.latitude, branch_from.longitude, branch_to.latitude, branch_to.longitude)
    price = calculate_delivery_price(distance, shipment_data.weight, shipment_data.length, shipment_data.width)
    
    
    tracking_number = create_tracking_number()
    barcode_path=generate_barcode(tracking_number,tracking_number,False)
    shipment = Shipment(
        tracking_number=tracking_number,
        sender_id=user.get("id"),
        receiver_id=shipment_data.receiver_id,
        branch_from=shipment_data.branch_from,
        branch_to=shipment_data.branch_to,
        weight=shipment_data.weight,
        length=shipment_data.length,
        width=shipment_data.width,
        price=price,
        barcode_path=barcode_path
    )
    
    logger.info(f"Створення нової посилки: {shipment_data.receiver_id}")
    db.add(shipment)
    db.commit()
    
    add_shipment_status(tracking_number, "created", db)
    return {"message": "Посилка створена", "tracking_number": tracking_number}


@router.post("/shipment/calculate_price", status_code=status.HTTP_200_OK)
async def calculate_price(data: ShipmentCalculate, db: db_dependency):
    branch_from = db.query(Branch).filter(Branch.id == data.branch_from_id).first()
    branch_to = db.query(Branch).filter(Branch.id == data.branch_to_id).first()
    
    if not branch_from or not branch_to:
        raise HTTPException(status_code=404, detail="One or both branches not found")
    
    distance = calculate_distance(branch_from.latitude, branch_from.longitude, branch_to.latitude, branch_to.longitude)
    price = calculate_delivery_price(distance, data.weight, data.length, data.width)
    
    return {"distance_km": distance, "price": price}


@router.get('/my-shipments', status_code=status.HTTP_200_OK)
async def get_user_shipments(db: db_dependency, user: user_dependency):
    if not user:
        raise HTTPException(status_code=401, detail="Authentication required")
    shipments = db.query(Shipment).filter((Shipment.sender_id == user.get("id")) | (Shipment.receiver_id == user.get("id"))).all()
    return shipments

@router.get('/{tracking_number}', status_code=status.HTTP_200_OK)
async def get_shipment(tracking_number: str, db: db_dependency, user: user_dependency):
    shipment = db.query(Shipment).filter(Shipment.tracking_number == tracking_number).first()
    if not shipment:
        raise HTTPException(status_code=404, detail="Замовлення не знайдено")
    return shipment

@router.put('/change_status/{tracking_number}', status_code=status.HTTP_200_OK)
async def change_status(tracking_number: str, shipment_update: ShipmentUpdate, db: db_dependency, user: user_dependency):
    if not user:
        raise HTTPException(status_code=401, detail="Authentication required")
    if not existing_status(shipment_update.status):
        raise HTTPException(status_code=400, detail="Invalid status")
    
    shipment = db.query(Shipment).filter(Shipment.tracking_number == tracking_number).first()
    if not shipment:
        raise HTTPException(status_code=404, detail="Замовлення не знайдено")
    if user.get("role") not in ['admin', 'courier']:
        raise HTTPException(status_code=403, detail="Тільки адміністратори та кур'єри можуть змінювати статус")
    
    shipment.status = shipment_update.status
    db.commit()
    add_shipment_status(tracking_number, shipment_update.status, db)
    
    logger.info(f"Статус посилки {tracking_number} змінено на {shipment_update.status}")
    return {"message": "Статус замовлення успішно змінено"}

@router.delete('/{tracking_number}', status_code=status.HTTP_200_OK)
async def delete_shipment(tracking_number: str, db: db_dependency, user: user_dependency):
    if not user:
        raise HTTPException(status_code=401, detail="Authentication required")
    shipment = db.query(Shipment).filter(Shipment.tracking_number == tracking_number).first()
    if not shipment:
        raise HTTPException(status_code=404, detail="Замовлення не знайдено")
    if user.get("id") != shipment.sender_id:
        raise HTTPException(status_code=403, detail="Тільки відправник може видалити замовлення")
    
    db.delete(shipment)
    db.commit()
    logger.info(f"Замовлення {tracking_number} видалено користувачем {user.get('id')}")
    
    return {"message": "Замовлення успішно видалено"}

@router.get('/{shipment_id}/statuses', status_code=status.HTTP_200_OK)
async def get_shipment_statuses(shipment_id: int, db: db_dependency, user: user_dependency):
    if not user:
        raise HTTPException(status_code=401, detail="Authentication required")
    shipment_statuses = db.query(ShipmentStatus).filter(ShipmentStatus.shipment_id == shipment_id).all()
    return shipment_statuses