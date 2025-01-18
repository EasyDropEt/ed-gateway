from rmediator.decorators import request_handler
from rmediator.types import RequestHandler

from src.application.common.responses.base_response import BaseResponse
from src.application.contracts.infrastructure.persistence.abc_unit_of_work import (
    ABCUnitOfWork,
)
from src.application.features.drivers.dtos.driver_account_dto import DriverAccountDto
from src.application.features.drivers.requests.commands.login_driver_command import (
    LoginDriverCommand,
)
from src.common.logging_helpers import get_logger

LOG = get_logger()

DRIVERS_DB = {}


@request_handler(LoginDriverCommand, BaseResponse[DriverAccountDto])
class LoginDriverCommandHandler(RequestHandler):
    def __init__(self, uow: ABCUnitOfWork):
        self._uow = uow

    async def handle(
        self, request: LoginDriverCommand
    ) -> BaseResponse[DriverAccountDto]: ...
