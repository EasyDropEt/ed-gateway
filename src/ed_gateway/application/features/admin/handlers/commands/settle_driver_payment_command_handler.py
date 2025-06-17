from ed_core.documentation.api.abc_core_api_client import \
    DriverPaymentSummaryDto
from ed_domain.common.exceptions import EXCEPTION_NAMES, ApplicationException
from rmediator.decorators import request_handler
from rmediator.types import RequestHandler

from ed_gateway.application.common.responses.base_response import BaseResponse
from ed_gateway.application.contracts.infrastructure.api.abc_api import ABCApi
from ed_gateway.application.features.admin.requests.commands import \
    SettleDriverPaymentCommand
from ed_gateway.common.logging_helpers import get_logger

LOG = get_logger()


@request_handler(SettleDriverPaymentCommand, BaseResponse[DriverPaymentSummaryDto])
class SettleDriverPaymentCommandHandler(RequestHandler):
    def __init__(
        self,
        api_handler: ABCApi,
    ):
        self._api_handler = api_handler

        self._success_message = "Driver payment settled successfully."
        self._error_message = "Failed to settle driver payment."

    async def handle(
        self, request: SettleDriverPaymentCommand
    ) -> BaseResponse[DriverPaymentSummaryDto]:
        dto = request.dto

        LOG.info(f"Calling auth update_admin API with request: {dto}")
        settle_driver_payment_response = (
            await self._api_handler.core_api.settle_driver_payment(
                str(request.admin_id), str(request.driver_id), request.dto
            )
        )

        LOG.info(
            "Received response from update_admin - success: %s",
            settle_driver_payment_response.get("is_success"),
        )
        if not settle_driver_payment_response["is_success"]:
            raise ApplicationException(
                EXCEPTION_NAMES[settle_driver_payment_response["http_status_code"]],
                self._error_message,
                settle_driver_payment_response["errors"],
            )

        driver_payment_summary = settle_driver_payment_response["data"]
        return BaseResponse[DriverPaymentSummaryDto].success(
            self._success_message, driver_payment_summary
        )
