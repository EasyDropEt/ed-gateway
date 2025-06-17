from ed_domain.common.exceptions import EXCEPTION_NAMES, ApplicationException
from rmediator.decorators import request_handler
from rmediator.types import RequestHandler

from ed_gateway.application.common.responses.base_response import BaseResponse
from ed_gateway.application.contracts.infrastructure.api.abc_api import ABCApi
from ed_gateway.application.features.admin.dtos import AdminDto
from ed_gateway.application.features.admin.requests.commands import \
    LoginAdminVerifyCommand
from ed_gateway.application.service.auth_api_service import AuthApiService
from ed_gateway.common.logging_helpers import get_logger

LOG = get_logger()


@request_handler(LoginAdminVerifyCommand, BaseResponse[AdminDto])
class LoginAdminVerifyCommandHandler(RequestHandler):
    def __init__(self, api: ABCApi):
        self._api = api

        self._auth_service = AuthApiService(api.auth_api)

    async def handle(self, request: LoginAdminVerifyCommand) -> BaseResponse[AdminDto]:
        user = await self._auth_service.login_verify({**request.dto})
        get_admin_response = await self._api.core_api.get_admin_by_user_id(
            str(user["id"])
        )
        if get_admin_response["is_success"] is False:
            raise ApplicationException(
                EXCEPTION_NAMES[get_admin_response["http_status_code"]],
                "Admin login failed.",
                get_admin_response["errors"],
            )

        return BaseResponse[AdminDto].success(
            "Admin logged in successfully",
            AdminDto(
                **get_admin_response["data"],
                token=user["token"],
            ),
        )
