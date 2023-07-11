from fastapi import APIRouter

from app.settings import settings

from .score import router as score_router
from .ticket import router as ticket_router
from .admin import router as admin_router

router = APIRouter(prefix=settings.API_V1_PREFIX)

router.include_router(score_router)
router.include_router(ticket_router)
router.include_router(admin_router)
