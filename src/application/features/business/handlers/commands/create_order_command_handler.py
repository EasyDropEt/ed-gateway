from rmediator.decorators import request_handler
from rmediator.types import RequestHandler

from src.application.common.responses.base_response import BaseResponse
from src.application.contracts.infrastructure.persistence.abc_unit_of_work import (
    ABCUnitOfWork,
)
from src.application.features.business.dtos.order_dto import OrderDto
from src.application.features.business.requests.commands.create_order_command import (
    CreateOrderCommand,
)
from src.common.logging_helpers import get_logger

LOG = get_logger()


@request_handler(CreateOrderCommand, BaseResponse[OrderDto])
class CreateOrderCommandHandler(RequestHandler):
    def __init__(self, uow: ABCUnitOfWork):
        self._uow = uow

    async def handle(self, request: CreateOrderCommand) -> BaseResponse[OrderDto]: ...
