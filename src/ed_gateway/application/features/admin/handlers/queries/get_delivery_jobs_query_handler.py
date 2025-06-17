from ed_core.documentation.api.abc_core_api_client import DeliveryJobDto
from ed_domain.common.exceptions import EXCEPTION_NAMES, ApplicationException
from rmediator.decorators import request_handler
from rmediator.types import RequestHandler

from ed_gateway.application.common.responses.base_response import BaseResponse
from ed_gateway.application.contracts.infrastructure.api.abc_api import ABCApi
from ed_gateway.application.features.admin.requests.queries import \
    GetDeliveryJobsQuery
from ed_gateway.common.logging_helpers import get_logger

LOG = get_logger()


@request_handler(GetDeliveryJobsQuery, BaseResponse[list[DeliveryJobDto]])
class GetDeliveryJobsQueryHandler(RequestHandler):
    def __init__(self, api: ABCApi):
        self._api = api

        self._success_message = "DeliveryJobs fetched successfully."
        self._error_message = "Failed to fetch delivery jobs."

    async def handle(
        self, request: GetDeliveryJobsQuery
    ) -> BaseResponse[list[DeliveryJobDto]]:
        LOG.info("Calling core get_delivery_jobs API")
        response = await self._api.core_api.get_delivery_jobs()

        LOG.info(f"Received response from get_delivery_job: {response}")
        if not response["is_success"]:
            raise ApplicationException(
                EXCEPTION_NAMES[response["http_status_code"]],
                self._error_message,
                response["errors"],
            )

        return BaseResponse[list[DeliveryJobDto]].success(
            self._success_message, response["data"]
        )
