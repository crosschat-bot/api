from fastapi import Request as _Request
from orx.impl.http import HTTPClient

from .integration import Integration, IntegrationManager


class RequestState:
    http: HTTPClient
    integration: Integration
    integration_manager: IntegrationManager


class Request(_Request):
    state: RequestState  # type: ignore
