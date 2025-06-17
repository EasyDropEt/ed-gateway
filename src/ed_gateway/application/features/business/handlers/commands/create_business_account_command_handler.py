from ed_core.documentation.api.abc_core_api_client import (BusinessDto,
                                                           CreateBusinessDto)
from ed_domain.common.exceptions import EXCEPTION_NAMES, ApplicationException
from ed_domain.core.entities.notification import NotificationType
from rmediator.decorators import request_handler
from rmediator.types import RequestHandler

from ed_gateway.application.common.responses.base_response import BaseResponse
from ed_gateway.application.contracts.infrastructure.api.abc_api import ABCApi
from ed_gateway.application.contracts.infrastructure.email.abc_email_templater import \
    ABCEmailTemplater
from ed_gateway.application.features.business.requests.commands import \
    CreateBusinessAccountCommand
from ed_gateway.common.logging_helpers import get_logger

LOG = get_logger()


@request_handler(CreateBusinessAccountCommand, BaseResponse[BusinessDto])
class CreateBusinessAccountCommandHandler(RequestHandler):
    def __init__(
        self,
        api_handler: ABCApi,
        email_templater: ABCEmailTemplater,
    ):
        self._api_handler = api_handler
        self._email_templater = email_templater

        self._success_message = "Business account created successfully."
        self._error_message = "Failed to create business account."

    async def handle(
        self, request: CreateBusinessAccountCommand
    ) -> BaseResponse[BusinessDto]:
        dto = request.dto

        LOG.info(f"Calling auth create_get_otp API with request: {dto}")
        create_user_response = await self._api_handler.auth_api.create_get_otp(
            {
                "first_name": dto["owner_first_name"],
                "last_name": dto["owner_last_name"],
                "email": dto["email"],
                "phone_number": dto["phone_number"],
                "password": dto["password"],
            }
        )

        LOG.info(
            f"Received response from create_get_otp: {create_user_response}")
        if not create_user_response["is_success"]:
            raise ApplicationException(
                EXCEPTION_NAMES[create_user_response["http_status_code"]],
                self._error_message,
                create_user_response["errors"],
            )

        user = create_user_response["data"]

        LOG.info(f"Calling core create_business API with request: {dto}")
        create_business_response = await self._api_handler.core_api.create_business(
            {
                "user_id": user["id"],
                "business_name": dto["business_name"],
                "owner_first_name": dto["owner_first_name"],
                "owner_last_name": dto["owner_last_name"],
                "phone_number": dto["phone_number"],
                "email": dto["email"],
                "location": dto["location"],
            }
        )

        LOG.info(
            f"Received response from create_business: {create_business_response}")
        if create_business_response["is_success"] is False:
            await self._api_handler.auth_api.delete_user(user["id"])
            raise ApplicationException(
                EXCEPTION_NAMES[create_user_response["http_status_code"]],
                self._error_message,
                create_business_response["errors"],
            )

        await self._api_handler.notification_api.send_notification(
            {
                "user_id": user["id"],
                "message": self._email_templater.welcome_business(
                    dto["owner_first_name"]
                ),
                "notification_type": NotificationType.EMAIL,
            }
        )

        business = create_business_response["data"]
        return BaseResponse[BusinessDto].success(self._success_message, business)
