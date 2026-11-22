import React, { useState } from 'react';
import { PollutantReading } from '../types';

interface PollutantBreakdownGridProps {
  pollutants: PollutantReading[];
}

export const PollutantBreakdownGrid: React.FC<PollutantBreakdownGridProps> = ({ pollutants }) => {
  const [expandedIndex, setExpandedIndex] = useState<number | null>(null);

  const toggleExpand = (idx: number) => {
    setExpandedIndex((prev) => (prev === idx ? null : idx));
  };

  if (!pollutants || pollutants.length === 0) return null;

  return (
    <section aria-labelledby="pollutants-heading" className="space-y-4">
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-2">
        <div>
          <div className="flex items-center gap-2">
            <span className="text-2xl" aria-hidden="true">
              🔬
            </span>
            <h2 id="pollutants-heading" className="text-xl sm:text-2xl font-bold text-[#1F2937]">
              6 Core Pollutants & Exceedance Analysis
            </h2>
          </div>
          <p className="text-xs sm:text-sm text-[#4B5563] mt-0.5">
            Strict benchmark comparisons against CPCB National Standards and WHO 2021 Guidelines.
          </p>
        </div>
        <div className="text-xs text-[#6B7280] font-medium flex items-center gap-3">
          <span className="inline-flex items-center gap-1.5">
            <span className="w-2.5 h-2.5 rounded-full bg-emerald-600 inline-block" aria-hidden="true" />
            WHO Safe Tick
          </span>
          <span className="inline-flex items-center gap-1.5">
            <span className="w-2.5 h-2.5 rounded-full bg-amber-600 inline-block" aria-hidden="true" />
            CPCB Safe Tick
          </span>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-6">
        {pollutants.map((pol, idx) => {
          const isExpanded = expandedIndex === idx;
          const whoLimit = pol.who_limit ?? 15.0;
          const cpcbLimit = pol.cpcb_limit ?? 60.0;
          const maxScale = Math.max(pol.value * 1.25, cpcbLimit * 2.2, whoLimit * 2.5, 10.0);

          const whoPercent = Math.min(95, Math.max(5, (whoLimit / maxScale) * 100));
          const cpcbPercent = Math.min(95, Math.max(5, (cpcbLimit / maxScale) * 100));
          const currentPercent = Math.min(100, Math.max(3, (pol.value / maxScale) * 100));

          const isAboveCpcb = pol.value > cpcbLimit;
          const isAboveWho = pol.value > whoLimit;

          return (
            <article
              key={pol.name}
              className="bg-white border border-[#E5E7EB] rounded-2xl p-5 shadow-xs flex flex-col justify-between transition-all hover:border-[#D1D5DB]"
            >
              <div>
                {/* Header: Name and Status Badge */}
                <div className="flex items-start justify-between gap-2">
                  <div>
                    <span className="text-xs font-bold uppercase tracking-wider text-[#6B7280]">
                      Pollutant
                    </span>
                    <h3 className="text-lg font-extrabold text-[#1F2937] leading-snug">
                      {pol.name}
                    </h3>
                  </div>

                  {/* Multiplier / Status Badge */}
                  <span
                    className={`px-2.5 py-1 rounded-full text-xs font-bold flex items-center gap-1 ${
                      isAboveCpcb
                        ? 'bg-rose-100 text-rose-800 border border-rose-200'
                        : isAboveWho
                        ? 'bg-amber-100 text-amber-900 border border-amber-200'
                        : 'bg-emerald-100 text-emerald-800 border border-emerald-200'
                    }`}
                  >
                    <span aria-hidden="true">{isAboveCpcb ? '⚠️' : isAboveWho ? '⚡' : '✅'}</span>
                    {pol.status || (isAboveCpcb ? 'Above CPCB' : isAboveWho ? 'Above WHO' : 'Safe')}
                  </span>
                </div>

                {/* Current Value Display */}
                <div className="mt-3 flex items-baseline gap-2">
                  <span className="text-3xl font-black text-[#1F2937] tracking-tight">
                    {pol.value}
                  </span>
                  <span className="text-sm font-semibold text-[#6B7280]">{pol.unit}</span>
                </div>

                {/* Multiplier string callout if elevated */}
                {(pol.cpcb_multiplier && pol.cpcb_multiplier > 1.0) ||
                (pol.who_multiplier && pol.who_multiplier > 1.0) ? (
                  <div className="mt-1 text-xs font-semibold text-[#B45309]">
                    {pol.cpcb_multiplier && pol.cpcb_multiplier > 1.0
                      ? `${pol.cpcb_multiplier}× India Limit`
                      : 'Within India Limit'}{' '}
                    • {pol.who_multiplier ? `${pol.who_multiplier}× WHO` : ''}
                  </div>
                ) : (
                  <div className="mt-1 text-xs font-semibold text-emerald-700">
                    Complies with WHO clean air thresholds
                  </div>
                )}

                {/* Dual-Threshold Progress Bar */}
                <div className="mt-4 space-y-1.5">
                  <div
                    className="relative w-full h-3.5 bg-gray-100 rounded-full overflow-hidden border border-gray-200"
                    role="progressbar"
                    aria-valuenow={pol.value}
                    aria-valuemin={0}
                    aria-valuemax={maxScale}
                    aria-label={`${pol.name} level: ${pol.value} ${pol.unit}`}
                  >
                    {/* Fill Bar */}
                    <div
                      className={`h-full rounded-full transition-all duration-300 ${
                        isAboveCpcb ? 'bg-rose-600' : isAboveWho ? 'bg-amber-500' : 'bg-emerald-500'
                      }`}
                      style={{ width: `${currentPercent}%` }}
                    />

                    {/* WHO Safe Tick Marker */}
                    <div
                      className="absolute top-0 bottom-0 w-0.5 bg-emerald-700 z-10"
                      style={{ left: `${whoPercent}%` }}
                      title={`WHO Safe Limit: ${whoLimit} ${pol.unit}`}
                    />

                    {/* CPCB Safe Tick Marker */}
                    <div
                      className="absolute top-0 bottom-0 w-0.5 bg-amber-700 z-10"
                      style={{ left: `${cpcbPercent}%` }}
                      title={`CPCB Safe Limit: ${cpcbLimit} ${pol.unit}`}
                    />
                  </div>

                  {/* Tick Labels */}
                  <div className="flex justify-between text-[11px] font-mono text-[#6B7280]">
                    <span>0</span>
                    <span className="text-emerald-700 font-bold">WHO: {whoLimit}</span>
                    <span className="text-amber-700 font-bold">CPCB: {cpcbLimit}</span>
                  </div>
                </div>
              </div>

              {/* Expandable Disclosure for Sources and Health Effects */}
              <div className="mt-4 pt-3 border-t border-gray-100">
                <button
                  type="button"
                  onClick={() => toggleExpand(idx)}
                  aria-expanded={isExpanded}
                  aria-controls={`pollutant-detail-${idx}`}
                  className="w-full text-left text-xs font-bold text-[#D97706] hover:text-[#B45309] flex items-center justify-between py-1 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-blue-600 rounded"
                >
                  <span>{isExpanded ? '▼ Hide Health & Source Details' : '▶ What happens above safe range?'}</span>
                  <span className="text-[10px] uppercase font-mono text-gray-400">CPCB / WHO</span>
                </button>

                {isExpanded && (
                  <div
                    id={`pollutant-detail-${idx}`}
                    className="mt-2.5 p-3 rounded-xl bg-[#FFFBF7] border border-[#FFE8D6] text-xs text-[#4B5563] space-y-2 animate-fadeIn"
                  >
                    <div>
                      <strong className="block text-[#1F2937] font-semibold">Primary Emission Sources:</strong>
                      <p className="mt-0.5 text-[#4B5563]">
                        {pol.primary_sources || 'Urban vehicular exhaust, industrial combustion, and road dust.'}
                      </p>
                    </div>
                    <div>
                      <strong className="block text-[#1F2937] font-semibold">Physiological Health Effect:</strong>
                      <p className="mt-0.5 text-[#4B5563]">
                        {pol.exceedance_health_effect || 'Causes airway inflammation and increased pulmonary resistance.'}
                      </p>
                    </div>
                  </div>
                )}
              </div>
            </article>
          );
        })}
      </div>
    </section>
  );
};
