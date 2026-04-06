from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncConnection

from app.db.session import get_db
from app.schemas.user import UserCreate, UserResponse, UserUpdate
from app.schemas.response import ApiResponse, success_response, error_response
from app.services.user_service import UserService
from app.utils.auth import get_current_user

router = APIRouter()


@router.post("", response_model=ApiResponse[UserResponse], status_code=status.HTTP_201_CREATED)
async def create_user(
        user_in: UserCreate,
        conn: AsyncConnection = Depends(get_db),
        current_user: UserResponse = Depends(get_current_user)
):
    """创建新用户"""
    try:
        user_service = UserService(conn)
        user = await user_service.create_user(user_in)
        return success_response(data=user, message="用户创建成功")
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("", response_model=ApiResponse[List[UserResponse]])
async def get_users(
        skip: int = 0,
        limit: int = 100,
        conn: AsyncConnection = Depends(get_db),
        current_user: UserResponse = Depends(get_current_user)
):
    """获取用户列表"""
    user_service = UserService(conn)
    users = await user_service.get_users(skip=skip, limit=limit)
    return success_response(data=users, message="获取用户列表成功")


@router.get("/{user_id}", response_model=ApiResponse[UserResponse])
async def get_user(
        user_id: int,
        conn: AsyncConnection = Depends(get_db),
        current_user: UserResponse = Depends(get_current_user)
):
    """通过ID获取用户"""
    user_service = UserService(conn)
    user = await user_service.get_user(user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="用户不存在"
        )
    return success_response(data=user, message="获取用户成功")


@router.put("/{user_id}", response_model=ApiResponse[UserResponse])
async def update_user(
        user_id: int,
        user_in: UserUpdate,
        conn: AsyncConnection = Depends(get_db),
        current_user: UserResponse = Depends(get_current_user)
):
    """更新用户信息"""
    user_service = UserService(conn)
    user = await user_service.update_user(user_id, user_in)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="用户不存在"
        )
    return success_response(data=user, message="更新用户成功")


@router.delete("/{user_id}", response_model=ApiResponse[dict])
async def delete_user(
        user_id: int,
        conn: AsyncConnection = Depends(get_db),
        current_user: UserResponse = Depends(get_current_user)
):
    """删除用户"""
    user_service = UserService(conn)
    # 先检查用户是否存在
    user = await user_service.get_user(user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="用户不存在"
        )
    
    success = await user_service.delete_user(user_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="删除用户失败"
        )
    
    return success_response(data={"user_id": user_id}, message="删除用户成功")
