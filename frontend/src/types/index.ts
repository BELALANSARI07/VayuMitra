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

export interface PollutantReading {
  name: string;
  value: number;
  unit: string;
}

export interface HourlyForecast {
  hour: number;
  pm25: number;
  pm10: number;
  aqi_label: string;
  is_safe_window: boolean;
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
