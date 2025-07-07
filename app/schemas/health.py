from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    """健康检查响应模型"""
    
    status: str = Field(..., description="API状态")
    database: str = Field(..., description="数据库连接状态")
    api_version: str = Field(..., description="API版本") 