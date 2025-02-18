from fastapi import APIRouter, status, HTTPException
from ..dependencies import logger
from ..models.courier_model import Courier
from ..models.shipment_model import Shipment
from ..models.route_model import Route, RouteShipment
from ..services.utils import user_dependency, db_dependency
from ..services.shipment_service import add_shipment_status
from ..services.courier_service import check_received_shipments

router = APIRouter()

def get_courier(user, db):
    if user.get("role") != "courier":
        raise HTTPException(status_code=403, detail="Only couriers can access this data")
    courier = db.query(Courier).filter(Courier.user_id == user.get("id")).first()
    if not courier:
        raise HTTPException(status_code=404, detail="Courier not found")
    return courier

def get_active_route(courier, db, required_status=None):
    route = db.query(Route).filter(Route.courier_id == courier.id, Route.status != "completed").first()
    if not route:
        raise HTTPException(status_code=404, detail="No active routes found")
    if required_status and route.status != required_status:
        raise HTTPException(status_code=400, detail=f"Route must be in '{required_status}' status")
    return route

def update_shipments_status(route, status, db):
    shipments = db.query(RouteShipment).filter(RouteShipment.route_id == route.id).all()
    for shipment in shipments:
        shipment_obj = db.query(Shipment).filter(Shipment.id == shipment.shipment_id).first()
        if shipment_obj:
            shipment_obj.status = status
            add_shipment_status(shipment_obj.tracking_number, status, db)
    db.commit()

@router.get("/routes/my", status_code=status.HTTP_200_OK)
async def get_my_route(db: db_dependency, user: user_dependency):
    courier = get_courier(user, db)
    route = get_active_route(courier, db)
    shipments = db.query(RouteShipment).filter(RouteShipment.route_id == route.id).all()
    shipment_list = [db.query(Shipment).filter(Shipment.id == shipment.shipment_id).first() for shipment in shipments]
    return {
        "route_id": route.id,
        "branch_from": route.branch_from_id,
        "branch_to": route.branch_to_id,
        "status": route.status,
        "shipments": shipment_list
    }

@router.put("/routes/{route_id}/start", status_code=status.HTTP_200_OK)
async def start_route(route_id: int, db: db_dependency, user: user_dependency):
    courier = get_courier(user, db)
    route = get_active_route(courier, db, required_status="created")
    route.status = "in_transit"
    update_shipments_status(route, "in_transit", db)
    return {"message": "Route started, all shipments are now in transit"}

@router.put("/routes/{route_id}/complete", status_code=status.HTTP_200_OK)
async def complete_route(route_id: int, db: db_dependency, user: user_dependency):
    courier = get_courier(user, db)
    route = get_active_route(courier, db, required_status="in_transit")
    check_received_shipments(route, db)
    route.status = "completed"
    db.commit()
    return {"message": "Route completed, shipments updated"}
