from os import environ
from pathlib import Path

from pydantic import BaseModel
from yaml import safe_load


class Scope(BaseModel):
    guilds: list[str | int]
    allow: list[str]


class Integration(BaseModel):
    id: int
    token: str
    scopes: list[Scope]
    system: bool = False

    def can(self, permission: str) -> bool:
        if self.system:
            return True

        for scope in self.scopes:
            if permission in scope.allow or "*" in scope.allow:
                return True

        return False

    def can_in(self, permission: str, guild: int) -> bool:
        valid_scopes = [scope for scope in self.scopes if permission in scope.allow or "*" in scope.allow]

        for scope in valid_scopes:
            if guild in scope.guilds or "*" in scope.guilds:
                return True

        return False


class AuthenticationError(Exception):
    pass


class IntegrationManager:
    def __init__(self) -> None:
        self._integrations: dict[str, Integration] = {}

        raw_data = Path("config.yml").read_text()
        data = safe_load(raw_data)

        for integration in data["integrations"]:
            self._integrations[integration["token"]] = Integration(**integration)

        self._integrations[environ["TOKEN"]] = Integration(
            id=0,
            token=environ["TOKEN"],
            scopes=[
                Scope(guilds=["*"], allow=["*"]),
            ],
            system=True,
        )

    def authenticate(self, token: str) -> Integration:
        if integration := self._integrations[token]:
            return integration

        raise ValueError(f"Invalid token: {token}")

    def get(self, id: int) -> Integration:
        for integration in self._integrations.values():
            if integration.id == id:
                return integration

        raise ValueError(f"Invalid id: {id}")
