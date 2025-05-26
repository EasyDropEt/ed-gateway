from ed_core.documentation.abc_core_api_client import DriverPaymentSummaryDto
from ed_domain.common.exceptions import ApplicationException, Exceptions
from rmediator.decorators import request_handler
from rmediator.types import RequestHandler

from ed_gateway.application.common.responses.base_response import BaseResponse
from ed_gateway.application.contracts.infrastructure.api.abc_api import ABCApi
from ed_gateway.application.features.drivers.requests.queries import \
    GetDriverPaymentSummaryQuery
from ed_gateway.common.logging_helpers import get_logger

LOG = get_logger()


@request_handler(GetDriverPaymentSummaryQuery, BaseResponse[DriverPaymentSummaryDto])
class GetDriverPaymentSummaryQueryHandler(RequestHandler):
    def __init__(self, api: ABCApi):
        self._api = api

    async def handle(
        self, request: GetDriverPaymentSummaryQuery
    ) -> BaseResponse[DriverPaymentSummaryDto]:
        response = self._api.core_api.get_driver_payment_summary(str(request.driver_id))

        if not response["is_success"]:
            LOG.error(
                "Failed to fetch driver payment summary for driver %s: %s",
                request.driver_id,
                response["errors"],
            )
            raise ApplicationException(
                Exceptions.InternalServerException,
                "Failed to fetch driver payment summary.",
                response["errors"],
            )

        return BaseResponse[DriverPaymentSummaryDto].success(
            "Driver payment summary fetched successfully.", response["data"]
        )
