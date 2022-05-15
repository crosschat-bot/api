from pydantic import BaseModel

from src.impl.integration import Scope


class Integration(BaseModel):
    id: int
    scopes: list[Scope]
    system: bool = False


class GetIntegrationResponse(BaseModel):
    integration: Integration
