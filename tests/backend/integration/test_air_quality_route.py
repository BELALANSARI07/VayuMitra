"""
Integration tests for GET /api/air-quality
"""
import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app


@pytest.fixture
async def client():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac


@pytest.mark.anyio
async def test_get_air_quality_delhi_success(client: AsyncClient):
    response = await client.get("/api/air-quality", params={"lat": 28.6139, "lon": 77.2090, "city": "Delhi"})
    assert response.status_code == 200
    data = response.json()
    assert "aqi_value" in data
    assert "aqi_label" in data
    assert "pollutants" in data
    assert "hourly_forecast_24h" in data
    assert "best_safe_window" in data
    assert len(data["hourly_forecast_24h"]) == 24
    assert data["location_label"] == "Delhi"


@pytest.mark.anyio
async def test_get_air_quality_invalid_coordinates(client: AsyncClient):
    response = await client.get("/api/air-quality", params={"lat": 120.0, "lon": 77.2090})
    # Validation error (coordinates out of range)
    assert response.status_code == 422 or response.status_code == 400


@pytest.mark.anyio
async def test_health_check(client: AsyncClient):
    response = await client.get("/api/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"
