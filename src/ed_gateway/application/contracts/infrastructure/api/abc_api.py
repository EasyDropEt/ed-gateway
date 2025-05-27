from abc import ABCMeta, abstractmethod

from ed_auth.documentation.api.abc_auth_api_client import ABCAuthApiClient
from ed_core.documentation.api.abc_core_api_client import ABCCoreApiClient


class ABCApi(metaclass=ABCMeta):
    @property
    @abstractmethod
    def core_api(self) -> ABCCoreApiClient: ...

    @property
    @abstractmethod
    def auth_api(self) -> ABCAuthApiClient: ...
