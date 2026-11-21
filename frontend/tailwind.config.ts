import type { Config } from 'tailwindcss';

export default {
  content: ['./index.html', './src/**/*.{js,ts,jsx,tsx}'],
  theme: {
    extend: {
      colors: {
        'vayu-bg': '#FFFBF7',
        'vayu-peach': '#FFE8D6',
        'vayu-peach-dark': '#FFDAB9',
        'vayu-charcoal': '#1F2937',
        'vayu-gray': '#4B5563',
      },
    },
  },
  plugins: [],
} satisfies Config;
