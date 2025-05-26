from ed_core.documentation.abc_core_api_client import DeliveryJobDto
from ed_domain.common.exceptions import ApplicationException, Exceptions
from rmediator.decorators import request_handler
from rmediator.types import RequestHandler

from ed_gateway.application.common.responses.base_response import BaseResponse
from ed_gateway.application.contracts.infrastructure.api.abc_api import ABCApi
from ed_gateway.application.features.drivers.requests.commands import \
    CancelDeliveryJobCommand
from ed_gateway.common.logging_helpers import get_logger

LOG = get_logger()


@request_handler(CancelDeliveryJobCommand, BaseResponse[DeliveryJobDto])
class CancelDeliveryJobCommandHandler(RequestHandler):
    def __init__(self, api: ABCApi):
        self._api = api

    async def handle(
        self, request: CancelDeliveryJobCommand
    ) -> BaseResponse[DeliveryJobDto]:
        LOG.info(
            f"Calling core cancel_delivery_job API with driver_id: {request.driver_id}, delivery_job_id: {request.delivery_job_id}"
        )
        response = self._api.core_api.cancel_delivery_job(
            str(request.driver_id), str(request.delivery_job_id)
        )

        LOG.info(f"Received response from cancel_delivery_job: {response}")
        if not response["is_success"]:
            raise ApplicationException(
                Exceptions.InternalServerException,
                "Failed to cancel delivery job.",
                response["errors"],
            )

        return BaseResponse[DeliveryJobDto].success(
            "Delivery job canceled successfully.", response["data"]
        )
