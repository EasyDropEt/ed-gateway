from ed_domain_model.services.auth.dtos import UnverifiedUserDto
from rmediator.decorators import request_handler
from rmediator.types import RequestHandler

from src.application.common.responses.base_response import BaseResponse
from src.application.contracts.infrastructure.api.abc_api import ABCApi
from src.application.features.drivers.requests.commands.login_driver_command import \
    LoginDriverCommand
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
        unverified_user_dto = self._api.auth_api.login_get_otp({**request.dto})

        return BaseResponse[UnverifiedUserDto].success(
            "Log-in OTP sent successfully", unverified_user_dto
        )
