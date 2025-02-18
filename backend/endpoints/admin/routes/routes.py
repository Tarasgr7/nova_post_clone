from fastapi import APIRouter, status,HTTPException
from ....models.route_model import Route,RouteShipment
from ....models.shipment_model import Shipment
from ....schemas.route_schemas import RouteCreate,RouteShipmentCreate
from ....services.utils import db_dependency, user_dependency, check_admin_role





router = APIRouter()


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_route(route_data: RouteCreate, db: db_dependency, user: user_dependency):
  check_admin_role(user)
  route = Route(**route_data.dict())
  db.add(route)
  db.commit()
  db.refresh(route)
  return route


@router.get("/", status_code=status.HTTP_200_OK)
def get_routes(db: db_dependency, user: user_dependency):
  check_admin_role(user)
  routes = db.query(Route).all()
  return routes


@router.get("/{route_id}", status_code=status.HTTP_200_OK)
def get_route_by_id(route_id: int, db: db_dependency, user: user_dependency):
  check_admin_role(user)
  route = db.query(Route).filter(Route.id == route_id).first()
  if not route:
    raise HTTPException(status_code=404, detail="Маршрут не знайдено")
  return route


@router.delete("/{route_id}", status_code=status.HTTP_200_OK)
def delete_route(route_id: int, db: db_dependency, user: user_dependency):
  check_admin_role(user)
  route = db.query(Route).filter(Route.id == route_id).first()
  if not route:
    raise HTTPException(status_code=404, detail="Маршрут не знайдено")
  db.delete(route)
  db.commit()
  return {"message": "Маршрут успішно видалено"}


@router.post("/route/shipment", status_code=status.HTTP_201_CREATED)
async def create_route_shipment( shipment_data: RouteShipmentCreate, db: db_dependency, user: user_dependency):#+
    check_admin_role(user)#+
    route = db.query(Route).filter(Route.id == shipment_data.route_id).first()#+
    shipment = db.query(Shipment).filter(Shipment.id == shipment_data.shipment_id).first()#+
    if not route:#+
        raise HTTPException(status_code=404, detail="Маршрут не знайдено")#+
    route_shipment = RouteShipment(route_id=shipment_data.route_id, shipment_id=shipment_data.shipment_id)#+
    db.add(route_shipment)#+
    db.commit()#+
    db.refresh(route_shipment)#+
    return route_shipment#+

@router.get("/route/{route_id}/shipment", status_code=status.HTTP_200_OK)
def get_route_shipments(route_id: int, db: db_dependency, user: user_dependency):
    check_admin_role(user)
    route_shipments = db.query(RouteShipment).filter(RouteShipment.route_id == route_id).all()
    return route_shipments

@router.put("/route/{route_id}/courier",status_code=status.HTTP_200_OK)
def update_route_courier(route_id: int, courier_id: int, db: db_dependency, user: user_dependency):
    check_admin_role(user)
    route = db.query(Route).filter(Route.id == route_id).first()
    if not route:
        raise HTTPException(status_code=404, detail="Маршрут не знайдено")
    route.courier_id = courier_id
    db.commit()
    db.refresh(route)
    return route

@router.put("/route/{route_id}/status", status_code=status.HTTP_200_OK)
def update_route_status(route_id: int, status: str, db: db_dependency, user: user_dependency):
    check_admin_role(user)
    route = db.query(Route).filter(Route.id == route_id).first()
    if not route:
        raise HTTPException(status_code=404, detail="Маршрут не знайдено")
    route.status = status
    db.commit()
    db.refresh(route)
    return route

@router.delete("/route/{route_id}/shipment/{shipment_id}", status_code=status.HTTP_200_OK)
def delete_route_shipment(route_id: int, shipment_id: int, db: db_dependency, user: user_dependency):
    check_admin_role(user)
    route_shipment = db.query(RouteShipment).filter(RouteShipment.route_id == route_id, RouteShipment.shipment_id == shipment_id).first()
    if not route_shipment:
        raise HTTPException(status_code=404, detail="Маршрут-відправка не знайдена")
    db.delete(route_shipment)
    db.commit()
    return {"message": "Маршрут-відправка успішно видалена"}
