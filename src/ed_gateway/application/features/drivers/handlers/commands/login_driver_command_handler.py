from ed_auth.documentation.api.auth_api_client import UnverifiedUserDto
from ed_domain.common.exceptions import EXCEPTION_NAMES, ApplicationException
from rmediator.decorators import request_handler
from rmediator.types import RequestHandler

from ed_gateway.application.common.responses.base_response import BaseResponse
from ed_gateway.application.contracts.infrastructure.api.abc_api import ABCApi
from ed_gateway.application.features.drivers.requests.commands.login_driver_command import \
    LoginDriverCommand
from ed_gateway.common.logging_helpers import get_logger

LOG = get_logger()

DRIVERS_DB = {}


@request_handler(LoginDriverCommand, BaseResponse[UnverifiedUserDto])
class LoginDriverCommandHandler(RequestHandler):
    def __init__(self, api: ABCApi):
        self._api = api

    async def handle(
        self, request: LoginDriverCommand
    ) -> BaseResponse[UnverifiedUserDto]:
        LOG.info(f"Calling auth login_get_otp API with request: {request.dto}")
        response = await self._api.auth_api.login_get_otp({**request.dto})

        LOG.info(f"Received response from login_get_otp: {response}")
        if not response["is_success"]:
            raise ApplicationException(
                EXCEPTION_NAMES[response["http_status_code"]],
                "Failed to send OTP for log-in",
                response["errors"],
            )

        return BaseResponse[UnverifiedUserDto].success(
            "Log-in OTP sent successfully", response["data"]
        )
