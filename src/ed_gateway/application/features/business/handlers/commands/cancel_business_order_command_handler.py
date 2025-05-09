from ed_core.documentation.abc_core_api_client import OrderDto
from ed_domain.common.exceptions import ApplicationException, Exceptions
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
        get_order_response = self._api.core_api.get_order(
            str(request.order_id))
        if get_order_response["is_success"] is False:
            raise ApplicationException(
                Exceptions.InternalServerException,
                "Failed to cancel order.",
                get_order_response["errors"],
            )

        order = get_order_response["data"]
        if order.business.id != str(request.business_id):
            raise ApplicationException(
                Exceptions.UnauthorizedException,
                "Failed to cancel order.",
                ["Order does not belong to the business."],
            )

        cancel_response = self._api.core_api.cancel_order(
            str(request.order_id))
        if cancel_response["is_success"] is False:
            raise ApplicationException(
                Exceptions.InternalServerException,
                "Failed to cancel order.",
                cancel_response["errors"],
            )

        return BaseResponse[OrderDto].success(
            "Order cancelled successfully.", cancel_response["data"]
        )
