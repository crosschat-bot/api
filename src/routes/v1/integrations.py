from fastapi import APIRouter, HTTPException

from src.impl.request import Request
from src.models.integrations import GetIntegrationResponse, Integration

router = APIRouter(prefix="/integrations")


@router.get("/{id}", response_model=GetIntegrationResponse)
async def get_integration(request: Request, id: int) -> GetIntegrationResponse:
    """Get the integration details about the specified integration."""

    if not request.state.integration.can("VIEW_INTEGRATIONS"):
        raise HTTPException(status_code=403)

    try:
        integration = request.state.integration_manager.get(id)
    except ValueError:
        raise HTTPException(status_code=404)

    return GetIntegrationResponse(integration=Integration(**integration.dict()))
