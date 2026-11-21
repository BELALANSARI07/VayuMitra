from __future__ import annotations
from enum import Enum
from pydantic import BaseModel, Field


class VulnerableGroup(str, Enum):
    ELDERLY = "elderly"
    CHILD = "child"
    ASTHMATIC = "asthmatic"
    PREGNANT = "pregnant"
    NONE = "none"


class CommuteMode(str, Enum):
    TWO_WHEELER = "two_wheeler"
    CAR_PETROL = "car_petrol"
    CAR_DIESEL = "car_diesel"
    AUTO_RICKSHAW = "auto_rickshaw"
    BUS = "bus"
    METRO = "metro"
    BICYCLE = "bicycle"
    WALK = "walk"
    EV = "ev"


class HomeType(str, Enum):
    APARTMENT_SEALED = "apartment_sealed"
    APARTMENT_UNSEALED = "apartment_unsealed"
    INDEPENDENT_HOUSE = "independent_house"
    KUTCHA = "kutcha"


class BudgetTier(str, Enum):
    FREE = "free"             # ₹0 — behavioral changes only
    LOW = "low"               # <= ₹500
    MEDIUM = "medium"         # <= ₹2,000
    HIGH = "high"             # <= ₹10,000+


class CookingFuel(str, Enum):
    LPG = "lpg"
    ELECTRIC = "electric"
    BIOMASS = "biomass"
    KEROSENE = "kerosene"


class PersonaInput(BaseModel):
    """Full persona configuration from the user."""
    lat: float = Field(..., ge=-90.0, le=90.0)
    lon: float = Field(..., ge=-180.0, le=180.0)
    pincode: str | None = Field(None, max_length=10, pattern=r"^\d{4,10}$")
    vulnerable_groups: list[VulnerableGroup] = Field(default=[VulnerableGroup.NONE], max_length=4)
    commute_mode: CommuteMode = CommuteMode.TWO_WHEELER
    commute_distance_km: float = Field(5.0, ge=0.1, le=200.0)
    home_type: HomeType = HomeType.APARTMENT_UNSEALED
    cooking_fuel: CookingFuel = CookingFuel.LPG
    budget_tier: BudgetTier = BudgetTier.LOW
    household_size: int = Field(4, ge=1, le=20)


class ImpactDelta(BaseModel):
    """Deterministic impact calculation result — never LLM-generated."""
    pm25_reduction_ug_per_day: float
    cigarette_equivalents_saved: float
    co2_saved_g_per_week: float | None = None
    nox_saved_mg_per_week: float | None = None
    formula_ref: str
    source_citation: str


class RoutineAction(BaseModel):
    time_slot: str                      # "Morning", "Afternoon", "Evening"
    action: str                         # Human-readable instruction
    rationale: str                      # Why this helps
    source: str                         # CPCB/WHO section reference
    impact: ImpactDelta


class IndoorHack(BaseModel):
    title: str
    description: str
    budget_tier: BudgetTier
    estimated_cost_inr: int
    effectiveness_pct: float            # e.g. 62.0 for DIY box fan filter
    source: str
    impact: ImpactDelta


class SustainableSwap(BaseModel):
    swap_from: str
    swap_to: str
    rationale: str
    source: str
    impact: ImpactDelta


class RoutinePlanResponse(BaseModel):
    location_label: str
    current_aqi: int
    aqi_label: str
    best_safe_window: str
    routines: list[RoutineAction]
    indoor_hacks: list[IndoorHack]
    sustainable_swaps: list[SustainableSwap]
    total_impact: ImpactDelta
    generated_at: str                   # ISO timestamp
