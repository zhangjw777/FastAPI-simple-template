from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.repositories.item_repository import ItemRepository
from app.schemas.item import ItemCreate, ItemUpdate


class ItemService:
    """物品服务类，处理物品相关业务逻辑"""
    
    def __init__(self, db: AsyncSession):
        self.repository = ItemRepository(db)
    
    async def create_item(self, item_in: ItemCreate, owner_id: int) -> dict:
        """创建新物品"""
        item = await self.repository.create(
            title=item_in.title,
            description=item_in.description,
            price=item_in.price,
            owner_id=owner_id,
        )
        
        return {
            "id": item.id,
            "title": item.title,
            "description": item.description,
            "price": item.price,
            "owner_id": item.owner_id,
            "created_at": item.created_at,
            "updated_at": item.updated_at,
        }
    
    async def get_items(self, skip: int = 0, limit: int = 100) -> List[dict]:
        """获取物品列表"""
        items = await self.repository.get_all(skip=skip, limit=limit)
        return [
            {
                "id": item.id,
                "title": item.title,
                "description": item.description,
                "price": item.price,
                "owner_id": item.owner_id,
                "created_at": item.created_at,
                "updated_at": item.updated_at,
            }
            for item in items
        ]
    
    async def get_items_by_owner(self, owner_id: int, skip: int = 0, limit: int = 100) -> List[dict]:
        """获取指定用户的所有物品"""
        items = await self.repository.get_items_by_owner(owner_id, skip=skip, limit=limit)
        return [
            {
                "id": item.id,
                "title": item.title,
                "description": item.description,
                "price": item.price,
                "owner_id": item.owner_id,
                "created_at": item.created_at,
                "updated_at": item.updated_at,
            }
            for item in items
        ]
    
    async def get_item(self, item_id: int) -> Optional[dict]:
        """通过ID获取物品"""
        item = await self.repository.get(item_id)
        if item is None:
            return None
        
        return {
            "id": item.id,
            "title": item.title,
            "description": item.description,
            "price": item.price,
            "owner_id": item.owner_id,
            "created_at": item.created_at,
            "updated_at": item.updated_at,
        }
    
    async def update_item(self, item_id: int, item_in: ItemUpdate) -> Optional[dict]:
        """更新物品信息"""
        item = await self.repository.get(item_id)
        if item is None:
            return None
        
        update_data = item_in.model_dump(exclude_unset=True)
        updated_item = await self.repository.update(item_id, **update_data)
        
        return {
            "id": updated_item.id,
            "title": updated_item.title,
            "description": updated_item.description,
            "price": updated_item.price,
            "owner_id": updated_item.owner_id,
            "created_at": updated_item.created_at,
            "updated_at": updated_item.updated_at,
        }
    
    async def delete_item(self, item_id: int) -> Optional[dict]:
        """删除物品"""
        item = await self.repository.delete(item_id)
        if item is None:
            return None
        
        return {
            "id": item.id,
            "title": item.title,
            "description": item.description,
            "price": item.price,
            "owner_id": item.owner_id,
            "created_at": item.created_at,
            "updated_at": item.updated_at,
        } 