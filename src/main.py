from typing import Callable, Coroutine

from fastapi import FastAPI, Request, Response
from orx.impl.http import HTTPClient

from src.impl.database import database
from src.impl.integration import AuthenticationError, IntegrationManager

from .routes import router

app = FastAPI()
http = HTTPClient()
integration_manager = IntegrationManager()

app.include_router(router)


@app.on_event("startup")  # type: ignore
async def startup() -> None:
    await database.connect()


@app.on_event("shutdown")  # type: ignore
async def shutdown() -> None:
    await database.disconnect()
    await http.close()


@app.middleware("http")  # type: ignore
async def orx_middleware(request: Request, call_next: Callable[..., Coroutine[None, None, Response]]) -> Response:
    request.state.http = http

    return await call_next(request)


@app.middleware("http")  # type: ignore
async def integration_middleware(
    request: Request,
    call_next: Callable[..., Coroutine[None, None, Response]],
) -> Response:
    if request.url.path.startswith(("/docs", "/openapi")):
        return await call_next(request)

    token = request.headers.get("Authorization")

    if not token:
        return Response(status_code=401)

    try:
        request.state.integration = integration_manager.authenticate(token)
        request.state.integration_manager = integration_manager
    except AuthenticationError:
        return Response(status_code=401)

    return await call_next(request)
