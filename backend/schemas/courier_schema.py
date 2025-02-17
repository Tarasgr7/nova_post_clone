from pydantic import BaseModel
from typing import Optional

class CourierCreate(BaseModel):
  user_id:int
  vehicle_id:Optional[int] = None
  active:bool = True
  locate: str = ""  # lat, lng, address


class CourierUpdate(BaseModel):
  locate: Optional[str] = None
  vehicle_id: Optional[int] = None  # None means no change
  active: Optional[bool] = None


