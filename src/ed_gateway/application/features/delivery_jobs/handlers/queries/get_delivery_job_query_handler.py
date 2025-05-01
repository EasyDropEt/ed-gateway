from ed_core.documentation.abc_core_api_client import DeliveryJobDto
from ed_domain.common.exceptions import ApplicationException, Exceptions
from rmediator.decorators import request_handler
from rmediator.types import RequestHandler

from ed_gateway.application.common.responses.base_response import BaseResponse
from ed_gateway.application.contracts.infrastructure.api.abc_api import ABCApi
from ed_gateway.application.features.delivery_jobs.requests.queries.get_delivery_job_query import \
    GetDeliveryJobQuery
from ed_gateway.common.logging_helpers import get_logger

LOG = get_logger()


@request_handler(GetDeliveryJobQuery, BaseResponse[DeliveryJobDto])
class GetDeliveryJobQueryHandler(RequestHandler):
    def __init__(self, api: ABCApi):
        self._api = api

    async def handle(
        self, request: GetDeliveryJobQuery
    ) -> BaseResponse[DeliveryJobDto]:
        response = self._api.core_api.get_delivery_job(
            str(request.delivery_job_id))

        if not response["is_success"]:
            LOG.error(
                "Failed to fetch driver.",
                request.delivery_job_id,
                response["errors"],
            )
            raise ApplicationException(
                Exceptions.InternalServerException,
                "Driver not found.",
                response["errors"],
            )

        return BaseResponse[DeliveryJobDto].success(
            "Delivery job fetched successfully.", response["data"]
        )
