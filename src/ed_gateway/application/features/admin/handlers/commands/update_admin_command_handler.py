from ed_core.documentation.api.abc_core_api_client import AdminDto
from ed_domain.common.exceptions import EXCEPTION_NAMES, ApplicationException
from rmediator.decorators import request_handler
from rmediator.types import RequestHandler

from ed_gateway.application.common.responses.base_response import BaseResponse
from ed_gateway.application.contracts.infrastructure.api.abc_api import ABCApi
from ed_gateway.application.features.admin.requests.commands import \
    UpdateAdminCommand
from ed_gateway.common.logging_helpers import get_logger

LOG = get_logger()


@request_handler(UpdateAdminCommand, BaseResponse[AdminDto])
class UpdateAdminCommandHandler(RequestHandler):
    def __init__(
        self,
        api_handler: ABCApi,
    ):
        self._api_handler = api_handler

        self._success_message = "Admin account updated successfully"
        self._error_message = "Failed to update admin account."

    async def handle(self, request: UpdateAdminCommand) -> BaseResponse[AdminDto]:
        dto = request.dto

        LOG.info(f"Calling auth update_admin API with request: {dto}")
        update_admin_response = await self._api_handler.core_api.update_admin(
            str(request.admin_id), request.dto
        )

        LOG.info(
            "Received response from update_admin - success: %s",
            update_admin_response.get("is_success"),
        )
        if not update_admin_response["is_success"]:
            raise ApplicationException(
                EXCEPTION_NAMES[update_admin_response["http_status_code"]],
                self._error_message,
                update_admin_response["errors"],
            )

        admin = update_admin_response["data"]
        return BaseResponse[AdminDto].success(self._success_message, admin)
