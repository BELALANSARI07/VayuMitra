import React from 'react';
import { BudgetTier, CommuteMode, CookingFuel, HomeType, VulnerableGroup } from '../types';

export interface PersonaState {
  vulnerableGroups: VulnerableGroup[];
  commuteMode: CommuteMode;
  commuteDistanceKm: number;
  homeType: HomeType;
  cookingFuel: CookingFuel;
  budgetTier: BudgetTier;
}

interface PersonaConfiguratorProps {
  persona: PersonaState;
  onChange: (updated: Partial<PersonaState>) => void;
  onSubmit: () => void;
  isLoading: boolean;
}

const VULNERABILITY_OPTIONS: { id: VulnerableGroup; label: string; icon: string }[] = [
  { id: 'child', label: 'Child (under 10)', icon: '👶' },
  { id: 'elderly', label: 'Elderly (65+)', icon: '👴' },
  { id: 'asthmatic', label: 'Asthma / Respiratory', icon: '🫁' },
  { id: 'pregnant', label: 'Pregnant Member', icon: '🤰' },
  { id: 'none', label: 'None', icon: '🛡️' },
];

const BUDGET_OPTIONS: { id: BudgetTier; label: string; range: string }[] = [
  { id: 'free', label: 'Free', range: '₹0 (Behavioral only)' },
  { id: 'low', label: 'Low', range: '≤ ₹500 (DIY Sealing/Filter)' },
  { id: 'medium', label: 'Medium', range: '≤ ₹2,000 (HEPA Sanctuary)' },
  { id: 'high', label: 'High', range: '₹10,000+ (Whole-Home)' },
];

