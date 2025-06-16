from ed_core.documentation.api.abc_core_api_client import WebhookDto
from ed_domain.common.exceptions import EXCEPTION_NAMES, ApplicationException
from rmediator.decorators import request_handler
from rmediator.types import RequestHandler

from ed_gateway.application.common.responses.base_response import BaseResponse
from ed_gateway.application.contracts.infrastructure.api.abc_api import ABCApi
from ed_gateway.application.features.business.requests.commands import \
    CreateWebhookCommand
from ed_gateway.common.logging_helpers import get_logger

LOG = get_logger()


@request_handler(CreateWebhookCommand, BaseResponse[WebhookDto])
class CreateWebhookCommandHandler(RequestHandler):
    def __init__(self, api_handler: ABCApi):
        self._api_handler = api_handler

        self._error_message = "Failed to create an webhook."
        self._success_message = "Webhook created successfully."

    async def handle(self, request: CreateWebhookCommand) -> BaseResponse[WebhookDto]:
        LOG.info("Sending core api request to create_business_webhook")
        response = await self._api_handler.core_api.create_business_webhook(
            str(request.business_id), request.dto
        )

        LOG.info(f"Received response from create_business_webhook: {response}")
        if not response["is_success"]:
            raise ApplicationException(
                EXCEPTION_NAMES[response["http_status_code"]],
                self._error_message,
                response["errors"],
            )

        return BaseResponse[WebhookDto].success(self._success_message, response["data"])
