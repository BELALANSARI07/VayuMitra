from __future__ import annotations

from fastapi import APIRouter, Request

from app.schemas.routine_plan import PersonaInput, RoutinePlanResponse
from app.services.routine_plan_service import generate_routine_plan

router = APIRouter()


@router.post("/routine-plan", response_model=RoutinePlanResponse)
async def create_routine_plan(
    body: PersonaInput,
    request: Request,
) -> RoutinePlanResponse:
    """
    Generate personalized low-emission daily routines, indoor hacks,
    and sustainable swaps with deterministic direct impact deltas.
    """
    return await generate_routine_plan(
        persona=body,
        http_client=request.app.state.http_client,
        cache=request.app.state.aqi_cache,
        knowledge_index=request.app.state.knowledge_index,
    )
