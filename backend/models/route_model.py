from sqlalchemy import Column, Integer, String, ForeignKey, DECIMAL, Boolean, TIMESTAMP, Interval
from sqlalchemy.orm import relationship
from datetime import datetime
from ..dependencies import Base

class Route(Base):
    __tablename__ = "routes"

    id = Column(Integer, primary_key=True, index=True)
    vehicle_id = Column(Integer, ForeignKey("vehicles.id"), nullable=False)
    branch_from = Column(Integer, ForeignKey("branches.id"), nullable=True)
    branch_to = Column(Integer, ForeignKey("branches.id"), nullable=True)
    estimated_time = Column(Interval, nullable=False)
    status = Column(String, nullable=False, default="pending")  # pending, in progress, completed
    created_at = Column(TIMESTAMP, default=datetime.utcnow)

    vehicle = relationship("Vehicle")
    branch_from_rel = relationship("Branch", foreign_keys=[branch_from])
    branch_to_rel = relationship("Branch", foreign_keys=[branch_to])