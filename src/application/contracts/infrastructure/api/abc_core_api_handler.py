from abc import ABCMeta, abstractmethod

from ed_domain_model.services.core.dtos import (CreateDriverDto,
                                                DeliveryJobDto, DriverDto)

from src.application.common.responses.api_response import ApiResponse


class ABCCoreApiHandler(metaclass=ABCMeta):
    @abstractmethod
    def create_driver(self, create_driver_dto: CreateDriverDto) -> ApiResponse[DriverDto]:...

    @abstractmethod
    def get_driver_delivery_jobs(self, driver_id: str) -> ApiResponse[list[DeliveryJobDto]]:...

    @abstractmethod
    def upload_driver_profile(self, driver_id: str) -> ApiResponse[DriverDto]:...

    @abstractmethod
    def get_driver(self, driver_id: str) -> ApiResponse[DriverDto]: ...
