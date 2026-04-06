from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field, field_validator

from app.schemas.role import Role


class UserBase(BaseModel):
    """用户基础模型"""

    email: Optional[EmailStr] = Field(None, description="用户邮箱")
    username: Optional[str] = Field(None, description="用户名")
    is_active: Optional[bool] = Field(True, description="是否激活")
    role: Optional[Role] = Field(None, description="用户角色")


class UserCreate(UserBase):
    """用户创建模型"""

    email: EmailStr = Field(..., description="用户邮箱")
    username: str = Field(..., description="用户名")
    password: str = Field(..., description="密码")
    role: Role = Field(Role.USER, description="用户角色")

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
    username: Optional[str] = Field(None, description="用户名")
    email: Optional[EmailStr] = Field(None, description="用户邮箱")
    password: Optional[str] = Field(None, description="密码")
    role: Optional[Role] = Field(None, description="用户角色")

    @field_validator("password")
    def password_min_length(cls, v):
        if v is not None:
            assert len(v) >= 8, "Password must be at least 8 characters"
        return v


class User(BaseModel):
    """用户完整模型（用于 Service 层）"""
    
    id: int
    email: str
    username: str
    hashed_password: str
    is_active: bool
    role: Role
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class UserResponse(BaseModel):
    """用户响应模型（API 返回，不包含密码）"""

    id: int = Field(..., description="用户ID")
    email: EmailStr = Field(..., description="用户邮箱")
    username: str = Field(..., description="用户名")
    is_active: bool = Field(..., description="是否激活")
    role: Role = Field(..., description="用户角色")
    created_at: datetime = Field(..., description="创建时间")
    updated_at: datetime = Field(..., description="更新时间")

    class Config:
        """配置"""
        from_attributes = True