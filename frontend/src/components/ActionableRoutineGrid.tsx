import React, { useState, useMemo, useEffect } from 'react';
import { ActionPlanCard, RoutinePlanResponse } from '../types';

interface ActionableRoutineGridProps {
  plan: RoutinePlanResponse;
}

type FilterCategory = 'All' | 'Routine' | 'Indoor Hack' | 'Sustainable Swap' | 'Mask & Commute';

export const ActionableRoutineGrid: React.FC<ActionableRoutineGridProps> = ({ plan }) => {
  const [selectedFilter, setSelectedFilter] = useState<FilterCategory>('All');
  const [completedCardIds, setCompletedCardIds] = useState<Set<string>>(new Set());
  const [expandedCardIds, setExpandedCardIds] = useState<Set<string>>(new Set());

  // Reset checkboxes when a new plan is generated
  useEffect(() => {
    setCompletedCardIds(new Set());
    setExpandedCardIds(new Set());
  }, [plan.generated_at]);

  // Adapt fallback cards if plan.action_cards is empty
  const allCards: ActionPlanCard[] = useMemo(() => {
    if (plan.action_cards && plan.action_cards.length > 0) {
      return plan.action_cards;
    }

    // Graceful fallback from legacy routine list
    const fallback: ActionPlanCard[] = [];
    plan.routines.forEach((r, i) => {
      fallback.push({
        id: `routine-${i}`,
        title: `${r.time_slot} Routine`,
        category: 'Routine',
        budget_tier: 'Free/DIY',
        action_detail: r.action,
        quantified_impact: {
          pm25_reduction_pct: 45.0,
          co2_saved_kg_week: 0.0,
          summary_badge: `-${r.impact.pm25_reduction_ug_per_day} µg PM2.5/day`,
        },
        why_it_works: r.rationale,
        source_citation: r.source,
      });
    });

    plan.indoor_hacks.forEach((h, i) => {
      fallback.push({
        id: `hack-${i}`,
        title: h.title,
        category: 'Indoor Hack',
        budget_tier: h.estimated_cost_inr === 0 ? 'Free/DIY' : 'Low-Cost',
        action_detail: h.description,
        quantified_impact: {
          pm25_reduction_pct: h.effectiveness_pct,
          co2_saved_kg_week: 0.0,
          summary_badge: `-${h.impact.pm25_reduction_ug_per_day} µg PM2.5/day`,
        },
        why_it_works: `Reduces indoor particulate infiltration and improves room CADR.`,
        source_citation: h.source,
      });
    });

    plan.sustainable_swaps.forEach((s, i) => {
      fallback.push({
        id: `swap-${i}`,
        title: `Shift to ${s.swap_to}`,
        category: 'Sustainable Swap',
        budget_tier: 'Free/DIY',
        action_detail: s.rationale,
        quantified_impact: {
          pm25_reduction_pct: 75.0,
          co2_saved_kg_week: Number(((s.impact.co2_saved_g_per_week || 0) / 1000).toFixed(1)),
          summary_badge: `-${s.impact.pm25_reduction_ug_per_day} µg PM2.5/day`,
        },
        why_it_works: `Avoids tailpipe and solid-fuel combustion emissions directly at source.`,
        source_citation: s.source,
      });
    });

    return fallback;
  }, [plan]);

  // Filtered cards based on active tab
  const filteredCards = useMemo(() => {
    if (selectedFilter === 'All') return allCards;
    return allCards.filter((c) => c.category === selectedFilter);
  }, [allCards, selectedFilter]);

  // Toggle card completion
  const toggleComplete = (id: string) => {
    setCompletedCardIds((prev) => {
      const next = new Set(prev);
      if (next.has(id)) next.delete(id);
      else next.add(id);
      return next;
    });
  };

  // Toggle citation expand
  const toggleCitation = (id: string) => {
    setExpandedCardIds((prev) => {
      const next = new Set(prev);
      if (next.has(id)) next.delete(id);
      else next.add(id);
      return next;
    });
  };

  // Dynamic impact metrics based on checked state
  const checkedCount = completedCardIds.size;
  const dynamicCo2SavedKg = useMemo(() => {
    let co2 = 0;
    allCards.forEach((c) => {
      if (completedCardIds.has(c.id)) {
        co2 += c.quantified_impact.co2_saved_kg_week;
      }
    });
    return co2.toFixed(1);
  }, [allCards, completedCardIds]);

  const dynamicAvgPm25Reduction = useMemo(() => {
    if (checkedCount === 0) return 0;
    let sumPct = 0;
    allCards.forEach((c) => {
      if (completedCardIds.has(c.id)) {
        sumPct += c.quantified_impact.pm25_reduction_pct;
      }
    });
    return Math.round(sumPct / checkedCount);
  }, [allCards, completedCardIds, checkedCount]);

  // Formatted plan generation time
  const formattedTime = useMemo(() => {
    try {
      return new Date(plan.generated_at).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' });
    } catch {
      return 'Just now';
    }
  }, [plan.generated_at]);

  return (
    <div className="space-y-8 animate-fadeIn">
      {/* 0. Dynamic Plan Timestamp & Personalization Feedback Banner */}
      <div className="flex flex-wrap items-center justify-between gap-3 p-4 bg-emerald-50/70 border border-emerald-200 rounded-2xl shadow-2xs">
        <div className="flex items-center gap-2.5 text-xs sm:text-sm font-extrabold text-emerald-950">
          <span className="p-1 bg-emerald-200 rounded-lg text-sm" aria-hidden="true">
            ⚡
          </span>
          <span>Personalized Plan Dynamically Computed</span>
          <span className="text-xs font-semibold text-emerald-700 bg-white px-2 py-0.5 rounded-md border border-emerald-200">
            Updated at {formattedTime}
          </span>
        </div>
        <div className="text-xs text-emerald-900 font-bold flex items-center gap-1.5">
          <span className="w-2.5 h-2.5 rounded-full bg-emerald-500 animate-pulse" aria-hidden="true" />
          <span>{allCards.length} Tailored Interventions Loaded</span>
        </div>
      </div>

      {/* 1. Total Aggregated Impact Hero Card (Pillar 4) */}
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
            <p className="text-sm text-gray-300 mt-1 max-w-xl">
              Deterministic calculations based on ICRP-66 respiratory minute ventilation rates and CPCB transport emission inventories for your selected profile.
            </p>
          </div>

          <div className="grid grid-cols-2 sm:grid-cols-3 gap-3 sm:gap-4">
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

        {/* Dynamic Checked Progress Tracker */}
        <div
          role="region"
          aria-live="polite"
          className="mt-6 pt-5 border-t border-white/10 flex flex-col sm:flex-row sm:items-center justify-between gap-4"
        >
          <div className="flex items-center gap-3">
            <div className="p-2.5 rounded-xl bg-emerald-500/20 border border-emerald-400/30 text-emerald-300 text-xl font-bold">
              ✓
            </div>
            <div>
              <span className="text-xs uppercase font-bold tracking-wider text-emerald-300">
                Your Active Action Check-in Tracker
              </span>
              <p className="text-sm text-gray-200 font-medium">
                Completed{' '}
                <strong className="text-white font-extrabold">
                  {checkedCount} of {allCards.length}
                </strong>{' '}
                actions today
              </p>
            </div>
          </div>

          <div className="flex flex-wrap items-center gap-3">
            <span className="px-3 py-1.5 rounded-xl bg-white/10 text-xs font-bold text-emerald-300 border border-emerald-400/20">
              Avg Inhalation Reduced: {dynamicAvgPm25Reduction}%
            </span>
            <span className="px-3 py-1.5 rounded-xl bg-white/10 text-xs font-bold text-teal-300 border border-teal-400/20">
              CO₂ Shift Checked: −{dynamicCo2SavedKg} kg/wk
            </span>
          </div>
        </div>
      </section>

      {/* 2. Interactive Action Plan Cards with Category Filters */}
      <section aria-labelledby="action-plan-heading" className="space-y-6">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div>
            <div className="flex items-center gap-2">
              <span className="text-2xl" aria-hidden="true">
                🎯
              </span>
              <h2 id="action-plan-heading" className="text-xl sm:text-2xl font-bold text-[#1F2937]">
                Actionable Low-Emission & Smog Defense Plan
              </h2>
            </div>
            <p className="text-xs sm:text-sm text-[#4B5563] mt-0.5">
              Interactive, budget-tiered interventions tailored to your commute, household, and building type.
            </p>
          </div>

          {/* Category Filter Tabs */}
          <div
            role="tablist"
            aria-label="Filter action categories"
            className="flex flex-wrap gap-2 bg-[#FFE8D6]/60 p-1.5 rounded-2xl border border-[#FFDAB9] self-start md:self-auto"
          >
            {(['All', 'Routine', 'Indoor Hack', 'Sustainable Swap', 'Mask & Commute'] as FilterCategory[]).map(
              (category) => {
                const isSelected = selectedFilter === category;
                return (
                  <button
                    key={category}
                    role="tab"
                    type="button"
                    aria-selected={isSelected}
                    onClick={() => setSelectedFilter(category)}
                    className={`px-3.5 py-1.5 rounded-xl text-xs font-bold transition-all duration-150 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-blue-600 ${
                      isSelected
                        ? 'bg-[#1F2937] text-white shadow-xs'
                        : 'bg-transparent text-[#1F2937] hover:bg-white/60'
                    }`}
                  >
                    {category}
                  </button>
                );
              }
            )}
          </div>
        </div>

        {/* Action Cards Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-5 sm:gap-6">
          {filteredCards.map((card) => {
            const isCompleted = completedCardIds.has(card.id);
            const isCitationOpen = expandedCardIds.has(card.id);

            return (
              <article
                key={card.id}
                className={`rounded-2xl p-5 sm:p-6 border transition-all flex flex-col justify-between ${
                  isCompleted
                    ? 'bg-emerald-50/60 border-emerald-300 shadow-2xs'
                    : 'bg-white border-[#E5E7EB] hover:border-[#D1D5DB] shadow-xs'
                }`}
              >
                <div>
                  {/* Top Bar: Checkbox, Category, Budget Tier */}
                  <div className="flex items-start justify-between gap-3">
                    <div className="flex items-center gap-3">
                      <input
                        id={`check-${card.id}`}
                        type="checkbox"
                        checked={isCompleted}
                        onChange={() => toggleComplete(card.id)}
                        aria-label={`Mark "${card.title}" as completed`}
                        className="w-5 h-5 rounded-md border-[#D1D5DB] text-emerald-600 focus:ring-emerald-500 cursor-pointer"
                      />
                      <label htmlFor={`check-${card.id}`} className="cursor-pointer">
                        <span className="text-[11px] font-extrabold uppercase tracking-wider text-[#6B7280]">
                          {card.category}
                        </span>
                      </label>
                    </div>

                    <span
                      className={`px-2.5 py-0.5 rounded-full text-[11px] font-bold uppercase tracking-wider ${
                        card.budget_tier === 'Free/DIY'
                          ? 'bg-emerald-100 text-emerald-900 border border-emerald-200'
                          : card.budget_tier === 'Low-Cost'
                          ? 'bg-amber-100 text-amber-900 border border-amber-200'
                          : 'bg-purple-100 text-purple-900 border border-purple-200'
                      }`}
                    >
                      {card.budget_tier}
                    </span>
                  </div>

                  {/* Card Title */}
                  <h3
                    className={`mt-3 text-base sm:text-lg font-bold leading-snug transition-colors ${
                      isCompleted ? 'line-through text-[#6B7280]' : 'text-[#1F2937]'
                    }`}
                  >
                    {card.title}
                  </h3>

                  {/* Action Detail */}
                  <p className="mt-2 text-xs sm:text-sm text-[#4B5563] leading-relaxed">
                    {card.action_detail}
                  </p>
                </div>

                {/* Footer: Quantified Impact Badge and Citation Disclosure */}
                <div className="mt-5 pt-4 border-t border-[#F3F4F6]">
                  <div className="flex items-center justify-between gap-2 flex-wrap">
                    <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-xl text-xs font-extrabold bg-[#FFE8D6] text-[#78350F] border border-[#FFDAB9]">
                      <span aria-hidden="true">⚡</span>
                      {card.quantified_impact.summary_badge}
                    </span>

                    {card.quantified_impact.co2_saved_kg_week > 0 && (
                      <span className="inline-flex items-center gap-1 px-2.5 py-1 rounded-xl text-xs font-extrabold bg-teal-50 text-teal-800 border border-teal-200">
                        🌱 −{card.quantified_impact.co2_saved_kg_week} kg CO₂/wk
                      </span>
                    )}
                  </div>

                  {/* Expandable Why This Works • Citation */}
                  <div className="mt-3.5">
                    <button
                      type="button"
                      onClick={() => toggleCitation(card.id)}
                      aria-expanded={isCitationOpen}
                      aria-controls={`citation-${card.id}`}
                      className="text-xs font-bold text-[#D97706] hover:text-[#B45309] cursor-pointer flex items-center gap-1 py-1 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-blue-600 rounded"
                    >
                      <span>{isCitationOpen ? '▼' : '▶'}</span>
                      <span>Why this works • Scientific source citation</span>
                    </button>

                    {isCitationOpen && (
                      <div
                        id={`citation-${card.id}`}
                        className="mt-2.5 text-xs text-[#4B5563] bg-[#FFFBF7] p-3 rounded-xl border border-[#FFE8D6] font-mono leading-relaxed space-y-1.5 animate-fadeIn"
                      >
                        <p>
                          <strong className="text-[#1F2937]">Mechanism:</strong> {card.why_it_works}
                        </p>
                        <p className="text-[#6B7280]">
                          <strong className="text-[#1F2937]">Source:</strong> {card.source_citation}
                        </p>
                      </div>
                    )}
                  </div>
                </div>
              </article>
            );
          })}
        </div>
      </section>
    </div>
  );
};
