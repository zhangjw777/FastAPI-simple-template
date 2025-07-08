import enum


class Role(str, enum.Enum):
    """用户角色"""
    ADMIN = "admin"
    USER = "user" 