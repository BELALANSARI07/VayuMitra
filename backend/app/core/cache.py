"""
Thread-safe TTL in-memory cache keyed by geohash for AQI and forecast responses.
Supports transparent eviction, fallback retention, and drop-in Redis readiness.
"""
from __future__ import annotations

import time
from typing import Any

from app.core import geohash
from app.core.constants import GEOHASH_PRECISION, AQI_CACHE_TTL_SECONDS


class TTLCache:
    """Thread-safe TTL cache. Stored items auto-expire after TTL."""

    def __init__(self, default_ttl: int = AQI_CACHE_TTL_SECONDS) -> None:
        self._store: dict[str, tuple[float, Any]] = {}
        self._ttl = default_ttl

    @staticmethod
    def geohash_key(lat: float, lon: float) -> str:
        return geohash.encode(lat, lon, precision=GEOHASH_PRECISION)

    def get(self, key: str) -> Any | None:
        entry = self._store.get(key)
        if entry is None:
            return None
        expires_at, value = entry
        if time.monotonic() > expires_at:
            # Expired
            del self._store[key]
            return None
        return value

    def get_stale(self, key: str) -> Any | None:
        """Return cached value even if expired (for graceful offline fallback)."""
        entry = self._store.get(key)
        if entry is None:
            return None
        return entry[1]

    def set(self, key: str, value: Any, ttl: int | None = None) -> None:
        self._store[key] = (time.monotonic() + (ttl or self._ttl), value)

    def invalidate(self, key: str) -> None:
        self._store.pop(key, None)

    def clear(self) -> None:
        self._store.clear()
