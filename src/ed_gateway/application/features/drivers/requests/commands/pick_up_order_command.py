from dataclasses import dataclass
from uuid import UUID

from ed_core.documentation.abc_core_api_client import PickUpOrderDto
from rmediator.decorators import request
from rmediator.mediator import Request

from ed_gateway.application.common.responses.base_response import BaseResponse


@request(BaseResponse[PickUpOrderDto])
@dataclass
class PickUpOrderCommand(Request):
    driver_id: UUID
    delivery_job_id: UUID
    order_id: UUID
