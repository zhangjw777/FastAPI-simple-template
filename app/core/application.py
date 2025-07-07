from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config import settings
from app.api.v1.api import api_router
from app.middlewares.exception_handler import add_exception_handlers
from app.core.events import startup_event_handler, shutdown_event_handler


def create_app() -> FastAPI:
    """
    应用工厂函数，创建FastAPI应用实例
    """
    app = FastAPI(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        description="FastAPI应用模板，基于SpringBoot结构理念",
        debug=settings.APP_DEBUG,
    )
    
    # 配置CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # 注册路由
    app.include_router(api_router, prefix="/api")
    
    # 注册事件处理器
    app.add_event_handler("startup", startup_event_handler(app))
    app.add_event_handler("shutdown", shutdown_event_handler(app))
    
    # 注册全局异常处理
    add_exception_handlers(app)
    
    @app.get("/")
    async def root():
        return {
            "app_name": settings.APP_NAME,
            "version": settings.APP_VERSION,
            "environment": settings.APP_ENV,
            "docs": "/docs",
        }
    
    return app 