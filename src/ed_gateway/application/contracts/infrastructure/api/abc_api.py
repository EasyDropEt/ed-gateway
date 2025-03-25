from abc import ABCMeta, abstractmethod

from ed_auth.documentation.abc_auth_api_client import ABCAuthApiClient
from ed_core.documentation.abc_core_api_client import ABCCoreApiClient


class ABCApi(metaclass=ABCMeta):
    @property
    @abstractmethod
    def core_api(self) -> ABCCoreApiClient: ...

    @property
    @abstractmethod
    def auth_api(self) -> ABCAuthApiClient: ...
