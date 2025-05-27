from ed_core.documentation.api.abc_core_api_client import DriverHeldFundsDto
from ed_domain.common.exceptions import ApplicationException, EXCEPTION_NAMES
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
        LOG.info(
            f"Calling core get_driver_held_funds API with driver_id: {request.driver_id}"
        )
        response = self._api.core_api.get_driver_held_funds(
            str(request.driver_id))

        LOG.info(f"Received response from get_driver_held_funds: {response}")
        if not response["is_success"]:
            raise ApplicationException(
                EXCEPTION_NAMES[response["http_status_code"]],
                "Failed to fetch driver held fundss.",
                response["errors"],
            )

        return BaseResponse[DriverHeldFundsDto].success(
            "Driver held funds fetched successfully.", response["data"]
        )
