from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class ItemBase(BaseModel):
    """物品基础模型"""
    
    title: Optional[str] = Field(None, description="物品标题")
    description: Optional[str] = Field(None, description="物品描述")
    price: Optional[float] = Field(None, ge=0, description="物品价格")


class ItemCreate(ItemBase):
    """物品创建模型"""
    
    title: str = Field(..., description="物品标题")


class ItemUpdate(ItemBase):
    """物品更新模型"""
    
    pass


class Item(BaseModel):
    """物品完整模型（用于 Service 层）"""
    
    id: int
    title: str
    description: Optional[str]
    price: Optional[float]
    owner_id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class ItemResponse(BaseModel):
    """物品响应模型（API 返回）"""
    
    id: int = Field(..., description="物品ID")
    title: str = Field(..., description="物品标题")
    description: Optional[str] = Field(None, description="物品描述")
    price: Optional[float] = Field(None, description="物品价格")
    owner_id: int = Field(..., description="物品所有者ID")
    created_at: datetime = Field(..., description="创建时间")
    updated_at: datetime = Field(..., description="更新时间")
    
    class Config:
        """配置"""
        from_attributes = True