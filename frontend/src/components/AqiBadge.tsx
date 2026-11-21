import React from 'react';
import { AQI_CONFIG } from '../utils/constants';

interface AqiBadgeProps {
  value: number;
  label: string;
}

export const AqiBadge: React.FC<AqiBadgeProps> = ({ value, label }) => {
  const config =
    AQI_CONFIG.find((b) => value >= b.min && value <= b.max) ||
    AQI_CONFIG[AQI_CONFIG.length - 1];

  return (
    <div
      role="status"
      aria-label={`Air Quality Index: ${value}, Category: ${label}`}
      className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full font-bold text-sm tracking-wide shadow-sm"
      style={{ backgroundColor: config.bgColor, color: config.textColor }}
    >
      <span aria-hidden="true" className="text-base">
        {config.icon}
      </span>
      <span>{label}</span>
      <span className="font-mono text-xs opacity-90">• AQI {value}</span>
    </div>
  );
};
