from src.application.contracts.infrastructure.api.abc_api import ABCApi
from src.application.contracts.infrastructure.api.abc_auth_api_handler import \
    ABCAuthApiHandler
from src.application.contracts.infrastructure.api.abc_core_api_handler import \
    ABCCoreApiHandler
from src.infrastructure.api.auth_api_handler import AuthApiHandler
from src.infrastructure.api.core_api_handler import CoreApiHandler


class Api(ABCApi):
    def __init__(self, core_api: str, auth_api: str) -> None:
        self._core_api_handler = CoreApiHandler(core_api)
        self._auth_api_handler = AuthApiHandler(auth_api)

    @property
    def core_api(self) -> ABCCoreApiHandler:
        return self._core_api_handler

    @property
    def auth_api(self) -> ABCAuthApiHandler:
        return self._auth_api_handler
