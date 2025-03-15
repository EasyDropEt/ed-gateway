from ed_domain_model.services.core.core_endpoints import CoreEndpoint
from ed_domain_model.services.core.dtos import DeliveryJobDto
from ed_domain_model.services.core.dtos.create_driver_dto import \
    CreateDriverDto
from ed_domain_model.services.core.dtos.driver_dto import DriverDto

from src.application.common.responses.api_response import ApiResponse
from src.application.contracts.infrastructure.api.abc_core_api_handler import \
    ABCCoreApiHandler
from src.infrastructure.api.api_client import ApiClient


class CoreApiHandler(ABCCoreApiHandler):
    def __init__(self, core_api: str) -> None:
        self._driver_endpoints = CoreEndpoint(core_api)

    def create_driver(self, create_driver_dto: CreateDriverDto) -> ApiResponse[DriverDto]:
        endpoint = self._driver_endpoints.get_description('create_driver')
        api_client = ApiClient[DriverDto](endpoint)

        return api_client({'request': create_driver_dto})

    def get_driver_delivery_jobs(self, driver_id: str) -> ApiResponse[list[DeliveryJobDto]]:
        endpoint = self._driver_endpoints.get_description('get_driver_delivery_jobs')
        api_client = ApiClient[list[DeliveryJobDto]](endpoint)

        return api_client({'path_params': {'driver_id': driver_id}}) 

    def upload_driver_profile(self, driver_id: str) -> ApiResponse[DriverDto]:
        endpoint = self._driver_endpoints.get_description('upload_driver_profile')
        api_client = ApiClient[DriverDto](endpoint)

        return api_client({'path_params': {'driver_id': driver_id}}) 

    def get_driver(self, driver_id: str) -> ApiResponse[DriverDto]:
        endpoint = self._driver_endpoints.get_description('get_driver')
        api_client = ApiClient[DriverDto](endpoint)

        return api_client({'path_params': {'driver_id': driver_id}}) 
