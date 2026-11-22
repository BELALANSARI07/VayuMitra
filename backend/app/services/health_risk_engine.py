"""
Health Risk Engine:
Zero-hallucination deterministic health impact calculation, safe limit comparisons
(CPCB NAAQS 2009/2024 vs WHO AQG 2021), Berkeley Earth cigarette equivalents,
and clinical health impact categorization across AQI bands.
"""
from __future__ import annotations

from typing import Any, Literal
from app.core.constants import CIGARETTE_PM25_EQUIVALENT_UG, POLLUTANT_THRESHOLDS

PollutantStatus = Literal["Safe", "Above WHO", "Above CPCB (Unsafe)", "Hazardous"]


def pm25_to_cigarettes_24h(pm25: float) -> float:
    """
    Convert 24-hour outdoor PM2.5 concentration (µg/m³) into cigarette equivalents
    using the Berkeley Earth rule of thumb (1 cigarette ≈ 22 µg/m³ for 24 hours).
    
    Formula: max(0.0, pm25) / 22.0 rounded to 1 decimal place.
    """
    return round(max(0.0, float(pm25)) / CIGARETTE_PM25_EQUIVALENT_UG, 1)


def normalize_pollutant_key(name: str) -> str:
    """Normalize input names like 'PM2.5', 'pm25', 'nitrogen_dioxide' to constant keys."""
    cleaned = name.strip().lower().replace(".", "").replace("-", "_").replace(" ", "_")
    mapping = {
        "pm25": "pm2_5",
        "pm2_5": "pm2_5",
        "pm10": "pm10",
        "no2": "no2",
        "nitrogen_dioxide": "no2",
        "so2": "so2",
        "sulphur_dioxide": "so2",
        "sulfur_dioxide": "so2",
        "o3": "o3",
        "ozone": "o3",
        "co": "co",
        "carbon_monoxide": "co",
    }
    return mapping.get(cleaned, cleaned)


def analyze_pollutant(name_or_key: str, value: float) -> dict[str, Any]:
    """
    Perform rigorous, deterministic exceedance analysis for a single pollutant against
    CPCB NAAQS standards and WHO 2021 Air Quality Guidelines.
    """
    key = normalize_pollutant_key(name_or_key)
    meta = POLLUTANT_THRESHOLDS.get(key)
    val = max(0.0, float(value))

    if not meta:
        return {
            "name": name_or_key,
            "value": round(val, 2),
            "unit": "µg/m³",
            "cpcb_limit": 60.0,
            "who_limit": 15.0,
            "cpcb_multiplier": round(val / 60.0, 1),
            "who_multiplier": round(val / 15.0, 1),
            "status": "Safe" if val <= 15.0 else "Above WHO",
            "primary_sources": "Urban combustion and industrial emissions",
            "exceedance_health_effect": "Elevated particulate or gaseous airway irritation on prolonged exposure.",
        }

    cpcb_limit = float(meta["cpcb_24h"])
    who_limit = float(meta["who_24h"])
    unit = str(meta["unit"])
    display_name = str(meta["display_name"])
    sources = str(meta["sources"])
    health_effect = str(meta["health_effect"])

    cpcb_mult = round(val / cpcb_limit, 1)
    who_mult = round(val / who_limit, 1)

    # Determine status
    if key == "o3":
        # CPCB and WHO are identical (100 µg/m³ 8-hr)
        if val <= 100.0:
            status: PollutantStatus = "Safe"
        elif val <= 200.0:
            status = "Above CPCB (Unsafe)"
        else:
            status = "Hazardous"
    elif key == "co":
        # CPCB 8h is 2.0 mg/m³, WHO 24h is 4.0 mg/m³
        if val <= 2.0:
            status = "Safe"
        elif val <= 4.0:
            status = "Above CPCB (Unsafe)"
        else:
            status = "Hazardous"
    else:
        # Standard progression: Safe <= WHO < Above WHO <= CPCB < Above CPCB <= 2*CPCB < Hazardous
        if val <= who_limit:
            status = "Safe"
        elif val <= cpcb_limit:
            status = "Above WHO"
        elif val <= cpcb_limit * 2.0:
            status = "Above CPCB (Unsafe)"
        else:
            status = "Hazardous"

    return {
        "name": display_name,
        "value": round(val, 2),
        "unit": unit,
        "cpcb_limit": cpcb_limit,
        "who_limit": who_limit,
        "cpcb_multiplier": cpcb_mult,
        "who_multiplier": who_mult,
        "status": status,
        "primary_sources": sources,
        "exceedance_health_effect": health_effect,
    }


