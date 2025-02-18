from pydantic import BaseModel
from typing import Optional

class RouteCreate(BaseModel):
  branch_from_id:int
  branch_to_id: int
  courier_id: Optional[int] = None
  





class RouteShipmentCreate(BaseModel):
  route_id: int
  shipment_id: int