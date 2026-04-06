"""
物品服务层 - 业务逻辑处理
"""
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncConnection

from app.db.repositories.item_repository import ItemRepository
from app.schemas.item import ItemCreate, ItemUpdate, Item


class ItemService:
    """物品服务类，处理物品相关业务逻辑"""
    
    def __init__(self, conn: AsyncConnection):
        self.repository = ItemRepository(conn)
    
    async def create_item(self, item_in: ItemCreate, owner_id: int) -> Item:
        """创建新物品"""
        item_data = await self.repository.create(
            title=item_in.title,
            description=item_in.description,
            price=item_in.price,
            owner_id=owner_id,
        )
        
        return Item(**item_data)
    
    async def get_items(self, skip: int = 0, limit: int = 100) -> list[Item]:
        """获取物品列表"""
        items_data = await self.repository.get_all(skip=skip, limit=limit)
        return [Item(**item_data) for item_data in items_data]
    
    async def get_items_by_owner(self, owner_id: int, skip: int = 0, limit: int = 100) -> list[Item]:
        """获取指定用户的所有物品"""
        items_data = await self.repository.get_items_by_owner(owner_id, skip=skip, limit=limit)
        return [Item(**item_data) for item_data in items_data]
    
    async def get_item(self, item_id: int) -> Optional[Item]:
        """通过ID获取物品"""
        item_data = await self.repository.get_by_id(item_id)
        if item_data is None:
            return None
        
        return Item(**item_data)
    
    async def update_item(self, item_id: int, item_in: ItemUpdate) -> Optional[Item]:
        """更新物品信息"""
        item_data = await self.repository.get_by_id(item_id)
        if item_data is None:
            return None
        
        update_data = item_in.model_dump(exclude_unset=True)
        updated_item_data = await self.repository.update(item_id, **update_data)
        
        return Item(**updated_item_data) if updated_item_data else None
    
    async def delete_item(self, item_id: int) -> bool:
        """删除物品"""
        return await self.repository.delete(item_id)
    
    async def count_items(self) -> int:
        """获取物品总数"""
        return await self.repository.count()
    
    async def count_items_by_owner(self, owner_id: int) -> int:
        """获取指定用户的物品总数"""
        return await self.repository.count_by_owner(owner_id)