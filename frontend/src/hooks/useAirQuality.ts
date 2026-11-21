import { useState, useEffect, useCallback } from 'react';
import { AirQualityData } from '../types';

const API_BASE = import.meta.env.VITE_API_BASE_URL || '';

export function useAirQuality(initialLat = 28.6139, initialLon = 77.209) {
  const [data, setData] = useState<AirQualityData | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const [coords, setCoords] = useState<{ lat: number; lon: number; label?: string }>({
    lat: initialLat,
    lon: initialLon,
    label: 'Delhi-NCR',
  });

  const fetchAQI = useCallback(async (lat: number, lon: number, city?: string, pincode?: string) => {
    setIsLoading(true);
    setError(null);
    try {
      const base = API_BASE || (typeof window !== 'undefined' ? window.location.origin : 'http://localhost:8000');
      const url = new URL(`${base}/api/air-quality`);
      url.searchParams.set('lat', lat.toString());
      url.searchParams.set('lon', lon.toString());
      if (city) url.searchParams.set('city', city);
      if (pincode) url.searchParams.set('pincode', pincode);

      const resp = await fetch(url.toString());
      if (!resp.ok) {
        throw new Error(`Failed to load air quality: ${resp.statusText}`);
      }
      const json: AirQualityData = await resp.json();
      setData(json);
      setCoords({ lat: json.lat, lon: json.lon, label: json.location_label });
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : 'Failed to fetch AQI');
    } finally {
      setIsLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchAQI(coords.lat, coords.lon);
  }, [fetchAQI, coords.lat, coords.lon]);

  const searchLocation = useCallback(
    async (query: string) => {
      // If numeric, query as pincode; else query as city
      const isPincode = /^\d{6}$/.test(query);
      if (isPincode) {
        // Sample coords for Delhi / Noida / Gurugram pincodes
        if (query.startsWith('110')) fetchAQI(28.6139, 77.209, undefined, query);
        else if (query.startsWith('201')) fetchAQI(28.5355, 77.391, undefined, query);
        else if (query.startsWith('122')) fetchAQI(28.4595, 77.0266, undefined, query);
        else fetchAQI(coords.lat, coords.lon, undefined, query);
      } else {
        const lower = query.toLowerCase();
        if (lower.includes('noida')) fetchAQI(28.5355, 77.391, 'Noida');
        else if (lower.includes('gurugram') || lower.includes('gurgaon')) fetchAQI(28.4595, 77.0266, 'Gurugram');
        else fetchAQI(28.6139, 77.209, query);
      }
    },
    [fetchAQI, coords.lat, coords.lon]
  );

  return {
    data,
    isLoading,
    error,
    coords,
    setCoords: (lat: number, lon: number, label?: string) => {
      setCoords({ lat, lon, label });
      fetchAQI(lat, lon, label);
    },
    searchLocation,
    refetch: () => fetchAQI(coords.lat, coords.lon),
  };
}
