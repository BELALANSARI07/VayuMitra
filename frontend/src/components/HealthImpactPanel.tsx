import React, { useState } from 'react';
import { HealthImpactData } from '../types';

interface HealthImpactPanelProps {
  healthImpact?: HealthImpactData;
  cigaretteEquivalent?: number;
  aqiValue?: number;
  aqiLabel?: string;
}

export const HealthImpactPanel: React.FC<HealthImpactPanelProps> = ({
  healthImpact,
  cigaretteEquivalent,
  aqiValue = 250,
  aqiLabel = 'Poor',
}) => {
  const [isRisksExpanded, setIsRisksExpanded] = useState<boolean>(true);

  if (!healthImpact) return null;

  const cigCount = cigaretteEquivalent ?? Number((aqiValue / 22.0).toFixed(1));
  const hasRedFlags = healthImpact.red_flag_symptoms && healthImpact.red_flag_symptoms.length > 0;

  return (
    <section aria-labelledby="health-impact-heading" className="space-y-6">
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-2">
        <div>
          <div className="flex items-center gap-2">
            <span className="text-2xl" aria-hidden="true">
              🫁
            </span>
            <h2 id="health-impact-heading" className="text-xl sm:text-2xl font-bold text-[#1F2937]">
              Clinical Health Impact & Physiological Risk Assessment
            </h2>
          </div>
          <p className="text-xs sm:text-sm text-[#4B5563] mt-0.5">
            CPCB NAQI band clinical mapping & Berkeley Earth particulate toxicological equivalences.
          </p>
        </div>
        <span className="px-3 py-1 rounded-full text-xs font-bold uppercase tracking-wider bg-[#FFE8D6] text-[#78350F] border border-[#FFDAB9] self-start sm:self-auto">
          Current Band: {healthImpact.category_label || aqiLabel} (AQI {aqiValue})
        </span>
      </div>

      {/* 1. Prominent Cigarette Equivalent Callout */}
      <div className="bg-gradient-to-r from-amber-500/10 via-rose-500/10 to-amber-500/10 border-2 border-amber-300 rounded-3xl p-6 sm:p-7 shadow-xs">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div className="flex items-start sm:items-center gap-4">
            <div className="p-3.5 bg-amber-100 rounded-2xl border border-amber-200 text-3xl" aria-hidden="true">
              🚬
            </div>
            <div>
              <span className="text-xs font-bold uppercase tracking-wider text-amber-800">
                Toxicological Particulate Equivalence (Berkeley Earth Rule)
              </span>
              <h3 className="text-xl sm:text-2xl font-black text-[#1F2937] mt-0.5">
                Breathing outdoor air for 24h ≈{' '}
                <span className="text-rose-700 underline decoration-rose-300 decoration-wavy decoration-2">
                  {cigCount} cigarettes
                </span>
              </h3>
              <p className="text-xs text-[#4B5563] mt-1 font-medium">
                Calculated deterministically using Muller & Berkeley Lab toxicological conversion (22 µg/m³ PM2.5 in 24h ≈ 1 cigarette smoked).
              </p>
            </div>
          </div>

          <div className="bg-white/80 border border-amber-200 px-4 py-2.5 rounded-2xl text-center self-start sm:self-center shrink-0">
            <span className="block text-2xl font-black text-rose-700">
              {cigCount} / day
            </span>
            <span className="text-[11px] font-bold text-[#6B7280] uppercase tracking-wider">
              Smoked Equivalents
            </span>
          </div>
        </div>
      </div>

      {/* 2. Side-by-Side Comparison: Healthy Adults vs. Sensitive Demographics */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Healthy Adults */}
        <div className="bg-white border border-[#E5E7EB] rounded-2xl p-6 shadow-xs flex flex-col justify-between">
          <div>
            <div className="flex items-center gap-2 mb-3">
              <span className="text-xl" aria-hidden="true">
                🏃
              </span>
              <h3 className="text-base font-bold text-[#1F2937]">
                Impact on Healthy Adults
              </h3>
            </div>
            <p className="text-sm text-[#374151] leading-relaxed">
              {healthImpact.healthy_adults_impact}
            </p>
          </div>
          <div className="mt-4 pt-3 border-t border-gray-100 text-xs text-[#6B7280] font-medium flex items-center gap-2">
            <span className="w-2 h-2 rounded-full bg-blue-500" aria-hidden="true" />
            Advisory: Limit high-intensity outdoor stamina drills during peak smog hours.
          </div>
        </div>

        {/* Sensitive Groups */}
        <div className="bg-amber-50/50 border border-amber-200 rounded-2xl p-6 shadow-xs flex flex-col justify-between">
          <div>
            <div className="flex items-center gap-2 mb-3">
              <span className="text-xl" aria-hidden="true">
                🛡️
              </span>
              <h3 className="text-base font-bold text-[#92400E]">
                Sensitive & Vulnerable Groups
              </h3>
            </div>
            <p className="text-sm text-[#78350F] leading-relaxed font-medium">
              {healthImpact.sensitive_groups_impact}
            </p>
          </div>
          <div className="mt-4 pt-3 border-t border-amber-200 text-xs text-[#92400E] font-medium flex items-center gap-2">
            <span className="w-2 h-2 rounded-full bg-rose-500" aria-hidden="true" />
            Includes: Children (&lt;10 yrs), Seniors (65+), Asthmatics, Pregnant women, Heart patients.
          </div>
        </div>
      </div>

      {/* 3. Collapsible Short-Term vs. Long-Term Risks */}
      <div className="bg-white border border-[#E5E7EB] rounded-2xl p-5 shadow-xs">
        <button
          type="button"
          onClick={() => setIsRisksExpanded((prev) => !prev)}
          aria-expanded={isRisksExpanded}
          aria-controls="short-long-term-risks"
          className="w-full flex items-center justify-between text-left font-bold text-sm text-[#1F2937] py-1 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-blue-600 rounded"
        >
          <span className="flex items-center gap-2">
            <span className="text-lg" aria-hidden="true">
              ⏱️
            </span>
            Clinical Risk Timelines (Short-Term Exposure vs. Long-Term Cumulative Damage)
          </span>
          <span className="text-xs text-[#D97706] font-mono">
            {isRisksExpanded ? '▲ Collapse' : '▼ View Details'}
          </span>
        </button>

        {isRisksExpanded && (
          <div
            id="short-long-term-risks"
            className="mt-4 pt-4 border-t border-gray-100 grid grid-cols-1 md:grid-cols-2 gap-6 animate-fadeIn"
          >
            <div className="space-y-1.5">
              <span className="text-xs font-bold uppercase tracking-wider text-amber-700 block">
                ⚡ Acute Short-Term Physiological Risks (Hours to Days)
              </span>
              <p className="text-xs sm:text-sm text-[#4B5563] leading-relaxed">
                {healthImpact.short_term_risks}
              </p>
            </div>

            <div className="space-y-1.5">
              <span className="text-xs font-bold uppercase tracking-wider text-rose-700 block">
                🏥 Chronic Long-Term Cumulative Risks (Months to Years)
              </span>
              <p className="text-xs sm:text-sm text-[#4B5563] leading-relaxed">
                {healthImpact.long_term_risks}
              </p>
            </div>
          </div>
        )}
      </div>

      {/* 4. High-Contrast Red-Flag Symptoms Alert Strip */}
      {hasRedFlags && (
        <div
          role="alert"
          aria-live="polite"
          className="bg-rose-50 border-2 border-rose-400 rounded-2xl p-5 text-rose-950 flex flex-col sm:flex-row sm:items-center justify-between gap-4 shadow-xs"
        >
          <div className="flex items-start gap-3">
            <span className="text-2xl text-rose-700 shrink-0" aria-hidden="true">
              🚨
            </span>
            <div>
              <strong className="block text-sm sm:text-base font-extrabold text-rose-900">
                Red-Flag Clinical Symptoms — Seek Medical Care if Experiencing:
              </strong>
              <div className="mt-2 flex flex-wrap gap-2">
                {healthImpact.red_flag_symptoms.map((symptom, idx) => (
                  <span
                    key={idx}
                    className="inline-flex items-center gap-1 px-3 py-1 rounded-full text-xs font-bold bg-white text-rose-900 border border-rose-300 shadow-2xs"
                  >
                    <span className="text-rose-600" aria-hidden="true">
                      ⚠️
                    </span>
                    {symptom}
                  </span>
                ))}
              </div>
            </div>
          </div>

          <div className="shrink-0 text-xs text-rose-800 font-semibold bg-white/70 px-3 py-2 rounded-xl border border-rose-200">
            Immediate Action: Inhale prescribed bronchodilator & isolate in HEPA room.
          </div>
        </div>
      )}
    </section>
  );
};
