from ed_domain.common.exceptions import EXCEPTION_NAMES, ApplicationException
from rmediator.decorators import request_handler
from rmediator.types import RequestHandler

from ed_gateway.application.common.responses.base_response import BaseResponse
from ed_gateway.application.contracts.infrastructure.api.abc_api import ABCApi
from ed_gateway.application.features.business.requests.commands import \
    DeleteApiKeyCommand
from ed_gateway.common.logging_helpers import get_logger

LOG = get_logger()


@request_handler(DeleteApiKeyCommand, BaseResponse[None])
class DeleteApiKeyCommandHandler(RequestHandler):
    def __init__(
        self,
        api_handler: ABCApi,
    ):
        self._api_handler = api_handler

        self._success_message = "API Key deleted succesfully."
        self._error_message = "Failed to delete API key."

    async def handle(self, request: DeleteApiKeyCommand) -> BaseResponse[None]:
        LOG.info(
            f"Calling auth delete_business_api_key API with: {request.api_key_prefix}"
        )
        response = await self._api_handler.core_api.delete_business_api_key(
            str(request.business_id), request.api_key_prefix
        )

        LOG.info(
            "Received response from delete_business_api_key - success: %s",
            response.get("is_success"),
        )
        if not response["is_success"]:
            raise ApplicationException(
                EXCEPTION_NAMES[response["http_status_code"]],
                self._error_message,
                response["errors"],
            )

        return BaseResponse[None].success(self._success_message, response["data"])
