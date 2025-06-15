from ed_core.documentation.api.abc_core_api_client import BusinessReportDto
from ed_domain.common.exceptions import EXCEPTION_NAMES, ApplicationException
from rmediator.decorators import request_handler
from rmediator.types import RequestHandler

from ed_gateway.application.common.responses.base_response import BaseResponse
from ed_gateway.application.contracts.infrastructure.api.abc_api import ABCApi
from ed_gateway.application.features.business.requests.queries import \
    GetBusinessReportQuery
from ed_gateway.common.logging_helpers import get_logger

LOG = get_logger()


@request_handler(GetBusinessReportQuery, BaseResponse[BusinessReportDto])
class GetBusinessReportQueryHandler(RequestHandler):
    def __init__(self, api: ABCApi):
        self._api = api

        self._error_message = "Failed to fetch report."
        self._success_message = "Report fetched successfully."

    async def handle(
        self, request: GetBusinessReportQuery
    ) -> BaseResponse[BusinessReportDto]:
        LOG.info(
            f"Calling core get_business_report API with business_id: {request.business_id}"
        )
        response = await self._api.core_api.get_business_report(
            str(request.business_id),
        )

        LOG.info(f"Received response from get_business_report: {response}")
        if response["is_success"] is False:
            raise ApplicationException(
                EXCEPTION_NAMES[response["http_status_code"]],
                self._error_message,
                response["errors"],
            )

        return BaseResponse[BusinessReportDto].success(
            self._success_message, response["data"]
        )
