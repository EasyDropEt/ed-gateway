from ed_core.documentation.api.abc_core_api_client import OrderDto
from ed_domain.common.exceptions import ApplicationException, EXCEPTION_NAMES
from rmediator.decorators import request_handler
from rmediator.types import RequestHandler

from ed_gateway.application.common.responses.base_response import BaseResponse
from ed_gateway.application.contracts.infrastructure.api.abc_api import ABCApi
from ed_gateway.application.features.drivers.requests.queries.get_driver_orders_query import \
    GetDriverOrdersQuery
from ed_gateway.common.logging_helpers import get_logger

LOG = get_logger()


@request_handler(GetDriverOrdersQuery, BaseResponse[list[OrderDto]])
class GetDriverOrdersQueryHandler(RequestHandler):
    def __init__(self, api: ABCApi):
        self._api = api

    async def handle(
        self, request: GetDriverOrdersQuery
    ) -> BaseResponse[list[OrderDto]]:
        LOG.info(
            f"Calling core get_driver_orders API with driver_id: {request.driver_id}"
        )
        response = self._api.core_api.get_driver_orders(str(request.driver_id))

        LOG.info(f"Received response from get_driver_orders: {response}")
        if not response["is_success"]:
            raise ApplicationException(
                EXCEPTION_NAMES[response["http_status_code"]],
                "Failed to fetch orders.",
                response["errors"],
            )

        return BaseResponse[list[OrderDto]].success(
            "Orders fetched successfully.", response["data"]
        )
