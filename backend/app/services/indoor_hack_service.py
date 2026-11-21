"""
Indoor Air Quality Hack Service:
Generates budget-tiered indoor interventions (sealing, DIY filtration, humidity/hygiene)
coupled with deterministic exposure reduction metrics.
"""
from __future__ import annotations

from app.core.constants import TransportMode
from app.schemas.routine_plan import BudgetTier, HomeType, IndoorHack, ImpactDelta
from app.services.impact_engine import (
    calculate_exposure_reduction,
    ActivityLevel,
)


def get_budget_ranked_hacks(
    ambient_pm25: float,
    budget_tier: BudgetTier,
    home_type: HomeType,
    has_child: bool = False,
) -> list[IndoorHack]:
    """Return prioritized indoor hacks matching user budget tier and home infiltration profile."""
    hacks: list[IndoorHack] = []

    # 1. Free Behavioral Hacks (Always applicable)
    wet_mop_impact = calculate_exposure_reduction(
        pm25_ambient_ug_m3=ambient_pm25,
        duration_baseline_min=180.0,
        duration_shifted_min=180.0,
        activity_level=ActivityLevel.REST,
        pm25_shifted_ug_m3=ambient_pm25 * 0.82,  # 18% reduction from avoiding resuspension
        is_child=has_child,
        is_indoor=True,
    )
    hacks.append(
        IndoorHack(
            title="Wet-Mopping & Microfiber Cleaning (No Dry Sweeping)",
            description="Replace dry brooms with damp microfiber mopping once daily. Dry brooms resuspend toxic heavy metal particulates into breathing zones for 2-4 hours.",
            budget_tier=BudgetTier.FREE,
            estimated_cost_inr=0,
            effectiveness_pct=18.0,
            source="WHO Indoor Air Quality Guidelines / ICMR IAQ Protocol 2023",
            impact=ImpactDelta(
                pm25_reduction_ug_per_day=wet_mop_impact.pm25_inhaled_ug,
                cigarette_equivalents_saved=wet_mop_impact.cigarette_equivalents,
                formula_ref=wet_mop_impact.formula_ref,
                source_citation=wet_mop_impact.source,
            ),
        )
    )

    exhaust_timing_impact = calculate_exposure_reduction(
        pm25_ambient_ug_m3=ambient_pm25,
        duration_baseline_min=60.0,
        duration_shifted_min=60.0,
        activity_level=ActivityLevel.LIGHT,
        pm25_shifted_ug_m3=ambient_pm25 * 0.70,  # 30% reduction in kitchen spillover
        is_child=has_child,
        is_indoor=True,
    )
    hacks.append(
        IndoorHack(
            title="Timed Kitchen Exhaust & Lidded Cooking",
            description="Run the kitchen exhaust fan during all frying/tadka cooking and keep it active for 15 minutes post-cooking with kitchen doors closed.",
            budget_tier=BudgetTier.FREE,
            estimated_cost_inr=0,
            effectiveness_pct=30.0,
            source="WHO Guidelines on Household Fuel Combustion, p. 29",
            impact=ImpactDelta(
                pm25_reduction_ug_per_day=exhaust_timing_impact.pm25_inhaled_ug,
                cigarette_equivalents_saved=exhaust_timing_impact.cigarette_equivalents,
                formula_ref=exhaust_timing_impact.formula_ref,
                source_citation=exhaust_timing_impact.source,
            ),
        )
    )

    # 2. Low Budget Hacks (<= ₹500)
    if budget_tier in (BudgetTier.LOW, BudgetTier.MEDIUM, BudgetTier.HIGH):
        sealing_impact = calculate_exposure_reduction(
            pm25_ambient_ug_m3=ambient_pm25,
            duration_baseline_min=360.0,
            duration_shifted_min=360.0,
            activity_level=ActivityLevel.REST,
            is_child=has_child,
            is_indoor=True,
            home_sealed=True,
        )
        hacks.append(
            IndoorHack(
                title="Door & Window Gap Weatherstripping Tape",
                description="Apply self-adhesive EPDM rubber or foam sealing tape (10m roll) along window seams and door bottom sweeps to block smog infiltration drafts.",
                budget_tier=BudgetTier.LOW,
                estimated_cost_inr=220,
                effectiveness_pct=52.0,
                source="Datta et al. 2020 / CSIR-NEERI Infiltration Study",
                impact=ImpactDelta(
                    pm25_reduction_ug_per_day=sealing_impact.pm25_inhaled_ug,
                    cigarette_equivalents_saved=sealing_impact.cigarette_equivalents,
                    formula_ref=sealing_impact.formula_ref,
                    source_citation=sealing_impact.source,
                ),
            )
        )

        diy_filter_impact = calculate_exposure_reduction(
            pm25_ambient_ug_m3=ambient_pm25,
            duration_baseline_min=360.0,
            duration_shifted_min=360.0,
            activity_level=ActivityLevel.REST,
            is_child=has_child,
            is_indoor=True,
            has_diy_filter=True,
            home_sealed=home_type == HomeType.APARTMENT_SEALED,
        )
        hacks.append(
            IndoorHack(
                title="DIY MERV-13 Box Fan / Table Fan Filter Hack",
                description="Attach a 16x16 or 20x20 inch MERV-13 pleated AC/furnace filter sheet to the intake of an existing table or box fan using binder clips or masking tape.",
                budget_tier=BudgetTier.LOW,
                estimated_cost_inr=480,
                effectiveness_pct=62.0,
                source="Smart Air / CADR Field Evaluations 2022",
                impact=ImpactDelta(
                    pm25_reduction_ug_per_day=diy_filter_impact.pm25_inhaled_ug,
                    cigarette_equivalents_saved=diy_filter_impact.cigarette_equivalents,
                    formula_ref=diy_filter_impact.formula_ref,
                    source_citation=diy_filter_impact.source,
                ),
            )
        )

    # 3. Medium / High Budget Hacks (<= ₹2,000 to ₹10,000+)
    if budget_tier in (BudgetTier.MEDIUM, BudgetTier.HIGH):
        hepa_impact = calculate_exposure_reduction(
            pm25_ambient_ug_m3=ambient_pm25,
            duration_baseline_min=480.0,
            duration_shifted_min=480.0,
            activity_level=ActivityLevel.REST,
            is_child=has_child,
            is_indoor=True,
            pm25_shifted_ug_m3=20.0,  # True HEPA bedroom target
            home_sealed=True,
        )
        hacks.append(
            IndoorHack(
                title="True HEPA H13 Bedroom Clean Air Sanctuary",
                description="Deploy a certified True HEPA H13 filtration unit (CADR > 200 m³/h) in the primary bedroom with all windows closed during overnight sleeping hours.",
                budget_tier=BudgetTier.MEDIUM,
                estimated_cost_inr=1950,
                effectiveness_pct=88.0,
                source="WHO Air Quality Guidelines 2021 / US EPA IAQ Guidance",
                impact=ImpactDelta(
                    pm25_reduction_ug_per_day=hepa_impact.pm25_inhaled_ug,
                    cigarette_equivalents_saved=hepa_impact.cigarette_equivalents,
                    formula_ref=hepa_impact.formula_ref,
                    source_citation=hepa_impact.source,
                ),
            )
        )

    return hacks
