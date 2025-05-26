from ed_core.documentation.abc_core_api_client import OrderDto
from ed_domain.common.exceptions import ApplicationException, Exceptions
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
        response = self._api.core_api.get_consumer_delivery_jobs(
            str(request.consumer_id)
        )

        LOG.info(
            f"Received response from get_consumer_delivery_jobs: {response}")
        if not response["is_success"]:
            LOG.error(
                "Failed to fetch orders for consumer %s: %s",
                request.consumer_id,
                response["errors"],
            )
            raise ApplicationException(
                Exceptions.InternalServerException,
                "Failed to fetch orders.",
                response["errors"],
            )

        return BaseResponse[list[OrderDto]].success(
            "C onsumer orders fetched successfully.", response["data"]
        )
