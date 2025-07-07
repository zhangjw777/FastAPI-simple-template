import asyncio
import os
from typing import AsyncGenerator, Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.core.application import create_app
from app.db.session import Base, get_db
from config import settings

# 测试数据库URL
TEST_DATABASE_URL = "sqlite+aiosqlite:///./test.db"

# 设置测试数据库
engine = create_async_engine(
    TEST_DATABASE_URL,
    echo=False,
    future=True,
)
TestSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


@pytest.fixture(scope="session")
def event_loop() -> Generator:
    """创建事件循环"""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


async def override_get_db() -> AsyncGenerator[AsyncSession, None]:
    """测试数据库会话"""
    db = TestSessionLocal()
    try:
        yield db
    finally:
        await db.close()


@pytest.fixture(scope="session")
async def test_db() -> AsyncGenerator[AsyncSession, None]:
    """创建测试数据库"""
    # 创建数据库表
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    
    # 提供测试数据库会话
    db = TestSessionLocal()
    try:
        yield db
    finally:
        await db.close()
        
    # 清理
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    
    await engine.dispose()


@pytest.fixture(scope="function")
async def client(test_db: AsyncSession) -> Generator:
    """创建测试客户端"""
    # 设置测试环境
    os.environ["TESTING"] = "True"
    
    # 创建应用
    app = create_app()
    
    # 覆盖依赖
    app.dependency_overrides[get_db] = override_get_db
    
    # 创建测试客户端
    with TestClient(app) as test_client:
        yield test_client 