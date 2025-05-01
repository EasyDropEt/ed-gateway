from ed_core.documentation.abc_core_api_client import DriverDto
from ed_domain.common.exceptions import ApplicationException, Exceptions
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
        response = self._api.core_api.get_driver(str(request.driver_id))

        if not response["is_success"]:
            LOG.error(
                "Failed to fetch driver.",
                request.driver_id,
                response["errors"],
            )
            raise ApplicationException(
                Exceptions.InternalServerException,
                "Driver not found.",
                response["errors"],
            )

        return BaseResponse[DriverDto].success(
            "Driver fetched successfully.", response["data"]
        )
