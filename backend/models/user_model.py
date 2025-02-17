from sqlalchemy import Column, Integer, String, ForeignKey, DECIMAL, TIMESTAMP
from sqlalchemy.orm import relationship
from datetime import datetime
from ..dependencies import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    phone = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(String, default="user")
    created_at = Column(TIMESTAMP, default=datetime.utcnow)

    shipments_sent = relationship("Shipment", foreign_keys="[Shipment.sender_id]", back_populates="sender")
    shipments_received = relationship("Shipment", foreign_keys="[Shipment.receiver_id]", back_populates="receiver")
