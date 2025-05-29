from ed_auth.documentation.api.abc_auth_api_client import ABCAuthApiClient
from ed_auth.documentation.api.auth_api_client import AuthApiClient
from ed_core.documentation.api.abc_core_api_client import ABCCoreApiClient
from ed_core.documentation.api.core_api_client import CoreApiClient
from ed_notification.documentation.api.notification_api_client import \
    NotificationApiClient

from ed_gateway.application.contracts.infrastructure.api.abc_api import ABCApi
from ed_gateway.common.typing.config import Config


class Api(ABCApi):
    def __init__(self, config: Config) -> None:
        self._core_api_client = CoreApiClient(config["core_api"])
        self._auth_api_client = AuthApiClient(config["auth_api"])
        self._notification_api_client = NotificationApiClient(
            config["notification_api"]
        )

    @property
    def core_api(self) -> ABCCoreApiClient:
        return self._core_api_client

    @property
    def auth_api(self) -> ABCAuthApiClient:
        return self._auth_api_client

    @property
    def notification_api(self) -> NotificationApiClient:
        return self._notification_api_client
