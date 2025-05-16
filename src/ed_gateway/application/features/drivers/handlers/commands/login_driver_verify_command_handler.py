from ed_domain.common.exceptions import ApplicationException, Exceptions
from rmediator.decorators import request_handler
from rmediator.types import RequestHandler

from ed_gateway.application.common.responses.base_response import BaseResponse
from ed_gateway.application.contracts.infrastructure.api.abc_api import ABCApi
from ed_gateway.application.features.drivers.dtos import DriverAccountDto
from ed_gateway.application.features.drivers.requests.commands import \
    LoginDriverVerifyCommand
from ed_gateway.common.logging_helpers import get_logger

LOG = get_logger()


@request_handler(LoginDriverVerifyCommand, BaseResponse[DriverAccountDto])
class LoginDriverVerifyCommandHandler(RequestHandler):
    def __init__(self, api: ABCApi):
        self._api = api

    async def handle(
        self, request: LoginDriverVerifyCommand
    ) -> BaseResponse[DriverAccountDto]:
        LOG.info("Handling LoginDriverVerifyCommand")
        verify_response = self._api.auth_api.login_verify_otp(request.dto)
        if verify_response["is_success"] is False:
            raise ApplicationException(
                Exceptions.InternalServerException,
                "Driver login failed.",
                verify_response["errors"],
            )

        user = verify_response["data"]
        get_driver_response = self._api.core_api.get_driver_by_user_id(str(user["id"]))
        if get_driver_response["is_success"] is False:
            raise ApplicationException(
                Exceptions.InternalServerException,
                "Driver login failed.",
                get_driver_response["errors"],
            )

        print("GET DRIVER RESPONSE", get_driver_response)

        return BaseResponse[DriverAccountDto].success(
            "Driver logged in successfully",
            DriverAccountDto(
                **get_driver_response["data"],  # type: ignore
                token=user["token"],
            ),
        )
