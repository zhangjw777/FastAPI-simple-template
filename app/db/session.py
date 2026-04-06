"""
数据库连接管理模块 - 使用 SQLAlchemy Core
支持原生 SQL 查询，不使用 ORM
"""
import logging
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncConnection, AsyncEngine, create_async_engine
from sqlalchemy import MetaData, text

from config import settings

# 获取数据库URL
db_url = settings.DATABASE_URL

# SQLite URL 兼容性处理
if db_url.startswith("sqlite"):
    db_url = db_url.replace("sqlite", "sqlite+aiosqlite", 1)

# 创建异步引擎
engine: AsyncEngine = create_async_engine(
    db_url,
    echo=settings.DATABASE_ECHO,
    future=True,
    pool_pre_ping=True,  # 连接池预检
)

# 创建 MetaData 对象用于表定义
metadata = MetaData()


async def get_db() -> AsyncGenerator[AsyncConnection, None]:
    """
    获取数据库连接的依赖函数
    返回 AsyncConnection 而非 AsyncSession，用于执行原生 SQL
    """
    async with engine.begin() as conn:
        yield conn


async def execute_sql(conn: AsyncConnection, sql: str, params: dict = None):
    """
    执行 SQL 查询的辅助函数
    
    Args:
        conn: 数据库连接
        sql: SQL 查询字符串
        params: 查询参数（字典形式）
    
    Returns:
        查询结果
    """
    result = await conn.execute(text(sql), params or {})
    return result


async def fetch_one(conn: AsyncConnection, sql: str, params: dict = None) -> dict | None:
    """
    执行查询并返回单条记录
    
    Args:
        conn: 数据库连接
        sql: SQL 查询字符串
        params: 查询参数
    
    Returns:
        单条记录（字典形式）或 None
    """
    result = await execute_sql(conn, sql, params)
    row = result.first()
    if row:
        return dict(row._mapping)
    return None


async def fetch_all(conn: AsyncConnection, sql: str, params: dict = None) -> list[dict]:
    """
    执行查询并返回所有记录
    
    Args:
        conn: 数据库连接
        sql: SQL 查询字符串
        params: 查询参数
    
    Returns:
        记录列表（每条记录为字典）
    """
    result = await execute_sql(conn, sql, params)
    rows = result.fetchall()
    return [dict(row._mapping) for row in rows]


async def close_db() -> None:
    """关闭数据库连接池"""
    await engine.dispose()
    logging.info("数据库连接池已关闭")