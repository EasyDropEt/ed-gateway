from rmediator.decorators import request_handler
from rmediator.types import RequestHandler

from src.application.common.responses.base_response import BaseResponse
from src.application.contracts.infrastructure.persistence.abc_unit_of_work import (
    ABCUnitOfWork,
)
from src.application.features.business.dtos.order_dto import OrderDto
from src.application.features.business.requests.queries.get_orders_query import (
    GetOrdersQuery,
)
from src.common.logging_helpers import get_logger

LOG = get_logger()


@request_handler(GetOrdersQuery, BaseResponse[list[OrderDto]])
class GetOrdersQueryHandler(RequestHandler):
    def __init__(self, uow: ABCUnitOfWork):
        self._uow = uow

    async def handle(self, request: GetOrdersQuery) -> BaseResponse[list[OrderDto]]: ...
