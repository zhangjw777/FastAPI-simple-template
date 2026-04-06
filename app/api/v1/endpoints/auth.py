import logging
from datetime import timedelta, datetime
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncConnection

from app.db.session import get_db
from app.schemas.token import Token
from app.schemas.response import ApiResponse, success_response
from app.services.user_service import UserService
from app.utils.security import create_access_token
from config import settings

router = APIRouter()


@router.post("/login", response_model=ApiResponse[Token])
async def login_for_access_token(
        form_data: OAuth2PasswordRequestForm = Depends(),
        conn: AsyncConnection = Depends(get_db)
):
    """
    登录获取访问令牌
    
    Args:
        form_data: 表单数据，包含用户名和密码
        conn: 数据库连接
    
    Returns:
        ApiResponse[Token]: 访问令牌响应
    """
    user_service = UserService(conn)
    user = await user_service.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户名或密码错误",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # 创建访问令牌
    access_token_expires = timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
    logging.info(f"用户 {user.username} 正在登录")
    logging.info(f"JWT过期时间设置(分钟): {settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES}")
    
    user_data_for_token = {
        "username": user.username,
        "id": user.id,
        "email": user.email,
    }
    
    access_token = create_access_token(
        expires_delta=access_token_expires, user_info=user_data_for_token
    )

    token_data = {
        "access_token": access_token,
        "token_type": "bearer"
    }
    
    return success_response(data=token_data, message="登录成功")
