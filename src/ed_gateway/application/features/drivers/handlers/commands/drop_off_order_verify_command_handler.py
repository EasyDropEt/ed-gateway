from ed_domain.common.exceptions import ApplicationException, Exceptions
from rmediator.decorators import request_handler
from rmediator.types import RequestHandler

from ed_gateway.application.common.responses.base_response import BaseResponse
from ed_gateway.application.contracts.infrastructure.api.abc_api import ABCApi
from ed_gateway.application.features.drivers.requests.commands import \
    DropOffOrderVerifyCommand
from ed_gateway.common.logging_helpers import get_logger

LOG = get_logger()


@request_handler(DropOffOrderVerifyCommand, BaseResponse[None])
class DropOffOrderVerifyCommandHandler(RequestHandler):
    def __init__(self, api: ABCApi):
        self._api = api

    async def handle(self, request: DropOffOrderVerifyCommand) -> BaseResponse[None]:
        response = self._api.core_api.verify_order_drop_off(
            str(request.driver_id),
            str(request.delivery_job_id),
            str(request.order_id),
            request.dto,
        )
        if response["is_success"] is False:
            LOG.error(
                "Failed to verify drop off order.",
                request.driver_id,
                request.delivery_job_id,
                response["errors"],
            )
            raise ApplicationException(
                Exceptions.InternalServerException,
                "Failed to verify drop off order.",
                response["errors"],
            )

        return BaseResponse[None].success(
            "Order drop off completed successfully.",
            None,
        )
