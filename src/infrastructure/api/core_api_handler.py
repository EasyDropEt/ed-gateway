from ed_domain_model.services.core.dtos.create_driver_dto import \
    CreateDriverDto
from ed_domain_model.services.core.dtos.driver_dto import DriverDto
from ed_domain_model.services.core.endpoints.drivers import (DeliveryJobDto,
                                                             DriversEndpoint)

from src.application.contracts.infrastructure.api.abc_core_api_handler import \
    ABCCoreApiHandler
from src.infrastructure.api.api_client import ApiClient


class CoreApiHandler(ABCCoreApiHandler):
    def __init__(self, core_api: str) -> None:
        self._driver_endpoints = DriversEndpoint(core_api)

    def create_driver(self, create_driver_dto: CreateDriverDto) -> DriverDto:
        endpoint = self._driver_endpoints.get_description('create_driver')
        api_client = ApiClient(endpoint)

        return api_client.send({'request': create_driver_dto}) # type: ignore

    def get_driver_delivery_jobs(self, driver_id: str) -> list[DeliveryJobDto]:
        endpoint = self._driver_endpoints.get_description('get_driver_delivery_jobs')
        api_client = ApiClient(endpoint)

        return api_client.send({'path_params': {'driver_id': driver_id}}) # type: ignore

    def upload_driver_profile(self, driver_id: str) -> DriverDto:
        endpoint = self._driver_endpoints.get_description('upload_driver_profile')
        api_client = ApiClient(endpoint)

        return api_client.send({'path_params': {'driver_id': driver_id}}) # type: ignore

    def get_driver(self, driver_id: str) -> DriverDto:
        endpoint = self._driver_endpoints.get_description('get_driver')
        api_client = ApiClient(endpoint)

        return api_client.send({'path_params': {'driver_id': driver_id}}) # type: ignore
