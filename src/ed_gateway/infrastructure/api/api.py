from ed_auth.documentation.api.abc_auth_api_client import ABCAuthApiClient
from ed_auth.documentation.api.auth_api_client import AuthApiClient
from ed_core.documentation.api.abc_core_api_client import ABCCoreApiClient
from ed_core.documentation.api.core_api_client import CoreApiClient

from ed_gateway.application.contracts.infrastructure.api.abc_api import ABCApi


class Api(ABCApi):
    def __init__(self, core_api: str, auth_api: str) -> None:
        self._core_api_client = CoreApiClient(core_api)
        self._auth_api_client = AuthApiClient(auth_api)

    @property
    def core_api(self) -> ABCCoreApiClient:
        return self._core_api_client

    @property
    def auth_api(self) -> ABCAuthApiClient:
        return self._auth_api_client
