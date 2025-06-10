from ed_core.documentation.api.abc_core_api_client import OrderDto
from ed_domain.common.exceptions import EXCEPTION_NAMES, ApplicationException
from rmediator.decorators import request_handler
from rmediator.types import RequestHandler

from ed_gateway.application.common.responses.base_response import BaseResponse
from ed_gateway.application.contracts.infrastructure.api.abc_api import ABCApi
from ed_gateway.application.features.consumers.requests.queries import \
    GetConsumerOrdersQuery
from ed_gateway.common.logging_helpers import get_logger

LOG = get_logger()


@request_handler(GetConsumerOrdersQuery, BaseResponse[list[OrderDto]])
class GetConsumerOrdersQueryHandler(RequestHandler):
    def __init__(self, api: ABCApi):
        self._api = api

    async def handle(
        self, request: GetConsumerOrdersQuery
    ) -> BaseResponse[list[OrderDto]]:
        LOG.info(
            f"Calling core get_consumer_delivery_jobs API with consumer_id: {request.consumer_id}"
        )
        id = request.consumer_id
        response = await self._api.core_api.get_consumer_orders(str(id))

        LOG.info(
            f"Received response from get_consumer_delivery_jobs: {response}")
        if not response["is_success"]:
            raise ApplicationException(
                EXCEPTION_NAMES[response["http_status_code"]],
                "Failed to fetch orders.",
                response["errors"],
            )

        return BaseResponse[list[OrderDto]].success(
            "Consumer orders fetched successfully.", response["data"]
        )
