from ed_core.documentation.api.abc_core_api_client import OrderDto
from ed_domain.common.exceptions import EXCEPTION_NAMES, ApplicationException
from rmediator.decorators import request_handler
from rmediator.types import RequestHandler

from ed_gateway.application.common.responses.base_response import BaseResponse
from ed_gateway.application.contracts.infrastructure.api.abc_api import ABCApi
from ed_gateway.application.features.consumers.requests.commands import \
    RateDeliveryCommand
from ed_gateway.common.logging_helpers import get_logger

LOG = get_logger()


@request_handler(RateDeliveryCommand, BaseResponse[OrderDto])
class RateDeliveryCommandHandler(RequestHandler):
    def __init__(
        self,
        api_handler: ABCApi,
    ):
        self._api_handler = api_handler

        self._success_message = "Consumer account updated successfully"
        self._error_message = "Failed to update consumer account."

    async def handle(self, request: RateDeliveryCommand) -> BaseResponse[OrderDto]:
        dto = request.dto

        LOG.info(f"Calling auth rate_delivery API with request: {dto}")
        rate_delivery_response = await self._api_handler.core_api.rate_delivery(
            str(request.consumer_id), str(request.order_id), request.dto
        )

        LOG.info(
            "Received response from rate_delivery - success: %s",
            rate_delivery_response.get("is_success"),
        )
        if not rate_delivery_response["is_success"]:
            raise ApplicationException(
                EXCEPTION_NAMES[rate_delivery_response["http_status_code"]],
                self._error_message,
                rate_delivery_response["errors"],
            )

        order = rate_delivery_response["data"]
        return BaseResponse[OrderDto].success(self._success_message, order)
