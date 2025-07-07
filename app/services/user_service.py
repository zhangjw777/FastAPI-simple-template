from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate, UserUpdate
from app.utils.security import get_password_hash, verify_password


class UserService:
    """用户服务类，处理用户相关业务逻辑"""
    
    def __init__(self, db: AsyncSession):
        self.repository = UserRepository(db)
    
    async def create_user(self, user_in: UserCreate) -> dict:
        """创建新用户"""
        # 检查邮箱是否已存在
        existing_user = await self.repository.get_by_email(user_in.email)
        if existing_user:
            raise ValueError("Email already registered")
        
        # 检查用户名是否已存在
        existing_user = await self.repository.get_by_username(user_in.username)
        if existing_user:
            raise ValueError("Username already taken")
        
        # 创建用户
        hashed_password = get_password_hash(user_in.password)
        user = await self.repository.create(
            email=user_in.email,
            username=user_in.username,
            hashed_password=hashed_password,
        )
        
        # 转换为字典
        return {
            "id": user.id,
            "email": user.email,
            "username": user.username,
            "is_active": user.is_active,
            "is_superuser": user.is_superuser,
            "created_at": user.created_at,
            "updated_at": user.updated_at,
        }
    
    async def authenticate_user(self, username: str, password: str) -> Optional[dict]:
        """验证用户"""
        user = await self.repository.get_by_username(username)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        
        # 转换为字典
        return {
            "id": user.id,
            "email": user.email,
            "username": user.username,
            "is_active": user.is_active,
            "is_superuser": user.is_superuser,
        }
    
    async def get_users(self, skip: int = 0, limit: int = 100) -> List[dict]:
        """获取用户列表"""
        users = await self.repository.get_all(skip=skip, limit=limit)
        return [
            {
                "id": user.id,
                "email": user.email,
                "username": user.username,
                "is_active": user.is_active,
                "is_superuser": user.is_superuser,
                "created_at": user.created_at,
                "updated_at": user.updated_at,
            }
            for user in users
        ]
    
    async def get_user(self, user_id: int) -> Optional[dict]:
        """通过ID获取用户"""
        user = await self.repository.get(user_id)
        if user is None:
            return None
        
        return {
            "id": user.id,
            "email": user.email,
            "username": user.username,
            "is_active": user.is_active,
            "is_superuser": user.is_superuser,
            "created_at": user.created_at,
            "updated_at": user.updated_at,
        }
    
    async def update_user(self, user_id: int, user_in: UserUpdate) -> Optional[dict]:
        """更新用户信息"""
        user = await self.repository.get(user_id)
        if user is None:
            return None
        
        update_data = user_in.model_dump(exclude_unset=True)
        
        # 如果更新密码，则需要哈希
        if "password" in update_data:
            update_data["hashed_password"] = get_password_hash(update_data.pop("password"))
        
        updated_user = await self.repository.update(user_id, **update_data)
        
        return {
            "id": updated_user.id,
            "email": updated_user.email,
            "username": updated_user.username,
            "is_active": updated_user.is_active,
            "is_superuser": updated_user.is_superuser,
            "created_at": updated_user.created_at,
            "updated_at": updated_user.updated_at,
        }
    
    async def delete_user(self, user_id: int) -> Optional[dict]:
        """删除用户"""
        user = await self.repository.delete(user_id)
        if user is None:
            return None
        
        return {
            "id": user.id,
            "email": user.email,
            "username": user.username,
            "is_active": user.is_active,
            "is_superuser": user.is_superuser,
            "created_at": user.created_at,
            "updated_at": user.updated_at,
        } 