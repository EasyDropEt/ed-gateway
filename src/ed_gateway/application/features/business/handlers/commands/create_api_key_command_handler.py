from ed_core.documentation.api.abc_core_api_client import ApiKeyDto
from ed_domain.common.exceptions import EXCEPTION_NAMES, ApplicationException
from rmediator.decorators import request_handler
from rmediator.types import RequestHandler

from ed_gateway.application.common.responses.base_response import BaseResponse
from ed_gateway.application.contracts.infrastructure.api.abc_api import ABCApi
from ed_gateway.application.features.business.requests.commands import \
    CreateApiKeyCommand
from ed_gateway.common.logging_helpers import get_logger

LOG = get_logger()


@request_handler(CreateApiKeyCommand, BaseResponse[ApiKeyDto])
class CreateApiKeyCommandHandler(RequestHandler):
    def __init__(self, api_handler: ABCApi):
        self._api_handler = api_handler

        self._error_message = "Failed to create an api_key."
        self._success_message = "API key created successfully."

    async def handle(self, request: CreateApiKeyCommand) -> BaseResponse[ApiKeyDto]:
        LOG.info("Sending core api request to create_business_api_key")
        response = await self._api_handler.core_api.create_business_api_key(
            str(request.business_id), request.dto
        )

        LOG.info(
            f"Received response from create_business_api_keys: {response}")
        if not response["is_success"]:
            raise ApplicationException(
                EXCEPTION_NAMES[response["http_status_code"]],
                self._error_message,
                response["errors"],
            )

        return BaseResponse[ApiKeyDto].success(self._success_message, response["data"])
