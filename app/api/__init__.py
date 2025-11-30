# app/api/__init__.py
from fastapi import APIRouter

from .operator import router as operator_router
from .source import router as source_router
from .lead import router as lead_router
from .contact import router as contact_router
from .stats import router as stats_router

router = APIRouter()

router.include_router(operator_router, prefix="/operators", tags=["operators"])
router.include_router(source_router, prefix="/sources", tags=["sources"])
router.include_router(lead_router, prefix="/leads", tags=["leads"])
router.include_router(contact_router, prefix="/contacts", tags=["contacts"])
router.include_router(stats_router, prefix="/stats", tags=["stats"])
