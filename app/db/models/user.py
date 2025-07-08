from sqlalchemy import Boolean, Column, String, Enum as SQLAlchemyEnum
from sqlalchemy.orm import relationship

from app.db.session import Base
from app.db.models.base import BaseModel
from app.schemas.role import Role


class User(Base, BaseModel):
    """用户模型"""
    
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    role = Column(SQLAlchemyEnum(Role), default=Role.USER, nullable=False)
    
    # 关系
    items = relationship("Item", back_populates="owner", cascade="all, delete-orphan") 