from __future__ import annotations

from fastapi import APIRouter, Query, Request

from app.core.security import validate_coordinates
from app.schemas.air_quality import AirQualityResponse
from app.services.air_quality_service import fetch_air_quality

router = APIRouter()


@router.get("/air-quality", response_model=AirQualityResponse)
async def get_air_quality(
    request: Request,
    lat: float = Query(..., ge=-90.0, le=90.0, description="Latitude"),
    lon: float = Query(..., ge=-180.0, le=180.0, description="Longitude"),
    pincode: str | None = Query(None, max_length=10, pattern=r"^\d{4,10}$"),
    city: str | None = Query(None, max_length=100),
) -> AirQualityResponse:
    """
    Fetch live air quality data, 24h pollutant timeline, and optimal ventilation window.
    Features 15-minute TTL caching and graceful offline fallback.
    """
    lat, lon = validate_coordinates(lat, lon)

    return await fetch_air_quality(
        lat=lat,
        lon=lon,
        pincode=pincode,
        city=city,
        http_client=request.app.state.http_client,
        cache=request.app.state.aqi_cache,
    )
