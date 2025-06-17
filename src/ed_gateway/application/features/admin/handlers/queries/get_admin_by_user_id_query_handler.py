from ed_core.documentation.api.abc_core_api_client import AdminDto
from ed_domain.common.exceptions import EXCEPTION_NAMES, ApplicationException
from rmediator.decorators import request_handler
from rmediator.types import RequestHandler

from ed_gateway.application.common.responses.base_response import BaseResponse
from ed_gateway.application.contracts.infrastructure.api.abc_api import ABCApi
from ed_gateway.application.features.admin.requests.queries import \
    GetAdminByUserIdQuery
from ed_gateway.common.logging_helpers import get_logger

LOG = get_logger()


@request_handler(GetAdminByUserIdQuery, BaseResponse[AdminDto])
class GetAdminByUserIdQueryHandler(RequestHandler):
    def __init__(self, api: ABCApi):
        self._api = api

        self._success_message = "Admin fetched successfully."
        self._error_message = "Failed to fetch admin."

    async def handle(self, request: GetAdminByUserIdQuery) -> BaseResponse[AdminDto]:
        LOG.info(
            f"Calling core get_admin_by_user_id API with user_id: {request.user_id}"
        )
        response = await self._api.core_api.get_admin_by_user_id(str(request.user_id))

        LOG.info(f"Received response from get_admin_by_user_id: {response}")
        if not response["is_success"]:
            raise ApplicationException(
                EXCEPTION_NAMES[response["http_status_code"]],
                self._error_message,
                response["errors"],
            )

        return BaseResponse[AdminDto].success(self._success_message, response["data"])
