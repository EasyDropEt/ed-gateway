from rmediator.decorators import request_handler
from rmediator.types import RequestHandler

from src.application.common.responses.base_response import BaseResponse
from src.application.contracts.infrastructure.persistence.abc_unit_of_work import (
    ABCUnitOfWork,
)
from src.application.features.business.dtos import BusinessAccountDto
from src.application.features.business.requests.commands import LoginBusinessCommand
from src.common.logging_helpers import get_logger

LOG = get_logger()


@request_handler(LoginBusinessCommand, BaseResponse[BusinessAccountDto])
class LoginBusinessCommandHandler(RequestHandler):
    def __init__(self, uow: ABCUnitOfWork):
        self._uow = uow

    async def handle(
        self, request: LoginBusinessCommand
    ) -> BaseResponse[BusinessAccountDto]: ...
