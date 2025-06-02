from ed_domain.common.exceptions import ApplicationException, EXCEPTION_NAMES
from rmediator.decorators import request_handler
from rmediator.types import RequestHandler

from ed_gateway.application.common.responses.base_response import BaseResponse
from ed_gateway.application.contracts.infrastructure.api.abc_api import ABCApi
from ed_gateway.application.features.drivers.requests.commands import \
    UpdateDriverCurrentLocationCommand
from ed_gateway.common.logging_helpers import get_logger

LOG = get_logger()


@request_handler(UpdateDriverCurrentLocationCommand, BaseResponse[None])
class UpdateDriverCurrentLocationCommandHandler(RequestHandler):
    def __init__(self, api: ABCApi):
        self._api = api

    async def handle(
        self, request: UpdateDriverCurrentLocationCommand
    ) -> BaseResponse[None]:
        LOG.info(
            f"Calling core update_driver_current_location API with request: {request.dto}"
        )
        update_response = await self._api.core_api.update_driver_current_location(
            driver_id=str(request.driver_id), update_location_dto=request.dto
        )

        LOG.info(
            f"Received response from update_driver_current_location: {update_response}"
        )
        if not update_response["is_success"]:
            raise ApplicationException(
                EXCEPTION_NAMES[response["http_status_code"]],
                "Driver location update failed.",
                update_response["errors"],
            )

        return BaseResponse[None].success(
            "Driver location updated successfully",
            None,
        )
