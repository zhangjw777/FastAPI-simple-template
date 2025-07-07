from sqlalchemy import Column, ForeignKey, String, Text, Float, Integer
from sqlalchemy.orm import relationship

from app.db.session import Base
from app.db.models.base import BaseModel


class Item(Base, BaseModel):
    """物品模型"""
    
    title = Column(String(100), index=True, nullable=False)
    description = Column(Text, nullable=True)
    price = Column(Float, nullable=True)
    
    # 外键
    owner_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    
    # 关系
    owner = relationship("User", back_populates="items") 