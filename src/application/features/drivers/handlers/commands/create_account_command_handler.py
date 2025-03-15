from rmediator.decorators import request_handler
from rmediator.types import RequestHandler

from src.application.common.responses.base_response import BaseResponse
from src.application.contracts.infrastructure.api.abc_api import ABCApi
from src.application.features.drivers.dtos.driver_account_dto import \
    DriverAccountDto
from src.application.features.drivers.requests.commands.create_driver_account_command import \
    CreateDriverAccountCommand
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
        response = self._api_handler.core_api.create_driver(request.dto)

        if response['is_success'] is False:
            return BaseResponse[DriverAccountDto].error(
                "Failed to create driver account", response['errors']
            )

        return BaseResponse[DriverAccountDto].success(
            "Driver accoutn created successfully", response['data']
        )

