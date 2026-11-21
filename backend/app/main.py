"""
VayuMitra FastAPI Application:
- Clean modular architecture (routers/, services/, schemas/, core/)
- Lifespan context manager for zero-overhead singleton initialization
- In-memory spatial TTL cache & sliding-window rate limiter
- Local LLM (Ollama) probe and telemetry
- Strict CORS, input sanitization, and masked error handling
- Single-port fullstack mounting: serves frontend/dist automatically for Azure App Service
"""
from __future__ import annotations

import sys
# Safeguard orjson DLL block on Windows environments
if "orjson" not in sys.modules:
    sys.modules["orjson"] = None  # type: ignore

from contextlib import asynccontextmanager
from pathlib import Path
from typing import Any, AsyncIterator
import httpx
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

from app.core.cache import TTLCache
from app.core.config import settings
from app.core.exceptions import global_exception_handler
from app.core.security import InMemoryRateLimiter
from app.routers import air_quality, chat, routine_plan
from app.services.rag_retriever import KnowledgeIndex

BASE_DIR = Path(__file__).resolve().parent.parent.parent


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """Startup & Shutdown lifecycle manager."""
    http_client = httpx.AsyncClient(
        timeout=httpx.Timeout(8.0, connect=4.0),
        limits=httpx.Limits(max_connections=25, max_keepalive_connections=15),
        headers={"User-Agent": "VayuMitra-UrbanAirAssistant/1.0"},
    )
    app.state.http_client = http_client

    yield

    await http_client.aclose()


app = FastAPI(
    title="VayuMitra API",
    version="1.0.0",
    description="GenAI Urban Air Quality Assistant for PromptWars Challenge 6",
    lifespan=lifespan,
)

# Pre-populate state defaults
app.state.knowledge_index = KnowledgeIndex(chunks_path=settings.CHUNKS_PATH)
app.state.http_client = httpx.AsyncClient(
    timeout=httpx.Timeout(8.0, connect=4.0),
    headers={"User-Agent": "VayuMitra-UrbanAirAssistant/1.0"},
)
app.state.aqi_cache = TTLCache(default_ttl=settings.AQI_CACHE_TTL_SECONDS)
app.state.rate_limiter = InMemoryRateLimiter(limit_per_minute=settings.RATE_LIMIT_CHAT_PER_MIN)


# --- Security Headers Middleware ---
class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:
        response = await call_next(request)
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        return response

app.add_middleware(SecurityHeadersMiddleware)

# --- CORS ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization"],
)

# --- Exception Handlers ---
app.add_exception_handler(Exception, global_exception_handler)

# --- Include Routers ---
app.include_router(air_quality.router, prefix="/api", tags=["Air Quality"])
app.include_router(routine_plan.router, prefix="/api", tags=["Routine Plan"])
app.include_router(chat.router, prefix="/api", tags=["Chat"])


@app.get("/api/health", tags=["Health"])
async def health_check(request: Request) -> dict[str, Any]:
    """Health check endpoint: reports local LLM (Ollama) status, cache, and knowledge store."""
    ollama_reachable = False
    active_local_models: list[str] = []
    try:
        r = await request.app.state.http_client.get(f"{settings.OLLAMA_BASE_URL}/api/tags", timeout=1.0)
        if r.status_code == 200:
            ollama_reachable = True
            active_local_models = [m.get("name", "") for m in r.json().get("models", [])]
    except Exception:
        pass

    return {
        "status": "healthy",
        "service": "vayumitra",
        "version": "1.0.0",
        "llm_mode": "local_ollama" if ollama_reachable else "deterministic_fallback",
        "ollama_reachable": ollama_reachable,
        "ollama_models": active_local_models,
        "rag_chunks_indexed": len(request.app.state.knowledge_index.chunks),
    }


# ---------------------------------------------------------------------------
# Mount Static Frontend Build (Single-Port Full-Stack for Azure App Service)
# ---------------------------------------------------------------------------
frontend_dist = BASE_DIR / "frontend" / "dist"
if frontend_dist.is_dir():
    from fastapi.staticfiles import StaticFiles

    assets_dir = frontend_dist / "assets"
    if assets_dir.is_dir():
        app.mount("/assets", StaticFiles(directory=str(assets_dir)), name="assets")

    @app.get("/{full_path:path}", include_in_schema=False)
    def serve_frontend(full_path: str):
        if full_path.startswith("api"):
            raise HTTPException(status_code=404, detail="API route not found")
        file_path = frontend_dist / full_path
        if file_path.is_file():
            return FileResponse(str(file_path))
        return FileResponse(str(frontend_dist / "index.html"))
