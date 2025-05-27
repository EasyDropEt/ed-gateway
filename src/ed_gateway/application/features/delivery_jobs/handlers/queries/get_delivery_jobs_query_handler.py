from ed_core.documentation.api.abc_core_api_client import DeliveryJobDto
from ed_domain.common.exceptions import EXCEPTION_NAMES, ApplicationException
from rmediator.decorators import request_handler
from rmediator.types import RequestHandler

from ed_gateway.application.common.responses.base_response import BaseResponse
from ed_gateway.application.contracts.infrastructure.api.abc_api import ABCApi
from ed_gateway.application.features.delivery_jobs.requests.queries import \
    GetDeliveryJobsQuery
from ed_gateway.common.logging_helpers import get_logger

LOG = get_logger()


@request_handler(GetDeliveryJobsQuery, BaseResponse[list[DeliveryJobDto]])
class GetDeliveryJobsQueryHandler(RequestHandler):
    def __init__(self, api: ABCApi):
        self._api = api

    async def handle(
        self, request: GetDeliveryJobsQuery
    ) -> BaseResponse[list[DeliveryJobDto]]:
        LOG.info(f"Calling core get_delivery_jobs API for request: {request}")
        response = self._api.core_api.get_delivery_jobs()

        LOG.info(f"Received response from get_delivery_jobs: {response}")
        if not response["is_success"]:
            LOG.error("Failed to fetch delivery jobs.")
            raise ApplicationException(
                EXCEPTION_NAMES[response["http_status_code"]],
                "Failed to fetch delivery jobs.",
                response["errors"],
            )

        return BaseResponse[list[DeliveryJobDto]].success(
            "Delivery jobs fetched successfully.", response["data"]
        )
