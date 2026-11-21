"""
Routine Plan Orchestrator Service:
Synthesizes live air quality data, persona vulnerability flags,
budget constraints, and transport modes into a complete actionable plan
with deterministic exposure & emission metrics.
"""
from __future__ import annotations

from datetime import datetime, timezone
import httpx

from app.core.cache import TTLCache
from app.schemas.routine_plan import (
    ImpactDelta,
    PersonaInput,
    RoutineAction,
    RoutinePlanResponse,
    VulnerableGroup,
)
from app.services.air_quality_service import fetch_air_quality
from app.services.impact_engine import (
    calculate_exposure_reduction,
    ActivityLevel,
)
from app.services.indoor_hack_service import get_budget_ranked_hacks
from app.services.rag_retriever import KnowledgeIndex
from app.services.sustainability_service import get_sustainable_swaps


async def generate_routine_plan(
    persona: PersonaInput,
    http_client: httpx.AsyncClient,
    cache: TTLCache,
    knowledge_index: KnowledgeIndex,
) -> RoutinePlanResponse:
    """Generate comprehensive, persona-tailored, quantified plan."""
    # 1. Fetch live or cached AQI
    aqi_data = await fetch_air_quality(
        lat=persona.lat,
        lon=persona.lon,
        pincode=persona.pincode,
        city=None,
        http_client=http_client,
        cache=cache,
    )

    ambient_pm25 = next(
        (p.value for p in aqi_data.pollutants if p.name == "PM2.5"),
        220.0,
    )

    is_vulnerable = any(
        g in (VulnerableGroup.CHILD, VulnerableGroup.ELDERLY, VulnerableGroup.ASTHMATIC, VulnerableGroup.PREGNANT)
        for g in persona.vulnerable_groups
    )
    has_child = VulnerableGroup.CHILD in persona.vulnerable_groups
    has_asthmatic = VulnerableGroup.ASTHMATIC in persona.vulnerable_groups

    # 2. Build time-shifted routines
    routines: list[RoutineAction] = []

    # Morning Routine
    # Shift outdoor activity away from 06:00-08:00 inversion peak to safe window (or indoor)
    morning_shift = calculate_exposure_reduction(
        pm25_ambient_ug_m3=ambient_pm25 * 1.2,  # Morning inversion spike
        duration_baseline_min=45.0,
        duration_shifted_min=45.0,
        activity_level=ActivityLevel.LIGHT,
        pm25_shifted_ug_m3=ambient_pm25 * 0.45,  # Shifted to safe window / indoor yoga
        is_child=has_child,
        is_indoor=True,
    )
    routines.append(
        RoutineAction(
            time_slot="Morning (06:00–10:00)",
            action="Shift morning walks or exercise indoors; avoid 06:00–08:30 ground-level smog peak.",
            rationale="Winter thermal inversions trap vehicular and biomass emissions closest to ground level at dawn. Light exercise during this period multiplies particulate inhalation by 3.2x.",
            source="ICRP-66 Respiratory Model & ICMR Smog Inversion Advisory 2023",
            impact=ImpactDelta(
                pm25_reduction_ug_per_day=morning_shift.pm25_inhaled_ug,
                cigarette_equivalents_saved=morning_shift.cigarette_equivalents,
                formula_ref=morning_shift.formula_ref,
                source_citation=morning_shift.source,
            ),
        )
    )

    # Afternoon Routine
    # Safe window utilization for essential errands or cross-ventilation
    afternoon_shift = calculate_exposure_reduction(
        pm25_ambient_ug_m3=ambient_pm25,
        duration_baseline_min=60.0,
        duration_shifted_min=60.0,
        activity_level=ActivityLevel.REST,
        pm25_shifted_ug_m3=ambient_pm25 * 0.65,  # Diurnal dispersion dip
        is_child=has_child,
        is_indoor=False,
    )
    routines.append(
        RoutineAction(
            time_slot="Afternoon (12:00–15:30)",
            action=f"Utilize the day's optimal dispersion window ({aqi_data.best_safe_window}) for outdoor errands or quick cross-ventilation.",
            rationale="Solar surface heating breaks the night-time boundary layer, temporarily diluting PM2.5 concentrations before evening calm sets in.",
            source="CPCB Diurnal Pollution Monitoring Studies & WHO AQG 2021",
            impact=ImpactDelta(
                pm25_reduction_ug_per_day=afternoon_shift.pm25_inhaled_ug,
                cigarette_equivalents_saved=afternoon_shift.cigarette_equivalents,
                formula_ref=afternoon_shift.formula_ref,
                source_citation=afternoon_shift.source,
            ),
        )
    )

    # Evening Routine
    # Cooking exhaust, window sealing, bedtime sanctuary
    evening_shift = calculate_exposure_reduction(
        pm25_ambient_ug_m3=ambient_pm25 * 1.15,
        duration_baseline_min=120.0,
        duration_shifted_min=120.0,
        activity_level=ActivityLevel.REST,
        pm25_shifted_ug_m3=ambient_pm25 * 0.35,  # Filtered / sealed bedroom
        is_child=has_child,
        is_indoor=True,
        home_sealed=True,
    )
    routines.append(
        RoutineAction(
            time_slot="Evening & Night (18:00–23:00)",
            action="Keep traffic-facing doors/windows sealed; run exhaust fan during cooking; seal bedroom before sleep.",
            rationale="Evening traffic rush hour combined with dropping temperatures traps fresh emissions. Overnight breathing in a sealed room prevents cumulative pulmonary inflammation.",
            source="WHO Guidelines on Household Fuel Combustion, §4 & Datta et al. 2020",
            impact=ImpactDelta(
                pm25_reduction_ug_per_day=evening_shift.pm25_inhaled_ug,
                cigarette_equivalents_saved=evening_shift.cigarette_equivalents,
                formula_ref=evening_shift.formula_ref,
                source_citation=evening_shift.source,
            ),
        )
    )

    # 3. Budget-Tiered Indoor Hacks
    indoor_hacks = get_budget_ranked_hacks(
        ambient_pm25=ambient_pm25,
        budget_tier=persona.budget_tier,
        home_type=persona.home_type,
        has_child=has_child,
    )

    # 4. Tailored Sustainable Swaps
    sustainable_swaps = get_sustainable_swaps(
        commute_mode=persona.commute_mode,
        commute_distance_km=persona.commute_distance_km,
        cooking_fuel=persona.cooking_fuel,
        ambient_pm25=ambient_pm25,
    )

    # 5. Aggregate Total Daily Impact (Deterministic sum)
    total_pm25_saved = sum(r.impact.pm25_reduction_ug_per_day for r in routines)
    if indoor_hacks:
        total_pm25_saved += indoor_hacks[0].impact.pm25_reduction_ug_per_day
    if sustainable_swaps:
        total_pm25_saved += sustainable_swaps[0].impact.pm25_reduction_ug_per_day

    total_cig_saved = round(total_pm25_saved / 22.0, 2)
    total_co2_saved = sum(s.impact.co2_saved_g_per_week or 0.0 for s in sustainable_swaps)
    total_nox_saved = sum(s.impact.nox_saved_mg_per_week or 0.0 for s in sustainable_swaps)

    total_impact = ImpactDelta(
        pm25_reduction_ug_per_day=round(total_pm25_saved, 2),
        cigarette_equivalents_saved=total_cig_saved,
        co2_saved_g_per_week=round(total_co2_saved, 1) if total_co2_saved > 0 else None,
        nox_saved_mg_per_week=round(total_nox_saved, 1) if total_nox_saved > 0 else None,
        formula_ref="Sum of deterministic time-shifted routine, indoor hack, and sustainable modal delta.",
        source_citation="ICRP-66 (alveolar deposition), Berkeley cigarette equivalence, CPCB/MoEFCC inventories",
    )

    return RoutinePlanResponse(
        location_label=aqi_data.location_label,
        current_aqi=aqi_data.aqi_value,
        aqi_label=aqi_data.aqi_label,
        best_safe_window=aqi_data.best_safe_window,
        routines=routines,
        indoor_hacks=indoor_hacks,
        sustainable_swaps=sustainable_swaps,
        total_impact=total_impact,
        generated_at=datetime.now(timezone.utc).isoformat(),
    )
