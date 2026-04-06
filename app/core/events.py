"""
应用生命周期事件
"""
from typing import Callable
from fastapi import FastAPI
from loguru import logger

from app.db.session import engine, close_db
from app.db.init_db import init_database
from config import settings


def startup_event_handler(app: FastAPI) -> Callable:
    """应用启动事件处理器"""
    async def startup() -> None:
        logger.info(f"Starting up {settings.APP_NAME} in {settings.APP_ENV} environment")
        
        # 初始化数据库连接和表结构
        try:
            await init_database(engine)
            logger.info("数据库初始化成功")
        except Exception as e:
            logger.error(f"数据库初始化失败: {e}")
            raise
        
        logger.info("Application startup complete")
    
    return startup


def shutdown_event_handler(app: FastAPI) -> Callable:
    """应用关闭事件处理器"""
    async def shutdown() -> None:
        logger.info("Shutting down application")
        
        # 关闭数据库连接
        await close_db()
        
        logger.info("Application shutdown complete")
    
    return shutdown