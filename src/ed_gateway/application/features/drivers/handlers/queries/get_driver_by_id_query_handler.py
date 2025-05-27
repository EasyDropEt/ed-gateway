from ed_core.documentation.api.abc_core_api_client import DriverDto
from ed_domain.common.exceptions import ApplicationException, EXCEPTION_NAMES
from rmediator.decorators import request_handler
from rmediator.types import RequestHandler

from ed_gateway.application.common.responses.base_response import BaseResponse
from ed_gateway.application.contracts.infrastructure.api.abc_api import ABCApi
from ed_gateway.application.features.drivers.requests.queries import \
    GetDriverByIdQuery
from ed_gateway.common.logging_helpers import get_logger

LOG = get_logger()


@request_handler(GetDriverByIdQuery, BaseResponse[DriverDto])
class GetDriverByIdQueryHandler(RequestHandler):
    def __init__(self, api: ABCApi):
        self._api = api

    async def handle(self, request: GetDriverByIdQuery) -> BaseResponse[DriverDto]:
        LOG.info(
            f"Calling core get_driver API with driver_id: {request.driver_id}")
        response = self._api.core_api.get_driver(str(request.driver_id))

        LOG.info(f"Received response from get_driver: {response}")
        if not response["is_success"]:
            raise ApplicationException(
                EXCEPTION_NAMES[response["http_status_code"]],
                "Driver not found.",
                response["errors"],
            )

        return BaseResponse[DriverDto].success(
            "Driver fetched successfully.", response["data"]
        )
