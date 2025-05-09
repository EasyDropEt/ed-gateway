from ed_auth.documentation.auth_api_client import UnverifiedUserDto
from ed_domain.common.exceptions import ApplicationException, Exceptions
from rmediator.decorators import request_handler
from rmediator.types import RequestHandler

from ed_gateway.application.common.responses.base_response import BaseResponse
from ed_gateway.application.contracts.infrastructure.api.abc_api import ABCApi
from ed_gateway.application.features.consumers.requests.commands import \
    LoginConsumerCommand
from ed_gateway.common.logging_helpers import get_logger

LOG = get_logger()


@request_handler(LoginConsumerCommand, BaseResponse[UnverifiedUserDto])
class LoginConsumerCommandHandler(RequestHandler):
    def __init__(self, api: ABCApi):
        self._api = api

    async def handle(
        self, request: LoginConsumerCommand
    ) -> BaseResponse[UnverifiedUserDto]:
        LOG.info("Handling LoginConsumerCommand")
        response = self._api.auth_api.login_get_otp(
            {"phone_number": request.dto["phone_number"]}
        )
        print("RESPONSE", response)
        if not response["is_success"]:
            raise ApplicationException(
                Exceptions.InternalServerException,
                "Failed to send OTP for log-in",
                response["errors"],
            )

        return BaseResponse[UnverifiedUserDto].success(
            "Log-in OTP sent successfully", response["data"]
        )
