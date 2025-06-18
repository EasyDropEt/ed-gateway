from ed_core.documentation.api.abc_core_api_client import DriverDto
from ed_domain.core.entities.notification import NotificationType
from rmediator.decorators import request_handler
from rmediator.types import RequestHandler

from ed_gateway.application.common.responses.base_response import BaseResponse
from ed_gateway.application.contracts.infrastructure.api.abc_api import ABCApi
from ed_gateway.application.contracts.infrastructure.email.abc_email_templater import \
    ABCEmailTemplater
from ed_gateway.application.contracts.infrastructure.image_upload.abc_image_uploader import \
    ABCImageUploader
from ed_gateway.application.features.drivers.requests.commands.create_driver_account_command import \
    CreateDriverAccountCommand
from ed_gateway.application.service.api_service import ApiService
from ed_gateway.common.logging_helpers import get_logger

LOG = get_logger()


@request_handler(CreateDriverAccountCommand, BaseResponse[DriverDto])
class CreateDriverAccountCommandHandler(RequestHandler):
    def __init__(
        self,
        api_handler: ABCApi,
        image_uploader: ABCImageUploader,
        email_templater: ABCEmailTemplater,
    ):
        self._api_handler = api_handler
        self._image_uploader = image_uploader
        self._email_templater = email_templater

        self._success_message = "Driver account created successfully."
        self._error_message = "Failed to create user account."

        self._api_service = ApiService(self._error_message)

    async def handle(
        self, request: CreateDriverAccountCommand
    ) -> BaseResponse[DriverDto]:
        dto = request.dto
        LOG.info(f"Calling auth create_get_otp API with request: {dto}")
        create_user = await self._api_handler.auth_api.create_get_otp(
            {
                "first_name": dto["first_name"],
                "last_name": dto["last_name"],
                "email": dto["email"],
                "phone_number": dto["phone_number"],
                "password": dto["password"],
            }
        )

        LOG.info(f"Received response from create_get_otp: {create_user}")
        self._api_service.verify(create_user)

        LOG.info(f"Calling core create_driver API with request: {dto}")
        user = create_user["data"]
        create_driver = await self._api_handler.core_api.create_driver(
            {
                "user_id": user["id"],
                "first_name": dto["first_name"],
                "last_name": dto["last_name"],
                "profile_image": "placeholder",
                "phone_number": dto["phone_number"],
                "email": dto["email"],
                "location": dto["location"],
                "car": dto["car"],
            }
        )

        LOG.info(f"Received response from create_driver: {create_driver}")
        self._api_service.basic_verify(create_driver)
        if not create_driver["is_success"]:
            await self._api_handler.auth_api.delete_user(user["id"])
            self._api_service.verify(create_driver)

        await self._api_handler.notification_api.send_notification(
            {
                "user_id": user["id"],
                "message": self._email_templater.welcome_driver(dto["first_name"]),
                "notification_type": NotificationType.EMAIL,
            }
        )

        driver = create_driver["data"]
        return BaseResponse[DriverDto].success(self._success_message, driver)
