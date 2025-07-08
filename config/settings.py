import os
from typing import Any, Dict, Optional
from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """应用配置类，使用pydantic进行环境变量验证和类型转换"""

    # 应用配置
    APP_NAME: str = "FastAPI-Template"
    APP_VERSION: str = "0.1.0"
    APP_ENV: str = "development"  # development, production, testing
    APP_DEBUG: bool = True
    APP_HOST: str = "0.0.0.0"
    APP_PORT: int = 8000

    # 数据库配置
    DATABASE_URL: str = "sqlite:///./app.db"
    DATABASE_ECHO: bool = True

    # JWT配置
    JWT_SECRET_KEY: str = "your-secret-key-change-in-production"
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24

    # 日志配置
    LOG_LEVEL: str = "INFO"

    # 验证环境
    @field_validator("APP_ENV")
    def validate_app_env(v: str) -> str:
        if v not in ["development", "production", "testing"]:
            raise ValueError(f"APP_ENV must be one of 'development', 'production', or 'testing', got '{v}'")
        return v

    # 从.env文件读取配置
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
    )

    def get_database_settings(self) -> Dict[str, Any]:
        """获取数据库相关设置"""
        return {
            "url": self.DATABASE_URL,
            "echo": self.DATABASE_ECHO,
        }


# 创建全局设置实例
settings = Settings()
