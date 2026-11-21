from __future__ import annotations
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    # --- LLM Provider Selection ---
    LLM_PROVIDER: str = "local"               # "local" (Ollama) | "gemini" | "openai" | "deterministic"
    LLM_API_KEY: str = ""

    # --- Local LLM (Ollama) ---
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    OLLAMA_MODEL: str = "llama3"              # Any installed model: llama3, qwen, mistral, phi3, etc.
    OLLAMA_TIMEOUT_SECONDS: float = 30.0

    # --- Cloud LLM (Optional fallback/alternative) ---
    LLM_MODEL_NAME: str = "gemini-2.0-flash"
    LLM_TEMPERATURE: float = 0.3
    LLM_MAX_OUTPUT_TOKENS: int = 1024

    # --- External AQI APIs ---
    WAQI_API_TOKEN: str = ""                   # Optional fallback
    OPEN_METEO_AQ_BASE_URL: str = "https://air-quality-api.open-meteo.com/v1/air-quality"
    OPEN_METEO_WX_BASE_URL: str = "https://api.open-meteo.com/v1/forecast"

    # --- Vector / Knowledge Index ---
    DATA_DIR: Path = Path("data")
    CHUNKS_PATH: Path = Path("data/processed/chunks.jsonl")
    INDEX_DIR: Path = Path("data/faiss_index")
    EMBEDDING_MODEL_NAME: str = "all-MiniLM-L6-v2"

    # --- Cache ---
    AQI_CACHE_TTL_SECONDS: int = 900

    # --- Security & Rate Limiting ---
    CORS_ALLOWED_ORIGINS: list[str] = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:8000",
        "http://127.0.0.1:8000",
        "https://vayumitra.vercel.app",
    ]
    RATE_LIMIT_CHAT_PER_MIN: int = 20
    RATE_LIMIT_DEFAULT_PER_MIN: int = 60

    # --- App Runtime ---
    DEBUG: bool = False


settings = Settings()
