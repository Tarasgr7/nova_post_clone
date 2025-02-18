from sqlalchemy import Column, Integer, String, ForeignKey, DECIMAL, Boolean, TIMESTAMP, Interval
from sqlalchemy.orm import relationship
from datetime import datetime
from ..dependencies import Base
class Worker(Base):
    __tablename__ = "worker"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    branch_id = Column(Integer, ForeignKey("branches.id"), nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)

    user = relationship("User")
    branch = relationship("Branch")