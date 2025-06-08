from ed_core.documentation.api.abc_core_api_client import (CreateDriverDto,
                                                           DriverDto)
from ed_domain.common.exceptions import EXCEPTION_NAMES, ApplicationException
from rmediator.decorators import request_handler
from rmediator.types import RequestHandler

from ed_gateway.application.common.responses.base_response import BaseResponse
from ed_gateway.application.contracts.infrastructure.api.abc_api import ABCApi
from ed_gateway.application.contracts.infrastructure.image_upload.abc_image_uploader import \
    ABCImageUploader
from ed_gateway.application.features.drivers.requests.commands.create_driver_account_command import \
    CreateDriverAccountCommand
from ed_gateway.common.logging_helpers import get_logger

LOG = get_logger()


@request_handler(CreateDriverAccountCommand, BaseResponse[DriverDto])
class CreateDriverAccountCommandHandler(RequestHandler):
    def __init__(self, api_handler: ABCApi, image_uploader: ABCImageUploader):
        self._api_handler = api_handler
        self._image_uploader = image_uploader

    async def handle(
        self, request: CreateDriverAccountCommand
    ) -> BaseResponse[DriverDto]:
        LOG.info(
            f"Calling auth create_get_otp API with request: {request.dto}")
        create_user_response = await self._api_handler.auth_api.create_get_otp(
            {
                "first_name": request.dto["first_name"],
                "last_name": request.dto["last_name"],
                "email": request.dto["email"],
                "phone_number": request.dto["phone_number"],
                "password": request.dto["password"],
            }
        )

        LOG.info(
            f"Received response from create_get_otp: {create_user_response}")
        if not create_user_response["is_success"]:
            raise ApplicationException(
                EXCEPTION_NAMES[create_user_response["http_status_code"]],
                "Failed to create user account",
                create_user_response["errors"],
            )

        LOG.info(f"Calling core create_driver API with request: {request.dto}")
        create_driver_response = await self._api_handler.core_api.create_driver(
            CreateDriverDto(
                user_id=create_user_response["data"]["id"],
                first_name=request.dto["first_name"],
                last_name=request.dto["last_name"],
                profile_image="placeholder",
                phone_number=request.dto["phone_number"],
                email=request.dto["email"],
                location=request.dto["location"],
                car=request.dto["car"],
            )
        )

        LOG.info(
            f"Received response from create_driver: {create_driver_response}")
        if create_driver_response["is_success"] is False:
            await self._api_handler.auth_api.delete_user(
                create_user_response["data"]["id"]
            )
            raise ApplicationException(
                EXCEPTION_NAMES[create_driver_response["http_status_code"]],
                "Failed to create driver account",
                create_driver_response["errors"],
            )

        return BaseResponse[DriverDto].success(
            "Driver account created successfully", create_driver_response["data"]
        )
