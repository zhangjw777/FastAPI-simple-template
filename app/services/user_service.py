"""
用户服务层 - 业务逻辑处理
"""
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncConnection

from app.db.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate, UserUpdate, User
from app.utils.security import get_password_hash, verify_password


class UserService:
    """用户服务类，处理用户相关业务逻辑"""
    
    def __init__(self, conn: AsyncConnection):
        self.repository = UserRepository(conn)
    
    async def create_user(self, user_in: UserCreate) -> User:
        """创建新用户"""
        # 检查邮箱是否已存在
        existing_user = await self.repository.get_by_email(user_in.email)
        if existing_user:
            raise ValueError("邮箱已被注册")
        
        # 检查用户名是否已存在
        existing_user = await self.repository.get_by_username(user_in.username)
        if existing_user:
            raise ValueError("用户名已被使用")
        
        # 创建用户
        hashed_password = get_password_hash(user_in.password)
        user_data = await self.repository.create(
            email=user_in.email,
            username=user_in.username,
            hashed_password=hashed_password,
            role=user_in.role.value,
        )
        
        return User(**user_data)
    
    async def authenticate_user(self, username: str, password: str) -> Optional[User]:
        """验证用户"""
        user_data = await self.repository.get_by_username(username)
        if not user_data:
            return None
        if not user_data.get("is_active", True):
            return None
        if not verify_password(password, user_data["hashed_password"]):
            return None
        
        return User(**user_data)
    
    async def get_users(self, skip: int = 0, limit: int = 100) -> list[User]:
        """获取用户列表"""
        users_data = await self.repository.get_all(skip=skip, limit=limit)
        return [User(**user_data) for user_data in users_data]
    
    async def get_user(self, user_id: int) -> Optional[User]:
        """通过ID获取用户"""
        user_data = await self.repository.get_by_id(user_id)
        if user_data is None:
            return None
        
        return User(**user_data)
    
    async def update_user(self, user_id: int, user_in: UserUpdate) -> Optional[User]:
        """更新用户信息"""
        user_data = await self.repository.get_by_id(user_id)
        if user_data is None:
            return None
        
        update_data = user_in.model_dump(exclude_unset=True)
        
        # 如果更新密码，则需要哈希
        if "password" in update_data:
            update_data["hashed_password"] = get_password_hash(update_data.pop("password"))
        
        # 如果更新角色，转换为字符串
        if "role" in update_data:
            update_data["role"] = update_data["role"].value
        
        updated_user_data = await self.repository.update(user_id, **update_data)
        
        return User(**updated_user_data) if updated_user_data else None
    
    async def delete_user(self, user_id: int) -> bool:
        """删除用户"""
        return await self.repository.delete(user_id)
    
    async def count_users(self) -> int:
        """获取用户总数"""
        return await self.repository.count()