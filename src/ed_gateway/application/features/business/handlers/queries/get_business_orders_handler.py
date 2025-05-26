from ed_core.documentation.abc_core_api_client import OrderDto
from ed_domain.common.exceptions import ApplicationException, Exceptions
from rmediator.decorators import request_handler
from rmediator.types import RequestHandler

from ed_gateway.application.common.responses.base_response import BaseResponse
from ed_gateway.application.contracts.infrastructure.api.abc_api import ABCApi
from ed_gateway.application.features.business.requests.queries import \
    GetBusinessOrdersQuery
from ed_gateway.common.logging_helpers import get_logger

LOG = get_logger()


@request_handler(GetBusinessOrdersQuery, BaseResponse[list[OrderDto]])
class GetBusinessOrdersQueryHandler(RequestHandler):
    def __init__(self, api: ABCApi):
        self._api = api

    async def handle(
        self, request: GetBusinessOrdersQuery
    ) -> BaseResponse[list[OrderDto]]:
        LOG.info(
            f"Calling core get_business_orders API with business_id: {request.business_id}"
        )
        response = self._api.core_api.get_business_orders(
            str(request.business_id),
        )

        LOG.info(f"Received response from get_business_orders: {response}")
        if response["is_success"] is False:
            raise ApplicationException(
                Exceptions.InternalServerException,
                "Failed to fetch orders.",
                response["errors"],
            )

        return BaseResponse[list[OrderDto]].success(
            "Orders fetched successfully.", response["data"]
        )
