from rmediator.decorators import request_handler
from rmediator.types import RequestHandler

from src.application.common.responses.base_response import BaseResponse
from src.application.contracts.infrastructure.api.abc_api import ABCApi
from src.application.features.drivers.dtos.driver_account_dto import \
    DriverAccountDto
from src.application.features.drivers.requests.commands.create_driver_account_command import \
    CreateDriverAccountCommand
from src.common.exception_helpers import ApplicationException, Exceptions
from src.common.logging_helpers import get_logger

LOG = get_logger()


@request_handler(CreateDriverAccountCommand, BaseResponse[DriverAccountDto])
class CreateDriverAccountCommandHandler(RequestHandler):
    def __init__(self, api_handler: ABCApi):
        self._api_handler = api_handler

    async def handle(
        self, request: CreateDriverAccountCommand
    ) -> BaseResponse[DriverAccountDto]:
        LOG.info("Handling CreateDriverAccountCommand")
        create_user_response = self._api_handler.auth_api.create_get_otp({
            "first_name": request.dto['first_name'],
            "last_name": request.dto['last_name'],
            "email": request.dto['email'],
            "phone_number": request.dto['phone_number'],
            'password': request.dto['password']
        })
        if not create_user_response['is_success']:
            raise ApplicationException(
                Exceptions.InternalServerException,
                "Failed to create user account",
                create_user_response['errors']
            )

        create_driver_response = self._api_handler.core_api.create_driver({
            "user_id": create_user_response['data']['id'],
            "first_name": request.dto['first_name'],
            "last_name":  request.dto['last_name'],
            "profile_image": request.dto['profile_image'],
            "phone_number": request.dto['phone_number'],
            "email": request.dto['email'],
            "location": request.dto['location'],
            "car": request.dto['car']
        })
        if create_driver_response['is_success'] is False:
            self._api_handler.auth_api.delete_user(create_user_response['data']['id'])
            raise ApplicationException(
                Exceptions.InternalServerException,
                "Failed to create driver account",
                create_driver_response['errors']
            )

        return BaseResponse[DriverAccountDto].success(
            "Driver account created successfully", create_driver_response['data']
        )

