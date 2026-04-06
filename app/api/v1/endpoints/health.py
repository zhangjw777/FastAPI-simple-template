from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncConnection
from sqlalchemy import text

from app.db.session import get_db
from app.schemas.health import HealthResponse
from app.schemas.response import ApiResponse, success_response

router = APIRouter()


@router.get("", response_model=ApiResponse[HealthResponse])
async def health_check(conn: AsyncConnection = Depends(get_db)):
    """
    健康检查端点，用于监控应用状态
    """
    # 测试数据库连接
    try:
        await conn.execute(text("SELECT 1"))
        db_status = "connected"
    except Exception:
        db_status = "disconnected"
    
    health_data = {
        "status": "ok" if db_status == "connected" else "degraded",
        "database": db_status,
        "api_version": "v1"
    }
    
    return success_response(data=health_data, message="系统运行正常")