from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncConnection

from app.db.session import get_db
from app.schemas.role import Role
from app.schemas.user import UserCreate, UserResponse, UserUpdate
from app.schemas.response import ApiResponse, success_response
from app.services.user_service import UserService
from app.utils.auth import get_current_user, get_current_user_optional

router = APIRouter()


def _require_admin(current_user: UserResponse) -> None:
    if current_user.role != Role.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="仅管理员可执行该操作"
        )


def _require_self_or_admin(current_user: UserResponse, target_user_id: int) -> None:
    if current_user.role == Role.ADMIN:
        return
    if current_user.id != target_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="没有权限操作其他用户"
        )


@router.post("", response_model=ApiResponse[UserResponse], status_code=status.HTTP_201_CREATED)
async def create_user(
        user_in: UserCreate,
        conn: AsyncConnection = Depends(get_db),
        current_user: Optional[UserResponse] = Depends(get_current_user_optional)
):
    """创建新用户。系统首次创建用户时自动初始化为管理员。"""
    user_service = UserService(conn)
    try:
        user_count = await user_service.count_users()

        if user_count == 0:
            bootstrap_user = user_in.model_copy(update={"role": Role.ADMIN})
            user = await user_service.create_user(bootstrap_user)
            return success_response(data=user, message="初始化管理员创建成功")

        if current_user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="请先登录管理员账号",
                headers={"WWW-Authenticate": "Bearer"},
            )

        _require_admin(current_user)
        user = await user_service.create_user(user_in)
        return success_response(data=user, message="用户创建成功")
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.post("/register", response_model=ApiResponse[UserResponse], status_code=status.HTTP_201_CREATED)
async def register_user(
        user_in: UserCreate,
        conn: AsyncConnection = Depends(get_db),
):
    "普通用户注册"
    user_service = UserService(conn)
    user = user_service.create_user(user_in)
    return success_response(data=user, message="用户注册成功")       

@router.get("", response_model=ApiResponse[List[UserResponse]])
async def get_users(
        skip: int = 0,
        limit: int = 100,
        conn: AsyncConnection = Depends(get_db),
        current_user: UserResponse = Depends(get_current_user)
):
    """获取用户列表"""
    _require_admin(current_user)
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
    _require_self_or_admin(current_user, user_id)
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
    _require_self_or_admin(current_user, user_id)

    if current_user.role != Role.ADMIN and ({"role", "is_active"} & user_in.model_fields_set):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="仅管理员可修改角色或启用状态"
        )

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
    _require_self_or_admin(current_user, user_id)

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
