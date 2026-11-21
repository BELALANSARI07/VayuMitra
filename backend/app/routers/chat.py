from __future__ import annotations

import json
from typing import AsyncIterator
import uuid

from fastapi import APIRouter, HTTPException, Request, status
from fastapi.responses import StreamingResponse

from app.core.security import InMemoryRateLimiter, sanitize_user_message, validate_coordinates
from app.schemas.chat import ChatRequest
from app.services.chat_service import stream_llm_response

router = APIRouter()


@router.post("/chat")
async def chat_endpoint(body: ChatRequest, request: Request) -> StreamingResponse:
    """
    Prompt-injection defended, rate-limited SSE streaming chat endpoint.
    Supports Local LLM (Ollama) + Cloud LLM + Deterministic Fallback.
    Grounds all responses in live AQI context and authoritative CPCB/WHO citations.
    """
    # 1. Rate Limiting Check
    rate_limiter: InMemoryRateLimiter = request.app.state.rate_limiter
    client_ip = request.client.host if request.client else "127.0.0.1"
    if not rate_limiter.is_allowed(client_ip):
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Too many chat queries. Please wait a moment before sending another message.",
        )

    # 2. Strict Input Sanitization & Injection Defense (raises 400 if malicious)
    clean_message = sanitize_user_message(body.message)
    lat, lon = validate_coordinates(body.lat, body.lon)

    # 3. Retrieve Knowledge Chunks
    knowledge_index = request.app.state.knowledge_index
    chunks = knowledge_index.retrieve(query=clean_message, top_k=4)

    # 4. Fetch Cached AQI Context
    aqi_cache = request.app.state.aqi_cache
    cache_key = aqi_cache.geohash_key(lat, lon)
    aqi_context = aqi_cache.get(cache_key)

    conversation_id = body.conversation_id or str(uuid.uuid4())

    async def event_generator() -> AsyncIterator[str]:
        async for event in stream_llm_response(
            user_message=clean_message,
            rag_chunks=chunks,
            aqi_context=aqi_context,
            conversation_id=conversation_id,
            http_client=request.app.state.http_client,
        ):
            sse_data = json.dumps(event, ensure_ascii=False)
            yield f"data: {sse_data}\n\n"

        # Signal completion with consistent formatting
        done_data = json.dumps({"event": "done"})
        yield f"data: {done_data}\n\n"

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Conversation-Id": conversation_id,
        },
    )
