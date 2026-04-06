"""
用户数据访问层 - 使用原生 SQL
"""
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncConnection
from sqlalchemy import text


class UserRepository:
    """用户仓库 - 使用原生 SQL 查询"""
    
    def __init__(self, conn: AsyncConnection):
        self.conn = conn
    
    async def get_by_id(self, user_id: int) -> Optional[dict]:
        """通过 ID 获取用户"""
        sql = """
            SELECT id, email, username, hashed_password, is_active, role, created_at, updated_at
            FROM users
            WHERE id = :user_id
        """
        result = await self.conn.execute(text(sql), {"user_id": user_id})
        row = result.first()
        return dict(row._mapping) if row else None
    
    async def get_by_email(self, email: str) -> Optional[dict]:
        """通过邮箱获取用户"""
        sql = """
            SELECT id, email, username, hashed_password, is_active, role, created_at, updated_at
            FROM users
            WHERE email = :email
        """
        result = await self.conn.execute(text(sql), {"email": email})
        row = result.first()
        return dict(row._mapping) if row else None
    
    async def get_by_username(self, username: str) -> Optional[dict]:
        """通过用户名获取用户"""
        sql = """
            SELECT id, email, username, hashed_password, is_active, role, created_at, updated_at
            FROM users
            WHERE username = :username
        """
        result = await self.conn.execute(text(sql), {"username": username})
        row = result.first()
        return dict(row._mapping) if row else None
    
    async def get_all(self, skip: int = 0, limit: int = 100) -> list[dict]:
        """获取所有用户（分页）"""
        sql = """
            SELECT id, email, username, hashed_password, is_active, role, created_at, updated_at
            FROM users
            ORDER BY created_at DESC
            LIMIT :limit OFFSET :skip
        """
        result = await self.conn.execute(text(sql), {"skip": skip, "limit": limit})
        rows = result.fetchall()
        return [dict(row._mapping) for row in rows]
    
    async def create(self, email: str, username: str, hashed_password: str, 
                    role: str = "user") -> dict:
        """创建新用户"""
        sql = """
            INSERT INTO users (email, username, hashed_password, role, is_active)
            VALUES (:email, :username, :hashed_password, :role, 1)
            RETURNING id, email, username, hashed_password, is_active, role, created_at, updated_at
        """
        result = await self.conn.execute(
            text(sql),
            {
                "email": email,
                "username": username,
                "hashed_password": hashed_password,
                "role": role
            }
        )
        row = result.first()
        return dict(row._mapping) if row else None
    
    async def update(self, user_id: int, **kwargs) -> Optional[dict]:
        """更新用户信息"""
        # 构建动态更新语句
        update_fields = []
        params = {"user_id": user_id}
        
        for key, value in kwargs.items():
            if key in ["email", "username", "hashed_password", "is_active", "role"]:
                update_fields.append(f"{key} = :{key}")
                params[key] = value
        
        if not update_fields:
            return await self.get_by_id(user_id)
        
        sql = f"""
            UPDATE users
            SET {', '.join(update_fields)}, updated_at = CURRENT_TIMESTAMP
            WHERE id = :user_id
            RETURNING id, email, username, hashed_password, is_active, role, created_at, updated_at
        """
        result = await self.conn.execute(text(sql), params)
        row = result.first()
        return dict(row._mapping) if row else None
    
    async def delete(self, user_id: int) -> bool:
        """删除用户"""
        sql = "DELETE FROM users WHERE id = :user_id"
        result = await self.conn.execute(text(sql), {"user_id": user_id})
        return result.rowcount > 0
    
    async def count(self) -> int:
        """获取用户总数"""
        sql = "SELECT COUNT(*) as count FROM users"
        result = await self.conn.execute(text(sql))
        row = result.first()
        return row.count if row else 0