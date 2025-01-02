from rmediator.decorators import request_handler
from rmediator.types import RequestHandler

from src.application.common.responses.base_response import BaseResponse
from src.application.contracts.infrastructure.persistence.abc_unit_of_work import (
    ABCUnitOfWork,
)
from src.application.features.drivers.dtos.delivery_job_dto import DeliveryJobDto
from src.application.features.drivers.requests.queries.get_delivery_job_by_id_query import (
    GetDeliveryJobByIdQuery,
)
from src.common.logging_helpers import get_logger

LOG = get_logger()


@request_handler(GetDeliveryJobByIdQuery, BaseResponse[DeliveryJobDto])
class GetDeliveryJobByIdQueryHandler(RequestHandler):
    def __init__(self, uow: ABCUnitOfWork):
        self._uow = uow

    async def handle(
        self, request: GetDeliveryJobByIdQuery
    ) -> BaseResponse[DeliveryJobDto]: ...
