from sqlalchemy import Column, Integer, String, ForeignKey, DECIMAL, Boolean, TIMESTAMP, Interval
from sqlalchemy.orm import relationship
from datetime import datetime
from ..dependencies import Base

class Vehicle(Base):
    __tablename__ = "vehicles"

    id = Column(Integer, primary_key=True, index=True)
    license_plate = Column(String, unique=True, nullable=False)
    model = Column(String)
    capacity = Column(DECIMAL(10,2))
    status = Column(String, nullable=False, default="available")  # available, in transit, maintenance
    created_at = Column(TIMESTAMP, default=datetime.utcnow)

