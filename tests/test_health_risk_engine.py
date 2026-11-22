"""
Unit tests for Health Risk Engine, CPCB/WHO safe limit multipliers,
Berkeley cigarette equivalents, dynamic AQI band clinical impact mappings,
and Air Quality / Routine Plan schema validation.
"""
import pytest
from app.services.health_risk_engine import (
    analyze_pollutant,
    assess_atmospheric_factors,
    map_cpcb_aqi_health_impact,
    pm25_to_cigarettes_24h,
)
from app.schemas.air_quality import (
    AirQualityResponse,
    AtmosphericFactors,
    HealthImpactData,
    HourlyForecast,
    PollutantReading,
)
from app.schemas.routine_plan import (
    ActionPlanCard,
    ImpactDelta,
    PersonaInput,
    QuantifiedImpactCard,
    RoutinePlanResponse,
)
from datetime import datetime, timezone


class TestCigaretteEquivalents:
    def test_berkeley_earth_standard_value(self):
        """22 µg/m³ for 24 hours equals 1 cigarette."""
        assert pm25_to_cigarettes_24h(22.0) == 1.0

    def test_delhi_severe_smog_value(self):
        """270 µg/m³ equals 12.3 cigarettes."""
        assert pm25_to_cigarettes_24h(270.0) == 12.3

    def test_zero_and_negative_input(self):
        """Negative or zero values should return 0.0."""
        assert pm25_to_cigarettes_24h(0.0) == 0.0
        assert pm25_to_cigarettes_24h(-15.0) == 0.0


class TestPollutantAnalysis:
    def test_pm25_safe_level(self):
        res = analyze_pollutant("PM2.5", 15.0)
        assert res["status"] == "Safe"
        assert res["who_multiplier"] == 1.0
        assert res["cpcb_multiplier"] == 0.2  # 15/60 = 0.25 -> 0.2 or 0.3 depending on float

    def test_pm25_above_who(self):
        res = analyze_pollutant("PM2.5", 50.0)
        assert res["status"] == "Above WHO"
        assert res["who_multiplier"] == 3.3
        assert res["cpcb_multiplier"] == 0.8

    def test_pm25_above_cpcb(self):
        res = analyze_pollutant("PM2.5", 100.0)
        assert res["status"] == "Above CPCB (Unsafe)"
        assert res["cpcb_multiplier"] == 1.7
        assert res["who_multiplier"] == 6.7

    def test_pm25_hazardous(self):
        res = analyze_pollutant("PM2.5", 270.0)
        assert res["status"] == "Hazardous"
        assert res["cpcb_multiplier"] == 4.5
        assert res["who_multiplier"] == 18.0
        assert "alveolar" in res["exceedance_health_effect"].lower()
        assert "Vehicles" in res["primary_sources"]

    def test_all_six_pollutants_coverage(self):
        for pol in ["PM2.5", "PM10", "NO2", "SO2", "O3", "CO"]:
            res = analyze_pollutant(pol, 50.0)
            assert res["name"] is not None
            assert res["unit"] is not None
            assert res["status"] in ["Safe", "Above WHO", "Above CPCB (Unsafe)", "Hazardous"]
            assert res["cpcb_limit"] > 0
            assert res["who_limit"] > 0


class TestCpcbAqiBandMappings:
    def test_all_six_official_bands(self):
        # 1. Good (0-50)
        good = map_cpcb_aqi_health_impact(30)
        assert good["category_label"] == "Good"
        assert len(good["red_flag_symptoms"]) == 0

        # 2. Satisfactory (51-100)
        sat = map_cpcb_aqi_health_impact(75)
        assert sat["category_label"] == "Satisfactory"

        # 3. Moderate (101-200)
        mod = map_cpcb_aqi_health_impact(150)
        assert mod["category_label"] == "Moderate"

        # 4. Poor (201-300)
        poor = map_cpcb_aqi_health_impact(250)
        assert poor["category_label"] == "Poor"

        # 5. Very Poor (301-400)
        vpoor = map_cpcb_aqi_health_impact(350)
        assert vpoor["category_label"] == "Very Poor"

        # 6. Severe (401-500+)
        sev = map_cpcb_aqi_health_impact(450)
        assert sev["category_label"] == "Severe"
        assert "Persistent cough" in sev["red_flag_symptoms"]
        assert "Breathlessness" in sev["red_flag_symptoms"]
        assert "Chest discomfort" in sev["red_flag_symptoms"]
        assert "Giddiness" in sev["red_flag_symptoms"]
        assert "Red/watery eyes" in sev["red_flag_symptoms"]


