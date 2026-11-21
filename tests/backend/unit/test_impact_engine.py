"""
Deterministic math tests — these MUST pass before any deployment.
All expected values are hand-calculated from published constants.
"""
import pytest
from app.services.impact_engine import (
    calculate_exposure_reduction,
    calculate_emission_savings,
    cigarette_equivalents,
    ActivityLevel,
    TransportMode,
)
from app.core.constants import (
    PM25_DEPOSITION_FRACTION,
    MINUTE_VENTILATION_LIGHT_EX_L_MIN,
    CIGARETTE_PM25_EQUIVALENT_UG,
    INDOOR_OUTDOOR_RATIO_UNSEALED,
    DIY_BOX_FAN_FILTER_EFFICIENCY,
)


class TestExposureReduction:
    def test_time_shift_outdoor_walk(self) -> None:
        """Shifting walk from 300 µg/m³ peak to 120 µg/m³ morning."""
        result = calculate_exposure_reduction(
            pm25_ambient_ug_m3=300.0,
            duration_baseline_min=60.0,
            duration_shifted_min=60.0,
            activity_level=ActivityLevel.LIGHT,
            pm25_shifted_ug_m3=120.0,
        )
        # Expected: (300 - 120) * 24.0 * 60 * 0.001 * 0.65 = 168.48 µg
        assert result.pm25_inhaled_ug == pytest.approx(168.48, rel=1e-2)
        assert result.cigarette_equivalents == pytest.approx(168.48 / 22.0, rel=1e-2)
        assert "ICRP" in result.source

    def test_indoor_with_diy_filter(self) -> None:
        """Moving indoors with DIY box-fan filter in unsealed apartment."""
        result = calculate_exposure_reduction(
            pm25_ambient_ug_m3=400.0,
            duration_baseline_min=60.0,
            duration_shifted_min=60.0,
            activity_level=ActivityLevel.REST,
            is_indoor=True,
            has_diy_filter=True,
            home_sealed=False,
        )
        # Shifted concentration: 400 * 0.70 * (1 - 0.62) = 106.4 µg/m³
        # Baseline: 400 * 7.5 * 60 * 0.001 * 0.65 = 117.0
        # Shifted:  106.4 * 7.5 * 60 * 0.001 * 0.65 = 31.122
        # Reduction: 117.0 - 31.122 = 85.878
        assert result.pm25_inhaled_ug == pytest.approx(85.88, rel=1e-2)

    def test_child_exposure(self) -> None:
        """Child exposure uses reduced ventilation rate."""
        result = calculate_exposure_reduction(
            pm25_ambient_ug_m3=250.0,
            duration_baseline_min=30.0,
            duration_shifted_min=30.0,
            activity_level=ActivityLevel.LIGHT,
            pm25_shifted_ug_m3=80.0,
            is_child=True,
        )
        # Child light exercise V_dot = 5.0 * 2.4 = 12.0 L/min
        # Reduction: (250 - 80) * 12.0 * 30 * 0.001 * 0.65 = 39.78
        assert result.pm25_inhaled_ug == pytest.approx(39.78, rel=1e-2)

    def test_zero_shift_returns_zero(self) -> None:
        """Same concentration and duration -> zero reduction."""
        result = calculate_exposure_reduction(
            pm25_ambient_ug_m3=200.0,
            duration_baseline_min=45.0,
            duration_shifted_min=45.0,
            activity_level=ActivityLevel.REST,
            pm25_shifted_ug_m3=200.0,
        )
        assert result.pm25_inhaled_ug == pytest.approx(0.0, abs=1e-6)


class TestEmissionSavings:
    def test_two_wheeler_to_metro(self) -> None:
        """8 km, 10 trips/week, two-wheeler -> metro."""
        result = calculate_emission_savings(
            mode_before=TransportMode.TWO_WHEELER,
            mode_after=TransportMode.METRO,
            distance_km=8.0,
            trips_per_week=10,
        )
        # CO2: (35.0 - 7.0) * 8 * 10 = 2240.0 g
        assert result.co2_saved_g == pytest.approx(2240.0, rel=1e-3)
        # NOx: (120.0 - 2.0) * 8 * 10 = 9440.0 mg
        assert result.nox_saved_mg == pytest.approx(9440.0, rel=1e-3)

    def test_car_diesel_to_ev(self) -> None:
        result = calculate_emission_savings(
            mode_before=TransportMode.CAR_DIESEL,
            mode_after=TransportMode.EV,
            distance_km=15.0,
            trips_per_week=10,
        )
        # CO2: (180 - 25) * 15 * 10 = 23250.0 g
        assert result.co2_saved_g == pytest.approx(23250.0, rel=1e-3)

    def test_same_mode_zero_savings(self) -> None:
        result = calculate_emission_savings(
            mode_before=TransportMode.BUS,
            mode_after=TransportMode.BUS,
            distance_km=10.0,
        )
        assert result.co2_saved_g == pytest.approx(0.0)
        assert result.nox_saved_mg == pytest.approx(0.0)


class TestCigaretteEquivalents:
    def test_known_value(self) -> None:
        assert cigarette_equivalents(110.0) == pytest.approx(5.0, rel=1e-2)

    def test_zero(self) -> None:
        assert cigarette_equivalents(0.0) == 0.0
