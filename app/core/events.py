from typing import Callable
from fastapi import FastAPI
from loguru import logger

from app.db.session import init_db, close_db
from config import settings


def startup_event_handler(app: FastAPI) -> Callable:
    """
    应用启动事件处理器
    """
    async def startup() -> None:
        logger.info(f"Starting up {settings.APP_NAME} in {settings.APP_ENV} environment")
        
        # 初始化数据库连接
        await init_db()
        
        logger.info("Application startup complete")
    
    return startup


def shutdown_event_handler(app: FastAPI) -> Callable:
    """
    应用关闭事件处理器
    """
    async def shutdown() -> None:
        logger.info("Shutting down application")
        
        # 关闭数据库连接
        await close_db()
        
        logger.info("Application shutdown complete")
    
    return shutdown 