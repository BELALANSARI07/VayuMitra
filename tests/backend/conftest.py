"""
Pytest configuration and shared fixtures for VayuMitra backend tests.
"""
import sys

# Safeguard against environments where native orjson DLL is restricted by policy
if "orjson" not in sys.modules:
    sys.modules["orjson"] = None  # type: ignore

import pytest
