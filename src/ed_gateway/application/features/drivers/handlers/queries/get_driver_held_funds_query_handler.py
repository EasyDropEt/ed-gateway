from ed_core.documentation.abc_core_api_client import DriverHeldFundsDto
from ed_domain.common.exceptions import ApplicationException, Exceptions
from rmediator.decorators import request_handler
from rmediator.types import RequestHandler

from ed_gateway.application.common.responses.base_response import BaseResponse
from ed_gateway.application.contracts.infrastructure.api.abc_api import ABCApi
from ed_gateway.application.features.drivers.requests.queries import \
    GetDriverHeldFundsQuery
from ed_gateway.common.logging_helpers import get_logger

LOG = get_logger()


@request_handler(GetDriverHeldFundsQuery, BaseResponse[DriverHeldFundsDto])
class GetDriverHeldFundsQueryHandler(RequestHandler):
    def __init__(self, api: ABCApi):
        self._api = api

    async def handle(
        self, request: GetDriverHeldFundsQuery
    ) -> BaseResponse[DriverHeldFundsDto]:
        response = self._api.core_api.get_driver_held_funds(
            str(request.driver_id))

        if not response["is_success"]:
            LOG.error(
                "Failed to fetch driver held fundss for driver %s: %s",
                request.driver_id,
                response["errors"],
            )
            raise ApplicationException(
                Exceptions.InternalServerException,
                "Failed to fetch driver held fundss.",
                response["errors"],
            )

        return BaseResponse[DriverHeldFundsDto].success(
            "Driver held funds fetched successfully.", response["data"]
        )
