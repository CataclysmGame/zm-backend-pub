from fastapi import APIRouter

from .health import router as health_router
from .v1 import router as api_v1_router

main_router = APIRouter()

main_router.include_router(api_v1_router)
main_router.include_router(health_router)
