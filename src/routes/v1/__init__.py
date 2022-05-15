from fastapi import APIRouter

from .integrations import router as integration_router

router = APIRouter()

router.include_router(integration_router)
