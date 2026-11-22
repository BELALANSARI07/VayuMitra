import React, { useState, useEffect } from 'react';
import { SkipLink } from './components/ui/SkipLink';
import { HeroLocationBar } from './components/HeroLocationBar';
import { DispersionAndWeatherBar } from './components/DispersionAndWeatherBar';
import { HealthImpactPanel } from './components/HealthImpactPanel';
import { PollutantBreakdownGrid } from './components/PollutantBreakdownGrid';
import { PersonaConfigurator, PersonaState } from './components/PersonaConfigurator';
import { ActionableRoutineGrid } from './components/ActionableRoutineGrid';
import { VayuChatDrawer } from './components/VayuChatDrawer';
import { useAirQuality } from './hooks/useAirQuality';
import { useRoutinePlan } from './hooks/useRoutinePlan';
import { useChat } from './hooks/useChat';

export const App: React.FC = () => {
  const { data: airQuality, isLoading: aqiLoading, coords, setCoords, searchLocation } = useAirQuality();
  const { plan, isLoading: planLoading, generatePlan } = useRoutinePlan();

  const [persona, setPersona] = useState<PersonaState>({
    vulnerableGroups: ['child', 'asthmatic'],
    commuteMode: 'two_wheeler',
    commuteDistanceKm: 8.0,
    homeType: 'apartment_unsealed',
    cookingFuel: 'lpg',
    budgetTier: 'low',
  });

  const [isChatOpen, setIsChatOpen] = useState(false);
  const { messages, isStreaming, sendMessage } = useChat(coords.lat, coords.lon);

  // Generate initial plan automatically when coords are loaded
  useEffect(() => {
    generatePlan(persona, coords.lat, coords.lon);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [coords.lat, coords.lon]);

  const handlePersonaChange = (updated: Partial<PersonaState>) => {
    setPersona((prev) => ({ ...prev, ...updated }));
  };

  const handlePersonaSubmit = () => {
    generatePlan(persona, coords.lat, coords.lon);
  };

  return (
    <div className="min-h-screen bg-[#FFFBF7] flex flex-col justify-between selection:bg-[#FFE8D6] selection:text-[#1F2937]">
      <SkipLink />

      <div className="max-w-6xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8 flex-1">
        {/* 1. Hero Location & Live AQI Bar */}
        <HeroLocationBar
          airQuality={airQuality}
          isLoading={aqiLoading}
          onLocationSelect={setCoords}
          onSearch={searchLocation}
        />

        {/* 2. Meteorological & Atmospheric Dispersion Bar */}
        {airQuality && (
          <DispersionAndWeatherBar
            atmosphericFactors={airQuality.atmospheric_factors}
            temperatureC={airQuality.temperature_c}
            humidityPct={airQuality.humidity_pct}
            windSpeedKmh={airQuality.wind_speed_kmh}
            bestSafeWindow={airQuality.best_safe_window}
          />
        )}

        {/* 3. Main Content Landmark */}
        <main id="main-content" tabIndex={-1} className="space-y-10 focus:outline-none">
          {/* Clinical Health Risk & Physiological Impact Panel */}
          {airQuality && (
            <HealthImpactPanel
              healthImpact={airQuality.health_impact}
              cigaretteEquivalent={airQuality.cigarette_equivalent_24h}
              aqiValue={airQuality.aqi_value}
              aqiLabel={airQuality.aqi_label}
            />
          )}

          {/* 6 Core Pollutants Exceedance Analysis Grid */}
          {airQuality && (
            <PollutantBreakdownGrid pollutants={airQuality.pollutants} />
          )}

          {/* Persona Configurator */}
          <PersonaConfigurator
            persona={persona}
            onChange={handlePersonaChange}
            onSubmit={handlePersonaSubmit}
            isLoading={planLoading}
          />

          {/* Actionable Plan Grid (Pillars 1, 2, 3, 4) */}
          {plan ? (
            <ActionableRoutineGrid plan={plan} />
          ) : planLoading ? (
            <div
              role="status"
              aria-live="polite"
              className="p-12 text-center bg-white rounded-3xl border border-[#E5E7EB] shadow-xs"
            >
              <span className="text-3xl animate-spin block mb-3">⏳</span>
              <p className="text-base font-bold text-[#1F2937]">
                Computing respiratory exposure & emission models...
              </p>
              <p className="text-xs text-[#6B7280] mt-1 font-mono">
                Applying ICRP-66 minute ventilation deltas & CPCB transport emission factors
              </p>
            </div>
          ) : null}
        </main>
      </div>

      {/* 4. Footer Landmark */}
      <footer role="contentinfo" className="bg-[#FFE8D6]/40 border-t border-[#FFDAB9] py-8 mt-12">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 text-center sm:flex sm:items-center sm:justify-between text-xs text-[#4B5563]">
          <div>
            <strong>VayuMitra • PromptWars [Challenge 6]</strong>
            <p className="mt-0.5 text-[#6B7280]">
              Built with clean modular architecture, zero-LLM fabricated math, and WCAG 2.1 AA accessibility.
            </p>
          </div>
          <div className="mt-4 sm:mt-0 space-x-3 text-[#1F2937] font-semibold">
            <span>CPCB NAAQS 2024</span>
            <span>•</span>
            <span>WHO AQG 2021</span>
            <span>•</span>
            <span>ICRP-66 Model</span>
            <span>•</span>
            <span>Berkeley Earth Rule</span>
          </div>
        </div>
      </footer>

      {/* 5. VayuChat Floating Drawer */}
      <VayuChatDrawer
        isOpen={isChatOpen}
        onClose={() => setIsChatOpen(false)}
        onOpen={() => setIsChatOpen(true)}
        messages={messages}
        isStreaming={isStreaming}
        onSendMessage={sendMessage}
      />
    </div>
  );
};
