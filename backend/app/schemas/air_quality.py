from __future__ import annotations
from datetime import datetime
from pydantic import BaseModel, Field


class AirQualityRequest(BaseModel):
    """Query parameters for air quality lookup."""
    lat: float = Field(..., ge=-90.0, le=90.0, description="Latitude")
    lon: float = Field(..., ge=-180.0, le=180.0, description="Longitude")
    pincode: str | None = Field(None, max_length=10, pattern=r"^\d{4,10}$")
    city: str | None = Field(None, max_length=100)


class PollutantReading(BaseModel):
    name: str                           # "PM2.5", "PM10", "NO2", "SO2", "O3", "CO"
    value: float                        # µg/m³ or mg/m³ for CO
    unit: str = "µg/m³"
    cpcb_limit: float | None = None
    who_limit: float | None = None
    cpcb_multiplier: float | None = None
    who_multiplier: float | None = None
    status: str | None = None           # "Safe" | "Above WHO" | "Above CPCB (Unsafe)" | "Hazardous"
    primary_sources: str | None = None
    exceedance_health_effect: str | None = None


class HourlyForecast(BaseModel):
    hour: int = Field(..., ge=0, le=23)
    pm25: float
    pm10: float
    aqi_label: str                      # "Good", "Moderate", "Severe", etc.
    is_safe_window: bool                # True if AQI <= 100 (Satisfactory)


class HealthImpactData(BaseModel):
    category_label: str
    healthy_adults_impact: str
    sensitive_groups_impact: str
    short_term_risks: str
    long_term_risks: str
    red_flag_symptoms: list[str] = Field(default_factory=list)


class AtmosphericFactors(BaseModel):
    wind_speed_kmh: float
    humidity_pct: float
    temperature_c: float
    dispersion_verdict: str
    best_ventilation_window: str


class AirQualityResponse(BaseModel):
    location_label: str                 # "Delhi-NCR" or resolved city name
    lat: float
    lon: float
    timestamp: datetime
    aqi_value: int
    aqi_label: str
    aqi_color_hex: str
    primary_pollutant: str
    pollutants: list[PollutantReading]
    hourly_forecast_24h: list[HourlyForecast]
    best_safe_window: str               # e.g. "06:00–08:30" or "No safe window today"
    temperature_c: float | None = None
    humidity_pct: float | None = None
    wind_speed_kmh: float | None = None
    data_source: str                    # "open-meteo" | "waqi" | "cached"
    # Upgraded fields:
    overall_aqi: int | None = None
    dominant_pollutant: str | None = None
    cigarette_equivalent_24h: float | None = None
    health_impact: HealthImpactData | None = None
    atmospheric_factors: AtmosphericFactors | None = None
