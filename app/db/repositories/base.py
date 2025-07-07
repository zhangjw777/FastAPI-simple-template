from typing import Generic, List, Optional, Type, TypeVar
from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.base import BaseModel

# 定义泛型类型变量
ModelType = TypeVar("ModelType", bound=BaseModel)


class BaseRepository(Generic[ModelType]):
    """基础仓库类，提供通用的CRUD操作"""
    
    def __init__(self, model: Type[ModelType], db: AsyncSession):
        self.model = model
        self.db = db
    
    async def get(self, id: int) -> Optional[ModelType]:
        """获取单个对象"""
        query = select(self.model).filter(self.model.id == id)
        result = await self.db.execute(query)
        return result.scalars().first()
    
    async def get_all(self, skip: int = 0, limit: int = 100) -> List[ModelType]:
        """获取多个对象"""
        query = select(self.model).offset(skip).limit(limit)
        result = await self.db.execute(query)
        return result.scalars().all()
    
    async def create(self, **kwargs) -> ModelType:
        """创建对象"""
        obj = self.model(**kwargs)
        self.db.add(obj)
        await self.db.commit()
        await self.db.refresh(obj)
        return obj
    
    async def update(self, id: int, **kwargs) -> Optional[ModelType]:
        """更新对象"""
        query = update(self.model).where(self.model.id == id).values(**kwargs).returning(self.model)
        result = await self.db.execute(query)
        await self.db.commit()
        return result.scalars().first()
    
    async def delete(self, id: int) -> Optional[ModelType]:
        """删除对象"""
        query = delete(self.model).where(self.model.id == id).returning(self.model)
        result = await self.db.execute(query)
        await self.db.commit()
        return result.scalars().first() 