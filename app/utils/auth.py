from typing import Optional
from datetime import datetime
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncConnection

from app.db.session import get_db
from app.schemas.token import TokenPayload
from app.schemas.user import UserResponse
from app.services.user_service import UserService
from config import settings

# OAuth2密码承载令牌
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    conn: AsyncConnection = Depends(get_db)
) -> UserResponse:
    """
    获取当前用户
    
    Args:
        token: JWT令牌
        conn: 数据库连接
    
    Returns:
        UserResponse: 用户信息
    
    Raises:
        HTTPException: 身份验证失败
    """
    try:
        # 解码令牌
        payload = jwt.decode(
            token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM]
        )
        token_data = TokenPayload(**payload)
        
        # 检查令牌是否过期
        if token_data.exp and datetime.fromtimestamp(token_data.exp) < datetime.now():
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="令牌已过期",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # 获取用户ID
        user_id: Optional[str] = token_data.sub
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="无法验证凭证",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except (JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="无法验证凭证",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # 从数据库获取用户
    user_service = UserService(conn)
    user = await user_service.get_user(int(user_id))
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户不存在",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return UserResponse.model_validate(user)