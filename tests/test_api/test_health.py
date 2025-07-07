import pytest
from httpx import AsyncClient

from tests.conftest import client


@pytest.mark.asyncio
async def test_health_check(client):
    """测试健康检查端点"""
    async with AsyncClient(app=client.app, base_url="http://test") as ac:
        response = await ac.get("/api/health")
    
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["database"] == "connected"
    assert data["api_version"] == "v1" 