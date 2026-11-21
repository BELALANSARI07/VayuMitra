import { useState, useCallback } from 'react';
import { RoutinePlanResponse } from '../types';
import { PersonaState } from '../components/PersonaConfigurator';

const API_BASE = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

export function useRoutinePlan() {
  const [plan, setPlan] = useState<RoutinePlanResponse | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  const generatePlan = useCallback(async (persona: PersonaState, lat: number, lon: number) => {
    setIsLoading(true);
    setError(null);

    const payload = {
      lat,
      lon,
      vulnerable_groups: persona.vulnerableGroups,
      commute_mode: persona.commuteMode,
      commute_distance_km: persona.commuteDistanceKm,
      home_type: persona.homeType,
      cooking_fuel: persona.cookingFuel,
      budget_tier: persona.budgetTier,
      household_size: 4,
    };

    try {
      const resp = await fetch(`${API_BASE}/api/routine-plan`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      });

      if (!resp.ok) {
        throw new Error(`Plan generation failed: ${resp.statusText}`);
      }

      const json: RoutinePlanResponse = await resp.json();
      setPlan(json);
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : 'Failed to generate plan');
    } finally {
      setIsLoading(false);
    }
  }, []);

  return { plan, isLoading, error, generatePlan };
}
