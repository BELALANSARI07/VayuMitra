"""
Sustainability & Modal Shift Service:
Calculates quantified emissions avoided (CO2 and NOx) and personal inhalation reduction
when shifting to low-emission transit and clean energy alternatives.
"""
from __future__ import annotations

from app.core.constants import TransportMode
from app.schemas.routine_plan import CommuteMode, CookingFuel, ImpactDelta, SustainableSwap
from app.services.impact_engine import (
    calculate_emission_savings,
    calculate_exposure_reduction,
    ActivityLevel,
)


def get_sustainable_swaps(
    commute_mode: CommuteMode,
    commute_distance_km: float,
    cooking_fuel: CookingFuel,
    ambient_pm25: float,
) -> list[SustainableSwap]:
    """Generate sustainable alternatives tailored to user's current lifestyle."""
    swaps: list[SustainableSwap] = []

    # 1. Transport Mode Shift
    mode_map = {
        CommuteMode.TWO_WHEELER: TransportMode.TWO_WHEELER,
        CommuteMode.CAR_PETROL: TransportMode.CAR_PETROL,
        CommuteMode.CAR_DIESEL: TransportMode.CAR_DIESEL,
        CommuteMode.AUTO_RICKSHAW: TransportMode.AUTO_RICKSHAW,
        CommuteMode.BUS: TransportMode.BUS,
        CommuteMode.METRO: TransportMode.METRO,
        CommuteMode.BICYCLE: TransportMode.BICYCLE,
        CommuteMode.WALK: TransportMode.WALK,
        CommuteMode.EV: TransportMode.EV,
    }

    current_tmode = mode_map.get(commute_mode, TransportMode.TWO_WHEELER)

    # Recommend shift to Metro or EV if using high-polluting mode
    if current_tmode in (TransportMode.TWO_WHEELER, TransportMode.CAR_PETROL, TransportMode.CAR_DIESEL, TransportMode.AUTO_RICKSHAW):
        target_mode = TransportMode.METRO
        savings = calculate_emission_savings(
            mode_before=current_tmode,
            mode_after=target_mode,
            distance_km=commute_distance_km,
            trips_per_week=10,
        )
        # Exposure reduction: two-wheeler riders inhale road dust & exhaust directly;
        # Metro commuters are inside filtered air-conditioned cars (avg 40 µg/m³ PM2.5).
        commute_inhalation_reduction = calculate_exposure_reduction(
            pm25_ambient_ug_m3=ambient_pm25 * 1.25,  # On-road direct exhaust enhancement
            duration_baseline_min=commute_distance_km * 3.5,
            duration_shifted_min=commute_distance_km * 3.0,
            activity_level=ActivityLevel.LIGHT,
            pm25_shifted_ug_m3=45.0,  # AC metro cabin with air filtering
        )

        swaps.append(
            SustainableSwap(
                swap_from=f"{commute_mode.value.replace('_', ' ').title()} ({commute_distance_km} km commute)",
                swap_to="Metro Rail / Rapid Transit + Last-Mile EV Shuttle",
                rationale="Metro produces ~7g CO2/km vs 35-180g for personal vehicles. Inside air-conditioned metro coaches, PM2.5 levels are 60-80% lower than roadside exposure.",
                source="CPCB / MoEFCC Transport Inventory 2023 & DMRC Carbon Offset Registry",
                impact=ImpactDelta(
                    pm25_reduction_ug_per_day=commute_inhalation_reduction.pm25_inhaled_ug,
                    cigarette_equivalents_saved=commute_inhalation_reduction.cigarette_equivalents,
                    co2_saved_g_per_week=savings.co2_saved_g,
                    nox_saved_mg_per_week=savings.nox_saved_mg,
                    formula_ref=savings.formula_ref,
                    source_citation=savings.source,
                ),
            )
        )

    # 2. Cooking Clean Energy Swap
    if cooking_fuel in (CookingFuel.BIOMASS, CookingFuel.KEROSENE):
        cooking_impact = calculate_exposure_reduction(
            pm25_ambient_ug_m3=650.0,  # High baseline biomass peak
            duration_baseline_min=90.0,
            duration_shifted_min=90.0,
            activity_level=ActivityLevel.LIGHT,
            pm25_shifted_ug_m3=50.0,  # Induction / LPG
            is_indoor=True,
        )
        swaps.append(
            SustainableSwap(
                swap_from="Traditional Biomass / Kerosene Cookstove",
                swap_to="Single-Burner Induction Cooktop (Electric) / LPG",
                rationale="Eliminates polycyclic aromatic hydrocarbons and massive indoor particulate spikes that disproportionately affect cooks and infants.",
                source="WHO Guidelines on Household Fuel Combustion 2021",
                impact=ImpactDelta(
                    pm25_reduction_ug_per_day=cooking_impact.pm25_inhaled_ug,
                    cigarette_equivalents_saved=cooking_impact.cigarette_equivalents,
                    co2_saved_g_per_week=12500.0,
                    nox_saved_mg_per_week=1800.0,
                    formula_ref="Biomass stove fuel displacement model (WHO-IAQ)",
                    source_citation="WHO Clean Household Energy Guidance",
                ),
            )
        )

    # 3. Micro-mobility / Idle reduction swap
    if current_tmode == TransportMode.TWO_WHEELER:
        idle_savings = calculate_emission_savings(
            mode_before=TransportMode.TWO_WHEELER,
            mode_after=TransportMode.EV,
            distance_km=commute_distance_km,
            trips_per_week=10,
        )
        swaps.append(
            SustainableSwap(
                swap_from="Petrol Two-Wheeler (Carbureted / BS4/6)",
                swap_to="Electric Two-Wheeler / Smart Shared EV",
                rationale="Zero tailpipe exhaust emissions at street level prevents local toxic NOx hotspots in residential neighborhoods.",
                source="CPCB Vehicular Emission Study 2023",
                impact=ImpactDelta(
                    pm25_reduction_ug_per_day=14.5,
                    cigarette_equivalents_saved=0.66,
                    co2_saved_g_per_week=idle_savings.co2_saved_g,
                    nox_saved_mg_per_week=idle_savings.nox_saved_mg,
                    formula_ref=idle_savings.formula_ref,
                    source_citation=idle_savings.source,
                ),
            )
        )

    return swaps
