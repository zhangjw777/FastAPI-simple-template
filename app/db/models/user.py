from sqlalchemy import Boolean, Column, String
from sqlalchemy.orm import relationship

from app.db.session import Base
from app.db.models.base import BaseModel


class User(Base, BaseModel):
    """用户模型"""
    
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    
    # 关系
    items = relationship("Item", back_populates="owner", cascade="all, delete-orphan") 