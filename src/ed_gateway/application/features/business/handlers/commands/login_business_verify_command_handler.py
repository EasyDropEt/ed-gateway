from ed_domain.common.exceptions import ApplicationException, Exceptions
from rmediator.decorators import request_handler
from rmediator.types import RequestHandler

from ed_gateway.application.common.responses.base_response import BaseResponse
from ed_gateway.application.contracts.infrastructure.api.abc_api import ABCApi
from ed_gateway.application.features.business.dtos.business_account_dto import \
    BusinessAccountDto
from ed_gateway.application.features.business.requests.commands import \
    LoginBusinessVerifyCommand
from ed_gateway.common.logging_helpers import get_logger

LOG = get_logger()


@request_handler(LoginBusinessVerifyCommand, BaseResponse[BusinessAccountDto])
class LoginBusinessVerifyCommandHandler(RequestHandler):
    def __init__(self, api: ABCApi):
        self._api = api

    async def handle(
        self, request: LoginBusinessVerifyCommand
    ) -> BaseResponse[BusinessAccountDto]:
        LOG.info(
            f"Calling auth login_verify_otp API with request: {request.dto}")
        verify_response = self._api.auth_api.login_verify_otp(request.dto)

        LOG.info(f"Received response from login_verify_otp: {verify_response}")
        if verify_response["is_success"] is False:
            raise ApplicationException(
                Exceptions.InternalServerException,
                "Login failed.",
                verify_response["errors"],
            )

        user = verify_response["data"]
        LOG.info(
            f"Calling core_api.get_business_by_user_id with user ID: {user['id']}")
        get_business_response = self._api.core_api.get_business_by_user_id(
            str(user["id"])
        )

        LOG.info(
            f"Received response from get_business_by_user_id: {get_business_response}"
        )
        if get_business_response["is_success"] is False:
            raise ApplicationException(
                Exceptions.InternalServerException,
                "Login failed.",
                get_business_response["errors"],
            )

        business = get_business_response["data"]
        return BaseResponse[BusinessAccountDto].success(
            "Business logged in successfully",
            BusinessAccountDto(
                **business,  # type: ignore
                token=user["token"],
            ),
        )
