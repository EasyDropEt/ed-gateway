from ed_auth.documentation.auth_api_client import UnverifiedUserDto
from rmediator.decorators import request_handler
from rmediator.types import RequestHandler

from ed_gateway.application.common.responses.base_response import BaseResponse
from ed_gateway.application.contracts.infrastructure.api.abc_api import ABCApi
from ed_gateway.application.features.business.requests.commands import \
    LoginBusinessCommand
from ed_gateway.common.exception_helpers import (ApplicationException,
                                                 Exceptions)
from ed_gateway.common.logging_helpers import get_logger

LOG = get_logger()

businessS_DB = {}


@request_handler(LoginBusinessCommand, BaseResponse[UnverifiedUserDto])
class LoginBusinessCommandHandler(RequestHandler):
    def __init__(self, api: ABCApi):
        self._api = api

    async def handle(
        self, request: LoginBusinessCommand
    ) -> BaseResponse[UnverifiedUserDto]:
        LOG.info("Handling LoginBusinessCommand")
        response = self._api.auth_api.login_get_otp({**request.dto})
        if not response["is_success"]:
            raise ApplicationException(
                Exceptions.InternalServerException,
                "Failed to send OTP for log-in",
                response["errors"],
            )

        return BaseResponse[UnverifiedUserDto].success(
            "Log-in OTP sent successfully", response["data"]
        )
