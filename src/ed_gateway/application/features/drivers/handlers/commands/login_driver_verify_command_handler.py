from ed_domain.common.exceptions import EXCEPTION_NAMES, ApplicationException
from rmediator.decorators import request_handler
from rmediator.types import RequestHandler

from ed_gateway.application.common.responses.base_response import BaseResponse
from ed_gateway.application.contracts.infrastructure.api.abc_api import ABCApi
from ed_gateway.application.features.drivers.dtos import DriverAccountDto
from ed_gateway.application.features.drivers.requests.commands import \
    LoginDriverVerifyCommand
from ed_gateway.application.service.auth_api_service import AuthApiService
from ed_gateway.common.logging_helpers import get_logger

LOG = get_logger()


@request_handler(LoginDriverVerifyCommand, BaseResponse[DriverAccountDto])
class LoginDriverVerifyCommandHandler(RequestHandler):
    def __init__(self, api: ABCApi):
        self._api = api
        self._auth_service = AuthApiService(api.auth_api)

    async def handle(
        self, request: LoginDriverVerifyCommand
    ) -> BaseResponse[DriverAccountDto]:
        user = await self._auth_service.login_verify({**request.dto})

        LOG.info(
            f"Calling core_api.get_driver_by_user_id with user ID: {user['id']}")
        get_driver_response = await self._api.core_api.get_driver_by_user_id(
            str(user["id"])
        )

        LOG.info(
            f"Received response from get_driver_by_user_id: {get_driver_response}")
        if get_driver_response["is_success"] is False:
            raise ApplicationException(
                EXCEPTION_NAMES[get_driver_response["http_status_code"]],
                "Driver login failed.",
                get_driver_response["errors"],
            )

        return BaseResponse[DriverAccountDto].success(
            "Driver logged in successfully",
            DriverAccountDto(
                **get_driver_response["data"],  # type: ignore
                token=user["token"],
            ),
        )
