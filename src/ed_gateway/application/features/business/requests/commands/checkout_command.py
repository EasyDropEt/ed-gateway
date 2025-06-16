from dataclasses import dataclass

from ed_core.documentation.api.abc_core_api_client import OrderDto
from rmediator.decorators import request
from rmediator.mediator import Request

from ed_gateway.application.common.responses.base_response import BaseResponse
from ed_gateway.application.features.business.dtos import CreateOrderDto


@request(BaseResponse[OrderDto])
@dataclass
class CheckoutCommand(Request):
    api_key: str
    dto: CreateOrderDto
