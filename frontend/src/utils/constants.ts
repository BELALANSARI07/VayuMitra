export interface DemoPreset {
  label: string;
  pincode: string;
  lat: number;
  lon: number;
}

export const DEMO_PRESETS: DemoPreset[] = [
  { label: 'Delhi-NCR', pincode: '110001', lat: 28.6139, lon: 77.209 },
  { label: 'Noida', pincode: '201301', lat: 28.5355, lon: 77.391 },
  { label: 'Gurugram', pincode: '122001', lat: 28.4595, lon: 77.0266 },
];

export interface AqiBandConfig {
  label: string;
  min: number;
  max: number;
  bgColor: string;
  textColor: string;
  icon: string;
}

export const AQI_CONFIG: AqiBandConfig[] = [
  { label: 'Good', min: 0, max: 50, bgColor: '#15803D', textColor: '#FFFFFF', icon: '🟢' },
  { label: 'Satisfactory', min: 51, max: 100, bgColor: '#65A30D', textColor: '#FFFFFF', icon: '🟡' },
  { label: 'Moderate', min: 101, max: 200, bgColor: '#A16207', textColor: '#FFFFFF', icon: '🟠' },
  { label: 'Poor', min: 201, max: 300, bgColor: '#C2410C', textColor: '#FFFFFF', icon: '🔴' },
  { label: 'Very Poor', min: 301, max: 400, bgColor: '#DC2626', textColor: '#FFFFFF', icon: '🟣' },
  { label: 'Severe', min: 401, max: 500, bgColor: '#7C3AED', textColor: '#FFFFFF', icon: '⚠️' },
];
