"""
Integration tests for POST /api/routine-plan
"""
import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app


@pytest.fixture
async def client():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac


@pytest.mark.anyio
async def test_create_routine_plan_delhi_success(client: AsyncClient):
    payload = {
        "lat": 28.6139,
        "lon": 77.2090,
        "vulnerable_groups": ["child", "asthmatic"],
        "commute_mode": "two_wheeler",
        "commute_distance_km": 8.0,
        "home_type": "apartment_unsealed",
        "cooking_fuel": "lpg",
        "budget_tier": "low",
        "household_size": 4,
    }
    response = await client.post("/api/routine-plan", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "current_aqi" in data
    assert "routines" in data
    assert len(data["routines"]) == 3  # Morning, Afternoon, Evening
    assert "indoor_hacks" in data
    assert len(data["indoor_hacks"]) >= 2
    assert "sustainable_swaps" in data
    assert len(data["sustainable_swaps"]) >= 1
    assert "total_impact" in data

    # Verify deterministic impact math is populated
    total = data["total_impact"]
    assert total["pm25_reduction_ug_per_day"] > 0
    assert total["cigarette_equivalents_saved"] > 0
    assert total["co2_saved_g_per_week"] is not None
    assert "ICRP-66" in total["source_citation"]
