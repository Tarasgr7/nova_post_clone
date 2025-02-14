from sqlalchemy import Column, Integer, String, ForeignKey, DECIMAL, Boolean, TIMESTAMP, Interval
from sqlalchemy.orm import relationship
from datetime import datetime
from ..dependencies import Base
class Courier(Base):
    __tablename__ = "couriers"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    vehicle_id = Column(Integer, ForeignKey("vehicles.id"), nullable=True)
    active = Column(Boolean, default=True)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)

    user = relationship("User")
    vehicle = relationship("Vehicle")