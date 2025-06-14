from ed_core.documentation.api.abc_core_api_client import ConsumerDto
from ed_domain.common.exceptions import EXCEPTION_NAMES, ApplicationException
from rmediator.decorators import request_handler
from rmediator.types import RequestHandler

from ed_gateway.application.common.responses.base_response import BaseResponse
from ed_gateway.application.contracts.infrastructure.api.abc_api import ABCApi
from ed_gateway.application.features.consumers.requests.commands import \
    UpdateConsumerCommand
from ed_gateway.common.logging_helpers import get_logger

LOG = get_logger()


@request_handler(UpdateConsumerCommand, BaseResponse[ConsumerDto])
class UpdateConsumerCommandHandler(RequestHandler):
    def __init__(
        self,
        api_handler: ABCApi,
    ):
        self._api_handler = api_handler

        self._success_message = "Consumer account updated successfully"
        self._error_message = "Failed to update consumer account."

    async def handle(self, request: UpdateConsumerCommand) -> BaseResponse[ConsumerDto]:
        dto = request.dto

        LOG.info(f"Calling auth update_consumer API with request: {dto}")
        update_consumer_response = await self._api_handler.core_api.update_consumer(
            str(request.consumer_id), request.dto
        )

        LOG.info(
            "Received response from update_consumer - success: %s",
            update_consumer_response.get("is_success"),
        )
        if not update_consumer_response["is_success"]:
            raise ApplicationException(
                EXCEPTION_NAMES[update_consumer_response["http_status_code"]],
                self._error_message,
                update_consumer_response["errors"],
            )

        consumer = update_consumer_response["data"]
        return BaseResponse[ConsumerDto].success(self._success_message, consumer)
