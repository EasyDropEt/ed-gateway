from ed_core.application.features.common.dtos import CreateConsumerDto
from ed_core.documentation.api.abc_core_api_client import ConsumerDto
from ed_domain.common.exceptions import EXCEPTION_NAMES, ApplicationException
from ed_domain.core.entities.notification import NotificationType
from rmediator.decorators import request_handler
from rmediator.types import RequestHandler

from ed_gateway.application.common.responses.base_response import BaseResponse
from ed_gateway.application.contracts.infrastructure.api.abc_api import ABCApi
from ed_gateway.application.contracts.infrastructure.email.abc_email_templater import \
    ABCEmailTemplater
from ed_gateway.application.contracts.infrastructure.image_upload.abc_image_uploader import \
    ABCImageUploader
from ed_gateway.application.features.consumers.requests.commands import \
    CreateConsumerCommand
from ed_gateway.common.logging_helpers import get_logger

LOG = get_logger()


@request_handler(CreateConsumerCommand, BaseResponse[ConsumerDto])
class CreateConsumerCommandHandler(RequestHandler):
    def __init__(
        self,
        api_handler: ABCApi,
        image_uploader: ABCImageUploader,
        email_templater: ABCEmailTemplater,
    ):
        self._api_handler = api_handler
        self._image_uploader = image_uploader
        self._email_templater = email_templater

        self._success_message = "Consumer account created successfully"
        self._error_message = "Failed to create consumer account."

    async def handle(self, request: CreateConsumerCommand) -> BaseResponse[ConsumerDto]:
        dto = request.dto

        LOG.info(f"Calling auth create_get_otp API with request: {dto}")
        create_user_response = await self._api_handler.auth_api.create_get_otp(
            {
                "first_name": dto["first_name"],
                "last_name": dto["last_name"],
                "email": dto["email"],
                "phone_number": dto["phone_number"],
            }
        )

        LOG.info(
            "Received response from create_get_otp - success: %s",
            create_user_response.get("is_success"),
        )
        if not create_user_response["is_success"]:
            raise ApplicationException(
                EXCEPTION_NAMES[create_user_response["http_status_code"]],
                self._error_message,
                create_user_response["errors"],
            )

        user = create_user_response["data"]
        LOG.info(
            "Calling core create_consumer API for user: %s %s",
            dto.get("first_name"),
            dto.get("last_name"),
        )
        create_consumer_response = await self._api_handler.core_api.create_consumer(
            CreateConsumerDto(
                user_id=user["id"],
                first_name=dto["first_name"],
                last_name=dto["last_name"],
                phone_number=dto["phone_number"],
                email=dto["email"],
                location=dto["location"],
            ).model_dump()  # type: ignore
        )

        LOG.info(
            f"Received response from create_consumer: {create_consumer_response}")
        if create_consumer_response["is_success"] is False:
            await self._api_handler.auth_api.delete_user(
                create_user_response["data"]["id"]
            )
            raise ApplicationException(
                EXCEPTION_NAMES[create_consumer_response["http_status_code"]],
                self._error_message,
                create_consumer_response["errors"],
            )

        await self._api_handler.notification_api.send_notification(
            {
                "user_id": user["id"],
                "message": self._email_templater.welcome_consumer(dto["first_name"]),
                "notification_type": NotificationType.EMAIL,
            }
        )

        consumer = create_consumer_response["data"]
        return BaseResponse[ConsumerDto].success(self._success_message, consumer)
