from ed_core.documentation.api.abc_core_api_client import OrderDto
from ed_domain.common.exceptions import EXCEPTION_NAMES, ApplicationException
from rmediator.decorators import request_handler
from rmediator.types import RequestHandler

from ed_gateway.application.common.responses.base_response import BaseResponse
from ed_gateway.application.contracts.infrastructure.api.abc_api import ABCApi
from ed_gateway.application.features.order.requests.queries import \
    GetOrderQuery
from ed_gateway.common.logging_helpers import get_logger

LOG = get_logger()


@request_handler(GetOrderQuery, BaseResponse[OrderDto])
class GetOrderQueryHandler(RequestHandler):
    def __init__(self, api: ABCApi):
        self._api = api

    async def handle(self, request: GetOrderQuery) -> BaseResponse[OrderDto]:
        LOG.info(f"Calling core get_order API with order_id: {request.id}")
        response = await self._api.core_api.get_order(str(request.id))

        LOG.info(f"Received response from get_order: {response}")
        if not response["is_success"]:
            raise ApplicationException(
                EXCEPTION_NAMES[response["http_status_code"]],
                "Failed to fetch order.",
                response["errors"],
            )

        return BaseResponse[OrderDto].success(
            "Order fetched successfully.", response["data"]
        )
