"""
Deterministic Impact Engine — VayuMitra
All formulas grounded in published respiratory physiology and emission factors.
Zero LLM estimation — pure deterministic mathematical calculation.
"""
from __future__ import annotations
from dataclasses import dataclass
from enum import Enum

from app.core.constants import (
    MINUTE_VENTILATION_REST_L_MIN,         # 7.5 L/min (adult at rest)
    MINUTE_VENTILATION_LIGHT_EX_L_MIN,     # 24.0 L/min (light exercise / walking)
    MINUTE_VENTILATION_MODERATE_EX_L_MIN,  # 40.0 L/min (jogging / cycling)
    MINUTE_VENTILATION_CHILD_REST_L_MIN,   # 5.0 L/min (child 6-10 y at rest)
    PM25_DEPOSITION_FRACTION,              # 0.65 (alveolar deposition, ICRP 66)
    CIGARETTE_PM25_EQUIVALENT_UG,          # 22.0 µg inhaled ≈ 1 cigarette (Berkeley)
    INDOOR_OUTDOOR_RATIO_UNSEALED,         # 0.70 (typical unsealed Indian home)
    INDOOR_OUTDOOR_RATIO_SEALED,           # 0.30 (sealed windows + weatherstrip)
    DIY_BOX_FAN_FILTER_EFFICIENCY,         # 0.62 (CADR evaluations)
    EMISSION_FACTORS,                       # dict[TransportMode, g_CO2_per_km]
    NOX_FACTORS,                            # dict[TransportMode, mg_NOx_per_km]
    TransportMode,
)


class ActivityLevel(str, Enum):
    REST = "rest"
    LIGHT = "light"
    MODERATE = "moderate"


@dataclass(frozen=True, slots=True)
class ExposureResult:
    """Immutable result of an exposure calculation."""
    pm25_inhaled_ug: float          # Total PM2.5 inhaled reduction/avoided (µg)
    cigarette_equivalents: float    # PM2.5 in cigarette-equivalent units
    formula_ref: str                # Human-readable formula string
    source: str                     # Citation key (e.g. "ICRP-66, Berkeley-Equiv")


@dataclass(frozen=True, slots=True)
class EmissionResult:
    """Immutable result of an emission savings calculation."""
    co2_saved_g: float
    nox_saved_mg: float
    formula_ref: str
    source: str


def _ventilation_rate(level: ActivityLevel, is_child: bool = False) -> float:
    """Return minute ventilation in L/min based on activity level and age group."""
    if is_child:
        base = MINUTE_VENTILATION_CHILD_REST_L_MIN
        multipliers = {
            ActivityLevel.REST: 1.0,
            ActivityLevel.LIGHT: 2.4,
            ActivityLevel.MODERATE: 3.6,
        }
        return base * multipliers[level]

    rates = {
        ActivityLevel.REST: MINUTE_VENTILATION_REST_L_MIN,
        ActivityLevel.LIGHT: MINUTE_VENTILATION_LIGHT_EX_L_MIN,
        ActivityLevel.MODERATE: MINUTE_VENTILATION_MODERATE_EX_L_MIN,
    }
    return rates[level]


def calculate_exposure_reduction(
    pm25_ambient_ug_m3: float,
    duration_baseline_min: float,
    duration_shifted_min: float,
    activity_level: ActivityLevel,
    pm25_shifted_ug_m3: float | None = None,
    is_child: bool = False,
    is_indoor: bool = False,
    has_diy_filter: bool = False,
    home_sealed: bool = False,
) -> ExposureResult:
    """
    Calculate PM2.5 inhalation reduction when shifting activity timing,
    duration, location (outdoor -> indoor), or adding filtration.

    Formula:
        Inhaled PM2.5 (µg) = C_air (µg/m³) × V_dot (L/min) × t (min) × 0.001 (m³/L) × DF

    Where:
        C_air  = ambient concentration (adjusted for I/O ratio if indoor)
        V_dot  = minute ventilation for activity level
        t      = duration in minutes
        DF     = alveolar deposition fraction (0.65, ICRP Publication 66)
    """
    v_dot = _ventilation_rate(activity_level, is_child)

    # Baseline exposure (original timing, outdoor)
    baseline_inhaled = (
        pm25_ambient_ug_m3
        * v_dot
        * duration_baseline_min
        * 0.001
        * PM25_DEPOSITION_FRACTION
    )

    # Shifted exposure
    shifted_concentration = (
        pm25_shifted_ug_m3 if pm25_shifted_ug_m3 is not None else pm25_ambient_ug_m3
    )

    if is_indoor:
        io_ratio = INDOOR_OUTDOOR_RATIO_SEALED if home_sealed else INDOOR_OUTDOOR_RATIO_UNSEALED
        shifted_concentration = shifted_concentration * io_ratio
        if has_diy_filter:
            shifted_concentration *= (1.0 - DIY_BOX_FAN_FILTER_EFFICIENCY)

    shifted_inhaled = (
        shifted_concentration
        * v_dot
        * duration_shifted_min
        * 0.001
        * PM25_DEPOSITION_FRACTION
    )

    reduction = baseline_inhaled - shifted_inhaled
    cig_eq = reduction / CIGARETTE_PM25_EQUIVALENT_UG

    formula = (
        f"ΔPM2.5 = (C_base × t_base − C_shift × t_shift) × V̇ × 0.001 × DF | "
        f"C_base={pm25_ambient_ug_m3}, C_shift={shifted_concentration:.1f}, "
        f"V̇={v_dot}, t_base={duration_baseline_min}, t_shift={duration_shifted_min}, "
        f"DF={PM25_DEPOSITION_FRACTION}"
    )

    return ExposureResult(
        pm25_inhaled_ug=round(reduction, 2),
        cigarette_equivalents=round(cig_eq, 2),
        formula_ref=formula,
        source="ICRP Publication 66 (respiratory deposition); Berkeley Lab cigarette equivalence (22 µg/cig)",
    )


def calculate_emission_savings(
    mode_before: TransportMode,
    mode_after: TransportMode,
    distance_km: float,
    trips_per_week: int = 10,
) -> EmissionResult:
    """
    Calculate CO2 and NOx savings from switching transport modes.

    Formula:
        ΔCO2 (g) = (EF_before − EF_after) × distance × trips
        ΔNOx (mg) = (NF_before − NF_after) × distance × trips
    """
    co2_before = EMISSION_FACTORS[mode_before] * distance_km * trips_per_week
    co2_after = EMISSION_FACTORS[mode_after] * distance_km * trips_per_week
    nox_before = NOX_FACTORS[mode_before] * distance_km * trips_per_week
    nox_after = NOX_FACTORS[mode_after] * distance_km * trips_per_week

    formula = (
        f"ΔCO2 = (EF[{mode_before.value}] − EF[{mode_after.value}]) × {distance_km} km × {trips_per_week} trips | "
        f"EF_before={EMISSION_FACTORS[mode_before]}, EF_after={EMISSION_FACTORS[mode_after]}"
    )

    return EmissionResult(
        co2_saved_g=round(co2_before - co2_after, 2),
        nox_saved_mg=round(nox_before - nox_after, 2),
        formula_ref=formula,
        source="CPCB/MoEFCC India Transport Emission Inventory 2023",
    )


def cigarette_equivalents(pm25_inhaled_ug: float) -> float:
    """Convert total inhaled PM2.5 (µg) to cigarette equivalents."""
    return round(pm25_inhaled_ug / CIGARETTE_PM25_EQUIVALENT_UG, 2)
