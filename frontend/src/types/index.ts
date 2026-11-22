export type VulnerableGroup = 'child' | 'elderly' | 'asthmatic' | 'pregnant' | 'none';

export type CommuteMode =
  | 'two_wheeler'
  | 'car_petrol'
  | 'car_diesel'
  | 'auto_rickshaw'
  | 'bus'
  | 'metro'
  | 'bicycle'
  | 'walk'
  | 'ev';

export type HomeType =
  | 'apartment_sealed'
  | 'apartment_unsealed'
  | 'independent_house'
  | 'kutcha';

export type BudgetTier = 'free' | 'low' | 'medium' | 'high';

export type CookingFuel = 'lpg' | 'electric' | 'biomass' | 'kerosene';

export type PollutantStatus = 'Safe' | 'Above WHO' | 'Above CPCB (Unsafe)' | 'Hazardous';

export interface PollutantReading {
  name: string;
  value: number;
  unit: string;
  cpcb_limit?: number;
  who_limit?: number;
  cpcb_multiplier?: number;
  who_multiplier?: number;
  status?: PollutantStatus;
  primary_sources?: string;
  exceedance_health_effect?: string;
}

export interface HourlyForecast {
  hour: number;
  pm25: number;
  pm10: number;
  aqi_label: string;
  is_safe_window: boolean;
}

export interface HealthImpactData {
  category_label: string;
  healthy_adults_impact: string;
  sensitive_groups_impact: string;
  short_term_risks: string;
  long_term_risks: string;
  red_flag_symptoms: string[];
}

export interface AtmosphericFactors {
  wind_speed_kmh: number;
  humidity_pct: number;
  temperature_c: number;
  dispersion_verdict: string;
  best_ventilation_window: string;
}

export interface AirQualityData {
  location_label: string;
  lat: number;
  lon: number;
  timestamp: string;
  aqi_value: number;
  aqi_label: string;
  aqi_color_hex: string;
  primary_pollutant: string;
  pollutants: PollutantReading[];
  hourly_forecast_24h: HourlyForecast[];
  best_safe_window: string;
  temperature_c?: number;
  humidity_pct?: number;
  wind_speed_kmh?: number;
  data_source: string;
  overall_aqi?: number;
  dominant_pollutant?: string;
  cigarette_equivalent_24h?: number;
  health_impact?: HealthImpactData;
  atmospheric_factors?: AtmosphericFactors;
}

export interface ImpactDelta {
  pm25_reduction_ug_per_day: number;
  cigarette_equivalents_saved: number;
  co2_saved_g_per_week?: number;
  nox_saved_mg_per_week?: number;
  formula_ref: string;
  source_citation: string;
}

export interface RoutineAction {
  time_slot: string;
  action: string;
  rationale: string;
  source: string;
  impact: ImpactDelta;
}

export interface IndoorHack {
  title: string;
  description: string;
  budget_tier: BudgetTier;
  estimated_cost_inr: number;
  effectiveness_pct: number;
  source: string;
  impact: ImpactDelta;
}

export interface SustainableSwap {
  swap_from: string;
  swap_to: string;
  rationale: string;
  source: string;
  impact: ImpactDelta;
}

export interface QuantifiedImpactCard {
  pm25_reduction_pct: number;
  co2_saved_kg_week: number;
  summary_badge: string;
}

export interface ActionPlanCard {
  id: string;
  title: string;
  category: 'Routine' | 'Indoor Hack' | 'Sustainable Swap' | 'Mask & Commute';
  budget_tier: 'Free/DIY' | 'Low-Cost' | 'Smart Home';
  action_detail: string;
  quantified_impact: QuantifiedImpactCard;
  why_it_works: string;
  source_citation: string;
}

export interface RoutinePlanResponse {
  location_label: string;
  current_aqi: number;
  aqi_label: string;
  best_safe_window: string;
  routines: RoutineAction[];
  indoor_hacks: IndoorHack[];
  sustainable_swaps: SustainableSwap[];
  total_impact: ImpactDelta;
  generated_at: string;
  action_cards?: ActionPlanCard[];
}

export interface CitationRef {
  source: string;
  page: number;
  section: string;
  relevance_score: number;
}

export interface ChatSSEEvent {
  event: 'token' | 'citation' | 'impact' | 'done' | 'error';
  content?: string;
  citations?: CitationRef[];
  impact?: ImpactDelta;
}
