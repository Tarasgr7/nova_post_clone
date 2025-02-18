from sqlalchemy import Column, Integer, String, ForeignKey, DECIMAL, Boolean, TIMESTAMP, Interval,DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from ..dependencies import Base


class Route(Base):
    __tablename__ = "routes"

    id = Column(Integer, primary_key=True, index=True)
    branch_from_id = Column(Integer, ForeignKey("branches.id"), nullable=False)
    branch_to_id = Column(Integer, ForeignKey("branches.id"), nullable=False)
    courier_id = Column(Integer, ForeignKey("couriers.id"), nullable=True)  # Кур'єр може бути призначений пізніше
    status = Column(String, default="created")  # 'created', 'in_progress', 'completed'
    created_at = Column(DateTime, default=datetime.utcnow)

    branch_from = relationship("Branch", foreign_keys=[branch_from_id], back_populates="routes_from")
    branch_to = relationship("Branch", foreign_keys=[branch_to_id], back_populates="routes_to")
    courier = relationship("Courier", foreign_keys=[courier_id])

    shipments = relationship("RouteShipment", back_populates="route")


class RouteShipment(Base):
    __tablename__ = "route_shipments"

    id = Column(Integer, primary_key=True, index=True)
    route_id = Column(Integer, ForeignKey("routes.id"), nullable=False)
    shipment_id = Column(Integer, ForeignKey("shipments.id"), nullable=False)
    
    route = relationship("Route", back_populates="shipments")
    shipment = relationship("Shipment", back_populates="route_shipments")

