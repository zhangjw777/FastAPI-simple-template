from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.schemas.health import HealthResponse

router = APIRouter()


@router.get("", response_model=HealthResponse)
async def health_check(db: AsyncSession = Depends(get_db)):
    """
    健康检查端点，用于监控应用状态
    """
    return {
        "status": "ok",
        "database": "connected",
        "api_version": "v1"
    } 