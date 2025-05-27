from dataclasses import dataclass
from uuid import UUID

from ed_core.documentation.api.abc_core_api_client import DeliveryJobDto
from rmediator.decorators import request
from rmediator.mediator import Request

from ed_gateway.application.common.responses.base_response import BaseResponse


@request(BaseResponse[DeliveryJobDto])
@dataclass
class ClaimDeliveryJobCommand(Request):
    driver_id: UUID
    delivery_job_id: UUID
