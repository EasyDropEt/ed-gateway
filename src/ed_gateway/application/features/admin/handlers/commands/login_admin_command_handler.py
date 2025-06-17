from ed_auth.documentation.api.auth_api_client import UnverifiedUserDto
from rmediator.decorators import request_handler
from rmediator.types import RequestHandler

from ed_gateway.application.common.responses.base_response import BaseResponse
from ed_gateway.application.contracts.infrastructure.api.abc_api import ABCApi
from ed_gateway.application.features.admin.requests.commands import \
    LoginAdminCommand
from ed_gateway.application.service.auth_api_service import AuthApiService
from ed_gateway.common.logging_helpers import get_logger

LOG = get_logger()


@request_handler(LoginAdminCommand, BaseResponse[UnverifiedUserDto])
class LoginAdminCommandHandler(RequestHandler):
    def __init__(self, api: ABCApi):
        self._api = api
        self._auth_service = AuthApiService(api.auth_api)

        self._success_message = "Log-in OTP sent successfully"

    async def handle(
        self, request: LoginAdminCommand
    ) -> BaseResponse[UnverifiedUserDto]:
        user = await self._auth_service.login({**request.dto})

        return BaseResponse[UnverifiedUserDto].success(self._success_message, user)