export const PersonaConfigurator: React.FC<PersonaConfiguratorProps> = ({
  persona,
  onChange,
  onSubmit,
  isLoading,
}) => {
  const toggleVulnerability = (group: VulnerableGroup) => {
    let next: VulnerableGroup[];
    if (group === 'none') {
      next = ['none'];
    } else {
      const filtered = persona.vulnerableGroups.filter((g) => g !== 'none');
      if (filtered.includes(group)) {
        next = filtered.filter((g) => g !== group);
        if (next.length === 0) next = ['none'];
      } else {
        next = [...filtered, group];
      }
    }
    onChange({ vulnerableGroups: next });
  };

  return (
    <section
      aria-labelledby="persona-configurator-heading"
      className="bg-white border border-[#E5E7EB] rounded-3xl p-6 sm:p-8 shadow-sm"
    >
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-2 border-b border-[#F3F4F6] pb-4">
        <div>
          <h2 id="persona-configurator-heading" className="text-xl sm:text-2xl font-bold text-[#1F2937]">
            Personalize Your Low-Emission Plan
          </h2>
          <p className="text-sm text-[#4B5563] mt-0.5">
            Tailor routines, indoor hacks, and sustainable swaps to your household reality.
          </p>
        </div>
        <span className="text-xs bg-[#FFE8D6] text-[#78350F] font-bold px-3 py-1 rounded-full uppercase tracking-wide self-start sm:self-auto">
          Challenge 6 Tailoring
        </span>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mt-6">
        {/* Household Vulnerabilities */}
        <div className="lg:col-span-3">
          <span id="vulnerability-group-label" className="block text-sm font-bold text-[#1F2937] mb-2.5">
            Household Vulnerabilities (Select all that apply):
          </span>
          <div
            role="group"
            aria-labelledby="vulnerability-group-label"
            className="flex flex-wrap gap-2.5"
          >
            {VULNERABILITY_OPTIONS.map((opt) => {
              const isSelected = persona.vulnerableGroups.includes(opt.id);
              return (
                <button
                  key={opt.id}
                  type="button"
                  onClick={() => toggleVulnerability(opt.id)}
                  aria-pressed={isSelected}
                  className={`px-4 py-2 rounded-xl text-sm font-semibold transition-all duration-150 flex items-center gap-2 focus-visible:outline-none focus-visible:ring-3 focus-visible:ring-blue-600 ${
                    isSelected
                      ? 'bg-[#FFE8D6] text-[#1F2937] border-2 border-[#D97706] shadow-sm'
                      : 'bg-[#FFFBF7] text-[#4B5563] border border-[#E5E7EB] hover:bg-[#FFE8D6]/40'
                  }`}
                >
                  <span aria-hidden="true">{opt.icon}</span>
                  <span>{opt.label}</span>
                </button>
              );
            })}
          </div>
        </div>

        {/* Commute Mode */}
        <div>
          <label htmlFor="commute-mode-select" className="block text-sm font-bold text-[#1F2937] mb-1.5">
            Primary Commute Mode:
          </label>
          <select
            id="commute-mode-select"
            value={persona.commuteMode}
            onChange={(e) => onChange({ commuteMode: e.target.value as CommuteMode })}
            className="w-full px-3.5 py-2.5 rounded-xl border border-[#D1D5DB] bg-white text-[#1F2937] font-medium focus-visible:outline-none focus-visible:ring-3 focus-visible:ring-blue-600 shadow-sm"
          >
            <option value="two_wheeler">🛵 Petrol Two-Wheeler (Motorcycle/Scooter)</option>
            <option value="car_petrol">🚗 Petrol Car</option>
            <option value="car_diesel">🚙 Diesel Car</option>
            <option value="auto_rickshaw">🛺 Auto-Rickshaw</option>
            <option value="bus">🚌 Public Bus</option>
            <option value="metro">🚇 Metro Rail Transit</option>
            <option value="ev">⚡ Electric Vehicle (EV)</option>
            <option value="bicycle">🚲 Bicycle</option>
            <option value="walk">🚶 Walking</option>
          </select>
        </div>

        {/* Commute Distance */}
        <div>
          <label htmlFor="commute-dist-input" className="block text-sm font-bold text-[#1F2937] mb-1.5">
            One-Way Commute Distance:
          </label>
          <div className="relative">
            <input
              id="commute-dist-input"
              type="number"
              min="0.5"
              max="150"
              step="0.5"
              value={persona.commuteDistanceKm}
              onChange={(e) => onChange({ commuteDistanceKm: parseFloat(e.target.value) || 5 })}
              className="w-full px-3.5 py-2.5 rounded-xl border border-[#D1D5DB] bg-white text-[#1F2937] font-medium focus-visible:outline-none focus-visible:ring-3 focus-visible:ring-blue-600 shadow-sm pr-12"
            />
            <span className="absolute right-3.5 top-2.5 text-sm font-semibold text-[#6B7280]" aria-hidden="true">
              km
            </span>
          </div>
        </div>

        {/* Home Infiltration Profile */}
        <div>
          <label htmlFor="home-type-select" className="block text-sm font-bold text-[#1F2937] mb-1.5">
            Home Structure Type:
          </label>
          <select
            id="home-type-select"
            value={persona.homeType}
            onChange={(e) => onChange({ homeType: e.target.value as HomeType })}
            className="w-full px-3.5 py-2.5 rounded-xl border border-[#D1D5DB] bg-white text-[#1F2937] font-medium focus-visible:outline-none focus-visible:ring-3 focus-visible:ring-blue-600 shadow-sm"
          >
            <option value="apartment_unsealed">🏢 Apartment (Standard unsealed windows)</option>
            <option value="apartment_sealed">🪟 Sealed Apartment (Weatherstripped)</option>
            <option value="independent_house">🏡 Independent House / Ground Floor</option>
            <option value="kutcha">🛖 Semi-Pucca / Kutcha Dwelling</option>
          </select>
        </div>

        {/* Cooking Fuel */}
        <div>
          <label htmlFor="cooking-fuel-select" className="block text-sm font-bold text-[#1F2937] mb-1.5">
            Cooking Fuel:
          </label>
          <select
            id="cooking-fuel-select"
            value={persona.cookingFuel}
            onChange={(e) => onChange({ cookingFuel: e.target.value as CookingFuel })}
            className="w-full px-3.5 py-2.5 rounded-xl border border-[#D1D5DB] bg-white text-[#1F2937] font-medium focus-visible:outline-none focus-visible:ring-3 focus-visible:ring-blue-600 shadow-sm"
          >
            <option value="lpg">🔥 Piped Natural Gas / LPG Cylinder</option>
            <option value="electric">⚡ Induction / Electric Stove</option>
            <option value="biomass">🪵 Wood / Biomass / Chulha</option>
            <option value="kerosene">🛢️ Kerosene Stove</option>
          </select>
        </div>

        {/* Budget Tier */}
        <div className="md:col-span-2">
          <span id="budget-group-label" className="block text-sm font-bold text-[#1F2937] mb-2">
            Air Quality Improvement Budget:
          </span>
          <div
            role="radiogroup"
            aria-labelledby="budget-group-label"
            className="grid grid-cols-2 sm:grid-cols-4 gap-2.5"
          >
            {BUDGET_OPTIONS.map((tier) => {
              const isSelected = persona.budgetTier === tier.id;
              return (
                <button
                  key={tier.id}
                  type="button"
                  role="radio"
                  aria-checked={isSelected}
                  onClick={() => onChange({ budgetTier: tier.id })}
                  className={`p-3 rounded-xl text-left transition-all duration-150 focus-visible:outline-none focus-visible:ring-3 focus-visible:ring-blue-600 ${
                    isSelected
                      ? 'bg-[#1F2937] text-white shadow-sm'
                      : 'bg-[#FFFBF7] text-[#1F2937] border border-[#E5E7EB] hover:bg-[#FFE8D6]/50'
                  }`}
                >
                  <span className="block text-sm font-bold">{tier.label}</span>
                  <span className={`block text-xs mt-0.5 ${isSelected ? 'text-gray-300' : 'text-[#6B7280]'}`}>
                    {tier.range}
                  </span>
                </button>
              );
            })}
          </div>
        </div>
      </div>

      {/* Submit Trigger */}
      <div className="mt-8 pt-5 border-t border-[#F3F4F6] flex justify-end">
        <button
          type="button"
          onClick={onSubmit}
          disabled={isLoading}
          aria-busy={isLoading}
          className="w-full sm:w-auto px-8 py-3.5 rounded-2xl bg-[#D97706] hover:bg-[#B45309] text-white font-extrabold text-base tracking-wide transition-all shadow-md hover:shadow-lg focus-visible:outline-none focus-visible:ring-4 focus-visible:ring-amber-400 disabled:opacity-60 flex items-center justify-center gap-2"
        >
          {isLoading ? (
            <>
              <span className="animate-spin text-lg">⏳</span> Generating Plan...
            </>
          ) : (
            <>
              <span>✨</span> Generate Personalized Air Quality Plan
            </>
          )}
        </button>
      </div>
    </section>
  );
};
