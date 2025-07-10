from typing import Optional
from pydantic import BaseModel, Field


class Token(BaseModel):
    """令牌响应模型"""
    
    access_token: str = Field(..., description="访问令牌")
    token_type: str = Field(..., description="令牌类型")


class TokenPayload(BaseModel):
    """令牌载荷模型"""
    
    sub: Optional[str] = Field(None, description="主题")
    exp: Optional[int] = Field(None, description="过期时间")
    user_info: Optional[dict] = Field(None, description="用户信息")