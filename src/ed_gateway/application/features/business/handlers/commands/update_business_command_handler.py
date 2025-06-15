from ed_core.documentation.api.abc_core_api_client import BusinessDto
from ed_domain.common.exceptions import EXCEPTION_NAMES, ApplicationException
from rmediator.decorators import request_handler
from rmediator.types import RequestHandler

from ed_gateway.application.common.responses.base_response import BaseResponse
from ed_gateway.application.contracts.infrastructure.api.abc_api import ABCApi
from ed_gateway.application.features.business.requests.commands import \
    UpdateBusinessCommand
from ed_gateway.common.logging_helpers import get_logger

LOG = get_logger()


@request_handler(UpdateBusinessCommand, BaseResponse[BusinessDto])
class UpdateBusinessCommandHandler(RequestHandler):
    def __init__(
        self,
        api_handler: ABCApi,
    ):
        self._api_handler = api_handler

        self._success_message = "Business account updated successfully"
        self._error_message = "Failed to update business account."

    async def handle(self, request: UpdateBusinessCommand) -> BaseResponse[BusinessDto]:
        dto = request.dto

        LOG.info(f"Calling auth update_business API with request: {dto}")
        update_business_response = await self._api_handler.core_api.update_business(
            str(request.business_id), request.dto
        )

        LOG.info(
            "Received response from update_business - success: %s",
            update_business_response.get("is_success"),
        )
        if not update_business_response["is_success"]:
            raise ApplicationException(
                EXCEPTION_NAMES[update_business_response["http_status_code"]],
                self._error_message,
                update_business_response["errors"],
            )

        business = update_business_response["data"]
        return BaseResponse[BusinessDto].success(self._success_message, business)
