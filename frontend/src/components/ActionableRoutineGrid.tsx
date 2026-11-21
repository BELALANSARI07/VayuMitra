import React from 'react';
import { RoutinePlanResponse } from '../types';
import { ImpactBadge } from './ImpactBadge';

interface ActionableRoutineGridProps {
  plan: RoutinePlanResponse;
}

export const ActionableRoutineGrid: React.FC<ActionableRoutineGridProps> = ({ plan }) => {
  return (
    <div className="space-y-10">
      {/* Total Aggregated Impact Hero Card (Pillar 4) */}
      <section
        aria-labelledby="total-impact-heading"
        className="bg-gradient-to-br from-[#1F2937] to-[#111827] text-white rounded-3xl p-6 sm:p-8 shadow-lg"
      >
        <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-6">
          <div>
            <div className="flex items-center gap-2">
              <span className="text-2xl" aria-hidden="true">
                📊
              </span>
              <h2 id="total-impact-heading" className="text-xl sm:text-2xl font-extrabold tracking-tight">
                Quantified Daily Impact Summary
              </h2>
            </div>
            <p className="text-sm text-gray-300 mt-1">
              Deterministic calculations based on ICRP-66 respiratory minute ventilation rates and CPCB transport emission inventories.
            </p>
          </div>

          <div className="grid grid-cols-2 sm:grid-cols-3 gap-4">
            <div className="bg-white/10 backdrop-blur-sm border border-white/10 rounded-2xl p-4">
              <span className="block text-xs uppercase font-bold text-gray-300 tracking-wider">
                PM2.5 Avoided
              </span>
              <span className="block text-2xl sm:text-3xl font-black text-emerald-400 mt-1">
                −{plan.total_impact.pm25_reduction_ug_per_day} <span className="text-sm font-semibold">µg/day</span>
              </span>
            </div>

            <div className="bg-white/10 backdrop-blur-sm border border-white/10 rounded-2xl p-4">
              <span className="block text-xs uppercase font-bold text-gray-300 tracking-wider">
                Cigarette Eq.
              </span>
              <span className="block text-2xl sm:text-3xl font-black text-amber-300 mt-1">
                −{plan.total_impact.cigarette_equivalents_saved} <span className="text-sm font-semibold">fewer</span>
              </span>
            </div>

            {plan.total_impact.co2_saved_g_per_week ? (
              <div className="bg-white/10 backdrop-blur-sm border border-white/10 rounded-2xl p-4 col-span-2 sm:col-span-1">
                <span className="block text-xs uppercase font-bold text-gray-300 tracking-wider">
                  Carbon Avoided
                </span>
                <span className="block text-2xl sm:text-3xl font-black text-teal-300 mt-1">
                  −{(plan.total_impact.co2_saved_g_per_week / 1000).toFixed(1)}{' '}
                  <span className="text-sm font-semibold">kg CO₂/wk</span>
                </span>
              </div>
            ) : null}
          </div>
        </div>

        <div className="mt-5 pt-4 border-t border-white/10 text-xs text-gray-400 font-mono">
          <strong>Deterministic Formula:</strong> {plan.total_impact.formula_ref}
        </div>
      </section>

      {/* Pillar 1: Low-Emission Daily Routines */}
      <section aria-labelledby="routines-heading">
        <div className="flex items-center gap-2 mb-4">
          <span className="text-2xl" aria-hidden="true">
            ⏱️
          </span>
          <div>
            <h2 id="routines-heading" className="text-xl sm:text-2xl font-bold text-[#1F2937]">
              Pillar 1: Time-Shifted Daily Routines
            </h2>
            <p className="text-sm text-[#4B5563]">
              Optimized outdoor activity, commute windows, and cooking ventilation schedules.
            </p>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {plan.routines.map((routine, idx) => (
            <article
              key={idx}
              className="bg-[#FFFBF7] border border-[#FFE8D6] rounded-2xl p-5 shadow-sm flex flex-col justify-between"
            >
              <div>
                <span className="inline-block px-3 py-1 rounded-full text-xs font-bold uppercase tracking-wide bg-[#FFE8D6] text-[#78350F] mb-3">
                  {routine.time_slot}
                </span>
                <h3 className="text-base font-bold text-[#1F2937] leading-snug">
                  {routine.action}
                </h3>
                <p className="text-xs text-[#4B5563] mt-2 leading-relaxed">
                  {routine.rationale}
                </p>
              </div>

              <div className="mt-4 pt-4 border-t border-[#FFE8D6]">
                <ImpactBadge
                  pm25ReductionUg={routine.impact.pm25_reduction_ug_per_day}
                  cigaretteEquivalents={routine.impact.cigarette_equivalents_saved}
                />

                <details className="mt-3 group">
                  <summary className="text-xs font-bold text-[#D97706] hover:text-[#B45309] cursor-pointer flex items-center gap-1 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-blue-600 rounded">
                    <span>▶</span> Why this works • Source citation
                  </summary>
                  <div className="mt-2 text-xs text-[#4B5563] bg-white p-3 rounded-xl border border-[#E5E7EB] font-mono leading-relaxed">
                    <p className="font-semibold text-[#1F2937]">Citation: {routine.source}</p>
                    <p className="text-[11px] text-[#6B7280] mt-1 break-all">{routine.impact.formula_ref}</p>
                  </div>
                </details>
              </div>
            </article>
          ))}
        </div>
      </section>

      {/* Pillar 2: Budget-Tiered Indoor Air Hacks */}
      <section aria-labelledby="indoor-hacks-heading">
        <div className="flex items-center gap-2 mb-4">
          <span className="text-2xl" aria-hidden="true">
            🏠
          </span>
          <div>
            <h2 id="indoor-hacks-heading" className="text-xl sm:text-2xl font-bold text-[#1F2937]">
              Pillar 2: Budget-Tiered Indoor Air Hacks
            </h2>
            <p className="text-sm text-[#4B5563]">
              From ₹0 behavioral fixes to DIY box-fan filtration and bedroom sealing sanctuaries.
            </p>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {plan.indoor_hacks.map((hack, idx) => (
            <article
              key={idx}
              className="bg-white border border-[#E5E7EB] rounded-2xl p-5 shadow-sm flex flex-col justify-between"
            >
              <div>
                <div className="flex items-center justify-between gap-2 mb-2">
                  <span className="px-2.5 py-0.5 rounded-full text-xs font-bold uppercase tracking-wide bg-[#FFE8D6] text-[#78350F]">
                    {hack.budget_tier.toUpperCase()} TIER • {hack.estimated_cost_inr === 0 ? 'FREE (₹0)' : `~₹${hack.estimated_cost_inr}`}
                  </span>
                  <span className="text-xs font-extrabold text-emerald-700 bg-emerald-50 px-2.5 py-0.5 rounded-full border border-emerald-200">
                    {hack.effectiveness_pct}% Effective
                  </span>
                </div>
                <h3 className="text-base font-bold text-[#1F2937] leading-snug">
                  {hack.title}
                </h3>
                <p className="text-xs text-[#4B5563] mt-2 leading-relaxed">
                  {hack.description}
                </p>
              </div>

              <div className="mt-4 pt-4 border-t border-[#F3F4F6]">
                <ImpactBadge
                  pm25ReductionUg={hack.impact.pm25_reduction_ug_per_day}
                  cigaretteEquivalents={hack.impact.cigarette_equivalents_saved}
                />

                <details className="mt-3 group">
                  <summary className="text-xs font-bold text-[#D97706] hover:text-[#B45309] cursor-pointer flex items-center gap-1 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-blue-600 rounded">
                    <span>▶</span> Scientific Validation & Source
                  </summary>
                  <div className="mt-2 text-xs text-[#4B5563] bg-[#FFFBF7] p-3 rounded-xl border border-[#FFE8D6] font-mono leading-relaxed">
                    <p className="font-semibold text-[#1F2937]">Source: {hack.source}</p>
                    <p className="text-[11px] text-[#6B7280] mt-1 break-all">{hack.impact.formula_ref}</p>
                  </div>
                </details>
              </div>
            </article>
          ))}
        </div>
      </section>

      {/* Pillar 3: Sustainable Alternatives & Modal Shifts */}
      <section aria-labelledby="swaps-heading">
        <div className="flex items-center gap-2 mb-4">
          <span className="text-2xl" aria-hidden="true">
            🌱
          </span>
          <div>
            <h2 id="swaps-heading" className="text-xl sm:text-2xl font-bold text-[#1F2937]">
              Pillar 3: Sustainable Alternatives & Mode Shifts
            </h2>
            <p className="text-sm text-[#4B5563]">
              Cleaner transport and domestic energy choices tailored to your commute and cooking habits.
            </p>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {plan.sustainable_swaps.map((swap, idx) => (
            <article
              key={idx}
              className="bg-[#FFFBF7] border border-[#FFE8D6] rounded-2xl p-5 shadow-sm flex flex-col justify-between"
            >
              <div>
                <div className="flex items-center gap-2 text-xs font-extrabold uppercase text-[#6B7280] mb-2">
                  <span className="line-through">{swap.swap_from}</span>
                  <span>➔</span>
                  <span className="text-emerald-700 bg-emerald-50 px-2 py-0.5 rounded border border-emerald-200">
                    {swap.swap_to}
                  </span>
                </div>
                <h3 className="text-base font-bold text-[#1F2937] leading-snug">
                  Shift to {swap.swap_to}
                </h3>
                <p className="text-xs text-[#4B5563] mt-2 leading-relaxed">
                  {swap.rationale}
                </p>
              </div>

              <div className="mt-4 pt-4 border-t border-[#FFE8D6]">
                <ImpactBadge
                  pm25ReductionUg={swap.impact.pm25_reduction_ug_per_day}
                  cigaretteEquivalents={swap.impact.cigarette_equivalents_saved}
                  co2SavedG={swap.impact.co2_saved_g_per_week}
                  noxSavedMg={swap.impact.nox_saved_mg_per_week}
                />

                <details className="mt-3 group">
                  <summary className="text-xs font-bold text-[#D97706] hover:text-[#B45309] cursor-pointer flex items-center gap-1 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-blue-600 rounded">
                    <span>▶</span> CPCB Inventory Citation & Formula
                  </summary>
                  <div className="mt-2 text-xs text-[#4B5563] bg-white p-3 rounded-xl border border-[#E5E7EB] font-mono leading-relaxed">
                    <p className="font-semibold text-[#1F2937]">Source: {swap.source}</p>
                    <p className="text-[11px] text-[#6B7280] mt-1 break-all">{swap.impact.formula_ref}</p>
                  </div>
                </details>
              </div>
            </article>
          ))}
        </div>
      </section>
    </div>
  );
};
