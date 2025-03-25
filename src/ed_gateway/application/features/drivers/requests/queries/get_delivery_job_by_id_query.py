from dataclasses import dataclass
from uuid import UUID

from rmediator.decorators import request
from rmediator.mediator import Request

from ed_gateway.application.common.responses.base_response import BaseResponse
from ed_gateway.application.features.drivers.dtos.delivery_job_dto import DeliveryJobDto


@request(BaseResponse[DeliveryJobDto])
@dataclass
class GetDeliveryJobByIdQuery(Request):
    id: UUID
