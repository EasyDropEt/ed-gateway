from ed_core.documentation.api.abc_core_api_client import AdminDto
from ed_domain.common.exceptions import EXCEPTION_NAMES, ApplicationException
from rmediator.decorators import request_handler
from rmediator.types import RequestHandler

from ed_gateway.application.common.responses.base_response import BaseResponse
from ed_gateway.application.contracts.infrastructure.api.abc_api import ABCApi
from ed_gateway.application.features.admin.requests.queries import \
    GetAdminQuery
from ed_gateway.common.logging_helpers import get_logger

LOG = get_logger()


@request_handler(GetAdminQuery, BaseResponse[AdminDto])
class GetAdminQueryHandler(RequestHandler):
    def __init__(self, api: ABCApi):
        self._api = api

    async def handle(self, request: GetAdminQuery) -> BaseResponse[AdminDto]:
        LOG.info(
            f"Calling core get_admin API with admin_id: {request.admin_id}")
        response = await self._api.core_api.get_admin(str(request.admin_id))

        LOG.info(f"Received response from get_admin: {response}")
        if not response["is_success"]:
            raise ApplicationException(
                EXCEPTION_NAMES[response["http_status_code"]],
                "Failed to fetch admin.",
                response["errors"],
            )

        return BaseResponse[AdminDto].success(
            "Admin fetched successfully.", response["data"]
        )
