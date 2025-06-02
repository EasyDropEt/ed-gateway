from ed_core.documentation.api.core_api_client import PickUpOrderDto
from ed_domain.common.exceptions import ApplicationException, EXCEPTION_NAMES
from rmediator.decorators import request_handler
from rmediator.types import RequestHandler

from ed_gateway.application.common.responses.base_response import BaseResponse
from ed_gateway.application.contracts.infrastructure.api.abc_api import ABCApi
from ed_gateway.application.features.drivers.requests.commands import \
    PickUpOrderCommand
from ed_gateway.common.logging_helpers import get_logger

LOG = get_logger()


@request_handler(PickUpOrderCommand, BaseResponse[PickUpOrderDto])
class PickUpOrderCommandHandler(RequestHandler):
    def __init__(self, api: ABCApi):
        self._api = api

    async def handle(self, request: PickUpOrderCommand) -> BaseResponse[PickUpOrderDto]:
        LOG.info(
            f"Calling core initiate_order_pick_up API with driver_id: {request.driver_id}, "
            f"delivery_job_id: {request.delivery_job_id}, order_id: {request.order_id}"
        )
        response = await self._api.core_api.initiate_order_pick_up(
            str(request.driver_id), str(
                request.delivery_job_id), str(request.order_id)
        )

        LOG.info(f"Received response from initiate_order_pick_up: {response}")
        if response["is_success"] is False:
            raise ApplicationException(
                EXCEPTION_NAMES[response["http_status_code"]],
                "Failed to pick up order.",
                response["errors"],
            )

        return BaseResponse[PickUpOrderDto].success(
            "Order pick up initiated successfully. Verification OTP sent to consumer.",
            response["data"],
        )
