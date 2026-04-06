from typing import Any, Optional, Generic, TypeVar
from pydantic import BaseModel, Field

T = TypeVar('T')


class ApiResponse(BaseModel, Generic[T]):
    """统一 API 响应格式"""
    success: bool = Field(..., description="请求是否成功")
    data: Optional[T] = Field(None, description="响应数据")
    message: str = Field(default="", description="响应消息")
    code: int = Field(default=200, description="业务状态码")

    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "data": {"id": 1, "name": "example"},
                "message": "操作成功",
                "code": 200
            }
        }


class PaginatedResponse(BaseModel, Generic[T]):
    """分页响应格式"""
    items: list[T] = Field(..., description="数据列表")
    total: int = Field(..., description="总数")
    page: int = Field(..., description="当前页码")
    page_size: int = Field(..., description="每页大小")
    pages: int = Field(..., description="总页数")

    class Config:
        json_schema_extra = {
            "example": {
                "items": [],
                "total": 100,
                "page": 1,
                "page_size": 10,
                "pages": 10
            }
        }


def success_response(
    data: Any = None,
    message: str = "操作成功",
    code: int = 200
) -> dict:
    """成功响应辅助函数"""
    return {
        "success": True,
        "data": data,
        "message": message,
        "code": code
    }


def error_response(
    message: str = "操作失败",
    code: int = 400,
    data: Any = None
) -> dict:
    """错误响应辅助函数"""
    return {
        "success": False,
        "data": data,
        "message": message,
        "code": code
    }
