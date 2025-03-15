from abc import ABCMeta, abstractmethod

from src.application.contracts.infrastructure.api.abc_auth_api_handler import \
    ABCAuthApiHandler
from src.application.contracts.infrastructure.api.abc_core_api_handler import \
    ABCCoreApiHandler


class ABCApi(metaclass=ABCMeta):
    @property
    @abstractmethod
    def core_api(self) -> ABCCoreApiHandler: ...


    @property
    @abstractmethod
    def auth_api(self) -> ABCAuthApiHandler: ...
