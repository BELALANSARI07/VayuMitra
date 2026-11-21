# backend/app package root
import sys

# Ensure orjson (which has a blocked native DLL on certain Windows environments)
# is safely bypassed so FastAPI falls back cleanly to standard JSON / Pydantic serialization
if "orjson" not in sys.modules:
    sys.modules["orjson"] = None  # type: ignore
