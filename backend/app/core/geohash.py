"""
Pure Python Geohash implementation with zero external dependencies.
Used for caching AQI and weather responses into spatial grid cells.
"""
from __future__ import annotations

_BASE32 = "0123456789bcdefghjkmnpqrstuvwxyz"
_BASE32_MAP = {c: i for i, c in enumerate(_BASE32)}


def encode(latitude: float, longitude: float, precision: int = 5) -> str:
    """
    Encode latitude and longitude into a geohash string.
    Precision 5 yields ~4.9 km x 4.9 km cells at the equator.
    """
    lat_interval = [-90.0, 90.0]
    lon_interval = [-180.0, 180.0]
    geohash: list[str] = []
    bits = [16, 8, 4, 2, 1]
    bit = 0
    ch = 0
    even = True

    while len(geohash) < precision:
        if even:
            mid = (lon_interval[0] + lon_interval[1]) / 2.0
            if longitude > mid:
                ch |= bits[bit]
                lon_interval[0] = mid
            else:
                lon_interval[1] = mid
        else:
            mid = (lat_interval[0] + lat_interval[1]) / 2.0
            if latitude > mid:
                ch |= bits[bit]
                lat_interval[0] = mid
            else:
                lat_interval[1] = mid

        even = not even
        if bit < 4:
            bit += 1
        else:
            geohash.append(_BASE32[ch])
            bit = 0
            ch = 0

    return "".join(geohash)
