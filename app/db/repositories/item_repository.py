"""
物品数据访问层 - 使用原生 SQL
"""
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncConnection
from sqlalchemy import text


class ItemRepository:
    """物品仓库 - 使用原生 SQL 查询"""
    
    def __init__(self, conn: AsyncConnection):
        self.conn = conn
    
    async def get_by_id(self, item_id: int) -> Optional[dict]:
        """通过 ID 获取物品"""
        sql = """
            SELECT id, title, description, price, owner_id, created_at, updated_at
            FROM items
            WHERE id = :item_id
        """
        result = await self.conn.execute(text(sql), {"item_id": item_id})
        row = result.first()
        return dict(row._mapping) if row else None
    
    async def get_all(self, skip: int = 0, limit: int = 100) -> list[dict]:
        """获取所有物品（分页）"""
        sql = """
            SELECT id, title, description, price, owner_id, created_at, updated_at
            FROM items
            ORDER BY created_at DESC
            LIMIT :limit OFFSET :skip
        """
        result = await self.conn.execute(text(sql), {"skip": skip, "limit": limit})
        rows = result.fetchall()
        return [dict(row._mapping) for row in rows]
    
    async def get_items_by_owner(self, owner_id: int, skip: int = 0, limit: int = 100) -> list[dict]:
        """获取指定用户的所有物品"""
        sql = """
            SELECT id, title, description, price, owner_id, created_at, updated_at
            FROM items
            WHERE owner_id = :owner_id
            ORDER BY created_at DESC
            LIMIT :limit OFFSET :skip
        """
        result = await self.conn.execute(
            text(sql),
            {"owner_id": owner_id, "skip": skip, "limit": limit}
        )
        rows = result.fetchall()
        return [dict(row._mapping) for row in rows]
    
    async def create(self, title: str, description: str, price: float, owner_id: int) -> dict:
        """创建新物品"""
        sql = """
            INSERT INTO items (title, description, price, owner_id)
            VALUES (:title, :description, :price, :owner_id)
            RETURNING id, title, description, price, owner_id, created_at, updated_at
        """
        result = await self.conn.execute(
            text(sql),
            {
                "title": title,
                "description": description,
                "price": price,
                "owner_id": owner_id
            }
        )
        row = result.first()
        return dict(row._mapping) if row else None
    
    async def update(self, item_id: int, **kwargs) -> Optional[dict]:
        """更新物品信息"""
        update_fields = []
        params = {"item_id": item_id}
        
        for key, value in kwargs.items():
            if key in ["title", "description", "price"]:
                update_fields.append(f"{key} = :{key}")
                params[key] = value
        
        if not update_fields:
            return await self.get_by_id(item_id)
        
        sql = f"""
            UPDATE items
            SET {', '.join(update_fields)}, updated_at = CURRENT_TIMESTAMP
            WHERE id = :item_id
            RETURNING id, title, description, price, owner_id, created_at, updated_at
        """
        result = await self.conn.execute(text(sql), params)
        row = result.first()
        return dict(row._mapping) if row else None
    
    async def delete(self, item_id: int) -> bool:
        """删除物品"""
        sql = "DELETE FROM items WHERE id = :item_id"
        result = await self.conn.execute(text(sql), {"item_id": item_id})
        return result.rowcount > 0
    
    async def count(self) -> int:
        """获取物品总数"""
        sql = "SELECT COUNT(*) as count FROM items"
        result = await self.conn.execute(text(sql))
        row = result.first()
        return row.count if row else 0
    
    async def count_by_owner(self, owner_id: int) -> int:
        """获取指定用户的物品总数"""
        sql = "SELECT COUNT(*) as count FROM items WHERE owner_id = :owner_id"
        result = await self.conn.execute(text(sql), {"owner_id": owner_id})
        row = result.first()
        return row.count if row else 0