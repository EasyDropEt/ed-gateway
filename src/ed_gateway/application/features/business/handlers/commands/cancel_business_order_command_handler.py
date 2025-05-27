from ed_core.documentation.api.abc_core_api_client import OrderDto
from ed_domain.common.exceptions import ApplicationException, EXCEPTION_NAMES
from rmediator.decorators import request_handler
from rmediator.types import RequestHandler

from ed_gateway.application.common.responses.base_response import BaseResponse
from ed_gateway.application.contracts.infrastructure.api.abc_api import ABCApi
from ed_gateway.application.features.business.requests.commands import \
    CancelBusinessOrderCommand
from ed_gateway.common.logging_helpers import get_logger

LOG = get_logger()


@request_handler(CancelBusinessOrderCommand, BaseResponse[OrderDto])
class CancelBusinessOrderCommandHandler(RequestHandler):
    def __init__(self, api: ABCApi):
        self._api = api

    async def handle(
        self, request: CancelBusinessOrderCommand
    ) -> BaseResponse[OrderDto]:
        LOG.info(f"Calling cancel_order API with order_id: {request.order_id}")
        cancel_response = self._api.core_api.cancel_order(
            str(request.order_id))

        LOG.info(f"Received response from cancel_order API: {cancel_response}")
        if cancel_response["is_success"] is False:
            raise ApplicationException(
                EXCEPTION_NAMES[response["http_status_code"]],
                "Failed to cancel order.",
                cancel_response["errors"],
            )

        return BaseResponse[OrderDto].success(
            "Order cancelled successfully.", cancel_response["data"]
        )
