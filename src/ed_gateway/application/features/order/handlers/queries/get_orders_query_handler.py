from ed_core.documentation.api.abc_core_api_client import OrderDto
from ed_domain.common.exceptions import EXCEPTION_NAMES, ApplicationException
from rmediator.decorators import request_handler
from rmediator.types import RequestHandler

from ed_gateway.application.common.responses.base_response import BaseResponse
from ed_gateway.application.contracts.infrastructure.api.abc_api import ABCApi
from ed_gateway.application.features.order.requests.queries import \
    GetOrdersQuery
from ed_gateway.common.logging_helpers import get_logger

LOG = get_logger()


@request_handler(GetOrdersQuery, BaseResponse[list[OrderDto]])
class GetOrdersQueryHandler(RequestHandler):
    def __init__(self, api: ABCApi):
        self._api = api

        self._success_message = "Orders fetched successfully."
        self._error_message = "Failed to fetch orders."

    async def handle(self, request: GetOrdersQuery) -> BaseResponse[list[OrderDto]]:
        LOG.info("Calling core get_orders API")
        response = await self._api.core_api.get_orders()

        LOG.info(f"Received response from get_order: {response}")
        if not response["is_success"]:
            raise ApplicationException(
                EXCEPTION_NAMES[response["http_status_code"]],
                self._error_message,
                response["errors"],
            )

        return BaseResponse[list[OrderDto]].success(
            self._success_message, response["data"]
        )
