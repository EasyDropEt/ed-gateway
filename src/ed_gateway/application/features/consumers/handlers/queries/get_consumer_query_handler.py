from ed_core.documentation.abc_core_api_client import ConsumerDto
from ed_domain.common.exceptions import ApplicationException, Exceptions
from rmediator.decorators import request_handler
from rmediator.types import RequestHandler

from ed_gateway.application.common.responses.base_response import BaseResponse
from ed_gateway.application.contracts.infrastructure.api.abc_api import ABCApi
from ed_gateway.application.features.consumers.requests.queries import \
    GetConsumerQuery
from ed_gateway.common.logging_helpers import get_logger

LOG = get_logger()


@request_handler(GetConsumerQuery, BaseResponse[ConsumerDto])
class GetConsumerQueryHandler(RequestHandler):
    def __init__(self, api: ABCApi):
        self._api = api

    async def handle(self, request: GetConsumerQuery) -> BaseResponse[ConsumerDto]:
        LOG.info(
            f"Calling core get_consumer API with consumer_id: {request.consumer_id}"
        )
        response = self._api.core_api.get_consumer(str(request.consumer_id))

        LOG.info(f"Received response from get_consumer: {response}")
        if not response["is_success"]:
            LOG.error(
                "Failed to fetch consumer.",
                request.consumer_id,
                response["errors"],
            )
            raise ApplicationException(
                Exceptions.InternalServerException,
                "Consumer not found.",
                response["errors"],
            )

        return BaseResponse[ConsumerDto].success(
            "Consumer fetched successfully.", response["data"]
        )
