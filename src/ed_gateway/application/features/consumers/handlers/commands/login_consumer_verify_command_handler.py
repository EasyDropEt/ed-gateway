from ed_domain.common.exceptions import ApplicationException, EXCEPTION_NAMES
from rmediator.decorators import request_handler
from rmediator.types import RequestHandler

from ed_gateway.application.common.responses.base_response import BaseResponse
from ed_gateway.application.contracts.infrastructure.api.abc_api import ABCApi
from ed_gateway.application.features.consumers.dtos import ConsumerDto
from ed_gateway.application.features.consumers.requests.commands import \
    LoginConsumerVerifyCommand
from ed_gateway.common.logging_helpers import get_logger

LOG = get_logger()


@request_handler(LoginConsumerVerifyCommand, BaseResponse[ConsumerDto])
class LoginConsumerVerifyCommandHandler(RequestHandler):
    def __init__(self, api: ABCApi):
        self._api = api

    async def handle(
        self, request: LoginConsumerVerifyCommand
    ) -> BaseResponse[ConsumerDto]:
        LOG.info("Handling LoginConsumerVerifyCommand")
        verify_response = self._api.auth_api.login_verify_otp(request.dto)
        if verify_response["is_success"] is False:
            raise ApplicationException(
                EXCEPTION_NAMES[response["http_status_code"]],
                "Consumer login failed.",
                verify_response["errors"],
            )

        user = verify_response["data"]
        get_consumer_response = self._api.core_api.get_consumer_by_user_id(
            str(user["id"])
        )
        if get_consumer_response["is_success"] is False:
            raise ApplicationException(
                EXCEPTION_NAMES[response["http_status_code"]],
                "Consumer login failed.",
                get_consumer_response["errors"],
            )

        return BaseResponse[ConsumerDto].success(
            "Consumer logged in successfully",
            ConsumerDto(
                **get_consumer_response["data"],  # type: ignore
                token=user["token"],
            ),
        )
