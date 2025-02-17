from pydantic import BaseModel

class ShipmentCreate(BaseModel):
  receiver_id:int
  branch_from:int
  branch_to:int
  weight: float
  length: float
  width: float
  price:float

class ShipmentUpdate(BaseModel):
  status:str