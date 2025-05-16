from ed_core.documentation.abc_core_api_client import DeliveryJobDto
from ed_domain.common.exceptions import ApplicationException, Exceptions
from rmediator.decorators import request_handler
from rmediator.types import RequestHandler

from ed_gateway.application.common.responses.base_response import BaseResponse
from ed_gateway.application.contracts.infrastructure.api.abc_api import ABCApi
from ed_gateway.application.features.drivers.requests.queries.get_driver_delivery_jobs_query import \
    GetDriverDeliveryJobsQuery
from ed_gateway.common.logging_helpers import get_logger

LOG = get_logger()


@request_handler(GetDriverDeliveryJobsQuery, BaseResponse[list[DeliveryJobDto]])
class GetDriverDeliveryJobsQueryHandler(RequestHandler):
    def __init__(self, api: ABCApi):
        self._api = api

    async def handle(
        self, request: GetDriverDeliveryJobsQuery
    ) -> BaseResponse[list[DeliveryJobDto]]:
        response = self._api.core_api.get_driver_delivery_jobs(str(request.driver_id))

        if not response["is_success"]:
            LOG.error(
                "Failed to fetch delivery jobs for driver %s: %s",
                request.driver_id,
                response["errors"],
            )
            raise ApplicationException(
                Exceptions.InternalServerException,
                "Failed to fetch delivery jobs.",
                response["errors"],
            )

        return BaseResponse[list[DeliveryJobDto]].success(
            "Delivery jobs fetched successfully.", response["data"]
        )
