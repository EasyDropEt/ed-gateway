from ed_domain_model.services.auth.dtos import UnverifiedUserDto
from rmediator.decorators import request_handler
from rmediator.types import RequestHandler

from src.application.common.responses.base_response import BaseResponse
from src.application.contracts.infrastructure.api.abc_api import ABCApi
from src.application.features.drivers.requests.commands.login_driver_command import (
    LoginDriverCommand,
)
from src.common.exception_helpers import ApplicationException, Exceptions
from src.common.logging_helpers import get_logger

LOG = get_logger()

DRIVERS_DB = {}


@request_handler(LoginDriverCommand, BaseResponse[UnverifiedUserDto])
class LoginDriverCommandHandler(RequestHandler):
    def __init__(self, api: ABCApi):
        self._api = api

    async def handle(
        self, request: LoginDriverCommand
    ) -> BaseResponse[UnverifiedUserDto]:
        LOG.info("Handling LoginDriverCommand")
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
