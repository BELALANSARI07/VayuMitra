"""
Centralized constants — no magic numbers anywhere else in the codebase.
Every value carries an explicit reference citing its scientific/policy source.
"""
from __future__ import annotations
from enum import Enum


# --- Respiratory Physiology (ICRP Publication 66, 1994 & EPA Exposure Factors Handbook) ---
MINUTE_VENTILATION_REST_L_MIN: float = 7.5           # Adult sitting/resting (L/min)
MINUTE_VENTILATION_LIGHT_EX_L_MIN: float = 24.0      # Walking 4-5 km/h / light chores (L/min)
MINUTE_VENTILATION_MODERATE_EX_L_MIN: float = 40.0    # Jogging / brisk cycling (L/min)
MINUTE_VENTILATION_CHILD_REST_L_MIN: float = 5.0      # Child 6-10 years at rest (L/min)
PM25_DEPOSITION_FRACTION: float = 0.65                # Alveolar deposition fraction (ICRP 66)

# --- Cigarette Equivalence (Berkeley Lab / Apte et al. 2015 / Muller & Muller 2018) ---
CIGARETTE_PM25_EQUIVALENT_UG: float = 22.0            # 22.0 µg PM2.5 inhaled ≈ 1 cigarette

# --- Indoor/Outdoor Infiltration Ratios (Datta et al. 2020, Indian residential environments) ---
INDOOR_OUTDOOR_RATIO_UNSEALED: float = 0.70          # Unsealed windows/doors in Indian metros
INDOOR_OUTDOOR_RATIO_SEALED: float = 0.30            # Weather-stripped, foam-sealed windows

# --- DIY Filtration Efficiency (Huang et al. / Smart Air CADR field evaluations) ---
DIY_BOX_FAN_FILTER_EFFICIENCY: float = 0.62           # 62% single-pass PM2.5 reduction

# --- National Air Quality Index (NAQI) Bands (CPCB India Standard) ---
AQI_BANDS: list[dict[str, object]] = [
    {"label": "Good",         "min": 0,   "max": 50,  "color_hex": "#15803D", "outdoor_advice": "Enjoy outdoor activities freely."},
    {"label": "Satisfactory", "min": 51,  "max": 100, "color_hex": "#65A30D", "outdoor_advice": "Minor breathing discomfort to sensitive people."},
    {"label": "Moderate",     "min": 101, "max": 200, "color_hex": "#A16207", "outdoor_advice": "Limit prolonged outdoor exertion for asthmatics/children."},
    {"label": "Poor",         "min": 201, "max": 300, "color_hex": "#C2410C", "outdoor_advice": "Shift outdoor activities to lowest-AQI time window."},
    {"label": "Very Poor",    "min": 301, "max": 400, "color_hex": "#DC2626", "outdoor_advice": "Avoid outdoor exertion. Wear N95 respirator if commuting."},
    {"label": "Severe",       "min": 401, "max": 500, "color_hex": "#7C3AED", "outdoor_advice": "Stay indoors. Seal openings. Run filtration."},
]


class TransportMode(str, Enum):
    TWO_WHEELER = "two_wheeler"
    CAR_PETROL = "car_petrol"
    CAR_DIESEL = "car_diesel"
    AUTO_RICKSHAW = "auto_rickshaw"
    BUS = "bus"
    METRO = "metro"
    BICYCLE = "bicycle"
    WALK = "walk"
    EV = "ev"


# --- Transport Emission Factors (CPCB / MoEFCC India Transport Inventories, g CO2/km) ---
EMISSION_FACTORS: dict[TransportMode, float] = {
    TransportMode.TWO_WHEELER:   35.0,
    TransportMode.CAR_PETROL:   165.0,
    TransportMode.CAR_DIESEL:   180.0,
    TransportMode.AUTO_RICKSHAW: 60.0,
    TransportMode.BUS:           20.0,   # Per passenger-km (average transit occupancy)
    TransportMode.METRO:          7.0,   # Per passenger-km (Delhi Metro DMRC inventory)
    TransportMode.BICYCLE:        0.0,
    TransportMode.WALK:           0.0,
    TransportMode.EV:            25.0,   # Grid-average India 2024
}

# --- NOx Emission Factors (CPCB India Vehicular Emission Studies, mg NOx/km) ---
NOX_FACTORS: dict[TransportMode, float] = {
    TransportMode.TWO_WHEELER:   120.0,
    TransportMode.CAR_PETROL:    45.0,
    TransportMode.CAR_DIESEL:   400.0,
    TransportMode.AUTO_RICKSHAW: 200.0,
    TransportMode.BUS:            30.0,
    TransportMode.METRO:           2.0,
    TransportMode.BICYCLE:         0.0,
    TransportMode.WALK:            0.0,
    TransportMode.EV:              0.0,
}

# --- Cache Configuration ---
AQI_CACHE_TTL_SECONDS: int = 900          # 15 minutes
GEOHASH_PRECISION: int = 5                # ~4.9 km x 4.9 km grid resolution

# --- Rate Limiting Defaults ---
RATE_LIMIT_CHAT_PER_MIN: int = 12         # Per client IP
RATE_LIMIT_DEFAULT_PER_MIN: int = 60      # Per client IP

# --- Input Constraints ---
MAX_CHAT_MESSAGE_LENGTH: int = 1_000      # Characters
MAX_PINCODE_LENGTH: int = 10
MAX_CITY_NAME_LENGTH: int = 100
MAX_LLM_OUTPUT_TOKENS: int = 1_024

# --- Demo Presets (Delhi-NCR, Noida, Gurugram) ---
DEMO_PRESETS: list[dict[str, object]] = [
    {"label": "Delhi-NCR",  "pincode": "110001", "lat": 28.6139, "lon": 77.2090, "city": "New Delhi"},
    {"label": "Noida",      "pincode": "201301", "lat": 28.5355, "lon": 77.3910, "city": "Noida"},
    {"label": "Gurugram",   "pincode": "122001", "lat": 28.4595, "lon": 77.0266, "city": "Gurugram"},
]
