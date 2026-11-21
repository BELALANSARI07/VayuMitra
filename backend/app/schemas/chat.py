from __future__ import annotations
from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    message: str = Field(
        ...,
        min_length=1,
        max_length=1000,
        description="User query regarding air quality routines, hacks, or swaps.",
    )
    lat: float = Field(..., ge=-90.0, le=90.0)
    lon: float = Field(..., ge=-180.0, le=180.0)
    conversation_id: str | None = Field(None, max_length=64)


class CitationRef(BaseModel):
    source: str
    page: int
    section: str
    relevance_score: float


class ChatSSEEvent(BaseModel):
    """Shape of each SSE data: JSON payload."""
    event: str                           # "token" | "citation" | "impact" | "done" | "error"
    content: str | None = None           # Streamed text token
    citations: list[CitationRef] | None = None
    impact: dict | None = None           # Serialized ImpactDelta when present
