import React from 'react';
import { AtmosphericFactors } from '../types';

interface DispersionAndWeatherBarProps {
  atmosphericFactors?: AtmosphericFactors;
  temperatureC?: number;
  humidityPct?: number;
  windSpeedKmh?: number;
  bestSafeWindow?: string;
}

export const DispersionAndWeatherBar: React.FC<DispersionAndWeatherBarProps> = ({
  atmosphericFactors,
  temperatureC,
  humidityPct,
  windSpeedKmh,
  bestSafeWindow,
}) => {
  const wind = atmosphericFactors?.wind_speed_kmh ?? windSpeedKmh ?? 5.5;
  const humidity = atmosphericFactors?.humidity_pct ?? humidityPct ?? 75.0;
  const temp = atmosphericFactors?.temperature_c ?? temperatureC ?? 17.0;
  const verdict =
    atmosphericFactors?.dispersion_verdict ??
    (wind < 6.0
      ? `Stagnant air (${wind} km/h wind) — smog trapped at street level due to nocturnal thermal inversion.`
      : `Active boundary-layer mixing (${wind} km/h wind).`);
  const safeWindow =
    atmosphericFactors?.best_ventilation_window ??
    bestSafeWindow ??
    '1:00 PM – 4:00 PM (Peak thermal mixing)';

  const isStagnant = wind < 6.0;

  return (
    <div
      role="region"
      aria-label="Atmospheric dispersion and meteorological conditions"
      className="bg-[#FFFBF7] border border-[#FFE8D6] rounded-2xl p-4 sm:p-5 shadow-xs"
    >
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 sm:gap-6 divide-y md:divide-y-0 md:divide-x divide-[#FFE8D6]">
        {/* 1. Wind Speed & Stagnation Verdict */}
        <div className="flex items-start gap-3 pt-2 md:pt-0">
          <span className="text-2xl mt-0.5" aria-hidden="true">
            🍃
          </span>
          <div>
            <div className="flex items-center gap-2">
              <span className="text-xs font-bold uppercase tracking-wider text-[#6B7280]">
                Wind & Dispersion
              </span>
              <span
                className={`px-2 py-0.5 rounded-full text-[11px] font-extrabold uppercase ${
                  isStagnant
                    ? 'bg-rose-100 text-rose-800 border border-rose-200'
                    : 'bg-emerald-100 text-emerald-800 border border-emerald-200'
                }`}
              >
                {isStagnant ? '⚠️ Stagnant Air' : '✅ Active Mixing'}
              </span>
            </div>
            <div className="mt-1 flex items-baseline gap-1.5">
              <span className="text-2xl font-black text-[#1F2937]">{wind}</span>
              <span className="text-xs font-bold text-[#6B7280]">km/h</span>
            </div>
            <p className="text-xs text-[#4B5563] mt-1 leading-snug">
              {verdict}
            </p>
          </div>
        </div>

        {/* 2. Humidity, Temperature & Winter Smog Inversion */}
        <div className="flex items-start gap-3 pt-4 md:pt-0 md:pl-6">
          <span className="text-2xl mt-0.5" aria-hidden="true">
            🌡️
          </span>
          <div>
            <span className="text-xs font-bold uppercase tracking-wider text-[#6B7280] block">
              Meteorological Trapping
            </span>
            <div className="mt-1 flex items-center gap-4 text-sm font-extrabold text-[#1F2937]">
              <span>
                Temp: <strong className="text-base">{temp}°C</strong>
              </span>
              <span>•</span>
              <span>
                Humidity: <strong className="text-base">{humidity}%</strong>
              </span>
            </div>
            <p className="text-xs text-[#4B5563] mt-1 leading-snug">
              {humidity > 70
                ? 'High humidity (>70%) combines with cold surface air to promote secondary aerosol nucleation and dense winter smog trapping.'
                : 'Moderate moisture levels allow steady particulate dispersion.'}
            </p>
          </div>
        </div>

        {/* 3. Highlighted Best Safe Window Today */}
        <div className="flex items-start gap-3 pt-4 md:pt-0 md:pl-6">
          <span className="text-2xl mt-0.5" aria-hidden="true">
            ☀️
          </span>
          <div className="w-full">
            <span className="text-xs font-bold uppercase tracking-wider text-[#4B5563] block">
              Optimal Outdoor & Ventilation Window
            </span>
            <div className="mt-1.5 p-2.5 rounded-xl bg-[#FFE8D6] border border-[#FFDAB9] flex items-center gap-2">
              <span className="w-2.5 h-2.5 rounded-full bg-emerald-600 animate-pulse shrink-0" aria-hidden="true" />
              <strong className="text-xs sm:text-sm font-extrabold text-[#78350F] leading-tight">
                {safeWindow}
              </strong>
            </div>
            <span className="text-[11px] text-[#6B7280] mt-1 block">
              Safest afternoon hours for quick cross-ventilation or necessary outdoor transit.
            </span>
          </div>
        </div>
      </div>
    </div>
  );
};
