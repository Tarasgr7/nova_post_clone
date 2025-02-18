from sqlalchemy import Column, Integer, String, ForeignKey, DECIMAL, Boolean, TIMESTAMP, Interval
from sqlalchemy.orm import relationship
from datetime import datetime
from ..dependencies import Base

class Shipment(Base):
    __tablename__ = "shipments"

    id = Column(Integer, primary_key=True, index=True)
    tracking_number = Column(String, unique=True, nullable=False)
    sender_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    receiver_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    branch_from = Column(Integer, ForeignKey("branches.id"), nullable=True)
    branch_to = Column(Integer, ForeignKey("branches.id"), nullable=True)
    location=Column(Integer, ForeignKey("branches.id"), nullable=True)
    weight = Column(DECIMAL(10,2), nullable=False)
    length = Column(DECIMAL(10, 2), nullable=False)
    width = Column(DECIMAL(10, 2), nullable=False)
    price = Column(DECIMAL(10,2), nullable=False)
    payment_status = Column(String, nullable=False, default="unpaid")  # paid, unpaid
    status = Column(String, nullable=False, default="created")  
    created_at = Column(TIMESTAMP, default=datetime.utcnow)

    sender = relationship("User", foreign_keys=[sender_id], back_populates="shipments_sent")
    receiver = relationship("User", foreign_keys=[receiver_id], back_populates="shipments_received")
    branch_from_rel = relationship("Branch", foreign_keys=[branch_from], back_populates="shipments_from")
    branch_to_rel = relationship("Branch", foreign_keys=[branch_to], back_populates="shipments_to")
    location_rel = relationship("Branch", foreign_keys=[location], back_populates="location")
    route_shipments = relationship("RouteShipment", back_populates="shipment")


class ShipmentStatus(Base):
    __tablename__ = "shipment_statuses"

    id = Column(Integer, primary_key=True, index=True)
    shipment_id = Column(Integer, ForeignKey("shipments.id"), nullable=False)
    status = Column(String, nullable=False)
    updated_at = Column(TIMESTAMP, default=datetime.utcnow)

    shipment = relationship("Shipment", back_populates="statuses")
Shipment.statuses = relationship("ShipmentStatus", back_populates="shipment", order_by="ShipmentStatus.updated_at")