from fastapi import APIRouter, status, HTTPException
from ..dependencies import logger
from ..models.courier_model import Courier
from ..models.shipment_model import Shipment
from ..models.route_model import Route, RouteShipment
from ..services.utils import user_dependency, db_dependency
from ..services.shipment_service import add_shipment_status
from ..services.courier_service import check_received_shipments,get_courier,get_active_route

router = APIRouter()



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
    route = get_active_route(courier, db)
    if route.status != "created":
        raise HTTPException(status_code=400, detail="Route must be in 'created' status to start")
    
    route.status = "in_transit"
    shipments = db.query(RouteShipment).filter(RouteShipment.route_id == route.id).all()
    for shipment in shipments:
        shipment_obj = db.query(Shipment).filter(Shipment.id == shipment.shipment_id).first()
        if shipment_obj:
            shipment_obj.status = "in_transit"
            add_shipment_status(shipment_obj.tracking_number, shipment_obj.status, db)
    db.commit()
    return {"message": "Route started, all shipments are now in transit"}

@router.put("/routes/{route_id}/complete", status_code=status.HTTP_200_OK)
async def complete_route(route_id: int, db: db_dependency, user: user_dependency):
    courier = get_courier(user, db)
    route = get_active_route(courier, db)
    if route.status != "in_transit":
        raise HTTPException(status_code=400, detail="Route must be in 'in_transit' status to complete")
    
    check_received_shipments(route, db)
    route.status = "completed"
    db.commit()
    return {"message": "Route completed, shipments updated"}
