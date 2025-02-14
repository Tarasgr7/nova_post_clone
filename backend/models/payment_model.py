from sqlalchemy import Column, Integer, String, ForeignKey, DECIMAL, Boolean, TIMESTAMP, Interval
from sqlalchemy.orm import relationship
from datetime import datetime
from ..dependencies import Base
from .shipment_model import Shipment


class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)
    shipment_id = Column(Integer, ForeignKey("shipments.id"), nullable=False)
    amount = Column(DECIMAL(10,2), nullable=False)
    payment_method = Column(String, nullable=False)  # card, cash, postpaid
    payment_status = Column(String, nullable=False, default="pending")  # paid, pending, failed
    created_at = Column(TIMESTAMP, default=datetime.utcnow)

    shipment = relationship("Shipment", back_populates="payment")

Shipment.payment = relationship("Payment", back_populates="shipment", uselist=False)
