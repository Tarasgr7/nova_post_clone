from ..models.shipment_model import Shipment
from ..models.courier_model import Courier
from ..models.route_model import Route,RouteShipment
from fastapi import status, HTTPException



def check_received_shipments(route,db):
  shipments = db.query(RouteShipment).filter(RouteShipment.route_id == route.id).all()
  shipment_list = [db.query(Shipment).filter(Shipment.id==shipment.shipment_id).first() for shipment in shipments]
  for shipment in shipment_list:
    if shipment.location != shipment.branch_to:
      raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Поточна локація посилки із номером : {shipment.tracking_number} має бути відповідною до пошти на яку відправлялось замовлення")

def get_courier(user, db):
    if user.get("role") != "courier":
        raise HTTPException(status_code=403, detail="Only couriers can access this data")
    courier = db.query(Courier).filter(Courier.user_id == user.get("id")).first()
    if not courier:
        raise HTTPException(status_code=404, detail="Courier not found")
    return courier

def get_active_route(courier, db):
    route = db.query(Route).filter(Route.courier_id == courier.id, Route.status != "completed").first()
    if not route:
        raise HTTPException(status_code=404, detail="No active routes found")
    return route