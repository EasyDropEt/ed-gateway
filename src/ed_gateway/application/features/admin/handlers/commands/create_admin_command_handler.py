from ed_core.documentation.api.abc_core_api_client import AdminDto
from ed_domain.common.exceptions import EXCEPTION_NAMES, ApplicationException
from rmediator.decorators import request_handler
from rmediator.types import RequestHandler

from ed_gateway.application.common.responses.base_response import BaseResponse
from ed_gateway.application.contracts.infrastructure.api.abc_api import ABCApi
from ed_gateway.application.contracts.infrastructure.email.abc_email_templater import \
    ABCEmailTemplater
from ed_gateway.application.contracts.infrastructure.image_upload.abc_image_uploader import \
    ABCImageUploader
from ed_gateway.application.features.admin.requests.commands import \
    CreateAdminCommand
from ed_gateway.application.service.auth_api_service import AuthApiService
from ed_gateway.common.logging_helpers import get_logger

LOG = get_logger()


@request_handler(CreateAdminCommand, BaseResponse[AdminDto])
class CreateAdminCommandHandler(RequestHandler):
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

        self._success_message = "Admin account created successfully"
        self._error_message = "Failed to create admin account."

    async def handle(self, request: CreateAdminCommand) -> BaseResponse[AdminDto]:
        dto = request.dto

        user = await self._auth_service.create(
            {
                "first_name": dto["first_name"],
                "last_name": dto["last_name"],
                "email": dto["email"],
                "phone_number": dto["phone_number"],
                "password": dto["password"],
            }
        )

        LOG.info("Calling core create_admin API for user: %s", user["id"])
        create_admin_response = await self._api.core_api.create_admin(
            {
                "user_id": user["id"],
                "first_name": dto["first_name"],
                "last_name": dto["last_name"],
                "phone_number": dto["phone_number"],
                "email": dto["email"],
                "role": dto["role"],
            }
        )

        LOG.info(
            f"Received response from create_admin: {create_admin_response}")
        if create_admin_response["is_success"] is False:
            await self._api.auth_api.delete_user(user["id"])
            raise ApplicationException(
                EXCEPTION_NAMES[create_admin_response["http_status_code"]],
                self._error_message,
                create_admin_response["errors"],
            )

        admin = create_admin_response["data"]
        return BaseResponse[AdminDto].success(self._success_message, admin)
