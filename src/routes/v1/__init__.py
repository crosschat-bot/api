from fastapi import APIRouter

from .integrations import router as integration_router

router = APIRouter(tags=["V1"])

router.include_router(integration_router)
