from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncConnection

from app.db.session import get_db
from app.schemas.item import ItemCreate, ItemResponse, ItemUpdate
from app.schemas.response import ApiResponse, success_response
from app.services.item_service import ItemService
from app.utils.auth import get_current_user
from app.schemas.user import UserResponse

router = APIRouter()


@router.post("", response_model=ApiResponse[ItemResponse], status_code=status.HTTP_201_CREATED)
async def create_item(
    item_in: ItemCreate,
    conn: AsyncConnection = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user)
):
    """创建新物品"""
    item_service = ItemService(conn)
    item = await item_service.create_item(item_in, owner_id=current_user.id)
    return success_response(data=item, message="物品创建成功")


@router.get("", response_model=ApiResponse[List[ItemResponse]])
async def get_items(
    skip: int = 0,
    limit: int = 100,
    conn: AsyncConnection = Depends(get_db)
):
    """获取物品列表"""
    item_service = ItemService(conn)
    items = await item_service.get_items(skip=skip, limit=limit)
    return success_response(data=items, message="获取物品列表成功")


@router.get("/{item_id}", response_model=ApiResponse[ItemResponse])
async def get_item(
    item_id: int,
    conn: AsyncConnection = Depends(get_db)
):
    """通过ID获取物品"""
    item_service = ItemService(conn)
    item = await item_service.get_item(item_id)
    if item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="物品不存在"
        )
    return success_response(data=item, message="获取物品成功")


@router.put("/{item_id}", response_model=ApiResponse[ItemResponse])
async def update_item(
    item_id: int,
    item_in: ItemUpdate,
    conn: AsyncConnection = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user)
):
    """更新物品信息"""
    item_service = ItemService(conn)
    item = await item_service.get_item(item_id)
    if item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="物品不存在"
        )
    
    if item.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="没有权限操作此物品"
        )
    
    updated_item = await item_service.update_item(item_id, item_in)
    return success_response(data=updated_item, message="更新物品成功")


@router.delete("/{item_id}", response_model=ApiResponse[dict])
async def delete_item(
    item_id: int,
    conn: AsyncConnection = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user)
):
    """删除物品"""
    item_service = ItemService(conn)
    item = await item_service.get_item(item_id)
    if item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="物品不存在"
        )
    
    if item.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="没有权限操作此物品"
        )
    
    success = await item_service.delete_item(item_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="删除物品失败"
        )
    
    return success_response(data={"item_id": item_id}, message="删除物品成功")