class TestAtmosphericFactors:
    def test_calm_wind_stagnation(self):
        res = assess_atmospheric_factors(wind_speed_kmh=4.0, humidity_pct=85.0, temp_c=14.0)
        assert "Stagnant" in res["dispersion_verdict"]
        assert "1:00 PM – 4:00 PM" in res["best_ventilation_window"]

    def test_moderate_dispersion(self):
        res = assess_atmospheric_factors(wind_speed_kmh=10.0)
        assert "Moderate" in res["dispersion_verdict"]

    def test_active_dispersion(self):
        res = assess_atmospheric_factors(wind_speed_kmh=22.0)
        assert "Active" in res["dispersion_verdict"]


class TestSchemaValidation:
    def test_air_quality_response_schema(self):
        res = AirQualityResponse(
            location_label="Delhi-NCR",
            lat=28.6139,
            lon=77.2090,
            timestamp=datetime.now(timezone.utc),
            aqi_value=426,
            aqi_label="Severe",
            aqi_color_hex="#7C3AED",
            primary_pollutant="PM2.5",
            pollutants=[
                PollutantReading(
                    name="PM2.5",
                    value=270.0,
                    unit="µg/m³",
                    cpcb_limit=60.0,
                    who_limit=15.0,
                    cpcb_multiplier=4.5,
                    who_multiplier=18.0,
                    status="Hazardous",
                    primary_sources="Vehicles",
                    exceedance_health_effect="Penetrates deep into alveolar tissues",
                )
            ],
            hourly_forecast_24h=[
                HourlyForecast(hour=14, pm25=120.0, pm10=180.0, aqi_label="Poor", is_safe_window=False)
            ],
            best_safe_window="13:00–15:00",
            data_source="open-meteo",
            overall_aqi=426,
            dominant_pollutant="PM2.5",
            cigarette_equivalent_24h=12.3,
            health_impact=HealthImpactData(
                category_label="Severe",
                healthy_adults_impact="Severe impact",
                sensitive_groups_impact="Emergency condition",
                short_term_risks="Acute lower respiratory tract infections",
                long_term_risks="Permanent reduction in lung capacity",
                red_flag_symptoms=["Persistent cough", "Breathlessness"],
            ),
            atmospheric_factors=AtmosphericFactors(
                wind_speed_kmh=5.2,
                humidity_pct=76.0,
                temperature_c=16.5,
                dispersion_verdict="Stagnant air (< 6 km/h wind)",
                best_ventilation_window="1:00 PM – 4:00 PM",
            ),
        )
        assert res.overall_aqi == 426
        assert res.cigarette_equivalent_24h == 12.3
        assert res.health_impact.category_label == "Severe"
        assert len(res.health_impact.red_flag_symptoms) == 2

    def test_routine_plan_response_with_action_cards(self):
        plan = RoutinePlanResponse(
            location_label="Delhi-NCR",
            current_aqi=380,
            aqi_label="Very Poor",
            best_safe_window="13:00–15:00",
            routines=[],
            indoor_hacks=[],
            sustainable_swaps=[],
            total_impact=ImpactDelta(
                pm25_reduction_ug_per_day=140.5,
                cigarette_equivalents_saved=6.4,
                formula_ref="Deterministic ICRP-66",
                source_citation="WHO AQG 2021",
            ),
            generated_at=datetime.now(timezone.utc).isoformat(),
            action_cards=[
                ActionPlanCard(
                    id="card-mask-1",
                    title="N95 Respirator",
                    category="Mask & Commute",
                    budget_tier="Low-Cost",
                    action_detail="Wear certified N95 during commute",
                    quantified_impact=QuantifiedImpactCard(
                        pm25_reduction_pct=92.0,
                        co2_saved_kg_week=0.0,
                        summary_badge="-92% PM2.5 inhaled",
                    ),
                    why_it_works="Electrostatic meltblown media",
                    source_citation="NIOSH 42 CFR 84",
                )
            ],
        )
        assert len(plan.action_cards) == 1
        assert plan.action_cards[0].category == "Mask & Commute"
        assert plan.action_cards[0].quantified_impact.pm25_reduction_pct == 92.0
