from ed_core.application.features.common.dtos import TrackOrderDto
from ed_domain.common.exceptions import ApplicationException, Exceptions
from rmediator.decorators import request_handler
from rmediator.types import RequestHandler

from ed_gateway.application.common.responses.base_response import BaseResponse
from ed_gateway.application.contracts.infrastructure.api.abc_api import ABCApi
from ed_gateway.application.features.order.requests.queries import \
    TrackOrderQuery
from ed_gateway.common.logging_helpers import get_logger

LOG = get_logger()


@request_handler(TrackOrderQuery, BaseResponse[TrackOrderDto])
class TrackOrderQueryHandler(RequestHandler):
    def __init__(self, api: ABCApi):
        self._api = api

    async def handle(self, request: TrackOrderQuery) -> BaseResponse[TrackOrderDto]:
        response = self._api.core_api.track_order(
            str(request.order_id),
        )
        if response["is_success"] is False:
            raise ApplicationException(
                Exceptions.InternalServerException,
                "Failed to fetch orders.",
                response["errors"],
            )

        return BaseResponse[TrackOrderDto].success(
            "Orders fetched successfully.", response["data"]
        )
