import React from 'react';

interface ImpactBadgeProps {
  pm25ReductionUg: number;
  cigaretteEquivalents: number;
  co2SavedG?: number;
  noxSavedMg?: number;
}

export const ImpactBadge: React.FC<ImpactBadgeProps> = ({
  pm25ReductionUg,
  cigaretteEquivalents,
  co2SavedG,
  noxSavedMg,
}) => {
  const absPm25 = Math.abs(pm25ReductionUg);
  const absCig = Math.abs(cigaretteEquivalents);

  return (
    <div
      className="flex flex-wrap items-center gap-2 mt-2.5"
      role="group"
      aria-label="Quantified direct health and emission impact metrics"
    >
      <span
        className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-md bg-emerald-50 border border-emerald-200 text-emerald-900 text-xs font-semibold"
        role="img"
        aria-label={`Reduces PM2.5 inhalation by ${absPm25.toFixed(1)} micrograms per day`}
      >
        <span aria-hidden="true">🛡️</span> −{absPm25.toFixed(1)} µg PM2.5/day
      </span>

      <span
        className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-md bg-amber-50 border border-amber-200 text-amber-900 text-xs font-semibold"
        role="img"
        aria-label={`Equivalent to ${absCig.toFixed(1)} fewer cigarettes inhaled`}
      >
        <span aria-hidden="true">🚬</span> −{absCig.toFixed(1)} cig eq.
      </span>

      {co2SavedG !== undefined && co2SavedG > 0 && (
        <span
          className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-md bg-teal-50 border border-teal-200 text-teal-900 text-xs font-semibold"
          role="img"
          aria-label={`Saves ${(co2SavedG / 1000).toFixed(1)} kilograms of carbon dioxide per week`}
        >
          <span aria-hidden="true">🌱</span> −{(co2SavedG / 1000).toFixed(1)} kg CO₂/wk
        </span>
      )}

      {noxSavedMg !== undefined && noxSavedMg > 0 && (
        <span
          className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-md bg-sky-50 border border-sky-200 text-sky-900 text-xs font-semibold"
          role="img"
          aria-label={`Avoids ${(noxSavedMg / 1000).toFixed(2)} grams of ground-level toxic nitrogen oxides per week`}
        >
          <span aria-hidden="true">⚡</span> −{(noxSavedMg / 1000).toFixed(2)} g NOx/wk
        </span>
      )}
    </div>
  );
};
