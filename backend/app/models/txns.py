from app.config.database import Base
from sqlalchemy import Column, Integer, String, DateTime, Boolean, func, Enum
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey
from enum import Enum as PyEnum, auto


class TxnType(PyEnum):
    CREDIT_PURCHASE = "credit_purchase"
    CANCELED = "canceled"
    REFUND = "refund"
    BONUS = "bonus"


class Txns(Base):
    __tablename__ = "txns"
    id = Column(Integer, autoincrement=True, primary_key=True)
    clerk_id = Column(String, ForeignKey("users.clerk_id"), nullable=False)
    txn_type = Column(Enum(TxnType))
    amount = Column(Integer, nullable=False)
    created_at = Column(DateTime, server_default=func.now())

    payment_id = Column(String, unique=True, nullable=False)
    payment_method = Column(String)
    credits_added = Column(Integer, nullable=False)
    user = relationship("Users", back_populates="txns")
