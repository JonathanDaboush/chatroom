
import pytest
from httpx import AsyncClient

# Placeholder FastAPI app for testing
from fastapi import FastAPI
app = FastAPI()

@pytest.mark.asyncio
async def test_health_async():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}