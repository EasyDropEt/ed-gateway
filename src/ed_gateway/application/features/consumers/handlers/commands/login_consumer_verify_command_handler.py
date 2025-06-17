from ed_domain.common.exceptions import EXCEPTION_NAMES, ApplicationException
from rmediator.decorators import request_handler
from rmediator.types import RequestHandler

from ed_gateway.application.common.responses.base_response import BaseResponse
from ed_gateway.application.contracts.infrastructure.api.abc_api import ABCApi
from ed_gateway.application.features.consumers.dtos import ConsumerDto
from ed_gateway.application.features.consumers.requests.commands import \
    LoginConsumerVerifyCommand
from ed_gateway.application.service.auth_api_service import AuthApiService
from ed_gateway.common.logging_helpers import get_logger

LOG = get_logger()


@request_handler(LoginConsumerVerifyCommand, BaseResponse[ConsumerDto])
class LoginConsumerVerifyCommandHandler(RequestHandler):
    def __init__(self, api: ABCApi):
        self._api = api

        self._auth_service = AuthApiService(api.auth_api)

    async def handle(
        self, request: LoginConsumerVerifyCommand
    ) -> BaseResponse[ConsumerDto]:
        user = await self._auth_service.login_verify({**request.dto})
        get_consumer_response = await self._api.core_api.get_consumer_by_user_id(
            str(user["id"])
        )
        if get_consumer_response["is_success"] is False:
            raise ApplicationException(
                EXCEPTION_NAMES[get_consumer_response["http_status_code"]],
                "Consumer login failed.",
                get_consumer_response["errors"],
            )

        return BaseResponse[ConsumerDto].success(
            "Consumer logged in successfully",
            ConsumerDto(
                **get_consumer_response["data"],
                token=user["token"],
            ),
        )
