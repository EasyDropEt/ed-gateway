from ed_core.documentation.api.abc_core_api_client import ConsumerDto
from ed_domain.common.exceptions import ApplicationException, Exceptions
from rmediator.decorators import request_handler
from rmediator.types import RequestHandler

from ed_gateway.application.common.responses.base_response import BaseResponse
from ed_gateway.application.contracts.infrastructure.api.abc_api import ABCApi
from ed_gateway.application.contracts.infrastructure.image_upload.abc_image_uploader import \
    ABCImageUploader
from ed_gateway.application.features.consumers.requests.commands import \
    CreateConsumerCommand
from ed_gateway.common.logging_helpers import get_logger

LOG = get_logger()


@request_handler(CreateConsumerCommand, BaseResponse[ConsumerDto])
class CreateConsumerCommandHandler(RequestHandler):
    def __init__(self, api_handler: ABCApi, image_uploader: ABCImageUploader):
        self._api_handler = api_handler
        self._image_uploader = image_uploader

    async def handle(self, request: CreateConsumerCommand) -> BaseResponse[ConsumerDto]:
        LOG.info(
            f"Calling auth create_get_otp API with request: {request.dto}")
        create_user_response = self._api_handler.auth_api.create_get_otp(
            {
                "first_name": request.dto["first_name"],
                "last_name": request.dto["last_name"],
                "email": request.dto["email"],
                "phone_number": request.dto["phone_number"],
            }
        )

        LOG.info("Received response from create_get_otp - success: %s",
                 create_user_response.get("is_success"))
        if not create_user_response["is_success"]:
            raise ApplicationException(
                Exceptions.InternalServerException,
                "Failed to create consumer account.",
                create_user_response["errors"],
            )

        LOG.info("Calling core create_consumer API for user: %s %s",
                 request.dto.get("first_name"), request.dto.get("last_name"))
        create_consumer_response = self._api_handler.core_api.create_consumer(
            {
                "user_id": create_user_response["data"]["id"],
                "first_name": request.dto["first_name"],
                "last_name": request.dto["last_name"],
                "phone_number": request.dto["phone_number"],
                "email": request.dto["email"],
                "location": request.dto["location"],
            }
        )

        LOG.info(
            f"Received response from create_consumer: {create_consumer_response}")
        if create_consumer_response["is_success"] is False:
            self._api_handler.auth_api.delete_user(
                create_user_response["data"]["id"])
            raise ApplicationException(
                Exceptions.InternalServerException,
                "Failed to create consumer account",
                create_consumer_response["errors"],
            )

        return BaseResponse[ConsumerDto].success(
            "Consumer account created successfully", create_consumer_response["data"]
        )
