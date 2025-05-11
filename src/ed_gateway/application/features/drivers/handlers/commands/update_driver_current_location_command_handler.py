from ed_domain.common.exceptions import ApplicationException, Exceptions
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
        LOG.info("Handling UpdateDriverCurrentLocationCommand")
        update_response = self._api.core_api.update_driver_current_location(
            driver_id=str(request.driver_id), update_location_dto=request.dto
        )
        if not update_response["is_success"]:
            raise ApplicationException(
                Exceptions.InternalServerException,
                "Driver location update failed.",
                update_response["errors"],
            )

        return BaseResponse[None].success(
            "Driver location updated successfully",
            None,
        )
