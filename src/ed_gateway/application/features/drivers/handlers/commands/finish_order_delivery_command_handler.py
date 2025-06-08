from ed_domain.common.exceptions import EXCEPTION_NAMES, ApplicationException
from rmediator.decorators import request_handler
from rmediator.types import RequestHandler

from ed_gateway.application.common.responses.base_response import BaseResponse
from ed_gateway.application.contracts.infrastructure.api.abc_api import ABCApi
from ed_gateway.application.features.drivers.requests.commands import \
    FinishOrderDeliveryCommand
from ed_gateway.common.logging_helpers import get_logger

LOG = get_logger()


@request_handler(FinishOrderDeliveryCommand, BaseResponse[None])
class FinishOrderDeliveryCommandHandler(RequestHandler):
    def __init__(self, api: ABCApi):
        self._api = api

    async def handle(self, request: FinishOrderDeliveryCommand) -> BaseResponse[None]:
        LOG.info(
            f"Calling core verify_order_drop_off API with driver_id: {request.driver_id}, "
            f"delivery_job_id: {request.delivery_job_id}, order_id: {request.order_id}, "
            f"dto: {request.dto}"
        )
        response = await self._api.core_api.finish_order_delivery(
            str(request.driver_id),
            str(request.delivery_job_id),
            str(request.order_id),
            request.dto,
        )

        LOG.info(f"Received response from verify_order_drop_off: {response}")
        if response["is_success"] is False:
            raise ApplicationException(
                EXCEPTION_NAMES[response["http_status_code"]],
                "Failed to verify drop off order.",
                response["errors"],
            )

        return BaseResponse[None].success(
            "Order drop off completed successfully.",
            None,
        )
