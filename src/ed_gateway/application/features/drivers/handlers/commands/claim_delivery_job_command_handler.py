from ed_core.documentation.abc_core_api_client import DeliveryJobDto
from ed_domain.common.exceptions import ApplicationException, Exceptions
from rmediator.decorators import request_handler
from rmediator.types import RequestHandler

from ed_gateway.application.common.responses.base_response import BaseResponse
from ed_gateway.application.contracts.infrastructure.api.abc_api import ABCApi
from ed_gateway.application.features.drivers.requests.commands.claim_delivery_job_command import \
    ClaimDeliveryJobCommand
from ed_gateway.common.logging_helpers import get_logger

LOG = get_logger()


@request_handler(ClaimDeliveryJobCommand, BaseResponse[DeliveryJobDto])
class ClaimDeliveryJobCommandHandler(RequestHandler):
    def __init__(self, api: ABCApi):
        self._api = api

    async def handle(
        self, request: ClaimDeliveryJobCommand
    ) -> BaseResponse[DeliveryJobDto]:
        response = self._api.core_api.claim_delivery_job(
            str(request.driver_id), str(request.delivery_job_id)
        )
        if response["is_success"] is False:
            LOG.error(
                "Failed to claim delivery job.",
                request.driver_id,
                request.delivery_job_id,
                response["errors"],
            )
            raise ApplicationException(
                Exceptions.InternalServerException,
                "Failed to claim delivery job.",
                response["errors"],
            )

        return BaseResponse[DeliveryJobDto].success(
            "Delivery job claimed successfully.", response["data"]
        )
