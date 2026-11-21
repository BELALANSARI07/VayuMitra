"""
Custom exceptions and safe exception handlers for VayuMitra.
Never leaks stack traces, paths, or internal tokens to the client.
"""
from __future__ import annotations

import logging
from starlette.requests import Request
from starlette.responses import JSONResponse

logger = logging.getLogger("vayumitra")


class VayuMitraError(Exception):
    """Base exception for application domain errors."""
    def __init__(self, message: str, status_code: int = 500):
        super().__init__(message)
        self.message = message
        self.status_code = status_code


class AQIFetchError(VayuMitraError):
    """External AQI API unreachable or returned invalid response."""
    def __init__(self, message: str = "Air quality data is temporarily unavailable."):
        super().__init__(message, status_code=503)


class LocationNotFoundError(VayuMitraError):
    def __init__(self, message: str = "Could not resolve the specified location or coordinates."):
        super().__init__(message, status_code=404)


async def global_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Catch-all: log detailed traceback internally, return safe masked message externally."""
    logger.exception("Unhandled error handling %s %s: %s", request.method, request.url.path, str(exc))
    return JSONResponse(
        status_code=500,
        content={"detail": "An internal server error occurred. Please try again later."},
    )
