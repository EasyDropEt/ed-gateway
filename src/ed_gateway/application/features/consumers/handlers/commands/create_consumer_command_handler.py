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
from ed_gateway.application.service.api_service import ApiService
from ed_gateway.application.service.auth_api_service import AuthApiService
from ed_gateway.common.logging_helpers import get_logger

LOG = get_logger()


@request_handler(CreateConsumerCommand, BaseResponse[ConsumerDto])
class CreateConsumerCommandHandler(RequestHandler):
    def __init__(
        self,
        api: ABCApi,
        image_uploader: ABCImageUploader,
        email_templater: ABCEmailTemplater,
    ):
        self._api = api
        self._image_uploader = image_uploader
        self._email_templater = email_templater

        self._auth_service = AuthApiService(api.auth_api)

        self._success_message = "Consumer account created successfully"
        self._error_message = "Failed to create consumer account."

        self._api_service = ApiService(self._error_message)

    async def handle(self, request: CreateConsumerCommand) -> BaseResponse[ConsumerDto]:
        dto = request.dto
        user = await self._auth_service.create(
            {
                "first_name": dto["first_name"],
                "last_name": dto["last_name"],
                "email": dto["email"],
                "phone_number": dto["phone_number"],
            }
        )

        LOG.info("Calling core create_consumer API for user: %s %s")
        create_consumer = await self._api.core_api.create_consumer(
            {
                "user_id": user["id"],
                "first_name": dto["first_name"],
                "last_name": dto["last_name"],
                "phone_number": dto["phone_number"],
                "email": dto["email"],
                "location": dto["location"],
            }
        )

        LOG.info(f"Received response from create_consumer: {create_consumer}")
        self._api_service.basic_verify(create_consumer)
        if not create_consumer["is_success"]:
            await self._api.auth_api.delete_user(user["id"])
            self._api_service.verify(create_consumer)

        await self._api.notification_api.send_notification(
            {
                "user_id": user["id"],
                "message": self._email_templater.welcome_consumer(dto["first_name"]),
                "notification_type": NotificationType.EMAIL,
            }
        )

        consumer = create_consumer["data"]
        return BaseResponse[ConsumerDto].success(self._success_message, consumer)
