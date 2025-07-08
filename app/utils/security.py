from datetime import datetime, timedelta, timezone
from typing import Any, Optional, Union, Dict
from jose import jwt
import bcrypt

from config import settings


def create_access_token(expires_delta: Optional[timedelta] = None,
                        user_info: Optional[Dict[str, Any]] = None) -> str:
    """
    创建JWT访问令牌
    
    Args:
        expires_delta: 过期时间
        user_info: 可选的用户附加信息字典，默认为None
    Returns:
        str: JWT令牌
    """
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES
        )

    # 创建标准JWT内容
    to_encode = {
        "exp": int(expire.timestamp()),  # 过期时间
    }
    
    # 如果有用户信息，添加subject和用户信息
    if user_info:
        # 确保有用户ID作为subject
        if "id" in user_info:
            to_encode["sub"] = str(user_info["id"])
        # 其他用户信息放入user_info字段
        to_encode["user_info"] = user_info
    
    encoded_jwt = jwt.encode(
        to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM
    )
    return encoded_jwt


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    验证密码
    
    Args:
        plain_password: 明文密码
        hashed_password: 哈希密码
    
    Returns:
        bool: 是否验证通过
    """
    password_byte = plain_password.encode('utf-8')
    hashed_password_byte = hashed_password.encode('utf-8')
    return bcrypt.checkpw(password_byte, hashed_password_byte)


def get_password_hash(password: str) -> str:
    """
    获取密码哈希
    
    Args:
        password: 明文密码
    
    Returns:
        str: 哈希密码
    """
    pwd_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(pwd_bytes, salt)
    return hashed_password.decode('utf-8')
