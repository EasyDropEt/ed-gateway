from ed_core.documentation.abc_core_api_client import ConsumerDto
from ed_domain.common.exceptions import ApplicationException, Exceptions
from rmediator.decorators import request_handler
from rmediator.types import RequestHandler

from ed_gateway.application.common.responses.base_response import BaseResponse
from ed_gateway.application.contracts.infrastructure.api.abc_api import ABCApi
from ed_gateway.application.features.consumers.requests.queries import \
    GetConsumerByUserIdQuery
from ed_gateway.common.logging_helpers import get_logger

LOG = get_logger()


@request_handler(GetConsumerByUserIdQuery, BaseResponse[ConsumerDto])
class GetConsumerByUserIdQueryHandler(RequestHandler):
    def __init__(self, api: ABCApi):
        self._api = api

    async def handle(
        self, request: GetConsumerByUserIdQuery
    ) -> BaseResponse[ConsumerDto]:
        LOG.info(
            f"Calling core get_consumer_by_user_id API with user_id: {request.user_id}"
        )
        response = self._api.core_api.get_consumer_by_user_id(
            str(request.user_id))

        LOG.info(f"Received response from get_consumer_by_user_id: {response}")
        if not response["is_success"]:
            raise ApplicationException(
                Exceptions.InternalServerException,
                "Failed to fetch consumer.",
                response["errors"],
            )

        return BaseResponse[ConsumerDto].success(
            "Consumer fetched successfully.", response["data"]
        )
