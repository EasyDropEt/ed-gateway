from ed_domain.common.exceptions import EXCEPTION_NAMES, ApplicationException
from rmediator.decorators import request_handler
from rmediator.types import RequestHandler

from ed_gateway.application.common.responses.base_response import BaseResponse
from ed_gateway.application.contracts.infrastructure.api.abc_api import ABCApi
from ed_gateway.application.features.drivers.requests.commands import \
    FinishOrderPickUpCommand
from ed_gateway.common.logging_helpers import get_logger

LOG = get_logger()


@request_handler(FinishOrderPickUpCommand, BaseResponse[None])
class FinishOrderPickUpCommandHandler(RequestHandler):
    def __init__(self, api: ABCApi):
        self._api = api

        self._error_message = "Failed to verify pick up order."

    async def handle(self, request: FinishOrderPickUpCommand) -> BaseResponse[None]:
        LOG.info(
            f"Calling core verify_order_pick_up API with driver_id: {request.driver_id}, "
            f"delivery_job_id: {request.delivery_job_id}, order_id: {request.order_id}"
        )
        response = await self._api.core_api.finish_order_pick_up(
            str(request.driver_id),
            str(request.delivery_job_id),
            str(request.order_id),
            request.dto,
        )

        LOG.info(f"Received response from verify_order_pick_up: {response}")
        if response["is_success"] is False:
            raise ApplicationException(
                EXCEPTION_NAMES[response["http_status_code"]],
                self._error_message,
                response["errors"],
            )

        return BaseResponse[None].success(
            "Order pick up completed successfully.",
            None,
        )
