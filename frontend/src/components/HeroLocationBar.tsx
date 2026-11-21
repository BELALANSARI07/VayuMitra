import React, { useState } from 'react';
import { AirQualityData } from '../types';
import { DEMO_PRESETS, DemoPreset } from '../utils/constants';
import { AqiBadge } from './AqiBadge';

interface HeroLocationBarProps {
  airQuality: AirQualityData | null;
  isLoading: boolean;
  onLocationSelect: (lat: number, lon: number, label: string) => void;
  onSearch: (query: string) => void;
}

export const HeroLocationBar: React.FC<HeroLocationBarProps> = ({
  airQuality,
  isLoading,
  onLocationSelect,
  onSearch,
}) => {
  const [searchInput, setSearchInput] = useState('');

  const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter' && searchInput.trim()) {
      onSearch(searchInput.trim());
    }
  };

  return (
    <header role="banner" className="bg-[#FFE8D6]/70 border border-[#FFDAB9] rounded-3xl p-6 sm:p-8 shadow-sm">
      <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-6">
        <div>
          <div className="flex items-center gap-2">
            <span className="text-3xl" aria-hidden="true">
              🌬️
            </span>
            <h1 className="text-3xl sm:text-4xl font-extrabold text-[#1F2937] tracking-tight">
              VayuMitra
            </h1>
          </div>
          <p className="mt-1.5 text-base sm:text-lg text-[#4B5563] font-medium">
            Urban Air Quality Assistant • Science-Grounded Smog Navigation
          </p>
        </div>

        {/* Quick Demo Location Presets */}
        <div>
          <span id="presets-label" className="block text-xs font-bold uppercase tracking-wider text-[#4B5563] mb-2">
            Quick Demo Presets:
          </span>
          <div
            role="group"
            aria-labelledby="presets-label"
            className="flex flex-wrap gap-2"
          >
            {DEMO_PRESETS.map((preset: DemoPreset) => {
              const isSelected = airQuality?.location_label.includes(preset.label);
              return (
                <button
                  key={preset.pincode}
                  type="button"
                  onClick={() => onLocationSelect(preset.lat, preset.lon, preset.label)}
                  aria-pressed={isSelected}
                  className={`px-3.5 py-1.5 rounded-xl text-sm font-semibold transition-all duration-150 focus-visible:outline-none focus-visible:ring-3 focus-visible:ring-blue-600 ${
                    isSelected
                      ? 'bg-[#1F2937] text-white shadow-sm'
                      : 'bg-white hover:bg-[#FFDAB9] text-[#1F2937] border border-[#D1D5DB]'
                  }`}
                >
                  📍 {preset.label}
                </button>
              );
            })}
          </div>
        </div>
      </div>

      {/* Search Input Bar */}
      <div className="mt-6 flex flex-col sm:flex-row gap-3">
        <div className="relative flex-1">
          <label htmlFor="location-search-input" className="sr-only">
            Search by pincode or city name
          </label>
          <input
            id="location-search-input"
            type="search"
            value={searchInput}
            onChange={(e) => setSearchInput(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Enter Indian pincode (e.g. 110001) or city (e.g. Noida)..."
            maxLength={100}
            className="w-full px-4 py-3 rounded-xl border border-[#D1D5DB] bg-white text-[#1F2937] placeholder:text-[#6B7280] font-medium focus-visible:outline-none focus-visible:ring-3 focus-visible:ring-blue-600 shadow-sm"
          />
        </div>
        <button
          type="button"
          onClick={() => searchInput.trim() && onSearch(searchInput.trim())}
          className="px-6 py-3 rounded-xl bg-[#1F2937] text-white font-bold hover:bg-[#374151] transition-colors focus-visible:outline-none focus-visible:ring-3 focus-visible:ring-blue-600 shadow-sm"
        >
          Check AQI
        </button>
      </div>

      {/* Live AQI Overview Card */}
      {isLoading ? (
        <div
          role="status"
          aria-live="polite"
          className="mt-6 p-6 rounded-2xl bg-white/90 border border-[#E5E7EB] flex items-center justify-center gap-3 text-[#4B5563] font-semibold"
        >
          <span className="animate-spin text-xl">⏳</span> Loading live air quality data...
        </div>
      ) : airQuality ? (
        <div
          role="region"
          aria-label="Live air quality overview"
          className="mt-6 p-5 sm:p-6 rounded-2xl bg-white/95 border border-[#E5E7EB] shadow-sm flex flex-col lg:flex-row lg:items-center lg:justify-between gap-6"
        >
          <div className="flex flex-wrap items-center gap-4">
            <div>
              <span className="text-xs uppercase font-bold tracking-wider text-[#6B7280]">
                Current Location
              </span>
              <h2 className="text-xl font-bold text-[#1F2937]">
                {airQuality.location_label}
              </h2>
            </div>
            <AqiBadge value={airQuality.aqi_value} label={airQuality.aqi_label} />
          </div>

          {/* Best Safe Window */}
          <div className="bg-[#FFFBF7] border border-[#FFE8D6] px-4 py-3 rounded-xl flex items-center gap-3">
            <span className="text-2xl" aria-hidden="true">
              🕒
            </span>
            <div>
              <span className="block text-xs font-bold uppercase tracking-wider text-[#4B5563]">
                Best Safe Outdoor Window Today
              </span>
              <span className="text-sm sm:text-base font-extrabold text-[#1F2937]">
                {airQuality.best_safe_window}
              </span>
            </div>
          </div>

          {/* Meteorological & Pollutant Snapshot */}
          <div className="flex flex-wrap items-center gap-4 text-xs sm:text-sm text-[#4B5563] font-medium border-t lg:border-t-0 pt-3 lg:pt-0">
            <div>
              <span className="text-[#6B7280]">Primary:</span>{' '}
              <strong className="text-[#1F2937]">{airQuality.primary_pollutant}</strong>
            </div>
            {airQuality.temperature_c !== undefined && (
              <div>
                <span className="text-[#6B7280]">Temp:</span>{' '}
                <strong className="text-[#1F2937]">{airQuality.temperature_c}°C</strong>
              </div>
            )}
            {airQuality.humidity_pct !== undefined && (
              <div>
                <span className="text-[#6B7280]">Humidity:</span>{' '}
                <strong className="text-[#1F2937]">{airQuality.humidity_pct}%</strong>
              </div>
            )}
          </div>
        </div>
      ) : null}
    </header>
  );
};
