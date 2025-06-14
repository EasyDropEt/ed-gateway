from dataclasses import dataclass
from uuid import UUID

from ed_core.documentation.api.abc_core_api_client import (OrderDto,
                                                           RateDeliveryDto)
from rmediator.decorators import request
from rmediator.mediator import Request

from ed_gateway.application.common.responses.base_response import BaseResponse


@request(BaseResponse[OrderDto])
@dataclass
class RateDeliveryCommand(Request):
    consumer_id: UUID
    order_id: UUID
    dto: RateDeliveryDto