def map_cpcb_aqi_health_impact(aqi_value: int) -> dict[str, Any]:
    """
    Deterministic CPCB AQI band health impact mapper covering all 6 official bands (0 to 500+).
    Returns clinical physiological impacts for healthy adults vs sensitive demographics,
    short-term/long-term risks, and red-flag clinical symptoms.
    """
    aqi = max(0, int(aqi_value))

    if aqi <= 50:
        return {
            "category_label": "Good",
            "healthy_adults_impact": "Clean, uncompromised air quality. Minimal to zero impact on respiratory function during all outdoor activities.",
            "sensitive_groups_impact": "Completely safe for infants, pregnant women, elderly, and individuals with chronic COPD or asthma.",
            "short_term_risks": "None observed at ambient levels.",
            "long_term_risks": "Zero elevated risk of cardio-respiratory disease.",
            "red_flag_symptoms": [],
        }
    elif aqi <= 100:
        return {
            "category_label": "Satisfactory",
            "healthy_adults_impact": "Acceptable air quality. Minor breathing discomfort may be experienced by exceptionally sensitive individuals during intense physical training.",
            "sensitive_groups_impact": "Mild airway irritation or cough possible in asthmatic children and seniors with pre-existing bronchitis.",
            "short_term_risks": "Slight throat tickle, mild eye dryness on prolonged outdoor exposure.",
            "long_term_risks": "Negligible long-term risk if seasonal averages stay within standard limits.",
            "red_flag_symptoms": ["Mild throat irritation", "Occasional dry cough"],
        }
    elif aqi <= 200:
        return {
            "category_label": "Moderate",
            "healthy_adults_impact": "Noticeable airway irritation and slight exercise fatigue during prolonged outdoor workouts or extended commutes.",
            "sensitive_groups_impact": "Asthmatics, children, and seniors experience reduced peak expiratory flow, wheezing, and coughing.",
            "short_term_risks": "Throat scratchiness, bronchial constriction, reduced exercise tolerance, stinging eyes.",
            "long_term_risks": "Frequent seasonal exacerbation of asthma and chronic bronchitis.",
            "red_flag_symptoms": [
                "Persistent dry cough",
                "Throat irritation",
                "Mild shortness of breath during exertion",
            ],
        }
    elif aqi <= 300:
        return {
            "category_label": "Poor",
            "healthy_adults_impact": "Breathing discomfort to most people on prolonged exposure; fatigue, airway dryness, and headaches during transit.",
            "sensitive_groups_impact": "Acute discomfort and elevated risk of asthma attacks for children, elderly, and cardiopulmonary patients.",
            "short_term_risks": "Bronchial constriction, persistent coughing, sinus congestion, burning eyes, tension headaches.",
            "long_term_risks": "Accelerated decline in lung vital capacity, increased systemic arterial inflammation.",
            "red_flag_symptoms": [
                "Persistent cough",
                "Breathlessness",
                "Chest tightness",
                "Red/watery eyes",
            ],
        }
    elif aqi <= 400:
        return {
            "category_label": "Very Poor",
            "healthy_adults_impact": "Causes respiratory illness on prolonged exposure; significant airway inflammation, pharyngeal burning, and reduced stamina in fit non-smokers.",
            "sensitive_groups_impact": "Acute medical distress in vulnerable demographics; high trigger rate for severe asthma attacks and cardiac arrhythmias.",
            "short_term_risks": "Severe wheezing, heavy phlegm production, chest heaviness, reduced blood oxygen saturation, severe ocular inflammation.",
            "long_term_risks": "Increased risk of ischemic heart disease, stroke, chronic obstructive pulmonary disease (COPD), and impaired child lung development.",
            "red_flag_symptoms": [
                "Breathlessness on mild movement",
                "Persistent cough with phlegm",
                "Chest discomfort",
                "Giddiness",
                "Red/watery eyes",
            ],
        }
    else:
        # 401 - 500+
        return {
            "category_label": "Severe",
            "healthy_adults_impact": "Affects healthy adults severely and gravely impacts those with pre-existing cardiopulmonary disease; physiological impact equals heavy active cigarette smoking.",
            "sensitive_groups_impact": "Medical emergency condition for asthmatics, COPD patients, elderly, pregnant women, and infants. Immediate indoor isolation mandatory.",
            "short_term_risks": "Acute lower respiratory tract infections, severe asthma exacerbations, sharp spike in emergency room visits for myocardial infarction and arrhythmias.",
            "long_term_risks": "Permanent reduction in pulmonary capacity, elevated lifetime lung cancer incidence, premature cardiovascular mortality.",
            "red_flag_symptoms": [
                "Persistent cough",
                "Breathlessness",
                "Chest discomfort",
                "Giddiness",
                "Red/watery eyes",
            ],
        }


def assess_atmospheric_factors(
    wind_speed_kmh: float | None = None,
    humidity_pct: float | None = None,
    temp_c: float | None = None,
) -> dict[str, Any]:
    """
    Evaluate meteorological conditions to determine boundary-layer dispersion verdicts
    and optimal cross-ventilation windows.
    """
    wind = 7.5 if wind_speed_kmh is None else float(wind_speed_kmh)
    humidity = 72.0 if humidity_pct is None else float(humidity_pct)
    temp = 18.0 if temp_c is None else float(temp_c)

    if wind < 6.0:
        dispersion_verdict = f"Stagnant air ({wind:.1f} km/h wind) — smog trapped at street level due to nocturnal thermal inversion and calm winds."
    elif wind < 15.0:
        dispersion_verdict = f"Moderate atmospheric dispersion ({wind:.1f} km/h) — partial pollutant dilution during peak afternoon boundary layer expansion."
    else:
        dispersion_verdict = f"Active dispersion ({wind:.1f} km/h) — favorable wind speeds promoting rapid boundary-layer dilution."

    # Best ventilation window is generally between 1:00 PM and 4:00 PM when solar radiation breaks the surface inversion
    best_ventilation_window = "1:00 PM – 4:00 PM (Peak solar thermal mixing & maximum boundary-layer height)"

    return {
        "wind_speed_kmh": round(wind, 1),
        "humidity_pct": round(humidity, 1),
        "temperature_c": round(temp, 1),
        "dispersion_verdict": dispersion_verdict,
        "best_ventilation_window": best_ventilation_window,
    }
