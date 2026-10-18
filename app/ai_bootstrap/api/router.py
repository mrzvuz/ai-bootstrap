from fastapi import APIRouter

from ai_bootstrap.api import events, openai

router = APIRouter()

router.include_router(events.router, prefix="/events", tags=["events"])
router.include_router(openai.router, prefix="/v1", tags=["openai"])
