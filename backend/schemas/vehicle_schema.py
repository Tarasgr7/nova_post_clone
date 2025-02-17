from pydantic import BaseModel

class VehicleCreate(BaseModel):
  license_plate: str
  model: str
  capacity: float
  status: str = "available"  # available, in transit, maintenance

class VehicleUpdate(BaseModel):
  status: str
