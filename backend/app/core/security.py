"""
Security utilities:
- Prompt injection defense & input sanitization
- SSRF-safe URL & network validation
- Coordinate bounds validation
- In-memory sliding-window / token rate limiter
"""
from __future__ import annotations

import ipaddress
import re
import time
from urllib.parse import urlparse

from fastapi import HTTPException, status
from app.core.constants import MAX_CHAT_MESSAGE_LENGTH, RATE_LIMIT_CHAT_PER_MIN


# --- Prompt Injection Patterns ---
_INJECTION_PATTERNS: list[re.Pattern] = [
    re.compile(r"ignore\s+(?:all\s+)?(?:previous|prior|above)\s+(?:instructions?|prompts?|rules?)", re.IGNORECASE),
    re.compile(r"you\s+are\s+now\s+(?:a|an|the)\s+", re.IGNORECASE),
    re.compile(r"system\s*:\s*", re.IGNORECASE),
    re.compile(r"<\|?(?:system|assistant|user|im_start|im_end)\|?>", re.IGNORECASE),
    re.compile(r"\[INST\]|\[/INST\]|<<SYS>>|<</SYS>>", re.IGNORECASE),
    re.compile(r"```\s*(?:system|prompt|instruction)", re.IGNORECASE),
    re.compile(r"(?:reveal|show|print|output|repeat)\s+(?:all\s+)?(?:your|the|system)?\s*(?:system\s+)?(?:prompts?|instructions?|rules?)", re.IGNORECASE),
    re.compile(r"do\s+not\s+follow\s+(?:your|the)\s+(?:system|original)", re.IGNORECASE),
]


def sanitize_user_message(message: str, max_length: int = MAX_CHAT_MESSAGE_LENGTH) -> str:
    """
    Validate and sanitize user chat input.
    Raises HTTPException 400 if an injection pattern is detected or length exceeded.
    """
    if not message or not message.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Message cannot be empty.",
        )

    if len(message) > max_length:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Message exceeds maximum allowed length of {max_length} characters.",
        )

    for pattern in _INJECTION_PATTERNS:
        if pattern.search(message):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Your message could not be processed. Please rephrase your question about air quality.",
            )

    # Strip null bytes and unsafe non-printable control characters (preserve normal newlines and tabs)
    cleaned = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f]", "", message)
    return cleaned.strip()


# --- SSRF & Coordinate Protections ---
_PRIVATE_NETWORKS = [
    ipaddress.ip_network("10.0.0.0/8"),
    ipaddress.ip_network("172.16.0.0/12"),
    ipaddress.ip_network("192.168.0.0/16"),
    ipaddress.ip_network("127.0.0.0/8"),
    ipaddress.ip_network("169.254.0.0/16"),
    ipaddress.ip_network("::1/128"),
    ipaddress.ip_network("fc00::/7"),
    ipaddress.ip_network("fe80::/10"),
]


def validate_coordinates(lat: float, lon: float) -> tuple[float, float]:
    """Validate latitude and longitude ranges."""
    if not (-90.0 <= lat <= 90.0 and -180.0 <= lon <= 180.0):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Coordinates out of valid geographical range.",
        )
    return (round(lat, 6), round(lon, 6))


def validate_external_url(url: str) -> str:
    """Ensure outgoing URL does not target loopback or private infrastructure."""
    parsed = urlparse(url)
    hostname = parsed.hostname
    if not hostname:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid target URL.")

    try:
        ip = ipaddress.ip_address(hostname)
        if any(ip in net for net in _PRIVATE_NETWORKS) or ip.is_loopback or ip.is_link_local:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Target destination is restricted.",
            )
    except ValueError:
        # Hostname (not raw IP) — allowed
        pass

    return url


# --- Lightweight In-Memory Rate Limiter ---
class InMemoryRateLimiter:
    """Sliding-window rate limiter per client IP."""

    def __init__(self, limit_per_minute: int = RATE_LIMIT_CHAT_PER_MIN) -> None:
        self.limit = limit_per_minute
        self.window_seconds = 60.0
        self._requests: dict[str, list[float]] = {}

    def is_allowed(self, client_ip: str) -> bool:
        now = time.monotonic()
        cutoff = now - self.window_seconds
        timestamps = self._requests.setdefault(client_ip, [])

        # Filter out old timestamps
        self._requests[client_ip] = [ts for ts in timestamps if ts > cutoff]

        if len(self._requests[client_ip]) >= self.limit:
            return False

        self._requests[client_ip].append(now)
        return True
