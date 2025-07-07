from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field, field_validator


class UserBase(BaseModel):
    """用户基础模型"""
    
    email: Optional[EmailStr] = Field(None, description="用户邮箱")
    username: Optional[str] = Field(None, description="用户名")
    is_active: Optional[bool] = Field(True, description="是否激活")
    is_superuser: Optional[bool] = Field(False, description="是否为超级用户")


class UserCreate(UserBase):
    """用户创建模型"""
    
    email: EmailStr = Field(..., description="用户邮箱")
    username: str = Field(..., description="用户名")
    password: str = Field(..., description="密码")
    
    @field_validator("username")
    def username_alphanumeric(cls, v):
        assert v.isalnum(), "Username must be alphanumeric"
        return v
    
    @field_validator("password")
    def password_min_length(cls, v):
        assert len(v) >= 8, "Password must be at least 8 characters"
        return v


class UserUpdate(UserBase):
    """用户更新模型"""
    
    password: Optional[str] = Field(None, description="密码")
    
    @field_validator("password")
    def password_min_length(cls, v):
        if v is not None:
            assert len(v) >= 8, "Password must be at least 8 characters"
        return v


class UserResponse(UserBase):
    """用户响应模型"""
    
    id: int = Field(..., description="用户ID")
    email: EmailStr = Field(..., description="用户邮箱")
    username: str = Field(..., description="用户名")
    created_at: datetime = Field(..., description="创建时间")
    updated_at: datetime = Field(..., description="更新时间")
    
    class Config:
        """配置"""
        
        from_attributes = True 