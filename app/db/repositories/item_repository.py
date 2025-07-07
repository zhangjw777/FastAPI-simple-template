from typing import List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Item
from app.db.repositories.base import BaseRepository


class ItemRepository(BaseRepository[Item]):
    def __init__(self, db: AsyncSession):
        super().__init__(Item, db)
    
    async def get_items_by_owner(self, owner_id: int, skip: int = 0, limit: int = 100) -> List[Item]:
        """获取指定用户的所有物品"""
        query = select(Item).filter(Item.owner_id == owner_id).offset(skip).limit(limit)
        result = await self.db.execute(query)
        return result.scalars().all() 