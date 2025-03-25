from ed_domain_model.services.core.dtos.driver_dto import DriverDto
from rmediator.decorators import request_handler
from rmediator.types import RequestHandler

from ed_gateway.application.common.responses.base_response import BaseResponse
from ed_gateway.application.contracts.infrastructure.api.abc_api import ABCApi
from ed_gateway.application.features.drivers.requests.commands.login_driver_verify_command import (
    LoginDriverVerifyCommand,
)
from ed_gateway.common.exception_helpers import ApplicationException, Exceptions
from ed_gateway.common.logging_helpers import get_logger

LOG = get_logger()


@request_handler(LoginDriverVerifyCommand, BaseResponse[DriverDto])
class LoginDriverVerifyCommandHandler(RequestHandler):
    def __init__(self, api: ABCApi):
        self._api = api

    async def handle(
        self, request: LoginDriverVerifyCommand
    ) -> BaseResponse[DriverDto]:
        verify_response = self._api.auth_api.login_verify_otp(request.dto)
        if verify_response["is_success"] is False:
            raise ApplicationException(
                Exceptions.InternalServerException,
                "Failed to verify OTP for log-in",
                verify_response["errors"],
            )

        user = verify_response["data"]
        get_driver_response = self._api.core_api.get_driver(str(user["id"]))
        if get_driver_response["is_success"] is False:
            raise ApplicationException(
                Exceptions.InternalServerException,
                "Failed to get driver data",
                get_driver_response["errors"],
            )

        return BaseResponse[DriverDto].success(
            "Driver logged in successfully", get_driver_response["data"]
        )
