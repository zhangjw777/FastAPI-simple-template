import os
import logging
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base

from config import settings

# 获取数据库URL
db_url = settings.DATABASE_URL

# 提取SQLite数据库文件路径（如果使用的是SQLite）
db_file_path = None
if db_url.startswith("sqlite:///"):
    # 从SQLite URL中提取文件路径
    db_file_path = db_url.replace("sqlite:///", "")

# 创建SQLite URL兼容性处理
if db_url.startswith("sqlite"):
    # SQLite URL needs to be adjusted for asyncio
    db_url = db_url.replace("sqlite", "sqlite+aiosqlite", 1)

# 创建异步引擎 // 连接某种数据库
engine = create_async_engine(
    db_url,
    echo=settings.DATABASE_ECHO,
    future=True,
)

# 创建会话工厂//其实就是数据库连接池，绑定之前的引擎。会话是操作数据库的直接手段，每次访问数据库都应创建一个会话
SessionLocal = async_sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    expire_on_commit=False,
)

# 创建Base类
Base = declarative_base()


async def init_db() -> None:
    """初始化数据库，仅在数据库文件不存在时创建所有表"""
    # 检查SQLite数据库文件是否存在
    db_exists = False
    if db_file_path and os.path.isfile(db_file_path):
        db_exists = True
        logging.info(f"发现现有数据库文件: {db_file_path}")
    else:
        logging.info(f"未找到数据库文件，将创建新的数据库: {db_file_path}")
        
    async with engine.begin() as conn:
        # 只在数据库文件不存在时创建表
        if not db_exists:
            # 创建所有表
            await conn.run_sync(Base.metadata.create_all)
            logging.info("创建了所有数据库表")
        else:
            logging.info("使用现有数据库，没有创建新表")


async def close_db() -> None:
    """关闭数据库连接"""
    await engine.dispose()


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """获取数据库会话的依赖函数"""
    db = SessionLocal()
    try:
        yield db
    finally:
        await db.close() 