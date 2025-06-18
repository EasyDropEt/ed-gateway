from ed_core.documentation.api.abc_core_api_client import (BusinessDto,
                                                           CreateBusinessDto)
from ed_domain.common.exceptions import (EXCEPTION_NAMES, ApplicationException,
                                         Exceptions)
from ed_domain.core.entities.notification import NotificationType
from rmediator.decorators import request_handler
from rmediator.types import RequestHandler

from ed_gateway.application.common.responses.base_response import BaseResponse
from ed_gateway.application.contracts.infrastructure.api.abc_api import ABCApi
from ed_gateway.application.contracts.infrastructure.email.abc_email_templater import \
    ABCEmailTemplater
from ed_gateway.application.features.business.requests.commands import \
    CreateBusinessAccountCommand
from ed_gateway.application.service.api_service import ApiService
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

        self._api_service = ApiService(self._error_message)

    async def handle(
        self, request: CreateBusinessAccountCommand
    ) -> BaseResponse[BusinessDto]:
        dto = request.dto

        LOG.info(f"Calling auth create_get_otp API with request: {dto}")
        create_user = await self._api_handler.auth_api.create_get_otp(
            {
                "first_name": dto["owner_first_name"],
                "last_name": dto["owner_last_name"],
                "email": dto["email"],
                "phone_number": dto["phone_number"],
                "password": dto["password"],
            }
        )

        LOG.info(f"Received response from create_get_otp: {create_user}")
        self._api_service.verify(create_user)
        user = create_user["data"]

        LOG.info(f"Calling core create_business API with request: {dto}")
        create_business = await self._api_handler.core_api.create_business(
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

        LOG.info(f"Received response from create_business: {create_business}")
        self._api_service.basic_verify(create_business)

        if not create_business["is_success"]:
            await self._api_handler.auth_api.delete_user(user["id"])
            self._api_service.verify(create_business)

        await self._api_handler.notification_api.send_notification(
            {
                "user_id": user["id"],
                "message": self._email_templater.welcome_business(
                    dto["owner_first_name"]
                ),
                "notification_type": NotificationType.EMAIL,
            }
        )

        business = create_business["data"]
        return BaseResponse[BusinessDto].success(self._success_message, business)
