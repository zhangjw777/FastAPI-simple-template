from typing import Optional
from datetime import datetime, timezone
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
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")
optional_oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login", auto_error=False)


def _credentials_exception(detail: str = "无法验证凭证") -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=detail,
        headers={"WWW-Authenticate": "Bearer"},
    )


async def _get_user_from_token(token: str, conn: AsyncConnection) -> UserResponse:
    try:
        payload = jwt.decode(
            token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM]
        )
        token_data = TokenPayload(**payload)
    except (JWTError, ValidationError):
        raise _credentials_exception()

    if token_data.exp is not None and datetime.fromtimestamp(token_data.exp, tz=timezone.utc) < datetime.now(timezone.utc):
        raise _credentials_exception("令牌已过期")

    if token_data.sub is None:
        raise _credentials_exception()

    try:
        user_id = int(token_data.sub)
    except (TypeError, ValueError):
        raise _credentials_exception()

    user_service = UserService(conn)
    user = await user_service.get_user(user_id)
    if user is None:
        raise _credentials_exception("用户不存在")
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="用户已被禁用",
        )

    return UserResponse.model_validate(user)


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
    return await _get_user_from_token(token, conn)


async def get_current_user_optional(
    token: Optional[str] = Depends(optional_oauth2_scheme),
    conn: AsyncConnection = Depends(get_db)
) -> Optional[UserResponse]:
    """可选地获取当前用户，不携带令牌时返回 None。"""
    if token is None:
        return None

    return await _get_user_from_token(token, conn)
