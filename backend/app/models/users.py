from app.config.database import Base
from sqlalchemy import Column, Integer, String, DateTime, Boolean, func, ForeignKey
from sqlalchemy.orm import relationship
from app.models.projects import Projects


class Users(Base):
    __tablename__ = "users"
    id = Column(Integer, autoincrement=True, nullable=True)
    clerk_id = Column(String, primary_key=True, index=True)
    email = Column(String, unique=True)
    full_name = Column(String)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now())
    credits = Column(Integer, default=100)
    is_active = Column(Boolean)
    projects = relationship(Projects, back_populates="user")

    # Relationship to Txns
    txns = relationship("Txns", back_populates="user")
