from sqlalchemy import Column, Integer, String, ForeignKey, DECIMAL, Boolean, TIMESTAMP, Interval
from sqlalchemy.orm import relationship
from datetime import datetime
from ..dependencies import Base

class Branch(Base):
    __tablename__ = "branches"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    address = Column(String, nullable=False)
    city = Column(String, nullable=False)
    phone = Column(String)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)

    shipments_from = relationship("Shipment", foreign_keys="[Shipment.branch_from]", back_populates="branch_from_rel")
    shipments_to = relationship("Shipment", foreign_keys="[Shipment.branch_to]", back_populates="branch_to_rel")
