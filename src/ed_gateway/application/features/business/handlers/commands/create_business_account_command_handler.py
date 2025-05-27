from ed_core.documentation.api.abc_core_api_client import BusinessDto
from ed_domain.common.exceptions import ApplicationException, Exceptions
from rmediator.decorators import request_handler
from rmediator.types import RequestHandler

from ed_gateway.application.common.responses.base_response import BaseResponse
from ed_gateway.application.contracts.infrastructure.api.abc_api import ABCApi
from ed_gateway.application.features.business.requests.commands import \
    CreateBusinessAccountCommand
from ed_gateway.common.logging_helpers import get_logger

LOG = get_logger()


@request_handler(CreateBusinessAccountCommand, BaseResponse[BusinessDto])
class CreateBusinessAccountCommandHandler(RequestHandler):
    def __init__(self, api_handler: ABCApi):
        self._api_handler = api_handler

    async def handle(
        self, request: CreateBusinessAccountCommand
    ) -> BaseResponse[BusinessDto]:
        LOG.info(
            f"Calling auth create_get_otp API with request: {request.dto}")
        create_user_response = self._api_handler.auth_api.create_get_otp(
            {
                "first_name": request.dto["owner_first_name"],
                "last_name": request.dto["owner_last_name"],
                "email": request.dto["email"],
                "phone_number": request.dto["phone_number"],
                "password": request.dto["password"],
            }
        )

        LOG.info(
            f"Received response from create_get_otp: {create_user_response}")
        if not create_user_response["is_success"]:
            raise ApplicationException(
                Exceptions.InternalServerException,
                "Failed to create user account",
                create_user_response["errors"],
            )

        LOG.info(
            f"Calling core create_business API with request: {request.dto}")
        create_business_response = self._api_handler.core_api.create_business(
            {
                "user_id": create_user_response["data"]["id"],
                "business_name": request.dto["business_name"],
                "owner_first_name": request.dto["owner_first_name"],
                "owner_last_name": request.dto["owner_last_name"],
                "phone_number": request.dto["phone_number"],
                "email": request.dto["email"],
                "location": request.dto["location"],
            }
        )

        LOG.info(
            f"Received response from create_business: {create_business_response}")
        if create_business_response["is_success"] is False:
            self._api_handler.auth_api.delete_user(
                create_user_response["data"]["id"])
            raise ApplicationException(
                Exceptions.InternalServerException,
                "Failed to create business account",
                create_business_response["errors"],
            )

        return BaseResponse[BusinessDto].success(
            "Business account created successfully",
            create_business_response["data"],
        )
