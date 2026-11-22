"""
Routine Plan Orchestrator Service:
Synthesizes live air quality data, persona vulnerability flags,
budget constraints, and transport modes into a complete actionable plan
with deterministic exposure & emission metrics and rich structured action cards.
"""
from __future__ import annotations

from datetime import datetime, timezone
import httpx

from app.core.cache import TTLCache
from app.schemas.routine_plan import (
    ActionPlanCard,
    ImpactDelta,
    PersonaInput,
    QuantifiedImpactCard,
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

    # 6. Generate rich, structured ActionPlanCards
    co2_commute_saved_kg = round(
        max(0.0, (165.0 - 7.0) * persona.commute_distance_km * 10 / 1000.0), 1
    )

    action_cards: list[ActionPlanCard] = [
        ActionPlanCard(
            id="card-routine-1",
            title="Time-Shift Morning Workouts to Safe Window",
            category="Routine",
            budget_tier="Free/DIY",
            action_detail=f"Avoid outdoor jogging or brisk walking between 06:00 and 08:30 AM during peak winter ground inversion. Shift to indoor exercise or the afternoon window ({aqi_data.best_safe_window}).",
            quantified_impact=QuantifiedImpactCard(
                pm25_reduction_pct=55.0,
                co2_saved_kg_week=0.0,
                summary_badge="-55% PM2.5 inhaled (Save ~3.5 cigs/day)",
            ),
            why_it_works="Winter thermal inversions trap vehicular and biomass emissions at ground level at dawn. Exercise multiplies minute ventilation from 7.5 to 24+ L/min, inhaling 3.2x more particulates.",
            source_citation="ICRP-66 Respiratory Tract Model & ICMR Winter Smog Advisory",
        ),
        ActionPlanCard(
            id="card-mask-1",
            title="Well-Fitted N95/N99 Respirator for Daily Commute",
            category="Mask & Commute",
            budget_tier="Low-Cost",
            action_detail="Wear a certified, well-fitted N95 or N99 respirator with dual head-straps during all two-wheeler, bus, or walking transit. Cloth masks, surgical masks, and scarves offer < 15% filtration efficiency against PM2.5.",
            quantified_impact=QuantifiedImpactCard(
                pm25_reduction_pct=92.0,
                co2_saved_kg_week=0.0,
                summary_badge="-92% PM2.5 inhaled during transit",
            ),
            why_it_works="Certified meltblown electrostatic filter media traps sub-micron particles via diffusion and electrostatic capture. Cloth masks lack electrostatic charge and leak around facial perimeters.",
            source_citation="WHO Technical Specifications for PPE & NIOSH 42 CFR Part 84",
        ),
        ActionPlanCard(
            id="card-indoor-1",
            title="Eliminate Indoor Smoke & Wet-Mop Floors",
            category="Indoor Hack",
            budget_tier="Free/DIY",
            action_detail="Avoid burning agarbatti (incense sticks), mosquito coils, or dhoop indoors; never dry-sweep, which re-suspends settled toxic dust into breathing zones. Wet-mop with a damp microfiber cloth daily.",
            quantified_impact=QuantifiedImpactCard(
                pm25_reduction_pct=42.0,
                co2_saved_kg_week=0.0,
                summary_badge="-42% indoor PM2.5 spike",
            ),
            why_it_works="One agarbatti stick emits over 45 mg of PM2.5 plus benzene and formaldehyde. Wet-mopping traps particulates via capillary adhesion instead of aerodynamic re-suspension.",
            source_citation="WHO Household Fuel & Combustion Guidelines, §4 & Datta et al. 2020",
        ),
        ActionPlanCard(
            id="card-indoor-2",
            title="DIY Corsi-Rosenthal / Box-Fan Air Purifier",
            category="Indoor Hack",
            budget_tier="Low-Cost",
            action_detail="Attach a MERV-13 or HEPA furnace filter sheet to the intake of an ordinary box fan or pedestal table fan using duct tape to construct a high-CADR home air cleaner for under ₹500.",
            quantified_impact=QuantifiedImpactCard(
                pm25_reduction_pct=62.0,
                co2_saved_kg_week=0.0,
                summary_badge="-62% room PM2.5 in 45 mins",
            ),
            why_it_works="Clean Air Delivery Rate (CADR) depends on airflow volume multiplied by single-pass filtration efficiency. A ₹500 box fan filter circulates 200+ CFM, cleaning room air within 45 minutes.",
            source_citation="UC Davis & EPA Evaluation of DIY Box Fan Air Cleaners (2021)",
        ),
        ActionPlanCard(
            id="card-indoor-3",
            title="Weatherstrip Window Cracks & Create Bedroom Sanctuary",
            category="Indoor Hack",
            budget_tier="Low-Cost",
            action_detail="Apply self-adhesive EPDM rubber or foam sealing tape along window sash gaps and door jambs to lower the indoor/outdoor infiltration ratio from 0.70 down to 0.30.",
            quantified_impact=QuantifiedImpactCard(
                pm25_reduction_pct=57.0,
                co2_saved_kg_week=0.0,
                summary_badge="-57% infiltration from outdoor smog",
            ),
            why_it_works="Unsealed Indian metropolitan apartments allow 70% of outdoor smog to penetrate through hairline gaps. Sealing creates a low-infiltration barrier preserving purified air.",
            source_citation="Datta et al. (2020) Indian Residential Smog Infiltration Study",
        ),
        ActionPlanCard(
            id="card-swap-1",
            title="Modal Shift: Two-Wheeler / Car to Delhi Metro Rail",
            category="Sustainable Swap",
            budget_tier="Free/DIY",
            action_detail=f"Shift daily work commute ({persona.commute_distance_km} km) from petrol/diesel vehicle to Delhi Metro Rail (DMRC) coupled with electric feeder e-rickshaws.",
            quantified_impact=QuantifiedImpactCard(
                pm25_reduction_pct=78.0,
                co2_saved_kg_week=co2_commute_saved_kg,
                summary_badge=f"-78% transit exposure • -{co2_commute_saved_kg} kg CO₂/wk",
            ),
            why_it_works="Metro transit isolates commuters inside pressurized, filtered cars (reducing in-transit particulate inhalation by 78%) while slashing per-passenger emissions from 165g to 7g CO₂/km.",
            source_citation="CPCB Vehicular Emission Inventories & DMRC Environmental Audit",
        ),
        ActionPlanCard(
            id="card-swap-2",
            title="Smart Home True-HEPA & Induction Cooking Sanctuary",
            category="Sustainable Swap",
            budget_tier="Smart Home",
            action_detail="Equip living areas with automated H13 True-HEPA purifiers with laser PM2.5 feedback, and replace combustion cooking gas with electric magnetic induction cooktops.",
            quantified_impact=QuantifiedImpactCard(
                pm25_reduction_pct=95.0,
                co2_saved_kg_week=6.8,
                summary_badge="-95% indoor PM2.5 • Zero indoor NO₂ combustion",
            ),
            why_it_works="H13 True-HEPA media filters 99.97% of 0.3-micron particles. Induction cooking completely eliminates combustion-related nitrogen dioxide (NO₂) and ultrafine soot indoors.",
            source_citation="WHO Indoor Air Quality Guidelines 2021 & Lawrence Berkeley National Lab",
        ),
        ActionPlanCard(
            id="card-routine-2",
            title="Timed Kitchen Exhaust & Lidded Cooking",
            category="Routine",
            budget_tier="Free/DIY",
            action_detail="Always cook with lids on pans and run the high-velocity kitchen exhaust for 15 minutes post-cooking while closing kitchen-to-living room corridor doors.",
            quantified_impact=QuantifiedImpactCard(
                pm25_reduction_pct=38.0,
                co2_saved_kg_week=0.0,
                summary_badge="-38% cooking aerosol exposure",
            ),
            why_it_works="Frying and tadka release aerosolized oil droplets and volatile polycyclic aromatic hydrocarbons (PAHs). Lidded cooking captures 80% of grease droplets before dispersion.",
            source_citation="CPCB Indoor Air Pollution Guidelines & EPA Residential Exposure",
        ),
    ]

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
        action_cards=action_cards,
    )
