from abc import ABCMeta, abstractmethod

from ed_domain_model.services.core.dtos.driver_dto import DriverDto
from ed_domain_model.services.core.endpoints.drivers import (CreateDriverDto,
                                                             DeliveryJobDto)


class ABCCoreApiHandler(metaclass=ABCMeta):
    @abstractmethod
    def create_driver(self, create_driver_dto: CreateDriverDto) -> DriverDto:...

    @abstractmethod
    def get_driver_delivery_jobs(self, driver_id: str) -> list[DeliveryJobDto]:...

    @abstractmethod
    def upload_driver_profile(self, driver_id: str) -> DriverDto:...

    @abstractmethod
    def get_driver(self, driver_id: str) -> DriverDto: ...
